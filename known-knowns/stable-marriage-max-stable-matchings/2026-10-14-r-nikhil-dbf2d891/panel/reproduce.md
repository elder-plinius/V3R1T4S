# REPRODUCE skeptic: does claim/instance_n28.prefs have exactly 2497797760 stable matchings?

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

**Summary.** I wrote my own exhaustive counter from the definition before opening the author's code. It finds exactly **2497797760** stable matchings in claim/instance_n28.prefs.

- Every one of those matchings was re-checked against the definition, with 0 failures.
- A completeness check at every matching also had 0 failures.
- A second, different counting algorithm on my rotation poset gives the same number.
- The author's memoised count gives the same number.
- The author's reverse-search enumeration also gives 2497797760 with 0 unstable matchings. I ran it from a copy patched only to skip a large memo table, to stay within the 2 GB memory budget (section 6).

The issues with the author's resource statements are in "Mismatches and issues"; none of them affect the value.

**What I read.** I read claim/CLAIM.md, claim/REPRODUCE.md and the three data files.
- I never opened claim/count_stable.py.
- I opened claim/smcount3.c only after my own n = 28 result was finished, to find out why its `enumerate` mode used about 2.9 GB.

**Where I worked.** Everything ran in a scratch copy, panel/scratch_reproduce/claim.
- Its files have the same sha256 as claim/. I checked instance_n28.prefs, a357271_1.txt, A357271.txt, smcount3.c and count_stable.py.
- The claim folder was not modified.

## 1. Definition (verbatim from claim/CLAIM.md, section "Definition")

> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, MIT Press 1989, Sec. 1.1). The
> quantity is the number of stable matchings of the instance.

File format, from claim/CLAIM.md, "Files": after the comment line(s), "lines 1-28 are the men's lists (women numbered 1..28, most preferred first), lines 29-56 the women's lists (men 1..28, most preferred first)".

## 2. My checker

Source files (scratch, not part of the claim):
- panel/scratch_reproduce/mine/mysm_n28run.c, sha256 69dbe42901e690b8c5b2ce934d68a94fc2f913c87bab508d3aa28b1d0f08c088.
  - This is the exact source of the binary `mysm` that produced every `mysm` output below.
- panel/scratch_reproduce/mine/mysm.c, sha256 cfb9c9c91a3760d42b183ae4c1da646447581035690546800e6e3fbc06f52e34.
  - It is the same code plus two modes added afterwards, `vtest` and `count`, built separately as `mysm_v2`.
  - Everything before the added modes is byte-identical to mysm_n28run.c.
- panel/scratch_reproduce/mine/parse_oeis.py, sha256 23fb3e4fa01356385f8d63ee9bacfb65aeb614df5119866e34a53692c5507701.
  - This is my parser for claim/a357271_1.txt.

Method (C, one thread):

1. **Parser.**
   - Lines starting with '#' are comments.
   - There must be exactly 2n data rows of n integers each, with nothing else on the row.
   - Every row must be a permutation of 1..n, which means the lists are complete and strict. Otherwise the program aborts.
2. **Gale-Shapley.** Running it with men proposing gives M0; running it with women proposing gives Mz.
   - Both are re-checked against the definition.
   - Every man must weakly prefer M0 to Mz, and every woman Mz to M0.
3. **Rotations along one chain M0 -> Mz.** At the current matching M:
   - For each man with p_M(m) != p_Mz(m), s_M(m) is the first woman after p_M(m) on his list who prefers m to her partner, and next_M(m) = p_M(s_M(m)).
   - The program aborts if s_M(m) is undefined or next_M leaves that set.
   - One cycle of next_M is taken as a rotation and eliminated.
   - Each move must take a man down his list and a woman up hers. No (man, woman) step may occur twice.
   - Every intermediate matching is re-checked against the definition, and the chain must end exactly at Mz.
   - Rotations are indexed in elimination order.
4. **Poset edges.**
   - Type 1: the rotation that moves m to w precedes the rotation that moves m from w.
   - Type 2: suppose a rotation moves m from w_i to w_{i+1}, and w is a woman strictly between them on m's list. Then the unique rotation that moves w from a man she ranks below m to a man she ranks above m precedes it.
     - There is no such rotation if her M0 partner already beats m.
     - The program aborts if she has no such crossing, has two, or is ever matched to m.
   - Every edge is re-derived from the rotation records alone, and must have a type-1 or type-2 witness.
   - Every edge must point forward in the index order, so that order is a linear extension.
