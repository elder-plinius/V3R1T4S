# PREREG (frozen 2026-10-19T19:37Z, before any model was scored on any test split)

criterion (verbatim from target.md): see target.md. One element per claim.

null_test: not needed because the claim is an explicit saved model plus a predictions file scored by a deterministic checker against a table value; the required trivial baselines (zero-force and train-mean-force) and the seed spread are reported instead (below).

## Elements and order
Mo, Ni, Si, Cu, Ge, Li (stop when budget ends; an element is attempted only after the previous one has a complete package or a documented miss).

## Metric (frozen)
Force MAE = mean over all flattened force components of |pred - truth| on the benchmark json 'test' ids, eV/A. Checker reproduced the listed snap_mlearn and alignnff_mlearn_all_wt1 Mo values to all digits (scout.md).

## Data protocol (frozen)
- Training data: benchmark json 'train' ids only; structures from jarvis-tools figshare 'mlearn' (forces verified equal to the benchmark json).
- The benchmark has no val key. Val = train ids at positions i%10==5 in the benchmark's own order (stratified across the dataset's groups, as the official test split is).
- Selection phase: fit on train minus val, tune/select ONLY on val force MAE. Test labels are not read during selection.
- Final phase: retrain the selected configuration on all train ids with seeds 1, 2, 3 (fixed now); prediction = mean of the 3 seeds' forces. Test is scored once per element for this ensemble and for each seed. No retuning after seeing test; a changed plan would be PREREG.v2.md.
- No pretrained weights of any kind.

## Model families (cheapest first)
F1: MACE trained from scratch (mace-torch, CPU, 4 threads), small sizes (hidden 16/32/64 channels, L=1, r_max 4.5/5.5, 2 layers), forces-weighted loss; sizes chosen on val.
F2 (only if F1 misses on val by a clear margin and budget remains): same MACE on the residual of a fitted pair potential (delta-learning).
Linear ACE/MTP/GAP were considered; no Windows-installable implementation was available, so they are not attempted (to be revisited on Linux).

## Success rule (frozen)
Claim an element only if: ens_test_MAE + 2*sd_seed <= 0.95 * live_best_MAE (live_best re-fetched right before claiming), where sd_seed is the sample standard deviation of the 3 individual-seed test MAEs; AND saved model re-run reproduces predictions to 1e-6 eV/A; AND no test ids in any training path. Otherwise the element is reported as a miss.

## Baselines reported with every package
zero-force MAE, train-mean-force MAE, the live best, the seed spread.
