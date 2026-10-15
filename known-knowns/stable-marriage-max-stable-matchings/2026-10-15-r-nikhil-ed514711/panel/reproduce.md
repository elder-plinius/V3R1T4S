# REPRODUCE skeptic verdict: claim/instance_n15.prefs (order 15, claimed 30362 stable matchings)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Scope and order of work. I read claim/CLAIM.md, then claim/REPRODUCE.md, then the data files only
(claim/instance_n15.prefs, claim/a357271_1.txt, claim/A357271.txt, claim/published_n15_27059.prefs). I wrote and ran my own
counters, including on claim/instance_n15.prefs, BEFORE opening claim/count_stable.py or claim/smcount3.c. I looked at
those two files only afterwards, with a safety grep before running them. All work ran in a scratch copy
(panel/scratch_reproduce/claim; the sha256 of all 8 files equals the original claim/). claim/ was not modified. Paths here
are relative to the run folder. My scripts are in panel/scratch_reproduce/mine/.
Limits: 1 thread, and every long job ran under `nice -n 15`.

## Definition (quoted verbatim from claim/CLAIM.md, section "Definition")
> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, MIT Press 1989, Sec. 1.1). The
> quantity is the number of stable matchings of the instance.

## My checker (written from the definition alone)
- Stability test (`full_check` in smc_mine.c, `is_stable` in mine.py) is a literal transcription of the definition. It
  loops over all n*n pairs (m, w) with w != wife(m) and rejects if rank_m(w) < rank_m(wife(m)) AND
  rank_w(m) < rank_w(husband(w)). It also checks that the matching is a bijection.
- `smc_mine brute FILE`: enumerates ALL n! bijections and tests each one with full_check. No pruning.
- `smc_mine bt FILE`: backtracking over men 1..n. It prunes a partial matching only when a pair (m, w) of two ALREADY
  matched agents is blocking. That is sound because both partners in such a pair are fixed, so the pair blocks in
  every completion and no stable matching can be lost. Every complete matching is re-checked with full_check before
  it is counted (`leaves_rejected_by_full_check`). The search is exhaustive, not a sample. It can dump every stable
  matching (wives of men 1..n).
- `mine.py count FILE`: a separately written Python counter that backtracks over WOMEN instead (a different variable
  order, so the pruning differs). It re-checks every complete matching with is_stable and prints the sha256 of the
  sorted set of matchings, so the two counters' SETS, not just their counts, can be compared. With `brute` it also runs
  a pure itertools.permutations brute force (tiny n only).
- Parsers (mine.py, structure.py):
  - .prefs: skip '#' lines, then require exactly 2n lines of n integers, each a permutation of 1..n (complete, strict).
  - claim/a357271_1.txt: read the ranking tables using the file's own explanation: row i, column j "a,b" = man i's
    rank of woman j, and woman j's rank of man i. Each table is validated as permutations, cross-checked against the
    file's MiniZinc rankWomen/rankMen blocks, and converted to preference lists.
  - The expected counts are taken from each table header ("order N example with K SM").
- recheck.py: re-reads the C dump and re-checks every listed matching with is_stable: perfect, distinct, stable.

## Test results of my checker (real output, panel/scratch_reproduce/mine/out/run_all.log)
Hand-verified tiny instances. I derived these by hand before running:
- t2a (m1: w1 w2, m2: w2 w1; w1: m2 m1, w2: m1 m2) has 2 stable matchings.
- t2b (all lists 1 2) has 1.
- t3 (cyclic: men i -> w_i, w_i+1, w_i+2; w1: m2 m3 m1, w2: m3 m1 m2, w3: m1 m2 m3) has exactly 3, with wives
  (1,2,3), (2,3,1), (3,1,2); the other 3 permutations each have a blocking pair.
