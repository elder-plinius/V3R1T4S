# CRITERION skeptic verdict: n = 14 claim (instance_n14.prefs, 24992 stable matchings)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

What I read: CLAIM.md, REPRODUCE.md, instance_n14.prefs, A357271.txt, a357271_1.txt, count_stable.py and smcount3.c, all in the claim folder, and nothing else in the run folder. Everything ran on a copy at `../panel/scratch_criterion/claim`. My own checking scripts are `../panel/scratch_criterion/tools/verify_criterion.py` and `../panel/scratch_criterion/tools/baseline2.py` (panel scratch, not part of the claim). All paths here are relative to the claim folder. I ran on one thread at `nice -n 15`. The claim folder itself was not modified: its hashes were identical before and after all runs.

## 0. File identity

```
$ shasum -a 256 instance_n14.prefs a357271_1.txt A357271.txt count_stable.py smcount3.c CLAIM.md REPRODUCE.md
2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965  instance_n14.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
54ad7882acc3c6d5d6eb6d0979c179ff7956aec5c42a6eb96f47667652a8c524  count_stable.py
41ec90df17cadde0d657d5aaa118dd34c54e983ac21fe7b4cd6adef8f2eb56f2  smcount3.c
4f1827dc9ea396270f3e58afabb7362d11499ce8f1b6ba48473e008aea47c9f3  CLAIM.md
b8f50c1750dfd84a4aefbe78f4c66067774f3657492a4a2be385ff71c5541a7f  REPRODUCE.md
```
The object hash matches CLAIM.md's "object sha256", and the three hashes listed in REPRODUCE.md match.

## 1. The criterion, word by word

Verbatim (CLAIM.md): "for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men and n women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13 (beat 7,123), n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap calibration cell. Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact. Shape: record (explicit preference lists; stable matchings counted exactly by your own enumerator: closed subsets of the rotation poset, or exhaustive enumeration, cross-checked)."

Requirements extracted:
- R1 (which n): one n whose maximum is not known, not in {6, 8, 10, 12, 16}. The enumerated cells are 13, 15, 14 and 7; n = 14 is a named cell with the bar 20,176.
- R2 (the object): a stable-marriage instance with exactly n men and n women, every list complete and strict, given as explicit preference lists.
- R3 (the bar): "the best known instance of size n". For the n = 14 cell the criterion itself sets this to 20,176, and it has to match the status source.
- R4 (comparison): strictly more stable matchings than the bar.
- R5 (counting): exact counting by the claimant's own enumerator (closed subsets of the rotation poset, or exhaustive enumeration), cross-checked.
- R6 (scope): one cell. Success is existential ("for an n"), so beating one named cell is a win for that cell. This claim covers only n = 14 and says nothing about n = 13, 15 or 7.

## 2. Requirement-by-requirement check

### R1: n = 14 is allowed. MET.
My own parse of the instance (verify_criterion.py):
```
[1] row_lengths: [14] n (entries per row): 14
```
The status source's comment lines (verify_criterion.py, quoting A357271.txt):
```
[2] %C lines:
      a(n) is from Appendix C of Thurber's 2002 paper, using the maximum from each row. At the time of publication, the bounds were known to be exact up to n=4. A357269 shows that they are also exact for n=5. This sequence is not to be confused with A069156, also from Thurber's Appendix C, which uses only the first column, making for looser bounds for n > 11. a(6), a(8), a(10), a(12), and a(16) are also conjectured to be exact.
      Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.
```
So n = 14 is not known exact, not conjectured exact, not excluded, and it is a named cell.

### R2: an order-14 instance with 28 complete strict lists. MET.
```
[1] comment_lines: 1 data_lines: 28 blank_lines: 0
[1] row_lengths: [14] n (entries per row): 14
[1] data_lines == 2n: True
[1] every line a permutation of 1..14 (complete, strict, no ties/repeats): True (28/28)
[1] non-integer tokens: []
```
Lines 1-14 are the men's lists over women 1..14 and lines 15-28 are the women's lists over men 1..14, as CLAIM.md specifies. The single `#` comment line is skipped by every parser, mine included. Both provided parsers also reject bad input: count_stable.py asserts each list is a permutation, and smcount3.c rejects ragged rows, row counts other than 2n, and non-permutations.

