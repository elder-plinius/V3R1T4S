#!/usr/bin/env python3
"""Statistician diagnostics for BORDA-12 (PREREG.md, frozen 2026-11-19 10:35 UTC).

Written fresh from PREREG.md for this run; the 2026-11-17 statistician
script was read only as a template for conventions (charge table, rank
helpers, file layout). No numbers are copied from it.

D1: bootstrap 95% CIs (1,000 samples, seed 20261119) for BORDA-12 +
    paired diffs vs LLR12 (0.5647), ENS10 (0.5637), 150M (0.4620),
    B62 (0.3915), VenusREM 0.516; number comparison vs M1 0.5658 only
    (no paired diff — M1's score file is not available to us).
D2: Mighell replication of the frozen BORDA-12 rule (same 12 members,
    same formula, no refit); rho vs Mighell bar 0.576 and M1 Mighell
    0.5784. Diagnostic only.
D3: per-position mean absolute rank error for BORDA-12 vs 150M.
D4: mutant-class slices (charge-flip |dcharge|=2, Pro-involving) —
    descriptive only. Charge convention (same as 2026-11-17): K,R = +1;
    D,E = -1; H = 0 (not counted as charged); all others 0.
D5: null test, 400 permutations (seed 20261119) -> ../null_test.md.
D6: leave-one-out + pairwise rank correlations for BORDA-12's members,
    recomputed independently; confirm against the constructor's
    build_borda12.log values. Diagnostic only; must NOT ground any
    member choice this run or later.

This script reads DMS_score ONLY to score (Spearman of a score column vs
DMS_score, the official convention, same as ./checker.py). It never uses
labels to choose anything and fits nothing on Matreyek or Mighell labels.
"""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

RUN = Path(__file__).resolve().parents[3]
WS = RUN.parents[1]
DATA = RUN / "data"
OUT = RUN / "attempts" / "statistician" / "output"
CONS_OUT = RUN / "attempts" / "constructor" / "output"
REF_MAT = WS / "runs/2026-10-16-0453/data/dms_ref/DMS_ProteinGym_substitutions/PTEN_HUMAN_Matreyek_2021.csv"
REF_MIG = WS / "runs/2026-10-16-0453/data/dms_ref/DMS_ProteinGym_substitutions/PTEN_HUMAN_Mighell_2018.csv"
S150_MAT = WS / "runs/2026-11-07-0953/attempts/lens-constructor/output/score_150m_masked.csv"
S150_MIG = WS / "runs/2026-11-09-0953/attempts/constructor/output/score_150m_mighell.csv"
B62_MAT = WS / "runs/2026-11-03-0953/attempts/lens-statistician/output/score_B62.csv"
ENS10_MAT = WS / "runs/2026-11-15-0953/attempts/constructor/output/score_ens10.csv"
LLR12_MAT = WS / "runs/2026-11-17-0953/attempts/constructor/output/score_llr12.csv"
CHECKER = WS / "checker.py"
SEED = 20261119

# CSV model name -> zip column (same mapping as PREREG.md / constructor).
NAME_MAP = {
    "VenusREM": "VenusREM", "ProSST (K=128)": "ProSST-128",
    "ProSST (K=512)": "ProSST-512", "ProSST (K=1024)": "ProSST-1024",
    "ProSST (K=2048)": "ProSST-2048", "ProSST (K=4096)": "ProSST-4096",
    "S3F": "S3F", "S3F-MSA": "S3F_MSA", "S2F-MSA": "S2F_MSA",
    "ESCOTT": "ESCOTT", "ESM3 open (1.4B)": "ESM3", "RSALOR": "RSALOR",
}
M1_MEMBERS = [
    "VenusREM", "ProSST (K=128)", "ProSST (K=512)", "ProSST (K=1024)",
    "ProSST (K=2048)", "ProSST (K=4096)", "S3F", "S3F-MSA", "S2F-MSA",
    "ESCOTT", "ESM3 open (1.4B)", "RSALOR",
]
# Constructor's LOO values from build_borda12.log (for confirmation only).
LOO_LOG = {
    "VenusREM": 0.5684, "ProSST (K=128)": 0.5639, "ProSST (K=512)": 0.5619,
    "ProSST (K=1024)": 0.5626, "ProSST (K=2048)": 0.5684,
    "ProSST (K=4096)": 0.5664, "S3F": 0.5689, "S3F-MSA": 0.5717,
    "S2F-MSA": 0.5713, "ESCOTT": 0.5661, "ESM3 open (1.4B)": 0.5688,
    "RSALOR": 0.5696,
}
CH = {"K": 1, "R": 1, "D": -1, "E": -1}  # H = 0, same convention as 2026-11-17


