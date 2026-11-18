context: subagent

# REPRODUCE-skeptic verdict — partial win p2 (activity-cliff MSE, CHEMBL244_Ki)

**The definition I was told to quote (verbatim, the p2 criterion in claim/claim.md):**

> "A cliff-subset result: on one target, lower MSE than a faithfully reproduced MoleculeACE
> paper baseline (the repo's own best descriptor+model for that target, run by the attacker and
> reported with its code) restricted to the test molecules with cliff_mol==1, with at least 40
> such molecules, while not being worse on the non-cliff subset."

## Method

Before reading any of the author's verify/ code, I wrote my own checker from that definition:
`panel/repro_check.py` (own file, own code). It recomputes everything from the claim package
alone (`claim/data/CHEMBL244_Ki.csv` + saved objects):

- CSV sha256 must equal the claimed `b296c5956c9b3659fa039f057ebcb617919acd759c9255ed72bee917d99b4ef2`
- official split = rows with `split=='test'` (621); both prediction files' `test_row_indices`
  must equal it exactly, in order; 2476 train rows; cliff test molecules must be 296 (>= 40)
- M1/B cliff-subset and non-cliff-subset MSE recomputed from `result/M1_predictions.json` and
  `result/B_predictions.json` against the CSV `y` labels, compared to the claimed full-precision values
- my own retrain of the baseline from the stated repo config — SVR(C=10, epsilon=0.1, gamma=0.01,
  kernel='rbf') on Morgan ECFP radius 2 / 1024 bits, trained on the 2476 train rows only — must
  reproduce `result/B_predictions.json`
- stereo-stripped InChIKey (skeleton block, first 14 chars) train/test disjointness
- consistency of the baseline record, paper rows, and machine-readable verdicts
  (`output/baseline_B_chembl244.json`, `data/MoleculeACE_results_CHEMBL244_rows.csv`,
  `output/M1_read_result.json`, `output/null_test_244.json`)

## Commands and pasted output

All commands run with the panel's designated interpreter (scikit-learn + rdkit venv, reached
relatively as `..\..\.venv-mace\Scripts\python.exe` from the folder containing `claim/`).
Full checker output also saved at `panel/run1.txt` and `panel/run2.txt`.

**Primary — my own checker, run 1:**

```
> ..\..\.venv-mace\Scripts\python.exe panel\repro_check.py claim
PASS | csv sha256 matches claim | b296c5956c9b3659fa039f057ebcb617919acd759c9255ed72bee917d99b4ef2
PASS | row count 3097, all rows split in {train,test} | rows=3097 train=2476 test=621
PASS | official split sizes 2476 train / 621 test
PASS | test cliff_mol==1 count == 296 and >= 40 | cliff=296 noncliff=325
PASS | M1 test_row_indices == rows with split=='test', exact order
PASS | M1 cliff-subset MSE matches claim | 0.5501943375378687
PASS | M1 noncliff-subset MSE matches claim | 0.33343039149183445
INFO | M1: mse_all=0.43675104854437247 mse_cliff=0.5501943375378687 mse_noncliff=0.33343039149183445
PASS | B test_row_indices == rows with split=='test', exact order
PASS | B cliff-subset MSE matches claim | 0.634573831368627
PASS | B noncliff-subset MSE matches claim | 0.39931062625682384
INFO | B: mse_all=0.511448965569374 mse_cliff=0.634573831368627 mse_noncliff=0.39931062625682384
PASS | M1 cliff MSE strictly lower than baseline B | 0.550194337538 < 0.634573831369
PASS | M1 noncliff MSE not worse than baseline B | 0.333430391492 <= 0.399310626257
PASS | every molecule parses to an InChIKey | parse_failures=0
PASS | no test InChIKey skeleton (stereo-stripped) appears in train | disjoint
PASS | ECFP fingerprint width 1024 | (2476, 1024)
PASS | my retrained SVR/ECFP (C=10,eps=0.1,gamma=0.01,rbf,r=2/1024b,train-only) reproduces B_predictions.json | max_abs_diff=0.000e+00
INFO | my B retrain: mse_all=0.511448965569374 rmse=0.7151566021294735 mse_cliff=0.634573831368627 rmse_cliff=0.7966014256631901 mse_noncliff=0.39931062625682384
PASS | baseline record (output/baseline_B_chembl244.json) matches my recomputed B
PASS | paper rows file has the CHEMBL244_Ki / SVM / ECFP row
PASS | my retrained B rmse matches repo published rmse 0.715156602 (<=1e-6) | mine=0.715156602 paper=0.715156602
PASS | my retrained B cliff rmse matches repo published cliff_rmse 0.796601426 (<=1e-6) | mine=0.796601426 paper=0.796601426
PASS | my retrained B rmse within the baseline record tolerance
PASS | SVM/ECFP is the repo's own best (lowest rmse) descriptor+model for this target | best=SVM/ECFP rmse=0.715156602
PASS | output/M1_read_result.json matches my recomputed MSEs
PASS | output/M1_read_result.json P2_THRESHOLDS_MET is true
REPRO_SKEPTIC: PASS
```

**Determinism — identical second run:**

```
> ..\..\.venv-mace\Scripts\python.exe panel\repro_check.py claim   # run 2, redirected
run1 sha256: 69BF171DCA8D4ECA01C38E3FBF23A4E8C11C0EA8915EE7DB4B63BEC7E1F22B33
run2 sha256: 69BF171DCA8D4ECA01C38E3FBF23A4E8C11C0EA8915EE7DB4B63BEC7E1F22B33
DETERMINISM: IDENTICAL OUTPUT
```

**Secondary — the author's own scripts, run only after my checker passed (from `claim/`):**

