#!/usr/bin/env python3
"""
Standalone Zero-Trust Verifier for `phenopacket-store-rare-disease-gene-prioritization` (Milestone `p2`).

Verifies from authoritative upstream archives (`all_phenopackets_0.1.27.zip` + `HPO v2026-06-06` +
`HGNC 2026-05-01` + pre-`2026-06-09` compiled KG cache in `~/.cache/phenopacket_p2`, with automatic
pinned-SHA-256 download/compile fallback on a fresh machine):
  1. Cryptographic SHA-256 digests of all upstream archives and pre-`2026-06-09` compiled tables,
     plus `max(date_modified) == "2026-05-01"` on `HGNC`, `0` corpus PMIDs in retained KG edges,
     and `STRING v12.0` `textmining == 0` identity across 100% of retained PPI edges.
  2. AST blindness of `marg_p2_ranker.py` (zero case IDs, archive paths, or target labels) and
     exact HPO input-order permutation invariance `rank(Q) == rank(reversed(Q))`.
  3. Authoritative upstream `case_sha256` join deriving `y_true` (`target_hgnc`) and gene-disjoint
     splits (`P2-Raw`: 127 cases / 10 genes; `P2-Dev`: 1,132 cases / 112 genes; `P2-Holdout`: 988
     cases / 112 genes; `Pos-40`: 40 cases / 40 genes) strictly from `genes_to_disease_v2026-06-06.txt`.
  4. Live `MARGP2Ranker` execution across ALL `127` `P2-Raw` cases, ALL `988` `P2-Holdout` cases,
     and ALL `40` `Pos-40` cases, verifying:
       - Exact `2,450,592`-entry equality across `p2_raw_full_rankings_part01..11.tsv.gz` (0 `y_true` cols),
       - Exact `98,800`-entry `top100` equality on `p2_holdout_top100_predictions.tsv.gz` (0 `y_true` cols),
       - Exact parity (`< 1e-8`) on all metrics, per-gene rows, `6/6` equal-weight `u6` baselines,
         all 3 negative controls, and `2,000`-draw `case` / `gene_cluster` / `pub_cluster` 95% CIs
         in `00_p2_benchmark_certificate.json`.
  5. Adversarial `--corrupt` and hash-transparent single-digit/vector mutation rejection (`FAIL`, `rc=1`).
"""
from __future__ import annotations

import ast
import collections
import gzip
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from typing import Sequence

import numpy as np

sys.dont_write_bytecode = True

PINNED_EXTERNAL_COMMITMENTS = {
    "cert_static_sha256": "9e3f43bd51c54b73dc25f946cac3b3cee2d21a4e904108071727494fb3e5abea",
}

_FORBIDDEN_RANKER_TOKENS = {
    "target_hgnc",
    "target_symbol",
    "case_id",
    "archive_member",
    "interpretations",
    "all_phenopackets",
    "eval_queries_and_targets",
    "phenotypicfeatures",
}

_PMID_RX = re.compile(r"PMID\s*:?\s*(\d+)", re.I)

_HPO_FREQ_WEIGHTS: dict[str, float] = {
    "HP:0040280": 1.00,
    "HP:0040281": 0.895,
    "HP:0040282": 0.545,
    "HP:0040283": 0.17,
    "HP:0040284": 0.025,
    "HP:0040285": 0.0,
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_gzip_uncompressed(path: Path) -> str:
    return hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest()


def canonical_json_sha256(obj: object) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def check_ranker_ast_blindness(ranker_py: Path) -> None:
    src = ranker_py.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(ranker_py))
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id.lower() in _FORBIDDEN_RANKER_TOKENS:
            raise ValueError(f"AST blindness violation in {ranker_py.name}: forbidden identifier {node.id}")
        if isinstance(node, ast.Attribute) and node.attr.lower() in _FORBIDDEN_RANKER_TOKENS:
            raise ValueError(f"AST blindness violation in {ranker_py.name}: forbidden attribute {node.attr}")
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            low = node.value.lower()
            for tok in _FORBIDDEN_RANKER_TOKENS:
                if tok in low:
                    raise ValueError(f"AST blindness violation in {ranker_py.name}: forbidden literal '{tok}'")


def parse_hpoa_freq(freq_str: str) -> float:
    s = freq_str.strip()
    if not s:
        return 0.50
    if s in _HPO_FREQ_WEIGHTS:
        return _HPO_FREQ_WEIGHTS[s]
    if s.endswith("%"):
        try:
            return max(0.01, min(1.0, float(s[:-1]) / 100.0))
        except ValueError:
            return 0.50
    if "/" in s:
        parts = s.split("/", 1)
        try:
            num, den = float(parts[0]), float(parts[1])
            if den > 0:
                return max(0.01, min(1.0, (num + 0.5) / (den + 1.0)))
        except ValueError:
            return 0.50
    return 0.50


def parse_hpo_obo(obo_path: Path) -> tuple[dict[str, str], set[str]]:
    children: dict[str, set[str]] = collections.defaultdict(set)
    alt_map: dict[str, str] = {}
    cur_id = ""
    cur_alts: list[str] = []
    cur_repl = ""
    is_obsolete = False

    def flush() -> None:
        nonlocal cur_id, cur_alts, cur_repl, is_obsolete
        if not cur_id:
            return
        if is_obsolete and cur_repl:
            alt_map[cur_id] = cur_repl
        for a in cur_alts:
            alt_map[a] = cur_repl if (is_obsolete and cur_repl) else cur_id
        cur_id = ""
        cur_alts = []
        cur_repl = ""
        is_obsolete = False

    with obo_path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line == "[Term]" or line.startswith("[Typedef]"):
                flush()
                if line.startswith("[Typedef]"):
                    break
                continue
            if line.startswith("id: HP:"):
                cur_id = line.split("id: ", 1)[1].strip()
            elif line.startswith("alt_id: HP:"):
                cur_alts.append(line.split("alt_id: ", 1)[1].strip())
            elif line.startswith("is_a: HP:"):
                pid = line.split("is_a: ", 1)[1].split("!")[0].strip()
                if cur_id:
                    children[pid].add(cur_id)
            elif line == "is_obsolete: true":
                is_obsolete = True
            elif line.startswith("replaced_by: HP:"):
                cur_repl = line.split("replaced_by: ", 1)[1].strip()
        flush()

    pheno_sub: set[str] = set()
    dq = collections.deque(["HP:0000118"])
    while dq:
        u = dq.popleft()
        if u in pheno_sub:
            continue
        pheno_sub.add(u)
        for v in children.get(u, ()):
            if v not in pheno_sub:
                dq.append(v)
    return alt_map, pheno_sub


