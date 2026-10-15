# REPRODUCE skeptic verdict: claim/instance_n22.prefs (n = 22, claimed 12277568 stable matchings)

context: subagent (Claude Code Agent tool, fresh context, sees only claim/)

What I looked at: claim/CLAIM.md, claim/REPRODUCE.md and the data files claim/instance_n22.prefs, claim/a357271_1.txt
and claim/A357271.txt. I never opened claim/count_stable.py. I wrote my own counter, ran it and got its result before
opening claim/smcount3.c. I then opened smcount3.c only to grep its allocation sizes, so I could bound its memory
before running the author's commands. All work ran in a scratch copy (panel/scratch_reproduce/claim/), one process at a
time, single-threaded, under `nice -n 15`. The session was paused twice by usage limits. Every output below comes from
runs made after the last resume.

## Definition (quoted verbatim from claim/CLAIM.md, section "Definition")

> Stable marriage instance of order n: n men and n women, each with a complete strict preference list over the other
> side. A matching (bijection men -> women) is stable iff there is no blocking pair (m, w): m prefers w to his partner
> and w prefers m to her partner (Gusfield & Irving, The Stable Marriage Problem, MIT Press 1989, Sec. 1.1). The
> quantity is the number of stable matchings of the instance.

## My own checker (written from the definition before reading any author code)

File: panel/scratch_reproduce/mine/mycount.c (one C file, `cc -O2 -Wall -Wextra`, compiles with no warnings).
sha256: 5d3f40abdee692be5726f27d8ef1e28e2d6116fc11a6fecae79b7d34ad64541b

- Parsers (my own). Prefs format: lines starting with `#` are comments; then there must be exactly 2n data lines of
  exactly n integers each. Every line must be a permutation of 1..n (complete and strict); otherwise the program aborts.
  Lines 1..n are the men's lists and lines n+1..2n the women's. Ranking-table format of claim/a357271_1.txt: the block
  "order N example with K SM" has N rows of N pairs "a,b". Row i, column j means man i ranks woman j a-th and woman j
  ranks man i b-th (as the file explains). Every rank vector must be a permutation. The parsed table is also compared
  with the MiniZinc `rankWomen[w,m]` / `rankMen[m,w]` arrays in the same file, and all five agree.
- Stability test, literally the quoted definition over all n*n pairs: M must be a bijection, and M is unstable iff some
  (m, w) has rank_m(w) < rank_m(M(m)) and rank_w(m) < rank_w(M^-1(w)).
  ```
  for (m) for (w) if (mrank[m][w] < mrank[m][M[m]] && wrank[w][m] < wrank[w][Minv[w]]) return 0;
  ```
- Exhaustive lattice walk. Gale-Shapley with men proposing gives the man-optimal M0. Then a DFS: each popped matching M
  is re-checked with the test above. For each man m, s_M(m) is the first woman after M(m) on m's list who prefers m to
  her partner, and next_M(m) is that woman's partner. Every cycle of next_M is an exposed rotation. Eliminating it (each
  m_i takes M(m_{i+1})) gives a neighbour. The visited set is an open-addressing hash table of exact 128-bit keys:
  5 bits per man (woman index + 1), men 1-12 in one 64-bit word and men 13-22 in the other, 2^25 slots. A matching is
  marked when pushed. The count is the number of distinct visited matchings that pass the definition test. Nothing is
  sampled.
- Built-in consistency checks:
  - exactly one sink (a matching with no exposed rotation), and it equals the woman-optimal matching from women-proposing
    Gale-Shapley;
  - every (m, w) pair belongs to at most one rotation (inconsistencies counted);
  - two different maximal chains M0 -> Mz have length equal to the number of distinct rotations.
- Transposed walk: the same walk with women as proposers, starting from the woman-optimal matching. It must visit the
  same set. I compare the count and two order-independent 64-bit checksums (sum and xor of a hash of each 110-bit
  man->woman key).
- Brute force (`--bf`, uses only the definition): backtracking over all bijections (man 1, 2, ... each tries every
  unused woman). A partial assignment is pruned only when it already contains a blocking pair between two assigned
  couples. Every leaf is re-checked with the full definition. Its set is compared with the walk's set by count and both
  checksums.

