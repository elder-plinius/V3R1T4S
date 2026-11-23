# PREREG.v2 — pivot to partial win p2 on CHEMBL244_Ki (coagulation factor X)

Frozen 2026-11-18T03:0xZ, BEFORE any CHEMBL244_Ki test evaluation. No CHEMBL244 test read has
occurred at freeze time. This prereg supersedes the JAK1 plan (v1 read failed; see
attempts/final/NOTES.md) for THIS run's remaining attack budget. The JAK1 PREREG stands unchanged
for the record; its outcome is negative: candidate v1 test MSE 0.1728 > listed best 0.16617
(bootstrap fraction 0.467); v2/v3 cancelled — power analysis shows no pool member approaches
the ~0.12 needed for criterion (c) at n_test=126, so further reads cannot produce a claim and
are withheld as unnecessary test reads.

## Partial win attacked (verbatim from the bank)

p2: "A cliff-subset result: on one target, lower MSE than a faithfully reproduced MoleculeACE
paper baseline (the repo's own best descriptor+model for that target, run by the attacker and
reported with its code) restricted to the test molecules with cliff_mol==1, with at least 40
such molecules, while not being worse on the non-cliff subset."

## Target

CHEMBL244_Ki (moleculeace-chembl244-ki, coagulation factor X). CSV sha256 recorded in
data/csv_sha256.txt (fetched 2026-11-18 with the 30-CSV batch). Official split column:
2476 train / 621 test; Polaris API nTrainDatapoints 2476 (data/count_check.json, fetched
2026-11-18T00:36Z). Cliff test molecules (cliff_mol==1, split=='test'): 296 ≥ 40 ✓.
The repo's own best descriptor+model for this target per the corrected results CSV
(data/MoleculeACE_results.csv): SVM/ECFP, overall RMSE 0.715, cliff RMSE 0.797.
Repo config used verbatim: C=10, epsilon=0.1, gamma=0.01, kernel=rbf
(data/repo_config244/SVM_ECFP.yml); ECFP = Morgan radius 2, 1024 bits
(MoleculeACE/benchmark/featurization.py).

## Statistic and exact thresholds (frozen)

Let B = my reproduced baseline (SVM/ECFP, repo config, deterministic) and M = my frozen recipe,
both trained on the official 2476 train rows, both read on the official 621 test rows ONCE.
1. mse_cliff(M) < mse_cliff(B), where mse_cliff is sklearn MSE over the 296 test rows with
   cliff_mol==1, AND
2. mse_noncliff(M) ≤ mse_noncliff(B) (621−296 = 325 rows), AND
3. baseline reproduction gate: my B's overall test RMSE within ±10% of the paper's 0.715
   (0.6435–0.7865); if it misses, the p2 comparison is UNRESOLVED (no claim), diagnose only.
   (The paper's values are means over its runs; ±10% is the same tolerance convention as PREREG.)
4. null_test: required. The frozen recipe M, retrained 400 times with train labels shuffled
   (rng 20261118+k), must score test MSE worse than the real M for every control
   (real beats all 400 on OVERALL test MSE — the headline statistic; the cliff/noncliff split
   is additionally reported per control).
5. Test-read budget for this prereg: (i) the baseline B read (one test evaluation, required for
   the p2 comparison itself); (ii) at most TWO frozen-candidate reads M1, M2, each declared in
   NOTES with its OOF evidence BEFORE the read. Selection only on OOF CV over the 2476 train
   rows (5-fold, seed 20261118). Every read reported.

## Recipe construction rules (frozen)

Member pool: SVR (ECFP4/ECFP6/FCFP4/MACCS/RDKIT2D/counts, repo gamma grid incl. C=10 gamma=0.01),
RF (250 trees, seeds 0-4), replica-averaged RF, LGBM, KNN, SVR_SHRINK, MMP_LITE. NCD excluded
(pool decision made on OOF before any test read; if its OOF wins it may be included, declared).
The baseline SVM/ECFP (repo config) is FORCED into the pool as a member, so the ensemble is
never worse than B on OOF by construction. Combiner: greedy forward on OOF; weights by
non-negative ridge with inner-CV alpha (NOT coordinate descent on OOF residuals — v1 lesson:
that overfits 489-row OOF; on 2476 rows the risk is lower but the same failure mode is excluded
by freezing the ridge combiner).

## Honesty notes

- The p2 claim is scoped EXACTLY: one target (CHEMBL244_Ki), my recipe vs my reproduced
  repo-config SVM/ECFP baseline, cliff subset + non-cliff non-inferiority. Nothing about the
  leaderboard (the listed best 0.4750 on chembl244-ki is a 3-entry table and NOT part of p2).
- The leaderboard page for chembl244-ki was fetched once (2026-11-18T00:33Z, survey) and will be
  re-fetched at claim time only for the report's status line, not as a comparison bar.
