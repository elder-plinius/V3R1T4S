# CRITERION skeptic verdict (V3R1T4S panel)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Inputs read: CLAIM.md, REPRODUCE.md, instance_n13.prefs, published_n13_7123.prefs, a357271_1.txt, A357271.txt,
count_stable.py, smcount3.c. All paths in this file are relative to the claim folder. Every program was run in a scratch
copy of the claim folder (one thread, niced). The claim folder itself was not modified. Toolchain: Python 3.9.6, Apple clang 21.0.0.

Independent checker: ../panel/scratch_criterion/mine/verify_criterion.py. I wrote it fresh for this review, and it
imports nothing from the claim. It parses every file itself. It counts stable matchings by theory-free backtracking that
assigns a husband to each WOMAN in turn (the claim's brute force goes man by man) and prunes a partial assignment only
when two assigned couples already contain a blocking pair. It re-checks every complete matching from scratch against
the definition and stores every matching in a set, which rules out double counting. I calibrated it against plain
exhaustive enumeration of all n! bijections.

## 1. Criterion read word by word (verbatim in CLAIM.md)

> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men
> and n women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13
> (beat 7,123), n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap
> calibration cell. Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact.
> Shape: record (explicit preference lists; stable matchings counted exactly by your own enumerator: closed subsets
> of the rotation poset, or exhaustive enumeration, cross-checked).

Requirements extracted:
- R1: n is one whose maximum is not known, and n is not 6, 8, 10, 12 or 16.
- R2: the object is a stable-marriage instance with n men and n women (square).
- R3: every one of the 2n preference lists is complete and strict (no ties, no omissions).
- R4: the preference lists are given explicitly.
- R5: the cell is a named one, n = 13 with bar 7,123, and 7,123 is what the status source gives for the order-13 instance.
- R6: the instance has STRICTLY more stable matchings than the bar.
- R7: the count is exact and comes from the claimant's own enumerator (closed subsets of the rotation poset, or
  exhaustive enumeration).
- R8: the count is cross-checked.
- R9: one cell. The success condition is existential in n ("for an n"), so one named cell is enough. Nothing beyond
  that cell may be credited.

## 2. Requirement-by-requirement check

### R1: n = 13, maximum not known. MET
A357271.txt (%C line): "At the time of publication, the bounds were known to be exact up to n=4. A357269 shows that
they are also exact for n=5. ... a(6), a(8), a(10), a(12), and a(16) are also conjectured to be exact."
13 is neither known nor conjectured exact. It is the first named cell and is not on the excluded list.

### R2, R3, R4: explicit, square, complete, strict. MET
Object hash (matches the "object sha256" in CLAIM.md):
```
ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69  instance_n13.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```
My parser (verify_criterion.py, section 1). It requires pure-digit ASCII tokens and ignores the single '#' comment line:
```
== 1. claimed object instance_n13.prefs ==
comment_lines: 1  data_lines: 26  entries_per_line: [13]  has_CR: False  has_TAB: False
men_lines(1-13)_are_permutations_of_1..13: True
women_lines(14-26)_are_permutations_of_1..13: True
problems (ties/incomplete/non-square): none
```
The file holds 13 men's lists over women 1..13 and 13 women's lists over men 1..13, each a permutation of 1..13. It is
in the declared format (most preferred first).

### R5: the bar is 7,123, and published_n13_7123.prefs is that instance. MET
Status-source file a357271_1.txt (grep):
```
14:lb(13)=7123 (previously 6720)
136:/*  order 13 example with 7123 SM
```
A357271 data line, parsed by me (the older Thurber bound; 7123 is the larger of the two order-13 values in the status source):
```
A357271 offset: 1  terms: 28
A357271 data line a(7) = 71
A357271 data line a(13) = 6720
A357271 data line a(14) = 20176
A357271 data line a(15) = 25011
```
The charter's other bars (n=15: 27,059; n=14: 20,176; n=7: 81) also agree with the status source.