### Test results of my checker (real output)

Hand-checkable instances:
- t2 is Knuth's order-2 instance (men 12/21, women 21/12). By hand it has 2 stable matchings.
- t3 is an order-3 cyclic instance (men 123/231/312, women 231/312/123). By hand, of the 6 bijections exactly 3 are
  stable: the men's first choices, the men's second choices and the women's first choices. Each of the other three has a
  blocking pair, (m3,w1), (m2,w3) and (m1,w2) respectively.
- t3b has identical lists for everyone and 1 stable matching by hand.
```
$ ./mycount prefs t2.prefs --bf
parsed prefs: comment_lines=1 empty_lines=0 data_lines=4 order n=2; all 4 lists are complete strict permutations of 1..2
man-optimal M0 (GS men propose; woman of man 1..n): 1 2
woman-optimal Mz (GS women propose; woman of man 1..n): 2 1
M0 stable by definition: yes; Mz stable by definition: yes
walk(men side): visited=2 verified_stable=2 unstable=0 edges=1 sinks=1 sink_is_woman_optimal=1 distinct_rotations=1 rotation_inconsistencies=0 stable_pairs=4 max_stack=1 checksum_sum=acbb2ff7284a01ba checksum_xor=803a2fe89729fe3a cpu=0.00s
maximal chains M0->Mz: length(first-cycle rule)=1 ends_at_Mz=yes; length(last-cycle rule)=1 ends_at_Mz=yes; distinct rotations=1
walk(women side, transposed): visited=2 verified_stable=2 unstable=0 edges=1 sinks=1 sink_is_man_optimal=1 distinct_rotations=1 rotation_inconsistencies=0 stable_pairs=4 max_stack=1 checksum_sum=acbb2ff7284a01ba checksum_xor=803a2fe89729fe3a cpu=0.00s; chain length=1 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=2 nodes=5 leaves_failing_recheck=0 checksum_sum=acbb2ff7284a01ba checksum_xor=803a2fe89729fe3a cpu=0.00s
bruteforce set equals walk set: yes
RESULT count=2
$ ./mycount prefs t3.prefs --bf
parsed prefs: comment_lines=1 empty_lines=0 data_lines=6 order n=3; all 6 lists are complete strict permutations of 1..3
man-optimal M0 (GS men propose; woman of man 1..n): 1 2 3
woman-optimal Mz (GS women propose; woman of man 1..n): 3 1 2
M0 stable by definition: yes; Mz stable by definition: yes
walk(men side): visited=3 verified_stable=3 unstable=0 edges=2 sinks=1 sink_is_woman_optimal=1 distinct_rotations=2 rotation_inconsistencies=0 stable_pairs=9 max_stack=1 checksum_sum=cac4d720d8f80259 checksum_xor=353f28ff676007ad cpu=0.00s
maximal chains M0->Mz: length(first-cycle rule)=2 ends_at_Mz=yes; length(last-cycle rule)=2 ends_at_Mz=yes; distinct rotations=2
walk(women side, transposed): visited=3 verified_stable=3 unstable=0 edges=2 sinks=1 sink_is_man_optimal=1 distinct_rotations=2 rotation_inconsistencies=0 stable_pairs=9 max_stack=1 checksum_sum=cac4d720d8f80259 checksum_xor=353f28ff676007ad cpu=0.00s; chain length=2 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=3 nodes=12 leaves_failing_recheck=0 checksum_sum=cac4d720d8f80259 checksum_xor=353f28ff676007ad cpu=0.00s
bruteforce set equals walk set: yes
RESULT count=3
$ ./mycount prefs t3b.prefs --bf
parsed prefs: comment_lines=1 empty_lines=0 data_lines=6 order n=3; all 6 lists are complete strict permutations of 1..3
man-optimal M0 (GS men propose; woman of man 1..n): 1 2 3
woman-optimal Mz (GS women propose; woman of man 1..n): 1 2 3
M0 stable by definition: yes; Mz stable by definition: yes
walk(men side): visited=1 verified_stable=1 unstable=0 edges=0 sinks=1 sink_is_woman_optimal=1 distinct_rotations=0 rotation_inconsistencies=0 stable_pairs=3 max_stack=0 checksum_sum=2e43a4bbf9caef5e checksum_xor=2e43a4bbf9caef5e cpu=0.00s
maximal chains M0->Mz: length(first-cycle rule)=0 ends_at_Mz=yes; length(last-cycle rule)=0 ends_at_Mz=yes; distinct rotations=0
walk(women side, transposed): visited=1 verified_stable=1 unstable=0 edges=0 sinks=1 sink_is_man_optimal=1 distinct_rotations=0 rotation_inconsistencies=0 stable_pairs=3 max_stack=0 checksum_sum=2e43a4bbf9caef5e checksum_xor=2e43a4bbf9caef5e cpu=0.00s; chain length=0 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=1 nodes=8 leaves_failing_recheck=0 checksum_sum=2e43a4bbf9caef5e checksum_xor=2e43a4bbf9caef5e cpu=0.00s
bruteforce set equals walk set: yes
RESULT count=1
```

