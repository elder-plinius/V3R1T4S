# Criterion skeptic verdict (V3R1T4S panel): cell n = 15, claimed 30362 stable matchings

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

What I looked at: only the claim package, meaning CLAIM.md, REPRODUCE.md, instance_n15.prefs, published_n15_27059.prefs,
a357271_1.txt, A357271.txt, count_stable.py and smcount3.c. Every command ran on a scratch copy of the claim folder,
on one thread under `nice -n 15`. I did not modify the claim folder, and I re-checked its sha256 values after the runs.
My own checker is `../panel/scratch_criterion/mycode/indep_check.py` (path relative to the claim folder). It shares no
code with the claim's counters. Toolchain: Python 3.9.6 and Apple clang 21.0.0. I used no web access.

## 1. The criterion, word by word (verbatim from CLAIM.md)

> for an n whose maximum is not known, give a stable-marriage instance (complete strict preference lists for n men
> and n women) with strictly more stable matchings than the best known instance of size n. Cells in order: n = 13
> (beat 7,123), n = 15 (beat 27,059), n = 14 (beat 20,176; no search has touched it), and n = 7 (beat 81) as a cheap
> calibration cell. Do not aim at n = 6, 8, 10, 12 or 16, which are conjectured exact.
> Shape: record (explicit preference lists; stable matchings counted exactly by your own enumerator: closed subsets
> of the rotation poset, or exhaustive enumeration, cross-checked).

Requirements I extracted from that text:
- R1. n must be a value whose maximum is not known. It must be a named cell and must not be 6, 8, 10, 12 or 16.
  The claimed cell is "n = 15 (beat 27,059)".
- R2. The claim must give one explicit instance with n men and n women and complete, strict preference lists. That
  means every list is a permutation of the other side, with no ties, no omissions, and equal numbers on both sides.
- R3. The bar is "the best known instance of size n". For this cell the criterion names it as 27,059, and the
  comparison instance must be the one the status source gives.
- R4. The instance must have "strictly more" stable matchings than the bar.
- R5. The count must be exact, made by the claimant's own enumerator (closed subsets of the rotation poset, or
  exhaustive enumeration), and cross-checked.
- R6. The claim covers one cell and must not borrow anything from other cells.

## 2. Requirement-by-requirement check

### R0. Identity of the checked files
```
$ shasum -a 256 instance_n15.prefs a357271_1.txt A357271.txt published_n15_27059.prefs
ed5147118033557c8331a5b2b9ec7b08ee67139ee00f417b951f58ac24983fef  instance_n15.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
586a5f5e7e4f124ebe57afe67273d5f5bba01f947f4ddd0397354f8fb001d600  published_n15_27059.prefs
```
The first three hashes equal the values stated in CLAIM.md (lines 9-10) and REPRODUCE.md.

### R1. n = 15 is an open, named cell: MET
The criterion lists "n = 15 (beat 27,059)" as a cell, and 15 is not one of the excluded orders 6, 8, 10, 12, 16.
Status source, A357271.txt as fetched:
```
6:%I A357271 #23 May 26 2025 15:56:20
11:%C A357271 a(n) is from Appendix C of Thurber's 2002 paper, using the maximum from each row. At the time of publication, the bounds were known to be exact up to n=4. A357269 shows that they are also exact for n=5. This sequence is not to be confused with A069156, also from Thurber's Appendix C, which uses only the first column, making for looser bounds for n > 11. a(6), a(8), a(10), a(12), and a(16) are also conjectured to be exact.
12:%C A357271 Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file.
```
The n = 15 value is therefore neither known exactly (exact only up to n = 5) nor conjectured exact.

