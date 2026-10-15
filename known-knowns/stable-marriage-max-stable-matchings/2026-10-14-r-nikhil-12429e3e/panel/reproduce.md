# REPRODUCE skeptic verdict: claim/instance_n18.prefs has exactly 530528 stable matchings

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Paths are relative to the run folder, the folder that contains claim/. I read only claim/: CLAIM.md first, then
REPRODUCE.md, then the data files claim/instance_n18.prefs, claim/a357271_1.txt and claim/A357271.txt. I did not open
claim/count_stable.py or claim/smcount3.c until my own counters had produced their n = 18 results. After that I only
scanned them for unsafe calls before running the REPRODUCE.md commands. All work ran in a scratch copy,
panel/scratch_reproduce/claim (checked byte-identical to claim/ with cmp). My own code is in panel/scratch_reproduce/mine.
claim/ was not modified. Every program ran on one thread under `nice -n 15`. Tools: Python 3.9.6, Apple clang 21.0.0 (arm64).

## Definition (quoted verbatim from claim/CLAIM.md)

> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, MIT Press 1989, Sec. 1.1). The
> quantity is the number of stable matchings of the instance.

What is claimed: claim/instance_n18.prefs (18 men, 18 women, complete strict lists on both sides) has exactly 530528
stable matchings. That is more than the bar a(18) = 456300 from OEIS A357271 (saved as claim/A357271.txt).
claim/instance_n18.prefs has sha256 12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488.

## My own checkers (written from the definition before reading the author's code)

1. panel/scratch_reproduce/mine/smlat.py (Python, sha256 4ca328fd0c2833d63289c0d2198cf58d3dff34364b45c22924e8d33d9e83d928)
   - Parsers, written by me:
     - The .prefs format: '#' lines are comments, then 2n lines of n integers. Every list must be a permutation of 1..n.
     - The ranking tables in claim/a357271_1.txt: "a,b" in row i, column j means man i ranks woman j a-th and woman j
       ranks man i b-th, as the file explains. The parser also reads the MiniZinc arrays rankMen and rankWomen and checks
       that they agree with the tables.
   - is_stable is the definition itself. First it checks that the matching is a bijection. Then, for every man m and
     every woman w whom m ranks above his partner, it tests whether w ranks m above her partner (O(n^2)).
   - The count is a breadth-first lattice walk:
     - Start from the man-optimal matching M0 (Gale-Shapley with the men proposing).
     - In a matching M, s_M(m) is the first woman after M(m) on m's list who prefers m to her partner, and next_M(m) is
       that woman's partner. The exposed rotations are the cycles of next_M.
     - Eliminating a cycle moves each man m in it to s_M(m).
     - The visited set is keyed by the matching encoded as one integer (5 bits per man).
     - EVERY visited matching is re-checked with is_stable.
   - The walk also reports:
     - the number of sinks (matchings with no exposed rotation). This must be 1, and the sink must be the woman-optimal
       matching found by Gale-Shapley with the women proposing;
     - the number of distinct rotations seen anywhere in the lattice, and the length of one maximal chain M0 -> Mz;
     - the sha256 of the sorted list of all matchings found.
   - It also has a brute-force mode that checks all n! bijections with is_stable (small n only).
2. panel/scratch_reproduce/mine/smbt.c (C, sha256 70969f82c34560f5bb641aa7b03f4054ef44d1a778e541e99c57871674139e3c)
   This is exhaustive backtracking that uses no rotation theory at all.
   - Men are assigned in order. In mode `full`, each man may take any unused woman, so the search covers every
     bijection.
   - A branch is cut only when two pairs already assigned form a blocking pair. Such a pair stays blocking in every
     completion, so the cut is justified by the definition alone.
   - Every leaf is re-checked against the full definition (all n^2 pairs).
   - Mode `bounded` restricts each man to the women between his man-optimal and woman-optimal partners (Gale-Shapley).
   - The program can write out every stable matching it finds, so I can compare the full set of matchings with the
     Python walk, not just the count.

### Test results of my checkers (pasted program output)