Published instances in claim/a357271_1.txt (expected counts stated in the file: 81, 365, 1690, 7123, 27059):
```
$ ./mycount table claim/a357271_1.txt 7 --bf --cap=22
parsed table 'order 7 example with 81 SM': order n=7; all 14 rank vectors are permutations of 1..7; MiniZinc rankWomen/rankMen arrays agree with table: yes
man-optimal M0 (GS men propose; woman of man 1..n): 2 1 4 6 5 3 7
woman-optimal Mz (GS women propose; woman of man 1..n): 7 6 5 3 2 4 1
M0 stable by definition: yes; Mz stable by definition: yes
count stated in file for this instance: 81
walk(men side): visited=81 verified_stable=81 unstable=0 edges=158 sinks=1 sink_is_woman_optimal=1 distinct_rotations=18 rotation_inconsistencies=0 stable_pairs=43 max_stack=14 checksum_sum=a09a3d810321ee3f checksum_xor=86a0f076e9ca072f cpu=0.00s
maximal chains M0->Mz: length(first-cycle rule)=18 ends_at_Mz=yes; length(last-cycle rule)=18 ends_at_Mz=yes; distinct rotations=18
walk(women side, transposed): visited=81 verified_stable=81 unstable=0 edges=158 sinks=1 sink_is_man_optimal=1 distinct_rotations=18 rotation_inconsistencies=0 stable_pairs=43 max_stack=16 checksum_sum=a09a3d810321ee3f checksum_xor=86a0f076e9ca072f cpu=0.01s; chain length=18 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=81 nodes=598 leaves_failing_recheck=0 checksum_sum=a09a3d810321ee3f checksum_xor=86a0f076e9ca072f cpu=0.00s
bruteforce set equals walk set: yes
RESULT count=81
$ ./mycount table claim/a357271_1.txt 9 --bf --cap=22
parsed table 'order 9 example with 365 SM': order n=9; all 18 rank vectors are permutations of 1..9; MiniZinc rankWomen/rankMen arrays agree with table: yes
man-optimal M0 (GS men propose; woman of man 1..n): 1 3 2 5 7 6 4 8 9
woman-optimal Mz (GS women propose; woman of man 1..n): 9 8 5 6 4 3 2 1 7
M0 stable by definition: yes; Mz stable by definition: yes
count stated in file for this instance: 365
walk(men side): visited=365 verified_stable=365 unstable=0 edges=897 sinks=1 sink_is_woman_optimal=1 distinct_rotations=32 rotation_inconsistencies=0 stable_pairs=73 max_stack=25 checksum_sum=01feee73d50db8aa checksum_xor=aa585b1f526033ee cpu=0.00s
maximal chains M0->Mz: length(first-cycle rule)=32 ends_at_Mz=yes; length(last-cycle rule)=32 ends_at_Mz=yes; distinct rotations=32
walk(women side, transposed): visited=365 verified_stable=365 unstable=0 edges=897 sinks=1 sink_is_man_optimal=1 distinct_rotations=32 rotation_inconsistencies=0 stable_pairs=73 max_stack=28 checksum_sum=01feee73d50db8aa checksum_xor=aa585b1f526033ee cpu=0.01s; chain length=32 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=365 nodes=4378 leaves_failing_recheck=0 checksum_sum=01feee73d50db8aa checksum_xor=aa585b1f526033ee cpu=0.00s
bruteforce set equals walk set: yes
RESULT count=365
$ ./mycount table claim/a357271_1.txt 11 --bf --cap=22
parsed table 'order 11 example with 1690 SM': order n=11; all 22 rank vectors are permutations of 1..11; MiniZinc rankWomen/rankMen arrays agree with table: yes
man-optimal M0 (GS men propose; woman of man 1..n): 1 3 2 5 4 7 6 8 9 10 11
woman-optimal Mz (GS women propose; woman of man 1..n): 11 10 7 8 5 6 4 3 2 1 9
M0 stable by definition: yes; Mz stable by definition: yes
count stated in file for this instance: 1690
walk(men side): visited=1690 verified_stable=1690 unstable=0 edges=5040 sinks=1 sink_is_woman_optimal=1 distinct_rotations=50 rotation_inconsistencies=0 stable_pairs=111 max_stack=45 checksum_sum=6ea64b6db5f5ff68 checksum_xor=b56e3277a5edad88 cpu=0.00s
maximal chains M0->Mz: length(first-cycle rule)=50 ends_at_Mz=yes; length(last-cycle rule)=50 ends_at_Mz=yes; distinct rotations=50
walk(women side, transposed): visited=1690 verified_stable=1690 unstable=0 edges=5040 sinks=1 sink_is_man_optimal=1 distinct_rotations=50 rotation_inconsistencies=0 stable_pairs=111 max_stack=50 checksum_sum=6ea64b6db5f5ff68 checksum_xor=b56e3277a5edad88 cpu=0.01s; chain length=50 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=1690 nodes=29817 leaves_failing_recheck=0 checksum_sum=6ea64b6db5f5ff68 checksum_xor=b56e3277a5edad88 cpu=0.00s
bruteforce set equals walk set: yes
RESULT count=1690
$ ./mycount table claim/a357271_1.txt 13 --bf --cap=22
parsed table 'order 13 example with 7123 SM': order n=13; all 26 rank vectors are permutations of 1..13; MiniZinc rankWomen/rankMen arrays agree with table: yes
man-optimal M0 (GS men propose; woman of man 1..n): 2 1 4 3 8 5 6 7 9 10 11 12 13
woman-optimal Mz (GS women propose; woman of man 1..n): 13 12 11 8 9 6 7 5 4 3 2 10 1
M0 stable by definition: yes; Mz stable by definition: yes
count stated in file for this instance: 7123
walk(men side): visited=7123 verified_stable=7123 unstable=0 edges=24728 sinks=1 sink_is_woman_optimal=1 distinct_rotations=71 rotation_inconsistencies=0 stable_pairs=155 max_stack=68 checksum_sum=5f48f3c02e63b2dc checksum_xor=d0e1a70e634387d0 cpu=0.01s
maximal chains M0->Mz: length(first-cycle rule)=71 ends_at_Mz=yes; length(last-cycle rule)=71 ends_at_Mz=yes; distinct rotations=71
walk(women side, transposed): visited=7123 verified_stable=7123 unstable=0 edges=24728 sinks=1 sink_is_man_optimal=1 distinct_rotations=71 rotation_inconsistencies=0 stable_pairs=155 max_stack=78 checksum_sum=5f48f3c02e63b2dc checksum_xor=d0e1a70e634387d0 cpu=0.00s; chain length=71 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=7123 nodes=184992 leaves_failing_recheck=0 checksum_sum=5f48f3c02e63b2dc checksum_xor=d0e1a70e634387d0 cpu=0.02s
bruteforce set equals walk set: yes
RESULT count=7123
$ ./mycount table claim/a357271_1.txt 15 --bf --cap=22
parsed table 'order 15 example with 27059 SM': order n=15; all 30 rank vectors are permutations of 1..15; MiniZinc rankWomen/rankMen arrays agree with table: yes
man-optimal M0 (GS men propose; woman of man 1..n): 1 3 2 5 4 9 6 7 8 10 11 12 13 14 15
woman-optimal Mz (GS women propose; woman of man 1..n): 15 14 11 12 7 10 9 8 6 5 4 3 2 1 13
M0 stable by definition: yes; Mz stable by definition: yes
count stated in file for this instance: 27059
walk(men side): visited=27059 verified_stable=27059 unstable=0 edges=106441 sinks=1 sink_is_woman_optimal=1 distinct_rotations=94 rotation_inconsistencies=0 stable_pairs=203 max_stack=96 checksum_sum=1aeb7319a4768f92 checksum_xor=4d1baaf12a783510 cpu=0.03s
maximal chains M0->Mz: length(first-cycle rule)=94 ends_at_Mz=yes; length(last-cycle rule)=94 ends_at_Mz=yes; distinct rotations=94
walk(women side, transposed): visited=27059 verified_stable=27059 unstable=0 edges=106441 sinks=1 sink_is_man_optimal=1 distinct_rotations=94 rotation_inconsistencies=0 stable_pairs=203 max_stack=102 checksum_sum=1aeb7319a4768f92 checksum_xor=4d1baaf12a783510 cpu=0.02s; chain length=94 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
bruteforce(all bijections): count=27059 nodes=1100301 leaves_failing_recheck=0 checksum_sum=1aeb7319a4768f92 checksum_xor=4d1baaf12a783510 cpu=0.12s
bruteforce set equals walk set: yes
RESULT count=27059
```

