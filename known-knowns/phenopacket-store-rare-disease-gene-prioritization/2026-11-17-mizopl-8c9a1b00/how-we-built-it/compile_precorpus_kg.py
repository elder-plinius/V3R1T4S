#!/usr/bin/env python3
"""
Standalone Pre-Corpus (`< 2026-06-09`) Upstream Fetcher & Knowledge-Graph Compiler
for fresh-machine reproduction when `~/.cache/phenopacket_p2` is not yet populated.

Every upstream archive is verified against its pinned SHA-256 digest before parsing,
all `1,755` corpus PMIDs from `phenopacket-store 0.1.27` are purged from retained edges,
`STRING v12.0` `textmining` is set identically to `0`, all `.gz` outputs are written
with deterministic `mtime=0` / empty-filename GZIP headers, and all 4 decompressed
payload SHA-256 digests are verified before exit.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import io
import json
import math
import re
import shutil
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

PINNED_MANIFEST = json.loads(r"""{
  "upstream_files": {
    "all_phenopackets_0.1.27.zip": [
      "https://github.com/monarch-initiative/phenopacket-store/releases/download/0.1.27/all_phenopackets.zip",
      "d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a"
    ],
    "hp_v2026-06-06.obo": [
      "https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-06/hp.obo",
      "ddc8f8a99844b61cd27cdc17958a954dce55349d4d03f318e71426e1550b7f36"
    ],
    "phenotype_v2026-06-06.hpoa": [
      "https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-06/phenotype.hpoa",
      "9e10da9c4b92c2d58f65e2fbd005a8511b5bfde43dd4a026564c72cf2918fbb3"
    ],
    "genes_to_phenotype_v2026-06-06.txt": [
      "https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-06/genes_to_phenotype.txt",
      "857cd3c28ce46b3fa5cb65f38a88ed8e4ee3c8c9c92463066ce7e7e3aa9b8ed4"
    ],
    "genes_to_disease_v2026-06-06.txt": [
      "https://github.com/obophenotype/human-phenotype-ontology/releases/download/v2026-06-06/genes_to_disease.txt",
      "81e8d2e0bc1c1052c383614ad85388325deeacb4b9478c6d9585597f45602bac"
    ],
    "hgnc_complete_set_2026-06-01.txt": [
      "https://storage.googleapis.com/public-download-files/hgnc/archive/archive/monthly/tsv/hgnc_complete_set_2026-05-01.txt",
      "8a56d4af702d74364813fc764a96034a349a36e011fb54b3952ab53ae043dd8e"
    ]
  },
  "raw_kg_files": {
    "monarch-kg_2026-05-09.tar.gz": [
      "https://data.monarchinitiative.org/monarch-kg/2026-05-09/monarch-kg.tar.gz",
      "85143b5e5e9380d2e5c37bb561a0890269d5b8f9627bb58417f7d46fa83263e4"
    ],
    "upheno-base-with-bridge_v2025-10-12.obo": [
      "https://github.com/obophenotype/upheno/releases/download/v2025-10-12/upheno-base-with-bridge.obo",
      "1df3d294b3739429370e0d1770d65094ec2bc8ae53b5ce3a767795fecd1b0efa"
    ],
    "9606.protein.links.detailed.v12.0.txt.gz": [
      "https://stringdb-downloads.org/download/protein.links.detailed.v12.0/9606.protein.links.detailed.v12.0.txt.gz",
      "28a2ea3b22c964e691c0f2f934c5e3e397a4b0a12c833d8787fa02b7847b91b6"
    ],
    "9606.protein.info.v12.0.txt.gz": [
      "https://stringdb-downloads.org/download/protein.info.v12.0/9606.protein.info.v12.0.txt.gz",
      "144de4b0d98c6a7dfde6ddc2591cf88657f27b989eadff4f501450c3ed1f0f1c"
    ],
    "9606.protein.aliases.v12.0.txt.gz": [
      "https://stringdb-downloads.org/download/protein.aliases.v12.0/9606.protein.aliases.v12.0.txt.gz",
      "b65f730b993ed0c1bd72edf4565d3d425db42861101b29699704810e8f125680"
    ],
    "goa_human_2026-05-19.gaf.gz": [
      "https://release.geneontology.org/2026-05-19/annotations/goa_human.gaf.gz",
      "db472faff1785878521693af62646546cea6af4a386609dd01c72c0554a46a30"
    ],
    "go-basic_2026-05-19.obo": [
      "https://release.geneontology.org/2026-05-19/ontology/go-basic.obo",
      "923645000afcb1df0e72e252b64950b1c2bcc98c9393fec8c1dd1a0f7c9d4d77"
    ],
    "upheno-equivalence-model_v2025-10-12.obo": [
      "https://github.com/obophenotype/upheno/releases/download/v2025-10-12/upheno-equivalence-model.obo",
      "f7a41cd8557e147add80628593d0441c1278e83ab37d66063359f5eb0c5b82e1"
    ]
  },
  "expected_uncompressed_kg_sha256": {
    "xspec_ontology.json.gz": "e1436e5a7586213a306b9ab6fb794ab3a6f2ce787812ea9be2c3f27a35360944",
    "xspec_orth_pheno.tsv.gz": "7f59c2451018af545deee1a77d7a4926d8816da71adf438b8d3f31bb2d3543fb",
    "string_v12_notm_edges.tsv.gz": "ff38052116c6b4fa95e37e418bade7026b272b2bd2f5601639887559d34c8475",
    "go_2026_05_19_clean.json.gz": "3cb6c0b630c8c660828ddcaa4014c6831526d01e965e54bcd321493113bcb135"
  }
}""")
PMID_RX = re.compile(r"PMID\s*:?\s*(\d+)", re.I)
ALLOWED_ONT_PFX = {"HP", "MP", "ZP", "UPHENO", "WBPhenotype", "FBcv", "FYPO", "XPO", "DDPHENO"}
NONHUMAN_PHENO_PFX = {"MP", "ZP", "WBPhenotype", "FBcv", "FYPO", "XPO", "DDPHENO"}
FORBIDDEN_PHENO_SOURCES = {
    "infores:phenopacket-store",
    "infores:hpo-annotations",
    "infores:omim",
    "infores:orphanet",
    "infores:mondo",
    "infores:cureid",
    "infores:clingen",
}
EXP_GO_EVID = {"EXP", "IDA", "IPI", "IMP", "IGI", "IEP", "HTP", "HDA", "HMP", "HGI", "HEP", "IC", "TAS"}


def sha256_path(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_gzip_payload(p: Path) -> str:
    return hashlib.sha256(gzip.decompress(p.read_bytes())).hexdigest()


def write_gzip_deterministic_bytes(path: Path, payload: bytes) -> None:
    with path.open("wb") as raw_f:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_f, mtime=0) as gz_f:
            gz_f.write(payload)


def fetch_verified(url: str, dst: Path, expected_sha256: str) -> None:
    if dst.is_file() and sha256_path(dst) == expected_sha256:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "MARG-P2-Reproducer/1.0"})
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=300) as r, dst.open("wb") as out:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
            out.write(chunk)
    actual = h.hexdigest()
    if actual != expected_sha256:
        dst.unlink(missing_ok=True)
        raise RuntimeError(f"SHA-256 mismatch fetching {url}: {actual} != {expected_sha256}")


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        p = self.parent.get(x, x)
        if p != x:
            p = self.find(p)
            self.parent[x] = p
        else:
            self.parent.setdefault(x, x)
        return p

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return

        def rk(s: str) -> tuple[int, str]:
            px = s.split(":", 1)[0]
            return (0 if px == "HP" else (1 if px == "UPHENO" else 2), s)

        if rk(rb) < rk(ra):
            ra, rb = rb, ra
        self.parent[rb] = ra


def collapse_tarjan_sccs(uf: UnionFind, raw_isa: list[tuple[str, str]]) -> None:
    cp_raw: dict[str, set[str]] = collections.defaultdict(set)
    all_terms = set(uf.parent.keys())
    for c_raw, p_raw in raw_isa:
        rc, rp = uf.find(c_raw), uf.find(p_raw)
        if rc != rp:
            cp_raw[rc].add(rp)
    all_reps = {uf.find(t) for t in all_terms} | set(cp_raw.keys())
    for vs in list(cp_raw.values()):
        all_reps.update(vs)

    sys.setrecursionlimit(max(80000, len(all_reps) + 2000))
    ix_c = 0
    idxs: dict[str, int] = {}
    low: dict[str, int] = {}
    stk: list[str] = []
    on_s: set[str] = set()

    def strongconnect(v: str) -> None:
        nonlocal ix_c
        idxs[v] = low[v] = ix_c
        ix_c += 1
        stk.append(v)
        on_s.add(v)
        for w in cp_raw.get(v, ()):
            if w not in idxs:
                strongconnect(w)
                low[v] = min(low[v], low[w])
            elif w in on_s:
                low[v] = min(low[v], idxs[w])
        if low[v] == idxs[v]:
            scc = []
            while True:
                w = stk.pop()
                on_s.remove(w)
                scc.append(w)
                if w == v:
                    break
            if len(scc) > 1:
                base = scc[0]
                for ot in scc[1:]:
                    uf.union(base, ot)

    for v in sorted(all_reps):
        if v not in idxs:
            strongconnect(v)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", type=Path, default=Path.home() / ".cache" / "phenopacket_p2")
    args = ap.parse_args()
    cdir: Path = args.cache_dir
    kg_dir = cdir / "compiled_kg"
    raw_dir = cdir / "_raw_tmp"
    kg_dir.mkdir(parents=True, exist_ok=True)

    for fn, (url, sha) in PINNED_MANIFEST["upstream_files"].items():
        fetch_verified(url, cdir / fn, sha)

    exp_uncomp: dict[str, str] = PINNED_MANIFEST["expected_uncompressed_kg_sha256"]
    if all(
        (kg_dir / fn).is_file() and sha256_gzip_payload(kg_dir / fn) == exp_sha
        for fn, exp_sha in exp_uncomp.items()
    ):
        return 0

    try:
        for fn, (url, sha) in PINNED_MANIFEST["raw_kg_files"].items():
            fetch_verified(url, raw_dir / fn, sha)

        # 0. Parse HPO OBO, two-pass HGNC 19,296 universe, and 1,755 corpus PMIDs
        parents_hpo: dict[str, set[str]] = collections.defaultdict(set)
        children_hpo: dict[str, set[str]] = collections.defaultdict(set)
        alt_map: dict[str, str] = {}
        cid, alts, repl, obs = "", [], "", False

        def flush_h() -> None:
            nonlocal cid, alts, repl, obs
            if cid:
                if obs and repl:
                    alt_map[cid] = repl
                for a in alts:
                    alt_map[a] = repl if (obs and repl) else cid
            cid, alts, repl, obs = "", [], "", False

        with (cdir / "hp_v2026-06-06.obo").open(encoding="utf-8") as f:
            for raw in f:
                s = raw.strip()
                if s == "[Term]" or s.startswith("[Typedef]"):
                    flush_h()
                    if s.startswith("[Typedef]"):
                        break
                    continue
                if s.startswith("id: HP:"):
                    cid = s[4:].strip()
                elif s.startswith("alt_id: HP:"):
                    alts.append(s[8:].strip())
                elif s.startswith("is_a: HP:") and cid:
                    p = s[6:].split("!")[0].strip()
                    parents_hpo[cid].add(p)
                    children_hpo[p].add(cid)
                elif s == "is_obsolete: true":
                    obs = True
                elif s.startswith("replaced_by: HP:"):
                    repl = s[13:].strip()
            flush_h()

        pheno_sub: set[str] = set()
        dq = collections.deque(["HP:0000118"])
        while dq:
            u = dq.popleft()
            if u not in pheno_sub:
                pheno_sub.add(u)
                dq.extend(v for v in children_hpo.get(u, ()) if v not in pheno_sub)

        pc_raw: list[str] = []
        sym_to_h: dict[str, str] = {}
        ent_to_h: dict[str, str] = {}
        with (cdir / "hgnc_complete_set_2026-06-01.txt").open(encoding="utf-8") as f:
            cols = f.readline().rstrip("\n").split("\t")
            ih, isym, iloc, ient = (
                cols.index("hgnc_id"),
                cols.index("symbol"),
                cols.index("locus_group"),
                cols.index("entrez_id"),
            )
            for ln in f:
                p = ln.rstrip("\n").split("\t")
                if len(p) <= max(ih, isym, iloc, ient) or p[iloc] != "protein-coding gene":
                    continue
                h = p[ih]
                pc_raw.append(h)
                sym_to_h[p[isym]] = h
                if p[ient]:
                    ent_to_h[p[ient]] = h

        pc_hgnc = sorted(set(pc_raw), key=lambda x: int(x.split(":")[1]))
        h_to_idx = {h: i for i, h in enumerate(pc_hgnc)}

        uni_to_h: dict[str, str] = {}
        prev_cnt: collections.Counter[str] = collections.Counter()
        prev_cand: dict[str, str] = {}
        mgi_orth: dict[str, set[str]] = collections.defaultdict(set)
        rgd_orth: dict[str, set[str]] = collections.defaultdict(set)
        with (cdir / "hgnc_complete_set_2026-06-01.txt").open(encoding="utf-8") as f:
            cols = f.readline().rstrip("\n").split("\t")
            ih, iloc, iprev, iuni, imgd, irgd = (
                cols.index("hgnc_id"),
                cols.index("locus_group"),
                cols.index("prev_symbol"),
                cols.index("uniprot_ids"),
                cols.index("mgd_id"),
                cols.index("rgd_id"),
            )
            for ln in f:
                p = ln.rstrip("\n").split("\t")
                if len(p) <= max(ih, iloc, iprev, iuni, imgd, irgd) or p[iloc] != "protein-coding gene":
                    continue
                h = p[ih]
                if h not in h_to_idx:
                    continue
                for u in p[iuni].strip('"').split("|"):
                    u = u.strip()
                    if u:
                        uni_to_h[u] = h
                for ps in p[iprev].strip('"').split("|"):
                    ps = ps.strip()
                    if ps and ps not in sym_to_h:
                        prev_cnt[ps] += 1
                        prev_cand[ps] = h
                for m in p[imgd].strip('"').split("|"):
                    m = m.strip()
                    if m.startswith("MGI:"):
                        mgi_orth[h].add(m)
                for r in p[irgd].strip('"').split("|"):
                    r = r.strip()
                    if r.startswith("RGD:"):
                        rgd_orth[h].add(r)
        prev_to_h = {s: h for s, h in prev_cand.items() if prev_cnt[s] == 1}

        corpus_pmids: set[str] = set()
        with zipfile.ZipFile(cdir / "all_phenopackets_0.1.27.zip") as zf:
            for n in sorted(zf.namelist()):
                if n.endswith(".json"):
                    corpus_pmids.update(PMID_RX.findall(zf.read(n).decode("utf-8")))

        def norm_term(tid: str) -> str | None:
            if ":" not in tid:
                return None
            px = tid.split(":", 1)[0]
            if px not in ALLOWED_ONT_PFX:
                return None
            if px == "HP":
                tid = alt_map.get(tid, tid)
                if tid not in pheno_sub:
                    return None
            return tid

        # 1A. Step-1 XSpec reduction: HPO + upheno-base-with-bridge.obo + monarch-kg.tar.gz
        uf1 = UnionFind()
        raw_isa1: list[tuple[str, str]] = []
        for child, pset in parents_hpo.items():
            if child in pheno_sub:
                uf1.find(child)
                for par in pset:
                    if par in pheno_sub:
                        uf1.find(par)
                        raw_isa1.append((child, par))

        cur_id1, is_obs1, cur_edges1 = "", False, []

        def flush_up1() -> None:
            nonlocal cur_id1, is_obs1, cur_edges1
            if cur_id1 and not is_obs1:
                cid1 = norm_term(cur_id1)
                if cid1:
                    uf1.find(cid1)
                    for tgt in cur_edges1:
                        tid1 = norm_term(tgt)
                        if tid1:
                            uf1.find(tid1)
                            raw_isa1.append((cid1, tid1))
            cur_id1, is_obs1, cur_edges1 = "", False, []

        with (raw_dir / "upheno-base-with-bridge_v2025-10-12.obo").open(encoding="utf-8") as f:
            for raw in f:
                s = raw.strip()
                if s == "[Term]" or s.startswith("[Typedef]"):
                    flush_up1()
                    if s.startswith("[Typedef]"):
                        break
                    continue
                if s.startswith("id: ") and ":" in s[4:]:
                    cur_id1 = s[4:].strip()
                elif s == "is_obsolete: true":
                    is_obs1 = True
                elif s.startswith("is_a: ") and cur_id1:
                    tgt = s[6:].split("!")[0].split("{")[0].strip()
                    if ":" in tgt:
                        cur_edges1.append(tgt)
            flush_up1()

        nh_gene_tax: dict[str, str] = {}
        nh_geno_tax: dict[str, str] = {}
        hnode_to_h = {h: h for h in pc_hgnc}
        for ent, h in ent_to_h.items():
            hnode_to_h[f"NCBIGene:{ent}"] = h

        orth_pairs: set[tuple[str, str]] = set()
        for h, ms in mgi_orth.items():
            for m in ms:
                nh_gene_tax.setdefault(m, "NCBITaxon:10090")
                orth_pairs.add((h, m))
        for h, rs in rgd_orth.items():
            for r in rs:
                nh_gene_tax.setdefault(r, "NCBITaxon:10116")
                orth_pairs.add((h, r))

        geno_to_gene: dict[str, set[str]] = collections.defaultdict(set)
        raw_pheno: list[tuple[str, str]] = []

        with tarfile.open(raw_dir / "monarch-kg_2026-05-09.tar.gz", "r:gz") as tf:
            for mem in tf:
                f = tf.extractfile(mem)
                if f is None:
                    continue
                f.readline()
                if "nodes" in mem.name:
                    for raw in f:
                        p = raw.decode("utf-8", "replace").rstrip("\n").split("\t")
                        if len(p) <= 12:
                            continue
                        nid, cat, tax, xref = p[0], p[1], p[8], p[12]
                        if cat == "biolink:Gene":
                            if tax == "NCBITaxon:9606" or nid.startswith("HGNC:"):
                                if nid in h_to_idx:
                                    hnode_to_h[nid] = nid
                                elif xref:
                                    for tok in xref.strip("[]").replace("'", "").split(","):
                                        tok = tok.strip()
                                        if tok in h_to_idx:
                                            hnode_to_h[nid] = tok
                                            break
                            elif tax and tax != "NCBITaxon:9606":
                                nh_gene_tax[nid] = tax
                        elif cat in ("biolink:Genotype", "biolink:SequenceVariant") and tax and tax != "NCBITaxon:9606":
                            nh_geno_tax[nid] = tax
                elif "edges" in mem.name:
                    for raw in f:
                        p = raw.decode("utf-8", "replace").rstrip("\n").split("\t")
                        if len(p) <= 33:
                            continue
                        pred, src, pubs, neg, subj, obj = p[1], p[7], p[15], p[17], p[32], p[33]
                        if pred == "biolink:orthologous_to":
                            h1, h2 = hnode_to_h.get(subj), hnode_to_h.get(obj)
                            if h1 and obj in nh_gene_tax:
                                orth_pairs.add((h1, obj))
                            elif h2 and subj in nh_gene_tax:
                                orth_pairs.add((h2, subj))
                        elif pred in ("biolink:is_sequence_variant_of", "biolink:has_sequence_variant", "biolink:has_gene"):
                            if subj in nh_geno_tax and obj in nh_gene_tax:
                                geno_to_gene[subj].add(obj)
                            elif obj in nh_geno_tax and subj in nh_gene_tax:
                                geno_to_gene[obj].add(subj)
                        elif pred == "biolink:has_phenotype":
                            if neg.lower() == "true" or src in FORBIDDEN_PHENO_SOURCES or ":" not in obj:
                                continue
                            if obj.split(":", 1)[0] not in NONHUMAN_PHENO_PFX:
                                continue
                            if subj.startswith(("HGNC:", "MONDO:", "OMIM:", "ORPHA:", "phenopacket.store:")):
                                continue
                            if pubs and (set(PMID_RX.findall(pubs)) & corpus_pmids):
                                continue
                            if subj in nh_gene_tax or subj in nh_geno_tax:
                                raw_pheno.append((subj, obj))
                        elif pred == "biolink:same_as":
                            su, ou = norm_term(subj), norm_term(obj)
                            if su and ou:
                                uf1.union(su, ou)
                        elif pred == "biolink:subclass_of":
                            su, ou = norm_term(subj), norm_term(obj)
                            if su and ou:
                                uf1.find(su)
                                uf1.find(ou)
                                raw_isa1.append((su, ou))

        orth_wh = {m for _, m in orth_pairs}
        nh_phenos: dict[str, set[str]] = collections.defaultdict(set)
        for subj, ph in raw_pheno:
            if subj in orth_wh:
                nh_phenos[subj].add(ph)
            elif subj in geno_to_gene:
                for mg in geno_to_gene[subj]:
                    if mg in orth_wh:
                        nh_phenos[mg].add(ph)

        collapse_tarjan_sccs(uf1, raw_isa1)

        cp1: dict[str, list[str]] = collections.defaultdict(list)
        for c_raw, p_raw in raw_isa1:
            rc, rp = uf1.find(c_raw), uf1.find(p_raw)
            if rc != rp:
                cp1[rc].append(rp)
        old_parents = {k: sorted(set(v)) for k, v in cp1.items()}

        used_nh = set()
        for ps in nh_phenos.values():
            used_nh.update(ps)
        old_t2c = {t: uf1.find(t) for t in sorted(pheno_sub | used_nh)}

        deg_m: collections.Counter[str] = collections.Counter()
        deg_ht: collections.Counter[tuple[str, str]] = collections.Counter()
        for h, m in orth_pairs:
            tx = nh_gene_tax.get(m, "OTHER")
            deg_m[m] += 1
            deg_ht[(h, tx)] += 1

        step1_orth_records: dict[int, list[tuple[str, str, str, list[str]]]] = collections.defaultdict(list)
        for h, m in sorted(orth_pairs):
            ps = nh_phenos.get(m)
            if not ps:
                continue
            cs_old = sorted({uf1.find(t) for t in ps})
            if not cs_old:
                continue
            gi = h_to_idx[h]
            tx = nh_gene_tax.get(m, "OTHER")
            w_r = round(1.0 / math.sqrt(max(1, deg_m[m]) * max(1, deg_ht[(h, tx)])), 6)
            step1_orth_records[gi].append((m, tx, f"{w_r:.6f}", cs_old))

        # 1B. Step-2 XSpec reduction: merge upheno-equivalence-model.obo onto Step-1 graph
        uf2 = UnionFind()
        raw_isa2: list[tuple[str, str]] = []
        for t, c in old_t2c.items():
            uf2.union(t, c)
        for c, pars in old_parents.items():
            uf2.find(c)
            for p in pars:
                uf2.find(p)
                raw_isa2.append((c, p))

        cur_id2, is_obs2, cur_isa2, cur_eq2 = "", False, [], []

        def flush_up2() -> None:
            nonlocal cur_id2, is_obs2, cur_isa2, cur_eq2
            if cur_id2 and not is_obs2:
                cid2 = norm_term(cur_id2)
                if cid2:
                    uf2.find(cid2)
                    for tgt in cur_isa2:
                        tid2 = norm_term(tgt)
                        if tid2 and tid2 != cid2:
                            uf2.find(tid2)
                            raw_isa2.append((cid2, tid2))
                    for eq in cur_eq2:
                        eid2 = norm_term(eq)
                        if eid2 and eid2 != cid2:
                            uf2.union(cid2, eid2)
            cur_id2, is_obs2, cur_isa2, cur_eq2 = "", False, [], []

        with (raw_dir / "upheno-equivalence-model_v2025-10-12.obo").open(encoding="utf-8", errors="replace") as f:
            for raw in f:
                s = raw.strip()
                if s == "[Term]" or s.startswith("[Typedef]"):
                    flush_up2()
                    continue
                if s.startswith("id: "):
                    cur_id2 = s[4:].strip()
                elif s == "is_obsolete: true":
                    is_obs2 = True
                elif s.startswith("is_a: ") and cur_id2:
                    cur_isa2.append(s[6:].split("!")[0].split("{")[0].strip())
                elif (s.startswith("equivalent_to: ") or s.startswith("xref: ")) and cur_id2:
                    tgt = s.split(": ", 1)[1].split("!")[0].split("{")[0].strip()
                    if ":" in tgt and tgt.split(":", 1)[0] in ALLOWED_ONT_PFX:
                        cur_eq2.append(tgt)
            flush_up2()

        collapse_tarjan_sccs(uf2, raw_isa2)

        cp2: dict[str, list[str]] = {}
        for c_raw, p_raw in raw_isa2:
            rc, rp = uf2.find(c_raw), uf2.find(p_raw)
            if rc != rp:
                cp2.setdefault(rc, []).append(rp)
        concept_parents_clean = {k: sorted(set(vs)) for k, vs in cp2.items()}

        used_terms = set(pheno_sub) | set(old_t2c.keys())
        orth_lines = ["gidx\thgnc_id\torth_id\ttaxon\torth_weight\tdirect_concepts\n"]
        for gi in sorted(step1_orth_records):
            hid = pc_hgnc[gi]
            for mid, tx, w_str, cs_old in step1_orth_records[gi]:
                used_terms.update(cs_old)
                cs_new = sorted({uf2.find(c) for c in cs_old})
                orth_lines.append(f"{gi}\t{hid}\t{mid}\t{tx}\t{w_str}\t{'|'.join(cs_new)}\n")

        write_gzip_deterministic_bytes(kg_dir / "xspec_orth_pheno.tsv.gz", "".join(orth_lines).encode("utf-8"))

        new_t2c = {t: uf2.find(t) for t in sorted(used_terms)}
        ont_bytes = json.dumps(
            {"term_to_concept": new_t2c, "concept_parents": concept_parents_clean},
            separators=(",", ":"),
        ).encode("utf-8")
        write_gzip_deterministic_bytes(kg_dir / "xspec_ontology.json.gz", ont_bytes)

        # 2. Compile STRING v12.0 (textmining == 0 identically)
        ensp_h: dict[str, str] = {}
        ensp_e: dict[str, str] = {}
        ensp_gi: dict[str, int] = {}
        with gzip.open(raw_dir / "9606.protein.aliases.v12.0.txt.gz", "rt", encoding="utf-8", errors="replace") as f:
            for ln in f:
                if ln.startswith("#"):
                    continue
                p = ln.rstrip("\n").split("\t")
                if len(p) >= 3:
                    if p[1] in h_to_idx:
                        ensp_h[p[0]] = p[1]
                    elif p[2] == "Ensembl_HGNC_entrez_id" and p[1] in ent_to_h:
                        ensp_e[p[0]] = ent_to_h[p[1]]
        with gzip.open(raw_dir / "9606.protein.info.v12.0.txt.gz", "rt", encoding="utf-8", errors="replace") as f:
            for ln in f:
                if ln.startswith("#"):
                    continue
                p = ln.rstrip("\n").split("\t")
                h = ensp_h.get(p[0]) or ensp_e.get(p[0]) or sym_to_h.get(p[1]) or prev_to_h.get(p[1])
                if h and h in h_to_idx:
                    ensp_gi[p[0]] = h_to_idx[h]

        best_e: dict[tuple[int, int], tuple[float, float, float]] = {}
        inv_1mp = 1.0 / (1.0 - 0.041)

        def np_fn(x: int) -> float:
            return 0.0 if x <= 41 else (x * 0.001 - 0.041) * inv_1mp

        with gzip.open(raw_dir / "9606.protein.links.detailed.v12.0.txt.gz", "rt", encoding="utf-8", errors="replace") as f:
            f.readline()
            for ln in f:
                p = ln.split()
                if len(p) < 10:
                    continue
                u, v = ensp_gi.get(p[0]), ensp_gi.get(p[1])
                if u is None or v is None or u == v:
                    continue
                if u > v:
                    u, v = v, u
                c_nb, c_fu, c_co, c_cx, c_ex, c_db = (
                    int(p[2]), int(p[3]), int(p[4]), int(p[5]), int(p[6]), int(p[7])
                )
                if c_nb == 0 and c_fu == 0 and c_co == 0 and c_cx == 0 and c_ex == 0 and c_db == 0:
                    continue
                p_nb, p_fu, p_co, p_cx, p_ex, p_db = (
                    np_fn(c_nb), np_fn(c_fu), np_fn(c_co), np_fn(c_cx), np_fn(c_ex), np_fn(c_db)
                )
                sed = 1.0 - (1.0 - p_ex) * (1.0 - p_db)
                sfn = 1.0 - (1.0 - p_cx) * (1.0 - p_co) * (1.0 - p_fu) * (1.0 - p_nb)
                stot = 1.0 - (1.0 - sed) * (1.0 - sfn)
                if stot >= 0.15:
                    prev = best_e.get((u, v))
                    if prev is None or stot > prev[0]:
                        best_e[(u, v)] = (stot, sed, sfn)

        with (kg_dir / "string_v12_notm_edges.tsv.gz").open("wb") as raw_f:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw_f, mtime=0) as gz_f:
                with io.TextIOWrapper(gz_f, encoding="utf-8", newline="\n") as tf_out:
                    tf_out.write("u_idx\tv_idx\ts_notm\ts_exp_db\ts_func\n")
                    for (u, v), (st, se, sf) in sorted(best_e.items()):
                        tf_out.write(f"{u}\t{v}\t{st:.5f}\t{se:.5f}\t{sf:.5f}\n")

        # 3. Compile GO 2026-05-19 (0 corpus PMIDs)
        go_ns: dict[str, str] = {}
        go_pr: dict[str, list[str]] = collections.defaultdict(list)
        go_alt: dict[str, str] = {}
        ns_s = {"cellular_component": "C", "biological_process": "P", "molecular_function": "F"}
        gi_c, gn_c, ga_c, gr_c, go_ob, grels = "", "", [], "", False, []

        def fl_g() -> None:
            nonlocal gi_c, gn_c, ga_c, gr_c, go_ob, grels
            if gi_c:
                if go_ob and gr_c:
                    go_alt[gi_c] = gr_c
                for a in ga_c:
                    go_alt[a] = gr_c if (go_ob and gr_c) else gi_c
                if not go_ob and gn_c in ns_s:
                    go_ns[gi_c] = ns_s[gn_c]
                    go_pr[gi_c].extend(grels)
            gi_c, gn_c, ga_c, gr_c, go_ob, grels = "", "", [], "", False, []

        with (raw_dir / "go-basic_2026-05-19.obo").open(encoding="utf-8") as f:
            for raw in f:
                s = raw.strip()
                if s == "[Term]" or s.startswith("[Typedef]"):
                    fl_g()
                    if s.startswith("[Typedef]"):
                        break
                    continue
                if s.startswith("id: GO:"):
                    gi_c = s[4:].strip()
                elif s.startswith("namespace: "):
                    gn_c = s.split("namespace: ", 1)[1].strip()
                elif s.startswith("alt_id: GO:"):
                    ga_c.append(s.split("alt_id: ", 1)[1].strip())
                elif s == "is_obsolete: true":
                    go_ob = True
                elif s.startswith("replaced_by: GO:"):
                    gr_c = s.split("replaced_by: ", 1)[1].strip()
                elif s.startswith("is_a: GO:"):
                    grels.append(s[6:].split("!")[0].strip())
                elif s.startswith("relationship: part_of GO:"):
                    grels.append(s.split("relationship: part_of ", 1)[1].split("!")[0].strip())
            fl_g()

        go_pars: dict[str, list[str]] = {}
        for g_id, rl in go_pr.items():
            asp = go_ns.get(g_id)
            ps = sorted({go_alt.get(t, t) for t in rl if go_ns.get(go_alt.get(t, t)) == asp and go_alt.get(t, t) != g_id})
            if ps:
                go_pars[g_id] = ps

        gene_go_w: dict[int, dict[str, float]] = collections.defaultdict(dict)
        with gzip.open(raw_dir / "goa_human_2026-05-19.gaf.gz", "rt", encoding="utf-8", errors="replace") as f:
            for ln in f:
                if ln.startswith("!"):
                    continue
                p = ln.rstrip("\n").split("\t")
                if len(p) < 9 or "NOT" in p[3].split("|") or p[6] == "ND":
                    continue
                if set(PMID_RX.findall(p[5])) & corpus_pmids:
                    continue
                h = uni_to_h.get(p[1]) or sym_to_h.get(p[2]) or prev_to_h.get(p[2])
                gid = go_alt.get(p[4], p[4])
                if h and h in h_to_idx and gid in go_ns:
                    w = 1.0 if p[6] in EXP_GO_EVID else 0.65
                    gi = h_to_idx[h]
                    if w > gene_go_w[gi].get(gid, 0.0):
                        gene_go_w[gi][gid] = w

        go_bytes = json.dumps(
            {
                "go_aspect": go_ns,
                "go_parents": go_pars,
                "gene_go": {str(k): sorted(v.items()) for k, v in sorted(gene_go_w.items())},
            },
            separators=(",", ":"),
        ).encode("utf-8")
        write_gzip_deterministic_bytes(kg_dir / "go_2026_05_19_clean.json.gz", go_bytes)
    finally:
        shutil.rmtree(raw_dir, ignore_errors=True)

    for fn, exp_sha in exp_uncomp.items():
        actual = sha256_gzip_payload(kg_dir / fn)
        if actual != exp_sha:
            raise RuntimeError(f"Compiled KG uncompressed payload SHA-256 mismatch on {fn}: {actual} != {exp_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
