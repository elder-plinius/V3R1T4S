# Research charter v1 (2026-10-24) (published part: methods only)

## Quarries

1. **id:** cap-set-dim7-dim8
   **question:** Is there a cap set (a set of distinct vectors in {0,1,2}^n with no three distinct members summing to zero mod 3) of size at least 237 in F_3^7 (it cannot exceed 288), or of size at least 513 in F_3^8?
   **shape:** record (table cell); partial wins are a larger cap in F_3^9 or F_3^10, a stronger cap-set capacity lower bound with an explicit admissible set, or a DRAT-checked proof of r(7) <= 287.
   **where defined:** bank entry `cap-set-dim7-dim8`; arXiv:2508.07932; arXiv:2206.09804; OEIS A090245. The bank's attributions: 236 for n=7 (Calderbank-Fishburn lower bound, Thackeray's 2022 upper bound 288), 512 for n=8 (FunSearch 2023, matched by X-evolve 2025).
   **status to confirm first:** OEIS A090245, the Wikipedia cap-set page and a fresh arXiv search for the best known size in each dimension (bank check was 2026-10-03: 236 and 512); affine and projective caps are different problems with different tables.
   **why us:** unions of orbits under a prescribed subgroup of AGL(n,3) with an exact maximum independent selection of orbits in CP-SAT, twisted gluing of product and doubling constructions, SAT or ILP "swap k out, k+1 in" moves from the 236-cap, and priority-function evolution with a better score. The bank warns that 236 has stood for decades.
   **weight:** 5 · **wild:** no

2. **id:** small-ramsey-lower-bounds
   **question:** For some (s, t), is there a graph on N vertices, with no clique of size s and no independent set of size t, certified exactly by two independent methods, such that N+1 exceeds the best known lower bound for R(s,t) (or for a multicolour analogue)?
   **shape:** record (table cell); off by one, since a graph on N vertices proves R(s,t) >= N+1. Partial wins: a multicolour classical Ramsey record, or the exact value of a circulant Ramsey number R_C(4,k) or R_C(5,k) with no published value.
   **where defined:** bank entry `small-ramsey-lower-bounds`; Radziszowski's dynamic survey DS1; arXiv:2603.09172 (AlphaEvolve); ScaleAutoResearch-Ramsey; arXiv:2608.18169 (Yu); arXiv:2608.18769 (circulant Ramsey numbers); arXiv:2610.12122 (Cremer).
   **status to confirm first:** the maximum over DS1's latest revision and every 2026 paper or repository, found by a fresh search for the specific R(s,t): many cells moved in March to October 2026 (R(4,16) to R(4,20) by AlphaEvolve and then by Yu's order-251 circulants, which also move R(4,21); Cremer: R(6,8) >= 135 and R(8,10) >= 345). The bank did not open DS1 itself, and R_C(3,n) for n = 13..20 is exactly known, so plain circulant search there is exhausted.
   **why us:** cyclotomic circulant and block-circulant graphs on primes and near-primes, one-vertex extension of a record graph by SAT, two-orbit (bi-circulant) graphs through the projected-distance integer program, tabu search on edge flips from Paley-type seeds, and multicolour cells that AI pipelines have not swept; every graph is checked by an exact bitset branch-and-bound and by a SAT UNSAT proof.
   **weight:** 4 · **wild:** no

3. **id:** kissing-number-dims-25-48
   **question:** In some dimension d from 25 to 48, are there K integer-coordinate vectors of identical squared norm, every pair with inner product at most half of it, with K larger than B(d), the maximum over every dimension d' <= d of every source (Cohn's table, the listed arXiv papers, the named public repositories, any other source a fresh search finds, and the constant-weight-code formula for d = 32..39)?
   **shape:** record (table cell); beating Cohn's table alone is not a result, a count from a formula alone is not a certificate, and an unreadable source makes the verdict PENDING TABLE CHECK. Partial win: a verified improved upper bound.
   **where defined:** bank entry `kissing-number-dims-25-48`; cohn.mit.edu/kissing-numbers; arXiv:2609.35051 (Yang et al.), arXiv:2609.21591, arXiv:2608.13906, arXiv:2607.20359, arXiv:2511.13391, arXiv:2312.05121; repositories alexlegeartis/KissingNumbers, Oxelra-AI/Qiushi-Engine-Kissing-Number-Research, wcgbg/sphere-packing, CDM1619/PackingStar, k-nic/kissing_d25-31, Felpix-Studios/kissing-number; Brouwer's A(n,d,w) table for the Edel-Rains-Sloane value 2^17 + 2^7*A(d,8,8) + 2d(d-1).
   **status to confirm first:** every source above, read live with an honest client, then the maximum over d' <= d: Cohn's table is stale for most d from 25 to 47 and many records live only in repositories that update within days. Orientation only, never the bar: Cohn on 2026-10-20 lists d33 364736 and d34 384836, derived from the codes A(33,8,8) >= 1809 and A(34,8,8) >= 1965 in this repository's constant-weight-codes directory.
   **why us:** explicit vector sets built from machine-verified constant-weight codes (each extra codeword adds 128 to the kissing number), plateau-walk local search for larger A(d,8,8), and cross-section and antipode constructions for d from 40 to 47; every set is regenerated from its code and checked in exact integers.
   **weight:** 2 · **wild:** no