All eight test counts equal the expected values. For each test, the brute force over all bijections (definition only)
finds exactly the same set as the walk.

## The claimed object: claim/instance_n22.prefs

My parser reads it as order n = 22: 1 comment line and 44 data lines, all 44 lists complete strict permutations of
1..22 (first line of the output below). My counter, run 1 (`./mycount prefs claim/instance_n22.prefs --cap=25`):
```
parsed prefs: comment_lines=1 empty_lines=0 data_lines=44 order n=22; all 44 lists are complete strict permutations of 1..22
man-optimal M0 (GS men propose; woman of man 1..n): 1 2 5 6 3 4 9 10 7 8 13 14 11 12 15 16 17 18 19 20 21 22
woman-optimal Mz (GS women propose; woman of man 1..n): 22 21 20 19 14 13 16 15 10 9 12 11 8 7 6 5 4 3 2 1 18 17
M0 stable by definition: yes; Mz stable by definition: yes
walk(men side): visited=12277568 verified_stable=12277568 unstable=0 edges=80877088 sinks=1 sink_is_woman_optimal=1 distinct_rotations=211 rotation_inconsistencies=0 stable_pairs=444 max_stack=524 checksum_sum=d5aa21eea1ab21a2 checksum_xor=45e1841d702e32da cpu=20.88s
maximal chains M0->Mz: length(first-cycle rule)=211 ends_at_Mz=yes; length(last-cycle rule)=211 ends_at_Mz=yes; distinct rotations=211
walk(women side, transposed): visited=12277568 verified_stable=12277568 unstable=0 edges=80877088 sinks=1 sink_is_man_optimal=1 distinct_rotations=211 rotation_inconsistencies=0 stable_pairs=444 max_stack=416 checksum_sum=d5aa21eea1ab21a2 checksum_xor=45e1841d702e32da cpu=21.67s; chain length=211 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
RESULT count=12277568
```
```
       94.38 real        41.96 user         0.59 sys
           538935296  maximum resident set size
```

