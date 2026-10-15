# REPRODUCE skeptic verdict: claim/instance_n13.prefs has exactly 7698 stable matchings (n = 13, bar 7123)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Inputs read: claim/CLAIM.md, claim/REPRODUCE.md and the data files claim/instance_n13.prefs, claim/published_n13_7123.prefs, claim/a357271_1.txt, claim/A357271.txt. All work was done in a scratch copy (panel/scratch_reproduce/claim/); my own code is in panel/scratch_reproduce/mine/. I wrote and ran my parser and counters (steps 1-4 and 7) BEFORE opening or running claim/count_stable.py or claim/smcount3.c. Before running the author's code, I only grepped it for risky calls (none). Single thread, `nice -n 15`.

## 1. Definition (quoted verbatim from claim/CLAIM.md)
> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, MIT Press 1989, Sec. 1.1). The
> quantity is the number of stable matchings of the instance.

## 2. My own checker (written from the definition only)
- panel/scratch_reproduce/mine/myparse.py: my own strict parser.
  - .prefs files: ASCII only, no CR, '#' comment lines skipped, no blank data lines, exactly 2n data lines of n integers, every line a permutation of 1..n.
  - claim/a357271_1.txt: uses the file's stated format ("the '1,5' in row 3, column 4 means that Man 3 ranks Woman 4 as his 1st choice, and she ranks him as her 5th choice"). Reads every "order K example with X SM" ranking table and checks that ranks form permutations per man (row) and per woman (column). Converts ranks to preference lists. Independently parses the MiniZinc blocks (rankWomen[woman][man], rankMen[man][woman]) and cross-checks them against the table.
- panel/scratch_reproduce/mine/mycount.c (C): exhaustive backtracking over all bijections, assigning man 1..n in turn to an unused woman.
  - A partial assignment is cut only if a blocking pair exists between two already-assigned people. Both of their partners are fixed, so that pair blocks every completion: the pruning is sound and the search is exhaustive.
  - Every complete bijection reached is re-checked by def_check(), a separate literal implementation of the definition. It scans the raw preference lists (for each man, every woman he lists before his partner; does she list him before her partner?) and does not use the rank tables used for pruning.
  - Mode `all` turns pruning off and visits all n! bijections.
- panel/scratch_reproduce/mine/mycheck2.py (Python): a second independent implementation.
  - It assigns WOMEN in turn, tries men in her preference order, and prunes the same way. It then checks every complete bijection with a literal definition test (`list.index` comparisons over all n^2 pairs).
  - It also re-verifies against the definition every matching listed by the C program and compares the two SETS of matchings.

### Tests on tiny instances verified by hand
- hand_n2: m1: w1>w2, m2: w2>w1; w1: m2>m1, w2: m1>m2. By hand, both matchings are stable (in one, both men have their 1st choice; in the other, both women do): 2.
- hand_n3_cyclic: men m1: 1 2 3, m2: 2 3 1, m3: 3 1 2; women w1: 2 3 1, w2: 3 1 2, w3: 1 2 3. By hand there are 3 stable matchings: (1,2,3), (2,3,1), (3,1,2) (wife of m1,m2,m3). Each of the 3 transposition matchings has a blocking pair, e.g. (m3,w1) for (1,3,2).
- hand_n3_identical: all men list 1 2 3 and all women list 1 2 3. By hand the unique stable matching is (1,2,3).

Output:
```
file=inst/hand_n2.txt n=2 mode=prune nodes=5 complete_bijections_checked=2 stable_matchings=2 complete_bijections_failing_definition=0
file=inst/hand_n2.txt n=2 mode=all nodes=5 complete_bijections_checked=2 stable_matchings=2 complete_bijections_failing_definition=0
  stable matchings listed (wife of man1..n): 1 2 / 2 1
file=inst/hand_n3_cyclic.txt n=3 mode=prune nodes=12 complete_bijections_checked=3 stable_matchings=3 complete_bijections_failing_definition=0
file=inst/hand_n3_cyclic.txt n=3 mode=all nodes=16 complete_bijections_checked=6 stable_matchings=3 complete_bijections_failing_definition=3
  stable matchings listed (wife of man1..n): 1 2 3 / 2 3 1 / 3 1 2
file=inst/hand_n3_identical.txt n=3 mode=prune nodes=8 complete_bijections_checked=1 stable_matchings=1 complete_bijections_failing_definition=0
file=inst/hand_n3_identical.txt n=3 mode=all nodes=16 complete_bijections_checked=6 stable_matchings=1 complete_bijections_failing_definition=5
  stable matchings listed (wife of man1..n): 1 2 3
(python, women order) hand_n2: 2; hand_n3_cyclic: 3; hand_n3_identical: 1; sets equal to the C lists: True (all three)
```
All match the hand counts and the hand-derived matchings.

