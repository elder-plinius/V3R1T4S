# REPRODUCE skeptic verdict: [[25,5,12;8]]_3 from claim/object/eaqecc_25_5_12_8.json

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

Confirmed. I wrote my own checker from the definition before opening claim/checkers/ or claim/rebuild/. It computes,
from the matrix S alone, s = 28, c = 8, k = 5 and the exact EAQECC minimum distance d = 12. Two independent exact
methods give this, and each covers the whole space:

- an enumeration of all 9^11 - 1 nonzero words of the GF(9) code behind span(S)^perp;
- a GF(3) rank test on every 11-subset and every 12-subset of positions.

Both methods agree with brute force on 240 random small cases. Both catch seeded negatives. They agree with each
other down to the count of 1192 weight-12 supports. Every value printed by the author's REPRODUCE.md steps 1 to 6
matches what REPRODUCE.md says it should be. Repeated runs give byte-identical output. I re-derived the no-search
proof step by step, and computed d(E_13) exactly as 15, which is at least the bound of 15 the proof uses.

I did not run step 7 (the live table fetch); the table and novelty skeptics cover it. In the saved copy
(claim/table/row_25_5.txt), the cell (25,5,8) is listed as [[25,5,11-18;8]]_3, so d_lower 11 < 12 <= d_upper 18.

## Definition used (quoted from CLAIM.md, success criterion)

> "with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic
> commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in
> the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition
> used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper."

Conventions, from the object's S_convention field: rows are (x|z) over GF(3), and <(x|z),(x'|z')> = x.z' - z.x'.
Weight means symplectic weight, the number of positions i with (x_i, z_i) != (0, 0). Both the symplectic dual and the
weight are the same under either sign convention and under the (z|x) ordering.

The object's sha256 is e33e8fb04dc70d4d703e033310b6efafb1825109a93d649ecef183451ee09ec3, the same as in CLAIM.md.
It was unchanged when I finished.

## What I computed and how (my code is in mine/)

- **mine/lin.py:** my own GF(3) and GF(9) linear algebra. GF(9) = GF(3)[w]/(w^2 - w - 1), encoded a + 3b. Field
  axioms are checked on the full tables, and w has order 8.
- **mine/params.py, run on S:**
  - rows 28, rank s = 28 (so the generators are independent).
  - M = S J S^T is antisymmetric with zero diagonal; rank(M) = 16, so c = 8 and k = 25 - 28 + 8 = 5.
  - dim span(S)^perp = 22. The isotropic part H = {a^T S : a^T M = 0} has dimension 12.
  - span(S), span(S)^perp and H are each closed under multiplication by w, with w acting as (a|b) -> (b|a+b).
  - GF(9) rank of phi^{-1}(span(S)^perp) is 11, and of H it is 6. So span(S)^perp = phi(C) for a GF(9)-linear
    [25,11] code C, and symplectic weight equals Hamming weight on C.
- **Exact method 1, mine/enum_bz9.c (bit-sliced GF(3), modular ternary Gray code):**
  - Enumerates every projective word of C: TOTAL_PROJECTIVE 3922632451 = (9^11 - 1)/8, so all 9^11 - 1 nonzero words
    up to GF(9)* scalars. Weight and membership in H are scalar-invariant because H is GF(9)-linear. An earlier estimate of
    about 3.9e8 was off by a factor of 10; the true count is about 3.9e9, and it still runs in
    about 10 s.
  - Every word of weight <= 13 is tested for membership in span(S), meaning symplectic orthogonality to all 22 basis
    vectors of span(S)^perp.
  - Result: no word of weight < 12. At weight 12 there are 1204 projective words: 12 in H and 1192 outside H. At
    weight 13 there are 19440 projective words, none in H. The minimum weight outside H is 12.
  - Full distribution of C (all words): A_12 = 9632, A_13 = 155520, ..., A_25 = 1651406904, summing to 9^11.
  - The exact MacWilliams transform (mine/post.py) gives nonnegative integers with B_0 = 1, summing to 9^14. The dual
    has minimum distance 9.
  - Enumerating H alone gives 12 projective words of weight 12, matching the H count found inside C.
  - All 40 printed witnesses were re-checked in Python straight from S: weight as printed, in span(S)^perp, not in
    span(S). Example of weight 12, in GF(9) digits: 1200000000000487868400487.
  - Two runs with different witness limits gave identical weight lines. Peak memory was 1.4 MB.
- **Exact method 2, mine/sub_subset_ea64.c, which uses no GF(9) structure:**
  - For each position set T, it compares dim V_T = 22 - rank(V on the complement) with dim H_T = 12 - rank(H on the
    complement), where V = span(S)^perp. Some vector of V outside H is supported in T exactly when dim V_T > dim H_T.
  - t = 11: all 4457400 subsets, 0 violating, so d >= 12. Smaller t then follows, since every set of fewer than 11
    positions lies inside some 11-set.
  - t = 12: all 5200300 subsets, 1192 violating, so d <= 12.
  - The "exact" mode (t = 1, 2, ...) prints EXACT_D 12.
  - The 1192 violating 12-sets equal the 1192 distinct supports of the weight-12 words outside H from method 1.
- **Result:** d = 12 exactly, so the code is [[25,5,12;8]]_3 with c = 8 >= 1.

## Tests of my checker (mine/tests.py, seed 12345; mine/negative.py, seed 777)