Run 2 (determinism), same command:
```
parsed prefs: comment_lines=1 empty_lines=0 data_lines=44 order n=22; all 44 lists are complete strict permutations of 1..22
man-optimal M0 (GS men propose; woman of man 1..n): 1 2 5 6 3 4 9 10 7 8 13 14 11 12 15 16 17 18 19 20 21 22
woman-optimal Mz (GS women propose; woman of man 1..n): 22 21 20 19 14 13 16 15 10 9 12 11 8 7 6 5 4 3 2 1 18 17
M0 stable by definition: yes; Mz stable by definition: yes
walk(men side): visited=12277568 verified_stable=12277568 unstable=0 edges=80877088 sinks=1 sink_is_woman_optimal=1 distinct_rotations=211 rotation_inconsistencies=0 stable_pairs=444 max_stack=524 checksum_sum=d5aa21eea1ab21a2 checksum_xor=45e1841d702e32da cpu=21.13s
maximal chains M0->Mz: length(first-cycle rule)=211 ends_at_Mz=yes; length(last-cycle rule)=211 ends_at_Mz=yes; distinct rotations=211
walk(women side, transposed): visited=12277568 verified_stable=12277568 unstable=0 edges=80877088 sinks=1 sink_is_man_optimal=1 distinct_rotations=211 rotation_inconsistencies=0 stable_pairs=444 max_stack=416 checksum_sum=d5aa21eea1ab21a2 checksum_xor=45e1841d702e32da cpu=20.14s; chain length=211 ends_at_M0=yes
men-side and women-side walks visit the same set: yes
RESULT count=12277568
```
```
       83.26 real        40.69 user         0.58 sys
           538935296  maximum resident set size
```