```
## A. hand-verified tiny instances (expected by hand: t2a=2, t2b=1, t3=3)
-- t2a: C brute: 2  C bt: 2  matchings: 1 2;2 1;
women_first_backtrack_count: 2  distinct: 2  nodes: 5  leaf_rejected: 0
pure_bruteforce_count: 2  same_set: True
-- t2b: C brute: 1  C bt: 1  matchings: 1 2;
women_first_backtrack_count: 1  distinct: 1  nodes: 4  leaf_rejected: 0
pure_bruteforce_count: 1  same_set: True
-- t3: C brute: 3  C bt: 3  matchings: 1 2 3;2 3 1;3 1 2;
women_first_backtrack_count: 3  distinct: 3  nodes: 12  leaf_rejected: 0
pure_bruteforce_count: 3  same_set: True
## B. random instances n=3..8 (12 each): pure brute force vs C bt vs Python women-first (count + exact set)
random instances: 72  mismatches: 0
```
Published instances, parsed by my own parser from claim/a357271_1.txt. Expected counts stated in the file: 81, 365,
1690, 7123, 27059.
```
order 7: stated 81 SM, minizinc_block_agrees_with_table: True, written mine/out/oeis_n7.prefs
order 9: stated 365 SM, minizinc_block_agrees_with_table: True, written mine/out/oeis_n9.prefs
order 11: stated 1690 SM, minizinc_block_agrees_with_table: True, written mine/out/oeis_n11.prefs
order 13: stated 7123 SM, minizinc_block_agrees_with_table: True, written mine/out/oeis_n13.prefs
order 15: stated 27059 SM, minizinc_block_agrees_with_table: True, written mine/out/oeis_n15.prefs
-- order 7 pure brute force (all n! bijections, no pruning):
stable_matchings: 81 leaves_checked: 5040 digest_xor: 44ef21d1c18ed671
-- order 9 pure brute force (all n! bijections, no pruning):
stable_matchings: 365 leaves_checked: 362880 digest_xor: 4ccb4c5a7993f25c
-- order 11 pure brute force (all n! bijections, no pruning):
stable_matchings: 1690 leaves_checked: 39916800 digest_xor: 6b83907cee5519be
-- order 7 C bt:
stable_matchings: 81 leaves_rejected_by_full_check: 0 search_nodes: 598 digest_xor: 44ef21d1c18ed671
   C bt sorted-set sha256: 6dc9b0cf8390380b55f2e300dd019215fbe4618ee3a083ff6417380f13392e01
-- order 7 Python women-first:
women_first_backtrack_count: 81  distinct: 81  nodes: 572  leaf_rejected: 0
sorted_matchings_sha256: 6dc9b0cf8390380b55f2e300dd019215fbe4618ee3a083ff6417380f13392e01
-- order 9 C bt:
stable_matchings: 365 leaves_rejected_by_full_check: 0 search_nodes: 4378 digest_xor: 4ccb4c5a7993f25c
   C bt sorted-set sha256: 5cc8e8a46dbec8027e9676454a0b42cc49c699c200362ddfa97d518c672f0f37
-- order 9 Python women-first:
women_first_backtrack_count: 365  distinct: 365  nodes: 3823  leaf_rejected: 0
sorted_matchings_sha256: 5cc8e8a46dbec8027e9676454a0b42cc49c699c200362ddfa97d518c672f0f37
-- order 11 C bt:
stable_matchings: 1690 leaves_rejected_by_full_check: 0 search_nodes: 29817 digest_xor: 6b83907cee5519be
   C bt sorted-set sha256: 90ffff09f5a42702a419c0251d11c49e262c593282290e721978f75291ff1bca
-- order 11 Python women-first:
women_first_backtrack_count: 1690  distinct: 1690  nodes: 23439  leaf_rejected: 0
sorted_matchings_sha256: 90ffff09f5a42702a419c0251d11c49e262c593282290e721978f75291ff1bca
-- order 13 C bt:
stable_matchings: 7123 leaves_rejected_by_full_check: 0 search_nodes: 184992 digest_xor: 81d3b5a39622eda8
   C bt sorted-set sha256: 22a9f449f5300f118b2f017e8231bbff2c30935098dd7759dcd7ec67dfd84a50
-- order 13 Python women-first:
women_first_backtrack_count: 7123  distinct: 7123  nodes: 129672  leaf_rejected: 0
sorted_matchings_sha256: 22a9f449f5300f118b2f017e8231bbff2c30935098dd7759dcd7ec67dfd84a50
-- order 15 C bt:
stable_matchings: 27059 leaves_rejected_by_full_check: 0 search_nodes: 1100301 digest_xor: 78cfdfdd78ffc831
   C bt sorted-set sha256: eab5b975806f9442ad456e4d60959e00741edc8da460810130bbb133adbe0265
-- order 15 Python women-first:
women_first_backtrack_count: 27059  distinct: 27059  nodes: 707859  leaf_rejected: 0
sorted_matchings_sha256: eab5b975806f9442ad456e4d60959e00741edc8da460810130bbb133adbe0265
-- my order-15 conversion vs claim/published_n15_27059.prefs (data lines):
   identical
```
Result: all five published counts reproduce exactly (81, 365, 1690, 7123, 27059). Orders 7, 9 and 11 also reproduce
by pure brute force with no pruning, giving the same set digest as backtracking. For every order, the two counters
(different variable orders) return byte-identical sorted sets of matchings. My own conversion of the published
order-15 table has the same data lines as claim/published_n15_27059.prefs.

