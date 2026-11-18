context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report

Verdict: the claim reproduces. My own checker, written before opening the package's verifiers, confirms every dual constraint exactly and the stated value.

## 1. Definition quoted (before reading package code)

Source: MinT, desc_OBoundLP.html, "An Alternative Formulation of the LP Bound for OOAs". Types F = {(f_0..f_T): sum f_i = s}, size |f| = sum i*f_i, multivariate Krawtchouk polynomials of the NRT scheme. Quote: "Suppose we can find a polynomial p ... such that c_f >= 0 ..., c_0 = 1, and p(e) <= 0 for all e in F with |e| >= k+1. Then ... the number of runs in any OOA(M, s, S_b, T, k) satisfies M >= b^(Ts)/p(0)."
That page's formulas were garbled in extraction, so I did not copy them. I derived the dual LP directly from the OOA definition (glossary: projections on coordinates (i,1..k_i) with sum k_i = k are balanced), which is the same LP.

My derivation, with a_X = (1/M) times the number of ordered run pairs of agreement shape X = (x_0..x_T):
- Single block, depth T: let E[i][j] be the sum of chi_w(d) over characters w of weight i, for a difference d of agreement shape j. Then E[0][j] = 1 and E[i][j] = b^i*[j>=i] - b^(i-1)*[j>=i-1].
- K_f(X) is the coefficient of prod z_i^(f_i) in prod_j (sum_i E[i][j] z_i)^(x_j).
- Strength k means sum over pairs of K_f = 0 for 1 <= |f| <= k. The sums are squared character sums, so they are >= 0 for |f| > k.
- If u_f <= 0 for |f| > k and g(X) = 1 + sum_f u_f K_f(X) >= 0 for all shapes X, then M >= g(diagonal), using a_diag >= 1 for multisets.

## 2-3. Own checker on the certificate

Files: object/certificate_b3_m11_s19_t3.json (60 dual weights; types and sizes consistent).
- 8855 types enumerated, equal to num_types_total.
- Every u_f with |f| >= 9 is <= 0.
- g(X) >= 0 for all 8855 shapes, exactly. 0 negatives, and exactly 1 shape is tight (g = 0).
- g(0,0,0,0,19) = 2403828588527406331/13544324988667 = 177478.6554914159. This equals the stated fraction exactly.
- 177478.655... > 177147 = 3^11. The excess is 4492049760013282/13544324988667.
- u_scaled_by_L equals u * common_denominator_L for all 60 rows.
- K values came from my own C (__int128) polynomial expansion. A separate Python Fraction implementation matched it on 43 shapes, including random shapes and the extreme shapes.
- Two runs of the checker gave identical output.

## Sanity test of my K machinery

An LP solved by scipy HiGHS with my K gave 214620.4038461552 for OOA(3^11, 12, S_3, 2, 9). This equals MinT's 11160261/52 = 214620.40384615384. (My brief quoted the same fraction; it is 214620.40, not 214635.8.) That confirms my eigenvalues and sign conventions.

## 4. Net to OOA and depth reduction

Quote, MinT glossary: "An (m-k, m, s)-net N in base b is equivalent to an OOA(b^m, s, S_b, infinity, k)". A (3,11,19)-net therefore gives OOA(3^11, 19, S_3, infinity, 8).
Strength is defined by balance of projections with k_i <= depth. Truncating to depth 4 only removes projections, so strength 8 is kept. So OOA(3^11, 19, S_3, 4, 8) would exist. M = 3^11 < the proven bound is a contradiction, so there is no (3,11,19)-net.
A net with t < 3 would also be a (3,11,19)-net, so the closure holds for t <= 3.
Limit: I used the MinT glossary for the equivalence; I did not fetch Martin-Stinson, Lawrence, or Mullen-Schmid.

## Package comparison (run only after my result)

In a copy at work-reproduce/claimcopy, run_checks.sh printed:
- Python Fraction: VERIFIED, min_LHS = 0.
- C99 int128: VERIFIED, min_scaled_LHS = 0.
- Corruption tests: OK.
- Final line: PASS.
This agrees with my result. The SHA256SUMS entries for the withheld panel/ files cannot be read; every other listed file is OK.

## Fetch log

All fetches used the User-Agent 'V3R1T4S-research (honest client; curl)'.
- 2026-11-18T01:26:39Z http://mint.sbg.ac.at/desc_OBoundLP.html 200 sha256 a878ed653883ad890fd2648a1a63655b23dbb7e8b48c38efdd2d035ea07b4404
- 2026-11-18T01:30:14Z http://mint.sbg.ac.at/desc_OOA.html 200 (page body was an "Invalid key" error) sha256 0c49553cac0328ba273a44b1c93e4e6f76bd62a47ae1ae853cd9f31f7c5c2831
- 2026-11-18T01:30:14Z http://mint.sbg.ac.at/desc_MNetFromOOA.html 200 (invalid key error) sha256 317e79377fa48e296b95676a5c761b4a4e5fddd6e3fd15d33bcfd668d9b1e1f9
- 2026-11-18T01:30:19Z http://mint.sbg.ac.at/desc_OOA.html (repeat) 200 (invalid key error), body not hashed
- Glossary: http://mint.sbg.ac.at/glossary.php fetched without logging the code or hash at about 01:30:1x, then refetched 2026-11-18T01:30:24Z 200 sha256 5300cf5fe62cbf54a6be51fb993b7a2e9e5b3f1c3158178c50f0ce4ac65aae03
- Not fetched: Martin-Stinson paper.

pass: true
