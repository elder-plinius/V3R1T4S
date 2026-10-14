# REPRODUCE skeptic verdict: claim/instance_n15.prefs has exactly 27510 stable matchings

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

Scope: I read only claim/CLAIM.md, claim/REPRODUCE.md and the files inside claim/. Everything ran in a scratch copy
(panel/scratch_reproduce/claim/, which `diff -r` showed to be identical to claim/). My own scripts are in
panel/scratch_reproduce/mine/. I used one CPU thread and `nice -n 15`. I wrote my checker and ran it on every
instance before opening claim/count_stable.py or claim/smclimb.c.

## Definition (quoted verbatim from claim/CLAIM.md)

> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, 1989, Sec. 1.1). The quantity is the
> number of stable matchings of the instance.

## My own checker (panel/scratch_reproduce/mine/sm_count.py, Python 3.9.6 standard library, written from the definition)

- Parser: reads the file as ASCII. It accepts only '#' comment lines and data lines whose tokens match [1-9][0-9]*. It
  requires an even number 2n of data rows, each with exactly n tokens that form a permutation of 1..n. The first n
  rows are the men's lists and the last n rows are the women's lists, most preferred first.
- `is_stable` (the literal definition): the matching must be a bijection, and no pair (m, w) with w not m's partner
  may have m ranking w above his partner and w ranking m above her partner. Its rank tables are built separately with
  list.index.
- Method `fc` (exhaustive): a depth-first search over all bijections men -> women. When man m gets woman w, every
  unassigned man x loses (a) w; (b) if w prefers x to m, every woman x does not strictly prefer to w; (c) every
  woman w2 that m prefers to w and that prefers m to x. A branch is cut only when some unassigned man has nothing
  left.
  - Soundness: each removal is forced by the definition. Otherwise (x, w) or (m, w2) would block in every
    completion.
  - Completeness of the check: take any non-matched pair (m, w) with q(w) = w's partner. The pair is tested when the
    later of m and q(w) is assigned (rule (c) or rule (b) respectively). So every leaf is a stable matching, and no
    stable matching is pruned.
  - Extra checks: every leaf is re-checked with `is_stable`, and the leaves are checked to be pairwise distinct. A
    sha256 of the sorted list of all matchings serves as a fingerprint.
- Method `plain` (exhaustive, most literal): the men are assigned in fixed order 1..n to free women. At each step,
  both possible blocking pairs against each already-assigned couple are tested directly. There is no other pruning
  and no precomputed masks.
- Method `perm`: no pruning at all. All n! bijections from itertools.permutations, each tested with `is_stable`
  (small n only).

### Tests of my checker

Hand-derived counts:
- n2_opposed: men m1: w1>w2, m2: w2>w1; women w1: m2>m1, w2: m1>m2. In {m1w1, m2w2} every man has his first choice,
  so it is stable. In {m1w2, m2w1} every woman has her first choice, so it is stable. Count 2.
- n2_same_prefs: everyone has identical lists (w1>w2 and m1>m2). {m1w1, m2w2} is stable, and in the other matching
  (m1, w1) blocks. Count 1.
- n3_cyclic: men m1: 1 2 3, m2: 2 3 1, m3: 3 1 2; women w1: m2 m3 m1, w2: m3 m1 m2, w3: m1 m2 m3. Wives (1,2,3) is
  stable because every man has his first choice. Wives (3,1,2) is stable because every woman has her first choice.
  Wives (2,3,1) is stable: everyone has their second choice, and each man is last on the list of his first-choice
  woman. The other three are blocked by (m3,w1), (m2,w3) and (m1,w2) respectively. Count 3.

Output:
```
== hand-checkable instances (count derived by hand, see report) ==
n1             hand=1 fc=1 plain=1 perm=1 OK
n2_same_prefs  hand=1 fc=1 plain=1 perm=1 OK
n2_opposed     hand=2 fc=2 plain=2 perm=2 OK
n3_cyclic      hand=3 fc=3 plain=3 perm=3 OK
n4_IL          known=10 fc=10 plain=10 perm=10 OK
== random instances, fc vs plain vs unpruned perm (fixed seed 20261014) ==
random instances tested: 398, mismatches: 0, max count seen: 6
SELFTEST PASS
```