### R3: the bar is 20176. MET for the value; the citation is wrong (see D1).
```
[2] A357271 offset: 1 number_of_terms: 28
[2] terms n=1..16: {1: 1, 2: 2, 3: 3, 4: 10, 5: 16, 6: 48, 7: 71, 8: 268, 9: 330, 10: 1000, 11: 1231, 12: 6472, 13: 6720, 14: 20176, 15: 25011, 16: 195472}
[2] A357271 a(14) = 20176
[2] %N: Lower bounds for the maximum number of stable matchings in the stable marriage problem based on composing smaller instances.
```
The 14th term of the data line (offset 1) is 20176, which matches the criterion's "beat 20,176". The newer linked file improves only n = 7, 9, 11, 13, 15 and has no n = 14 entry of any kind:
```
[3] 'order N example with K SM' headings: [('7', '81'), ('9', '365'), ('11', '1690'), ('13', '7123'), ('15', '27059')]
[3] lb(N)=K lines: [('7', '81'), ('9', '365'), ('11', '1690'), ('13', '7123'), ('15', '27059')]
[3] MiniZinc 'n = N;' blocks: ['7', '9', '11', '13', '15']
[3] any n=14 in headings/lb/blocks: False
[3] occurrences of '20176' in a357271_1.txt: 0 | of '24992': 0
[3] occurrences of '24992' in A357271.txt: 0
```
So the status source's n = 14 value is 20176 (revision #23, May 26 2025), from Thurber's (2002) composition table. The status source gives no explicit order-14 instance.

### R4: strictly more. MET.
```
[5] 24992 > 20176 (strict): True | difference: 4816 | ratio: 1.2387
```

### R5: exact counts, cross-checked. MET.
Provided counters, run from the copy of the claim folder exactly as REPRODUCE.md gives them (prefixed with `nice -n 15`):
```
$ python3 -I count_stable.py --prefs instance_n14.prefs --brute --expect 24992      (wrapped in time -p)
n: 14
lattice_count: 24992  (1.47s)
brute_count: 24992  (3.16s)
counters_agree: True
expected: 24992 PASS
real 5.76
user 2.41
sys 0.05
exit code: 0

$ cc -O2 -o smcount3 smcount3.c -lm        (no compiler diagnostics)
$ ./smcount3 count instance_n14.prefs 1
file: instance_n14.prefs
n: 14
rotations: 87
memo_states: 11165
count_poset: 24992
seconds_poset: 0.0021
count_lattice_verified: 24992
seconds_lattice: 0.0106
agree: yes
exit code: 0

$ ./smcount3 enumerate instance_n14.prefs
count_poset: 24992
enumerated_ideals: 24992
unstable_matchings_found: 0
n: 14
rotations: 87
seconds_enumerate: 0.01
agree: yes
exit code: 0
```
My own independent check (`python3 -I ../panel/scratch_criterion/tools/verify_criterion.py ../panel/scratch_criterion/claim`) uses no rotation theory and shares no code with the claim. It is a backtracking enumeration with pairwise blocking-pair pruning, run twice with different search trees (men in order, and women in reverse order). It stores every complete matching as a tuple in a set, then re-checks each one against the full definition, all n x n pairs:
```
[4] my_backtrack_men_order distinct matchings: 24992
[4] my_backtrack_women_reverse_order distinct matchings: 24992
[4] same set of matchings: True
[4] all are bijections: True
[4] all pass full definitional stability check: True
[4] equals claimed 24992: True
```
Positive controls: the provided Python counter reproduces known values.
```
$ python3 -I count_stable.py --knuth4 --brute --expect 10
n: 4 / lattice_count: 10 / brute_count: 10 / counters_agree: True / expected: 10 PASS   (exit code 0)
$ python3 -I count_stable.py --ident 8 --brute --expect 1
n: 8 / lattice_count: 1 / brute_count: 1 / counters_agree: True / expected: 1 PASS   (exit code 0)
$ python3 -I count_stable.py --oeis a357271_1.txt --n 7 --brute --expect 81
minizinc_blocks_match_paired_table: True / n: 7 / claimed_in_file: 81 / lattice_count: 81 / brute_count: 81 / counters_agree: True / expected: 81 PASS / matches_claimed_in_file: True   (exit code 0)
```
(Each control's output lines are joined with " / " here; nothing is omitted.) My script independently recounts the published order-7 instance exhaustively: `[7] published order-7 instance count (exhaustive): 81 (file says 81)`.

That makes seven exact counts of the claimed instance from four independent methods (rotation-poset ideal DP, lattice walk, reverse-search ideal enumeration, theory-free exhaustive backtracking), and all equal 24992. The counters are the claimant's own (smcount3.c's header says it was written for this lane).

### R6: one cell. MET.
The claim is about the n = 14 cell only, the third cell in the charter's priority order.

## 3. Stretched-definition hunt (nothing found)
- Ties or incomplete lists: none. All 28 of 28 lines are permutations of 1..14 and there are no non-integer tokens (R2 output).
- Non-square instance: none. There are 14 men and 14 women (28 data lines = 2n).
- Unstable matchings counted: none. Every matching I counted passes the full definitional check, smcount3 reports `unstable_matchings_found: 0`, and the Python lattice walk re-verifies every visited matching.
- Double counting: none. My counts are sizes of sets of distinct matchings, and two different search trees produce the identical set.
- The definition used is the standard one (no blocking pair, Gusfield and Irving Sec. 1.1). With strict complete lists on equal-sized sides there is no weak/strong/super ambiguity, and every stable matching is perfect (`all are bijections: True`). The quantity counted is stable matchings, not rotations or poset elements: the theory-free enumeration gives the same number.
- Reading the format: the parsers follow CLAIM.md's stated format (men first, most preferred first). Swapping which side is "men" would not change the count, because stable matchings correspond one-to-one.