def rho_scipy(a, b):
    return float(spearmanr(a, b).statistic)


def rho_fast(a_rank, b_rank):
    """Spearman via Pearson of precomputed average ranks (identical to
    scipy spearmanr for average-tie ranks; verified in main())."""
    a = a_rank - a_rank.mean()
    b = b_rank - b_rank.mean()
    return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))


def parse_mutant(m):
    g = re.match(r"^([A-Z])(\d+)([A-Z])$", m)
    return g.group(1), int(g.group(2)), g.group(3)


def pct_ranks(s):
    s = np.asarray(s, dtype=float)
    r = pd.Series(s).rank(method="average").to_numpy()
    out = (r - 1) / (len(s) - 1)
    out[np.isnan(s)] = 0.5
    return out


def load_col(ref_path, score_path):
    ref = pd.read_csv(ref_path)
    sc = pd.read_csv(score_path)
    m = ref.merge(sc, on="mutant", how="left", validate="one_to_one")
    assert len(m) == len(ref) and m["score"].notna().all()
    return ref["mutant"].to_numpy(), ref["DMS_score"].to_numpy(), m["score"].to_numpy()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = []

    # ---- Matreyek inputs ----
    mut, y, b12 = load_col(REF_MAT, CONS_OUT / "score_borda12.csv")
    _, _, llr = load_col(REF_MAT, LLR12_MAT)
    _, _, ens10 = load_col(REF_MAT, ENS10_MAT)
    _, _, s150 = load_col(REF_MAT, S150_MAT)
    _, _, b62 = load_col(REF_MAT, B62_MAT)
    _, _, trim = load_col(REF_MAT, CONS_OUT / "score_trim.csv")
    n = len(y)
    ry = rankdata(y)
    r_b12 = rankdata(b12)
    # sanity: fast rho matches scipy on the primary
    assert abs(rho_fast(r_b12, ry) - rho_scipy(b12, y)) < 1e-9
    log.append(f"Matreyek n={n} BORDA12 rho={rho_scipy(b12, y):.4f} "
               f"LLR12 rho={rho_scipy(llr, y):.4f} ENS10 rho={rho_scipy(ens10, y):.4f} "
               f"150M rho={rho_scipy(s150, y):.4f} B62 rho={rho_scipy(b62, y):.4f} "
               f"TRIM rho={rho_scipy(trim, y):.4f} M1=0.5658")

    # ---- D1: bootstrap CIs (paired, 1000 samples, seed 20261119) ----
    rng = np.random.default_rng(SEED)
    B = 1000
    idx = rng.integers(0, n, size=(B, n))
    ranks = {k: rankdata(v) for k, v in
             [("b12", b12), ("llr", llr), ("ens10", ens10), ("s150", s150), ("b62", b62)]}
    r_b12_b = np.array([rho_fast(r_b12[i], ry[i]) for i in idx])
    d_llr = np.array([rho_fast(r_b12[i], ry[i]) - rho_fast(ranks["llr"][i], ry[i]) for i in idx])
    d_ens = np.array([rho_fast(r_b12[i], ry[i]) - rho_fast(ranks["ens10"][i], ry[i]) for i in idx])
    d_150 = np.array([rho_fast(r_b12[i], ry[i]) - rho_fast(ranks["s150"][i], ry[i]) for i in idx])
    d_b62 = np.array([rho_fast(r_b12[i], ry[i]) - rho_fast(ranks["b62"][i], ry[i]) for i in idx])
    d_bar = r_b12_b - 0.516
    d_m1 = r_b12_b - 0.5658
    for name, arr in [("BORDA12", r_b12_b), ("BORDA12-LLR12", d_llr),
                      ("BORDA12-ENS10", d_ens), ("BORDA12-150M", d_150),
                      ("BORDA12-B62", d_b62), ("BORDA12-VenusREM 0.516", d_bar),
                      ("BORDA12-M1 0.5658 (number comparison only)", d_m1)]:
        lo, hi = np.percentile(arr, [2.5, 97.5])
        log.append(f"D1 {name}: mean={arr.mean():.4f} 95% CI [{lo:.4f}, {hi:.4f}]")
    # how often does the paired diff clear zero / M1?
    log.append(f"D1 paired P(BORDA12>LLR12)={float((d_llr > 0).mean()):.3f} "
               f"P(BORDA12>ENS10)={float((d_ens > 0).mean()):.3f} "
               f"P(BORDA12>M1 0.5658)={float((d_m1 > 0).mean()):.3f} "
               f"P(BORDA12>bar 0.531)={float((r_b12_b > 0.531).mean()):.3f}")

    # ---- D5: null test (400 permutations, seed 20261119) ----
    rng2 = np.random.default_rng(SEED)
    controls = [rho_scipy(rng2.permutation(b12), y) for _ in range(400)]
    best = max(controls)
    real = rho_scipy(b12, y)
    beats = "yes" if real > best else "no"
    log.append(f"D5 null: controls=400 best_control={best:.4f} real={real:.4f} "
               f"real_beats_all_controls={beats}")
    (RUN / "null_test.md").write_text(
        "# null_test.md — BORDA-12 (2026-11-19)\n\n"
        "controls: 400\n"
        f"best_control: {best:.4f}\n"
        f"real: {real:.4f}\n"
        f"real_beats_all_controls: {beats}\n"
        "command: venv/bin/python "
        "runs/2026-11-19-0953/attempts/statistician/code/diagnostics.py "
        "(D5 section; seed 20261119; 400 random permutations of the BORDA-12 scores)\n")

    # ---- D2: Mighell replication (frozen rule, no refit) ----
    ref_g = pd.read_csv(REF_MIG)
    zcols = [NAME_MAP[m] for m in M1_MEMBERS]
    mig = pd.read_csv(DATA / "PTEN_HUMAN_Mighell_2018.csv",
                      usecols=["mutant"] + zcols)
    mg = ref_g[["mutant", "DMS_score"]].merge(mig, on="mutant", how="left",
                                              validate="one_to_one")
    assert len(mg) == 7260 and mg["mutant"].is_unique
    assert mg[zcols].notna().all().all()
    y_g = mg["DMS_score"].to_numpy()
    R_g = np.column_stack([pct_ranks(mg[NAME_MAP[m]]) for m in M1_MEMBERS])
    b12_g = R_g.mean(axis=1)
    trim_g = np.sort(R_g, axis=1)[:, 1:-1].mean(axis=1)
    out_g = pd.DataFrame({"mutant": mg["mutant"], "score": b12_g})
    out_g.to_csv(OUT / "score_borda12_mighell.csv", index=False)
    r = subprocess.run([sys.executable, str(CHECKER), str(REF_MIG),
                        str(OUT / "score_borda12_mighell.csv"), "0.576"],
                       capture_output=True, text=True)
    log.append(f"D2 Mighell BORDA12: rho={rho_scipy(b12_g, y_g):.4f} :: "
               f"{(r.stdout + r.stderr).strip()}")
    log.append(f"D2 Mighell TRIM (diagnostic): rho={rho_scipy(trim_g, y_g):.4f}")
    _, _, s150_g = load_col(REF_MIG, S150_MIG)
    log.append(f"D2 Mighell 150M (reference): rho={rho_scipy(s150_g, y_g):.4f}")
    log.append("D2 Mighell bars: live best 0.561 (S3F-MSA), bar 0.576; "
               "M1 Mighell 0.5784")

    # ---- D3: per-position error autopsy ----
    def pos_err(scores, yv, mutants):
        rs = rankdata(scores) / len(scores)
        ryv = rankdata(yv) / len(yv)
        ae = np.abs(rs - ryv)
        pos = np.array([parse_mutant(m)[1] for m in mutants])
        rows = [(p, int((pos == p).sum()), float(ae[pos == p].mean()))
                for p in sorted(set(pos))]
        return pd.DataFrame(rows, columns=["position", "n_mutants",
                                           "mean_abs_rank_err"])
    d3_b = pos_err(b12, y, mut)
    d3_1 = pos_err(s150, y, mut)
    d3_b.to_csv(OUT / "d3_position_error_borda12.csv", index=False)
    d3_1.to_csv(OUT / "d3_position_error_150m.csv", index=False)
    worst_b = d3_b.nlargest(10, "mean_abs_rank_err")
    worst_1 = d3_1.nlargest(10, "mean_abs_rank_err")
    log.append("D3 BORDA12 worst positions: " + ", ".join(
        f"{int(r.position)}({r.mean_abs_rank_err:.3f})" for r in worst_b.itertuples()))
    log.append("D3 150M worst positions: " + ", ".join(
        f"{int(r.position)}({r.mean_abs_rank_err:.3f})" for r in worst_1.itertuples()))
    log.append(f"D3 worst-10 overlap: {len(set(worst_b.position) & set(worst_1.position))}/10")
    log.append(f"D3 mean abs rank err: BORDA12={d3_b.mean_abs_rank_err.mean():.4f} "
               f"150M={d3_1.mean_abs_rank_err.mean():.4f}")
    for p in (130, 123, 92, 125, 15):
        e = d3_b.loc[d3_b.position == p, "mean_abs_rank_err"].iloc[0]
        o = d3_1.loc[d3_1.position == p, "mean_abs_rank_err"].iloc[0]
        log.append(f"D3 pos {p}: BORDA12 err={e:.3f} vs 150M err={o:.3f}")

    # ---- D4: class slices (descriptive only) ----
    def dcharge(m):
        w, _, mm_ = parse_mutant(m)
        return CH.get(mm_, 0) - CH.get(w, 0)
    dc = np.array([dcharge(m) for m in mut])
    pro = np.array([("P" in (parse_mutant(m)[0], parse_mutant(m)[2])) for m in mut])
    for label, mask in [("charge-flip |dcharge|=2", np.abs(dc) == 2),
                        ("charge-change |dcharge|=1", np.abs(dc) == 1),
                        ("no charge change", dc == 0),
                        ("Pro-involving", pro),
                        ("all", np.ones(n, bool))]:
        log.append(f"D4 {label}: n={int(mask.sum())} rho_BORDA12={rho_scipy(b12[mask], y[mask]):.4f} "
                   f"rho_150M={rho_scipy(s150[mask], y[mask]):.4f}")

    # ---- D6: LOO + pairwise rank correlations (recomputed independently) ----
    mat = pd.read_csv(DATA / "PTEN_HUMAN_Matreyek_2021.csv",
                      usecols=["mutant"] + [NAME_MAP[m] for m in M1_MEMBERS])
    mm = pd.DataFrame({"mutant": mut}).merge(mat, on="mutant", how="left",
                                             validate="one_to_one")
    assert len(mm) == n
    R_m = np.column_stack([pct_ranks(mm[NAME_MAP[m]]) for m in M1_MEMBERS])
    # confirm the frozen Borda recomputes to the constructor's score file
    b12_re = R_m.mean(axis=1)
    log.append(f"D6 Borda recompute vs score file: max|diff|={np.abs(b12_re - b12).max():.2e} "
               f"rho_recomputed={rho_scipy(b12_re, y):.4f}")
    # pairwise rank correlations (Spearman of member raw scores)
    corr = np.corrcoef(np.column_stack([rankdata(mm[NAME_MAP[m]]) for m in M1_MEMBERS]).T)
    iu = np.triu_indices(12, k=1)
    off = corr[iu]
    log.append(f"D6 member pairwise rank corr: mean={off.mean():.4f} "
               f"min={off.min():.4f} max={off.max():.4f}")
    pd.DataFrame(corr, index=M1_MEMBERS, columns=M1_MEMBERS).to_csv(
        OUT / "member_pairwise_rank_corr.csv")
    # LOO, recomputed
    loo_rows = []
    max_dev = 0.0
    for j, mname in enumerate(M1_MEMBERS):
        keep = [k for k in range(12) if k != j]
        loo = R_m[:, keep].mean(axis=1)
        v = rho_scipy(loo, y)
        dev = abs(v - LOO_LOG[mname])
        max_dev = max(max_dev, dev)
        loo_rows.append((mname, v, LOO_LOG[mname], dev))
        log.append(f"D6 LOO drop {mname}: rho={v:.4f} (log {LOO_LOG[mname]:.4f}, "
                   f"|diff|={dev:.4f})")
    pd.DataFrame(loo_rows, columns=["dropped_member", "rho_recomputed",
                                    "rho_build_log", "abs_diff"]).to_csv(
        OUT / "loo_borda12.csv", index=False)
    log.append(f"D6 LOO confirmation: max |recomputed - build log| = {max_dev:.4f} "
               f"({'CONFIRMED' if max_dev < 0.001 else 'MISMATCH'})")
    loo_vals = [r[1] for r in loo_rows]
    log.append(f"D6 LOO range: [{min(loo_vals):.4f}, {max(loo_vals):.4f}] "
               f"vs full BORDA12 {rho_scipy(b12, y):.4f}")

    print("\n".join(log))
    (OUT / "diagnostics.log").write_text("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