5. **Enumeration: reverse search over closed subsets, with no visited set.**
   - The parent of an ideal is the ideal minus its highest-index element.
   - The children of an ideal add a rotation of larger index whose predecessors are all present. The program keeps a per-rotation count of missing predecessors and a sorted candidate list.
   - The matching is updated incrementally as rotations are added and removed.
   - At **every** visited ideal the program checks:
     - (a) the matching is a bijection;
     - (b) **the definition over all n*n pairs (m, w)**: no pair where m prefers w to his partner and w prefers m to hers. This is a full check, vectorised over w, with no incremental shortcut;
     - (c) when a rotation is applied, each of its men currently holds the rotation's old woman, and undo restores the matching exactly;
     - (d) with `local` (used for n = 28): the rotations exposed in the current matching are recomputed from scratch as the cycles of next_M. Each must be a known rotation with identical pairs, not yet in the ideal, with all its predecessors present. Their number must equal the number of rotations the poset allows to be added;
     - (e) an order-independent hash of all visited matchings is accumulated (sum and xor of 64-bit Zobrist hashes).
6. **`brute` (definition only).**
   - Backtracking over all bijections, one man at a time.
   - A branch is pruned only when a blocking pair already exists among people whose partners are fixed. This is exact pruning: no completion of that branch can be stable.
   - Every leaf gets the full n*n definition check.
7. **`count` (a second algorithm on the same poset).** It uses #ideals(S) = #ideals(S \ up(x)) + #ideals(S \ down(x)), multiplies over comparability components, and memoises on the remaining set.

**Why the enumeration count equals the number of stable matchings.**

*Upper bound: the count is at most the number of stable matchings.*
- Every visited matching passed (a) and (b), so each one is a stable matching.
- Distinct ideals give distinct matchings:
  - Type-1 edges make each man's rotations a chain, so his rotations within an ideal form a prefix of that chain.
  - Two different ideals have prefixes of different lengths for some man.
  - Each step moves him strictly down his list (checked at each step by (c)), so his partner differs.

*Lower bound: the count is at least the number of stable matchings.* Each edge is a genuine precedence:
- **Type 1:** while the rotation that moves m from w is exposed, m holds w, so the rotation that moved him to w has already been eliminated.
- **Type 2:** in every M where the later rotation is exposed, s_M(m) = w_{i+1}. So every woman strictly between w_i and w_{i+1} prefers her M-partner to m, which means the rotation that moved her past m has already been eliminated.
- Gusfield & Irving ch. 2-3 give two facts: one chain contains all rotations, and stable matchings correspond one-to-one to closed subsets of the rotation poset. Every closed set of the true poset is therefore closed in mine.

*A check that does not depend on that theorem.* Check (d) passed at all 2497797760 matchings, so:
- the visited set contains M0 and is closed under eliminating any exposed rotation;
- every stable matching can be reached from M0 by such eliminations;
- no exposed rotation outside the 362 found was ever met.

## 3. Tests of my checker (pasted program output)

### Tiny hand-checkable instances

The instances:
- t1: n = 1.
- t2: n = 2, with opposed lists: men (1 2 | 2 1), women (2 1 | 1 2).
- t2b: n = 2, with identical lists.
- t3: n = 3, cyclic: men (1 2 3 | 2 3 1 | 3 1 2), women (2 3 1 | 3 1 2 | 1 2 3).
- t4: n = 4, the 10-matching type: men (1 2 3 4 | 2 1 4 3 | 3 4 1 2 | 4 3 2 1), women (4 3 2 1 | 3 4 1 2 | 2 1 4 3 | 1 2 3 4).

Expected counts by hand:
- t1: 1.
- t2: 2. Men-optimal (1,2) and women-optimal (2,1) are both stable, and there are only two bijections.
- t2b: 1.
- t3: 3. The stable matchings are: all men get their first choice, all men get their second choice, or all women get their first choice. The other three bijections are unstable. I checked one by hand: (m1-w1, m2-w3, m3-w2) is blocked by (m3, w1).
- t4: 10. This agrees with claim/A357271.txt: a(4) = 10, and its comment says "the bounds were known to be exact up to n=4".