Tiny instances written by hand and counted by hand:
- tiny2: Knuth's order-2 instance. By hand it has 2 stable matchings: everyone with their first choice, on the men's
  side or on the women's side.
- tiny2b: order 2, both men prefer w1 and both women prefer m1. By hand it has 1 stable matching, because m1 and w1 must
  be matched to each other.
- tiny3: the order-3 cyclic Latin square. By hand it has 3 stable matchings, and I checked all 6 bijections by hand.

```
== tiny2
brute_force_count: 2
parsed: n=2, preference lines=4, comment lines=1, all lists complete strict permutations: yes
count: 2
unstable: 0
sinks: 1
sink_is_Mz: True
M0: [1, 2]
Mz: [2, 1]
== tiny2b
brute_force_count: 1
parsed: n=2, preference lines=4, comment lines=1, all lists complete strict permutations: yes
count: 1
unstable: 0
sinks: 1
sink_is_Mz: True
M0: [1, 2]
Mz: [1, 2]
== tiny3
brute_force_count: 3
parsed: n=3, preference lines=6, comment lines=1, all lists complete strict permutations: yes
count: 3
unstable: 0
sinks: 1
sink_is_Mz: True
M0: [1, 2, 3]
Mz: [3, 1, 2]
```

Random instances (seed 20261015), lattice walk compared with brute force over all n! bijections:
```
random tests: 400 instances (n=1..7), brute force vs lattice walk mismatches: 0; max count seen 6
```

The published instances in claim/a357271_1.txt, read with my own parser (`python3 -I smlat.py oeis ../claim/a357271_1.txt .`):
```
order 7: expected 81, lattice_count 81, unstable 0, sinks 1, sink_is_Mz True, rotations 18, chain_len 18, minizinc_arrays_agree True, MATCH
order 9: expected 365, lattice_count 365, unstable 0, sinks 1, sink_is_Mz True, rotations 32, chain_len 32, minizinc_arrays_agree True, MATCH
order 11: expected 1690, lattice_count 1690, unstable 0, sinks 1, sink_is_Mz True, rotations 50, chain_len 50, minizinc_arrays_agree True, MATCH
order 13: expected 7123, lattice_count 7123, unstable 0, sinks 1, sink_is_Mz True, rotations 71, chain_len 71, minizinc_arrays_agree True, MATCH
order 15: expected 27059, lattice_count 27059, unstable 0, sinks 1, sink_is_Mz True, rotations 94, chain_len 94, minizinc_arrays_agree True, MATCH
```

The C backtracking (`./smbt FILE full`, then `./smbt FILE bounded`) on the same instances, which the Python parser
exported to .prefs files:
```
== tiny2
search_nodes: 5
leaf_recheck_failures: 0
stable_matchings: 2
candidate_pairs: 4
search_nodes: 5
leaf_recheck_failures: 0
stable_matchings: 2
== tiny2b
search_nodes: 4
leaf_recheck_failures: 0
stable_matchings: 1
candidate_pairs: 2
search_nodes: 3
leaf_recheck_failures: 0
stable_matchings: 1
== tiny3
search_nodes: 12
leaf_recheck_failures: 0
stable_matchings: 3
candidate_pairs: 9
search_nodes: 12
leaf_recheck_failures: 0
stable_matchings: 3
== oeis_n7
search_nodes: 598
leaf_recheck_failures: 0
stable_matchings: 81
candidate_pairs: 47
search_nodes: 597
leaf_recheck_failures: 0
stable_matchings: 81
== oeis_n9
search_nodes: 4378
leaf_recheck_failures: 0
stable_matchings: 365
candidate_pairs: 77
search_nodes: 4096
leaf_recheck_failures: 0
stable_matchings: 365
== oeis_n11
search_nodes: 29817
leaf_recheck_failures: 0
stable_matchings: 1690
candidate_pairs: 116
search_nodes: 27748
leaf_recheck_failures: 0
stable_matchings: 1690
== oeis_n13
search_nodes: 184992
leaf_recheck_failures: 0
stable_matchings: 7123
candidate_pairs: 164
search_nodes: 175233
leaf_recheck_failures: 0
stable_matchings: 7123
== oeis_n15
search_nodes: 1100301
leaf_recheck_failures: 0
stable_matchings: 27059
candidate_pairs: 218
search_nodes: 1004325
leaf_recheck_failures: 0
stable_matchings: 27059
```
All five published counts (81, 365, 1690, 7123, 27059) are reproduced by both of my methods.

