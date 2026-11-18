#!/usr/bin/env python3
"""
MARG-P2: Multi-Route Analytical Ranker for Unannotated Rare-Disease Causal Gene Discovery.

Standalone zero-leakage operator (`rank_all_19296_genes(obs_hpo_terms)`):
  - Candidate space: fixed 19,296 HGNC protein-coding genes (2026-05-01 monthly snapshot).
  - Symmetric candidate treatment: zero target-gene HPOA membership indicators or penalties.
  - Strictly pre-corpus (< 2026-06-09), PMID-purged knowledge-graph inputs:
      (f1) Cross-species orthologue knockout log-likelihood (`Monarch KG 2026-05-09` +
           `Upheno v2025-10-12` OWL equivalence/subsumption bridges)
      (f2) Zero-diagonal L2-whitened physical/functional interactome consensus
           (`STRING v12.0`, `textmining == 0` identically)
      (f3) Zero-diagonal L2-whitened specific macromolecular module consensus
           (`Gene Ontology 2026-05-19` + `HGNC 2026-05-01` structural gene groups)
      (f4) Zero-diagonal L_3 paralogue/direct-partner peak transfer
      (f5) 19,296-background analytical-null 2nd-order cross-species-to-complex bridge
      (f6) Bounded multi-route log-concordance (`log1p(z_xs) * log1p(z_hu)`)
"""
from __future__ import annotations

import collections
import gc
import gzip
import hashlib
import io
import json
import math
import os
import re
import struct
import sys
from pathlib import Path
from typing import Collection, Sequence

import numpy as np
from scipy import sparse

sys.dont_write_bytecode = True

_LE_DT = {
    np.dtype("float32"): "<f4",
    np.dtype("float64"): "<f8",
    np.dtype("int32"): "<i4",
    np.dtype("uint16"): "<u2",
    np.dtype("uint8"): "|u1",
}


def _save_bin_gz(path: Path, **arrays: np.ndarray) -> None:
    buf = io.BytesIO()
    buf.write(b"MARGTNS1")
    buf.write(struct.pack("<I", len(arrays)))
    for key in sorted(arrays.keys()):
        arr = np.asarray(arrays[key])
        dt_str = _LE_DT[arr.dtype]
        arr_le = np.ascontiguousarray(arr, dtype=np.dtype(dt_str))
        kb = key.encode("utf-8")
        db = dt_str.encode("ascii")
        raw = arr_le.tobytes()
        buf.write(struct.pack("<H", len(kb)) + kb)
        buf.write(struct.pack("<H", len(db)) + db)
        buf.write(struct.pack("<B", arr_le.ndim))
        for dim in arr_le.shape:
            buf.write(struct.pack("<I", int(dim)))
        buf.write(struct.pack("<I", len(raw)))
        buf.write(raw)
    with gzip.open(path, "wb", compresslevel=6) as f:
        f.write(buf.getvalue())


def _load_bin_gz(path: Path) -> dict[str, np.ndarray]:
    with gzip.open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"MARGTNS1":
        raise ValueError("Invalid MARGTNS1 header")
    off = 8
    (n_arr,) = struct.unpack_from("<I", data, off)
    off += 4
    out: dict[str, np.ndarray] = {}
    for _ in range(n_arr):
        (klen,) = struct.unpack_from("<H", data, off)
        off += 2
        key = data[off : off + klen].decode("utf-8")
        off += klen
        (dlen,) = struct.unpack_from("<H", data, off)
        off += 2
        dt_str = data[off : off + dlen].decode("ascii")
        off += dlen
        (ndim,) = struct.unpack_from("<B", data, off)
        off += 1
        shape = struct.unpack_from(f"<{ndim}I", data, off)
        off += 4 * ndim
        (nbytes,) = struct.unpack_from("<I", data, off)
        off += 4
        arr = np.frombuffer(data, dtype=np.dtype(dt_str), count=int(np.prod(shape)), offset=off).reshape(shape).copy()
        off += nbytes
        out[key] = arr
    return out

_PMID_RX = re.compile(r"PMID\s*:?\s*(\d+)", re.I)

_HPO_FREQ_WEIGHTS: dict[str, float] = {
    "HP:0040280": 1.00,
    "HP:0040281": 0.895,
    "HP:0040282": 0.545,
    "HP:0040283": 0.17,
    "HP:0040284": 0.025,
    "HP:0040285": 0.0,
}

_TAXON_PRIORS: dict[str, float] = {
    "NCBITaxon:10090": 1.00,
    "NCBITaxon:10116": 0.90,
    "NCBITaxon:7955": 0.75,
    "NCBITaxon:8355": 0.70,
    "NCBITaxon:8364": 0.70,
    "NCBITaxon:7227": 0.50,
    "NCBITaxon:6239": 0.50,
    "NCBITaxon:4896": 0.35,
    "NCBITaxon:44689": 0.30,
}


def _parse_hpoa_freq(freq_str: str) -> float:
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


def _parse_hpo_obo(obo_path: Path) -> tuple[dict[str, set[str]], dict[str, str], set[str]]:
    parents: dict[str, set[str]] = collections.defaultdict(set)
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
                    parents[cur_id].add(pid)
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
        for v in sorted(children.get(u, ())):
            if v not in pheno_sub:
                dq.append(v)

    return parents, alt_map, pheno_sub


def zscore_1d(v: np.ndarray) -> np.ndarray:
    m = float(v.mean())
    s = float(v.std())
    if s <= 1e-12:
        return np.zeros_like(v, dtype=np.float64)
    return (v - m) / s