Output of `mysm enum tX local scalar`, then the sorted matchings (woman of man 1..n) from `enum dump` and `brute dump`:
```
== t1
enumerated_ideals: 1          unstable_matchings ...: 0   all_checks_passed: yes
-- enum dump:  1|
-- brute dump: 1|
== t2
rotations found along chain M0->Mz: 1 (total pairs 2, max size 2)
enumerated_ideals: 2          unstable_matchings ...: 0   all_checks_passed: yes
-- enum dump:  1 2|2 1|
-- brute dump: 1 2|2 1|
== t2b
enumerated_ideals: 1          unstable_matchings ...: 0   all_checks_passed: yes
-- enum dump:  1 2|
-- brute dump: 1 2|
== t3
rotations found along chain M0->Mz: 2 (total pairs 6, max size 3)
poset edges: type1 occurrences 3, type2 occurrences 0, distinct edges 1 (...)
enumerated_ideals: 3          unstable_matchings ...: 0   all_checks_passed: yes
-- enum dump:  1 2 3|2 3 1|3 1 2|
-- brute dump: 1 2 3|2 3 1|3 1 2|
== t4
rotations found along chain M0->Mz: 6 (total pairs 12, max size 2)
poset edges: type1 occurrences 8, type2 occurrences 0, distinct edges 8 (...)
enumerated_ideals: 10         unstable_matchings ...: 0   all_checks_passed: yes
-- enum dump:  1 2 3 4|1 2 4 3|2 1 3 4|2 1 4 3|2 4 1 3|3 1 4 2|3 4 1 2|3 4 2 1|4 3 1 2|4 3 2 1|
-- brute dump: 1 2 3 4|1 2 4 3|2 1 3 4|2 1 4 3|2 4 1 3|3 1 4 2|3 4 1 2|3 4 2 1|4 3 1 2|4 3 2 1|
```
For layout I joined lines; every number is as printed.

### Random instances: enumerator (with `local` and `scalar` on) vs definition-only brute force

A trial counts as a mismatch if the counts differ, either hash differs, or any check fails.
```
rand n=1 trials=3000: mismatches=0 (total stable matchings 3000, max 1)
rand n=2 trials=3000: mismatches=0 (total stable matchings 3400, max 2)
rand n=3 trials=3000: mismatches=0 (total stable matchings 3870, max 3)
rand n=4 trials=3000: mismatches=0 (total stable matchings 4494, max 5)
rand n=5 trials=3000: mismatches=0 (total stable matchings 5157, max 6)
rand n=6 trials=3000: mismatches=0 (total stable matchings 5706, max 7)
rand n=7 trials=3000: mismatches=0 (total stable matchings 6598, max 11)
rand n=8 trials=3000: mismatches=0 (total stable matchings 7371, max 12)
rand n=9 trials=1000: mismatches=0 (total stable matchings 2713, max 12)
rand n=10 trials=300: mismatches=0 (total stable matchings 892, max 10)
rand n=12 trials=50: mismatches=0 (total stable matchings 183, max 10)
```

### Published instances in claim/a357271_1.txt (my own parser)

