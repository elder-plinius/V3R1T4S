Reviewer: REPRODUCE skeptic (Claude Opus 5.5, general-purpose subagent)
context: subagent (fresh context, given only claim/)

# Claim B: f(3,6) = 13 (no S_6 triple on 12 vertices; S_6 triple on 13 vertices)

Scope: only files in claim/ and the arXiv source (PDF fetched 2026-10-29; abstract page lists [v1] only, "Submitted on 9 Apr
2026"). Scratch work in a private temp directory; proof files deleted after each job; nothing written inside claim/.

## 1. Definition at the source (arXiv:2604.08790, p. 4)
> Definition 2.1 (Schütte's property for sets of tournaments). Let τ = {T1, ..., Tm} be a set of m labeled tournaments each on the
> same vertex set V(τ). The set τ has Schütte's property Sk if for every set of k vertices U ⊂ V(τ), there is a tournament Ti ∈ τ
> and a vertex u ∈ V(τ) such that u → U in Ti.

> Definition 2.2. For m, k ∈ N, define f(m, k) to be the minimum size of a vertex set V such that there is an Sk set of m
> tournaments on V.

Figure 7: f(3,6) ≤ 13 unstarred; f(3,5) = 9* starred.

## 2. Own checker and encoder (written before reading package code)
Same checker and encoder as in my report for claim A (A/reproduce.md, section 2; validated there on f(1,2), f(2,2), f(2,3),
f(2,4) SAT/UNSAT at the starred values and f(3,5) SAT at 9).

    witnesses/witness_cube_m3k6n13_d11a7b0.json: m=3 k=6 n=13 subsets=1716 undominated=0 -> S_k OK
    (sha256 74c242cc84021da5d258185ac2e9d72b392258c9cb2d263333362156e5c062a5)

## 3. Claimant's encoder vs mine
Definition 2.2 part of certify/encoder/cube.py is identical to mine, clause by clause:

    m3k6n12 (6, 0, 0)   mine 100716 theirs-def 100716 prefix identical: True def-subset identical: True other clauses use def aux: False
    m3k6n12 (11, 11, 0) mine 100716 theirs-def 100716 prefix identical: True def-subset identical: True other clauses use def aux: False

Read line by line: cube.py (level 1 units, at-most-d on all 36 rows, v2 bound count(T_3,0) ≤ a+b with units if a+b = 0, level-2
T_3 prefix units per block) and cube3.py (cells, pivot cell = largest, ties to the smallest first vertex; level-3 units for the
pivot s's T_1 and T_2 rows inside C; at-most-e on T_1 rows inside C; e from z//2 = ceil((z-1)/2)). pysat seqcounter tested by me:
L = 1..12, b = 1..L+1, SAT iff count ≤ b, 98,304 cases PASS. All row lengths here are ≤ 11.

## 4. Relabelling lemmas re-derived
- L1 (L1_SOUNDNESS_NOTE.md) and v2 (V2_PREREG.v2.md): max-out-degree pair to (T_1, 0), d ≥ ceil(11/2) = 6; order T_2, T_3 so
  deg_T2(0) ≥ deg_T3(0) (a tournament permutation, independent of the vertex relabelling); prefixes inside A and B. Correct.
- L2 (L2_PREREG.md): permutations inside the four blocks {1..a},{a+1..d},{d+1..d+b},{d+b+1..11} fix vertex 0's T_1 and T_2 rows as
  sets and all degrees, so T_3's row of 0 can be made a prefix in each block; sum(c) ≤ a+b by v2. Correct.
- L3 (L3_SOUNDNESS_L3.md): cells (block prefix/suffix pieces) are intervals on which all three rows of 0 are constant; any
  permutation of a cell preserves the parent CNF; pivot of max T_1 out-degree inside C, e ≥ floor(z/2); then prefixes inside A', B'.
  Correct.
Cover lemmas (certify/certlib.py cover_cnf, read line by line): level 1 = exact counters + NF + per-child (¬units ∨ some bound
exceeded), including the v2 comparison count(T_3,0) ≤ count(T_2,0) and the v2 at-most row; level 2 = parent non-Def-2.2 clauses +
T_3 prefix NF + per-child ¬units; level 3 = parent non-Def-2.2 clauses + counters on T_1 rows inside C + NF + per-child
(¬units ∨ some row in C has count ≥ e+1). Each expresses the corresponding lemma; structural asserts (child = parent + units on
arc vars + exactly the regenerated seqcounter clauses) ran without failure for the 7 cover lemmas I rebuilt.

Tree completeness (my own enumeration, my own cell/pivot code, against jobs.tsv): COVER1; 147 level-1 cubes = 126 leaves + 21
COVER2; their children = 114 level-2 leaves + 40 COVER3; their children = 2,569 level-3 leaves (smallest pivot cell size 6). Every
one of the 2,871 jobs reached exactly once, no extra or missing jobs; ledger.tsv has exactly one row per job, all `VERIFIED`.

## 5. Reproduction: spot check only
A full re-run is about 96,500 CPU-s (ledger: solve 53,197 + convert 38,431 + check 4,876 s; largest solve 1,412 s), out of my budget.
I re-ran a seeded random sample (seed 20261029) of 17 of the 2,871 jobs with the REPRODUCE.md pipeline (solve.py, drat-trim,
my own rebuilt cake_lpr, see A/reproduce.md section 5), computing each CNF sha256 myself and comparing with ledger.tsv column 5:

    m3k6n12/COVER1                        cnf 024616bf...0216  SHA_MATCH  cake_lpr "s VERIFIED UNSAT"
    m3k6n12/COVER2/9_0_1, 8_1_1, 7_0_3    SHA_MATCH  "s VERIFIED UNSAT" (each)
    m3k6n12/COVER3/8_1_1_1-0-0-0, 8_1_1_0-0-0-0, 9_0_1_0-0-1-0    SHA_MATCH  "s VERIFIED UNSAT" (each)
    level-1 leaves 11_8_0, 8_8_0, 9_4_1   SHA_MATCH  "s VERIFIED UNSAT" (each)
    level-2 leaves 8_1_2_1-2-0-0, 9_1_2_1-1-0-0    SHA_MATCH  "s VERIFIED UNSAT" (each)
    level-3 leaves 8_0_2_0-1-0-1_L3_3_1_3, 8_1_2_1-0-0-0_L3_5_3_0, 8_0_2_0-0-1-0_L3_4_3_0,
                   9_1_1_0-0-0-0_L3_4_4_3, 10_1_1_0-0-0-0_L3_4_0_3    SHA_MATCH  "s VERIFIED UNSAT" (each)
    17/17 UNSAT, 17/17 SHA_MATCH, 17/17 drat-trim s VERIFIED, 17/17 cake_lpr rc=0 with stdout exactly "s VERIFIED UNSAT"
    wall 124 s, 220 user-s

Four further sampled leaves (7_3_2, 8_1_1_1-0-0-1, 7_0_1_0-1-0-0, 8_0_2_0-1-0-0_L3_4_0_1; about 400 ledger CPU-s) were dropped to
stay within budget after the full cell-A run. Negative control: the leaf 11_8_0 with one unit clause removed is rejected by my
cake_lpr ("c Checking failed at line: 1 ...", rc=0).

## 6. What was not reproduced
- 2,854 of 2,871 jobs (including all 18 remaining COVER2, 37 remaining COVER3 lemmas and all expensive leaves) were not re-run by
  me; their VERIFIED status rests on the claimant's ledger.
- I did not rebuild the other 2,854 CNFs to compare hashes (certify/assemble.py writes inside claim/logs/certify-work/, and an
  equivalent rebuild was out of budget); certify/assemble.out's "2871 VERIFIED with matching CNF sha256" is the claimant's output.
- Trusted as for A: CakeML proof of cake_lpr, basis_ffi.c, compiler, OS.
- Housekeeping: certify/__pycache__ directories appeared inside claim/ during my session from a process that was not mine (all my
  Python ran with -I -B).

No mismatch was found in anything I checked. But per the panel rule, for an exhaustive search a sample is a spot check and cannot
pass; 17 of 2,871 jobs is a sample.
pass: false
