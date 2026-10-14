# V3R1T4S panel: CRITERION skeptic (lane A, run 2026-10-14-1512)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Files read: claim/CLAIM.md, claim/REPRODUCE.md, claim/a357271_1.txt, claim/instance_n15.prefs,
claim/ong_n15_published_27059.prefs, claim/count_stable.py, claim/smclimb.c. Nothing else in the run folder was opened.
All commands ran on a copy of claim/ in panel/scratch_criterion/claim/, one process at a time on one CPU thread.
Every copied file has the same sha256 as the original, and claim/ was not modified:

```
CLAIM.md identical_to_copy=yes 7658a810da50439238222933dca205a3a83e20b947f521c249f99e7c2250ad0b
REPRODUCE.md identical_to_copy=yes c775a7fc1108d0225b8a90d8d5a442d01ad31bb67dfb2619817b61c29dc8caa6
a357271_1.txt identical_to_copy=yes 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47
count_stable.py identical_to_copy=yes 54ad7882acc3c6d5d6eb6d0979c179ff7956aec5c42a6eb96f47667652a8c524
instance_n15.prefs identical_to_copy=yes 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8
ong_n15_published_27059.prefs identical_to_copy=yes 586a5f5e7e4f124ebe57afe67273d5f5bba01f947f4ddd0397354f8fb001d600
smclimb.c identical_to_copy=yes 8244716dff88cd40678bd260f3678256c16b7f68615cc9e9f4ef6440878d317c
```

Both sha256 values that CLAIM.md and REPRODUCE.md state (instance_n15.prefs 3a7359d3...ab539a8 and
a357271_1.txt 95735e18...4db5cd47) match the files.

## 1. The criterion, word by word

The criterion as quoted in claim/CLAIM.md:

> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men
> and n women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13
> (beat 7,123), n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap
> calibration cell. Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact.
> Shape: record (explicit preference lists; stable matchings counted exactly by your own enumerator: closed subsets
> of the rotation poset, or exhaustive enumeration, cross-checked).

The criterion contains these requirements:

- R1, the quantifier on n. "For an n" is existential, so one cell is enough. "Cells in order" sets the order in which
  to search; it does not require every cell. The criterion lists no partial wins, so beating one cell meets the full
  criterion. An allowed n must be one whose maximum is not known. The named cells are 13, 15, 14 and 7. The excluded n
  are 6, 8, 10, 12 and 16.
- R2, the object. The instance must give complete strict preference lists for n men and n women: the same number of
  men and women, no ties, and nobody left out of any list.
- R3, the bar. The instance must have strictly more stable matchings than the best known instance of size n. For
  n = 15 the criterion states the number to beat: 27,059.
- R4, the count. The stable matchings (matchings with no blocking pair) must be counted exactly by the claimant's
  own enumerator, using closed subsets of the rotation poset or exhaustive enumeration, and the count must be
  cross-checked.
- R5, the shape. The preference lists must be explicit.

## 2. Requirement-by-requirement check

### R1: n = 15 is an allowed cell. Met.
- CLAIM.md says "cell: n = 15", and my parser reads `n_from_rows: 15` (output under R2).
- The criterion names 15 as a cell ("n = 15 (beat 27,059)"), and 15 is not in the excluded set {6, 8, 10, 12, 16}.
- The status source gives 27059 only as a lower bound, so the maximum for n = 15 is not known.
  `grep -n` on claim/a357271_1.txt:
```
15:lb(15)=27059 (previously 25011, or 26424 shown in A371810)
184:/* Order 15 example with 27059 SM
```

### R2: complete strict lists for 15 men and 15 women. Met.
I wrote my own parser, panel/scratch_criterion/tools/check_format.py; it shares no code with the claimant's.
Its output on the claimed file (the file also has no CR, TAB or non-ASCII bytes):
```
== claimed claim/instance_n15.prefs
  sha256: 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8
  total_lines: 31
  comment_line_numbers: [1]
  blank_lines: 0
  data_lines: 30
  n_from_rows: 15
  rows_even: True
  row_lengths: [15]
  men_lists_are_permutations_of_1..n: 15
  women_lists_are_permutations_of_1..n: 15
  ties_or_repeats: 0
  entries_outside_1..n: 0
```
The file has one comment line and 30 data lines. Each data line is a permutation of 1..15: lines 1-15 are the men's
lists (women, best first) and lines 16-30 are the women's lists (men, best first). There are no ties, no incomplete
lists, and the instance is square. Both provided counters also reject lists that are not permutations
(count_stable.py asserts; smclimb.c uses check_perms), and both accepted this file.