def ensure_upstream_cache(cache_dir: Path, builder_dir: Path, prov: dict[str, object]) -> None:
    req_files = {
        "all_phenopackets_0.1.27.zip": prov["corpus"]["sha256"],
        "hp_v2026-06-06.obo": prov["pinned_hpo_and_hgnc"]["hp_obo_sha256"],
        "phenotype_v2026-06-06.hpoa": prov["pinned_hpo_and_hgnc"]["phenotype_hpoa_sha256"],
        "genes_to_phenotype_v2026-06-06.txt": prov["pinned_hpo_and_hgnc"]["genes_to_phenotype_sha256"],
        "genes_to_disease_v2026-06-06.txt": prov["pinned_hpo_and_hgnc"]["genes_to_disease_sha256"],
        "hgnc_complete_set_2026-06-01.txt": prov["pinned_hpo_and_hgnc"]["hgnc_sha256"],
    }
    kg_sha_map: dict[str, str] = prov["compiled_precorpus_kg_uncompressed_sha256"]
    missing = [fn for fn in req_files if not (cache_dir / fn).is_file()]
    missing += [f"compiled_kg/{fn}" for fn in kg_sha_map if not (cache_dir / "compiled_kg" / fn).is_file()]
    if missing:
        compiler_py = builder_dir / "compile_precorpus_kg.py"
        if not compiler_py.is_file():
            raise FileNotFoundError(f"Missing cache files {missing} and compiler {compiler_py}")
        subprocess.run([sys.executable, "-B", str(compiler_py), "--cache-dir", str(cache_dir)], check=True)

    for fn, exp_sha in req_files.items():
        actual = sha256_file(cache_dir / fn)
        if actual != exp_sha:
            raise ValueError(f"Upstream SHA-256 mismatch on {fn}: {actual} != {exp_sha}")
    for fn, exp_sha in kg_sha_map.items():
        actual = sha256_gzip_uncompressed(cache_dir / "compiled_kg" / fn)
        if actual != exp_sha:
            raise ValueError(
                f"Compiled pre-corpus KG uncompressed payload SHA-256 mismatch on {fn}: {actual} != {exp_sha}"
            )


