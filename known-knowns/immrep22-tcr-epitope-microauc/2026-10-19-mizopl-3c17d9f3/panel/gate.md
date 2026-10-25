# Gate Decision: `immrep22-tcr-epitope-microauc`

target_id: immrep22-tcr-epitope-microauc
category: disease-research
reproduce_pass: true
novelty_pass: true
criterion_pass: true
confirmed_scope: Multi-Chain (alpha/beta/alphabeta) OOB + Analytical LOO + CSLS Hubness-Corrected CLSS Ensemble trained strictly on claim/training_data/ achieves 17-epitope _Average MicroAUC = 0.882173 in claim/clss_tcr_stats.txt (856 bytes, sha256 3c17d9f39dc9b72c93441d4cc5d4b9fae9d986fe09f8abf3b27fe971d0212090) via the official claim/evaluation/evaluate.py vs the best published tcrexab = 0.847347 (+0.034826 >= +0.0200, winning 15/17 epitopes with 1-sided Wilcoxon p = 6.7139e-04 and 9/17 epitopes over all 22 published methods), single-epitope SPRWYFYYL MicroAUC = 0.877874 vs published column max 0.837823 (+0.040050 >= +0.0300, p1), companion Task 2 _Average Rank = 2.859120 vs published best 3.284289 (-0.425169 <= -0.2500, p2), 17-epitope negative-sampling provenance audit across clss_tcr, tcrexab, tcrexb, and tcrexa (p3), zero control-repertoire overlap, and Levenshtein d_Lev >= 2 MicroAUC = 0.868783 (+0.037753 over d_Lev >= 2 tcrexab 0.831030 and +0.021436 over full-set 0.847347), after reproducing tcrexab (0.846619), tcrexb (0.831443), and tcrexa (0.785032) within <= 0.0024.

## Panel Summary

1. **REPRODUCE (`panel/reproduce.md`, `pass: true`):**
   - Wrote an independent standalone checker (`indep_immrep22_check.py`) from the verbatim definition before inspecting `claim/author_checker_immrep22.py` or `claim/run_clss_immrep22.py`.
   - Verified byte counts and `sha256` checksums of all artifacts (`claim/clss_tcr_stats.txt` `sha256: 3c17d9f3...`, `claim/immrep22_audit_manifest.json` `sha256: 84eaaa15...`, `claim/clss_tcr_scores/SPRWYFYYL.txt` `sha256: 3313dcb9...`, `claim/clss_tcr_scores/testSet_Global.txt` `sha256: 7b67dfa0...`, and official `evaluation/` files).
   - Ran `claim/evaluation/evaluate.py`, `claim/author_checker_immrep22.py`, `claim/run_clss_immrep22.py`, and `claim/audit_immrep22_p3_and_leakage.py`, reproducing `claim/clss_tcr_stats.txt` and `claim/immrep22_audit_manifest.json` bit-for-bit.

2. **NOVELTY (`panel/novelty.md`, `pass: true`):**
   - Performed single honest HTTP `GET` fetches of `microaucs.csv` (`tcrexab = 0.847347`, `SPRWYFYYL` max `0.837823`) and `epitoperank.csv` (`tcrexab = 3.284289`).
   - Audited the last 24 months of literature (`110` citations to Meysman et al. 2023; recent Oct 13, 2026 bioRxiv `10.64898/2026.10.13.758726` reporting `0.8394` mean micro-AUC), confirming our `0.882173` strictly beats all published results.
   - Confirmed `0` occurrences in V3R1T4S `TROPHY_CASE.md` and `0` open pull requests touching `immrep22-tcr-epitope-microauc`.

3. **CRITERION (`panel/criterion.md`, `pass: true`):**
   - Verified every clause of the full `success_criterion` and all three enumerated partial wins (`p1`, `p2`, `p3`) simultaneously, plus pointwise inductive scoring (`|diff| <= 4.66e-15`), zero control-repertoire overlap (`0 / 17`), Levenshtein $d_{\text{Lev}} \ge 2$ exclusion (`0.868783` vs `0.831030`), 400-permutation null model (`z = +22.63`), and negated-score control (`0.118008`).

status: CONFIRMED_SOLUTION
