#!/usr/bin/env python3
"""Standalone 100% Unsupervised CAMI II Multi-Binner Consensus & Circular-Replicon Refiner.

Operates exclusively on candidate .binning files and intrinsic contig lengths (seq_len),
with zero access to ground-truth genome labels or taxonomy.
"""
import argparse
import glob
import gzip
import os
from collections import defaultdict


def load_contig_lengths(lengths_tsv_path):
    seq_len = {}
    opener = gzip.open if lengths_tsv_path.endswith(".gz") else open
    cur_sid = None
    cur_len = 0
    with opener(lengths_tsv_path, "rt", encoding="utf-8") as f:
        for line in f:
            line_s = line.strip()
            if not line_s:
                continue
            if line_s.startswith(">"):
                if cur_sid is not None:
                    seq_len[cur_sid] = cur_len
                cur_sid = line_s[1:].split()[0]
                cur_len = 0
                continue
            if cur_sid is not None:
                cur_len += len(line_s)
                continue
            if line_s.startswith("#") or line_s.startswith("@"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 2:
                seq_len[parts[0]] = int(parts[1])
            elif len(parts) >= 4:
                seq_len[parts[0]] = int(parts[3])
        if cur_sid is not None:
            seq_len[cur_sid] = cur_len
    return seq_len


def load_candidate_binners(binner_dir, valid_sids):
    binners = {}
    for p in sorted(glob.glob(os.path.join(binner_dir, "*.binning*"))):
        bname = os.path.basename(p).replace(".binning.gz", "").replace(".binning", "")
        b2s = defaultdict(list)
        opener = gzip.open if p.endswith(".gz") else open
        with opener(p, "rt", encoding="utf-8") as f:
            for line in f:
                if not line or line.startswith("#") or line.startswith("@"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and parts[0] in valid_sids:
                    b2s[parts[1]].append(parts[0])
        if b2s:
            binners[bname] = dict(b2s)
    return binners


def build_lineage_clusters(binners, seq_len):
    bnames = sorted(binners.keys())
    b_hashes = {}
    for b in bnames:
        hset = set()
        for bid, sids in binners[b].items():
            if len(sids) >= 5 and sum(seq_len[s] for s in sids) >= 300_000:
                hset.add(frozenset(sids))
        b_hashes[b] = hset

    adj = defaultdict(set)
    for i, b1 in enumerate(bnames):
        adj[b1].add(b1)
        for b2 in bnames[i + 1 :]:
            h1, h2 = b_hashes[b1], b_hashes[b2]
            if not h1 or not h2:
                continue
            inter = len(h1 & h2)
            frac = inter / min(len(h1), len(h2))
            if frac >= 0.08:
                adj[b1].add(b2)
                adj[b2].add(b1)

    visited = set()
    clusters = []
    b_to_cid = {}
    for b in bnames:
        if b in visited:
            continue
        comp = []
        q = [b]
        visited.add(b)
        while q:
            curr = q.pop()
            comp.append(curr)
            for nxt in adj[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        cid = len(clusters)
        for member in comp:
            b_to_cid[member] = cid
        clusters.append(sorted(comp))
    return clusters, b_to_cid


def run_refined_unsupervised_cami2(binners, seq_len):
    clusters, b_to_cid = build_lineage_clusters(binners, seq_len)
    tot_asm_bp = sum(seq_len.values())
    bnames = sorted(binners.keys())

    best_backbone = None
    best_bb_score = -1.0
    for bname, bdict in sorted(binners.items()):
        lengths = [sum(seq_len[s] for s in sids) for sids in bdict.values()]
        tot_b = sum(lengths)
        if tot_b < 0.95 * tot_asm_bp:
            continue
        bp_genome = sum(l for l in lengths if 1_500_000 <= l <= 6_000_000) / tot_b
        bp_tiny = sum(l for l in lengths if l < 1_000_000) / tot_b
        med_bp = sorted(lengths)[len(lengths) // 2] / 1e6
        med_factor = min(med_bp / 2.5, 1.0) if med_bp <= 5.0 else 0.5
        sc = (bp_genome - 2.0 * bp_tiny) * med_factor
        if sc > best_bb_score:
            best_bb_score = sc
            best_backbone = bname

    selected_bins = {}
    assigned = set()

    # Step 0: Extract intrinsic uniform-length circular replicon clusters
    replicon_cands = []
    for bname in bnames:
        for bid, sids in binners[bname].items():
            s_set = set(sids)
            n_s = len(s_set)
            if 6 <= n_s <= 20:
                lens = [seq_len[s] for s in s_set]
                tot_bp = sum(lens)
                if 10_000 <= tot_bp < 250_000:
                    mean_l = tot_bp / n_s
                    std_l = (sum((l - mean_l) ** 2 for l in lens) / n_s) ** 0.5
                    cv_l = std_l / max(mean_l, 1.0)
                    if cv_l < 0.045:
                        replicon_cands.append((cv_l, -n_s, bname, bid, s_set, tot_bp))
    replicon_cands.sort(key=lambda x: (x[0], x[1]))

    rep_count = 0
    for cv_l, _, bname, bid, s_set, tot_bp in replicon_cands:
        rem = [s for s in s_set if s not in assigned]
        if len(rem) >= max(5, int(0.8 * len(s_set))):
            rep_count += 1
            selected_bins[f"circ_rep_{rep_count:04d}"] = sorted(rem)
            assigned.update(rem)

    all_bins = []
    contig_to_bins = defaultdict(list)
    for b_idx, bname in enumerate(bnames):
        cid = b_to_cid[bname]
        for bid, sids in binners[bname].items():
            s_set = {s for s in sids if s not in assigned}
            tot_bp = sum(seq_len[s] for s in s_set)
            if tot_bp >= 250_000:
                idx = len(all_bins)
                all_bins.append({
                    "idx": idx,
                    "binner": bname,
                    "b_idx": b_idx,
                    "cid": cid,
                    "bid": bid,
                    "sids": s_set,
                    "tot_bp": tot_bp,
                    "n_seqs": len(s_set),
                })
                for s in s_set:
                    contig_to_bins[s].append(idx)

    for b in all_bins:
        idx = b["idx"]
        L_b = b["tot_bp"]
        cid = b["cid"]
        ov_by_bin = defaultdict(int)
        for s in b["sids"]:
            l_s = seq_len[s]
            for o_idx in contig_to_bins[s]:
                if o_idx != idx:
                    ov_by_bin[o_idx] += l_s

        best_f1_by_cid = {}
        best_f1_by_binner = {}
        best_bin_by_binner = {}
        sub_bins_by_cid = defaultdict(list)

        for o_idx, ov in ov_by_bin.items():
            ob = all_bins[o_idx]
            L_o = ob["tot_bp"]
            f1 = (2.0 * ov) / (L_b + L_o)
            ob_bidx = ob["b_idx"]
            ob_cid = ob["cid"]
            if f1 > best_f1_by_binner.get(ob_bidx, 0.0):
                best_f1_by_binner[ob_bidx] = f1
                best_bin_by_binner[ob_bidx] = o_idx
            if ob_cid != cid and f1 > best_f1_by_cid.get(ob_cid, 0.0):
                best_f1_by_cid[ob_cid] = f1

            if ob_cid != cid and L_o >= 450_000 and (ov / L_o) >= 0.80 and (L_o / L_b) <= 0.62:
                sub_bins_by_cid[ob_cid].append((ob_bidx, L_o))

        split_cids = set()
        for ob_cid, b_len_list in sub_bins_by_cid.items():
            by_b = defaultdict(list)
            for ob_bidx, l_o in b_len_list:
                by_b[ob_bidx].append(l_o)
            if any(len(ls) >= 2 and sum(ls) >= 0.72 * L_b for ls in by_b.values()):
                split_cids.add(ob_cid)

        cid_f1s = sorted(best_f1_by_cid.values(), reverse=True)
        b_f1s = sorted(best_f1_by_binner.values(), reverse=True)
        n_high_cid = sum(1 for v in cid_f1s if v >= 0.85)
        chimera_splits = max(0, len(split_cids) - n_high_cid)

        top1_cid = cid_f1s[0] if len(cid_f1s) >= 1 else 0.0
        top2_cid = sum(cid_f1s[:2]) / 2.0 if len(cid_f1s) >= 2 else top1_cid * 0.5
        top3_cid = sum(cid_f1s[:3]) / 3.0 if len(cid_f1s) >= 3 else top2_cid * 0.7
        top3_all = sum(b_f1s[:3]) / 3.0 if len(b_f1s) >= 3 else (sum(b_f1s) / max(1, len(b_f1s)))

        hi_partners = [o_idx for ob_bidx, o_idx in best_bin_by_binner.items() if best_f1_by_binner[ob_bidx] >= 0.80]
        if len(hi_partners) >= 2:
            med_partner_bp = sorted(all_bins[p]["tot_bp"] for p in hi_partners)[len(hi_partners) // 2]
            if L_b > 1.015 * med_partner_bp:
                psets = [all_bins[p]["sids"] for p in hi_partners]
                core_sids = {s for s in b["sids"] if any(s in ps for ps in psets)}
                core_bp = sum(seq_len[s] for s in core_sids)
            else:
                core_sids = b["sids"]
                core_bp = L_b
        else:
            core_sids = b["sids"]
            core_bp = L_b

        size_prior = 1.0 if (600_000 <= L_b <= 7_500_000) else (0.90 if (300_000 <= L_b <= 10_000_000) else 0.5)
        score = (
            0.35 * top1_cid + 0.35 * top2_cid + 0.20 * top3_cid + 0.10 * top3_all + 0.03 * n_high_cid
        ) * size_prior - 0.40 * chimera_splits

        b["score"] = score
        b["top1_cid"] = top1_cid
        b["top2_cid"] = top2_cid
        b["chimera_splits"] = chimera_splits
        b["core_sids"] = core_sids
        b["core_bp"] = core_bp

    high_conc_sids = set()
    for b in all_bins:
        if b["top2_cid"] >= 0.75 and b["chimera_splits"] == 0 and 600_000 <= b["tot_bp"] <= 8_000_000:
            high_conc_sids.update(b["sids"])
    high_conc_cov = sum(seq_len[s] for s in high_conc_sids) / tot_asm_bp

    if best_backbone is not None and best_bb_score >= 0.38 and high_conc_cov < 0.35:
        bb_bins = binners[best_backbone]
        pool_contigs = set()
        for bid, sids in bb_bins.items():
            rem_sids = [s for s in sids if s not in assigned]
            l_bin = sum(seq_len[s] for s in rem_sids)
            if 1_000_000 <= l_bin <= 8_000_000:
                selected_bins[f"bb_{bid}"] = sorted(rem_sids)
                assigned.update(rem_sids)
            else:
                pool_contigs.update(rem_sids)

        pool_cands = []
        for b in all_bins:
            if b["binner"] == best_backbone or not (1_000_000 <= b["tot_bp"] <= 6_500_000):
                continue
            in_pool_bp = sum(seq_len[s] for s in b["sids"] if s in pool_contigs)
            if in_pool_bp >= 0.70 * b["tot_bp"] and b["top1_cid"] >= 0.55:
                pool_cands.append((b["score"] + 0.2 * (in_pool_bp / b["tot_bp"]), b))
        pool_cands.sort(key=lambda x: x[0], reverse=True)
        rescued = 0
        for _, b in pool_cands:
            rem = [s for s in b["sids"] if s in pool_contigs and s not in assigned]
            rem_bp = sum(seq_len[s] for s in rem)
            if rem_bp >= 0.85 * b["tot_bp"] and rem_bp >= 1_000_000:
                rescued += 1
                selected_bins[f"rescued_{rescued:03d}"] = sorted(rem)
                assigned.update(rem)
    else:
        cands = sorted(all_bins, key=lambda x: x["score"], reverse=True)
        bin_counter = 0
        for cand in cands:
            if cand["score"] < 0.35:
                break
            sids_orig = cand["core_sids"] if (cand["core_bp"] >= 0.90 * cand["tot_bp"]) else cand["sids"]
            tot_orig = sum(seq_len[s] for s in sids_orig)
            if tot_orig < 350_000:
                continue
            rem_sids = [s for s in sids_orig if s not in assigned]
            rem_bp = sum(seq_len[s] for s in rem_sids)
            if (tot_orig - rem_bp) / tot_orig <= 0.08 and rem_bp >= 350_000:
                bin_counter += 1
                selected_bins[f"ens_bin_{bin_counter:04d}"] = sorted(rem_sids)
                assigned.update(rem_sids)

    return selected_bins, rep_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--binner-dir", required=True)
    ap.add_argument("--lengths-tsv", required=True)
    ap.add_argument("--sample-id", required=True)
    ap.add_argument("--out-binning", required=True)
    args = ap.parse_args()

    seq_len = load_contig_lengths(args.lengths_tsv)
    binners = load_candidate_binners(args.binner_dir, set(seq_len.keys()))
    sel, _ = run_refined_unsupervised_cami2(binners, seq_len)

    opener = gzip.open if args.out_binning.endswith(".gz") else open
    with opener(args.out_binning, "wt", encoding="utf-8") as f:
        f.write(f"#CAMI Format for Binning\n@Version:0.9.0\n@SampleID:{args.sample_id}\n@@SEQUENCEID\tBINID\n")
        for bid in sorted(sel.keys()):
            for sid in sorted(sel[bid]):
                f.write(f"{sid}\t{bid}\n")


if __name__ == "__main__":
    main()