Determinism: after the `cpu=...s` timing fields are removed, the two output files are byte-identical. Both normalised
files have sha256
428a91bf9eab0a88181d045b7be70dfb45cbd6fa2e610eaa7a89e0a319bf9271 (run 1) and 428a91bf9eab0a88181d045b7be70dfb45cbd6fa2e610eaa7a89e0a319bf9271 (run 2).
That includes the count, the set checksums, the numbers of edges and rotations, and the M0/Mz matchings.

What this shows:
- Lower bound, with no theory needed: 12277568 distinct matchings (distinct exact keys), each re-checked against the
  definition, 0 unstable. So the instance has at least 12277568 stable matchings, which is more than 11221136.
- Exactness: the walk from the man-optimal end and the transposed walk from the woman-optimal end visit the same
  12277568-element set (equal sums and xors). The walk has a single sink, equal to Mz. There are 211 distinct
  rotations, and every maximal chain tested has length 211.

Definition-only brute force over all bijections on n = 22 (no rotation theory at all; capped at 330 s):
```
parsed prefs: comment_lines=1 empty_lines=0 data_lines=44 order n=22; all 44 lists are complete strict permutations of 1..22
man-optimal M0 (GS men propose; woman of man 1..n): 1 2 5 6 3 4 9 10 7 8 13 14 11 12 15 16 17 18 19 20 21 22
woman-optimal Mz (GS women propose; woman of man 1..n): 22 21 20 19 14 13 16 15 10 9 12 11 8 7 6 5 4 3 2 1 18 17
M0 stable by definition: yes; Mz stable by definition: yes
bruteforce(all bijections): count=12277568 nodes=906223507 leaves_failing_recheck=0 checksum_sum=d5aa21eea1ab21a2 checksum_xor=45e1841d702e32da cpu=109.14s
exit=0
Thu Oct 15 02:26:00 +04 2026
```
```
      192.55 real       107.45 user         1.69 sys
             1916928  maximum resident set size
```

The last two lines of that output (exit status and end time) were added by my wrapper.

The brute force examines every bijection (906223507 search nodes). It prunes a partial assignment only when two of its
assigned couples already form a blocking pair, and no completion of such an assignment can be stable. It finds exactly
12277568 stable matchings, with the same two set checksums as both walks (sum d5aa21eea1ab21a2, xor 45e1841d702e32da).
This exact count uses only the definition, with no rotation or lattice theory.

## Author's commands from claim/REPRODUCE.md (run only after my own result, in the scratch copy)

`cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n22.prefs 1` compiled without errors and printed:
```
file: instance_n22.prefs
n: 22
rotations: 211
memo_states: 489227
count_poset: 12277568
seconds_poset: 0.2519
count_lattice_verified: 12277568
seconds_lattice: 35.3829
agree: yes
```
```
       35.89 real        21.07 user         0.50 sys
          1194950656  maximum resident set size
```