Parser output. The ranking tables and the MiniZinc arrays were parsed independently and agree exactly:
```
order 7: stated 81 SM; 7 x 7 table parsed, all 2n rank vectors are permutations; MiniZinc rankMen/rankWomen identical to table -> ong_n7.prefs
order 9: stated 365 SM; 9 x 9 table parsed, all 2n rank vectors are permutations; MiniZinc rankMen/rankWomen identical to table -> ong_n9.prefs
order 11: stated 1690 SM; 11 x 11 table parsed, all 2n rank vectors are permutations; MiniZinc rankMen/rankWomen identical to table -> ong_n11.prefs
order 13: stated 7123 SM; 13 x 13 table parsed, all 2n rank vectors are permutations; MiniZinc rankMen/rankWomen identical to table -> ong_n13.prefs
order 15: stated 27059 SM; 15 x 15 table parsed, all 2n rank vectors are permutations; MiniZinc rankMen/rankWomen identical to table -> ong_n15.prefs
```
Each block below gives:
- `mysm enum ong_nN.prefs local scalar`;
- `mysm brute ong_nN.prefs`;
- a comparison of the sorted lists of all matchings from `enum dump` and `brute dump`.
```
--- order 7: mysm enum (local scalar)
rotations found along chain M0->Mz: 18 (total pairs 36, max size 2)
poset edges: type1 occurrences 29, type2 occurrences 0, distinct edges 29 (all have witnesses, all go forward in chain order)
enumerated_ideals: 81
unstable_matchings (blocking pair found, full n*n check): 0
not_a_bijection: 0
rotation_not_exposed_when_applied: 0, undo_mismatch: 0
scalar_vs_vector_check_mismatch: 0
local_completeness_failures: 0
hash_sum: 2b0c23401eba5750 hash_xor: 1efd9d5813eda998
all_checks_passed: yes
--- order 7: mysm brute
brute_force_stable_matchings: 81
hash_sum: 2b0c23401eba5750 hash_xor: 1efd9d5813eda998
--- order 7: sorted matching lists: enum 81 lines (81 distinct), brute 81 lines; cmp: identical
--- order 9: mysm enum (local scalar)
rotations found along chain M0->Mz: 32 (total pairs 64, max size 2)
poset edges: type1 occurrences 55, type2 occurrences 0, distinct edges 55 (all have witnesses, all go forward in chain order)
enumerated_ideals: 365
unstable_matchings (blocking pair found, full n*n check): 0
not_a_bijection: 0
rotation_not_exposed_when_applied: 0, undo_mismatch: 0
scalar_vs_vector_check_mismatch: 0
local_completeness_failures: 0
hash_sum: d141315715d04da2 hash_xor: 838224bf3b43f6e6
all_checks_passed: yes
--- order 9: mysm brute
brute_force_stable_matchings: 365
hash_sum: d141315715d04da2 hash_xor: 838224bf3b43f6e6
--- order 9: sorted matching lists: enum 365 lines (365 distinct), brute 365 lines; cmp: identical
--- order 11: mysm enum (local scalar)
rotations found along chain M0->Mz: 50 (total pairs 100, max size 2)
poset edges: type1 occurrences 89, type2 occurrences 0, distinct edges 89 (all have witnesses, all go forward in chain order)
enumerated_ideals: 1690
unstable_matchings (blocking pair found, full n*n check): 0
not_a_bijection: 0
rotation_not_exposed_when_applied: 0, undo_mismatch: 0
scalar_vs_vector_check_mismatch: 0
local_completeness_failures: 0
hash_sum: 65fe543a4e0c7788 hash_xor: ce84f38204f9bf86
all_checks_passed: yes
--- order 11: mysm brute
brute_force_stable_matchings: 1690
hash_sum: 65fe543a4e0c7788 hash_xor: ce84f38204f9bf86
--- order 11: sorted matching lists: enum 1690 lines (1690 distinct), brute 1690 lines; cmp: identical
--- order 13: mysm enum (local scalar)
rotations found along chain M0->Mz: 71 (total pairs 142, max size 2)
poset edges: type1 occurrences 129, type2 occurrences 2, distinct edges 130 (all have witnesses, all go forward in chain order)
enumerated_ideals: 7123
unstable_matchings (blocking pair found, full n*n check): 0
not_a_bijection: 0
rotation_not_exposed_when_applied: 0, undo_mismatch: 0
scalar_vs_vector_check_mismatch: 0
local_completeness_failures: 0
hash_sum: ef2a59a32d38a19a hash_xor: 409fdd894d5d0d42
all_checks_passed: yes
--- order 13: mysm brute
brute_force_stable_matchings: 7123
hash_sum: ef2a59a32d38a19a hash_xor: 409fdd894d5d0d42
--- order 13: sorted matching lists: enum 7123 lines (7123 distinct), brute 7123 lines; cmp: identical
--- order 15: mysm enum (local scalar)
rotations found along chain M0->Mz: 94 (total pairs 188, max size 2)
poset edges: type1 occurrences 173, type2 occurrences 8, distinct edges 179 (all have witnesses, all go forward in chain order)
enumerated_ideals: 27059
unstable_matchings (blocking pair found, full n*n check): 0
not_a_bijection: 0
rotation_not_exposed_when_applied: 0, undo_mismatch: 0
scalar_vs_vector_check_mismatch: 0
local_completeness_failures: 0
hash_sum: 84fb3f167f5d7312 hash_xor: cf2d52b3808b86b4
all_checks_passed: yes
--- order 15: mysm brute
brute_force_stable_matchings: 27059
hash_sum: 84fb3f167f5d7312 hash_xor: cf2d52b3808b86b4
--- order 15: sorted matching lists: enum 27059 lines (27059 distinct), brute 27059 lines; cmp: identical
```
All five published counts (81, 365, 1690, 7123, 27059) are reproduced, and the enumerator and the brute force produce exactly the same sets of matchings.

