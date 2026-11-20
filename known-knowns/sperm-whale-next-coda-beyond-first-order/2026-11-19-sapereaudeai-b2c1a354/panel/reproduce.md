# REPRODUCE skeptic verdict: partial win p4 (turn-taking), target sperm-whale-next-coda-beyond-first-order

context: subagent (Claude Code Agent tool, reproduce type)

Scope: claim package only (CLAIM.md, REPRODUCE.md, PREREG.md, PREREG.v2.md, baseline/, result/, code/, null/). No other run file was read.
All paths below are relative to the claim folder; my own work lives in `../panel_work/reproduce/` (scripts in `scripts/`, fetched data in its own new directory `fetched/`, outputs in `out/`).
All Python ran as `python -I -B` on the run's venv interpreter, single-threaded, one job at a time, with the data path passed as an argument. No installs. Nothing was unpickled. There was no outward action, and no credentials were asked for or handled.

## Definitions my checker implements (quoted)

- Bank criterion: "Streams: codas grouped by REC, ordered by TsTo, with ties (7 in the file) kept in file order." "Folds: sort the distinct REC strings and put the i-th in fold i mod 5; each fold is held out once." "Scored: every coda with at least 2 earlier codas in its stream."
- p4: "predict whether the next coda carries the same whale label as the previous one with held-out log-loss at least 0.05 bits below a smoothed first-order model of that same-or-switch sequence, with a bootstrap interval over REC groups excluding 0."
- Readings frozen in PREREG.md and restated in CLAIM.md: "Target y_t = 1 if Whale_t equals Whale_{t-1}". The reference is "P(y_t | y_{t-1}) from training-fold counts with additive smoothing alpha chosen from the R1 grid {0.01, 0.03, 0.1, 0.3, 1} by inner leave-one-training-fold-out CV". Counts are over "positions >= 2 of training streams". Inner CV takes the "total held-out log-loss on that fold's scored positions; the grid value with the lowest total wins, ties to the first grid value". The bootstrap resamples the "REC groups owning a scored position, with replacement, statistic = pooled per-coda gain".

## My checker (written before reading any author code)

`../panel_work/reproduce/scripts/check_p4.py`:
- Reads the CSV with the `csv` module, not pandas.
- Builds streams by a stable sort on TsTo within each REC (ties keep file order) and assigns folds from the sorted REC strings.
- Computes y_t from the Whale labels, compared both as raw strings and as numbers, and builds the scored set t >= 2.
- Fits the binary first-order reference with P(same | s) = (n(s,same) + alpha) / (n(s) + 2 alpha). Alpha comes from leave-one-training-fold-out inner CV with ties to the first grid value, then the reference is refit on the 4 training folds.
- Compares everything with result/folds.csv, result/p4_per_position.csv and result/p4_summary.json.
- Recomputes the bits per row as -(y log2 p + (1-y) log2(1-p)) and runs its own REC bootstrap with a fresh seed.

`scripts/boot_extra.py` runs more bootstrap seeds and a reference-sensitivity check. `scripts/my_leak.py` is my own leakage and training-isolation test against the author's fitted model. `scripts/cmp_null.py` is the null spot check.

## Checks