4. **id:** conway-99-graph
   **question:** Does a strongly regular graph with parameters (99,14,1,2) exist, that is, a 99-vertex graph in which every edge lies in exactly one triangle and every non-adjacent pair has exactly two common neighbours?
   **shape:** existence (or a certified non-existence); confirmed only by an explicit 99 x 99 adjacency matrix with A^2 = 14I + A + 2(J - I - A) checked in integers. Non-existence needs a formal proof or a reproducible exhaustive computation with DRAT or LRAT certificates and an independently re-derived encoding. Near misses are never results. Partial wins are certified exclusions of specific automorphisms.
   **where defined:** bank entry `conway-99-graph`; arXiv:2608.11211; arXiv:2308.02978; hunting-srg99 repository.
   **status to confirm first:** the literature on forced structure and excluded automorphism orders (arXiv:2608.11211, arXiv:2308.02978 and their refinements, bank check 2026-10-03), re-searched before claiming that an automorphism case is new.
   **why us:** prescribed automorphisms not yet excluded (orders 3 and 11) solved as orbit-matrix SAT, exact cover for the partial-geometry structure of the 693 triangles, and cube-and-conquer with a different encoding than the literature's; every UNSAT claim carries a proof checked by drat-trim or cake_lpr.
   **weight:** 1 · **wild:** no

5. **id:** moore-graph-57
   **question:** Does a 57-regular graph on 3250 vertices with diameter 2 and girth 5 exist, that is, a graph with A^2 + A - 56I = J?
   **shape:** existence (or a certified non-existence); confirmed only by an explicit adjacency list checked exactly in integers, and a non-existence argument counts only if formalised in Lean or Isabelle and machine-checked. Partial wins: a computer-verified exclusion of an automorphism of a specific odd prime order not already in the literature, or an independent machine-checked verification of the no-involutions theorem.
   **where defined:** bank entry `moore-graph-57`; arXiv:2606.29183; Symmetry 16(12):1563 (MDPI, 2024); arXiv:2210.09577.
   **status to confirm first:** arXiv:2606.29183 and its references (bank check 2026-10-03); the no-involutions preprint is unrefereed, so anything built on it states that dependency. The history of this problem is full of incorrect non-existence claims.
   **why us:** fixed-subgraph, eigenvalue-multiplicity (1729 and 1520) and trace arguments pushed to automorphisms of order 3, 5, 7 and 11, and orbit-matrix search with CP-SAT for large odd-order semiregular groups, all in exact arithmetic.
   **weight:** 1 · **wild:** yes

## Lenses

1. **key:** constructor · **title:** Build from structure · **skeptic:** no
   Choose a structured family (restrictions of larger schemes, group orbits, lattices from codes, symmetric seeds) where the objective has a fast exact evaluator, reason about which parameters could beat the record, then search only that family. Dead when the family's best provably cannot reach the record.

2. **key:** optimizer · **title:** Warm-start from the record · **skeptic:** no
   Start from the current record object, perturb and polish with an exact objective (flip-graph walks, active-set or SLSQP polishing followed by exact certification). Dead when long runs plateau at the record across three seeds.

3. **key:** solver · **title:** Let a solver argue · **skeptic:** no
   Encode the cell as SAT, ILP or a polynomial system with symmetry breaking you can justify, and keep every certificate. Dead when encodings time out at sizes below what a record needs.

4. **key:** object-as-data · **title:** Read the record holder · **skeptic:** no
   Treat the current best object as data: invariants, symmetries, near-misses and slack; find regularities its authors did not use. Dead when local moves around the record all lose.

5. **key:** evaluator-first · **title:** Exact, fast, twice · **skeptic:** no
   Spend the first hour on a fast exact evaluator and a second independent one; test both on the record holder and on seeded flawed objects. Floats only for search.

6. **key:** already-settled · **title:** Prove it is not new · **skeptic:** yes
   Assume the cell is already beaten: read the live table, its pending submissions, the public repositories the bank names, arXiv for the last 6 months, this repo's TROPHY_CASE.md, known-knowns and open pull requests. Dead (for the cell) when it is listed or claimed.

## Heuristics

1. Exact arithmetic or an interval certificate decides; floats only search.
2. Two independent exact checkers before believing any object.
3. Seed from the record holder.
4. Prefer cells where the checker runs in seconds.
5. A tie is not a record; one cell per claim.
6. Re-read the live cell right before claiming.
7. Compare against the sorted or canonical form of the cell (permutations, rotations, reflections, isomorphism).
8. Pick cells the active record-chasers are not working this week.

## Kill criteria

1. The two exact checkers disagree and it cannot be resolved.
2. The live cell, or a public repository or paper the bank names, already equals or beats the object.
3. The cell is improved in this repo, an open pull request, a sibling workspace or the literature.
4. Search plateaus at the record across three distinct seeds.
5. A non-existence or exclusion argument has no formal proof or checked DRAT or LRAT certificate.
6. A claimed exhaustive search turns out capped, or the exact check cannot run at the cell's size on one laptop.