### R2. An explicit order-15 instance with complete, strict, square lists: MET
Output of my strict parser, which works at byte level, splits on single spaces and rejects any non-numeric token:
```
[instance_n15.prefs] bytes=1189 sha256=ed5147118033557c8331a5b2b9ec7b08ee67139ee00f417b951f58ac24983fef
[instance_n15.prefs] non_ascii_bytes=0 CR=0 TAB=0
[instance_n15.prefs] total_lines=31 comment_line_numbers=[1] blank_lines=0 data_lines=30
[instance_n15.prefs] distinct_entries_per_data_line=[15]
[instance_n15.prefs] data lines that are permutations of 1..15: men lines 1-15: 15/15, women lines 16-30: 15/15
```
The file has 15 men's lists and 15 women's lists, and each is a permutation of 1..15. So the lists are complete (no
omissions), strict (no ties or repeats) and square (15 x 15). Line 1 is a `#` comment, which every parser ignores. The
claim's counters also reject non-permutations (count_stable.py line 215; `check_perms` in smcount3.c).

### R3. The bar 27059 is the status source's n = 15 value, and published_n15_27059.prefs is that instance: MET
Lines in the status source:
```
a357271_1.txt:15:lb(15)=27059 (previously 25011, or 26424 shown in A371810)
a357271_1.txt:184:/* Order 15 example with 27059 SM 
a357271_1.txt:201:n = 15;
```
The A357271 data line, as I parsed it (offset 1, per `%O A357271 1,2`):
```
number_of_terms: 28 offset 1 (per %O 1,2)
a(13)=6720 a(14)=20176 a(15)=25011
```
The status source contains three n = 15 values: 25011 (data line), 26424 (A371810, mentioned in the file) and 27059
(the linked file). The largest is 27059, which equals the bar the charter names.

I converted the order-15 paired ranking table myself. In that table, "a,b" in row i, column j means man i ranks woman j
in place a and woman j ranks man i in place b. I turned each table into most-preferred-first lists. Output:
```
header count in a357271_1.txt for order 15: 27059
own conversion == published_n15_27059.prefs (men lists): True
own conversion == published_n15_27059.prefs (women lists): True
paired table == MiniZinc rankMen block: True | paired table == MiniZinc rankWomen block: True
```
So published_n15_27059.prefs is the status source's instance, and it is internally consistent with the file's MiniZinc
blocks. Every method counts exactly 27059 stable matchings for it:
```
$ python3 -I count_stable.py --prefs published_n15_27059.prefs --brute --expect 27059
n: 15
lattice_count: 27059  (0.75s)
brute_count: 27059  (4.64s)
counters_agree: True
expected: 27059 PASS
exit code: 0
$ python3 -I count_stable.py --oeis a357271_1.txt --n 15 --expect 27059
minizinc_blocks_match_paired_table: True
n: 15
claimed_in_file: 27059
lattice_count: 27059  (0.83s)
expected: 27059 PASS
matches_claimed_in_file: True
exit code: 0
$ ./smcount3 count published_n15_27059.prefs 1
file: published_n15_27059.prefs
n: 15
rotations: 94
memo_states: 16515
count_poset: 27059
seconds_poset: 0.0041
count_lattice_verified: 27059
seconds_lattice: 0.0159
agree: yes
exit code: 0
$ ./smcount3 enumerate published_n15_27059.prefs
count_poset: 27059
enumerated_ideals: 27059
unstable_matchings_found: 0
n: 15
rotations: 94
seconds_enumerate: 0.01
agree: yes
exit code: 0
```
My own enumeration of the published instance gives the same number:
```
[published_n15_27059.prefs] own_enum_A(women-side, reverse order): listed=27059 distinct=27059 failing_definition_check=0; own_enum_B(men-side, shuffled order): listed=27059 distinct=27059 failing_definition_check=0; same_set_A_B=True; man_optimal_GS_in_set=True woman_optimal_GS_in_set=True man_opt_is_best_for_every_man=True woman_opt_is_worst_for_every_man=True (4.7s)
```

### R4. Strictly more stable matchings: MET
Output of my checker:
```
own count claimed instance: 30362; own count published instance: 27059; claimed > 27059: True; margin: 3303
```
30362 > 27059. This is a strict inequality with a margin of 3303.

