#!/usr/bin/env python3
"""Build BORDA-12: plain equal-weight Borda (mean percentile rank) over
M1's 12 published members (PREREG.md, frozen 2026-11-19 10:35 UTC).

Method (frozen):
- Membership: M1's 12 as published in V3R1T4S PR #467 (selected by its
  authors only on non-cancer assays): VenusREM; ProSST (K=128, 512, 1024,
  2048, 4096); S3F; S3F-MSA; S2F-MSA; ESCOTT; ESM3 open (1.4B); RSALOR.
- p_m(i) = percentile rank of model m's score for mutant i over the 5,083
  reference mutants (rank/(n-1), ties averaged, ascending: a higher model
  score gets a higher rank). BORDA12(i) = mean_m p_m(i), equal weight
  1/12 each, no fitted weight, no clipping, no logit.
- Diagnostic (frozen, never a claim): D-TRIM = trimmed Borda over M1's
  12 (drop each mutant's min and max member rank, mean of the rest).
- NaN in a member column -> neutral rank 0.5 for that member/mutant
  (frozen rule; NaN counts reported).
- The build code reads ONLY the mutant column and the member score columns
  (usecols) from the fetched assay files. It NEVER reads DMS_score for
  method construction; labels are touched only by ./checker.py and by the
  G3 identity check, which reports recomputed-vs-CSV values as a
  diagnostic and NEVER drives a drop decision.

Gates (before scoring): G1 checker fixtures (DMS_score -> 1.0 PASS,
negated -> -1.0 FAIL); G2 E2 rho = 0.3666 reproduction; G3 LABEL-FREE
member check: drop only if a column is missing, constant, or >5% NaN
(fix for the 2026-11-17 self-break latent caveat).
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# --- Path resolution (fixed 2026-11-19, REPRODUCE-skeptic defect) --------
# Original code used Path(__file__).resolve().parents[3] as the run folder.
# That is only correct in the run-folder layout
#   <WS>/runs/<run>/attempts/constructor/code/build_borda12.py
# (parents[3] == <run>). In the packaged layout
#   <pkg>/how-we-built-it/build_borda12.py
# parents[3] lands one level too high (the workspace parent), so the
# script died with FileNotFoundError on the reference CSV. Scoring logic
# below is unchanged; only how RUN/WS are found changed.
# Resolution order:
#   1. --run-dir <run-folder> (or $V3R1T4S_RUN_DIR) if given;
#   2. parents[3] if it holds data/PTEN_HUMAN_Matreyek_2021.csv
#      (the original run-folder layout, preserved verbatim);
#   3. any ancestor that holds data/PTEN_HUMAN_Matreyek_2021.csv;
#   4. otherwise a clear error naming the --run-dir fix, instead of a
#      misleading FileNotFoundError on a wrong path.


def _is_run_dir(d: Path) -> bool:
    return (d / "data" / "PTEN_HUMAN_Matreyek_2021.csv").is_file()


def _find_run(explicit=None):
    import os

    if explicit:
        d = Path(explicit).expanduser().resolve()
        if _is_run_dir(d):
            return d
        raise SystemExit(
            f"--run-dir {d} does not contain "
            "data/PTEN_HUMAN_Matreyek_2021.csv"
        )
    env = os.environ.get("V3R1T4S_RUN_DIR")
    if env:
        return _find_run(env)
    here = Path(__file__).resolve()
    cand = here.parents[3]
    if _is_run_dir(cand):
        return cand
    for anc in here.parents:
        if _is_run_dir(anc):
            return anc
    raise SystemExit(
        "Could not locate the run folder from this script's location. "
        "Run it from the run-folder layout "
        "(<WS>/runs/<run>/attempts/constructor/code/build_borda12.py), "
        "or pass --run-dir <WS>/runs/<run> "
        "(e.g. python3 build_borda12.py --run-dir runs/2026-11-19-0953)."
    )


def _parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", default=None,
                    help="run folder holding data/ (default: auto-detect)")
    return ap.parse_args()


RUN = _find_run(_parse_args().run_dir)
WS = RUN.parents[1]  # <WORKDIR>
DATA = RUN / "data"
OUT = RUN / "attempts" / "constructor" / "output"
REF_MAT = WS / "runs/2026-10-16-0453/data/dms_ref/DMS_ProteinGym_substitutions/PTEN_HUMAN_Matreyek_2021.csv"
E2_FILE = WS / "runs/2026-10-30-0954/attempts/lens-constructor/output/score_E2.csv"
CHECKER = WS / "checker.py"
BAR = 0.531
M1_BAR = 0.5658

# CSV model name -> column name in the Zenodo zip assay files.
NAME_MAP = {
    "VenusREM": "VenusREM",
    "ProSST (K=128)": "ProSST-128",
    "ProSST (K=512)": "ProSST-512",
    "ProSST (K=1024)": "ProSST-1024",
    "ProSST (K=2048)": "ProSST-2048",
    "ProSST (K=4096)": "ProSST-4096",
    "S3F": "S3F",
    "S3F-MSA": "S3F_MSA",
    "S2F-MSA": "S2F_MSA",
    "ESCOTT": "ESCOTT",
    "ESM3 open (1.4B)": "ESM3",
    "RSALOR": "RSALOR",
}
# M1's 12 (PR #467), in the order listed in the PR body.
M1_MEMBERS = [
    "VenusREM", "ProSST (K=128)", "ProSST (K=512)", "ProSST (K=1024)",
    "ProSST (K=2048)", "ProSST (K=4096)", "S3F", "S3F-MSA", "S2F-MSA",
    "ESCOTT", "ESM3 open (1.4B)", "RSALOR",
]


def run_checker(ref, score, bar):
    r = subprocess.run(
        [sys.executable, str(CHECKER), str(ref), str(score), str(bar)],
        capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def pct_ranks(s):
    r = s.rank(method="average", ascending=True)  # 1..n
    pct = (r - 1) / (len(s) - 1)
    pct[s.isna()] = 0.5  # frozen neutral-rank rule
    return pct


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = []

    # ---- G1: checker fixtures -------------------------------------------
    ref = pd.read_csv(REF_MAT)
    pos = ref[["mutant"]].copy(); pos["score"] = ref["DMS_score"]
    pos.to_csv(OUT / "fixture_pos.csv", index=False)
    rc, out = run_checker(REF_MAT, OUT / "fixture_pos.csv", BAR)
    log.append(f"G1 positive (score=DMS_score): rc={rc} :: {out}")
    assert rc == 0, "G1 positive fixture must PASS"
    neg = ref[["mutant"]].copy(); neg["score"] = -ref["DMS_score"]
    neg.to_csv(OUT / "fixture_neg.csv", index=False)
    rc, out = run_checker(REF_MAT, OUT / "fixture_neg.csv", BAR)
    log.append(f"G1 negative (score=-DMS_score): rc={rc} :: {out}")
    assert rc == 1, "G1 negative fixture must FAIL"

    # ---- G2: E2 reproduction --------------------------------------------
    rc, out = run_checker(REF_MAT, E2_FILE, BAR)
    log.append(f"G2 E2 reproduction: rc={rc} :: {out}")
    assert "0.3666" in out, f"G2: E2 rho not 0.3666: {out}"

    # ---- G3: label-free member check + diagnostic identity report -------
    csv = pd.read_csv(DATA / "DMS_substitutions_Spearman_DMS_level.csv")
    mat_row = csv[csv["DMS ID"] == "PTEN_HUMAN_Matreyek_2021"].iloc[0]
    zip_cols = set(pd.read_csv(DATA / "PTEN_HUMAN_Matreyek_2021.csv",
                               nrows=0).columns)
    use_cols = ["mutant"] + [NAME_MAP[m] for m in M1_MEMBERS]
    missing = [zc for zc in use_cols[1:] if zc not in zip_cols]
    assert not missing, f"missing zip columns: {missing}"
    scores = pd.read_csv(DATA / "PTEN_HUMAN_Matreyek_2021.csv",
                         usecols=use_cols)
    merged = ref[["mutant", "DMS_score"]].merge(scores, on="mutant",
                                                how="left", validate="one_to_one")
    assert len(merged) == 5083, f"merged n={len(merged)} != 5083"
    assert merged["mutant"].is_unique
    dropped = []
    for m in M1_MEMBERS:
        zc = NAME_MAP[m]
        col = merged[zc]
        n_nan = int(col.isna().sum())
        n_uniq = int(col.nunique(dropna=True))
        # Label-free drop rule only: missing / constant / >5% NaN.
        drop = (n_uniq <= 1) or (n_nan > 0.05 * len(merged))
        # Diagnostic identity check only — never drives a drop.
        rho = float(spearmanr(merged["DMS_score"], col, nan_policy="omit").statistic)
        csv_val = float(mat_row[m])
        log.append(f"G3 {m:18s} [{zc:12s}] recomputed={rho:.4f} "
                   f"csv={csv_val:.4f} diff={rho - csv_val:+.4f} "
                   f"NaN={n_nan} uniq={n_uniq} "
                   f"{'DROP(label-free)' if drop else 'keep'}")
        if drop:
            dropped.append(m)
    assert not dropped, f"G3 label-free drop fired for: {dropped}"
    final_members = [m for m in M1_MEMBERS if m not in dropped]
    log.append(f"final members: {len(final_members)}; dropped: {dropped or 'none'}")

    # ---- percentile ranks + BORDA-12 --------------------------------------
    ranks = {}
    for m in final_members:
        ranks[m] = pct_ranks(merged[NAME_MAP[m]].astype(float))
    rank_df = pd.DataFrame(ranks)

    borda12 = rank_df[final_members].mean(axis=1)
    out_df = pd.DataFrame({"mutant": merged["mutant"], "score": borda12})
    assert out_df["score"].notna().all() and len(out_df) == 5083
    out_df.to_csv(OUT / "score_borda12.csv", index=False)
    rc, out = run_checker(REF_MAT, OUT / "score_borda12.csv", BAR)
    log.append(f"BORDA12 checker: rc={rc} :: {out}")
    borda_rho = float(spearmanr(merged["DMS_score"], borda12).statistic)
    log.append(f"BORDA12 rho (direct recompute): {borda_rho:.4f} "
               f"vs bar 0.531, vs M1 0.5658: diff {borda_rho - M1_BAR:+.4f}")

    # ---- diagnostic (frozen, never a claim) -------------------------------
    trim = rank_df[final_members].apply(
        lambda row: np.sort(row.values)[1:-1].mean(), axis=1)
    d = pd.DataFrame({"mutant": merged["mutant"], "score": trim})
    d.to_csv(OUT / "score_trim.csv", index=False)
    rho = float(spearmanr(merged["DMS_score"], trim).statistic)
    rc, out = run_checker(REF_MAT, OUT / "score_trim.csv", BAR)
    log.append(f"DIAG trim: rho={rho:.4f} vs M1 diff {rho - M1_BAR:+.4f} "
               f":: checker rc={rc} :: {out}")

    # ---- mechanism diagnostics (descriptive) ------------------------------
    corr = rank_df[final_members].corr(method="spearman")
    corr.to_csv(OUT / "member_pairwise_rank_corr.csv")
    mean_offdiag = (corr.values[np.triu_indices(len(final_members), 1)]).mean()
    log.append(f"member mean pairwise rank corr: {mean_offdiag:.4f}")
    for m in final_members:
        others = [k for k in final_members if k != m]
        loo_score = rank_df[others].mean(axis=1)
        v = float(spearmanr(merged["DMS_score"], loo_score).statistic)
        log.append(f"  leave-one-out Borda (drop {m}): rho={v:.4f}")

    print("\n".join(log))
    (OUT / "build_borda12.log").write_text("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
