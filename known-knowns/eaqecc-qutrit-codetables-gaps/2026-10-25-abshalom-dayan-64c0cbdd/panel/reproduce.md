# REPRODUCE skeptic verdict: [[28,7,13;9]]_3 (object/eaqecc_28_7_13_9.json)

**Bottom line: PASS.** I wrote my own checker before reading the author's code. From the matrix S alone it gives
s = 30, c = 9, k = 7 and d = 13 exactly. The search is exhaustive: all C(28,12) = 30421755 position 12-subsets
were checked with no pruning, and none holds a vector of span(S)^perp outside the isotropic part, so d >= 13. Of
the C(28,13) = 37442160 13-subsets, 9036 hold such a vector, so d <= 13. The checked weight-13 witnesses confirm
the upper bound. The author's REPRODUCE.md steps 1-6 all printed exactly the values that REPRODUCE.md states. The
author's method-A list of deficient 15-subsets is, after taking complements, exactly my list of 9036 bad
13-subsets. I also re-derived the author's no-search proof (step 6) and found it valid. Every run was
deterministic. Not in scope here: the live table check (step 7, d_lower 12 < 13 <= d_upper 18) and novelty. The
other skeptics cover those.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

Run: started 2026-10-25 00:12:36 UTC, author steps finished 00:22:15 UTC (from `date -u`).
Object: claim/object/eaqecc_28_7_13_9.json, sha256 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78
(matches CLAIM.md). The files in claim/ were hashed before and after all runs and were unchanged. The author's
steps ran in a copy, author_run/.

## Definition checked (quoted from CLAIM.md, success criterion)

> "with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors
> in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC
> definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and
> d <= d_upper. Results for c = 0 are excluded"

Conventions from the object JSON: rows of S are (x|z) over GF(3) with 2n = 56 columns, and
<(x|z),(x'|z')> = x.z' - z.x'. The weight is the symplectic weight #{i : (x_i, z_i) != (0,0)}.

## What I computed and how (mine/)

- `mine/ea_prep.py` (Python, own GF(3) elimination, reads only "S" and "n"):
  - s = rank S.
  - M = S J S^T and c = rank(M)/2, asserting that rank M is even.
  - k = n - s + c.
  - N = span(S)^perp as the null space of the functionals (-z|x).
  - I = {aS : aM = 0}. dim I is cross-checked against dim U + dim V - dim(U+V) and against s - rank M. Each basis
    vector of I is checked to lie in N and in span S.
  - A basis H of N whose first dim I rows span I.
  - Output: `rows=30 n=28 s=rank(S)=30 rank(SJS^T)=18 c=9 k=n-s+c=7 dim_N=26 dim_I=12 2k=14`.
    The 30 rows are independent (s = 30 = row count), c = 9 >= 1, and these match the JSON's n = 28, k = 7, c = 9.
- `mine/ea_subset.c` (C, own bit-sliced GF(3) echelon code): an exact test over position subsets.
  - Write v = aH. v lies in N \ I iff the coordinates of a outside the I block are not all zero.
  - Some such v is supported on T iff ker(pi_I) is not contained in U = span{columns of H at the complement Z of T}.
  - The test counts the echelon pivots that land in the non-I coordinates (the I coordinates are ordered first).
  - It is a DFS over all complements Z. With prune=1, a partial Z that is already good counts all its completions
    at once, using the binomial coefficient (valid because U only grows as Z grows). With prune=0, every leaf is
    visited.
  - It checks that good + bad = C(n,W).
- Results on the object:

| W | prune | examined | leaves visited | sets T holding a vector of N \ I |
|---|---|---|---|---|
| 12 | 1 | 30421755 | 7125 | 0 |
| 12 | 0 | 30421755 | 30421755 | **0** -> d >= 13 |
| 13 | 1 | 37442160 | 253319 | 9036 |
| 13 | 0 | 37442160 | 37442160 | **9036** -> d <= 13 |

  The pruned and unpruned bad lists for W = 13 are identical: the sha256 of the sorted list is
  9b084ca14d23b578f7a6a4352f32a29975cc83ab9f95d34cafc04d06f2f0b793 for both runs and for a rerun. Each run took
  at most 13.64 s and peaked at 1.46 MB resident memory (from `/usr/bin/time -l`).
- `mine/witness_and_negative.py` checks witnesses directly from S, with plain arithmetic. For 55 of the bad
  13-subsets (the first 5 plus 50 chosen at random with seed 7), it solves for the vectors of span(S)^perp
  supported on T and picks one outside span(S). Each one has symplectic weight 13, is orthogonal to all 30 rows and
  is not in span S (`witnesses_checked=55 all_weight_13_outside_isotropic=True`). So d = 13 exactly.
- `mine/gf9_conventions.py` (extra check): S equals phi(D9) as stated (rows phi(r), phi(w r) in order), G9 is
  Hermitian-orthogonal to D9, and rank G9 = 13, rank D9 = 15 over GF(9).

## Tests of my checker

- **Brute force, random S** (`mine/test_bruteforce.py 80 random`, seed 20261025): n = 2..7, and every fifth case
  has a deliberately dependent row. On each case I enumerated all vectors of N, checked |N| = 3^(2n-s) by
  scanning all 3^(2n) vectors when 2n <= 12, and checked |I| = 3^dimI. I computed d and, for every W, the exact
  number of W-subsets that contain the support of some vector in N \ I. These were compared with ea_subset at
  every W, both with prune 0 and prune 1. Result: 79 cases, 79 OK, FAILURES=0. The brute-force d values were
  1 (26 cases), 2 (23), 3 (10), 4 (4), and N contained in I (16). A rerun was byte-identical.