- **150 random S that are not GF(9)-linear (n = 3 to 5):** brute force over all of GF(3)^{2n} straight from the
  definition. |perp| and |H| match my s and c, and method 2's exact d matches the brute-force d (including cases with
  no vector outside H). 150 passed.
- **60 random GF(9)-linear S (n = 3 to 5, whole-space brute force) and 30 more (n = 6, 7, brute force over span(S)^perp):**
  method 1's weight distribution times 8 matches brute force at every weight, method 1's minimum outside H matches,
  and so does method 2. 90 passed.
- **Seeded negative N1:** I planted a random weight-11 GF(9) vector u, giving S' = basis of span(S) ∩ {u, wu}^perp.
  u is in span(S')^perp and not in span(S'), so d <= 11 by construction. Results: s = 26, c = 8, k = 7. Method 2 gives
  EXACT_D 9, with 14 violating 9-sets. Method 1 (35303692060 projective words, 80 s) gives a minimum of 9 outside H,
  with 14 projective words of weight 9. Both reject the claimed d = 12.
- **Seeded negative N2:** one entry of S changed by +1. Results: c = 9, k = 6, w-closure lost, and method 2 gives
  EXACT_D 11. The mismatch with the claimed parameters is detected.

## Author's REPRODUCE.md steps

I ran these on a copy of claim/ (in run/claim) after my own numbers were done; claim/ itself was not modified.

| Step | What it checks | Result |
|---|---|---|
| 1 | Rebuild the object | Prints exactly the documented line (`... [25,11] hull=6 -> [[25,5,?;8]]  S 28x50  D9 14x25`). sha256 of rebuilt.json = e33e8fb0...9ec3, the same as the object. |
| 2 | Method A, infoset | `n=25 s=28 c=8 k=5 dim_N=22 dim_I=12 N_closed_under_w=True`, `kappa=11 (2*kappa == dim_N: True)`. m = 14: subsets 2708307, 1223980, 525113 (sum 4457400), deficient 0, 0, 0. m = 13: deficient 728, 323, 153 (sum 1204, matching my 1204 weight-12 projective words). |
| 3 | Witnesses | witness.py: `symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False`. gf9info witness: dimension 1, codeword `0 1 0 0 0 0 0 0 5 0 0 7 0 0 8 1 4 8 6 1 0 5 0 1 3`, `weight=12 in_N=True orthogonal_to_all_rows_of_S=True in_isotropic_part=False`. My code confirms both vectors from S; a scalar multiple of each is in my list of 1192. |
| 4 | Method B, subset_ea64 | `n=25 s=28 c=8 k=5 dim_isotropic=12 dim_dual=22`. W = 11: examined 1485800 three times, 0 violating. W = 12: examined 1733434, 1733433, 1733433 with 401, 402, 389 violating (sum 1192). |
| 5 | bz64 | `K=11 n=25 d=12 sets=11,11,3 maxw=5 words=6216969` with the same witness word. |
| 6 | punct_check | Last line `RESULT: d_EA = 12 exactly (no distance search): True`. |
| 7 | Live fetch | Not run, as instructed. |

Every printed value matches REPRODUCE.md. Running steps 2 and 4 to 6 twice more gave byte-identical output
(sha256 75221462e7bb1025d1164426e4270e058cf1f57e700342fb4aeddfd4e620bd42 both times), so the results are deterministic.

## No-search proof, re-derived (mine/proof.py, built from the construction text only)

- **Curve points:** y^3 + y = x^4 over GF(9) has exactly 27 affine points. Ordered by (x, y) code, the first three
  are (0,0), (0,4), (0,8), and these are the only points with x = 0.
- **Monomials:** the 11 monomials x^i y^j with j <= 2 and 3i + 4j <= 13 have distinct pole orders
  {0,3,4,6,7,8,9,10,11,12,13}, and x^3 y is the only one with pole order 13.
- **Bound d(E_13) >= 15:** a nonzero f in L(13 P_inf) has at most (pole order of f) affine zeros. There are two cases:
  - pole order 13: at most 13 zeros, so at least 14 nonzero affine coordinates, plus the nonzero 28th coordinate,
    giving weight >= 15;
  - otherwise: pole order <= 12, so affine weight >= 15.

  The premises (v_inf(x) = -3, v_inf(y) = -4, distinct pole orders) are standard and were checked above. I also
  computed it exactly: enumerating all 3922632451 projective words of the [28,11] code E_13 gives a minimum weight of
  15 (9036 projective words).
- **Puncturing:** deleting coordinates 0, 1, 2 leaves rank 11 and lowers each weight by at most 3, so d >= 12.
- **Column scaling:** scaling columns 6,7,8,12,...,20,24 by w (nonzero) changes no weight.
- **The constructed code is the claimed one:** it spans exactly phi^{-1}(span(S)^perp), and the JSON G9 spans the
  same code.
- **Hull and duality:**
  - The Hermitian hull has dimension 6; without the scaling it has dimension 4, as CLAIM.md says.
  - The JSON D9 spans the Hermitian dual of C, and span(S) = phi(C^{perp_h}).
  - The rows of S are exactly phi(r), phi(w r) for the rows r of D9, in order.
  - phi(hull) = H.
- **Upper bound:** the weight-12 witness lies in phi(C) and outside span(S), so d = 12.

## Process notes

- At the very start the machine-wide heavy-job count printed 3, and I ran my 35-second test suite (mostly Python,
  with only brief calls of my C programs on tiny inputs) without waiting. Before every later run the count was 2.
- I started no background jobs, and none are left running.

pass: true