### R3: the bar is 27059, and 27510 is strictly greater. Met.
- The status-source file claim/a357271_1.txt (sha256 checked above) states `lb(15)=27059` and contains the block
  "Order 15 example with 27059 SM" (grep output under R1).
- My own conversion of that block's ranking table to preference lists is identical to
  claim/ong_n15_published_27059.prefs. Its MiniZinc rankMen/rankWomen blocks give the same lists:
```
== OEIS file, order 15
  header line lb(15): [('27059', ' (previously 25011, or 26424 shown in A371810)')]
  "Order 15 example with K SM": K = 27059
  MiniZinc blocks give the same lists as the paired table: True
  my conversion of the paired table == published .prefs men lists: True
  my conversion of the paired table == published .prefs women lists: True
  claimed instance == OEIS instance: False
```
- Every counter gives 27059 on the published instance, both from the .prefs file and parsed directly from the OEIS
  ranking tables (output under R4). So the bar is reproduced under the same definition and the same list reading as
  the claimed instance.
- The comparison:
```
27510 > 27059: True  margin: 451  ratio: 1.0167
```

### R4: exact count, by the claimant's own enumerators, cross-checked. Met.
These are the REPRODUCE.md commands, run in the copy of claim/, plus three controls. Output pasted verbatim:
```
$ python3 -I count_stable.py --prefs instance_n15.prefs --brute --expect 27510
n: 15
lattice_count: 27510  (2.66s)
brute_count: 27510  (11.88s)
counters_agree: True
expected: 27510 PASS
exit=0
$ cc -O2 -o smclimb smclimb.c && ./smclimb count instance_n15.prefs 1
file: instance_n15.prefs
n: 15
count: 27510
verify: 1
seconds: 0.0468
exit=0
$ python3 -I count_stable.py --prefs ong_n15_published_27059.prefs --brute --expect 27059
n: 15
lattice_count: 27059  (2.47s)
brute_count: 27059  (13.46s)
counters_agree: True
expected: 27059 PASS
exit=0
$ python3 -I count_stable.py --oeis a357271_1.txt --n 15 --expect 27059
minizinc_blocks_match_paired_table: True
n: 15
claimed_in_file: 27059
lattice_count: 27059  (2.40s)
expected: 27059 PASS
matches_claimed_in_file: True
exit=0
$ ./smclimb count ong_n15_published_27059.prefs 1
file: ong_n15_published_27059.prefs
n: 15
count: 27059
verify: 1
seconds: 0.0173
exit=0
$ python3 -I count_stable.py --knuth4 --brute --expect 10
n: 4
lattice_count: 10  (0.00s)
brute_count: 10  (0.00s)
counters_agree: True
expected: 10 PASS
exit=0
$ python3 -I count_stable.py --ident 15 --brute --expect 1
n: 15
lattice_count: 1  (0.00s)
brute_count: 1  (0.48s)
counters_agree: True
expected: 1 PASS
exit=0
```
I also wrote my own exhaustive counter, panel/scratch_criterion/tools/bf.c. It has its own parser and assigns women
in order, whereas the claimant's brute force assigns men. It prunes a partial matching only when two of its pairs
already form a blocking pair, and it re-checks every complete matching against the full definition. "swap" exchanges
the roles of men and women; "relabel S" applies a random relabelling of men and women from seed S. Output:
```
== instance_n15.prefs
mode=plain n=15 stable_matchings=27510 leaves=27510 leaves_failing_full_definition_check=0
mode=swap n=15 stable_matchings=27510 leaves=27510 leaves_failing_full_definition_check=0
mode=relabel n=15 stable_matchings=27510 leaves=27510 leaves_failing_full_definition_check=0
mode=relabel n=15 stable_matchings=27510 leaves=27510 leaves_failing_full_definition_check=0
== ong_n15_published_27059.prefs
mode=plain n=15 stable_matchings=27059 leaves=27059 leaves_failing_full_definition_check=0
mode=swap n=15 stable_matchings=27059 leaves=27059 leaves_failing_full_definition_check=0
mode=relabel n=15 stable_matchings=27059 leaves=27059 leaves_failing_full_definition_check=0
mode=relabel n=15 stable_matchings=27059 leaves=27059 leaves_failing_full_definition_check=0
```
Four exact counts agree on 27510:
- the claimant's Python lattice walk;
- the claimant's Python exhaustive enumeration;
- the claimant's C lattice walk, which re-checks every matching;
- my own C exhaustive enumeration.

