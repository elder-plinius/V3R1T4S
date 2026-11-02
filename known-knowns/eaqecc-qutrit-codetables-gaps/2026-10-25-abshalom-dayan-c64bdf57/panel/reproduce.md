# REPRODUCE skeptic verdict: [[23,4,12;9]]_3 (object/eaqecc_23_4_12_9.json)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

**Bottom line: PASS.** My own exact checker, written from the definition before I opened claim/checkers/ or
claim/rebuild/, enumerates all 3^18 - 1 = 387420488 nonzero vectors of span(S)^perp and gives s = 28, c = 9, k = 4,
d = 12. Every value the author's REPRODUCE.md steps 1 to 7 print matches what REPRODUCE.md says. I re-derived the
no-search proof myself and checked each premise, including an exhaustive check that d(E_11) = 17. I found no
mismatch, no missing object and no non-determinism. Step 8 (the live table) was not run because it is left to the
other skeptics.

Object: claim/object/eaqecc_23_4_12_9.json, sha256 c64bdf57a5280892b8d4e085ea565c865d5584de5198baa9763cb516318f06f4
(checked before and after my runs). Work ran 2026-10-25 from 11:21:55 to 11:25:43 UTC (date -u).

## Definition (quoted from the success criterion in claim/CLAIM.md)

"with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation
matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the
symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by
Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper."

Conventions used (from the object JSON): the rows of S are (x|z) over GF(3), 46 columns, and
<(x|z),(x'|z')> = x.z' - z.x'. Symplectic weight is the number of positions i with (x_i, z_i) != (0, 0).

## My checker (mine/)

- mine/prep.py works from S alone. It computes s = rank_GF(3)(S), the matrix M = S J S^T and its rank, c = rank(M)/2
  and k = n - s + c. It computes N = span(S)^perp as the nullspace of S J and asserts that every basis vector is
  orthogonal to every row and that dim N = 2n - s. It computes I = {aS : aM = 0}, asserts that I lies in span(S) and
  in N, then extends a basis of I to a basis of N with the I vectors first.
- mine/enum.c (binary my_infoset) enumerates every GF(3) combination of the 18 basis vectors with bit-sliced GF(3)
  arithmetic and stores nothing. A vector lies in I exactly when all of its coefficients on the 8 non-I basis vectors
  are 0, which follows from how the basis was built. The program records a weight histogram for vectors outside I, a
  separate histogram for nonzero vectors inside I, the minimum weight outside I (d) and one witness.
- Tests (mine/test_small.py): the brute-force reference enumerates all of GF(3)^(2n), tests orthogonality to S and
  tests membership in span(S) against the full span set. It computes s from |span|, c from (s - dim I)/2, k, and both
  histograms and d. I ran it on random S with n = 2 to 5, up to 7 rows, including dependent rows and CSS-like rows.
  - seed 1: 300/300 cases agree, 0 mismatches.
  - seed 7: 299/299 cases agree, 0 mismatches.
  - Seeded negative (one I vector deliberately labelled as non-I): the tests caught 192/192 and 203/203 of these.
  - Full-size seeded negative: I changed one entry of S (row 0, column 5, +1) and the checker reported
    rank(SJS^T) = 20, c = 10, k = 5, dimI = 8 and d_EA = 11, so the error was detected.

## Results on S

- mine/prep.py printed: `n=23 rows=28 s=28 rank(SJS^T)=18 c=9 k=4 dimN=18 dimI=10`.
- mine/my_infoset ran in 1.26 s real time with a maximum resident set of 1425408 bytes (/usr/bin/time -l). It
  printed `nonzero_enumerated=387420488`, which equals 3^18 - 1.
  - Outside I: `12:2608 13:33264 14:168864 15:709752 16:3027368 17:10008496 18:26400848 19:55778488 20:89282712
    21:101956224 22:74190744 23:25802072`, which sums to 3^18 - 3^10.
  - Inside I: `12:8 13:24 14:112 15:408 16:1168 17:3632 18:7464 19:13376 20:16488 21:12144 22:4224`, which sums to
    3^10 - 1.
  - It printed `d_EA=12`.
- Determinism: a second run gave the same output, sha256 01d4eb801e75d90001078ee73ea1557efcfbed6b2c5c5976fabcc1da926e5032
  for both.
- My witness is basis vector 17. mine/witness_check.py reports weight 12, support
  [0,1,2,4,5,8,9,10,13,15,18,20], orthogonal to every row of S, and not in span(S) (rank test).
- So s = 28, c = 9, k = 4 and d = 12, established by enumerating the whole space. d_lower is 11 < 12 and d_upper is
  18 >= 12 for the listed cell (23,4,9), per CLAIM.md. Checking the table itself is the other skeptics' role.

## No-search proof, re-derived (mine/proof.py, using only my own GF(9) code)

