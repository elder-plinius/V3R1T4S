# Reproduce skeptic: [[28,6,12;6]]_3 claim

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line:** every claimed value checks out exactly: n = 28, k = 6, c = 6, d = 12. I got them from S alone with two exact methods of my own that work differently. The author's REPRODUCE.md steps 1 to 4 print exactly what REPRODUCE.md says they will print. The rebuild is byte-identical (sha256 51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573). Every run is deterministic. I found no mismatch, no missing object and no non-determinism.

I did **not** check the live table (d_lower = 11, d_upper = 17 for (n,k,c) = (28,6,6), and the re-fetch the criterion asks for) or novelty. Other skeptics cover those. I also did not run REPRODUCE.md step 5 (the network fetch).

## Definition (quoted from claim/CLAIM.md, success criterion)

> "with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl)"

Conventions, from the object's `S_convention` field: S rows are (x|z) over GF(3), and <(x|z),(x'|z')> = x.z' - z.x'. Weight means symplectic weight, the number of positions i with (x_i, z_i) != (0,0).

## Order of work

1. I read claim/CLAIM.md and the object JSON's convention fields.
2. I wrote and tested my own checker (folder mine/).
3. I ran it on the claim and kept its numbers.
4. Only then did I open claim/REPRODUCE.md, claim/checkers/ and claim/rebuild/.

## My method and why it is exact

**Parameters** (mine/gf3.py, mine/mycheck.py) use exact GF(3) Gaussian elimination:
- s = rank(S).
- c = rank(S J S^T)/2.
- k = n - s + c.
- N = span(S)^perp is the null space of the rows (-s_z | s_x).
- I = span(S) ∩ N.

**Method 1: Brouwer-Zimmermann enumeration** (mine/bz.c, driven by mine/mycheck.py). C = N is a GF(3)-linear code with K = 28 dimensions. It is split into m = 2 information sets Q_1 and Q_2, on disjoint sets of 14 positions each (both coordinates of every position). In each set, the columns of the systematic generator matrix form the identity. So every codeword is exactly one message (its values on Q_j), and I enumerate messages with exactly t nonzero positions for t = 0, 1, ...