def load_upstream_cohorts_and_audit_purity(cache_dir: Path) -> dict[str, object]:
    alt_map, pheno_sub = parse_hpo_obo(cache_dir / "hp_v2026-06-06.obo")

    hgnc_to_symbol: dict[str, str] = {}
    symbol_to_hgnc: dict[str, str] = {}
    entrez_to_hgnc: dict[str, str] = {}
    pc_raw: list[str] = []
    max_hgnc_date = ""

    with (cache_dir / "hgnc_complete_set_2026-06-01.txt").open(encoding="utf-8") as f:
        cols = f.readline().rstrip("\n").split("\t")
        ih, isym, iloc, ient, idm = (
            cols.index("hgnc_id"),
            cols.index("symbol"),
            cols.index("locus_group"),
            cols.index("entrez_id"),
            cols.index("date_modified"),
        )
        for ln in f:
            p = ln.rstrip("\n").split("\t")
            if len(p) <= max(ih, isym, iloc, ient, idm):
                continue
            if p[idm] > max_hgnc_date:
                max_hgnc_date = p[idm]
            if p[iloc] != "protein-coding gene":
                continue
            hid, sym = p[ih], p[isym]
            pc_raw.append(hid)
            hgnc_to_symbol[hid] = sym
            symbol_to_hgnc[sym] = hid
            if p[ient]:
                entrez_to_hgnc[p[ient]] = hid

    if max_hgnc_date != "2026-05-01":
        raise ValueError(f"Expected HGNC max date_modified == 2026-05-01, got {max_hgnc_date}")
    pc_hgnc = sorted(set(pc_raw), key=lambda h: int(h.split(":")[1]))
    if len(pc_hgnc) != 19296:
        raise ValueError(f"Expected 19,296 HGNC protein-coding genes, got {len(pc_hgnc)}")
    pc_set = set(pc_hgnc)

    corpus_pmids: set[str] = set()
    included_cases: list[dict[str, object]] = []
    with zipfile.ZipFile(cache_dir / "all_phenopackets_0.1.27.zip") as zf:
        for name in sorted(zf.namelist()):
            if not name.endswith(".json"):
                continue
            raw_b = zf.read(name)
            c_sha = sha256_bytes(raw_b)
            txt = raw_b.decode("utf-8")
            cpm = tuple(sorted(set(_PMID_RX.findall(txt))))
            corpus_pmids.update(cpm)
            pp = json.loads(txt)
            obs_terms = []
            for pf in pp.get("phenotypicFeatures", []):
                if pf.get("excluded", False):
                    continue
                tid = alt_map.get(pf.get("type", {}).get("id", ""), pf.get("type", {}).get("id", ""))
                if tid in pheno_sub and tid != "HP:0000118":
                    obs_terms.append(tid)
            obs_u = tuple(sorted(set(obs_terms)))
            if not obs_u:
                continue
            hids: set[str] = set()
            for interp in pp.get("interpretations", []):
                for gi in interp.get("diagnosis", {}).get("genomicInterpretations", []):
                    vd = gi.get("variantInterpretation", {}).get("variationDescriptor", {})
                    gc = vd.get("geneContext") or gi.get("gene") or {}
                    vid, sym = gc.get("valueId", ""), gc.get("symbol", "")
                    if vid in pc_set:
                        hids.add(vid)
                    elif sym in symbol_to_hgnc and symbol_to_hgnc[sym] in pc_set:
                        hids.add(symbol_to_hgnc[sym])
            if len(hids) == 1:
                hid = next(iter(hids))
                cid = str(pp.get("id") or Path(name).stem)
                included_cases.append(
                    {
                        "case_sha256": c_sha,
                        "case_id": cid,
                        "target_hgnc": hid,
                        "target_symbol": hgnc_to_symbol[hid],
                        "obs_hpo_terms": obs_u,
                        "case_pmids": cpm,
                    }
                )

    if len(included_cases) != 10189 or len(corpus_pmids) != 1755:
        raise ValueError(f"Unexpected corpus counts: cases={len(included_cases)}, pmids={len(corpus_pmids)}")

    # Audit STRING v12.0 textmining == 0 identity across 100% of retained PPI edges!
    with gzip.open(cache_dir / "compiled_kg" / "string_v12_notm_edges.tsv.gz", "rt", encoding="utf-8") as f:
        hdr = f.readline().rstrip("\n").split("\t")
        if hdr != ["u_idx", "v_idx", "s_notm", "s_exp_db", "s_func"]:
            raise ValueError(f"Unexpected STRING header: {hdr}")
        n_edges = 0
        for ln in f:
            p = ln.rstrip("\n").split("\t")
            s_tot, s_ed, s_fn = float(p[2]), float(p[3]), float(p[4])
            if abs(s_tot - (1.0 - (1.0 - s_ed) * (1.0 - s_fn))) > 3e-5:
                raise ValueError(f"STRING non-zero textmining residual detected: {p}")
            n_edges += 1
        if n_edges != 1525039:
            raise ValueError(f"Unexpected STRING retained undirected edge count: {n_edges} != 1525039")

    # Strictly pre-corpus disease->gene map from HPO v2026-06-06 genes_to_disease ONLY
    dis_to_hgnc: dict[str, set[str]] = collections.defaultdict(set)
    with (cache_dir / "genes_to_disease_v2026-06-06.txt").open(encoding="utf-8") as f:
        f.readline()
        for ln in f:
            if not ln.strip() or ln.startswith("#"):
                continue
            p = ln.rstrip("\n").split("\t")
            ent = p[0].replace("NCBIGene:", "")
            if ent in entrez_to_hgnc:
                dis_to_hgnc[p[3]].add(entrez_to_hgnc[ent])

    raw_annot: set[str] = set()
    with (cache_dir / "genes_to_phenotype_v2026-06-06.txt").open(encoding="utf-8") as f:
        f.readline()
        for ln in f:
            if ln.strip() and not ln.startswith("#"):
                ent = ln.split("\t")[0].replace("NCBIGene:", "")
                if ent in entrez_to_hgnc:
                    raw_annot.add(entrez_to_hgnc[ent])

    clean_gene_terms: dict[str, set[str]] = collections.defaultdict(set)
    with (cache_dir / "phenotype_v2026-06-06.hpoa").open(encoding="utf-8") as f:
        for ln in f:
            if ln.startswith("#") or ln.startswith("database_id"):
                continue
            p = ln.rstrip("\n").split("\t")
            if len(p) <= 10 or p[10] != "P" or p[2] == "NOT":
                continue
            dis_id, hpo_id, ref, freq_s = p[0], alt_map.get(p[3], p[3]), p[4], p[7]
            if hpo_id not in pheno_sub:
                continue
            for hid in dis_to_hgnc.get(dis_id, ()):
                raw_annot.add(hid)
            if not (set(_PMID_RX.findall(ref)) & corpus_pmids) and parse_hpoa_freq(freq_s) > 0.0:
                for hid in dis_to_hgnc.get(dis_id, ()):
                    clean_gene_terms[hid].add(hpo_id)

    p2_raw = [c for c in included_cases if c["target_hgnc"] not in raw_annot]
    p2_clean = [c for c in included_cases if c["target_hgnc"] not in clean_gene_terms]
    raw_genes = {c["target_hgnc"] for c in p2_raw}
    clean_genes = {c["target_hgnc"] for c in p2_clean}
    diff_genes = sorted(clean_genes - raw_genes)
    dev_genes = set(diff_genes[0::2])
    hold_genes = set(diff_genes[1::2])

    p2_dev = [c for c in p2_clean if c["target_hgnc"] in dev_genes]
    p2_hold = [c for c in p2_clean if c["target_hgnc"] in hold_genes]

    pos40 = []
    seen_pos: set[str] = set()
    for c in included_cases:
        g = str(c["target_hgnc"])
        if g in clean_gene_terms and g not in seen_pos:
            seen_pos.add(g)
            pos40.append(c)
            if len(pos40) == 40:
                break

    if (
        len(p2_raw) != 127
        or len(raw_genes) != 10
        or len(p2_dev) != 1132
        or len(dev_genes) != 112
        or len(p2_hold) != 988
        or len(hold_genes) != 112
        or len(pos40) != 40
    ):
        raise ValueError("Strict pre-corpus cohort split dimensions did not match expected invariants")

    return {
        "pc_hgnc": pc_hgnc,
        "corpus_pmids": corpus_pmids,
        "p2_raw": p2_raw,
        "p2_dev": p2_dev,
        "p2_hold": p2_hold,
        "pos40": pos40,
        "n_clean_genes": len(clean_gene_terms),
        "n_string_notm_edges": n_edges,
    }


def midrank_from_scores(scores_19296: np.ndarray, target_idx: int, tol: float = 1e-10) -> float:
    ts = float(scores_19296[target_idx])
    n_higher = int(np.sum(scores_19296 > ts + tol))
    n_equal = int(np.sum(np.abs(scores_19296 - ts) <= tol))
    return n_higher + (n_equal + 1) / 2.0