## 4. Composition: is this just a re-listing of a known value? No.
CLAIM.md says (for information only) that the instance is the lexicographic product O[K2] of an order-7 instance with 85 stable matchings and Knuth's order-2 instance. I checked this directly against the file:
```
[6] instance == O[K2] with extracted outer O (men_flip=fix, women_flip=fix): True
[6] outer O stable matchings (exhaustive over 7! permutations): 85
```
- The status source's own n = 14 value is itself a composition bound (`%N: ... based on composing smaller instances`), so a composition-built instance is the same kind of object as the bar.
- 24992 appears nowhere in the status source (`occurrences of '24992' ...: 0` in both files), and the status source has no explicit order-14 instance at all.
- The order-14 count is not determined by the outer count alone. It had to be computed, and it was computed exactly. Baselines built with the same constructions from the status source's own published order-7 instance (81):
```
[7] baseline O81[K2] (order 14) stable matchings: 23744 | all stable: True | > 20176: True
K2[O81] (outer K2, inner published order-7): 13216
K2[O85] (outer K2, inner extracted order-7): 14450
O85[K2] rebuilt == instance: True | count: 24992
```
Conclusion: the claimed object is a new explicit order-14 instance whose exact count (24992) is larger than the table's value (20176). It is not a re-listing. One caveat: the 20176 bar is soft. Mechanically doubling the status source's own published order-7 instance already gives 23744 > 20176, a number that, as far as the status source shows, was never published. The claimed instance also beats that baseline (24992 > 23744). Whatever it gains beyond the baseline comes from the 85-matching order-7 instance, which CLAIM.md attributes to Jo (2026, Zenodo). That preprint is not in the claim folder; I confirmed only that the outer instance extracted from instance_n14.prefs has 85 stable matchings.

## 5. Null model
None is needed. This is an existence claim about one explicit finite object: the count is a deterministic function of the 28 lists, computed exactly by several independent methods, and compared with a fixed published number. Nothing is sampled or estimated, and no statistic or p-value is involved. How the instance was found (any search or selection over variants) cannot inflate an exact count of the final object. The only comparisons that matter are the bar itself (R3/R4) and the composition baselines in section 4, and all of them are below 24992.

## 6. Defects and residuals (they do not change the literal verdict, but must be handled)
- D1 (must fix before publication): CLAIM.md's "bar:" line attributes 20176 to "Ong, Ang, Ho, Eilers, Marks, Buzi (2025): lb(14)=20176, the explicit instance in the file linked from OEIS A357271 (a357271_1.txt ...)". That is false. The file has no lb(14), no order-14 instance and no "20176" (section R3 output). 20176 is term 14 of the A357271 data line, which A357271's %C attributes to Thurber's (2002) Appendix C composition table. The value is right; only the attribution is wrong.
- D2 (cannot be checked from claim/; for the panel lead): whether Jo (2026, Zenodo), whose order-7 instance the claim builds on, or any source newer than A357271 revision #23 already reports an n = 14 value of at least 24992. If one does, the claim is subsumed and this pass must be revisited. Both the status source and the charter ("no search has touched it") point to 20176 as the bar.
- D3 (wording): "the best known value 20176" should be scoped as "the n = 14 value listed in OEIS A357271", because a mechanical doubling of a published instance already exceeds it (23744, section 4).

## 7. Verdict
Every literal requirement is met. R1: n = 14 is a named, non-excluded cell. R2: an explicit 14 x 14 instance with complete strict lists. R3: the bar is 20176 per the criterion and per the status source. R4: 24992 > 20176. R5: exact counts by the claimant's own rotation-poset and exhaustive enumerators, cross-checked, and reproduced by my independent enumeration. R6: one cell. No stretched definitions were found, and the win is not subsumed by anything in the status source, including the same construction applied to the status source's own instances. D1 must be corrected and D2 checked by the lead before publication.

confirmed_scope: The explicit order-14 stable marriage instance in instance_n14.prefs (sha256 2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965; 14 men and 14 women, every list a complete strict permutation of 1..14) has exactly 24992 stable matchings by agreeing exact rotation-poset and exhaustive-enumeration counts, which is strictly more than 20176, the n = 14 term of OEIS A357271 as saved in A357271.txt (revision #23, May 26 2025) and the bar the criterion names for its n = 14 cell.
pass: true