Why this is complete:
- Let μ_j(v) be the number of nonzero positions of v inside set j. Then μ_j(v) ≤ wt(v restricted to that set's positions).
- The two position sets are disjoint, so a vector not reached by level t has μ_1, μ_2 ≥ t+1, which gives wt(v) ≥ 2(t+1).
- So after level t, **every** vector of N of weight ≤ 2t+1 has been enumerated. Nothing is sampled or skipped.

How vectors in I are excluded: membership in I is decided by the syndrome (<v,y_1>, ..., <v,y_28>) over a basis y_i of N. It vanishes on N exactly when v ∈ N ∩ N^perp = N ∩ span(S) = I.

When the result is proven: U is the minimum weight among enumerated vectors outside I. If U ≤ 2(t+1), any vector of N \ I lighter than U would already have been enumerated, so d = U.

Duplicates: distinct vectors are counted once using the μ values, which gives exact weight counts below the completeness bound.

**Method 2: position-subset rank test on S** (mine/subset.c). This shares no code with method 1. For each w-subset T of positions, the vectors of N supported inside T form the kernel of the rows(S) x 2w matrix with columns -S[:,n+p] and S[:,p] for p ∈ T. The kernel has size 3^def(T). Every w-subset is visited by depth-first search with an incremental echelon basis, and the program sums 3^def(T) - 1 over all of them.
- A sum of 0 at w = 11 means no nonzero vector of N has weight ≤ 11. That is stronger than needed, since it doesn't even exclude I.
- At w = 12, with no lighter words, the sum equals A_12, the number of weight-12 vectors of N.

## Tests of my checker (before using it on the claim)

- **mine/tests.py: 161 checks (6 known-positive codes, each with a parameter check, plus 149 random cases), 0 failures.** Every case compares d and the exact weight counts, split into in-I and not-in-I, against brute force (mine/brute.py, numpy). The brute force shares no code with bz.c. It either enumerates all of GF(3)^(2n) for n ≤ 5, or every combination of a basis of N. It decides span(S) membership with a different test (dot product against null(S)). The cases are:
  - Known positives:
    - the qutrit [[5,1,3]]_3 code: got s=4, c=0, k=1, d=3;
    - the EA repetition family [[n,1,n;n-1]]_3 for n = 4, 5, 7, 8: all correct;
    - the CSS code from the ternary Golay [11,6,5]_3: got [[11,1,5]]_3 with c=0.
  - Random S for n = 2 to 14, including shapes like the claim's (K = n, two information sets of n/2 positions).
  - n = 28 cases with K = 10, 12, 13, which exercise the full bit width.
  - 29 "full distribution" cases (among the 149) run to completion, where every weight count matched.
- **mine/excl_tests.py: 30 cases, 0 failures.** S contains a weight-1 isotropic generator, so N has weight-1 vectors that lie in I and must be excluded. In 16 of these cases the exclusion raises d above N's minimum weight, and d still matched brute force.
- **mine/subset_tests.py: 158 cases (n, rows, w), 0 failures.** The sum Σ_T (3^def(T) - 1) equals Σ_j A_j C(n-j, w-j) from brute force.
- **Seeded negatives** on the claim's own S (mine/negatives.py). In every case the checker reports a difference from the claim:
  - One entry changed (S[0][0] += 1, or S[17][40] += 2): gives s=28, c=7, k=7, d=11, with 906 weight-11 vectors outside I.
  - A weight-11 vector planted in N (27 generators made orthogonal to it): k=7. A verified witness of weight 8 gives d ≤ 8. The subset method agrees: sum 0 at w=7, so d = 8.
  - Exclusion check: the planted vector is added to S, so it lies in I. counts_in[11] = 4, and the method-1 weight counts (in I plus outside I) predict the method-2 subset sums at every w = 6..13, all equal (for example 23150 at w=11 and 3507566 at w=13).

## Results on claim/object/eaqecc_28_6_12_6.json

**Parameters** (mine/claim_t5_seed1.out):
- rank(S) = 28 = s.
- rank(S J S^T) = 12, so c = 6.
- k = 28 - 28 + 6 = 6.
- dim N = 28, dim I = 16 (= s - 2c).

**Method 1** (mine/claim_t5_seed{1,2,3}.out, three different disjoint partitions):
- Every level count is the exact message count. For example level 5 is 65601536 = C(14,5)·8^5 per set, and the total is 139787874 leaves.
- After level 5, every weight ≤ 11 has been enumerated. The only vector of weight ≤ 11 is the zero vector (in I). Nothing else of weight 1..11 exists, inside or outside I.
- A weight-12 vector outside I was found, so U = 12 ≤ 12 and the program printed `RESULT d=12 proven`.
- Python checked each partition's witness on its own: it is orthogonal to every row of S, not in span(S), and has weight 12.

**Level 6** (mine/claim_t6_seed{1,2,3}.out, identical on all three partitions): exact counts up to weight 13.

| Weight | In I | Outside I |
|---|---|---|
| 12 | 504 | 56448 |
| 13 | 0 | 1112832 |

**Method 2** (mine/claim_subset_w{11,12,13}.out):

| w | Subsets visited | Dependent subsets | Σ(3^def - 1) |
|---|---|---|---|
| 11 | 21474180 = C(28,11) | 0 | 0 |
| 12 | 30421755 | 7119 | 56952 = 504 + 56448 |
| 13 | 37442160 | not needed | 2024064 = A_13 + 16·A_12 = 1112832 + 16·56952 |

Method 2 agrees exactly with method 1.

**Conclusion: d = 12 exactly.** No nonzero vector of span(S)^perp has weight ≤ 11, and witnesses of weight 12 outside span(S) exist.

**Conventions** (mine/conventions.out):
- GF(9) with w^2 = w + 1 is a field.
- S equals phi(D9) row by row (rows r, w·r).
- My own evaluation of the construction text gives the same 14 rows as G9, as a set. Their order differs, and the text does not fix an order.
- D9 is Hermitian-orthogonal to G9.
- span(phi(G9)) = span(S)^perp.

## Comparison with the claim and with the author's outputs

**Claim** (object fields n=28, k=6, c=6, d=12): all four agree with my values.

**Author's REPRODUCE.md steps 1 to 4:** I ran them verbatim, twice, in fresh copies of claim/ (mine/run_author.sh, outputs in mine/author_run1.out and mine/author_run2.out). Apart from the timing lines, the two runs are identical. claim/ itself was left unchanged.

- **Step 1:** `rebuilt.json` sha256 51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573. That equals the object's hash, and `cmp` reports the files identical. This matches REPRODUCE.md.
- **Step 2:** prints `n=28 s=28 c=6 k=6 dim_N=28 dim_I=16 N_closed_under_w=True` and `kappa=14`.
  - m = 17: `deficient=0` in all 4 parts, and the parts' subsets sum to 21474180 = C(28,17).
  - m = 16: deficient = 4184, 1850, 770, 315, summing to 7119, over 30421755 subsets.

  All as stated in REPRODUCE.md. The 7119 is the same as my 7119 dependent 12-subsets, which are the complements.
- **Step 3:** both witness lines are exactly as expected: `weight=12 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False` and `symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False`. I re-checked both author witnesses with my own gf3.py: weight 12, in span(S)^perp, not in span(S).
- **Step 4:** prints `n=28 s=28 c=6 k=6 dim_isotropic=16 dim_dual=28`.
  - W = 11: `with_vector_outside_isotropic=0` in all 4 parts, over 21474180 subsets.
  - W = 12: 1773, 1798, 1714, 1771, summing to 7056.

  All as stated. This also agrees with my counts: 56448/8 = 7056 supports carry vectors outside I, and 504/8 = 63 carry only isotropic vectors, for 7056 + 63 = 7119.

I read the author's code for logic errors and found none:
- the GF(9) route checks closure of N under w before using Hamming weight over GF(9);
- infoset's pruning only counts subsets by binomial coefficients;
- subset_ea puts I's basis first and flags a dependent non-I row.

## Issues found

None that affect the result. Minor observations:
- The headers of claim/checkers/gf3prep.py, claim/checkers/subset_ea.c and claim/checkers/witness.py say they were written for an earlier run (2026-10-24-1253). The rest of the package says run 2026-10-24-1500. This is provenance only, and my independent methods confirm the same numbers.
- The order of G9's rows is not fixed by the construction text. The rebuild fixes it (sorted by pole order) and reproduces the bytes exactly.

## Resources

- Every heavy job ran with `nice -n 10`, a perl `alarm` hard cap (600 to 2700 s) and one core.
- Wall times:
  - my method 1: 0.5 s at level 5 and 5.2 s at level 6;
  - my method 2: 3.2 s, 4.9 s and 6.6 s;
  - the author's steps: 28.7 s.
- PIDs are recorded in mine/pids.log. All my processes had finished before I wrote this verdict.

pass: true
