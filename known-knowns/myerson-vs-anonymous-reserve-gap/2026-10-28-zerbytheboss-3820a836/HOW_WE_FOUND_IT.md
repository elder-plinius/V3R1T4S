# How We Found It — `myerson-vs-anonymous-reserve-gap`

contributor text, unverified

## Investigation Brief
The Hartline-Roughgarden conjecture posited that second-price auctions with the best anonymous reserve guarantee at least a 1/2 fraction of Myerson's optimal auction revenue (OPT/AR <= 2). Jin, Lu, Tang, and Xiao (SODA 2019, arXiv:1804.00480, JLTX) refuted this conjecture by introducing a triangular equalisation construction with 4 buyers achieving OPT/AR ~ 2.1596. However, their 4-buyer parameters were rounded to four decimals and evaluated numerically. Subsequent work by Feng and Jin (arXiv:2411.03583v1, Result 3 and Theorem 7) inherited the 0.4630 bound from JLTX and explicitly noted that the exact maximum gap remains open. The bank set a certified bar of 2.1600 over all reserves r >= 0.

## Method & Results
1. **Calibrated Baseline**: We implemented the JLTX triangular equalisation recursion from first principles, verifying the 3-buyer instance (OPT = 2.1361) and 4-buyer instance (OPT = 2.1596) to four decimal places.
2. **5-Buyer Construction**: We formulated the equalisation conditions where each buyer's distribution is a triangular distribution Tri(v_i, q_i) with exact rational cutoffs and atom probabilities. By expanding the recursion to 5 buyers (including Tri(inf) as buyer 0), we optimized the parameter vector to satisfy AR(v_i) <= 1 for all candidate cutoffs while maximizing OPT = sum_i v_i q_i prod_{j<i}(1 - q_j).
3. **Exact Certificate**: We proved that the second-price payment integrand 1 - D2(x) admits a closed-form partial fraction decomposition with rational residues. By JLTX Lemma 9, virtual valuations are negative below cutoffs, guaranteeing AR'(p) >= 0 on each interval between cutoffs. Thus, checking AR(v_i) at the finite cutoffs bounds AR over ALL r >= 0. Evaluated in 50-digit interval arithmetic, max AR <= 0.99999528 < 1.0 while exact rational OPT = 108154841521/50000000000 > 2.1630. This rigorously certifies OPT/AR >= 2.16310706 >= 2.16000000.
4. **Scaling Behavior**: We scaled the recursion to n = 5..25 buyers. The ratio peaks at n=6 with OPT ~ 2.163604, confirming the robustness of the triangular equalisation family.
