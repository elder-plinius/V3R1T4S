#!/usr/bin/env python3
"""V3R1T4S canonical checker for proteingym-cancer-dms-zero-shot (hardened).

Implements the bank's verification convention:
- load the assay's ProteinGym reference CSV (mutant id + DMS_score column)
- load the attacker's score file (mutant id + score column)
- REJECT any file with duplicate mutant IDs (loud FAIL, no silent merge)
- require the mutant sets to match EXACTLY (else FAIL with reason)
- inner join, drop NaN pairs, compute Spearman with scipy
- PASS iff spearman > bar (bar = live best + 0.015)

Hardening history:
- 2026-10-16: duplicate-mutant rejection added (v2). The 2026-10-16 04:53 CDT hunt
  found (H6, tested) that a score file with every row duplicated passed the old
  set-equality check and was silently merged (n 5083 -> 10166, rho re-weighted),
  reporting a wrong n and a recomputed rho. Duplication could not manufacture a
  PASS on its own, but the instrument was misreporting. Fixed by failing fast on
  any duplicate mutant ID in either input file.

Usage: checker.py <reference.csv> <score.csv> <bar> [--mutant-col M] [--ref-col DMS_score] [--pred-col score]
Prints a one-line verdict plus details; exit 0 on PASS, 1 on FAIL.
"""
import sys
import pandas as pd
from scipy.stats import spearmanr

CHECKER_VERSION = "2.0-dupe-reject"


def die(msg):
    print(msg)
    return 1


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        return die(f"FAIL: usage: checker.py <reference.csv> <score.csv> <bar> [options] "
                   f"(checker v{CHECKER_VERSION})")
    ref_path, score_path, bar = args[0], args[1], float(args[2])
    mutant_col, ref_col, pred_col = "mutant", "DMS_score", "score"
    for i, a in enumerate(args[3:]):
        if a == "--mutant-col":
            mutant_col = args[4 + i]
        elif a == "--ref-col":
            ref_col = args[4 + i]
        elif a == "--pred-col":
            pred_col = args[4 + i]

    ref = pd.read_csv(ref_path)
    pred = pd.read_csv(score_path)
    for col, df, name in [(mutant_col, ref, "reference"), (ref_col, ref, "reference"),
                          (mutant_col, pred, "score file"), (pred_col, pred, "score file")]:
        if col not in df.columns:
            return die(f"FAIL: column '{col}' missing from {name} (checker v{CHECKER_VERSION})")

    # HARDENING (v2): reject duplicate mutant IDs before any join. The join below
    # is one-to-one only when both key columns are unique; duplicates silently
    # inflate n and re-weight rho (observed 2026-10-16: n 5083 -> 10166).
    for df, name in [(ref, "reference"), (pred, "score file")]:
        ids = df[mutant_col].astype(str)
        dup_mask = ids.duplicated(keep=False)
        if dup_mask.any():
            n_dup_ids = ids[dup_mask].nunique()
            n_dup_rows = int(dup_mask.sum())
            return die(f"FAIL: {name} has duplicate mutant IDs "
                       f"({n_dup_rows} rows across {n_dup_ids} duplicated IDs); "
                       f"score files must list each mutant exactly once "
                       f"(checker v{CHECKER_VERSION})")

    ref_ids = set(ref[mutant_col].astype(str))
    pred_ids = set(pred[mutant_col].astype(str))
    if ref_ids != pred_ids:
        return die(f"FAIL: mutant sets differ (ref={len(ref_ids)}, pred={len(pred_ids)}, "
                   f"only_in_ref={len(ref_ids - pred_ids)}, only_in_pred={len(pred_ids - ref_ids)}) "
                   f"(checker v{CHECKER_VERSION})")

    m = ref[[mutant_col, ref_col]].merge(pred[[mutant_col, pred_col]], on=mutant_col)
    m = m.dropna(subset=[ref_col, pred_col])
    if len(m) < 3:
        return die(f"FAIL: only {len(m)} usable pairs after NaN drop (checker v{CHECKER_VERSION})")
    rho, _ = spearmanr(m[ref_col], m[pred_col])
    verdict = "PASS" if (rho == rho and rho > bar) else "FAIL"  # rho==rho guards NaN
    print(f"{verdict}: spearman={rho:.4f} n={len(m)} bar={bar:.3f} (checker v{CHECKER_VERSION})")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
