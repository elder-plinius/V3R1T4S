# PREREG.v2: private-quarry-B (charter Q15), run 2026-10-18-0202: mean BLEU at 0.10, 0.20, 0.30 (test scoring deferred)

Frozen at 2026-10-18T07:19:21Z (from date -u) by the main session (Opus 5.5, claude-opus-5-5[1m]), BEFORE the objects below exist. This
is an addition to PREREG.md (unchanged), written after that PREREG's NED cells were scored and gated. Charter v4.5 asks
this lane for its proportions "on all three metrics"; PREREG.md claimed mean NED only, and the test BLEU and BCFS of every
object scored so far are known (out/score_test.out), so none of those objects may carry a BLEU or BCFS claim. This file
pre-registers NEW objects for mean BLEU. BCFS is not attempted here (it is a B-cubed score over each language's pooled
alignments, not a sum of item scores, so the per-item rule below does not apply to it).

Disclosure for the skeptics: the main session has seen the test BLEU of all 11 frozen entries, COMB-NEW and COMB-ALL10
at 0.10-0.30 (they beat Mockingbird-I1 and FeVeT on BLEU). The objects below use the same entry lists and differ only in
the per-item risk and the weight-fitting statistic; nothing below uses test gold.

## Cells (one claim per cell, each in its own run folder created by the session that scores it)
| cell | P | entries (order) | bar = highest mean BLEU known at P (official scale, left-to-right) |
|---|---|---|---|
| L10 | 0.10 | out/comb_all10_entries.json (7) | our own COMB-ALL10 0.7339216116265356 (FeVeT 0.6833751184272755, Mockingbird-I1 0.6633184488563897) |
| L20 | 0.20 | out/comb_new_entries.json (6) | our own COMB-NEW 0.7080911153196365 (Mockingbird-I1 0.632633947442519; FeVeT none) |
| L30 | 0.30 | out/comb_new_entries.json (6) | our own COMB-NEW 0.6839233380559118 (FeVeT 0.6356571184958077, Mockingbird-I1 0.6058548112827981) |
The bars include our own NED-targeted objects of this run, so a BLEU claim is not subsumed by them.

## Object (one per cell, no selection among variants)
BLEU-MBR combiner (tools/stage2_bleu.py, written after this file): for each item with candidate strings c_1..c_K (the
entries' frozen predictions), output c_i with i = argmin_i sum_j w_j * (1 - BLEU(c_j -> c_i)) + 1e-7*(3 - w_i) + 1e-9*i,
where BLEU(a -> b) is the official scorer's per-item bleu_score(a, b, n=4, trim=False) with a in the gold slot (an empty
prediction becomes 2*len(a) 'Ø' as in compare_words). Weights w in {0,1,2,3}^K minus the zero tuple, fit at P on all 10
val-P families (main_only/val_gold; cut from training-P) by maximising the official mean BLEU (compare_words aggregation,
statistics.mean over families); tuple ties: higher BLEU rounded to 12 decimals, then smaller weight sum, then
lexicographically smaller tuple. Test predictions written with those weights and frozen (sha256) in this session.

## Rules
1. No surprise-test gold is read for these objects in this session. A later session scores them (official scorer, both
   summation modes; Mockingbird-I1 reproduced bit for bit first), runs a paired permutation null of 400 controls against
   the bar holder's per-item predictions with the item BLEU (swap per cognate set, random.Random(20261018 + c)), runs the
   sealed checks it needs (every entry is already sealed at its P: out/sealed_*.log, out/sealed2_*.log; run 1806's two
   entries by that run's check), and panels each cell that meets: (i) mean BLEU higher than the bar by more than 1e-9 in
   both summation modes; (ii) the null passes (real difference above every control). Otherwise the cell is NOTHING.
2. Data rules are those of PREREG.md (rules 5-7).
null_test: required
