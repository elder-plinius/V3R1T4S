# NOTES interval-mishra (lens): literal outward-rounded interval replay of Mishra cert_B_08344

Hypotheses (guessed chance that the idea works / cost), cheapest decisive first:
1. H1 (70%, cost low): a struct Iv{lo,hi} widened by BitDecrement/BitIncrement on every + - * / sqrt, dropped into the leaf path of the previous C# verifier, passes all leaves; interval slack >> widening (old worst slack 3.4e-6 vs interval widths ~1e-15).
2. H2 (60%, low): trig by interval Horner + explicit Lagrange remainder (degree 10 in x^2, remainder <= 7e-21 on [0,1.3]) is tight enough that the corner enclosures stay ~1e-15 wide.
3. H3 (50%, medium): child-covers-parent can be certified per split by Iv comparison of the DIFFERENCES (c-cL) vs (h-hL) (cancellation-free: Iv widths scale with the half-width, not with |c|), margin half*1e-11 >= 8.5e-16 vs rounding e1 <= 1.1e-16.
4. H4 (80%, low): heuristic selectors (Math.Acos/Atan2/Cos/Sin, dot-product argmax, adaptive refinement) are harmless if every point they emit is re-certified by Iv membership; only cost is some lost points.
5. H5 (outside field: numerical analysis / verified computing, INTLAB-style, 60%): ball arithmetic would be 2x faster than endpoint intervals; not needed unless speed is a problem.
6. H6 (outside field: proof-carrying code / certificate checking, 40%): exact rational check (BigInteger) of a sample of leaf polygons as independent confirmation of the interval verdict; cost medium; delegated to second-checker lens.
7. H7 (strange, 15%, cost low): the interval checker finds a failing leaf because inflate 1e-11 coverage margin is too thin at the smallest boxes (half 8.5e-5 -> g = 8.5e-16) -> would be a (cosmetic) coverage defect of the certificate generator.
8. H8 (30%, low): rho top-end coverage, the double 2*fl(pi/5) falls short of 2pi/5 by ~1e-16 and is only rescued by the 1e-11 inflation of top seeds; Iv check of the 524,288 top seeds confirms.
9. H9 (strange, 10%): tau decimal vs header double: a verdict flips if comparison uses double tau instead of enclosure of 8344/10000 + 1e-12; handled by threshold = upper bound of max(tau_header, tau_decimal)+1e-12.
10. H10 (45%, medium): full run of 245,496,952 leaves in <= 4.5h on 6 threads (old double run 66.5 min; endpoint-interval ops 2-3x slower expected).

## Process log
- Iv.cs, IvConsts.cs (gen_ivconsts.py, mpmath.iv 70 digits), Core.cs (Ctx rewritten on Iv), Program.cs (LeafBound, FLower, Cover, header, seed checks) in code/LebVerifyI/
- Unit test: `ivtest` emits 20000x(add,sub,mul,div,sqr,sqrt,sin10,cos10,sin7) + constants -> ivtest_check.py (Fractions / mpmath.iv).

## Results log (appended)
- Full run PID 3720 (5 threads, BelowNormal), 149.14 min, RESULT VERIFIED, 486,799,600 / 245,496,952 / 0 failing. Worst slack 3.426674e-06.
- H1 confirmed (all leaves pass). H2 confirmed (trig widths ~1.5e-15, unit tests). H3 confirmed (0 cover failures). H4 confirmed. H7/H8 not triggered (no coverage defect). H9: threshold = upper end of max(tau_header, enclosure of 8344/10000)+1e-12. H10: 149 min on 5 threads.
- No PID left running.