My own conversion of the order-13 ranking table follows the file's stated semantics: "a,b" in row i, column j is the
rank man i gives woman j and the rank woman j gives man i. Output from verify_criterion.py, sections 3-4:
```
== 3. status-source file a357271_1.txt (ranking tables) ==
lb(13) line in file: ['lb(13)=7123 (previously 6720)']
order blocks found (order: stated count): {7: 81, 9: 365, 11: 1690, 13: 7123, 15: 27059}
order 7: stated 81, my count 81 (distinct 81, leaves failing definition 0, 0.0s) -> MATCH
order 9: stated 365, my count 365 (distinct 365, leaves failing definition 0, 0.0s) -> MATCH
order 11: stated 1690, my count 1690 (distinct 1690, leaves failing definition 0, 0.1s) -> MATCH
order 13: stated 7123, my count 7123 (distinct 7123, leaves failing definition 0, 1.1s) -> MATCH
order 15: stated 27059, my count 27059 (distinct 27059, leaves failing definition 0, 6.3s) -> MATCH
order-13 MiniZinc rankMen == table first components: True
order-13 MiniZinc rankWomen == table second components (transposed): True
== 4. published_n13_7123.prefs vs my own conversion of the order-13 table ==
published file: data_lines=26 problems=none
published_n13_7123.prefs identical to my conversion (all 26 lists): True
my count on published_n13_7123.prefs: 7123 (distinct 7123, leaves failing definition 0, 1.0s)
```
The claim's counters on the published instance (REPRODUCE.md commands 4 and 5, plus smcount3):
```
$ python3 -I count_stable.py --prefs published_n13_7123.prefs --brute --expect 7123
n: 13
lattice_count: 7123  (0.27s)
brute_count: 7123  (1.02s)
counters_agree: True
expected: 7123 PASS
exit code: 0
$ python3 -I count_stable.py --oeis a357271_1.txt --n 13 --expect 7123
minizinc_blocks_match_paired_table: True
n: 13
claimed_in_file: 7123
lattice_count: 7123  (0.28s)
expected: 7123 PASS
matches_claimed_in_file: True
exit code: 0
$ ./smcount3 count published_n13_7123.prefs 1
file: published_n13_7123.prefs
n: 13
rotations: 71
memo_states: 5931
count_poset: 7123
seconds_poset: 0.0011
count_lattice_verified: 7123
seconds_lattice: 0.0073
agree: yes
exit code: 0
```

### R6: strictly more. MET
```
== 6. comparison ==
claimed count 7698 == my count: True
my count > 7123 (strictly): True  margin: 575
lists differing from the published instance (line numbers 1-26): [1, 3, 5, 7, 8, 9, 11, 13, 14, 15, 17, 19, 21, 23]  positions differing: 57
identical to published instance: False
```

### R7, R8: exact count by the claimant's own enumerators, cross-checked. MET
REPRODUCE.md commands 1-3, run verbatim in the scratch copy:
```
$ python3 -I count_stable.py --prefs instance_n13.prefs --brute --expect 7698
n: 13
lattice_count: 7698  (0.22s)
brute_count: 7698  (0.78s)
counters_agree: True
expected: 7698 PASS
exit code: 0
$ cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n13.prefs 1
compiled OK
file: instance_n13.prefs
n: 13
rotations: 72
memo_states: 8373
count_poset: 7698
seconds_poset: 0.0011
count_lattice_verified: 7698
seconds_lattice: 0.0028
agree: yes
exit code: 0
$ ./smcount3 enumerate instance_n13.prefs
count_poset: 7698
enumerated_ideals: 7698
unstable_matchings_found: 0
n: 13
rotations: 72
seconds_enumerate: 0.01
agree: yes
exit code: 0
```
These are five agreeing methods, all printing 7698:
- closed subsets of the rotation poset: smcount3 memoised DP;
- reverse-search enumeration of every closed subset, each converted to its matching and re-checked against the
  definition (0 unstable);
- rotation-lattice walks with a visited set and a stability re-check of every matching, in Python and in C;
- theory-free exhaustive backtracking over perfect matchings (count_stable.py --brute).

