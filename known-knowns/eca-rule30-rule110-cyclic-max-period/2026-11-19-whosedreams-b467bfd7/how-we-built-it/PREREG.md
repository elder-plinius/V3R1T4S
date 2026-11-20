# PREREG — packaging run 2026-11-19-eca37-pack, eca-rule30-rule110-cyclic-max-period, A204371(37)=4403, main success criterion (frozen 2026-11-19T01:35:16Z, date -u)

null_test: not needed because the claim is one exact sequence term plus a witness state, checked by deterministic iteration and by agreement of two exhaustive implementations against a live table; there is no score or statistic to beat chance.

## Honesty note: this plan is written after the fact
The exhaustive n=37 search already ran, on 2026-11-18, on a Ryzen 9900X machine with about 53 GB under WSL2, and the send-back (result files, witnesses, and self-test log) already exists. The two implementations and their small-n self-test were written earlier, in a 2026-11-03 groundwork run. That work never froze a PREREG.md before measuring n=37. This file does not pretend otherwise: it is written now, before this packaging run copies the already-computed term and witness in, to freeze how THIS run judges the already-built claim. The claimed numbers (A204371(37)=4403 and witness 0x1c7dbbb23e) were already known when this was written. A live OEIS refetch of A204371 was required, and was done, immediately before packaging; if n=37 had already been listed, the claim would have been dropped.

## Criterion
Main success criterion, verbatim in TARGET_CRITERION.md: the exact value of A204371(37) from an exhaustive search over all 2^37 states, or over all rotation orbits with the rotation factor accounted for, run by two independent implementations that agree; both must reproduce A334497(1..24) and A204371(1..30) exactly and both must report A334497(25..30); a witness on the maximal cycle must be given; bit order must follow the Wolfram convention; the term must not already be in the live OEIS entry at claim time. Partial wins p1 and p2 are not sought in this package.

## Checkers and thresholds
1. Independent checker (verify-it-yourself/check_period.py, standard-library Python): re-iterate witness 0x1c7dbbb23e under Rule 110 at width 37, Wolfram bit order (cell 0 = LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic), and require a return at step 4403 with no shorter period among the divisors of 4403 (1, 7, 17, 37, 119, 259, 629, 4403).
2. Agreement of the two shipped implementations on n=37: both result files must say max_period=4403 and witness=0x1c7dbbb23e. The programs themselves (how-we-built-it/impl1/maxcycle.c and how-we-built-it/impl2/maxcycle.c) are the exhaustive search: impl1 marks rotation orbits and converts an orbit return into a state period; impl2 walks every state with a 3-colour scheme and no rotation folding. Reflection is not used.
3. Self-test record in how-we-built-it/selftest/: both implementations reproduce A334497(1..24) and A204371(1..30) exactly (no BUG or MISMATCH lines) and both report A334497(25..30). A value below a listed term would have been treated as a bug.
4. Live table (the-record-we-beat/RECORD.md): pass only if A204371(37) is absent from the live OEIS entry and b-file at fetch time.
5. Held-out width, as the bank verification method asks: re-run both implementations at Rule 110, n=31, and require agreement with the listed term A204371(31)=2759.
6. Note, honestly, that 4403 equals the single-cell floor A180001(37). Equality with that floor is allowed; the exhaustive search is what shows that no longer cycle exists.

Status allowed: CONFIRMED_SOLUTION only if checks 1 to 6 pass, a three-skeptic panel (fresh contexts) all end pass: true, the gate copies the criterion panelist's confirmed_scope exactly, and kit/check_run.py prints CHECK_RUN: PASS. Otherwise at most PROMISING. This packaging run writes PROMISING and does not stamp CONFIRMED_*.