### Fault injection: the per-matching checks catch wrong posets

- `dropall` removes every poset edge, so many non-ideals are visited:
  ```
  enumerated_ideals: 262144
  unstable_matchings (blocking pair found, full n*n check): 1301
  not_a_bijection: 171752
  rotation_not_exposed_when_applied: 128130, undo_mismatch: 3072
  all_checks_passed: NO
  ```
- `addfalse` adds one false edge, which makes the count too small. The stability check cannot see this; the local check does:
  ```
  FAULT INJECTION: added false edge 39 -> 93
  enumerated_ideals: 27058
  unstable_matchings (blocking pair found, full n*n check): 0
  local_completeness_failures: 1
  all_checks_passed: NO
  ```
  Without `local`, the same run prints `enumerated_ideals: 27058 ... all_checks_passed: yes`. This is why `local` was switched on for n = 28.
- `droptype2` on orders 13 and 15 still gives 7123 and 27059 with all checks passing. On these instances the type-2 edges are implied by the type-1 edges.

### The vectorised check against the scalar definition, including unstable inputs

`mysm_v2 vtest FILE 200000` tests uniformly random bijections and single transpositions of M0 and of Mz:
```
(order 15)  vtest: 600000 matchings tested, 555361 unstable by scalar definition check, 0 disagreements with vector check
(order 28)  vtest: 600000 matchings tested, 571380 unstable by scalar definition check, 0 disagreements with vector check
```

### Determinism

The same `mysm` binary as the n = 28 run was run twice per instance; the outputs were compared with `cmp`, excluding the time_s line:
```
n=13: run1 and run2 outputs identical (excluding time_s line)
enumerated_ideals: 7123
hash_sum: ef2a59a32d38a19a hash_xor: 409fdd894d5d0d42
all_checks_passed: yes
n=15: run1 and run2 outputs identical (excluding time_s line)
enumerated_ideals: 27059
hash_sum: 84fb3f167f5d7312 hash_xor: cf2d52b3808b86b4
all_checks_passed: yes
```
The hash fingerprints also equal those from the separate earlier runs above.

## 4. The claimed object: claim/instance_n28.prefs

My C parser (the first line of every mysm run on it):
```
parsed ../claim/instance_n28.prefs: comment_lines=1 data_rows=56 n=28; all 56 lists are permutations of 1..28 (complete, strict)
```
A separate Python check:
```
comment lines: 1 data lines: 56 trailing empty: True
n = 28 rows = 56 all rows length n: True
all rows are permutations of 1..n: True
distinct men lists: 28 distinct women lists: 28
```
So the instance has order 28, with 28 men's and 28 women's lists, each complete and strict. **Confirmed.**

## 5. My count on claim/instance_n28.prefs

Command: `nice -n 15 ./mysm enum ../claim/instance_n28.prefs local`. It ran with nohup in the background, with the full n*n definition check and the local completeness check at every matching. The full stdout:
```
parsed ../claim/instance_n28.prefs: comment_lines=1 data_rows=56 n=28; all 56 lists are permutations of 1..28 (complete, strict)
M0 (man-optimal, GS): 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
Mz (woman-optimal, GS): 16 15 14 13 20 19 18 17 24 23 22 21 28 27 26 25 4 3 2 1 8 7 6 5 12 11 10 9
rotations found along chain M0->Mz: 362 (total pairs 724, max size 2)
poset edges: type1 occurrences 696, type2 occurrences 0, distinct edges 696 (all have witnesses, all go forward in chain order)
minimal rotations: 14
enumerated_ideals: 2497797760
unstable_matchings (blocking pair found, full n*n check): 0
not_a_bijection: 0
rotation_not_exposed_when_applied: 0, undo_mismatch: 0
local_completeness_failures: 0
hash_sum: 14285145928a5040 hash_xor: e070bba4c85ae7bf
max_ideal_size: 362 (R=362), ideals_of_size_R: 1
time_s: 840.04
all_checks_passed: yes
```
stderr progress lines (the first and the last two):
```
progress: 134217728 matchings, unstable 0, 49.0 s
progress: 2281701376 matchings, unstable 0, 775.7 s
progress: 2415919104 matchings, unstable 0, 814.5 s
```
Second algorithm on my poset (`mysm_v2 count`, split/memo):
```
count_ideals (split/memo): 2497797760, memo entries 2230, time_s 0.02
```
The same mode on the test instances gave 3, 10, 81, 365, 1690, 7123 and 27059.