I read the source of both counters. Neither contains a hardcoded count. The brute force tests both blocking-pair
directions for every pair of assigned couples, which is sound and complete. The `--expect` flag only sets the exit
code, and the printed counts are computed independently of it.

My independent recount (verify_criterion.py, sections 2 and 5):
```
== 2. calibration of my counter against exhaustive enumeration of all n! bijections ==
order-4 Latin instance: exhaustive=10 mine=(10, 10)
random instances tested: 72, all agree with exhaustive enumeration: True
== 5. my count on the claimed instance ==
my count on instance_n13.prefs: 7698 (distinct 7698, leaves failing definition 0, 1.0s)
same instance with men and women swapped: 7698 (distinct 7698, failing 0)
same instance under a random relabelling of men and women: 7698 (distinct 7698, failing 0)
```

### R9: one cell. MET, scope limited
CLAIM.md names the cell n = 13 only. Nothing is claimed, and nothing is confirmed here, for n = 15, 14 or 7.

## 3. Hunt for stretched definitions and hidden quantifiers
- Ties: none. All 26 lists are permutations (R3 output).
- Incomplete lists: none. Every list has 13 entries.
- Non-square instance: none. 13 men and 13 women, 26 data lines.
- Relabelling of the published instance: impossible. The number of stable matchings does not change when men or women
  are renamed or when the two sides are swapped. My runs confirm this (7698 after a swap and after a random
  relabelling), and 7698 != 7123. The object differs from the published instance in 14 of 26 lists (57 positions).
- Counting unstable matchings: none. My counter found 0 leaves failing the definition, smcount3 enumerate reports
  unstable_matchings_found: 0, and both lattice walks re-check every matching.
- Double counting: none. My set of distinct matchings has 7698 elements, equal to the number of leaves. The lattice walks
  de-duplicate with a visited set.
- Format or orientation games: the declared format is the one under which my conversion of the status source's own
  table reproduces its stated 7123. My counter reproduces all five stated values in a357271_1.txt (81, 365, 1690, 7123,
  27059), so the bar instance is read with the right semantics. The count is invariant under swapping men and women, so
  a side mix-up cannot change it.
- "best known": the bar is the charter's named 7,123, which equals lb(13) in the status source. The data-line value
  6720 is lower. I did not search literature outside the status source (no web access, by design), so
  non-subsumption is established only against the status source as fetched (2026-10-14) and the charter's bar.
- "maximum not known": see R1.

## 4. Null models
None is needed. The claim is a deterministic exact count of one explicit finite object, compared with a fixed published
value. There is no sampling, estimate, score or significance claim, so there is no null distribution to test against.
The controls that do matter were run:
- positive controls: the same counters reproduce the published 7123, and my counter reproduces every value stated in
  the status-source file;
- calibration: my counter matched exhaustive n! enumeration on 72 random instances (n = 5..8) and the order-4 Latin
  instance (10);
- invariance: side swap and random relabelling leave the count unchanged.

## 5. Non-blocking observations
- The comment line of instance_n13.prefs records the search's provenance, including a file outside this package. Every
  parser ignores it. The sha256 covers the file including that line.
- The count_stable.py docstring says the brute force is "meant for n <= 9 or so", while CLAIM.md says it is feasible up
  to about n = 15. At n = 13 it ran in 0.78 s, so this has no effect.

## 6. Verdict
Every requirement R1-R9 is literally met in the named cell n = 13, the first-listed cell. The criterion's success
condition is existential in n, so this cell is a genuine win. Within the status source, it is not subsumed by the
published instance or by any value given there.

confirmed_scope: The explicit order-13 stable marriage instance instance_n13.prefs (sha256 ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69; 13 men and 13 women, all 26 lists complete strict orderings of 1..13) has exactly 7698 stable matchings, as counted by every counter supplied in the claim and by an independent brute-force recount, which is strictly more than the 7123 stable matchings of the order-13 instance stated in the status-source file a357271_1.txt (OEIS A357271, fetched 2026-10-14) and named as the charter's n = 13 bar, so the charter criterion is met in the n = 13 cell only.

pass: true