### Tests on the published instances inside claim/a357271_1.txt (my own parser)
```
header lb values: {7: 81, 9: 365, 11: 1690, 13: 7123, 15: 27059}
block header counts: {7: 81, 9: 365, 11: 1690, 13: 7123, 15: 27059}
ranking tables found for n = [7, 9, 11, 13, 15] ; MiniZinc blocks found for n = [7, 9, 11, 13, 15]
n=7: table 7x7 pairs, ranks valid permutations, MiniZinc block vs table: identical, header count 81, lb 81 -> inst/oeis_n7.txt
n=9: table 9x9 pairs, ranks valid permutations, MiniZinc block vs table: identical, header count 365, lb 365 -> inst/oeis_n9.txt
n=11: table 11x11 pairs, ranks valid permutations, MiniZinc block vs table: identical, header count 1690, lb 1690 -> inst/oeis_n11.txt
n=13: table 13x13 pairs, ranks valid permutations, MiniZinc block vs table: identical, header count 7123, lb 7123 -> inst/oeis_n13.txt
n=15: table 15x15 pairs, ranks valid permutations, MiniZinc block vs table: identical, header count 27059, lb 27059 -> inst/oeis_n15.txt
parsed ../claim/published_n13_7123.prefs: n=13, comment_lines=1, data_lines=26, all 26 lists are permutations of 1..13
published_n13_7123.prefs == my conversion of OEIS order-13 ranking table: IDENTICAL
```
My C counter (pruned):
```
file=inst/oeis_n7.txt n=7 mode=prune nodes=598 complete_bijections_checked=81 stable_matchings=81 complete_bijections_failing_definition=0
file=inst/oeis_n9.txt n=9 mode=prune nodes=4378 complete_bijections_checked=365 stable_matchings=365 complete_bijections_failing_definition=0
file=inst/oeis_n11.txt n=11 mode=prune nodes=29817 complete_bijections_checked=1690 stable_matchings=1690 complete_bijections_failing_definition=0
file=inst/oeis_n13.txt n=13 mode=prune nodes=184992 complete_bijections_checked=7123 stable_matchings=7123 complete_bijections_failing_definition=0
file=inst/oeis_n15.txt n=15 mode=prune nodes=1100301 complete_bijections_checked=27059 stable_matchings=27059 complete_bijections_failing_definition=0
```
My C counter, NO pruning (all n! bijections, each checked against the definition):
```
file=inst/oeis_n7.txt n=7 mode=all nodes=13700 complete_bijections_checked=5040 stable_matchings=81 complete_bijections_failing_definition=4959
  n=7: set of stable matchings from unpruned all-n! enumeration IDENTICAL to pruned search
file=inst/oeis_n9.txt n=9 mode=all nodes=986410 complete_bijections_checked=362880 stable_matchings=365 complete_bijections_failing_definition=362515
  n=9: set of stable matchings from unpruned all-n! enumeration IDENTICAL to pruned search
file=inst/oeis_n11.txt n=11 mode=all nodes=108505112 complete_bijections_checked=39916800 stable_matchings=1690 complete_bijections_failing_definition=39915110
  n=11: set of stable matchings from unpruned all-n! enumeration IDENTICAL to pruned search
```
My Python counter (women order):
```
file=inst/oeis_n7.txt n=7 python_women_order: nodes=572 complete_bijections=81 stable_matchings=81 distinct=81
listed matchings in inst/oeis_n7.prune.out: 81, distinct 81, each re-checked against definition: 81 stable, 0 not; set equal to python enumeration: True
file=inst/oeis_n9.txt n=9 python_women_order: nodes=3823 complete_bijections=365 stable_matchings=365 distinct=365
listed matchings in inst/oeis_n9.prune.out: 365, distinct 365, each re-checked against definition: 365 stable, 0 not; set equal to python enumeration: True
file=inst/oeis_n11.txt n=11 python_women_order: nodes=23439 complete_bijections=1690 stable_matchings=1690 distinct=1690
listed matchings in inst/oeis_n11.prune.out: 1690, distinct 1690, each re-checked against definition: 1690 stable, 0 not; set equal to python enumeration: True
file=inst/oeis_n13.txt n=13 python_women_order: nodes=129672 complete_bijections=7123 stable_matchings=7123 distinct=7123
listed matchings in inst/oeis_n13.prune.out: 7123, distinct 7123, each re-checked against definition: 7123 stable, 0 not; set equal to python enumeration: True
```
All five published counts (81, 365, 1690, 7123, 27059) are reproduced exactly. The bar 7123 is therefore confirmed by my own counters on the instance parsed straight from the status source's file.