def norm_pos_scale(v: np.ndarray) -> np.ndarray:
    n = v.size
    m = float(np.partition(v, n // 2)[n // 2])
    shifted = v - m
    idx_995 = min(n - 1, int(0.995 * n))
    q995 = float(np.partition(shifted, idx_995)[idx_995])
    rms = float(np.sqrt(np.mean(shifted * shifted)))
    denom = max(q995, rms, 1e-9)
    return shifted / denom


def row_whiten_nonneg_kernel(
    K: sparse.csr_matrix,
    gamma: float = 0.75,
    floor_quantile: float = 0.20,
) -> sparse.csr_matrix:
    row_sq = np.asarray(K.power(2).sum(axis=1)).ravel()
    nz = row_sq[row_sq > 0]
    tau0_sq = float(np.quantile(nz, floor_quantile)) if nz.size > 0 else 1.0
    scale = np.where(row_sq > 0, np.power(row_sq + tau0_sq, -0.5 * gamma), 0.0)
    return (sparse.diags(scale) @ K).tocsr()


class MARGP2Ranker:
    """Deterministic HPOA-blind 6-channel ranker over all 19,296 HGNC protein-coding genes."""

    def __init__(
        self,
        data_dir: Path | str | None = None,
        excluded_pmids: Collection[str] = (),
        weights: Sequence[float] | None = None,
    ) -> None:
        if data_dir is None:
            env_dir = os.environ.get("MARG_P2_CACHE_DIR", "")
            ddir = Path(env_dir) if env_dir else (Path.home() / ".cache" / "phenopacket_p2")
        else:
            ddir = Path(data_dir)
        kg_dir = ddir / "compiled_kg"
        excl_pmids = set(excluded_pmids)

        # 1. Fixed 19,296 HGNC protein-coding gene universe + structural gene groups (2026-05-01)
        hgnc_path = ddir / "hgnc_complete_set_2026-06-01.txt"
        raw_pc: list[str] = []
        hgnc_to_sym: dict[str, str] = {}
        entrez_to_hgnc: dict[str, str] = {}
        hgnc_grp_raw: dict[str, list[str]] = collections.defaultdict(list)

        with hgnc_path.open(encoding="utf-8") as f:
            cols = f.readline().rstrip("\n").split("\t")
            ih = cols.index("hgnc_id")
            isym = cols.index("symbol")
            iloc = cols.index("locus_group")
            ient = cols.index("entrez_id")
            igrp = cols.index("gene_group_id")
            for ln in f:
                p = ln.rstrip("\n").split("\t")
                if len(p) <= max(ih, isym, iloc, ient, igrp):
                    continue
                if p[iloc] != "protein-coding gene":
                    continue
                hid = p[ih]
                raw_pc.append(hid)
                hgnc_to_sym[hid] = p[isym]
                if p[ient]:
                    entrez_to_hgnc[p[ient]] = hid
                for gid in p[igrp].strip('"').split("|"):
                    gid_s = gid.strip()
                    if gid_s:
                        hgnc_grp_raw[gid_s].append(hid)

        self.pc_hgnc = sorted(set(raw_pc), key=lambda h: int(h.split(":")[1]))
        if len(self.pc_hgnc) != 19296:
            raise ValueError(f"Expected 19,296 HGNC protein-coding genes, found {len(self.pc_hgnc)}")
        self.n_genes = 19296
        self.hgnc_to_idx = {h: i for i, h in enumerate(self.pc_hgnc)}
        self.hgnc_to_symbol = hgnc_to_sym

        self.weights = (
            np.array(weights, dtype=np.float64)
            if weights is not None
            else np.full(6, 1.0 / 6.0, dtype=np.float64)
        )

        # 2. HPO v2026-06-06 DAG & strictly pre-corpus genes_to_disease_v2026-06-06.txt
        parents_str, alt_map, pheno_sub = _parse_hpo_obo(ddir / "hp_v2026-06-06.obo")
        self.hp_terms = sorted(pheno_sub)
        self.hp_t2i = {t: i for i, t in enumerate(self.hp_terms)}
        self.pheno_sub = pheno_sub
        self.alt_map = alt_map
        n_hp = len(self.hp_terms)

        hp_parents_idx: list[list[int]] = [[] for _ in range(n_hp)]
        for c_str, pset in sorted(parents_str.items()):
            ci = self.hp_t2i.get(c_str)
            if ci is not None:
                hp_parents_idx[ci] = sorted(self.hp_t2i[p] for p in pset if p in self.hp_t2i)

        self.hp_anc_idx: list[set[int]] = [set() for _ in range(n_hp)]
        for i in range(n_hp):
            anc: set[int] = set()
            dq = collections.deque([i])
            while dq:
                u = dq.popleft()
                if u in anc:
                    continue
                anc.add(u)
                for par in hp_parents_idx[u]:
                    if par not in anc:
                        dq.append(par)
            self.hp_anc_idx[i] = anc

        dis_to_hgnc: dict[str, set[str]] = collections.defaultdict(set)
        with (ddir / "genes_to_disease_v2026-06-06.txt").open(encoding="utf-8") as f:
            f.readline()
            for ln in f:
                if not ln.strip() or ln.startswith("#"):
                    continue
                p = ln.rstrip("\n").split("\t")
                ent = p[0].replace("NCBIGene:", "")
                hid = entrez_to_hgnc.get(ent)
                if hid is not None:
                    dis_to_hgnc[p[3]].add(hid)

        # 3. PMID-cleaned HPOA v2026-06-06 neighbor syndrome tables (zero diagonal enforced downstream)
        clean_gene_tf: dict[int, dict[int, float]] = collections.defaultdict(dict)
        dis_terms: dict[str, dict[int, float]] = collections.defaultdict(dict)
        with (ddir / "phenotype_v2026-06-06.hpoa").open(encoding="utf-8") as f:
            for ln in f:
                if ln.startswith("#") or ln.startswith("database_id"):
                    continue
                p = ln.rstrip("\n").split("\t")
                if len(p) <= 10 or p[10] != "P" or p[2] == "NOT":
                    continue
                dis_id = p[0]
                if dis_id not in dis_to_hgnc:
                    continue
                hpo_id = alt_map.get(p[3], p[3])
                ti = self.hp_t2i.get(hpo_id)
                if ti is None:
                    continue
                ref = p[4]
                if excl_pmids and (set(_PMID_RX.findall(ref)) & excl_pmids):
                    continue
                fw = _parse_hpoa_freq(p[7])
                if fw <= 0.0:
                    continue
                if fw > dis_terms[dis_id].get(ti, 0.0):
                    dis_terms[dis_id][ti] = fw
                for hid in dis_to_hgnc[dis_id]:
                    gi = self.hgnc_to_idx[hid]
                    if fw > clean_gene_tf[gi].get(ti, 0.0):
                        clean_gene_tf[gi][ti] = fw

        hpoa_term_counts: collections.Counter[int] = collections.Counter()
        gene_anc_freq: dict[int, dict[int, float]] = {}
        term_df: collections.Counter[int] = collections.Counter()

        for gidx, tdict in sorted(clean_gene_tf.items()):
            aw: dict[int, float] = {}
            for ti, fw in sorted(tdict.items()):
                hpoa_term_counts[ti] += fw
                for ai in sorted(self.hp_anc_idx[ti]):
                    if fw > aw.get(ai, 0.0):
                        aw[ai] = fw
            if aw:
                gene_anc_freq[gidx] = aw
                for ai in sorted(aw):
                    term_df[ai] += 1

        tot_hpoa_w = sum(hpoa_term_counts.values())
        n_ann = len(gene_anc_freq)
        self.ic_hpoa = np.zeros(n_hp, dtype=np.float64)
        for ti, df in term_df.items():
            self.ic_hpoa[ti] = -math.log((df + 0.5) / (n_ann + 1.0))

        self.ann_gidxs = np.array(sorted(gene_anc_freq.keys()), dtype=np.int32)
        n_ac = len(self.ann_gidxs)

        active_anc = sorted(
            (ti for ti in range(n_hp) if self.ic_hpoa[ti] > 0.15),
            key=lambda ti: self.hp_terms[ti],
        )
        self.anc_ti_to_col = {ti: col for col, ti in enumerate(active_anc)}
        self.ic_anc_vec = np.array([self.ic_hpoa[ti] for ti in active_anc], dtype=np.float32)

        g_rows, g_cols, g_vals = [], [], []
        for apos, gidx in enumerate(self.ann_gidxs):
            for ai, fw in sorted(gene_anc_freq[int(gidx)].items()):
                ci = self.anc_ti_to_col.get(ai)
                if ci is not None:
                    g_rows.append(apos)
                    g_cols.append(ci)
                    g_vals.append((fw ** 0.35) * (self.ic_anc_vec[ci] ** 1.35))
        self.H_dag = sparse.csr_matrix(
            (np.array(g_vals, dtype=np.float32), (np.array(g_rows, dtype=np.int32), np.array(g_cols, dtype=np.int32))),
            shape=(n_ac, len(active_anc)),
        )
        self.H_dag.sort_indices()
        self.h_norms = np.sqrt(np.asarray(self.H_dag.power(2).sum(axis=1)).ravel())
        self.med_hnorm = float(np.median(self.h_norms[self.h_norms > 0]))

        tmp_p: dict[int, list[int]] = collections.defaultdict(list)
        tmp_w: dict[int, list[float]] = collections.defaultdict(list)
        for apos, gidx in enumerate(self.ann_gidxs):
            for ai, fw in sorted(gene_anc_freq[int(gidx)].items()):
                if self.ic_hpoa[ai] > 1e-6:
                    tmp_p[ai].append(apos)
                    tmp_w[ai].append(fw)
        self.hpoa_inv_pos = {ai: np.array(v, dtype=np.int32) for ai, v in tmp_p.items()}
        self.hpoa_inv_fw = {ai: np.array(v, dtype=np.float32) for ai, v in tmp_w.items()}
        self._mica_row_cache: dict[int, np.ndarray] = {}
        self._xspec_row_cache: dict[int, np.ndarray] = {}

        # Input-hash-verified local cache in ~/.cache/phenopacket_p2/compiled_kg/ (0 files in object/!)
        kh = hashlib.sha256(b"v2_sorted_det:")
        for fn_k in (
            ddir / "hp_v2026-06-06.obo",
            ddir / "phenotype_v2026-06-06.hpoa",
            ddir / "genes_to_disease_v2026-06-06.txt",
            ddir / "hgnc_complete_set_2026-06-01.txt",
            kg_dir / "xspec_ontology.json.gz",
            kg_dir / "xspec_orth_pheno.tsv.gz",
        ):
            st_k = fn_k.stat()
            kh.update(f"{fn_k.name}:{st_k.st_size}:".encode("utf-8"))
        kh.update(",".join(sorted(excl_pmids)).encode("utf-8"))
        bg_cache_path = kg_dir / f"_bg_init_{kh.hexdigest()[:16]}.bin.gz"

        if bg_cache_path.is_file():
            bg = _load_bin_gz(bg_cache_path)
            self.mu_mica = bg["mu_mica"]
            self.denom_mica = bg["denom_mica"]
            self.concept_ic = bg["concept_ic"]
            self.has_xspec = bg["has_xspec"].astype(np.float64)
            self.mu1_xspec = bg["mu1_xspec"]
            hp_ptr = bg["hp_xs_ptr"]
            hp_idx = bg["hp_xs_idx"]
            self.hp_xs_anc = [tuple(int(x) for x in hp_idx[hp_ptr[ti] : hp_ptr[ti + 1]]) for ti in range(n_hp)]
            inv_ptr = bg["inv_ptr"]
            inv_g_all = bg["inv_g_all"].astype(np.int32)
            inv_wc_all = bg["inv_wc_all"]
            n_concepts = len(self.concept_ic)
            self.xs_inv_g = [inv_g_all[inv_ptr[c] : inv_ptr[c + 1]] for c in range(n_concepts)]
            self.xs_inv_wc = [inv_wc_all[inv_ptr[c] : inv_ptr[c + 1]] for c in range(n_concepts)]
        else:
            self.mu_mica = np.zeros(n_ac, dtype=np.float64)
            ex2_mica = np.zeros(n_ac, dtype=np.float64)
            for ti, w_bg in sorted(hpoa_term_counts.items()):
                row_v = self._get_hpoa_mica_row(ti)
                pr = w_bg / tot_hpoa_w
                self.mu_mica += pr * row_v
                ex2_mica += pr * (row_v.astype(np.float64) ** 2)
            sd_mica = np.sqrt(np.maximum(0.0, ex2_mica - self.mu_mica ** 2))
            self.denom_mica = sd_mica + 0.75 * float(np.median(sd_mica[sd_mica > 0]))
            self._mica_row_cache.clear()

            # 4. Cross-Species XSpec DAG (Monarch KG 2026-05-09 + Upheno v2025-10-12)
            with gzip.open(kg_dir / "xspec_ontology.json.gz", "rt", encoding="utf-8") as f:
                ont = json.load(f)
            term_to_concept: dict[str, str] = ont["term_to_concept"]
            concept_parents: dict[str, list[str]] = ont["concept_parents"]

            gene_orths: dict[int, list[tuple[str, float, list[str]]]] = collections.defaultdict(list)
            seed_concepts: set[str] = set(term_to_concept.values())
            with gzip.open(kg_dir / "xspec_orth_pheno.tsv.gz", "rt", encoding="utf-8") as f:
                f.readline()
                for ln in f:
                    p = ln.rstrip("\n").split("\t")
                    gidx = int(p[0])
                    c_list = [c for c in p[5].split("|") if c]
                    seed_concepts.update(c_list)
                    gene_orths[gidx].append((p[3], float(p[4]), c_list))

            xs_anc_cache: dict[str, tuple[str, ...]] = {}

            def get_xs_anc(c: str) -> tuple[str, ...]:
                cached = xs_anc_cache.get(c)
                if cached is not None:
                    return cached
                vis = {c}
                st = list(concept_parents.get(c, ()))
                while st:
                    u = st.pop()
                    if u not in vis:
                        vis.add(u)
                        st.extend(concept_parents.get(u, ()))
                res = tuple(sorted(vis))
                xs_anc_cache[c] = res
                return res

            for sc in sorted(seed_concepts):
                get_xs_anc(sc)

            hp_reachable: set[str] = set()
            hp_term_anc_c: list[list[str]] = [[] for _ in range(n_hp)]
            for ti, hp_t in enumerate(self.hp_terms):
                c = term_to_concept.get(hp_t)
                if c:
                    ancs = list(get_xs_anc(c))
                    hp_term_anc_c[ti] = ancs
                    hp_reachable.update(ancs)

            concept_list = sorted(hp_reachable)
            c_to_id = {c: i for i, c in enumerate(concept_list)}
            n_concepts = len(concept_list)

            gene_concept_w: dict[int, dict[int, float]] = {}
            concept_df = np.zeros(n_concepts, dtype=np.float64)
            for gidx, orth_list in gene_orths.items():
                comp_log_surv: dict[int, float] = collections.defaultdict(float)
                for tax, w_orth, direct_cs in orth_list:
                    tp = _TAXON_PRIORS.get(tax, 0.45)
                    ls = math.log(1.0 - min(0.98, tp * min(1.0, w_orth)))
                    anc_u: set[str] = set()
                    for dc in direct_cs:
                        anc_u.update(get_xs_anc(dc))
                    for ac in anc_u:
                        cid = c_to_id.get(ac)
                        if cid is not None:
                            comp_log_surv[cid] += ls
                if comp_log_surv:
                    cw = {cid: 1.0 - math.exp(ls) for cid, ls in comp_log_surv.items()}
                    gene_concept_w[gidx] = cw
                    for cid, val in cw.items():
                        concept_df[cid] += val

            n_cov = max(1, len(gene_concept_w))
            self.concept_ic = np.maximum(0.0, -np.log((concept_df + 0.5) / (n_cov + 1.0))).astype(np.float32)
            self.has_xspec = np.zeros(self.n_genes, dtype=np.float64)
            for gi in gene_concept_w:
                self.has_xspec[int(gi)] = 1.0

            self.hp_xs_anc = [() for _ in range(n_hp)]
            for ti in range(n_hp):
                cids = [c_to_id[a] for a in hp_term_anc_c[ti] if a in c_to_id and self.concept_ic[c_to_id[a]] > 1e-6]
                cids.sort(key=lambda x: float(self.concept_ic[x]), reverse=True)
                self.hp_xs_anc[ti] = tuple(cids)

            inv_g: list[list[int]] = [[] for _ in range(n_concepts)]
            inv_w: list[list[float]] = [[] for _ in range(n_concepts)]
            for gidx, cw in gene_concept_w.items():
                for cid, w in cw.items():
                    if self.concept_ic[cid] > 1e-6:
                        inv_g[cid].append(gidx)
                        inv_w[cid].append(w)
            self.xs_inv_g = [np.array(x, dtype=np.int32) for x in inv_g]
            self.xs_inv_wc = [
                np.array(inv_w[cid], dtype=np.float32) * float(self.concept_ic[cid])
                for cid in range(n_concepts)
            ]
            self.hp_xs_anc = [
                tuple(cid for cid in self.hp_xs_anc[ti] if self.xs_inv_g[cid].size > 0)
                for ti in range(n_hp)
            ]

            self.mu1_xspec = np.zeros(self.n_genes, dtype=np.float64)
            for ti, w_bg in sorted(hpoa_term_counts.items()):
                if w_bg > 0.0:
                    self.mu1_xspec += (w_bg / tot_hpoa_w) * self._get_xspec_row(ti)
            self._xspec_row_cache.clear()

            try:
                hp_ptr_l = [0]
                hp_idx_l: list[int] = []
                for ti in range(n_hp):
                    hp_idx_l.extend(self.hp_xs_anc[ti])
                    hp_ptr_l.append(len(hp_idx_l))
                inv_ptr_l = [0]
                for c in range(n_concepts):
                    inv_ptr_l.append(inv_ptr_l[-1] + int(self.xs_inv_g[c].size))
                _save_bin_gz(
                    bg_cache_path,
                    mu_mica=self.mu_mica,
                    denom_mica=self.denom_mica,
                    concept_ic=self.concept_ic,
                    has_xspec=self.has_xspec.astype(np.uint8),
                    mu1_xspec=self.mu1_xspec,
                    hp_xs_ptr=np.array(hp_ptr_l, dtype=np.int32),
                    hp_xs_idx=np.array(hp_idx_l, dtype=np.int32),
                    inv_ptr=np.array(inv_ptr_l, dtype=np.int32),
                    inv_g_all=np.concatenate(self.xs_inv_g).astype(np.uint16),
                    inv_wc_all=np.concatenate(self.xs_inv_wc).astype(np.float32),
                )
            except OSError:
                pass

            del ont, term_to_concept, concept_parents, gene_orths, xs_anc_cache, hp_term_anc_c, gene_concept_w
            gc.collect()

        # 5. STRING v12.0 (textmining == 0) zero-diagonal L2-whitened kernels
        u_l, v_l, st_l, sed_l = [], [], [], []
        with gzip.open(kg_dir / "string_v12_notm_edges.tsv.gz", "rt", encoding="utf-8") as f:
            f.readline()
            for ln in f:
                p = ln.rstrip("\n").split("\t")
                u_l.append(int(p[0]))
                v_l.append(int(p[1]))
                st_l.append(float(p[2]))
                sed_l.append(float(p[3]))
        u_raw = np.array(u_l, dtype=np.int32)
        v_raw = np.array(v_l, dtype=np.int32)
        st_raw = np.array(st_l, dtype=np.float32)
        sed_raw = np.array(sed_l, dtype=np.float32)

        u_sym = np.concatenate([u_raw, v_raw])
        v_sym = np.concatenate([v_raw, u_raw])
        wt_sym = np.concatenate([st_raw, st_raw])
        wed_sym = np.concatenate([sed_raw, sed_raw])

        A_tot = sparse.csr_matrix((wt_sym, (u_sym, v_sym)), shape=(self.n_genes, self.n_genes))
        m_ed = wed_sym >= 0.15
        A_ed = sparse.csr_matrix(
            (np.power(wed_sym[m_ed], 1.5), (u_sym[m_ed], v_sym[m_ed])),
            shape=(self.n_genes, self.n_genes),
        )

        def sym_norm(A: sparse.csr_matrix, d0: float) -> sparse.csr_matrix:
            d = np.asarray(A.sum(axis=1)).ravel()
            inv_s = np.zeros_like(d)
            np.divide(1.0, np.sqrt(d + d0), out=inv_s, where=d > 0)
            return (sparse.diags(inv_s) @ A @ sparse.diags(inv_s)).tocsr()

        S_ed = sym_norm(A_ed, 1.5)
        S_tot = sym_norm(A_tot, 3.0)
        K_ed_1 = S_ed[:, self.ann_gidxs].tocsr()
        K_ed_2 = (S_ed @ K_ed_1).tolil()
        for j, gi in enumerate(self.ann_gidxs):
            K_ed_2[int(gi), j] = 0.0
        self.K_ed = row_whiten_nonneg_kernel((K_ed_1 + 0.20 * K_ed_2.tocsr()).tocsr(), gamma=0.75, floor_quantile=0.15)
        self.K_tot = row_whiten_nonneg_kernel(S_tot[:, self.ann_gidxs].tocsr(), gamma=0.80, floor_quantile=0.15)

        # 6. GO 2026-05-19 + HGNC 2026-05-01 zero-diagonal K_go and 2nd-order K_bridge
        with gzip.open(kg_dir / "go_2026_05_19_clean.json.gz", "rt", encoding="utf-8") as f:
            gdata = json.load(f)
        go_aspect: dict[str, str] = gdata["go_aspect"]
        go_parents: dict[str, list[str]] = gdata["go_parents"]
        gene_go: dict[str, list[list]] = gdata["gene_go"]

        go_anc_cache: dict[str, tuple[str, ...]] = {}

        def get_go_anc(g: str) -> tuple[str, ...]:
            cached = go_anc_cache.get(g)
            if cached is not None:
                return cached
            vis = {g}
            st = list(go_parents.get(g, ()))
            while st:
                u = st.pop()
                if u not in vis:
                    vis.add(u)
                    st.extend(go_parents.get(u, ()))
            res = tuple(sorted(vis))
            go_anc_cache[g] = res
            return res

        term_genes: dict[str, list[tuple[int, float]]] = collections.defaultdict(list)
        for gidx_s, items in sorted(gene_go.items(), key=lambda kv: int(kv[0])):
            gidx = int(gidx_s)
            best_a: dict[str, float] = {}
            for gid, w in items:
                wf = float(w)
                for a in get_go_anc(gid):
                    if wf > best_a.get(a, 0.0):
                        best_a[a] = wf
            for a, wf in sorted(best_a.items()):
                term_genes[a].append((gidx, wf))

        aspect_mult = {"C": 1.45, "F": 1.15, "P": 0.90}
        n_go_genes = max(1, len(gene_go))
        rows_m, cols_m, vals_m = [], [], []
        kept_m = 0
        for gid, glist in sorted(term_genes.items()):
            df = len(glist)
            if df < 2 or df > 350:
                continue
            ic = -math.log((df + 0.5) / (n_go_genes + 1.0))
            asp_w = aspect_mult.get(go_aspect.get(gid, "P"), 1.0)
            mod_scale = math.sqrt(asp_w * (ic ** 2.0) / (df + 2.5))
            for gidx, wf in glist:
                rows_m.append(gidx)
                cols_m.append(kept_m)
                vals_m.append(wf * mod_scale)
            kept_m += 1

        b_rows, b_cols, b_vals = [], [], []
        kept_b = 0
        for _, hids_grp in sorted(hgnc_grp_raw.items()):
            ug = sorted({self.hgnc_to_idx[h] for h in hids_grp if h in self.hgnc_to_idx})
            df = len(ug)
            if 2 <= df <= 120:
                ic = -math.log((df + 0.5) / (self.n_genes + 1.0))
                mod_scale = math.sqrt(1.60 * (ic ** 2.0) / (df + 2.0))
                for gidx in ug:
                    rows_m.append(gidx)
                    cols_m.append(kept_m)
                    vals_m.append(mod_scale)
                kept_m += 1
            if 2 <= df <= 80:
                sc_b = 1.0 / math.sqrt(df + 1.0)
                for gidx in ug:
                    b_rows.append(gidx)
                    b_cols.append(kept_b)
                    b_vals.append(sc_b)
                kept_b += 1

        M_all = sparse.csr_matrix(
            (np.array(vals_m, dtype=np.float32), (np.array(rows_m, dtype=np.int32), np.array(cols_m, dtype=np.int32))),
            shape=(self.n_genes, kept_m),
        )
        M_ann = M_all[self.ann_gidxs, :].tocsr()
        K_go_raw = (M_all @ M_ann.T).tolil()
        for j, gi in enumerate(self.ann_gidxs):
            K_go_raw[int(gi), j] = 0.0
        self.K_go = row_whiten_nonneg_kernel(K_go_raw.tocsr(), gamma=0.75, floor_quantile=0.20)

        m_b = wed_sym >= 0.25
        A_ed_b = sparse.csr_matrix(
            (np.power(wed_sym[m_b], 1.5), (u_sym[m_b], v_sym[m_b])),
            shape=(self.n_genes, self.n_genes),
        )
        S_ed_b = sym_norm(A_ed_b, 2.0)
        M_grp_b = sparse.csr_matrix(
            (np.array(b_vals, dtype=np.float32), (np.array(b_rows, dtype=np.int32), np.array(b_cols, dtype=np.int32))),
            shape=(self.n_genes, kept_b),
        )
        S_grp_b = (M_grp_b @ M_grp_b.T).tolil()
        S_grp_b.setdiag(0.0)
        self.K_bridge = row_whiten_nonneg_kernel((S_ed_b + 0.50 * S_grp_b.tocsr()).tocsr(), gamma=0.75, floor_quantile=0.20)

        p_orth = self.has_xspec / max(1.0, self.has_xspec.sum())
        self.mu_bridge = np.asarray(self.K_bridge @ p_orth).ravel()
        sq_bridge = np.asarray(self.K_bridge.power(2) @ p_orth).ravel()
        sd_b = np.sqrt(np.maximum(0.0, sq_bridge - self.mu_bridge ** 2))
        self.sd_bridge = sd_b + float(np.median(sd_b[sd_b > 0]))

        # 7. Disease-level L_3 paralogue-peak tables (strictly from genes_to_disease_v2026-06-06.txt)
        dis_list = sorted(dis_terms.keys())
        self.n_dis = len(dis_list)
        dis_term_df: collections.Counter[int] = collections.Counter()
        dis_anc = []
        dis_sizes = []
        g2apos = {int(g): i for i, g in enumerate(self.ann_gidxs)}
        d_rows, d_cols = [], []

        for di, d in enumerate(dis_list):
            tdict_d = dis_terms[d]
            dis_sizes.append(len(tdict_d))
            for hid in sorted(dis_to_hgnc[d]):
                gi = self.hgnc_to_idx[hid]
                if gi in g2apos:
                    d_rows.append(g2apos[gi])
                    d_cols.append(di)
            aw_d: dict[int, float] = {}
            for ti, fw in sorted(tdict_d.items()):
                for ai in sorted(self.hp_anc_idx[ti]):
                    if fw > aw_d.get(ai, 0.0):
                        aw_d[ai] = fw
            dis_anc.append(aw_d)
            for ai in sorted(aw_d):
                dis_term_df[ai] += 1

        self.ic_dis = np.zeros(n_hp, dtype=np.float64)
        for ti, df in dis_term_df.items():
            self.ic_dis[ti] = -math.log((df + 0.5) / (self.n_dis + 1.0))

        inv_d: dict[int, list[int]] = collections.defaultdict(list)
        inv_dfw: dict[int, list[float]] = collections.defaultdict(list)
        for di, aw_d in enumerate(dis_anc):
            for ai, fw in sorted(aw_d.items()):
                if self.ic_dis[ai] > 1e-6:
                    inv_d[ai].append(di)
                    inv_dfw[ai].append(fw)
        self.dis_inv_d = {ai: np.array(v, dtype=np.int32) for ai, v in inv_d.items()}
        self.dis_inv_fw = {ai: np.array(v, dtype=np.float32) for ai, v in inv_dfw.items()}
        self.dis_pen = np.power(np.array(dis_sizes, dtype=np.float64) + 12.0, -0.25)
        self.d_rows = np.array(d_rows, dtype=np.int32)
        self.d_cols = np.array(d_cols, dtype=np.int32)
        self._dis_row_cache: dict[int, np.ndarray] = {}

        self.K3_mod = self.K_go.power(3.0).tocsc()
        self.K3_ed = self.K_ed.power(3.0).tocsc()
        self.K_ed_csc = self.K_ed.tocsc()
        self.K_tot_csc = self.K_tot.tocsc()
        self.K_go_csc = self.K_go.tocsc()
        self.K_bridge_csc = self.K_bridge.tocsc()
        gc.collect()

    def _get_xspec_row(self, ti: int) -> np.ndarray:
        cached = self._xspec_row_cache.get(ti)
        if cached is not None:
            return cached
        best = np.zeros(self.n_genes, dtype=np.float32)
        for cid in self.hp_xs_anc[ti]:
            gs = self.xs_inv_g[cid]
            cand_w = self.xs_inv_wc[cid]
            cur = best[gs]
            m = cand_w > cur
            if np.any(m):
                best[gs[m]] = cand_w[m]
        self._xspec_row_cache[ti] = best
        return best

    def _get_hpoa_mica_row(self, ti: int) -> np.ndarray:
        cached = self._mica_row_cache.get(ti)
        if cached is not None:
            return cached
        best = np.zeros(len(self.ann_gidxs), dtype=np.float32)
        q_ancs = sorted(self.hp_anc_idx[ti], key=lambda ai: (-float(self.ic_hpoa[ai]), ai))
        q_mult = math.sqrt(max(0.5, float(self.ic_hpoa[ti]) if self.ic_hpoa[ti] > 0 else 2.0))
        for ai in q_ancs:
            ic_a = float(self.ic_hpoa[ai])
            if ic_a <= 1e-6 or ai not in self.hpoa_inv_pos:
                continue
            apos = self.hpoa_inv_pos[ai]
            val = q_mult * (np.power(self.hpoa_inv_fw[ai], 0.35) * (ic_a ** 1.4))
            m = val > best[apos]
            if np.any(m):
                best[apos[m]] = val[m]
        self._mica_row_cache[ti] = best
        return best

    def _get_dis_llr_row(self, ti: int) -> np.ndarray:
        cached = self._dis_row_cache.get(ti)
        if cached is not None:
            return cached
        best = np.zeros(self.n_dis, dtype=np.float32)
        q_ancs = sorted(self.hp_anc_idx[ti], key=lambda ai: (-float(self.ic_dis[ai]), ai))
        for ai in q_ancs:
            ic_a = float(self.ic_dis[ai])
            if ic_a <= 1e-6 or ai not in self.dis_inv_d:
                continue
            ds = self.dis_inv_d[ai]
            val = np.log1p(self.dis_inv_fw[ai] * np.expm1(0.85 * ic_a))
            m = val > best[ds]
            if np.any(m):
                best[ds[m]] = val[m]
        self._dis_row_cache[ti] = best
        return best

    def compute_6_channels(self, obs_hpo_terms: Sequence[str]) -> np.ndarray:
        q_clean = tuple(
            sorted(
                {
                    self.alt_map.get(t, t)
                    for t in obs_hpo_terms
                    if self.alt_map.get(t, t) in self.pheno_sub
                    and self.alt_map.get(t, t) != "HP:0000118"
                }
            )
        )
        if not q_clean:
            return np.zeros((6, self.n_genes), dtype=np.float64)

        tis = [self.hp_t2i[t] for t in q_clean]
        m = len(tis)

        raw_xspec = np.zeros(self.n_genes, dtype=np.float64)
        for ti in tis:
            raw_xspec += self._get_xspec_row(ti)
        c1 = raw_xspec - 1.25 * m * self.mu1_xspec
        f1 = norm_pos_scale(c1)

        sum_mica = np.zeros(len(self.ann_gidxs), dtype=np.float64)
        q_anc_u: set[int] = set()
        for ti in tis:
            sum_mica += self._get_hpoa_mica_row(ti)
            for ai in self.hp_anc_idx[ti]:
                ci = self.anc_ti_to_col.get(ai)
                if ci is not None:
                    q_anc_u.add(ci)
        s_mica = (sum_mica - m * self.mu_mica) / (math.sqrt(m) * self.denom_mica)

        q_vec = np.zeros(len(self.ic_anc_vec), dtype=np.float32)
        if q_anc_u:
            qi = np.array(sorted(q_anc_u), dtype=np.int32)
            q_vec[qi] = np.power(self.ic_anc_vec[qi], 1.35)
        q_norm = float(np.linalg.norm(q_vec)) + 1e-9
        dots = self.H_dag @ q_vec
        s_bidi = dots / (np.power(q_norm, 0.55) * np.power(self.h_norms + 0.40 * self.med_hnorm, 0.45))
        comb_z = zscore_1d(0.65 * s_mica + 0.35 * zscore_1d(s_bidi))

        act = np.maximum(0.0, comb_z - 1.6)
        if np.count_nonzero(act) < 3:
            th = np.partition(comb_z, -10)[-10]
            act = np.maximum(0.0, comb_z - th + 0.25)
        if np.count_nonzero(act) > 50:
            th = np.partition(act, -50)[-50]
            act = np.where(act >= th, act, 0.0)
        psi = np.power(act, 2.0)
        psi /= psi.sum() + 1e-12
        nz_psi = np.flatnonzero(psi)
        psi_nz = psi[nz_psi]

        s_ed = np.asarray(self.K_ed_csc[:, nz_psi] @ psi_nz).ravel()
        s_tot = np.asarray(self.K_tot_csc[:, nz_psi] @ psi_nz).ravel()
        f2 = norm_pos_scale(0.70 * norm_pos_scale(s_ed) + 0.30 * norm_pos_scale(s_tot))

        s_go = np.asarray(self.K_go_csc[:, nz_psi] @ psi_nz).ravel()
        f3 = norm_pos_scale(s_go)

        sum_dis = np.zeros(self.n_dis, dtype=np.float64)
        for ti in tis:
            sum_dis += self._get_dis_llr_row(ti)
        d_sc = sum_dis * self.dis_pen
        g_sc = np.zeros(len(self.ann_gidxs), dtype=np.float64)
        np.maximum.at(g_sc, self.d_rows, d_sc[self.d_cols])
        gz = zscore_1d(g_sc)
        idx_top = np.sort(np.argpartition(gz, -60)[-60:])
        psi_top = np.exp(3.0 * 0.85 * (gz[idx_top] - gz[idx_top].max()))
        l3_mod = np.power(np.asarray(self.K3_mod[:, idx_top] @ psi_top).ravel(), 1.0 / 3.0)
        l3_ed = np.power(np.asarray(self.K3_ed[:, idx_top] @ psi_top).ravel(), 1.0 / 3.0)
        f4 = norm_pos_scale(0.65 * norm_pos_scale(l3_mod) + 0.35 * norm_pos_scale(l3_ed))

        z1_std = zscore_1d(c1)
        x1_pos = np.maximum(0.0, z1_std - 1.2)
        if np.count_nonzero(x1_pos) > 80:
            thx = np.partition(x1_pos, -80)[-80]
            x1_pos = np.where(x1_pos >= thx, x1_pos, 0.0)
        x1_vec = np.power(x1_pos, 2.0)
        x1_sum = float(x1_vec.sum())
        if x1_sum > 1e-12:
            nz_x1 = np.flatnonzero(x1_vec)
            raw_b = np.asarray(self.K_bridge_csc[:, nz_x1] @ (x1_vec[nz_x1] / x1_sum)).ravel()
            f5 = norm_pos_scale(np.maximum(0.0, raw_b - self.mu_bridge) / self.sd_bridge)
        else:
            f5 = np.zeros(self.n_genes, dtype=np.float64)

        z_xs = np.maximum(np.maximum(0.0, f1), 0.75 * np.maximum(0.0, f5))
        z_hu = np.maximum(0.0, (f2 + f3 + f4) / 3.0)
        f6 = norm_pos_scale(np.log1p(z_xs) * np.log1p(z_hu))

        return np.vstack([f1, f2, f3, f4, f5, f6])

    def score_19296(self, obs_hpo_terms: Sequence[str], weights: Sequence[float] | None = None) -> np.ndarray:
        w = self.weights if weights is None else np.asarray(weights, dtype=np.float64)
        return np.round(w @ self.compute_6_channels(obs_hpo_terms), 11)

    def rank_all_19296_genes(self, obs_hpo_terms: Sequence[str]) -> list[tuple[str, float]]:
        """
        Blind Ranker Contract: takes ONLY `obs_hpo_terms` (`Sequence[str]`) and returns
        a deterministic full ranking of all 19,296 HGNC protein-coding genes.
        """
        sc = self.score_19296(obs_hpo_terms)
        order = np.lexsort((np.arange(self.n_genes), -sc))
        return [(self.pc_hgnc[int(i)], float(sc[int(i)])) for i in order]
