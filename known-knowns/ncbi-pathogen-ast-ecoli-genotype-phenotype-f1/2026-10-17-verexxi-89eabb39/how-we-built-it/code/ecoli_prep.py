"""Build the eligible E. coli/Shigella isolate table and the long R/S phenotype table from a frozen NCBI Pathogen
Detection metadata TSV, with the paper's (PMC13513162) eligibility and phenotype-mapping rules:
- eligible: assembly accession, AMR genotypes and AST phenotypes all present (non-NULL)  [reproduces S1 flags exactly]
- phenotypes: AST field split into name=CALL entries; only R and S kept; the eight antibiotics; exact duplicate
  isolate-antibiotic-call rows collapsed, non-identical duplicates retained                [reproduces S9 exactly]
- SNP cluster: PDS_acc from Clusters/*.cluster_list.tsv joined on target_acc; isolates without a PDS are singletons.
- split: an isolate is TEST iff int(sha256('V3R1T4S-ecoli-2026-10-16|' + cluster), 16) % 100 < 20 (whole clusters).
usage: ecoli_prep.py METADATA_TSV CLUSTER_LIST_TSV OUTDIR"""
import sys, os, hashlib, pandas as pd, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ecoli_rules import ANTIBIOTICS
meta, cl, out = sys.argv[1:4]; os.makedirs(out, exist_ok=True)
cols = ["target_acc", "asm_acc", "biosample_acc", "AST_phenotypes", "AMR_genotypes", "amrfinder_version", "scientific_name",
        "collection_date", "epi_type", "isolation_source", "geo_loc_name", "host", "source_type", "computed_types"]
df = pd.read_csv(meta, sep="\t", usecols=cols, dtype=str, keep_default_na=False)
n_all = len(df)
def present(s): return s.str.strip().ne("") & s.str.strip().ne("NULL")
elig = df[present(df.asm_acc) & present(df.AMR_genotypes) & present(df.AST_phenotypes)].copy()
c = pd.read_csv(cl, sep="\t", dtype=str)
pds = c.drop_duplicates("target_acc").set_index("target_acc").PDS_acc
elig["cluster"] = elig.target_acc.map(pds)
elig["has_pds"] = elig.cluster.notna()
elig["cluster"] = elig.cluster.fillna("NOPDS_" + elig.target_acc)
elig["split"] = ["test" if int(hashlib.sha256(("V3R1T4S-ecoli-2026-10-16|" + k).encode()).hexdigest(), 16) % 100 < 20 else "train" for k in elig.cluster]
rows = []
for iso, f in zip(elig.target_acc, elig.AST_phenotypes):
    for t in str(f).split(","):
        t = t.strip()
        if "=" in t:
            n, call = t.rsplit("=", 1)
            if call in ("R", "S") and n in ANTIBIOTICS: rows.append((iso, n, call))
L = pd.DataFrame(rows, columns=["isolate", "antibiotic", "AST_call"]).drop_duplicates()
elig = elig[elig.target_acc.isin(set(L.isolate)) | True]
elig.to_csv(os.path.join(out, "isolates.csv.gz"), index=False)
L.to_csv(os.path.join(out, "long_rs.csv.gz"), index=False)
sp = elig[["target_acc", "cluster", "split"]].sort_values("target_acc")
sp.to_csv(os.path.join(out, "split.csv"), index=False)
print("rows in export:", n_all, "| eligible:", len(elig), "| with PDS:", int(elig.has_pds.sum()), "| clusters:", elig.cluster.nunique())
print("amrfinder versions among eligible:", elig.amrfinder_version.value_counts().head(5).to_dict())
print("long R/S rows (8 antibiotics):", len(L), "| conflicting isolate-antibiotic keys:", int((L.groupby(["isolate", "antibiotic"]).AST_call.nunique() > 1).sum()))
print("split isolates:", sp.split.value_counts().to_dict())
for ab, g in L.groupby("antibiotic"):
    s = g.isolate.map(elig.set_index("target_acc").split)
    print(f"  {ab}: n {len(g)} R {int((g.AST_call=='R').sum())} | test n {int((s=='test').sum())} R {int(((s=='test')&(g.AST_call=='R')).sum())}")
print("split.csv sha256:", hashlib.sha256(open(os.path.join(out, "split.csv"), "rb").read()).hexdigest())