## (3) Structure of claim/instance_n18.prefs

My Python parser (first line of the `count` output below) reports:
`parsed: n=18, preference lines=36, comment lines=1, all lists complete strict permutations: yes`.

The C parser applies the same validation and accepts the file. A separate awk check gives:
```
comment_lines=1 data_lines=36 lines_not_a_permutation_of_1..18=0
```
So the file is an order-18 instance: 18 men's lists and 18 women's lists, each a permutation of 1..18 (complete and strict).

## (4) My counters on claim/instance_n18.prefs

Python lattice walk, run 1 (`python3 -I smlat.py count ../claim/instance_n18.prefs py_run1_matchings.txt`, timed with the BSD time utility, option -l):
```
parsed: n=18, preference lines=36, comment lines=1, all lists complete strict permutations: yes
count: 530528
unstable: 0
sinks: 1
sink_is_Mz: True
Mz_visited: True
M0_stable: True
Mz_stable: True
distinct_rotations: 137
chain_len: 137
edges: 2862704
sha256_sorted_matchings: c597510f3dcbac427a822f736f34d7b4b76882c825ff757e78cab541d6852b50
M0: [1, 2, 5, 6, 3, 4, 9, 10, 13, 14, 11, 12, 7, 8, 15, 16, 17, 18]
Mz: [18, 17, 16, 15, 10, 9, 12, 11, 8, 7, 6, 5, 4, 3, 2, 1, 14, 13]
       35.85 real        24.77 user         0.30 sys
           175439872  maximum resident set size
```

C exhaustive backtracking over all bijections (mode full, pruned only by blocking pairs), run 1
(`./smbt ../claim/instance_n18.prefs full c_full_run1_matchings.txt`):
```
n: 18
mode: full
M0_stable: 1
Mz_stable: 1
candidate_pairs: 324
search_nodes: 22372619
leaf_recheck_failures: 0
stable_matchings: 530528
( nice -n 15 timeout 500 ./smbt ../claim/instance_n18.prefs full ; )  2.94s user 0.13s system 53% cpu 5.777 total
```

Comparing the two sets of matchings (each sorted with LC_ALL=C sort):
```
  530528 py_run1_matchings.txt
  530528 c_full_run1_matchings.txt
 1061056 total
63d02b6f423d3450aadaad6c74dcadd11f916c9e09f1b02107c5b8ee1f75516c  py1.sorted
63d02b6f423d3450aadaad6c74dcadd11f916c9e09f1b02107c5b8ee1f75516c  c1.sorted
SETS IDENTICAL (python lattice walk vs C exhaustive backtracking)
duplicate lines py:        0  c:        0
c597510f3dcbac427a822f736f34d7b4b76882c825ff757e78cab541d6852b50  py_run1_matchings.txt
```

The two methods are independent: one walks the rotation lattice, the other searches every bijection pruned only by the
definition. They find the same 530528 distinct matchings, and every one of them passes the definition check.
The exhaustive search needs no theory, so 530528 is the exact count by the definition alone.

## (7) Determinism (each of my counters run a second time)

