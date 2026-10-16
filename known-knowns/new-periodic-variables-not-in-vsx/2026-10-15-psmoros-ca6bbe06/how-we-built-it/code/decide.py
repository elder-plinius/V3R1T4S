"""Stage-B decision (frozen; run 2026-10-15-1643, calibrator-v2). usage: decide.py
Inputs: data/var_draw_order.csv, data/gaia_draw_order.csv, data/cst_draw_order.csv, data/fetch_*.tsv,
        out/var.jsonl, out/gaia.jsonl, out/cst.jsonl (pipeline.analyze per LC file, from run_many.py).
Applies pipeline.select(DELTA, FLOW) and PREREG.md's decision literally. Prints the null_test.md lines.
Writes results/vsx_reproduce_known_table.csv, results/controls_table.csv, results/far.txt."""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, "<WORKDIR>/runs/2026-10-15-1407/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from period_check import agree
import pipeline
from params import DELTA, FLOW, MODE, T_THRESH, N_VAR, N_CTRL


def load(kind):
    p = f"out/{kind}.jsonl"
    R = {}
    if os.path.exists(p):
        for l in open(p):
            r = json.loads(l); R[int(os.path.basename(r["file"])[:4])] = r
    return R


def fetchlog(kind):
    p = f"data/fetch_{kind}.tsv"
    if not os.path.exists(p): return pd.DataFrame(columns=["draw", "code", "bytes", "status", "url"])
    return pd.read_csv(p, sep="\t", names=["draw", "code", "bytes", "status", "url"]).drop_duplicates("draw", keep="last")


# ---- variables: the first N_VAR usable in draw order ----
var = pd.read_csv("data/var_draw_order.csv"); fl = fetchlog("var"); R = load("var")
rows, nuse = [], 0
for _, f in fl.sort_values("draw").iterrows():
    i = int(f.draw); v = var.iloc[i]
    row = dict(draw=i, vsx_oid=int(v.OID), name=v.Name.strip(), type=v.Type.strip(), P_vsx=float(v.Period),
               ra=v.RA_full, dec=v.DE_full, fetch_code=f.code, lc_status=f.status,
               provenance="ZTF-derived (ZTF name)" if v.Name.strip().startswith("ZTF ") else "other/unknown (non-ZTF name)")
    if f.status == "usable":
        if nuse >= N_VAR: break
        nuse += 1
        r = R.get(i)
        if r is None:
            row.update(scored=False)
        else:
            P, S, b = pipeline.select(r, DELTA, FLOW, MODE)
            rec = bool(np.isfinite(P) and agree(P, row["P_vsx"]))
            zb = r["bands"]
            row.update(scored=True, P_rec=P, S=S, recovered=rec,
                       ztf_oid=";".join(f"{k}:{zb[k][0]}" for k in sorted(zb)), n_epochs=r.get("n_epochs"),
                       Z_full=(b[1] if b else 0.0), alias_dist=(b[4] if b else None))
    rows.append(row)
V = pd.DataFrame(rows)

# ---- controls: VSX CST (0 fresh) then Gaia, until N_CTRL usable ----
crow = []
for kind in ("cst", "gaia"):
    if not os.path.exists(f"data/{kind}_draw_order.csv"): continue
    dd = pd.read_csv(f"data/{kind}_draw_order.csv"); fl = fetchlog(kind); R = load(kind)
    for _, f in fl.sort_values("draw").iterrows():
        i = int(f.draw); g = dd.iloc[i]
        row = dict(set=kind, draw=i, id=(int(dd.OID.iloc[i]) if kind == "cst" else int(dd.source_id.iloc[i])), fetch_code=f.code, lc_status=f.status)
        if f.status == "usable":
            r = R.get(i)
            if r is None: row.update(scored=False)
            else:
                P, S, b = pipeline.select(r, DELTA, FLOW, MODE); zb = r["bands"]
                row.update(scored=True, P_rec=P, S=S, ztf_oid=";".join(f"{k}:{zb[k][0]}" for k in sorted(zb)), n_epochs=r.get("n_epochs"),
                           Z_full=(b[1] if b else 0.0), alias_dist=(b[4] if b else None))
        crow.append(row)
C = pd.DataFrame(crow)
os.makedirs("results", exist_ok=True)
Cs = C[C.get("scored", pd.Series(False, index=C.index)) == True] if len(C) else C
best_control = float(Cs.S.max()) if len(Cs) else float("nan")
Vs = V[V.get("scored", pd.Series(False, index=V.index)) == True] if len(V) else V
V["detected"] = [bool(s > best_control) if sc is True else None for s, sc in zip(V.get("S", [np.nan] * len(V)), V.get("scored", [False] * len(V)))]
V.to_csv("results/vsx_reproduce_known_table.csv", index=False)
C.to_csv("results/controls_table.csv", index=False)
recS = sorted(Vs.loc[Vs.recovered == True, "S"].tolist(), reverse=True)
real = recS[49] if len(recS) >= 50 else 0
n_real = int(((Vs.recovered == True) & (Vs.S > best_control)).sum())
lines = []
lines.append(f"usable variables scored: {len(Vs)} (target {N_VAR}); usable controls scored: {len(Cs)} (target {N_CTRL})")
lines.append(f"recovered: {int((Vs.recovered == True).sum())}/{len(Vs)}; recovered AND detected (S > best_control): {n_real}")
for pv, grp in Vs.groupby("provenance"):
    lines.append(f"  provenance {pv}: recovered {int((grp.recovered == True).sum())}/{len(grp)}, recovered&detected {int(((grp.recovered == True) & (grp.S > best_control)).sum())}")
lines.append(f"FAR at T={T_THRESH}: {int((Cs.S > T_THRESH).sum())}/{len(Cs)} controls with S > T")
for st, grp in Cs.groupby("set"):
    lines.append(f"  FAR {st}: {int((grp.S > T_THRESH).sum())}/{len(grp)}")
lines.append(f"variables with S > T: {int((Vs.S > T_THRESH).sum())}/{len(Vs)}; recovered with S > T: {int(((Vs.recovered == True) & (Vs.S > T_THRESH)).sum())}")
complete = len(Vs) >= N_VAR and len(Cs) >= N_CTRL
lines.append(f"stage B complete: {'yes' if complete else 'NO (partial; no PASS may be written)'}")
lines.append(f"PREREG decision: real_count={n_real} -> {'PASS' if (complete and n_real >= 50) else 'FAIL/INCOMPLETE'}")
lines.append(f"controls: {len(Cs)}")
lines.append(f"best_control: {best_control}")
lines.append(f"real: {real}")
lines.append(f"real_beats_all_controls: {'yes' if (complete and real > best_control) else 'no'}")
lines.append("command: cd <WORKDIR>/runs/2026-10-15-1643/attempts/calibrator-v2 && <WORKDIR>/venv/bin/python -I code/decide.py")
open("results/far.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