| Premise | Result |
|---|---|
| GF(9) = GF(3)[w]/(w^2 - w - 1) is a field; w is primitive | true; norm(w) = w^4 = 2 = -1 |
| Affine points of y^3 + y = x^4 over GF(9) | 27 |
| Monomials x^i y^j with j <= 2 and 3i + 4j <= 11 | 9 monomials, pole orders 0, 3, 4, 6, 7, 8, 9, 10, 11 (all distinct) |
| Genus and Riemann-Roch | g = 3, l(11P) = 11 + 1 - 3 = 9 because 11 > 2g - 2 = 4, so the 9 monomials form a basis of L(11P) |
| Rank of E_11 over GF(9) | 9 |
| d(E_11) >= 17 (Goppa-type argument) | true |
| d(E_11), checked exhaustively | 17 |
| Deleted coordinates [0,3,11,12,16] | points (0,0), (1,2), (3,6), (4,2), (5,5), as stated |
| Rank of E' after deletion and column scaling | 9 |
| rowspace(E') == rowspace(G9) | true |
| Hermitian hull dimension of E' | 5 |
| D9 | rank 14 and Hermitian-orthogonal to E' |
| S == phi(D9), rows r and w*r, in order | exactly equal |
| phi(E') | GF(3) rank 18 and orthogonal to every row of S, so span(S)^perp = phi(E') |
| REPRODUCE.md witness word | in E', weight 12, phi(word) not in span(S) |

How the bound follows:

- **The Goppa-type argument.** Take f in L(11P). If its x y^2 coefficient is nonzero, f has exactly 11 poles, so it
  has at most 11 zeros among the affine points. Its weight is then at least 27 - 11 = 16 on the affine coordinates,
  plus 1 for the extra coordinate. Otherwise f lies in L(10P), has at most 10 zeros and weight at least 17.
- **The exhaustive check of d(E_11).** I fed phi(E_11) (n = 28) to my_infoset. Symplectic weight under phi equals
  GF(9) Hamming weight because phi is bijective per coordinate. The run enumerated all 3^18 - 1 codewords and printed
  minimum weight 17.
- **The chain to d = 12.** Deleting 5 coordinates lowers any weight by at most 5, which gives d(E') >= 12. Scaling a
  column by w does not change any weight. Since span(S)^perp = phi(E'), d >= 12, and the witness gives d <= 12, so
  d = 12. Every premise holds.

## Author's REPRODUCE.md steps

I ran these in a copy of claim/ called author_run/, so claim/ itself was not modified. For each heavy run the
machine-wide heavy-job count printed 0.

- **Step 1: ran in full, matches.** The program printed `E_11 deleted=[0, 3, 11, 12, 16] scaled_cols=[...] [23,9]
  hull=5 -> [[23,4,?;9]]  S 28x46  D9 14x23`. rebuilt.json has sha256
  c64bdf57a5280892b8d4e085ea565c865d5584de5198baa9763cb516318f06f4, identical to the object.
- **Step 2: ran in full (both m values, all 3 parts each), matches.**
  - It printed `n=23 s=28 c=9 k=4 dim_N=18 dim_I=10 N_closed_under_w=True` and `kappa=9 (2*kappa == dim_N: True)`.
  - m = 12: every part printed deficient=0, with subsets 785460, 385917 and 180701 (sum 1352078).
  - m = 11: the parts printed deficient 185, 98 and 44.
- **Step 3: ran in full, matches.**
  - witness.py printed `symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False`.
  - gf9info.py witness printed GF(9)-dimension 1, the codeword `0 0 0 0 0 0 0 0 0 1 1 6 3 2 2 5 0 7 0 5 6 3 2`, and
    `weight=12 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`.
  - My own code independently confirms the witness: weight 12, orthogonal to S, not in span(S).
- **Step 4: ran in full (both W values, all 3 parts each), matches.**
  - It printed `n=23 s=28 c=9 k=4 dim_isotropic=10 dim_dual=18`.
  - W = 11: examined 450693, 450693 and 450692, with_vector_outside_isotropic=0 in every part.
  - W = 12: 114, 110 and 102 (326 in total).
- **Step 5: ran in full, matches.** It printed `K=9 n=23 d=12 sets=9,9,5 maxw=5 words=1758843` and the same
  weight-12 witness word.
- **Step 6: ran in full, matches.** The last line was `RESULT: d_EA = 12 exactly (no distance search): True`.
- **Step 7: ran in full, matches.**
  - It printed `n=23 s=28 rank(SJS^T)=18 c=9 k=4 dimN=18 dimI=10`, `nonzero vectors enumerated=387420488`, a
    histogram starting `12:2616 13:33288`, `weight 12: in isotropic part 8, outside 2608` and `d_EA = 12`.
  - The full histogram equals my outside-I plus inside-I histogram at every weight (checked by script).
  - Its witness is also weight 12, orthogonal to S and not in span(S) (checked with my code).
- **Cross-check of the support counts.** My weight-12 counts are 2608 outside I and 8 inside I. Over GF(9), each
  support carries 8 nonzero scalar multiples, so these counts mean 326 supports carry vectors outside I and 1 carries
  only I vectors. This agrees with the author's 326 and 327, assuming each weight-12 support holds a one-dimensional
  space, which is what step 3 reports for the witness support.
- **Step 8 (live table fetch): not run.** It is a network step and covering it is the other skeptics' role.

## Mismatches

None.

## Files

- Under mine/: prep.py, enum.c, test_small.py, witness_check.py, proof.py, enum_out.txt and E11_phi.txt.
- Under author_run/: the copies and outputs of the author's steps.
- No web access was used. No background jobs are left running.

pass: true
