"""Check the rule reimplementation against the paper's own S9 predictions and S10 confusion matrices."""
import os
import sys, pandas as pd, collections; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ecoli_rules import *
d = sys.argv[1]
s8 = pd.read_csv(d + "/03_Concordance_and_Discordance/NCBI_S8_AST_interpretable.csv")
s9 = pd.read_csv(d + "/03_Concordance_and_Discordance/NCBI_S9_prediction_level.csv")
geno = s8.drop_duplicates("isolate").set_index("isolate").amr_genotypes
s9["mine"] = [predict(a, geno[i]) for a, i in zip(s9.antibiotic, s9.isolate)]
for ab, g in s9.groupby("antibiotic", sort=False):
    mm = g[g.mine != g.genotype_predicted_call]
    tp = ((g.mine == "R") & (g.AST_call == "R")).sum(); fp = ((g.mine == "R") & (g.AST_call == "S")).sum()
    fn = ((g.mine == "S") & (g.AST_call == "R")).sum(); tn = ((g.mine == "S") & (g.AST_call == "S")).sum()
    print(f"{ab}: mismatches {len(mm)}  TP {tp} FP {fp} TN {tn} FN {fn}  F1 {2*tp/(2*tp+fp+fn):.6f}")
    if len(mm):
        c = collections.Counter()
        for i, p in zip(mm.isolate, mm.genotype_predicted_call):
            m = set(matched(ab, geno[i])); allt = [n + "=" + s for n, s in tokens(geno[i])]
            c[(p, tuple(sorted(m))[:3] if p == "S" else "")] += 1
        print("   ", c.most_common(6))
        ex = mm.iloc[0]; print("    example paper:", ex.genotype_predicted_call, ex.matched_markers, "| geno:", str(geno[ex.isolate])[:250])