`./smcount3 enumerate instance_n22.prefs` printed:
```
count_poset: 12277568
enumerated_ideals: 12277568
unstable_matchings_found: 0
n: 22
rotations: 211
seconds_enumerate: 14.73
agree: yes
```
```
       15.04 real         6.36 user         0.10 sys
           185466880  maximum resident set size
```

`grep -E '^%S|^%T|^%U' A357271.txt` printed:
```
%S A357271 1,2,3,10,16,48,71,268,330,1000,1231,6472,6720,20176,25011,195472,
%T A357271 200832,456300,637336,3419680,3506880,11221136,15481956,126112960,
%U A357271 127885440,262860800,384418176,2000043808
```

I extracted the terms myself (offset line `%O A357271 1,2`, so the first term is a(1)):
```
%O A357271 1,2
a(21) = 3506880
a(22) = 11221136
a(23) = 15481956
number of terms: 28
12277568 > 11221136: 1 (1 = true)
orders present in a357271_1.txt:
order 7 example with 81 SM
order 9 example with 365 SM
order 11 example with 1690 SM
order 13 example with 7123 SM
Order 15 example with 27059 SM
```

`shasum -a 256 instance_n22.prefs a357271_1.txt A357271.txt` printed:
```
213b4ac73bfb4218a4295514410d0d53b6a87f48e8f1462d61382579efdd5b37  instance_n22.prefs
95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47  a357271_1.txt
fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143  A357271.txt
```

## Comparison with the claim

| item | claimed (claim/CLAIM.md, claim/REPRODUCE.md) | found |
|---|---|---|
| order, lists | 22 men, 22 women, complete strict lists | n = 22, 44 lines, each a permutation of 1..22 (my parser) |
| number of stable matchings | 12277568 | 12277568 (my walk, every matching re-checked; transposed walk gives the same set; deterministic over 2 runs; my definition-only brute force over all bijections gives the same set) |
| author `count` | count_poset 12277568, count_lattice_verified 12277568, agree: yes | identical |
| author `enumerate` | enumerated_ideals 12277568, unstable_matchings_found 0, agree: yes | identical (14.73 s, against "about 10 s") |
| bar | a(22) = 11221136 from claim/A357271.txt | a(22) = 11221136 (term 22, offset 1); 12277568 > 11221136 |
| Ong et al. file | improves only n = 7, 9, 11, 13, 15 | claim/a357271_1.txt contains only orders 7, 9, 11, 13, 15 |
| sha256 instance_n22.prefs | 213b4ac73bfb4218a4295514410d0d53b6a87f48e8f1462d61382579efdd5b37 | identical |
| sha256 a357271_1.txt | 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47 | identical |
| sha256 A357271.txt | fd27d7c9ede8781f1fac606a633c62938a7bda778fc04f8557f26278a7c95143 | identical |

Mismatches: none in any claimed value, property or hash. Minor, non-substantive notes:
- REPRODUCE.md says the enumeration takes "about 10 s"; it took 14.73 s here at nice 15.
- The author's `count` command peaked at 1.19 GB resident memory.
- The comment line of claim/instance_n22.prefs names a source file outside the claim folder. It is information only and
  not needed to check the claim.

Outside my remit (not assessed): whether any source beyond the two saved OEIS files has a value above 11221136 for
n = 22, and whether n = 22 is an admissible cell under the charter. I can only confirm that the saved files give
a(22) = 11221136 and that the saved instance file has no order-22 instance.

## Verdict

My own counter, written from the quoted definition, reproduces the exact value 12277568 by two exhaustive methods. The
first is the lattice walk: every visited matching is re-checked, the walks from both ends visit the same set, and two
runs give identical output. The second is a brute force over all bijections that uses only the definition, and it finds
the identical set. My counter also reproduces all five published counts in claim/a357271_1.txt and the
three hand-checked tiny counts, and on each of those the walk and the brute force find the same set. The author's two commands, the bar a(22) = 11221136 and all three sha256 values match
the claim.
pass: true
