# criterion, Feigenbaum z=4, partial win p2
context: Claude Code subagent, fresh context [Sonnet 5.5]

Literal p2: 'The z = 4 (quartic maximum) Feigenbaum alpha or delta to at least 1000 decimals, two resolutions agreeing, exceeding the digit count of OEIS A195102 and Thurlby's thesis (about 330 digits) re-fetched live.'

My own check, from the definition. The file's coefficient format is not documented outside the author's checker, which I did not read; I recovered it from the data: phi(u) = 1 + u * S(2u-1), S the Chebyshev series of c_coeffs; g(x) = phi(x^4); alpha = 1/phi(1). Test at 60 digits first: the standard Feigenbaum-Cvitanovic equation g(x) = alpha g(g(x/alpha)), g(0)=1, alpha=1/g(1) holds to 1e-61 (so the recovered convention is right, not fitted loosely). Eigenfunction: h(x) = T(b, 2x^4-1) with the fixed-alpha linearisation (L h)(x) = alpha (g'(g(x/alpha)) h(x/alpha) + h(g(x/alpha))), alpha negative; (L h)/h is the same number at all test points. A double-precision collocation spectrum of L built from the file's g has leading eigenvalue 7.2847 (next ones 1, 0.29, 0.26 in magnitude), so it is the dominant (unstable) eigenvalue, delta_4.
At 1300 digits, 31 random points, both resolutions: fixed-point residual max 1e-1092 (N1=1070 coefficients) and 1e-1100 (N2=1100); spread of delta over points 1e-1087 and 1e-1099. alpha_4 from N1 and N2 agree to 1085 decimals; delta_4 to 1084 decimals (1082 claimed, understated). alpha_4 = -1.69030297140524485334378015032416134822827805970956196668242...; delta_4 = 7.28468621707334336430893056799555306947804661979979065907212...; both printed values agree with the file's strings (to 1099 decimals for alpha).

Clauses:
- At least 1000 decimals of alpha_4 or delta_4: MET at 1085 and 1084 by the agreement test (not a proof of error bound; residuals at sample points plus two resolutions agreeing, which is what p2 literally asks).
- Two resolutions agreeing: MET, 1070 vs 1100 coefficients (2.8 percent apart).
- Exceeds OEIS A195102 (49 digits) and Thurlby (331 and 325 proven digits): MET by a factor of 3. The first 331/325 digits match the thesis table per the cell's comparison (the leading 60 digits match A195102 here).
- Caveat: agreement of two resolutions of one method is not an error bound, and not the same as 'proven' digits; the criterion does not require proof for p2. Sign: the object prints the magnitude of alpha_4, as OEIS does. Newer literature for z=4 beyond the two named sources is the novelty skeptic's question.

confirmed_scope: The coefficient file defines a quartic (z=4) Feigenbaum fixed point and its dominant eigenfunction satisfying the defining equations to about 1e-1092 and 1e-1100 at 31 points, with alpha_4 = -1.6903029714... and delta_4 = 7.2846862170... agreeing between 1070 and 1100 coefficients to 1085 and 1084 decimals (not proven correct to that many digits), exceeding the 49 digits of A195102 and the 331 and 325 proven digits of Thurlby.
pass: true
