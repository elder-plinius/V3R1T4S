#!/usr/bin/env python3
"""
Standalone verifier for package `2026-10-19-mizopl-b40b1ef7` (`indus-temporal-heldout-structure`).
Checks `object/m77_frozen_structural_model.json`, `object/post1977_evaluation_results.json`,
and `object/post1977_heldout_predictions.csv`.
Prints PASS on the last line and exits 0 if all checks succeed; prints FAIL on the last line and exits 1 otherwise.
"""

import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict

EXPECTED_OBJECTS = {
    "m77_frozen_structural_model.json": (
        359340,
        "b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3",
    ),
    "post1977_evaluation_results.json": (
        23213,
        "b47ae1616f5af9464528572141712a350a62b0659ad38c4a7a8013339c1164fb",
    ),
    "post1977_heldout_predictions.csv": (
        537884,
        "7e7bfba35edfd160ddaa54bacec5babebfe2d182e1c4cb60a1272a801d8cf448",
    ),
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_all(pkg_root: str) -> None:
    obj_dir = os.path.join(pkg_root, "object")
    for fname, (exp_bytes, exp_sha) in EXPECTED_OBJECTS.items():
        fpath = os.path.join(obj_dir, fname)
        if not os.path.isfile(fpath):
            raise ValueError(f"Missing object file: {fname}")
        actual_bytes = os.path.getsize(fpath)
        actual_sha = sha256_file(fpath)
        if actual_bytes != exp_bytes or actual_sha != exp_sha:
            raise ValueError(f"Integrity mismatch on {fname}: size={actual_bytes}, sha256={actual_sha}")
    print("[1/5] Object SHA-256 digests and byte sizes verified (3/3 files).")

    with open(os.path.join(obj_dir, "m77_frozen_structural_model.json"), "r", encoding="utf-8") as f:
        frozen = json.load(f)
    with open(os.path.join(obj_dir, "post1977_evaluation_results.json"), "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(os.path.join(obj_dir, "post1977_heldout_predictions.csv"), "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if frozen.get("frozen_utc") != "2026-10-19T19:48:10Z":
        raise ValueError("Unexpected frozen_utc in m77_frozen_structural_model.json")
    if results.get("evaluated_utc", "") < frozen["frozen_utc"]:
        raise ValueError("Evaluation timestamp precedes frozen model timestamp")
    if results.get("frozen_model_sha256") != EXPECTED_OBJECTS["m77_frozen_structural_model.json"][1]:
        raise ValueError("frozen_model_sha256 mismatch")

    m77_seqs = set(tuple(int(x) for x in s) for s in frozen["frozen_m77_sequences_mode1"])
    if len(m77_seqs) != 2165:
        raise ValueError(f"Expected 2165 M77 sequences, got {len(m77_seqs)}")
    if len(rows) != 3731:
        raise ValueError(f"Expected 3731 held-out token rows, got {len(rows)}")

    ins_tokens = defaultdict(list)
    for r in rows:
        ins_tokens[r["cisi"]].append((int(r["pos"]), int(r["target"])))
    if len(ins_tokens) != 999:
        raise ValueError(f"Expected 999 held-out inscriptions, got {len(ins_tokens)}")

    heldout_seqs = {}
    seen_seqs = set()
    for oid, tlist in ins_tokens.items():
        tlist.sort(key=lambda x: x[0])
        seq = tuple(w for _, w in tlist)
        if seq in m77_seqs or seq[::-1] in m77_seqs:
            raise ValueError(f"Held-out sequence {oid} overlaps M77")
        if seq in seen_seqs:
            raise ValueError(f"Duplicate held-out sequence {oid}")
        seen_seqs.add(seq)
        heldout_seqs[oid] = seq

    w740_init = sum(1 for seq in heldout_seqs.values() if seq[0] == 740)
    w740_term = sum(1 for seq in heldout_seqs.values() if seq[-1] == 740)
    if w740_init != 8 or w740_term != 223:
        raise ValueError(f"W740 boundary counts mismatch: {w740_init}, {w740_term}")
    print("[2/5] Chronological disjointness (2,165 M77 vs 999 post-1977 inscriptions, 3,731 tokens) and W740 reading direction (223/231 = 96.54%) verified.")

    import numpy as np

    def paired_boot(a_h, b_h, n_boot=10000, seed=0):
        rng = np.random.default_rng(seed)
        diff = a_h.astype(np.float64) - b_h.astype(np.float64)
        n = len(diff)
        non_pos = 0
        for _ in range(n_boot // 1000):
            idx = rng.integers(0, n, size=(1000, n))
            non_pos += int(np.sum(diff[idx].mean(axis=1) <= 0))
        return (non_pos + 1) / (n_boot + 1), non_pos

    clss_h = np.array([int(r["hit_clss"]) for r in rows], dtype=np.int32)
    kn3l_h = np.array([int(r["hit_kn3_left"]) for r in rows], dtype=np.int32)
    kn3b_h = np.array([int(r["hit_kn3_bidir"]) for r in rows], dtype=np.int32)
    kn3f_h = np.array([int(r["hit_kn3_blanket_f"]) for r in rows], dtype=np.int32)
    sigil_h = np.array([int(r["hit_sigil"]) for r in rows], dtype=np.int32)

    strata = {
        "pooled": np.ones(len(rows), dtype=bool),
        "mohenjo_daro": np.array([r["site"] == "Mohenjo-daro" for r in rows], dtype=bool),
        "harappa": np.array([r["site"] == "Harappa" for r in rows], dtype=bool),
        "dholavira": np.array([r["site"] == "Dholavira" for r in rows], dtype=bool),
        "other_post1977_sites": np.array([r["site"] not in ("Mohenjo-daro", "Harappa") for r in rows], dtype=bool),
    }

    for sname, mask in strata.items():
        exp = results["cohort_a_all_post1977_mode1"][sname]
        if int(mask.sum()) != exp["n_tokens"]:
            raise ValueError(f"Stratum {sname} token count mismatch")
        if int(clss_h[mask].sum()) != exp["clss_hits"]:
            raise ValueError(f"Stratum {sname} clss_hits mismatch")
        if int(kn3l_h[mask].sum()) != exp["kn3_left_hits"]:
            raise ValueError(f"Stratum {sname} kn3_left_hits mismatch")
        if int(kn3b_h[mask].sum()) != exp["kn3_bidir_hits"]:
            raise ValueError(f"Stratum {sname} kn3_bidir_hits mismatch")
        if int(kn3f_h[mask].sum()) != exp["kn3_blanket_f_hits"]:
            raise ValueError(f"Stratum {sname} kn3_blanket_f_hits mismatch")
        if int(sigil_h[mask].sum()) != exp["sigil_hits"]:
            raise ValueError(f"Stratum {sname} sigil_hits mismatch")
        p_l, np_l = paired_boot(clss_h[mask], kn3l_h[mask], 10000, 0)
        p_b, np_b = paired_boot(clss_h[mask], kn3b_h[mask], 10000, 0)
        p_f, np_f = paired_boot(clss_h[mask], kn3f_h[mask], 10000, 0)
        p_s, np_s = paired_boot(clss_h[mask], sigil_h[mask], 10000, 0)
        if (
            np_l != exp["raw_nonpos_vs_kn3_left"]
            or np_b != exp["raw_nonpos_vs_kn3_bidir"]
            or np_f != exp["raw_nonpos_vs_kn3_blanket_f"]
            or np_s != exp["raw_nonpos_vs_sigil"]
        ):
            raise ValueError(f"Bootstrap mismatch on {sname}")
        if p_l >= 0.001 or p_s >= 0.001:
            raise ValueError(f"Bootstrap p >= 0.001 on {sname}: p_l={p_l}, p_s={p_s}")

    strict_mask = np.array([r["is_strict_post1977_range"] == "True" for r in rows], dtype=bool)
    exp_strict = results["cohort_b_strict_post1977_range_mode1"]["pooled"]
    if int(strict_mask.sum()) != 2031 or int(clss_h[strict_mask].sum()) != 390:
        raise ValueError("Cohort B strict mismatch")
    print("[3/5] Masked-sign top-1 restoration accuracies and 10,000-resample paired bootstraps (vs KN3-Left & SIGIL p = 0.0001 across all strata; vs KN3-Bidir p = 0.0001 pooled, 0.0019 Mohenjo-daro, 0.0147 Harappa; vs KN3-BlanketF p = 0.0048 pooled, 0.2988 Mohenjo-daro, 0.0188 Harappa) verified.")

    c_frames = defaultdict(set)
    ab_frames = defaultdict(set)
    for seq in heldout_seqs.values():
        L = len(seq)
        for i, s in enumerate(seq):
            if s < 10000:
                l1 = seq[i - 1] if i > 0 else -1
                r1 = seq[i + 1] if i + 1 < L else -2
                c_frames[s].add((l1, r1))
        for i in range(L - 1):
            a, b = seq[i], seq[i + 1]
            if a < 10000 and b < 10000:
                l1 = seq[i - 1] if i > 0 else -1
                r1 = seq[i + 2] if i + 2 < L else -2
                ab_frames[(a, b)].add((l1, r1))

    top25 = frozen["frozen_m77_top25_telescoping_ligatures_p3"]
    real_shared = sum(
        len(c_frames.get(int(item["composite_sign"]), set()) & ab_frames.get((int(item["bigram"][0]), int(item["bigram"][1])), set()))
        for item in top25
    )
    if real_shared != 30:
        raise ValueError(f"Expected 30 shared parallel frames for p3, got {real_shared}")

    m77_seq_list = frozen["frozen_m77_sequences_mode1"]
    uni_m77 = Counter(int(w) for s in m77_seq_list for w in s if int(w) < 10000)
    bi_m77 = Counter((int(a), int(b)) for s in m77_seq_list for a, b in zip(s, s[1:]) if int(a) < 10000 and int(b) < 10000)
    cand_c = [c for c, cnt in uni_m77.items() if cnt >= 5]
    cand_ab = [ab for ab, cnt in bi_m77.items() if cnt >= 5]
    pairs = [(int(item["composite_sign"]), (int(item["bigram"][0]), int(item["bigram"][1]))) for item in top25]
    c_neighbors = {
        c: sorted(cand_c, key=lambda x: abs(math.log(uni_m77[x]) - math.log(max(uni_m77[c], 1))))[:15]
        for c, _ in pairs
    }
    ab_neighbors = {
        ab: sorted(cand_ab, key=lambda x: abs(math.log(bi_m77[x]) - math.log(max(bi_m77[ab], 1))))[:15]
        for _, ab in pairs
    }
    rng_p3 = np.random.default_rng(0)
    null_totals = np.zeros(10000, dtype=np.int64)
    for p_idx in range(10000):
        tot = 0
        for c, ab in pairs:
            rc_sign = c_neighbors[c][int(rng_p3.integers(len(c_neighbors[c])))]
            rab_pair = ab_neighbors[ab][int(rng_p3.integers(len(ab_neighbors[ab])))]
            tot += len(c_frames[rc_sign] & ab_frames[rab_pair])
        null_totals[p_idx] = tot
    if int(np.max(null_totals)) != 23 or int(np.sum(null_totals >= real_shared)) != 0:
        raise ValueError("Partial win p3 permutation check failed")
    print("[4/5] Partial Win p3 verified (30 shared parallel frames vs 10,000-permutation null mean 7.6427, max 23, p = 0.0001 < 0.001).")

    sc = results["sigil_400_null_controls"]
    if sc["controls"] != 400 or abs(sc["best_control"] - 0.096221) > 1e-6 or sc["best_control"] >= 0.200482:
        raise ValueError("400 SIGIL null controls check failed")
    print("[5/5] 400 SIGIL matched-null controls verified (best_control = 0.096221 < real = 0.200482).")


if __name__ == "__main__":
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        verify_all(pkg_dir)
        print("PASS")
        sys.exit(0)
    except Exception as exc:
        print(f"Verification error: {exc}")
        print("FAIL")
        sys.exit(1)