- **Brute force, near-isotropic S** (`isotropic` mode, n = 4..8, larger I): 56 cases, 56 OK, FAILURES=0. Here d was
  1 (7), 2 (16), 3 (15), 4 (4), and N contained in I (14).
- **Seeded negative** (`mine/neg_planted12.json`): I planted a weight-12 vector v on T = 0,3,5,6,8,9,11,13,18,23,26,27
  into the dual by mapping each row r to r - (<r,v>/<u,v>)u, which leaves v outside span. My pipeline then reported
  c = 10, k = 8, dim_I = 10. At W = 12 it found 16861 bad sets, including the planted T exactly, so the checker
  rejects it. At W = 11 it found 1854 bad sets, so the perturbation lowered d further still. Either way, the
  checker does not miss low-weight vectors.

## Author's REPRODUCE.md steps 1-6 (run in a copy, author_run/)

| Step | REPRODUCE.md expects | Printed | Match |
|---|---|---|---|
| 1 rebuild | `E_15 scaled_cols=[] [28,13] hull=6 -> [[28,7,?;9]]  S 30x56  D9 15x28`; sha256 64c0cbdd...0c78 | identical line; rebuilt.json sha256 64c0cbddea11688f7cc06644d8751c2f62328aae74f7f149b89164a73dea0c78, byte-identical to the object (two runs) | yes |
| 2 prep | `n=28 s=30 c=9 k=7 dim_N=26 dim_I=12 N_closed_under_w=True`, `kappa=13` | identical, plus `kappa=13 (2*kappa == dim_N: True)` | yes |
| 2 m=16 | deficient=0 in all parts; subsets 18746445, 8232114, 3443196 (sum 30421755) | 18746445 / 8232114 / 3443196, deficient 0/0/0; sum 30421755 = C(28,16) | yes |
| 2 m=15 | deficient 5376, 2541, 1119 (9036) | 5376 / 2541 / 1119 (subsets 22138911 / 10514331 / 4788918, sum 37442160) | yes |
| 3a | `weight=13 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False` | identical | yes |
| 3b | `symplectic_weight=13 orthogonal_to_all_rows_of_S=True in_span_S=False` | identical, support 12,13,14,18..27 | yes |
| 4 prep | `n=28 s=30 c=9 k=7 dim_isotropic=12 dim_dual=26` | identical | yes |
| 4 W=12 | examined=10140585 per part, with_vector_outside_isotropic=0 | 10140585 x 3 = 30421755, 0/0/0 | yes |
| 4 W=13 | 2989, 3104, 2943 (9036) | 2989 / 3104 / 2943 (examined 12480720 x 3 = 37442160) | yes |
| 5 BZ | `K=13 n=28 d=13 sets=13,13,2 maxw=6 words=185659383` + witness | identical; witness 0..0 1 1 1 0 0 0 7 7 7 3 3 3 1 1 1 4 (0.86 s) | yes |
| 6 | `RESULT: d_EA = 13 exactly (no distance search): True` | identical (rank S=30, rank SJS^T=18, c=9, k=7, span(S)^perp = phi(E): True) | yes |

Cross-checks between the author's outputs and mine:

- Method A's deficient 15-subsets, listed with `infoset 15 p 3 list 100000`, give 9036 distinct complements. They
  equal my set of 9036 bad 13-subsets exactly.
- The three `first=` sets from step 4 are all in my bad list.
- I re-verified the vectors from step 3 and step 5 with my own code. Both have symplectic weight 13, are
  orthogonal to S and are not in span S. Their supports are in my bad list.
- Rerunning step 1, step 4 (W=13, part 1) and step 5 gave identical output.
- The author's C programs print computed variables. No expected value is hard-coded in checkers/ or rebuild/
  (checked with grep).

## Proof steps re-derived (step 6, onepoint_check.py)

Here E is the extended one-point code of the Hermitian curve y^3 + y = x^4 over GF(9), with m = 15. The curve has
genus 3, 27 affine rational points (asserted in the script) and a single point at infinity, P_inf. The
monomials x^i y^j with j <= 2 have distinct pole orders 3i + 4j. Those with 3i + 4j <= 15 are the 13 semigroup
values 0,3,4,6,...,15 (the gaps are 1, 2 and 5), and 15 - g + 1 = 13 agrees. The top monomial x^5 is unique, so
dim L(15 P_inf) = 13.

I checked the bound d(E) >= 28 - m = 13 case by case:

- **Top coefficient nonzero.** The pole order of f is exactly 15, so f has 15 zeros counted with multiplicity, all
  of them affine. That leaves at least 12 affine nonzeros, and the 28th coordinate adds 1: weight >= 13.
- **Top coefficient zero.** The pole order is <= 14, so there are at least 13 affine nonzeros: weight >= 13.

From the bound to the claim:

- phi(E) is orthogonal to S and has GF(3) dimension 26 = 2n - s, so phi(E) = span(S)^perp. Symplectic weight on
  phi(E) equals Hamming weight on E, so d_EA >= d(E) >= 13.
- The weight-13 witness lies in E and outside span S, so d_EA = 13.

The argument is sound, and my exhaustive search reaches the same value independently.

## Scope notes

- Not run: step 7 (the network fetch of the live table) and novelty. The other two skeptics cover them.
- The bound d <= d_upper = 18 and d_lower = 12 come from the table and were not checked here.
- Machine use: at most 2 CPU-heavy processes at a time, all under nice and alarm caps. Peak memory was below 25 MB in every run measured with `/usr/bin/time -l`.
  Everything was written inside the work folder.

pass: true