### R5. Exact counts by the claimant's own enumerators, cross-checked: MET
These are the claim's counters, run with the commands in REPRODUCE.md:
```
$ python3 -I count_stable.py --prefs instance_n15.prefs --brute --expect 30362
n: 15
lattice_count: 30362  (1.02s)
brute_count: 30362  (5.23s)
counters_agree: True
expected: 30362 PASS
exit code: 0
$ cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n15.prefs 1
file: instance_n15.prefs
n: 15
rotations: 95
memo_states: 20999
count_poset: 30362
seconds_poset: 0.0032
count_lattice_verified: 30362
seconds_lattice: 0.0146
agree: yes
exit code: 0
$ ./smcount3 enumerate instance_n15.prefs
count_poset: 30362
enumerated_ideals: 30362
unstable_matchings_found: 0
n: 15
rotations: 95
seconds_enumerate: 0.01
agree: yes
exit code: 0
```
My own exhaustive enumeration shares no code with these. It runs in two different variable orders and prunes partial
assignments that contain two pairs forming a blocking pair. I re-checked every complete matching it produced against
the definition over all 225 (m, w) pairs, and I checked distinctness with a set:
```
[instance_n15.prefs] own_enum_A(women-side, reverse order): listed=30362 distinct=30362 failing_definition_check=0; own_enum_B(men-side, shuffled order): listed=30362 distinct=30362 failing_definition_check=0; same_set_A_B=True; man_optimal_GS_in_set=True woman_optimal_GS_in_set=True man_opt_is_best_for_every_man=True woman_opt_is_worst_for_every_man=True (4.8s)
```
Summary of the counts:

| method | instance_n15.prefs | published_n15_27059.prefs |
|---|---|---|
| count_stable.py lattice walk (visited set, every matching re-checked) | 30362 | 27059 |
| count_stable.py brute force (pairwise blocking-pair pruning) | 30362 | 27059 |
| smcount3 count_poset (closed subsets of the rotation poset, memoised DP) | 30362 | 27059 |
| smcount3 count_lattice_verified | 30362 | 27059 |
| smcount3 enumerate (reverse search over ideals, every matching re-checked) | 30362, 0 unstable | 27059, 0 unstable |
| my enumeration A (women side) | 30362 distinct, 0 failing | 27059 distinct, 0 failing |
| my enumeration B (men side, shuffled order; same set as A) | 30362 | 27059 |

The claim's five counts and my two enumerations agree on both instances.

### R6. One cell: MET
CLAIM.md says "cell: n = 15". It claims nothing for n = 13, 14 or 7 and uses nothing from those cells.

## 3. Hunt for hidden quantifiers and stretched definitions
- **"for an n".** This is existential, so one n is enough. Under the stricter reading, each listed cell is a separate
  enumerated target, and the claim is exactly one of them (n = 15). "Cells in order" orders the targets; it does not
  make the n = 15 cell depend on n = 13.
- **"strictly".** The comparison is strict, not ">=": 30362 against 27059.
- **"best known".** This depends on time. The package's status source is OEIS revision #23 of 26 May 2025, fetched
  2026-10-14. Its largest n = 15 value is 27059, which is the bar the charter names. I had no web access, so I cannot
  rule out a larger value published outside the package. The cell names its bar explicitly as 27,059, so I note this
  limit but do not count it against the claim.
- **Ties, incomplete lists, non-square instances.** R2 rules these out: all 30 lines are permutations of 1..15.
- **A relabelling of the published instance.** Renaming men, renaming women or swapping the two sides does not change
  the number of stable matchings, so any relabelling would count 27059. This instance counts 30362, so it is not one.
  My checker's output: `lists differing: men 11/15, women 9/15; list positions differing: 132/450`.
- **Counting unstable matchings.** I re-checked every counted matching against the definition:
  `failing_definition_check=0` (my checker) and `unstable_matchings_found: 0` (smcount3 enumerate). count_stable.py
  asserts that every visited matching is stable.
- **Double counting.** My enumeration printed `listed=30362 distinct=30362`, and two variable orders gave the same set
  (`same_set_A_B=True`). The lattice walks de-duplicate with a visited set, and the reverse search runs over distinct
  ideals and equals the DP count.
- **Reading convention.** CLAIM.md fixes it: lines 1-15 are the men's lists, most preferred first. The same convention
  applied to the published table reproduces that table's stated 27059 (R3), so the claim and the bar are counted the
  same way. Swapping the sides would not change either count.
- **Stability notion.** The textbook one (no blocking pair), checked directly. With strict, complete lists, the
  distinctions between weak, strong and super-stability do not arise.