Peak RSS of my enumerator was about 4.8 MB.

**My result: 2497797760, equal to the claimed 2497797760.**

## 6. The author's commands (claim/REPRODUCE.md), run only after section 5

All commands were run from panel/scratch_reproduce/claim, the copy of claim/.

### 6a. Compile
```
$ cc -O2 -o smcount3 smcount3.c -lm
```
There was no output: no warnings and no errors.

### 6b. Memoised count
```
$ MEMO_MAX_STATES=40000000 nice -n 15 /usr/bin/time -l ./smcount3 count instance_n28.prefs 0
file: instance_n28.prefs
n: 28
rotations: 362
memo_states: 6324107
count_poset: 2497797760
seconds_poset: 2.8775
        3.14 real         1.71 user         0.60 sys
          2953887744  maximum resident set size
          2954840488  peak memory footprint
```
- count_poset is 2497797760, the claimed value and equal to my count.
- 362 rotations, the same as mine.
- 6324107 memo states and 2.9 s match REPRODUCE.md's "about 6.3 million memo states, about 2 s".
- Peak RSS was 2.95 GB; see the issues section.

### 6c. Reverse-search enumeration

**Unmodified run.**
- `nohup nice -n 15 ./smcount3 enumerate instance_n28.prefs` had an RSS of 2884624 KB after 2 s and still after 9 s.
- I killed it because of the 2 GB memory budget.
- The reason, found by reading claim/smcount3.c only after my count was done:
  - `enumerate_verified()` first calls `count_poset()`, which builds the memo table.
  - `main()` then calls `count_poset()` twice more for its `agree` line.
  - The memo table stays allocated for the whole run.

**Patched copy.** panel/scratch_reproduce/mine/author_lowmem/smcount3_lowmem.c, sha256 5883792156552b506bb0df49b77dea6eafc67cb4383548dd5914fd0429837723. The complete diff against claim/smcount3.c:
```
123c123
< static long g_states; static int g_verify_chain = 0;
---
> static long g_states; static int g_verify_chain = 0; static int g_skip_dp = 0; /* REPRODUCE-skeptic patch: SKIP_DP env skips the memo DP (memory) */
188a189
>     if (g_skip_dp) { g_states = 0; return 0; } /* patch */
388a390
>         g_skip_dp = getenv("SKIP_DP") != NULL; /* patch */
```
- `count_poset()` still finds the rotations along the chain, with its own per-matching stability check (`g_verify_chain = 1`). It still builds the predecessors and masks. It returns just before the memo DP.
- `rs_dfs()`, the reverse search with an `is_stable()` full n*n check at every ideal, is unchanged.
- Sanity check of the patched copy: on orders 13 and 15 it printed `enumerated_ideals: 7123` and `enumerated_ideals: 27059`, each with `unstable_matchings_found: 0`.
- The unpatched program on order 15 printed `count_poset: 27059`, `enumerated_ideals: 27059` and `agree: yes`.

The run on n = 28:
```
$ SKIP_DP=1 nohup nice -n 15 /usr/bin/time -l ../mine/author_lowmem/smcount3_lowmem enumerate instance_n28.prefs
count_poset: 0
enumerated_ideals: 2497797760
unstable_matchings_found: 0
n: 28
rotations: 362
seconds_enumerate: 3600.41
agree: NO
     3600.42 real      2351.82 user        25.59 sys
           182239232  maximum resident set size
             7373472  peak memory footprint
```
- `count_poset: 0` and `agree: NO` are artefacts of SKIP_DP, by construction.
- The values that matter:
  - **enumerated_ideals 2497797760**, equal to the count_poset of 6b and to my count;
  - **unstable_matchings_found 0**.
- To estimate progress I attached lldb twice and read rs_count and rs_unstable with read-only expressions. The values were 2004902520 / 0 and 2329413573 / 0.
- The 182 MB "maximum resident set size" comes from those attaches. The process's own peak memory footprint was 7.4 MB.
- The machine was heavily loaded, with load average 50-180 during this run.

