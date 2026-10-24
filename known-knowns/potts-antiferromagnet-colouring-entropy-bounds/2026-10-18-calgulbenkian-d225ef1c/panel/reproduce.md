# potts-wsq5-ub: reproduce report

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

## Hash check
The package folder matched the contributor's hash list (22 entries, all OK). The folder was copied to a private location and the work done on the copy. The parts were concatenated and the whole file has sha256 d225ef1cf4f8f3c335620d5c7e37c5d96afa60cdc47b228acce51b66065a91e1, equal to PARTS.txt.

## Definition (quoted from object/BOUND.md) and what I checked
"the states are the proper colourings w of a cycle C_m of m vertices (w_i != w_(i+1 mod m)), and T[w, w'] = 1 exactly when w' is also proper on the cycle and w_i != w'_i for every i (vertical neighbours differ), else 0." with q=5, m=14. Collatz-Wielandt: "for a nonnegative ... matrix M and any vector v with all entries positive, theta_1(M) <= max_i (M v)_i / v_i."

The certificate is a vector on symmetry orbits. I did NOT use the quotient matrix or the equitable-partition assertion. I lifted v to every proper colouring of C_14 and applied the FULL transfer matrix T of the definition:

1. My own C program (written from the definition before reading any of the author's code; not shipped in this package) enumerates all proper colourings up to colour relabelling (restricted-growth strings), computes each orbit under S_5 x D_14 as the lexicographic minimum over the 2m dihedral images after relabelling, numbers the orbits in lexicographic order of their minima, and lifts v (read from the file as little-endian 256-bit integers) to every colouring by orbit. Orbit count: 81433 found by my enumeration, 81433 in the file (equal).
2. For every orbit representative w it enumerates EVERY proper w' with w'_i != w_i for all i (depth-first, exhaustive, no sampling; about 1.5e7-ish leaves per orbit) and sums the lifted v over them in exact integer arithmetic (4 x 128-bit accumulators, normalised to 5 limbs, overflow-checked). This gives (T v)(w) exactly. Because T commutes with S_5 x D_14 and v is invariant, (T v) is constant on orbits, so the orbit representatives give every ratio of the full 268435460-state matrix.
3. Format validation first: the same program reproduced the author's y = C v exactly on all six small example certificates (q5_cyl_6/7/8), 0 mismatches.
4. On the real certificate my S equals the file's y in all 81433 orbits (log line "orbits where own S != certificate y: 0" below). So y is correct, not merely assumed.
5. A Python script of mine (run with -I, Fractions) then reads my S and v: all v strictly positive; C_hi = max_i S_i/v_i computed as an exact rational; the bound U is the least 40-decimal number with U^14 >= C_hi, found by exact integer comparison (outward rounding, upward); its 20-decimal upward rounding is compared to the claim.

## My run (command and real output)
Command: (own C program, run on the concatenated certificate with q = 5, width 14; 28 threads; wall time about 25 minutes)
Program log (progress lines removed):
    q=5 m=14 proper RGS count N=2238328
    orbits found by own enumeration: 81433 ; orbits in certificate: 81433
    orbits where own S != certificate y: 0

Command: (own Python script, run on the program output for width 14 with the published bound 3.250407145038276)
Output:
    orbits: 81433 ids contiguous: True
    all v > 0: True  min v bits: 223  max v bits: 224
    argmax orbit 80146 argmin orbit 74525
    C_hi = max (Cv)_i/v_i exactly = 70527689875082357677159322222225331322003283177851297924316568940791733691 / 4799926535208162933632183472881474187716556614045961155232665021516
    C_hi (decimal 40 digits): 14693493.6103191247992568599424794513959236209793
    C_lo = min ratio (decimal 40): 14693493.6103191247992568599424794513959236209793
    C_hi - C_lo (float): 1.6431131415882124e-60  relative: 1.1182589962364477e-67
    W <= C_hi^(1/m) <= (outward rounded UP, 40 decimals): 3.2504052058785496850598045891913500783901
       (rounded down, 40 decimals): 3.2504052058785496850598045891913500783900
    outward rounded UP at 20 decimals: 3.25040520587854968506
    published bound: 3.250407145038276  improvement (published - rounded-up claim) = 1.93915972631494e-06  >= 1e-9 : True
    exact check, margin as Fraction >= 1e-9: True

## Author's checker (run only after mine)
sh verify-it-yourself/run_checks.sh exit 0 and "ALL CHECKS PASS" (its output is not shipped separately). It agrees with my numbers: the same C_hi bound digits. Note the author's check_cert.py trusts y; my checker recomputed y independently, so mine is the stronger check. No disagreement.

## Result
Exact Collatz-Wielandt check on the full transfer matrix of proper 5-colourings of C_14 passes: v > 0 everywhere, max ratio C_hi equals the rational shown (min ratio equals it to 1e-67 relative, so v is an almost exact Perron vector), and W_sq(5) <= C_hi^(1/14) <= the upper-rounded decimal above. Improvement over the quoted published bound exceeds the 1e-9 margin (value above).

Note on the claimed digits: The claimed 3.25040520587854968506... equals the upward 20-decimal rounding.

## Limits
- The inequality W_sq(q) <= theta_1(C_m)^(1/m) for even m (Lundow and Markstrom 2008, "Theorem 2.2" per the author) is a cited theorem; the paper is not in the folder and I did not re-derive or check it. The numerical part (theta_1(C_14) <= C_hi) is what I verified. Whether the cited inequality's hypotheses hold for m = 14 is left to the criterion skeptic.
- Novelty and criterion wording were not judged.
- Determinism: output is exact integer arithmetic, independent of thread order.

pass: true