I also parsed all five published instances in claim/a357271_1.txt myself (panel/scratch_reproduce/mine/oeis_parse.py).
- The ranking tables use "i,j": row = man, column = woman; the man ranks her i-th and she ranks him j-th.
- I converted them to preference lists and cross-checked them against the file's MiniZinc rankMen/rankWomen blocks.
- I counted each one with my methods (unpruned `perm` for n <= 9, `plain` for n <= 11, `fc` for all).
- Each count matches the value stated in the file. The order-15 table equals claim/ong_n15_published_27059.prefs
  exactly.
```
orders found in status source: [7, 9, 11, 13, 15] claimed counts: {7: 81, 9: 365, 11: 1690, 13: 7123, 15: 27059}
order 7: table->lists ok, MiniZinc blocks agree with table: True, fc=81 (distinct 81, recheck-fail 0), plain=81, perm(unpruned)=81, claimed=81 -> MATCH
order 9: table->lists ok, MiniZinc blocks agree with table: True, fc=365 (distinct 365, recheck-fail 0), plain=365, perm(unpruned)=365, claimed=365 -> MATCH
order 11: table->lists ok, MiniZinc blocks agree with table: True, fc=1690 (distinct 1690, recheck-fail 0), plain=1690, claimed=1690 -> MATCH
order 13: table->lists ok, MiniZinc blocks agree with table: True, fc=7123 (distinct 7123, recheck-fail 0), claimed=7123 -> MATCH
order 15: table->lists ok, MiniZinc blocks agree with table: True, fc=27059 (distinct 27059, recheck-fail 0), claimed=27059 -> MATCH
order 15 table == ong_n15_published_27059.prefs (men lists equal: True, women lists equal: True)
```

## (2)-(4) My counter on the published instance and on the claimed instance

The parse of claim/instance_n15.prefs shows:
- 31 physical lines: 1 comment line (line 1) and 30 data rows.
- n = 15.
- Every one of the 30 rows (15 men's lists, then 15 women's lists) is a permutation of 1..15, so the lists are
  complete and strict on both sides.
- No CR characters, no tabs, and a trailing newline.

`fc` output, run 1:
```
file: ong_n15_published_27059.prefs
parse: {'n': 15, 'physical_lines': 31, 'comment_lines': [1], 'data_rows': 30, 'trailing_newline': True, 'has_CR': False, 'has_TAB': False}
fc_count: 27059
fc_distinct: 27059
fc_leaves_failing_definition_recheck: 0
fc_search_nodes: 108364
fc_sha256_sorted_matchings: 73589602c52b607c56530c4afe6377acfb2465270467485b13c2719ca4f7b9ff
first_matching(lex): 1 3 2 5 4 9 6 7 8 10 11 12 13 14 15
last_matching(lex): 15 14 11 12 7 10 9 8 6 5 4 3 2 1 13
seconds: 2.5
----
file: instance_n15.prefs
parse: {'n': 15, 'physical_lines': 31, 'comment_lines': [1], 'data_rows': 30, 'trailing_newline': True, 'has_CR': False, 'has_TAB': False}
fc_count: 27510
fc_distinct: 27510
fc_leaves_failing_definition_recheck: 0
fc_search_nodes: 108993
fc_sha256_sorted_matchings: aff7d79efbd374b813963949ccbd8ec445243232e87d44ea37c36b3514cbe12d
first_matching(lex): 1 3 2 5 4 9 6 7 8 10 11 12 13 14 15
last_matching(lex): 15 14 11 12 9 10 5 6 4 8 7 3 2 1 13
seconds: 2.5
```
`plain` output (the literal pairwise check, a separate code path):
```
file: instance_n15.prefs
parse: {'n': 15, 'physical_lines': 31, 'comment_lines': [1], 'data_rows': 30, 'trailing_newline': True, 'has_CR': False, 'has_TAB': False}
plain_count: 27510
seconds: 11.8
file: ong_n15_published_27059.prefs
parse: {'n': 15, 'physical_lines': 31, 'comment_lines': [1], 'data_rows': 30, 'trailing_newline': True, 'has_CR': False, 'has_TAB': False}
plain_count: 27059
seconds: 12.5
```
Both of my methods give 27510 for claim/instance_n15.prefs, which equals the claimed 27510. All 27510 enumerated
matchings pass the definition re-check and are distinct. 27510 > 27059.

