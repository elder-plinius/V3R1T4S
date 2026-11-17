"""Compare truth vintages on the published scores.csv rows: archive truth_ECDC (cases, deaths) vs the weekly
final vintage covid-cases-deaths-final_2024-09-27.csv, and for inc hosp CZ: ECDC hospitalisation file vs OWID file.
Usage: python -I vintage_diff.py <run_data_dir> <out_txt>"""
import sys, os
import pandas as pd
data, outf = sys.argv[1], sys.argv[2]
pub = pd.read_csv(os.path.join(data, "scores.csv"), dtype={"location": str})
def rd(p): return pd.read_csv(p, dtype={"location": str})
T = os.path.join(data, "truth")
ecdc = pd.concat([rd(os.path.join(T, "ECDC", f"truth_ECDC-Incident {f}.csv")).assign(target_variable=tv)
                  for tv, f in (("inc case", "Cases"), ("inc death", "Deaths"), ("inc hosp", "Hospitalizations"))])
fin = rd(os.path.join(T, "ECDC", "final", "covid-cases-deaths-final_2024-09-27.csv"))
owid = rd(os.path.join(T, "OWID", "truth_OWID-Incident Hospitalizations.csv")).assign(target_variable="inc hosp")
k = ["target_variable", "location", "date"]
keys = pub[["target_variable", "location", "target_end_date"]].drop_duplicates().rename(columns={"target_end_date": "date"})
A = keys.merge(ecdc[k + ["value"]].rename(columns={"value": "ecdc"}), on=k, how="left") \
        .merge(fin[k + ["value"]].rename(columns={"value": "final0927"}), on=k, how="left") \
        .merge(owid[k + ["value"]].rename(columns={"value": "owid"}), on=k, how="left")
L = [f"distinct published truth keys (target_variable, location, target_end_date): {len(A)}"]
for tv, G in A.groupby("target_variable"):
    L.append(f"{tv}: keys {len(G)}; ecdc present {G.ecdc.notna().sum()}; final0927 present {G.final0927.notna().sum()}; owid present {G.owid.notna().sum()}")
    both = G[G.ecdc.notna() & G.final0927.notna()]
    L.append(f"   ecdc vs final0927: compared {len(both)}, differ {(both.ecdc != both.final0927).sum()}")
    bo = G[G.ecdc.notna() & G.owid.notna()]
    L.append(f"   ecdc vs owid: compared {len(bo)}, differ {(bo.ecdc != bo.owid).sum()}")
D = A[A.ecdc.notna() & A.final0927.notna() & (A.ecdc != A.final0927)]
if len(D): L.append("ecdc != final0927 rows:\n" + D.head(40).to_string())
open(outf, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L))
