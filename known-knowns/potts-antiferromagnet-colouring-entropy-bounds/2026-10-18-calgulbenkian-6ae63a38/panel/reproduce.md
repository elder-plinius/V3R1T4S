# potts-wsq4-ub: reproduce report

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

## Hash check
The package folder matched the contributor's hash list (49 entries, all OK). The folder was copied to a private location and the work done on the copy. The parts were concatenated and the whole file has sha256 6ae63a3870e719d855663cc81e6517880c282a8bcb773dc2f26a7d32cd8bdf01, equal to PARTS.txt.

## Definition (quoted from object/BOUND.md) and what I checked
"the states are the proper colourings w of a cycle C_m of m vertices (w_i != w_(i+1 mod m)), and T[w, w'] = 1 exactly when w' is also proper on the cycle and w_i != w'_i for every i (vertical neighbours differ), else 0." with q=4, m=18. Collatz-Wielandt: "for a nonnegative ... matrix M and any vector v with all entries positive, theta_1(M) <= max_i (M v)_i / v_i."

The certificate is a vector on symmetry orbits. I did NOT use the quotient matrix or the equitable-partition assertion. I lifted v to every proper colouring of C_18 and applied the FULL transfer matrix T of the definition:

1. My own C program (written from the definition before reading any of the author's code; not shipped in this package) enumerates all proper colourings up to colour relabelling (restricted-growth strings), computes each orbit under S_4 x D_18 as the lexicographic minimum over the 2m dihedral images after relabelling, numbers the orbits in lexicographic order of their minima, and lifts v (read from the file as little-endian 256-bit integers) to every colouring by orbit. Orbit count: 451929 found by my enumeration, 451929 in the file (equal).
2. For every orbit representative w it enumerates EVERY proper w' with w'_i != w_i for all i (depth-first, exhaustive, no sampling; about 4e6 leaves per orbit) and sums the lifted v over them in exact integer arithmetic (4 x 128-bit accumulators, normalised to 5 limbs, overflow-checked). This gives (T v)(w) exactly. Because T commutes with S_4 x D_18 and v is invariant, (T v) is constant on orbits, so the orbit representatives give every ratio of the full 387420492-state matrix.
3. Format validation first: the same program reproduced the author's y = C v exactly on all six small example certificates (q4_cyl_6/8/9), 0 mismatches.
4. On the real certificate my S equals the file's y in all 451929 orbits (log line "orbits where own S != certificate y: 0" below). So y is correct, not merely assumed.
5. A Python script of mine (run with -I, Fractions) then reads my S and v: all v strictly positive; C_hi = max_i S_i/v_i computed as an exact rational; the bound U is the least 40-decimal number with U^18 >= C_hi, found by exact integer comparison (outward rounding, upward); its 20-decimal upward rounding is compared to the claim.

## My run (command and real output)
Command: (own C program, run on the concatenated certificate with q = 4, width 18; 27 threads; wall time about 38 minutes)
Program log (progress lines removed):
    q=4 m=18 proper RGS count N=16142521
    orbits found by own enumeration: 451929 ; orbits in certificate: 451929
    orbits where own S != certificate y: 0

Command: (own Python script, run on the program output for width 18 with the published bound 2.33606820555777)
Output:
    orbits: 451929 ids contiguous: True
    all v > 0: True  min v bits: 221  max v bits: 224
    argmax orbit 330432 argmin orbit 0
    C_hi = max (Cv)_i/v_i exactly = 10308110743659294181213305847653233613093647112644826588240099466940532396 / 2401410699841922024469331521067244028233344603985234653291323144461
    C_hi (decimal 40 digits): 4292523.0342056223587157719556590059728848958444
    C_lo = min ratio (decimal 40): 4292523.0342056223587157719556590059728848958444
    C_hi - C_lo (float): 2.6071006129789558e-45  relative: 6.073585609684277e-52
    W <= C_hi^(1/m) <= (outward rounded UP, 40 decimals): 2.3360602265554583581403491124455588569046
       (rounded down, 40 decimals): 2.3360602265554583581403491124455588569045
    outward rounded UP at 20 decimals: 2.33606022655545835815
    published bound: 2.33606820555777  improvement (published - rounded-up claim) = 7.97900231164186e-06  >= 1e-9 : True
    exact check, margin as Fraction >= 1e-9: True

## Author's checker (run only after mine)
sh verify-it-yourself/run_checks.sh exit 0 and "ALL CHECKS PASS" (its output is not shipped separately). It agrees with my numbers: the same C_hi bound digits. Note the author's check_cert.py trusts y; my checker recomputed y independently, so mine is the stronger check. No disagreement.

## Result
Exact Collatz-Wielandt check on the full transfer matrix of proper 4-colourings of C_18 passes: v > 0 everywhere, max ratio C_hi equals the rational shown (min ratio equals it to 6e-52 relative, so v is an almost exact Perron vector), and W_sq(4) <= C_hi^(1/18) <= the upper-rounded decimal above. Improvement over the quoted published bound exceeds the 1e-9 margin (value above).

Note on the claimed digits: The claim states 2.33606022655545835814... (truncation); the upward 20-decimal rounding is ...835815, so the claim is a truncation of the true value (...8140349), not an overstatement; the 40-decimal upward value above is the rigorous bound.

## Limits
- The inequality W_sq(q) <= theta_1(C_m)^(1/m) for even m (Lundow and Markstrom 2008, "Theorem 2.2" per the author) is a cited theorem; the paper is not in the folder and I did not re-derive or check it. The numerical part (theta_1(C_18) <= C_hi) is what I verified. Whether the cited inequality's hypotheses hold for m = 18 is left to the criterion skeptic.
- Novelty and criterion wording were not judged.
- Determinism: output is exact integer arithmetic, independent of thread order.

pass: true