| # | Check | Result |
|---|---|---|
| 1 | One plain fetch of data/sperm-whale-dialogues.csv from the pinned commit 7228c8ee… (V3R1T4S User-Agent, 60 s timeout): HTTP 200, 500,380 B, 2026-11-19T10:16:26Z. sha256 = 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2, equal to the claim's and to data/sperm-whale-dialogues.csv. | PASS |
| 2 | Streams: 3,840 rows, 219 RECs; 7 TsTo ties inside a REC (7 tie groups), matching the bank's "7". The author's pandas stream objects equal mine field by field and fold by fold (0 mismatches). | PASS |
| 3 | Folds regenerated from the sorted REC strings equal result/folds.csv for all 219 RECs. Per-fold coda counts are 598/1387/593/779/483. | PASS |
| 4 | Scored set: my 3,418 (REC, pos, fold, y_same) tuples equal the saved file's as a set, with no duplicates. The saved order is (fold, REC, pos). Per fold n = 514/1305/508/692/399. Same-label rate 0.3639555. Raw-string and numeric label equality agree at every transition. | PASS |
| 5 | My reference: inner-CV alpha per fold = 1.0, 0.01, 1.0, 0.01, 1.0, the same as the saved values. max abs(my P_ref - p_same_ref) = 0.0 over 3,418 rows. P(same given previous switch / same) is 0.228832/0.599808, 0.230429/0.603624, 0.226120/0.604147, 0.243517/0.604852 and 0.225331/0.582781 (folds 0-4), the same as the summary to 0.0. | PASS |
| 6 | Every p_same_ref, p_same_model and p_same_pattern is finite and strictly inside (0,1): model min 0.0165904, max 0.965612; reference 0.225331 to 0.604852; pattern 0.105778 to 0.790395. The binary distribution (p, 1-p) therefore sums to 1 with no zero entry. | PASS |
| 7 | My log-losses from the per-position file: reference 0.8503173539892255, model 0.7631118132162007, pattern 0.7908640718479825, gain 0.08720554077302466 bits per coda. Per fold (ref/model/gain): 0.8664/0.7937/+0.0727, 0.8494/0.7801/+0.0693, 0.8835/0.7325/+0.1511, 0.7903/0.7168/+0.0735, 0.8945/0.7875/+0.1070. Pooled and per-fold numbers equal result/p4_summary.json and the CLAIM table exactly (abs diff 0.0). The gain is at least 0.05. | PASS |
| 8 | Bootstrap with fresh seed 4242 over the 188 REC groups (10,000 resamples) gives 95% [0.065079, 0.115928]; the lower bound is above 0. Seeds 1, 99991 and 31337 give [0.065033, 0.116563], [0.065513, 0.116273] and [0.065524, 0.116111]; no resample in any seed was at or below 0. My implementation with the author's seed 20261119 gives [0.064864, 0.116622], equal to the claimed [0.0648639, 0.1166217]. | PASS |
| 9 | The reference does not depend on the smoothing choice. A fixed alpha anywhere in the grid, or alpha = 0, gives pooled 0.85033191 to 0.85033230. A per-fold oracle alpha (peeking at held-out data) gives 0.850314708, so the model's gain stays 0.087203 to 0.087220. | PASS |
| 10 | The author's frozen pipeline (REPRODUCE.md step 2), run on a hash-verified copy of code/ with the fetched CSV, ran twice. Both result p4_per_position.csv files are byte-identical to the saved file (sha256 b2c1a354…cdad6), and both p4_summary.json files are byte-identical to the saved one (sha256 12991940…57a). Per-fold console output equals result/run_output.txt apart from the timings. GATE p4 met. Deterministic. | PASS |
| 11 | Code hashes: code/swlib.py, leak.py, p4lib.py and score_p4.py equal the sha256 values frozen in PREREG.md. | PASS |
| 12 | My leakage test (`scripts/my_leak.py`, seed 8675309), against the model refit by the author's own fit_fold. The refit's batch predictions are bit-identical to the saved file at 3,418 of 3,418 positions, and the single-position path differs by at most 3.33e-16. At every held-out scored position I applied three perturbations. P1: every field of the predicted coda only, with Whale_t set so that the target y_t flips, TsTo_t set equal to TsTo_{t-1}, and nClicks, Duration and ICI1-28 shifted. P2: every field of the predicted coda and of all later codas, with my own random values, plus the target flip. P3: every float field of codas t onward set to NaN, nClicks to 1e9 and Whale to -999. Model and reference predictions changed at 0 of 3,418 positions under each of P1, P2 and P3, and the feature vector changed at 0 of 3,418. Positive controls reading Whale_t, nClicks_t or TsTo_t were flagged at 3,418 of 3,418. | PASS |
| 13 | Training isolation (mine): for each fold I replaced every field of every row of the held-out fold's streams with random values and refit. C, the C-selection losses, alpha, P_ref, the scaler mean and scale, and the LR coefficients and intercept were all bit-identical in all 5 folds, so the frozen model is trained on the training folds only. Training rows per fold = 3,418 minus the held-out n (2904/2113/2910/2726/3019). | PASS |
| 14 | Code read (after checks 1-9): p4lib.feats takes only the History view `_hist(s, t)`, which copies `v[:t]` of every field. It reads Whale, TsTo and Duration at t-1, t-2 and t-3, nClicks at t-1, and stream-local aggregates over rows [:t]. No field of coda t or later is read. Whale[t] is read only by `target()`, which supplies the label y. The p_ref index uses Whale[t-1] and Whale[t-2]. The StandardScaler sits inside the pipeline, fitted on training rows. swlib.switch_counts and switch_ref_fit implement the same reference as my checker, and swlib.rec_bootstrap draws resamples as my code does (hence the identical interval at seed 20261119). | PASS |
| 15 | Diagnostics from the saved file, my code, fresh seed 4242. Pattern-only LR: +0.059453 [0.044153, 0.078595]; claimed +0.0595 [0.0437, 0.0793]. Multi-label RECs (3,181 positions, 130 groups): +0.058957 [0.034793, 0.081735]; claimed +0.0590 [0.0347, 0.0809]. Single-label RECs (237 positions): mean +0.466353; claimed +0.4664. Folds 0, 1 and 3 (2,511 positions): +0.071140 [0.044210, 0.102835]; claimed +0.0711 [0.0441, 0.1036]. | PASS |
| 16 | Null controls (null/N4_controls.csv): 400 rows, ids 0-399 complete, seeds 1000+i. Max +0.000947, mean -0.005921; 0 of 400 at or above the real +0.087206. I reran controls 0-9 with null/nulls.py (N4) on the fetched CSV and all 10 are bit-identical to the saved rows (max abs diff 0.0). This is a spot check of reproducibility only; I did not rerun all 400. | PASS (spot check) |

## Notes (not failures)

- Bin edges are part of the main criterion's deliverables, but the p4 model and reference use no duration bins, so the bin-edge regeneration does not apply to p4.
- The 237 positions in single-label RECs carry a large average gain (+0.466 bits). On multi-label RECs alone the gain is +0.0590 with a REC-bootstrap lower bound of 0.0348 at my fresh seed. CLAIM.md discloses this. Whether it bears on reading "the dialogues folds" literally is for the CRITERION lens; the claimed numbers reproduce either way.
- The author's alpha picks alternate between 0.01 and 1.0 because the inner-CV totals differ only in the 4th to 5th decimal. This is immaterial (check 9).

## Key numbers reproduced

n = 3,418; reference 0.8503 bits per coda; model 0.7631; gain +0.0872. 95% REC bootstrap: [0.0649, 0.1166] at the author's seed and [0.0651, 0.1159] at my fresh seed 4242. Leakage: 0 of 3,418 positions changed under each of my three perturbations. Frozen rerun byte-identical twice.

No mismatch found.

pass: true