## The claimed object: claim/instance_n15.prefs
Structure, parsed by my own code:
```
bytes: 1189  non-ascii bytes: 0  CR bytes: 0  tabs: 0
total lines: 31  comment lines: 1  blank lines: 0  data lines: 30
comment lines all precede data: True
n = 15  lengths: [15]
men lists (lines 1-15) are permutations of 1..15 (complete, strict, no ties): True
women lists (lines 16-30) are permutations of 1..15 (complete, strict, no ties): True
ORDER_15_30_COMPLETE_STRICT_LISTS: True
```
My counters on it (run 3, from run_all.log; runs 1 and 2 printed the same numbers):
```
file: claim/instance_n15.prefs
n: 15
mode: bt
stable_matchings: 30362
leaves_checked: 30362
leaves_rejected_by_full_check: 0
search_nodes: 1092373
digest_xor: c1b2ba9e7d889730
digest_sum: b07ba0a50073a392
C bt dump: lines 30362  distinct 30362  sorted-set sha256 ee1890cbea8789cdc1743b5a802bd29590bed6da819976144f4a21f9d1facdbd
file: claim/instance_n15.prefs
n: 15  men lists: 15  women lists: 15  all strict complete: True
women_first_backtrack_count: 30362  distinct: 30362  nodes: 749350  leaf_rejected: 0
sorted_matchings_sha256: ee1890cbea8789cdc1743b5a802bd29590bed6da819976144f4a21f9d1facdbd
-- independent re-check of every matching in the C dump against the definition:
dump lines: 30362  distinct: 30362  all perfect matchings: True  stable per definition: 30362  exceeds 27059: True
C dump run 2 vs run 3: byte-identical
```
My exact, exhaustive count is 30362, which equals the claimed 30362. The two counters, with different search orders,
find the same set of 30362 distinct stable matchings. 30362 > 27059.

## Author's commands (claim/REPRODUCE.md), run after my own count, in the scratch copy, each prefixed with `nice -n 15`
```
$ python3 -I count_stable.py --prefs instance_n15.prefs --brute --expect 30362
n: 15
lattice_count: 30362  (1.26s)
brute_count: 30362  (6.37s)
counters_agree: True
expected: 30362 PASS
exit code: 0

$ cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n15.prefs 1
file: instance_n15.prefs
n: 15
rotations: 95
memo_states: 20999
count_poset: 30362
seconds_poset: 0.0048
count_lattice_verified: 30362
seconds_lattice: 0.0165
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

$ python3 -I count_stable.py --prefs published_n15_27059.prefs --brute --expect 27059
n: 15
lattice_count: 27059  (1.57s)
brute_count: 27059  (7.34s)
counters_agree: True
expected: 27059 PASS
exit code: 0

$ python3 -I count_stable.py --oeis a357271_1.txt --n 15 --expect 27059
minizinc_blocks_match_paired_table: True
n: 15
claimed_in_file: 27059
lattice_count: 27059  (1.06s)
expected: 27059 PASS
matches_claimed_in_file: True
exit code: 0
```
Every printed value matches what claim/REPRODUCE.md says it prints. Their randomness (`--random`, `climb`, `anneal`) is
not used by any of these commands. A second run of `./smcount3 count instance_n15.prefs 1` and
`./smcount3 enumerate instance_n15.prefs` printed the same counts again (30362 / 30362 / agree: yes; 30362 ideals,
0 unstable).

## sha256 (stated in claim/CLAIM.md and claim/REPRODUCE.md)
```
$ shasum -a 256 instance_n15.prefs a357271_1.txt A357271.txt
ed5147118033557c8331a5b2b9ec7b08ee67139ee00f417b951f58ac24983fef  instance_n15.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
instance_n15.prefs: MATCH
a357271_1.txt: MATCH
A357271.txt: MATCH
```
- The object sha256 in claim/CLAIM.md is ed5147...3fef, which matches.
- The a357271_1.txt sha256 in claim/CLAIM.md is 95735e...cd47, which matches.
- All three hashes in claim/REPRODUCE.md match.
- The scratch copy equals the original claim/ for all 8 files.

## Determinism
- My C counter, run 1 vs run 2: stdout byte-identical, and the matching dumps (in search order) byte-identical. Run 3
  also gave a byte-identical dump.
- My Python counter, run 1 vs run 2: stdout byte-identical. Run 3 gave the same count and set hash.
- The author's C counts were identical on re-run.
- My counters use no randomness or timing.

## Bar
- claim/a357271_1.txt states "lb(15)=27059", and its order-15 table counts to 27059 under my parser and both of my
  counters.
- claim/A357271.txt says the improved lower bounds for n=7, 9, 11, 13, 15 are in that linked file. Its data line still
  lists the older a(15)=25011, which is consistent with 27059 being the best known value.
- 30362 > 27059.

## Mismatches
None. Every claimed property was checked:
- order 15, 30 complete strict lists;
- exact count 30362 by my own exhaustive counter, cross-checked by a second counter with a different search order and
  an independent re-check of all 30362 matchings;
- strictly above 27059;
- all stated sha256 values;
- all REPRODUCE.md outputs;
- determinism.

pass: true