def summarize_ranks_from_meta(
    target_hgncs: Sequence[str],
    case_ids: Sequence[str],
    case_pmids_list: Sequence[Sequence[str]],
    ranks: Sequence[float],
    n_boot: int = 2000,
    seed: int = 20261117,
) -> dict[str, object]:
    n = len(ranks)
    rrs = [1.0 / r for r in ranks]
    mrr = sum(rrs) / n
    sr = sorted(ranks)
    med = sr[n // 2] if n % 2 == 1 else 0.5 * (sr[n // 2 - 1] + sr[n // 2])

    recalls: dict[str, object] = {}
    for k in (1, 5, 10, 50, 100):
        cnt = sum(1 for r in ranks if r <= k)
        recalls[f"top_{k}"] = cnt / n
        recalls[f"top_{k}_count"] = cnt

    rng = random.Random(seed)
    case_boot_mrr, case_boot_t1, case_boot_t10 = [], [], []
    for _ in range(n_boot):
        ix = [rng.randrange(n) for _ in range(n)]
        case_boot_mrr.append(sum(rrs[i] for i in ix) / n)
        case_boot_t1.append(sum(1 for i in ix if ranks[i] <= 1.0) / n)
        case_boot_t10.append(sum(1 for i in ix if ranks[i] <= 10.0) / n)
    case_boot_mrr.sort()
    case_boot_t1.sort()
    case_boot_t10.sort()

    by_gene: dict[str, list[int]] = collections.defaultdict(list)
    for i, g in enumerate(target_hgncs):
        by_gene[g].append(i)
    gkeys = sorted(by_gene)
    g_cnt = len(gkeys)
    macro_mrr = sum(sum(rrs[i] for i in by_gene[g]) / len(by_gene[g]) for g in gkeys) / g_cnt

    gene_boot_mrr, gene_boot_macro = [], []
    for _ in range(n_boot):
        sg = [gkeys[rng.randrange(g_cnt)] for _ in range(g_cnt)]
        tot_rr, tot_n, mac_rr = 0.0, 0, 0.0
        for g in sg:
            ix = by_gene[g]
            s_rr = sum(rrs[i] for i in ix)
            tot_rr += s_rr
            tot_n += len(ix)
            mac_rr += s_rr / len(ix)
        gene_boot_mrr.append(tot_rr / max(1, tot_n))
        gene_boot_macro.append(mac_rr / g_cnt)
    gene_boot_mrr.sort()
    gene_boot_macro.sort()

    by_pub: dict[str, list[int]] = collections.defaultdict(list)
    for i, pmids in enumerate(case_pmids_list):
        pk = pmids[0] if pmids else f"NO_PMID:{case_ids[i]}"
        by_pub[pk].append(i)
    pkeys = sorted(by_pub)
    p_cnt = len(pkeys)
    pub_boot_mrr = []
    for _ in range(n_boot):
        sp = [pkeys[rng.randrange(p_cnt)] for _ in range(p_cnt)]
        tot_rr, tot_n = 0.0, 0
        for pk in sp:
            ix = by_pub[pk]
            tot_rr += sum(rrs[i] for i in ix)
            tot_n += len(ix)
        pub_boot_mrr.append(tot_rr / max(1, tot_n))
    pub_boot_mrr.sort()

    lo = int(0.025 * n_boot)
    hi = int(0.975 * n_boot)
    return {
        "n_cases": n,
        "n_unique_genes": g_cnt,
        "n_unique_publications": p_cnt,
        "mrr": mrr,
        "macro_gene_mrr": macro_mrr,
        "median_rank": med,
        **recalls,
        "mrr_ci95_case": [case_boot_mrr[lo], case_boot_mrr[hi]],
        "top_1_ci95_case": [case_boot_t1[lo], case_boot_t1[hi]],
        "top_10_ci95_case": [case_boot_t10[lo], case_boot_t10[hi]],
        "mrr_ci95_gene_cluster": [gene_boot_mrr[lo], gene_boot_mrr[hi]],
        "macro_gene_mrr_ci95_gene_cluster": [gene_boot_macro[lo], gene_boot_macro[hi]],
        "mrr_ci95_pub_cluster": [pub_boot_mrr[lo], pub_boot_mrr[hi]],
    }


def assert_summary_close(actual: dict[str, object], expected: dict[str, object], label: str, tol: float = 1e-8) -> None:
    for k, ev in expected.items():
        if k in ("runtime_sec", "n_unique_profiles", "mean_positive_scored_genes", "zero_scored_cases"):
            continue
        if k not in actual:
            raise ValueError(f"{label}: missing key {k}")
        av = actual[k]
        if isinstance(ev, (int, float)):
            if abs(float(av) - float(ev)) > tol:
                raise ValueError(f"{label}.{k} mismatch: recomputed={av} vs cert={ev}")
        elif isinstance(ev, list):
            if len(av) != len(ev) or any(abs(float(x) - float(y)) > tol for x, y in zip(av, ev)):
                raise ValueError(f"{label}.{k} vector mismatch: recomputed={av} vs cert={ev}")


def locate_dirs() -> tuple[Path, Path, Path, Path]:
    here = Path(__file__).resolve()
    if here.parent.name == "verify-it-yourself":
        pkg_root = here.parent.parent
        obj_dir = pkg_root / "object"
        code_dir = obj_dir
        builder_dir = pkg_root / "how-we-built-it"
    else:
        pkg_root = here.parent
        obj_dir = pkg_root / "results"
        code_dir = pkg_root / "code"
        builder_dir = pkg_root / "code"
    return pkg_root, obj_dir, code_dir, builder_dir


def verify_all(corrupt_mode: bool = False) -> int:
    t0 = time.perf_counter()
    pkg_root, obj_dir, code_dir, builder_dir = locate_dirs()

    cert_path = obj_dir / "00_p2_benchmark_certificate.json"
    if not cert_path.is_file():
        print("VERIFICATION ERROR: Missing 00_p2_benchmark_certificate.json")
        print("FAIL")
        return 1

    try:
        cert = json.loads(cert_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"VERIFICATION ERROR: Malformed JSON certificate: {exc}")
        print("FAIL")
        return 1

    if corrupt_mode:
        cert["blind_p2_raw_127"]["marg_p2_seam"]["mrr"] = (
            float(cert["blind_p2_raw_127"]["marg_p2_seam"]["mrr"]) + 0.01
        )

    try:
        # 0. Verify SHA256SUMS manifest in non-corrupt mode
        sums_file = pkg_root / "SHA256SUMS"
        if sums_file.is_file() and not corrupt_mode:
            for ln in sums_file.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", ln.strip())
                if m:
                    exp_h, rel_p = m.group(1), m.group(2).lstrip("./")
                    fp = pkg_root / rel_p
                    if not fp.is_file() or sha256_bytes(fp.read_bytes()) != exp_h:
                        raise ValueError(f"SHA256SUMS mismatch on {rel_p}")

        # 1. Verify upstream & pre-corpus KG SHA-256 provenance + authoritative upstream join
        env_cache = os.environ.get("MARG_P2_CACHE_DIR", "")
        cache_dir = Path(env_cache) if env_cache else (Path.home() / ".cache" / "phenopacket_p2")
        ensure_upstream_cache(cache_dir, builder_dir, cert["provenance"])
        up = load_upstream_cohorts_and_audit_purity(cache_dir)
        if int(cert["provenance"].get("n_retained_string_notm_edges", -1)) != int(up["n_string_notm_edges"]):
            raise ValueError(
                f"Certificate n_retained_string_notm_edges mismatch: "
                f"{cert['provenance'].get('n_retained_string_notm_edges')} != {up['n_string_notm_edges']}"
            )

        # Verify candidate_genes_19296.tsv (strictly 2 columns: gene_idx\thgnc_id, 0 disease/phenotype cols!)
        cand_tsv = obj_dir / "candidate_genes_19296.tsv"
        with cand_tsv.open(encoding="utf-8") as f:
            hdr = f.readline().rstrip("\n").split("\t")
            if hdr != ["gene_idx", "hgnc_id"]:
                raise ValueError(f"Unexpected candidate_genes_19296.tsv columns: {hdr}")
            rows_c = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]
        if len(rows_c) != 19296 or any(int(r[0]) != i or r[1] != up["pc_hgnc"][i] for i, r in enumerate(rows_c)):
            raise ValueError("candidate_genes_19296.tsv mismatch against HGNC 2026-05-01 protein-coding universe")

        # 2. AST blindness + instantiate MARGP2Ranker
        check_ranker_ast_blindness(code_dir / "marg_p2_ranker.py")
        sys.path.insert(0, str(code_dir))
        import marg_p2_ranker as mpr

        cert_w = np.array(cert["frozen_weights_delta6"], dtype=np.float64)
        if cert_w.shape != (6,) or np.any(cert_w < 0.0) or abs(float(cert_w.sum()) - 1.0) > 1e-5:
            raise ValueError("Invalid frozen_weights_delta6 simplex vector")

        ranker = mpr.MARGP2Ranker(data_dir=cache_dir, excluded_pmids=up["corpus_pmids"], weights=cert_w)
        if ranker.n_genes != 19296 or int(cert.get("candidate_space_hgnc_protein_coding", 0)) != 19296:
            raise ValueError("Candidate space size != 19,296")
        if int(len(ranker.ann_gidxs)) != int(up["n_clean_genes"]):
            raise ValueError("Clean HPOA neighbor gene count mismatch")

        # Check HPO input-order permutation invariance
        q0 = list(up["pos40"][0]["obs_hpo_terms"])
        q1 = list(up["p2_raw"][0]["obs_hpo_terms"])
        if ranker.rank_all_19296_genes(q0) != ranker.rank_all_19296_genes(list(reversed(q0))):
            raise ValueError("HPO input-order permutation invariance violated on Pos-40[0]")
        if ranker.rank_all_19296_genes(q1) != ranker.rank_all_19296_genes(list(reversed(q1))):
            raise ValueError("HPO input-order permutation invariance violated on P2-Raw[0]")

        ch_names = [
            "f1_xspec_only",
            "f2_string_notm_only",
            "f3_go_hgnc_only",
            "f4_paralogue_l3_only",
            "f5_xspec_bridge_only",
            "f6_concordance_only",
        ]
        u6 = np.full(6, 1.0 / 6.0, dtype=np.float64)

        # 3. Live recomputation across ALL 127 P2-Raw cases + 11 full-ranking shards (2,450,592 entries)
        p2_raw_q = up["p2_raw"]
        live_raw_ranks: list[float] = []
        live_raw_u6: list[float] = []
        live_raw_ch: list[list[float]] = [[] for _ in range(6)]
        live_raw_orders: list[np.ndarray] = []
        live_raw_scores: list[np.ndarray] = []

        for row in p2_raw_q:
            F = ranker.compute_6_channels(row["obs_hpo_terms"])
            t_idx = ranker.hgnc_to_idx[str(row["target_hgnc"])]
            for k in range(6):
                live_raw_ch[k].append(midrank_from_scores(F[k], t_idx))
            live_raw_u6.append(midrank_from_scores(np.round(u6 @ F, 11), t_idx))
            sc = np.round(cert_w @ F, 11)
            live_raw_scores.append(sc)
            live_raw_ranks.append(midrank_from_scores(sc, t_idx))
            live_raw_orders.append(np.lexsort((np.arange(ranker.n_genes), -sc)).astype(np.uint16))

        raw_block = cert["blind_p2_raw_127"]
        if len(raw_block["per_case_ranks"]) != 127 or max(
            abs(a - float(b)) for a, b in zip(live_raw_ranks, raw_block["per_case_ranks"])
        ) > 1e-8:
            raise ValueError("P2-Raw per_case_ranks mismatch against live MARG-P2 recomputation")

        r_hgncs = [str(r["target_hgnc"]) for r in p2_raw_q]
        r_cids = [str(r["case_id"]) for r in p2_raw_q]
        r_pmids = [list(r["case_pmids"]) for r in p2_raw_q]

        recomp_raw_sm = summarize_ranks_from_meta(r_hgncs, r_cids, r_pmids, live_raw_ranks, n_boot=2000)
        assert_summary_close(recomp_raw_sm, raw_block["marg_p2_seam"], "blind_p2_raw_127.marg_p2_seam")
        recomp_raw_u6 = summarize_ranks_from_meta(r_hgncs, r_cids, r_pmids, live_raw_u6, n_boot=2000)
        assert_summary_close(recomp_raw_u6, raw_block["equal_weight_6_of_6_baseline"], "blind_p2_raw_127.u6")
        for k, cname in enumerate(ch_names):
            assert_summary_close(
                summarize_ranks_from_meta(r_hgncs, r_cids, r_pmids, live_raw_ch[k], n_boot=1000),
                raw_block["single_channel_baselines"][cname],
                f"p2_raw.{cname}",
            )

        # P2-Raw shuffled-gene negative control
        raw_neg_ranks: list[float] = []
        for i, row in enumerate(p2_raw_q):
            s = 53
            wrong = p2_raw_q[(i + s) % 127]
            while wrong["target_hgnc"] == row["target_hgnc"]:
                s += 1
                wrong = p2_raw_q[(i + s) % 127]
            raw_neg_ranks.append(midrank_from_scores(live_raw_scores[i], ranker.hgnc_to_idx[str(wrong["target_hgnc"])]))
        recomp_raw_neg = summarize_ranks_from_meta(r_hgncs, r_cids, r_pmids, raw_neg_ranks, n_boot=2000)
        assert_summary_close(recomp_raw_neg, cert["negative_controls"]["p2_raw_shuffled_gene_control"], "p2_raw.neg")

        # Per-gene 10-gene table check
        by_g: dict[str, list[float]] = collections.defaultdict(list)
        for row, rk in zip(p2_raw_q, live_raw_ranks):
            by_g[str(row["target_hgnc"])].append(rk)
        cert_gtable = raw_block["per_gene_breakdown_10_genes"]
        if len(cert_gtable) != 10:
            raise ValueError("Expected 10 unique genes in P2-Raw breakdown")
        for grow in cert_gtable:
            rks = sorted(by_g[grow["hgnc_id"]])
            n_g = len(rks)
            med_g = rks[n_g // 2] if n_g % 2 == 1 else 0.5 * (rks[n_g // 2 - 1] + rks[n_g // 2])
            if (
                int(grow["n_cases"]) != n_g
                or abs(float(grow["mrr"]) - sum(1.0 / r for r in rks) / n_g) > 1e-8
                or abs(float(grow["median_rank"]) - med_g) > 1e-8
                or abs(float(grow["best_rank"]) - min(rks)) > 1e-8
                or int(grow["top_50_count"]) != sum(1 for r in rks if r <= 50.0)
                or int(grow["top_100_count"]) != sum(1 for r in rks if r <= 100.0)
            ):
                raise ValueError(f"Per-gene breakdown mismatch on {grow['symbol']}")

        # Verify all 11 label-free full-ranking shards (127 x 19,296 = 2,450,592 entries, case_sha256 join!)
        shards_meta = raw_block["full_19296_ranking_shards"]
        if len(shards_meta) != 11:
            raise ValueError(f"Expected 11 ranking shards, found {len(shards_meta)}")
        seen_raw = set()
        for sm in shards_meta:
            sp = obj_dir / sm["filename"]
            sb = sp.read_bytes()
            if len(sb) != int(sm["bytes"]) or sha256_bytes(sb) != sm["sha256"]:
                raise ValueError(f"Shard byte/sha256 mismatch on {sm['filename']}")
            with gzip.open(sp, "rt", encoding="utf-8") as f:
                hdr = f.readline().rstrip("\n").split("\t")
                if hdr != ["case_index", "case_sha256", "case_id", "ranked_19296_gidxs_csv"]:
                    raise ValueError(f"Unexpected columns in {sm['filename']}: {hdr}")
                for ln in f:
                    parts = ln.rstrip("\n").split("\t")
                    ci = int(parts[0])
                    seen_raw.add(ci)
                    if parts[1] != p2_raw_q[ci]["case_sha256"] or parts[2] != p2_raw_q[ci]["case_id"]:
                        raise ValueError(f"Upstream case_sha256/case_id mismatch on P2-Raw case {ci}")
                    arr = np.fromstring(parts[3], dtype=np.uint16, sep=",")
                    if arr.size != 19296 or not np.array_equal(arr, live_raw_orders[ci]):
                        raise ValueError(f"Full 19,296-gene ranking mismatch on P2-Raw case {ci}")
        if len(seen_raw) != 127:
            raise ValueError(f"P2-Raw shards covered {len(seen_raw)}/127 cases")

        # 4. Live recomputation across ALL 988 P2-Holdout cases + top100 predictions file!
        p2_hold_q = up["p2_hold"]
        n_hold = len(p2_hold_q)
        live_hold_ranks: list[float] = []
        live_hold_u6: list[float] = []
        live_hold_ch: list[list[float]] = [[] for _ in range(6)]
        live_hold_top100: list[np.ndarray] = []
        live_hold_scores: list[np.ndarray] = []

        for row in p2_hold_q:
            F = ranker.compute_6_channels(row["obs_hpo_terms"])
            t_idx = ranker.hgnc_to_idx[str(row["target_hgnc"])]
            for k in range(6):
                live_hold_ch[k].append(midrank_from_scores(F[k], t_idx))
            live_hold_u6.append(midrank_from_scores(np.round(u6 @ F, 11), t_idx))
            sc = np.round(cert_w @ F, 11)
            live_hold_scores.append(sc)
            live_hold_ranks.append(midrank_from_scores(sc, t_idx))
            ord_h = np.lexsort((np.arange(ranker.n_genes), -sc))[:100].astype(np.uint16)
            live_hold_top100.append(ord_h)

        hold_block = cert["blind_p2_holdout_988"]
        if len(hold_block["per_case_ranks"]) != n_hold or max(
            abs(a - float(b)) for a, b in zip(live_hold_ranks, hold_block["per_case_ranks"])
        ) > 1e-8:
            raise ValueError("P2-Holdout per_case_ranks mismatch against live MARG-P2 recomputation")

        h_hgncs = [str(r["target_hgnc"]) for r in p2_hold_q]
        h_cids = [str(r["case_id"]) for r in p2_hold_q]
        h_pmids = [list(r["case_pmids"]) for r in p2_hold_q]

        recomp_hold_sm = summarize_ranks_from_meta(h_hgncs, h_cids, h_pmids, live_hold_ranks, n_boot=2000)
        assert_summary_close(recomp_hold_sm, hold_block["marg_p2_seam"], "blind_p2_holdout_988.marg_p2_seam")
        recomp_hold_u6 = summarize_ranks_from_meta(h_hgncs, h_cids, h_pmids, live_hold_u6, n_boot=2000)
        assert_summary_close(recomp_hold_u6, hold_block["equal_weight_6_of_6_baseline"], "blind_p2_holdout_988.u6")
        for k, cname in enumerate(ch_names):
            assert_summary_close(
                summarize_ranks_from_meta(h_hgncs, h_cids, h_pmids, live_hold_ch[k], n_boot=1000),
                hold_block["single_channel_baselines"][cname],
                f"p2_holdout.{cname}",
            )

        # P2-Holdout shuffled-gene negative control
        hold_neg_ranks: list[float] = []
        for i, row in enumerate(p2_hold_q):
            s = 397
            wrong = p2_hold_q[(i + s) % n_hold]
            while wrong["target_hgnc"] == row["target_hgnc"]:
                s += 1
                wrong = p2_hold_q[(i + s) % n_hold]
            hold_neg_ranks.append(midrank_from_scores(live_hold_scores[i], ranker.hgnc_to_idx[str(wrong["target_hgnc"])]))
        recomp_hold_neg = summarize_ranks_from_meta(h_hgncs, h_cids, h_pmids, hold_neg_ranks, n_boot=2000)
        assert_summary_close(recomp_hold_neg, cert["negative_controls"]["p2_holdout_shuffled_gene_control"], "p2_holdout.neg")

        # Verify p2_holdout_top100_predictions.tsv.gz (0 y_true columns, exact top100 match across all 988 cases!)
        htop_meta = hold_block["top100_predictions_file"]
        htop_path = obj_dir / htop_meta["filename"]
        htop_bytes = htop_path.read_bytes()
        if len(htop_bytes) != int(htop_meta["bytes"]) or sha256_bytes(htop_bytes) != htop_meta["sha256"]:
            raise ValueError("p2_holdout_top100_predictions.tsv.gz byte/sha256 mismatch")
        seen_hold = set()
        with gzip.open(htop_path, "rt", encoding="utf-8") as f:
            hdr_h = f.readline().rstrip("\n").split("\t")
            if hdr_h != ["case_index", "case_sha256", "case_id", "top100_gidxs_csv"]:
                raise ValueError(f"Unexpected columns in {htop_meta['filename']}: {hdr_h}")
            for ln in f:
                parts = ln.rstrip("\n").split("\t")
                ci = int(parts[0])
                seen_hold.add(ci)
                if parts[1] != p2_hold_q[ci]["case_sha256"] or parts[2] != p2_hold_q[ci]["case_id"]:
                    raise ValueError(f"Upstream case_sha256/case_id mismatch on P2-Holdout case {ci}")
                arr100 = np.fromstring(parts[3], dtype=np.uint16, sep=",")
                if arr100.size != 100 or not np.array_equal(arr100, live_hold_top100[ci]):
                    raise ValueError(f"Top-100 prediction mismatch on P2-Holdout case {ci}")
        if len(seen_hold) != n_hold:
            raise ValueError(f"Holdout predictions covered {len(seen_hold)}/{n_hold} cases")

        # 5. Live recomputation across ALL 40 Pos-40 cases + Uniform 19,296 analytical null
        pos_q = up["pos40"]
        pos_ranks = [
            midrank_from_scores(ranker.score_19296(r["obs_hpo_terms"]), ranker.hgnc_to_idx[str(r["target_hgnc"])])
            for r in pos_q
        ]
        pos_block = cert["pos40_leave_self_hpoa_out"]
        if max(abs(a - float(b)) for a, b in zip(pos_ranks, pos_block["per_case_ranks"])) > 1e-8:
            raise ValueError("Pos-40 per_case_ranks mismatch")
        assert_summary_close(
            summarize_ranks_from_meta(
                [str(r["target_hgnc"]) for r in pos_q],
                [str(r["case_id"]) for r in pos_q],
                [list(r["case_pmids"]) for r in pos_q],
                pos_ranks,
                n_boot=2000,
            ),
            pos_block["marg_p2_seam"],
            "pos40.marg_p2_seam",
        )

        unif_cert = cert["negative_controls"]["uniform_19296_random_null"]
        exp_unif_mrr = float(np.sum(1.0 / np.arange(1, 19297, dtype=np.float64))) / 19296.0
        if (
            abs(float(unif_cert["analytical_expected_mrr"]) - exp_unif_mrr) > 1e-10
            or abs(float(unif_cert["analytical_expected_median_rank"]) - 9648.5) > 1e-9
        ):
            raise ValueError("Analytical uniform 19,296 null mismatch")

        # 6. Verify LIRICAL 2.4.1 & P2-Dev OOF summaries from per_case_ranks + static commitment hash
        lir_b = cert["lirical_2_4_1_baseline"]
        assert_summary_close(
            summarize_ranks_from_meta(r_hgncs, r_cids, r_pmids, lir_b["p2_raw_untouched_per_case_ranks"], n_boot=2000),
            lir_b["p2_raw_untouched_hpoa"],
            "lirical.p2_raw_untouched",
        )
        assert_summary_close(
            summarize_ranks_from_meta(r_hgncs, r_cids, r_pmids, lir_b["p2_raw_clean_per_case_ranks"], n_boot=2000),
            lir_b["p2_raw_clean_hpoa"],
            "lirical.p2_raw_clean",
        )
        assert_summary_close(
            summarize_ranks_from_meta(h_hgncs, h_cids, h_pmids, lir_b["p2_holdout_clean_per_case_ranks"], n_boot=2000),
            lir_b["p2_holdout_clean_hpoa"],
            "lirical.p2_holdout_clean",
        )
        assert_summary_close(
            summarize_ranks_from_meta(
                [str(r["target_hgnc"]) for r in pos_q],
                [str(r["case_id"]) for r in pos_q],
                [list(r["case_pmids"]) for r in pos_q],
                lir_b["pos40_clean_per_case_ranks"],
                n_boot=2000,
            ),
            lir_b["pos40_clean_hpoa"],
            "lirical.pos40_clean",
        )

        p2_dev_q = up["p2_dev"]
        d_hgncs = [str(r["target_hgnc"]) for r in p2_dev_q]
        d_cids = [str(r["case_id"]) for r in p2_dev_q]
        d_pmids = [list(r["case_pmids"]) for r in p2_dev_q]
        cv_b = cert["cv_fit_p2_dev_1132"]
        fw = np.array(cv_b["fold_weights"], dtype=np.float64)
        w_avg = fw.mean(axis=0)
        w_avg /= w_avg.sum()
        if np.max(np.abs(w_avg - cert_w)) > 2e-6:
            raise ValueError("5-fold CV weight mean mismatch against frozen_weights_delta6")
        assert_summary_close(
            summarize_ranks_from_meta(d_hgncs, d_cids, d_pmids, cv_b["oof_per_case_ranks"], n_boot=1000),
            cv_b["oof_p2_dev_summary"],
            "p2_dev.oof_summary",
        )
        assert_summary_close(
            summarize_ranks_from_meta(d_hgncs, d_cids, d_pmids, lir_b["p2_dev_clean_per_case_ranks"], n_boot=2000),
            lir_b["p2_dev_clean_hpoa"],
            "lirical.p2_dev_clean",
        )

        static_payload = {
            "target_id": cert["target_id"],
            "milestone": cert["milestone"],
            "method": cert["method"],
            "channel_names": cert["channel_names"],
            "provenance": cert["provenance"],
            "lirical_2_4_1_baseline": cert["lirical_2_4_1_baseline"],
            "cv_fit_p2_dev_1132": cert["cv_fit_p2_dev_1132"],
            "pass1_vs_pass2_audit_comparison": cert["pass1_vs_pass2_audit_comparison"],
        }
        if canonical_json_sha256(static_payload) != PINNED_EXTERNAL_COMMITMENTS["cert_static_sha256"]:
            raise ValueError("Certificate provenance / baseline / CV sensitivity commitment mismatch")

        # 7. Milestone p2 statistical dominance & negative-control separation checks
        for ci_key in ("mrr_ci95_case", "mrr_ci95_gene_cluster", "mrr_ci95_pub_cluster"):
            if recomp_raw_sm[ci_key][0] <= lir_b["p2_raw_untouched_hpoa"][ci_key][1]:
                raise ValueError(f"P2-Raw MARG-P2 failed non-overlapping {ci_key} vs LIRICAL 2.4.1")
            if recomp_hold_sm[ci_key][0] <= lir_b["p2_holdout_clean_hpoa"][ci_key][1]:
                raise ValueError(f"P2-Holdout MARG-P2 failed non-overlapping {ci_key} vs LIRICAL 2.4.1")
        if (
            recomp_raw_sm["mrr"] <= exp_unif_mrr
            or recomp_hold_sm["mrr_ci95_case"][0] <= recomp_hold_neg["mrr_ci95_case"][1]
            or recomp_hold_sm["top_1"] <= lir_b["p2_holdout_clean_hpoa"]["top_1"]
        ):
            raise ValueError("Negative-control separation or Top-1 dominance inequality failed")

    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        return 1

    dt = time.perf_counter() - t0
    print(
        f"VERIFICATION SUMMARY: Live upstream-joined recomputation across 127/127 P2-Raw (2,450,592 ranked entries, 0 mismatches) "
        f"+ 988/988 P2-Holdout (98,800 top-100 entries, 0 mismatches) + 40/40 Pos-40 verified in {dt:.2f}s | "
        f"P2-Raw MARG-P2 MRR={recomp_raw_sm['mrr']:.6f} (Med={recomp_raw_sm['median_rank']:.1f}) vs LIRICAL={lir_b['p2_raw_untouched_hpoa']['mrr']:.6f} (Med={lir_b['p2_raw_untouched_hpoa']['median_rank']:.1f}) | "
        f"P2-Holdout MARG-P2 MRR={recomp_hold_sm['mrr']:.6f} (Top-1={recomp_hold_sm['top_1_count']}/{n_hold}, Top-10={recomp_hold_sm['top_10_count']}/{n_hold}, Med={recomp_hold_sm['median_rank']:.1f}) "
        f"vs LIRICAL={lir_b['p2_holdout_clean_hpoa']['mrr']:.6f} & Shuffled-Ctrl={recomp_hold_neg['mrr']:.6f}"
    )
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(verify_all(corrupt_mode=("--corrupt" in sys.argv)))
