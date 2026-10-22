context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Reproduce report: feigenbaum-z4-p2

Claim under test (partial win p2): the z = 4 Feigenbaum-Cvitanovic fixed point g(x) = phi(x^4) and its eigenfunction, given as Chebyshev coefficients at 1070 and 1100 terms (2.80 percent apart), satisfy the fixed-point and eigen-equations to below 1e-1087 at 31 points (1300-digit arithmetic), and give alpha_4 = -1.6903029714... and delta_4 = 7.2846862170... agreeing between the two resolutions to 1085 decimals (alpha_4) and 1082 (delta_4; 1084 measured), against 49 digits in OEIS A195102 and 331 / 325 proven digits in Thurlby's thesis. Verification method quoted: evaluate the fixed-point residual and the eigen-equation residual at 30 points by Clenshaw summation at precision D + 50, require both below 10^-(D+5), and confirm a second certificate at a different resolution gives the same digits.

Preparation. The contributor's hash list verified from inside the package folder (all OK); the six numbered parts reassemble (cat part01..part06) to a file whose sha256 is 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6, equal to PARTS.sha256 and INDEX.csv. Work was done on a private copy of the package. No network.

## My definitions (written down before opening the author's checker)

- g even, g(0) = 1, g(x) = alpha g(g(x/alpha)), alpha = 1/g(1) (negative, so g(1) = 1/alpha < 0). With g(x) = phi(x^4) and u = x^4 this is phi(u) phi(1) = phi( phi(u phi(1)^4)^4 ) (using alpha^4 = 1/phi(1)^4).
- Eigen-equation: the derivative of g -> alpha g(g(x/alpha)) at the fixed point with alpha held at its fixed-point value: (L psi)(u) = alpha [ phi'(B) 4 A^3 psi(w) + psi(B) ], w = u / alpha^4, A = phi(w), B = A^4, and L psi = delta psi.
- Reading the JSON. The file does not say how the coefficient lists encode phi and psi. I found the convention by trial against the equations themselves: phi(u) = 1 + u S_c(2u - 1) and psi(u) = S_b(2u - 1), where S is the Chebyshev series sum c_k T_k (first coefficient not halved), Clenshaw evaluation. Two wrong guesses were rejected by the residuals (the first guess for phi gave phi(0) = -1.83; a guess psi(u) = u S_b(2u-1) or a linearisation that also varies alpha gave a non-constant ratio L psi / psi). With the convention above the residuals are 1e-1092 and a constant ratio, so the convention is confirmed by the data, not assumed. (That the fixed-alpha linearisation is the right operator for delta_4 is the standard one and is supported by the digits matching the thesis below.)
- Checker (my own script, not shipped in this package): mpmath at 1300 digits, Clenshaw for values, a Chebyshev derivative recurrence for phi', 31 test points u = 1/32 ... 31/32, both resolutions; alpha = 1/phi(1); delta from the file compared with the ratio (L psi)(u)/psi(u); agreement of the two resolutions measured numerically as -log10 of the difference, and as a common-prefix count.

Command: my own checker, run on the reassembled object (not shipped separately). Real output:

    N1 N = 1070  alpha = -1.69030297140524485334378015032416134822827805970956196668242
      max fixed-point residual over 31 points: 1.269e-1092
      dT(u)/psi(u) at 3 points: ['7.284686217073343364308931', '7.284686217073343364308931', '7.284686217073343364308931']
      max eigen residual (delta from file) over 31 pts: 3.483e-1088  |psi| max 0.9945
    N2 N = 1100  alpha = -1.69030297140524485334378015032416134822827805970956196668242
      max fixed-point residual over 31 points: 1.264e-1100
      dT(u)/psi(u) at 3 points: ['7.284686217073343364308931', '7.284686217073343364308931', '7.284686217073343364308931']
      max eigen residual (delta from file) over 31 pts: 1.144e-1099  |psi| max 0.9945
    alpha_4 (from phi(1)) agreement N1 vs N2 decimals: 1085
    delta_4 (file) agreement N1 vs N2 decimals: 1082
    alpha_4 first 60: 1.69030297140524485334378015032416134822827805970956196668242
    delta_4 first 60: 7.28468621707334336430893056799555306947804661979979065907212
    own delta N1 7.284686217073343364308930567995553069478046619799790659072121290188346
    own delta N2 7.284686217073343364308930567995553069478046619799790659072121290188346
    -log10|delta_N1-delta_N2| (own ratios) = 1084.2083
    -log10|delta_N1-delta_N2| (file strings) = 1084.2083
    -log10|alpha_N1-alpha_N2| = 1085.9789
    -log10|own delta N2 - file delta N2| = 1099.0898
    α4 thesis decimals read 330 matching mine from file value (N2) for 330
    δ4 thesis decimals read 661 matching mine from file value (N2) for 324
    delta thesis digits in block 648
    delta_4 thesis block matches file value for 324 decimals of 648

Reading of the numbers.
- Fixed-point residual over 31 points: 1.27e-1092 (1070 terms) and 1.26e-1100 (1100 terms). Eigen-equation residual (L psi - delta psi) with delta taken from the file: 3.5e-1088 and 1.1e-1099. All below the claimed 1e-1087.
- alpha_4 from phi(1): the two resolutions agree to -log10|difference| = 1085.98, i.e. 1085 decimals. delta_4: 1084.21, i.e. 1084 decimals measured (a pure string-prefix count gives 1082 because of a run of digits near the boundary, which is why the claim says 1082 claimed, 1084 measured). My own delta from the eigen-ratio at u = 1/2 agrees with the file's delta_4_N2 to 1e-1099.
- Comparison with the thesis excerpt (the-record-we-beat/thurlby_table_4_6_excerpt.txt, digits transcribed from the PDF text): all 330 transcribed decimals of alpha_4 match my value; the delta_4 block matches for its 324 transcribed decimals (the further characters my script read were the table caption). OEIS A195102: the 49 data digits equal the leading digits of |alpha_4| (author's checker prints the same).
- Resolution gap: (1100 - 1070) / 1070 = 2.80 percent, above the required 2 percent.

## Author's checker, run only afterwards

sh verify-it-yourself/run_checks.sh, lines that matter:

    == reassemble the object from its 6 numbered parts and check sha256 (whole file first)
    whole file sha256 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6 ; PARTS.sha256 says 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6 ; INDEX.csv says 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6 ; parts checked: 6, bad: 0
    == z4_check.py: fixed-point and eigenfunction residuals at 1300 digits, two resolutions (about 30 s)
    fixed-point residuals phi(u)*phi(1) - phi(v) at 31 points: largest in absolute value 1.309e-1092
    eigen-equation residuals (L psi)(u) - delta psi(u) at the same 31 points: largest in absolute value -7.682e-1088
      psi(0) = 1.00000000000000000000 ; largest |psi(u)| at the test points 1.000
    fixed-point residuals phi(u)*phi(1) - phi(v) at 31 points: largest in absolute value -1.264e-1100
    eigen-equation residuals (L psi)(u) - delta psi(u) at the same 31 points: largest in absolute value -8.762e-1100
      psi(0) = 1.00000000000000000000 ; largest |psi(u)| at the test points 1.000
    |alpha_N1 - alpha_N2| ~ 1e-1086   decimals agreeing: 1085
    |delta_N1 - delta_N2| ~ 1e-1085   decimals agreeing: 1084
    worst fixed-point residual over both resolutions ~ 1e-1092; worst eigen-equation residual ~ 1e-1088
    claimed agreeing decimals: alpha 1085, delta 1082; measured: alpha 1085, delta 1084
    Thurlby thesis table 4.6, alpha_4: 330 decimals transcribed; leading characters equal to this computation: 332 of 332
    Thurlby thesis table 4.6, delta_4: 324 decimals transcribed; leading characters equal to this computation: 326 of 326
    OEIS A195102 data: 49 digits, leading digits equal to |alpha_4| of this computation: 49
    elapsed 31.5 s
    RESULT PASS
    negative control rejected as expected: worst fixed-point residual over both resolutions ~ 1e-900; worst eigen-equation residual ~ 1e-898
    ALL CHECKS PASS

Author and I agree on every residual order of magnitude and on the agreement counts 1085 / 1084 (they use the same equations; my code and conventions were written independently and the conventions were derived from the data as described).

## Limits, and answers to open questions concerning reproduction

- Residuals at 31 points are evidence, not a proof of an error bound (open question 1). What I confirm exactly is that both certificates satisfy the two equations at 31 points to the stated orders and that the two resolutions agree on the derived constants to 1085 / 1084 decimals; I do not prove that the equation has no nearby spurious solutions or that no eigenvalue larger than delta_4 exists (open question 3). The agreement of alpha_4 and delta_4 with the thesis's proven digits (330 and 324 decimals) is the supporting evidence that the equations and the eigenvalue are the right ones (open question 2).
- Open question 4: claimed 1082 for delta_4, measured 1084 (numerically 1084.21); both exceed 1000 as p2 requires. The sign of alpha_4 is negative in my equations and the file prints its magnitude, as OEIS does.
- Open question 5 (newer literature) is not a reproduction question.

pass: true