### 6d. grep and shasum

These outputs are in sections 7 and 8.

## 7. sha256 of the saved files vs. the stated values

```
$ shasum -a 256 instance_n28.prefs a357271_1.txt A357271.txt
dbf2d89155213b672ef7514493d16c7f02225a84dbcc31f4ae30068f085e1ad0  instance_n28.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```
- instance_n28.prefs matches the "object sha256" in claim/CLAIM.md and the value in claim/REPRODUCE.md.
- a357271_1.txt matches claim/REPRODUCE.md.
- A357271.txt matches both claim/CLAIM.md and claim/REPRODUCE.md.
- The original files in claim/ have the same hashes as the scratch copy.

**All match.**

## 8. Bar (from the saved status source only)

```
$ grep -E '^%S|^%T|^%U' A357271.txt
%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,
%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,
%U A357271 127885440,262860800,384418176,2000043808
```
My parse: `terms: 28 a(28)= 2000043808  a(28) < 2497797760: True`.
- The offset is 1 (`%O A357271 1,2`), so the 28th term is a(28) = 2000043808.
- claim/a357271_1.txt contains examples only for orders 7, 9, 11, 13 and 15 (header lines 29, 58, 94, 136 and 184). This is consistent with the entry's comment: "Improved lower bounds for n=7, 9, 11, 13, 15 are shown in linked Ong et al. (2025) file."
- 2497797760 > 2000043808, so the claim beats the bar given by the saved status source.
- I did not check, and cannot check from these files, whether a larger n = 28 instance exists elsewhere.

## Mismatches and issues

**No mismatch in any claimed value or property.**
- The count is 2497797760 from four routes:
  - my exhaustive enumeration, with the full definition check and the local completeness check at every matching;
  - my split/memo count;
  - the author's memo DP;
  - the author's reverse-search enumeration, with its own per-matching check.
- The instance has order 28, with 28 + 28 complete strict lists.
- The sha256 of all three saved files match the stated values.
- The bar is a(28) = 2000043808 < 2497797760.
- Both programs find 362 rotations. The author's program has about 6.3 million memo states, as stated.

**Determinism.**
- Repeated runs of my counter gave identical output, including the hash fingerprints of the full matching sets, on orders 13 and 15.
- The two methods in my program and the two in the author's agree.

**Issues. They concern resources and documentation, not the claim:**
1. The memo count peaked at 2.95 GB. `MEMO_MAX_STATES=40000000 ./smcount3 count instance_n28.prefs 0` reached a peak RSS of 2953887744 bytes. My task brief expected about 1.5 GB; claim/REPRODUCE.md gives no memory figure. I ran it once before I knew this, for 3 s, so it briefly exceeded my 2 GB budget.
2. The documentation of `enumerate` is wrong about memory. claim/CLAIM.md and claim/REPRODUCE.md say `enumerate` uses "memory O(rotations)". As shipped, it runs the memo DP first and keeps the roughly 2.9 GB table for the whole run.
   - So I could not run the REPRODUCE.md `enumerate` command verbatim within budget, and its literal `agree: yes` line was not reproduced.
   - The copy patched to skip only the DP reproduced the substance: `enumerated_ideals: 2497797760` and `unstable_matchings_found: 0`.
   - I checked myself that this equals the count_poset of 6b.
3. Timing. claim/REPRODUCE.md says "about 25 minutes" for the enumeration. Here it took 2352 s CPU and 3600 s wall on a heavily loaded machine. My own n = 28 enumeration took 840 s wall.

**Not checked.**
- claim/count_stable.py: I never opened or ran it, and REPRODUCE.md gives no command for it.
- The "origin" paragraph, which is labelled as information only.
- Whether a better n = 28 instance exists outside the saved status source.

**Verdict.** My own checker, built from the quoted definition, confirmed every claimed property and the exact value 2497797760:
- claim/instance_n28.prefs is an order-28 instance with complete strict preference lists;
- it has exactly 2497797760 stable matchings;
- that is strictly more than a(28) = 2000043808 in the saved A357271 entry;
- the saved files' sha256 match the stated values.

The coverage was exhaustive: every matching was checked, and no sampling was used.

pass: true