```
> ..\..\..\.venv-mace\Scripts\python.exe verify\verify_p2.py
M1  cliff 0.550194 noncliff 0.333430
B   cliff 0.634574 noncliff 0.399311
PASS  B == repo-config SVR recomputed max diff 0.00e+00
PASS  no InChIKey train/test overlap
VERIFY_P2: PASS

> ..\..\..\.venv-mace\Scripts\python.exe verify\baseline_B_244.py
 "mse": 0.511448965569374, "rmse": 0.7151566021294735,
 "mse_cliff": 0.634573831368627, "rmse_cliff": 0.7966014256631901,
 "mse_noncliff": 0.39931062625682384, "reproduced": true,
 "n_cliff_test": 296, "n_noncliff_test": 325
```
(identical to the package's `output/baseline_B_chembl244.json`; its side-effect folder
`claim/fx-baseline/` was removed afterwards to leave the package as found.)

**External cross-validation (live fetches of the two public sources named in REPRODUCE.md):**

- `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/configures/benchmark/CHEMBL244_Ki/SVM_ECFP.yml` →
  `C: 10 / epsilon: 0.1 / gamma: 0.01 / kernel: rbf` — exactly the repo config the claim states.
- `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/results/MoleculeACE_results.csv` →
  contains `CHEMBL244_Ki,SVM,ECFP,0,0.715156602,0.796601426`; every row of
  `data/MoleculeACE_results_CHEMBL244_rows.csv` matches the repo CSV row-for-row, and
  SVM/ECFP has the lowest rmse of all 24 rows for this target, i.e. it is genuinely
  "the repo's own best descriptor+model for that target".

## Findings

Confirmed from the claim package alone, deterministically:

1. **Same data:** `data/CHEMBL244_Ki.csv` sha256 matches the claim. Same label column `y`.
2. **Same split:** the test set is exactly the 621 rows with `split=='test'` (2476 train);
   both prediction files carry those exact indices, in order, with the slug
   `moleculeace-chembl244-ki` and the CSV sha recorded.
3. **Subset sizes:** 296 test molecules with `cliff_mol==1` (>= 40) and 325 non-cliff, as claimed.
4. **Same metric (MSE), recomputed from the CSV:** M1 cliff 0.5501943375378687 < B cliff
   0.634573831368627 (strictly lower, delta 0.0844); M1 non-cliff 0.33343039149183445 <=
   B non-cliff 0.39931062625682384 (better, i.e. not worse). All four match the claimed
   full-precision values to < 1e-12.
5. **Baseline faithfully reproduced — the strongest part of the claim:** my own retrain from the
   stated repo config (train rows only) reproduces `result/B_predictions.json` **bit-for-bit**
   (max_abs_diff = 0.00e+00), and the resulting rmse 0.7151566021294735 / cliff_rmse
   0.7966014256631901 match the repo's own published values (0.715156602 / 0.796601426) to < 1e-9,
   inside the record's tolerance and with the repo's published SVM/ECFP row verified live.
   The definition's "run by the attacker and reported with its code" is satisfied:
   `verify/baseline_B_244.py` is in the package and reproduces the record exactly.
6. **No train/test identity leakage at the molecule level:** stereo-stripped InChIKey skeleton
   blocks of all 3097 molecules computed; zero train/test overlap.
7. **Records consistent:** `output/baseline_B_chembl244.json` equals my retrain bit-for-bit;
   `output/M1_read_result.json`'s MSEs and `P2_THRESHOLDS_MET: true` match my recomputation;
   `output/null_test_244.json`'s `real_overall_mse` (0.43675104854437247) equals my recomputed
   M1 overall MSE and beats all 400 recorded label-shuffle controls.
8. **Determinism:** two complete runs byte-identical (same output sha256). SVR/ECFP is
   deterministic; no sampling anywhere in the verified path.
9. **Secondary agreement:** the author's `verify/verify_p2.py` and `verify/baseline_B_244.py`,
   run afterwards, agree with my checker on every number.

Caveats (on the record; none defeats the p2 definition):

- `claim.md` lists the baseline record as `baseline/baseline_B_chembl244.json`, but inside the
  claim package the same record is at `output/baseline_B_chembl244.json` (content verified
  against my retrain). No `baseline/` folder exists inside the package — a path-labeling slip,
  not a missing record.
- `claim.md` says REPRODUCE.md contains "exact commands (integrity, baseline, M1 retrain,
  verifier, null test)", but REPRODUCE.md actually documents only the standalone verifier
  command (`verify/verify_p2.py`, which is self-contained and passes). `verify/integrity_244.py`,
  `verify/M1_read.py` and `verify/null_test_244.py` reference data/artifacts outside the claim
  package (a run-root data dir, plus `output/M1_selection.json` and `output/sweep244_members.npz`,
  which are not in the package), so `result/M1_predictions.json` is verified as a frozen artifact
  (index alignment, MSE recomputation, verdict/null-test consistency) rather than by end-to-end
  retrain from the package. The baseline — the object the p2 definition requires to be
  reproducible — IS fully re-derived bit-for-bit. M1's selection provenance/leakage is the
  criterion skeptic's remit, not this panelist's.

## Verdict

Every property of the quoted p2 definition is confirmed from the claim package alone and is
deterministic on re-run: a faithfully reproduced repo-config baseline (bit-for-bit, matching the
repo's published numbers and its live-verified config and results row), the official
`split=='test'` evaluation on the exact CSV, 296 (>= 40) cliff test molecules, strictly lower
cliff-subset MSE for the candidate (0.5501943375378687 vs 0.634573831368627), and a better
(not worse) non-cliff MSE (0.33343039149183445 vs 0.39931062625682384).

pass: true