## (7) Determinism (my counter, run 2, separate process)
```
file: instance_n15.prefs
parse: {'n': 15, 'physical_lines': 31, 'comment_lines': [1], 'data_rows': 30, 'trailing_newline': True, 'has_CR': False, 'has_TAB': False}
fc_count: 27510
fc_distinct: 27510
fc_leaves_failing_definition_recheck: 0
fc_search_nodes: 108993
fc_sha256_sorted_matchings: aff7d79efbd374b813963949ccbd8ec445243232e87d44ea37c36b3514cbe12d
first_matching(lex): 1 3 2 5 4 9 6 7 8 10 11 12 13 14 15
last_matching(lex): 15 14 11 12 9 10 5 6 4 8 7 3 2 1 13
seconds: 2.1
---- run2 ong
file: ong_n15_published_27059.prefs
parse: {'n': 15, 'physical_lines': 31, 'comment_lines': [1], 'data_rows': 30, 'trailing_newline': True, 'has_CR': False, 'has_TAB': False}
fc_count: 27059
fc_distinct: 27059
fc_leaves_failing_definition_recheck: 0
fc_search_nodes: 108364
fc_sha256_sorted_matchings: 73589602c52b607c56530c4afe6377acfb2465270467485b13c2719ca4f7b9ff
first_matching(lex): 1 3 2 5 4 9 6 7 8 10 11 12 13 14 15
last_matching(lex): 15 14 11 12 7 10 9 8 6 5 4 3 2 1 13
seconds: 2.1
```
Run 1 and run 2 match exactly: the counts, the search-node counts and the sha256 of the full sorted set of
matchings. Only the wall-clock times differ.

## (5) The author's commands from claim/REPRODUCE.md, run verbatim in the scratch copy
```
$ python3 -I count_stable.py --prefs instance_n15.prefs --brute --expect 27510
n: 15
lattice_count: 27510  (1.68s)
brute_count: 27510  (10.66s)
counters_agree: True
expected: 27510 PASS
real 12.52
user 6.59
sys 0.08
exit=0

$ cc -O2 -o smclimb smclimb.c && ./smclimb count instance_n15.prefs 1     (Apple clang version 21.0.0)
cc_exit=0
file: instance_n15.prefs
n: 15
count: 27510
verify: 1
seconds: 0.0367
exit=0
$ ./smclimb count instance_n15.prefs 1 (second run)
file: instance_n15.prefs
n: 15
count: 27510
verify: 1
seconds: 0.0138
exit=0
$ ./smclimb count ong_n15_published_27059.prefs 1
file: ong_n15_published_27059.prefs
n: 15
count: 27059
verify: 1
seconds: 0.0148
exit=0

$ python3 -I count_stable.py --prefs ong_n15_published_27059.prefs --brute --expect 27059
n: 15
lattice_count: 27059  (1.80s)
brute_count: 27059  (12.73s)
counters_agree: True
expected: 27059 PASS
exit=0
$ python3 -I count_stable.py --oeis a357271_1.txt --n 15 --expect 27059
minizinc_blocks_match_paired_table: True
n: 15
claimed_in_file: 27059
lattice_count: 27059  (1.71s)
expected: 27059 PASS
matches_claimed_in_file: True
exit=0
```
The author's counters agree with my own counters on both instances (27510 and 27059).

## (6) sha256 of the saved files
```
$ shasum -a 256 instance_n15.prefs a357271_1.txt
3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8  instance_n15.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
```
Both values equal those stated in claim/CLAIM.md and claim/REPRODUCE.md, and an independent hashlib computation gave
MATCH for both. claim/a357271_1.txt states "lb(15)=27059", and the order-15 instance in it has exactly 27059 stable
matchings by my counter.

## Mismatches and notes

- No mismatch in any claimed value or property.
- Cosmetic only: the smclimb output also prints "file:" and "seconds:" lines that claim/REPRODUCE.md does not
  mention.
- Cosmetic only: the Python brute-force method took about 11-13 s, not the "about 15 s" stated.
- Not checked by me: that 27059 is still the best published value for n = 15 today. That needs a literature or
  OEIS check beyond the saved status file, and the reproduction did not need web access. Within the saved files, the
  bar is 27059 and the claimed instance beats it: 27510 > 27059.

## Verdict

My own exhaustive counter, built from the quoted definition, confirms every claimed property:
- order 15 with complete strict lists on both sides;
- exactly 27510 stable matchings, from two independent methods with every matching re-verified;
- deterministic across runs;
- matching sha256 values;
- strictly more than the 27059 of the published instance, which I also reproduced.

The author's commands reproduce the same numbers.

pass: true