The claimant's counters are their own code ("Written for V3R1T4S lane A"). Strictly, a lattice walk is not literally
"closed subsets of the rotation poset". R4 is met through the "exhaustive enumeration" branch, and the lattice walks
serve as the cross-check.

### R5: explicit preference lists. Met.
The claimed object is the file claim/instance_n15.prefs itself: 30 explicit lists.

## 3. Hunt for stretched definitions
- Ties: none (`ties_or_repeats: 0`).
- Incomplete lists: none. All 30 rows are permutations of 1..15.
- Non-square instance: no. There are 15 men's lists and 15 women's lists, and every row has length 15.
- Relabelling of the published instance: ruled out. Relabelling the men or women, or swapping their roles, does not
  change the number of stable matchings. My counter shows this directly: 27059 for the published instance and 27510
  for the claimed one, under role swap and two random relabellings. Since 27510 is not 27059, the claimed instance
  cannot be the published instance under any relabelling or role swap. In plain terms, the two files differ in
  `49 of 450` entries, in `[4, 5, 6, 8, 9, 10, 11, 12, 20, 22, 24, 25, 26, 27, 28]`: the lists of men
  4, 5, 6, 8, 9, 10, 11 and 12 and of women 5, 7, 9, 10, 11, 12 and 13.
- Reading the file a different way: CLAIM.md fixes the format as preference lists, best first. That is the same
  format as claim/ong_n15_published_27059.prefs, and I re-derived that file from the OEIS ranking tables myself. Both
  sides of the comparison are therefore read the same way.
- Counting unstable matchings: ruled out. My enumerator found
  `leaves_failing_full_definition_check=0`, and both lattice walks re-check every matching they visit (`verify: 1`;
  the Python walk asserts is_stable).
- Double counting: ruled out. An exhaustive enumerator reaches each bijection at most once (leaves = 27510 distinct
  bijections). The lattice walks remove duplicates with a visited set. All methods agree.
- Weak, strong or super-stability: these variants differ only when lists have ties or are incomplete. Neither
  applies here.
- Provenance (not a criterion issue): the comment line of claim/instance_n15.prefs records that the instance was
  found by local search starting from the published instance. The criterion does not restrict the method.

## 4. Null models
No null test is needed. The claim is not a statistical inference. It is the exact, deterministic count of one
explicit finite object, compared with a fixed number from a table, so there is no sampling and no chance agreement to
model. The risk worth controlling is a faulty counter or a faulty reading of the file. The controls above cover it:
- the published instance reproduces 27059, both from the .prefs file and from the OEIS ranking tables;
- Knuth's order-4 instance gives 10;
- identical lists give 1;
- the counts do not change under relabelling or role swap;
- two exhaustive enumerations written independently agree with two lattice walks.

## 5. Residual limits (these do not change the literal verdict)
- I checked "best known" against two things only: the bar the criterion itself fixes (27,059), and the status-source
  instance file. That file comes from a 2024-11-01 poster; the copy was fetched 2026-10-14. The package does not
  include the live A357271 data page or any later literature, and I did not check them (no web access, by
  instruction). Nothing in the package suggests a better order-15 instance exists. For this reason confirmed_scope is
  stated relative to the file and does not use the word "record".

## Verdict
The full criterion is met for the n = 15 cell; this is not a partial win. Every literal requirement, R1 to R5, holds.

confirmed_scope: The order-15 stable marriage instance in claim/instance_n15.prefs (sha256 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8; 15 men and 15 women with complete strict preference lists) has exactly 27510 stable matchings according to four agreeing exact counters, two of them exhaustive enumerations, which is strictly more than the 27059 of the order-15 instance given as lb(15)=27059 in the OEIS A357271 instance file claim/a357271_1.txt (sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47), the n = 15 bar named in the charter criterion.

pass: true
