context: Claude Code subagent, fresh context [Sonnet 5.5]

# CRITERION report for SID 375c90d2 (partial win p2)

[Edited 2026-11-18 when the package was assembled: the last clause of confirmed_scope referred to the package's draft README, which now states the narrower range; it was reworded to say so. The checks and verdict are unchanged.]

## Result of package checks
- Ran `verify-it-yourself/run_checks.sh` in a copy of this package (stdlib Python, about 45 s). All four OK lines and `PASS` came out, matching `verify-it-yourself/RECEIPTS.md`.
- Also ran `how-we-built-it/audit_mertens_moore_table9.py` and `how-we-built-it/brute_proper_bond_animals.py`. Both pass their assertions.
- I re-evaluated the six gamma expressions written in `how-we-built-it/PROOF.md` for e = 4..14 and compared them with `evaluations_e4_to_e14` in `object/bond_perimeter_binom_d_e_minus_3_formula.json`. They agree, so the README/PROOF formula and the checked object are the same thing.

## Fetch log
- 2026-11-18T17:32:35Z, https://arxiv.org/e-print/1805.02701, HTTP 301 (redirect, no body used).
- 2026-11-18T17:32:38Z, https://arxiv.org/e-print/1805.02701 (followed redirect), HTTP 200, sha256 c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf. This is the Mertens-Moore TeX source and matches the hash in the package's README.
- I read Table 9 and Appendix A directly from `bond-animals.tex` in that source.

## Clause 1: "proven closed formula for the binom(d, e-3) coefficient, not fitted"
- No fitting appears in the derivation.
- The formula is built by `how-we-built-it/prove_bond_perimeter_e_minus_3.py` and by `derive_symbolic(3)` in `verify-it-yourself/check_bond_perimeter_p2.py`. Both build all 16,314 excess-3 core multisets and sum exact rational polynomials in e.
- The checker first re-derives Mertens-Moore Theorems 5 and 6 with the same machinery.
- The argument in `how-we-built-it/PROOF.md` is a sketch, not a line-by-line proof. I re-read its main steps and found them sound:
  - Any subgraph of Z^r with cyclomatic number 2 or more needs at least 7 edges, while the repeated-axis part has at most 6 edges. So v is e+1 or e.
  - A chord along a singleton axis can only come from a direct bridge between two components.
  - Prüfer's weighted-tree count gives the sum over bridge structures.
- The closed form as a polynomial times (e+1)^(e-8) or e^(e-7) rests on the code's symbolic summation. It is not a formally verified proof. I judge it a computer-assisted constructive proof that the data below corroborate.
- The data are not used to choose coefficients. I confirmed the following against the Appendix A text of the TeX source:
  - The formula reproduces the binom(d, e-3) rows of D_4..D_11, 48 of 48 numbers. I spot-checked entries from D_7, D_8, D_9, D_10 and D_11 directly against the TeX; the audit script's table covers all eight polynomials.
  - Summed at q=1 for e=12, it gives 6199599459637248, which equals the published binom(d, 9) entry of D_12(1). That published entry came from Mertens-Moore's own route (the identity applied to D_1..D_11), not from enumeration at d=9, so it is an extrapolation test.
- Verdict: proven constructively and not fitted. The proof text is thinner than a paper-grade proof.

## Clause 2: "removes one of the enumeration tasks in Table 9"
- Table 9 is `tab:estimated_times` in the TeX source. Its caption says data for (e>=12, 14) and (e>=10, 12) already come from Theorems 4-6.
- The binom(d, e-3) coefficient means k = e-3, so the next unknown dimension is k = 9 at e = 12 and k = 11 at e = 14.
- So (d, e) = (9, 12) in the Pade column (listed at 4.5 years) and (11, 14) in the classical column (listed at 133,800 years) are genuinely removed.
- Both removals are valid. Only one is needed.
- Tasks (7,12), (8,12), (10,14) and the rest of the table remain, so b_13 is still not obtained. The README says so under "Not Claimed".

## Clause 3: "checked by computer against brute-force counts for small e and d"
- The package has an independent lattice bond-animal enumerator, `brute_proper_bond_animals.py` and the copy in `check_bond_perimeter_p2.py`.
- It computes the perimeter t and vertex count v from the raw definition, grid edges incident to the animal's vertices and not in the animal. It shares no code with the formula derivation, only the style of animal-growing and the t/v/chord identity.
- It is checked only for (d, e) = (1, 4), (2, 5), (3, 6), where d = k = e-3.
- That is literally "small e and d", but it is only 3 values of e.
- The brute force does not test e = 7 and above, d > k, or the polynomial-in-e shape.
- Only e = 6 exercises all six families nonzero. At e = 4 and 5, gamma_{2d+1} is zero by the (e-5) factor.
- The wider independent evidence is the published Appendix A comparison at e = 7..11 and e = 12 (at q=1). Those figures come from Mertens-Moore's own enumerations and analytic work, so they are independent of the package's formula.
- I did not run my own brute force at e = 7 or above. It would need tens of millions of animals in Python, which I judged too heavy to be worth it, since the published e = 7..11 data cover those points.

## README scope "for all d >= 3, e >= 3"
- This is not supported literally. The proof never uses d >= 3.
- The binom(d, e-3) coefficient is a formal coefficient in the polynomial-in-d expansion. It is zero for d < e-3, and nothing about d = 3 specifically is shown.
- At e = 3 the index is k = 0. Mertens-Moore sum from k = 1, so the formula only returns 0 there by its (e-3) factor and says nothing.
- The meaningful range is e >= 4, with d >= e-3 for a nonzero count.
- The checks confirm e = 4..14, plus brute force at the three small points above. Nothing was checked for d < k.

## Other checks
- Pitfalls: no conflation with p1 or the full target. The package makes no sigma^-7 claim.
- I did not do the novelty literature search, which belongs to another role.

confirmed_scope: For bond percolation on Z^d, a constructive computer-assisted derivation, with no fitted parameters, gives the closed form of the binom(d, e-3) coefficient of D_e(q), e >= 4, as q^(2(e+1)d-2e) times six gamma terms (q^0..q^-3, q^-2d, q^-2d-1). It matches the published binom(d, e-3) coefficients of Mertens-Moore D_4..D_11 (48 of 48 numbers) and the published binom(d, 9) entry of D_12(1). It matches an independent brute-force animal enumeration at (d, e) = (1,4), (2,5), (3,6). It supplies the data for tasks (9,12) and (11,14) of Table 9 (their (d, e) tasks). It does not give b_13 or any sigma^-7 coefficient, and the package's earlier draft wording "for all d >= 3, e >= 3" was wider than what was shown, so this sentence states the narrower range.

pass: true
