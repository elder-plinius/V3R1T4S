Reviewer: CRITERION skeptic (Claude Opus 5.5, general-purpose subagent)
context: subagent (fresh context, given only claim/)

# Claim B, cell f(3,6): criterion reading

Dictionary: Jeffries, arXiv:2604.08790 v1. I fetched the PDF and abstract page myself on 2026-10-29.
- Definition 2.1: a set of m labeled tournaments has S_k if every k-set U has some T_i and a vertex u -> U, so u is outside U.
- Definition 2.2: f(m,k) is the minimum size of V. Read literally it is degenerate for |V| < k, so the bank's n >= k+1 is the intended reading, and Figure 7 agrees with it.
- Figure 7 has rows k and columns m. The cell (k=6, m=3) holds 13, unstarred, so p1's "f(3,6) = 13" is the paper's f(m,k) with m = 3 and property S_6.
- arXiv lists v1 only.

## p1, word by word
- **"an UNSAT certificate (DRAT or LRAT checked by a formally verified checker such as cake_lpr)"**: met, with caveats.
  - There are 2,871 jobs: 62 cover lemmas (1 root, 21 level-2, 40 level-3) and 2,809 leaves (126 at level 1, 114 at level 2, 2,569 at level 3). Each has a VERIFIED ledger row. VERIFIED requires cake_lpr's exact stdout `s VERIFIED UNSAT` and an unchanged CNF sha256.
  - The proof files were deleted, so the package holds a reproducible certificate, not the files. A full re-check costs about 96,500 CPU seconds.
  - I regenerated and checked 4 jobs:
    - one level-1 leaf (9_4_1, CNF sha256 checked only)
    - COVER2/9_1_2
    - COVER3/10_0_1_0-0-1-0
    - leaf 7_0_0_0-0-0-0 (level 2)
    - leaf 8_0_1_0-0-1-0_L3_6_1_1 (level 3)

    Every checked job gave `s VERIFIED UNSAT`, and every CNF sha256 equals its ledger entry. The root lemma COVER1 (4.3 GB of memory) is covered only by the ledger and validation.out; I did not re-run it.
  - This is a 0.15% sample. The rest rests on the ledger and assemble.out (2,871/2,871).
- **"for a CNF encoding of 'three tournaments on 12 vertices with every 6-subset dominated'"**: met in cube-and-conquer form.
  - The tree has three levels. Each refined node has a cake_lpr-certified cover lemma. Its meaning rests on certlib.cover_cnf, which I read: the child CNF is asserted to be the parent CNF plus units plus regenerated seqcounter clauses, the counters are exact, and the child clauses are (not L_j) or (a row exceeds its bound).
  - The tree enumerates all children of every refined node (l2_children, l3_children). The ledgers only decide which nodes are refined, so they cannot drop a child.
  - As for claim A: under a strict "one CNF, one proof" reading this is not met. Under the standard reading it is.
- **"with symmetry breaking proved sound"**: met.
  - The argument spans four short texts: L1_SOUNDNESS_NOTE (level 1), V2_PREREG.v2 (T_2/T_3 order: the T_3 degree of 0 is <= a+b), L2_PREREG (level 2: the T_3 row of 0 is a prefix in each of 4 blocks, with sum(c) <= a+b under v2), and L3_SOUNDNESS_L3 (level 3: a pivot in the largest cell C of vertex 0's three rows).
  - I checked each step against Definition 2.1. Every relabelling is a vertex permutation applied to all three tournaments, or a permutation of tournament indices. Each later relabelling fixes vertex 0's rows as sets, and every degree, so it keeps the parent CNF.
  - The level-3 range e >= ceil((z-1)/2) = z//2 is correct.
  - The NF clauses in cover_cnf match the texts: prefix clauses, block-wise prefix clauses, le_cmp maximality, and the v2 comparison.
  - No counting fact is assumed. The d and e ranges are derived inside the certified lemmas.
- **"the encoding's correctness argued in a short note that a skeptic checks against Definition 2.2"**: met.
  - The encoder is the same as for f(2,5), and L1_SOUNDNESS_NOTE section 1 argues its correctness.
  - My own structural decoder ran on the regenerated (3,6,12) leaf 9_4_1, whose sha256 matches the ledger. It found:
    - exactly 924 = C(12,6) OR-clauses, each with 3*6 = 18 aux variables, one per (t, v not in U);
    - each aux implies exactly v -> U in one tournament, and the aux variables occur nowhere else;
    - the unit clauses equal the cube's rows.
  - The soundness argument is spread over four files plus DESIGN.md, and the L1 note's section 5 is stale. Together they are still short (about 10 KB), so I accept "a short note".

## Notation, upper bound, n >= k+1
- The witness `witnesses/witness_cube_m3k6n13_d11a7b0.json` was checked with my own code. It has 3 distinct tournaments on 13 vertices and satisfies the tournament axioms. All 1,716 6-subsets are dominated.
- n = 13 >= 7.
- This equals the published bar, so it is not an improvement. It is only needed for the exact value.

## Hidden quantifiers
- **"f(3,6) = 13" also needs that no S_6 triple exists on 7..11 vertices.** The package does not say so.
  - It follows from monotonicity in n, which I checked: append a vertex beaten by everyone in every tournament.
  - The bank's p1 wording already treats the 12-vertex certificate as the proof.
- **Trusted, not certified:** the written normal-form arguments (checked above), certlib.cover_cnf and the tree's completeness (Python), cake_lpr's C wrapper (its hash differs from the upstream list), the toolchain, and the OS.
- **Subsumption:** the cell is unstarred in Figure 7 and in the dissertation per TABLE_RECORD.md, and arXiv shows v1 only. Not subsumed.

## Null models
Shared pipeline, run on (2,5) jobs:
- A tampered LRAT is rejected.
- A fake one-line proof is rejected.
- A real proof replayed against a satisfiable cube is rejected.
- The satisfiable cube is solved SAT.

validation.out reports the same controls on (3,6) objects, including the satisfiable (3,6,13) cube 11_7_0 checked against an L3 proof.

confirmed_scope: There is no triple of tournaments on 12 vertices with property S_6 (Jeffries Def. 2.1); this is shown by a three-level cube-and-conquer certificate of 2,871 cake_lpr-checked LRAT proofs (a ledger records all 2,871; I regenerated 5 CNFs and checked 4 of them, all matching), under the written normal-form arguments and the Python cover-lemma construction; with the 13-vertex witness and monotonicity in n, this gives f(3,6) = 13 as partial win p1.

pass: true