```
== own python lattice walk, run 2
parsed: n=18, preference lines=36, comment lines=1, all lists complete strict permutations: yes
count: 530528
unstable: 0
sinks: 1
sink_is_Mz: True
Mz_visited: True
M0_stable: True
Mz_stable: True
distinct_rotations: 137
chain_len: 137
edges: 2862704
sha256_sorted_matchings: c597510f3dcbac427a822f736f34d7b4b76882c825ff757e78cab541d6852b50
M0: [1, 2, 5, 6, 3, 4, 9, 10, 13, 14, 11, 12, 7, 8, 15, 16, 17, 18]
Mz: [18, 17, 16, 15, 10, 9, 12, 11, 8, 7, 6, 5, 4, 3, 2, 1, 14, 13]
python run1 vs run2 dumps: identical
== own C exhaustive backtracking (full), run 2
n: 18
mode: full
M0_stable: 1
Mz_stable: 1
candidate_pairs: 324
search_nodes: 22372619
leaf_recheck_failures: 0
stable_matchings: 530528
C run1 vs run2 dumps: identical
== own C backtracking (bounded by Gale-Shapley partners)
n: 18
mode: bounded
M0_stable: 1
Mz_stable: 1
candidate_pairs: 308
search_nodes: 20631817
leaf_recheck_failures: 0
stable_matchings: 530528
```
The outputs are identical between runs, and so are the files of matchings written out (checked with cmp).

## (5) The author's commands from claim/REPRODUCE.md (run in the scratch copy of claim/)

```
$ cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n18.prefs 1
file: instance_n18.prefs
n: 18
rotations: 137
memo_states: 70214
count_poset: 530528
seconds_poset: 0.0196
count_lattice_verified: 530528
seconds_lattice: 1.3746
agree: yes
exit: 0
$ ./smcount3 enumerate instance_n18.prefs
count_poset: 530528
enumerated_ideals: 530528
unstable_matchings_found: 0
n: 18
rotations: 137
seconds_enumerate: 0.43
agree: yes
exit: 0
$ python3 -I count_stable.py --prefs instance_n18.prefs
n: 18
lattice_count: 530528  (54.38s)
exit: 0
$ grep -E '^%S|^%T|^%U' A357271.txt
%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,
%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,
%U A357271 127885440,262860800,384418176,2000043808
```
My own term-indexing check on claim/A357271.txt, which uses the offset from its %O line:
```
offset 1 ; a(18) = 456300 ; a(14) = 20176 ; 530528 > a(18): True
```
The author's three counters agree with my value: count_poset 530528, count_lattice_verified 530528, enumerated_ideals
530528 with unstable_matchings_found 0, and lattice_count 530528. They also agree with my structural numbers: 137
rotations, matching my distinct_rotations and chain_len.

## (6) sha256

```
$ shasum -a 256 instance_n18.prefs a357271_1.txt A357271.txt
12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488  instance_n18.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
--- stated hashes vs computed ---
instance_n18.prefs computed=12429e3eb7c67d315bddabe7ac71edc070cfbaae1760c67f66b8d2fa1e61b488 in_CLAIM.md=1 in_REPRODUCE.md=1
a357271_1.txt computed=95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47 in_CLAIM.md=0 in_REPRODUCE.md=1
A357271.txt computed=fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143 in_CLAIM.md=1 in_REPRODUCE.md=1
```
Every hash matches wherever it is stated. The hash of claim/a357271_1.txt is stated only in claim/REPRODUCE.md, and it
matches there. The files in claim/ and in the scratch copy hash the same.

## Mismatches

None in any claimed property or value.

Things noted that do not affect the claim:
- Timings in claim/REPRODUCE.md: `enumerate` says "about 10 s" and took 0.43 s; the Python lattice walk says
  "about 45 s" and took 54.38 s.
- claim/CLAIM.md says pruned brute force is feasible "up to about n = 15". My C version of that search finished
  n = 18 in about 3 s (22372619 search nodes).
- I checked the "best known" bar only against the saved files claim/A357271.txt and claim/a357271_1.txt, as
  instructed (no web access). The A357271 entry says the linked Ong et al. file improves only n = 7, 9, 11, 13, 15.
- The "origin" line in claim/CLAIM.md is marked as information only, and I did not check it.

## Verdict

- The definition is quoted above.
- The instance is a valid order-18 instance: 36 complete strict lists, 18 men and 18 women.
- My own checkers count exactly 530528 stable matchings, with every matching checked against the definition.
  The theory-free exhaustive search and the rotation-lattice walk find the same set of 530528 matchings.
- Both of my methods reproduce all five published counts.
- Re-runs are deterministic.
- The author's commands give the same value.
- All stated sha256 values match.
- 530528 > 456300 = a(18) in the saved claim/A357271.txt.

pass: true