## 4. Null models
**No null test is needed.** The claim is the exact number of stable matchings of one explicit, finite object. That
number was computed by deterministic exact methods (exhaustive enumeration and counting ideals of the rotation poset)
and compared with a fixed table value. There is no sampling, no estimate and no chance outcome for a null model to
explain. Randomness only entered the search that found the object, and that search ("origin") is not part of the claim.

**Controls run instead.**
- The baseline published instance counts exactly 27059 (R3), so the counters do not push it past the bar.
- Every published instance in a357271_1.txt reproduces its stated count with both the claim's counters and mine.
- Known small instances give their known values.

```
$ python3 -I count_stable.py --knuth4 --brute --expect 10
n: 4
lattice_count: 10  (0.00s)
brute_count: 10  (0.00s)
counters_agree: True
expected: 10 PASS
$ python3 -I count_stable.py --ident 8 --brute --expect 1
n: 8
lattice_count: 1  (0.00s)
brute_count: 1  (0.00s)
counters_agree: True
expected: 1 PASS
$ python3 -I count_stable.py --random 9 SEED --brute      (SEED = 1, 2, 3)
n: 9 lattice_count: 4  (0.00s) brute_count: 4  (0.00s) counters_agree: True
n: 9 lattice_count: 3  (0.00s) brute_count: 3  (0.00s) counters_agree: True
n: 9 lattice_count: 3  (0.00s) brute_count: 3  (0.00s) counters_agree: True
$ python3 -I count_stable.py --oeis a357271_1.txt --n K --brute      (K = 7, 9, 11, 13)
minizinc_blocks_match_paired_table: True n: 7 claimed_in_file: 81 lattice_count: 81  (0.00s) brute_count: 81  (0.00s) counters_agree: True matches_claimed_in_file: True
minizinc_blocks_match_paired_table: True n: 9 claimed_in_file: 365 lattice_count: 365  (0.01s) brute_count: 365  (0.01s) counters_agree: True matches_claimed_in_file: True
minizinc_blocks_match_paired_table: True n: 11 claimed_in_file: 1690 lattice_count: 1690  (0.04s) brute_count: 1690  (0.10s) counters_agree: True matches_claimed_in_file: True
minizinc_blocks_match_paired_table: True n: 13 claimed_in_file: 7123 lattice_count: 7123  (0.19s) brute_count: 7123  (1.01s) counters_agree: True matches_claimed_in_file: True
```
My own enumerator on every instance in a357271_1.txt:
```
   order 7: header says 81, own enumerator 81, equal=True; MiniZinc blocks agree with paired table: True
   order 9: header says 365, own enumerator 365, equal=True; MiniZinc blocks agree with paired table: True
   order 11: header says 1690, own enumerator 1690, equal=True; MiniZinc blocks agree with paired table: True
   order 13: header says 7123, own enumerator 7123, equal=True; MiniZinc blocks agree with paired table: True
   order 15: header says 27059, own enumerator 27059, equal=True; MiniZinc blocks agree with paired table: True
```

## 5. Decision
Every requirement of the criterion is literally met for the named cell n = 15:
- the instance is explicit, with complete, strict lists for 15 men and 15 women;
- its count of 30362 is exact and cross-checked by five claim counts and two independent enumerations of mine;
- 30362 is strictly greater than the bar of 27059, which is the status source's n = 15 value and the exact count of
  the published instance.

The object is not a relabelling of the published instance, and it beats every n = 15 value in the status source. This
is a genuine win in this one cell, not subsumed by anything in the package. No other cell is claimed or assessed.

confirmed_scope: The order-15 instance in instance_n15.prefs (sha256 ed5147118033557c8331a5b2b9ec7b08ee67139ee00f417b951f58ac24983fef; 15 men and 15 women, every list a permutation of 1..15) has exactly 30362 stable matchings, by the agreeing exact counts of the claim's five counters and the panel's own exhaustive enumeration with every matching re-checked against the definition, which is strictly more than the 27059 of the published order-15 instance in a357271_1.txt that the charter names as the bar for the n = 15 cell.
pass: true