## 3. The claimed object: claim/instance_n13.prefs (my own parser)
```
parsed ../claim/instance_n13.prefs: n=13, comment_lines=1, data_lines=26, all 26 lists are permutations of 1..13
```
The file is ASCII only, with no CR and no blank lines. It has 1 comment line followed by exactly 26 lines of 13 integers. Each line is a permutation of 1..13. So this is an order-13 instance with 26 complete strict preference lists (13 men, 13 women). Compared with the published 7123 instance, 14 of the 26 lists differ (men 1, 3, 5, 7, 8, 9, 11, 13; women 1, 2, 4, 6, 8, 10).

## 4. My counters on the claimed instance (steps 4 and 7: two runs of the C counter)
```
file=inst/claimed_n13.txt n=13 mode=prune nodes=187429 complete_bijections_checked=7698 stable_matchings=7698 complete_bijections_failing_definition=0
real 0.11
file=inst/claimed_n13.txt n=13 mode=prune nodes=187429 complete_bijections_checked=7698 stable_matchings=7698 complete_bijections_failing_definition=0
real 0.10
run1 and run2 outputs byte-identical
567b44338073a26e025f9682af6abcc125ea5b85fb65ae0701299760dbd78d09  inst/claimed_n13.run1.out
567b44338073a26e025f9682af6abcc125ea5b85fb65ae0701299760dbd78d09  inst/claimed_n13.run2.out
    7698 inst/claimed_n13.run1.out
    7698            (distinct lines)
file=inst/claimed_n13.txt n=13 python_women_order: nodes=134040 complete_bijections=7698 stable_matchings=7698 distinct=7698
listed matchings in inst/claimed_n13.run1.out: 7698, distinct 7698, each re-checked against definition: 7698 stable, 0 not; set equal to python enumeration: True
```
Two independent exhaustive implementations (C, men assigned in turn; Python, women assigned in turn) give the same set of exactly 7698 stable matchings. Every one of them passes the literal definition check, and every complete bijection reached passes it too. My count is deterministic: the two runs are byte-identical.

## 5. The author's commands from claim/REPRODUCE.md (run afterwards in the scratch copy)
```
$ python3 -I count_stable.py --prefs instance_n13.prefs --brute --expect 7698
n: 13
lattice_count: 7698  (0.32s)
brute_count: 7698  (1.08s)
counters_agree: True
expected: 7698 PASS
exit code: 0
$ cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n13.prefs 1
file: instance_n13.prefs
n: 13
rotations: 72
memo_states: 8373
count_poset: 7698
seconds_poset: 0.0009
count_lattice_verified: 7698
seconds_lattice: 0.0019
agree: yes
exit code: 0
$ ./smcount3 enumerate instance_n13.prefs
count_poset: 7698
enumerated_ideals: 7698
unstable_matchings_found: 0
n: 13
rotations: 72
seconds_enumerate: 0.00
agree: yes
exit code: 0
$ python3 -I count_stable.py --prefs published_n13_7123.prefs --brute --expect 7123
n: 13
lattice_count: 7123  (0.27s)
brute_count: 7123  (1.03s)
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
```
A second run of the first command printed the same lattice_count 7698, brute_count 7698, counters_agree True and expected 7698 PASS. In claim/count_stable.py, `random` is used only by an optional seeded `--random` test-instance mode, not by these commands. Every printed value matches the expected values stated in claim/REPRODUCE.md.

## 6. sha256
```
$ shasum -a 256 instance_n13.prefs a357271_1.txt A357271.txt      (scratch copy, and identical for the originals in claim/)
ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69  instance_n13.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```
- instance_n13.prefs matches the object sha256 in claim/CLAIM.md and claim/REPRODUCE.md.
- a357271_1.txt matches the bar-source sha256 in claim/CLAIM.md and claim/REPRODUCE.md.
- A357271.txt matches claim/REPRODUCE.md.

The status source as saved (claim/A357271.txt) gives a(13) = 6720 in the data line. Its comment points to the linked file, whose header states "lb(13)=7123 (previously 6720)". This agrees with the bar of 7123 in claim/CLAIM.md.

## Mismatches and caveats
- No mismatch on any number, property or hash.
- Not done: the unpruned all-13! (6.2e9 bijections) run on the claimed instance, which would take about 10 minutes at 1 thread. The pruned search is exhaustive by the soundness argument above. Its unpruned counterpart produced identical sets at n = 7, 9 and 11.
- Out of scope: whether a value above 7123 for n = 13 exists anywhere outside the saved status source. That is a status question for another panel member, not a reproduction mismatch.

Verdict: properties confirmed with my own checker.
- Order 13: 13 men and 13 women.
- 26 complete strict lists.
- Exactly 7698 stable matchings, by two independent exhaustive counters with identical sets, and deterministic.
- 7698 > 7123, the bar I re-counted from the status source's own file.
- The author's commands reproduce, and the hashes match.

pass: true
