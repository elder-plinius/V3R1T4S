# Honesty gate (hypercubic-percolation-1-over-d-series-next-term)

status: CONFIRMED_PARTIAL
confirmed_scope: For bond percolation on Z^d, a constructive computer-assisted derivation, with no fitted parameters, gives the closed form of the binom(d, e-3) coefficient of D_e(q), e >= 4, as q^(2(e+1)d-2e) times six gamma terms (q^0..q^-3, q^-2d, q^-2d-1). It matches the published binom(d, e-3) coefficients of Mertens-Moore D_4..D_11 (48 of 48 numbers) and the published binom(d, 9) entry of D_12(1). It matches an independent brute-force animal enumeration at (d, e) = (1,4), (2,5), (3,6). It supplies the data for tasks (9,12) and (11,14) of Table 9 (their (d, e) tasks). It does not give b_13 or any sigma^-7 coefficient, and the package's earlier draft wording "for all d >= 3, e >= 3" was wider than what was shown, so this sentence states the narrower range.

## Gate notes
- Object: object/bond_perimeter_binom_d_e_minus_3_formula.json, sha256 375c90d27cbeb9c56b6a3dedde08bc020aaac0864cc2a7f71cfbd4919009dec1.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic's own C++ enumerator of bond animals, written before reading the package, matches the closed formula exactly for e = 4..8 in all six coefficient families; the formula also matches all binom(d, e-3) coefficients of Mertens-Moore's D_4..D_11 and their D_12(1) entry.
- Scope narrowed from the package's draft ("all d >= 3, e >= 3") to e >= 4, as the CRITERION skeptic found; the formula is a constructive computer-assisted derivation with no fitted parameters, and it supplies Mertens-Moore's Table 9 tasks (9, 12) and (11, 14), not b_13.
