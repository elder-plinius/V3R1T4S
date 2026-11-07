# Skeptic 3: Target Criterion & Zero-Leakage Audit

context: independent rule and protocol audit started from target definition and solver code only

## Audit Summary

1. Inspected `how-we-built-it/solve_cami2_unsupervised.py` and verified via static AST and source analysis that the solver operates 100% unsupervised on candidate `.binning` assignments and intrinsic contig sequence lengths (`seq_len`), with zero access to ground-truth genome labels (`BINID` in `ground_truth/`), taxonomy (`TAXID`), or AMBER evaluation tables.
2. Verified that `verify-it-yourself/check_cami2_binning.py` implements the exact AMBER evaluation definitions (`CAMI-challenge/AMBER` and `second_challenge_evaluation/binning/genome_binning/scripts/recovered_g.py`): `recall_bp = tp_length_bp / gs_length_bp > 0.90`, `precision_bp = tp_length_bp / total_length_bp > 0.95`, and base-pair Adjusted Rand Index (`ARI (bp)`) computed from the contig-length confusion matrix over binned contigs.
3. Confirmed that partial-win criteria `p1`, `p2`, and `p3` in `bank/targets.json` are all strictly satisfied.

pass: true
