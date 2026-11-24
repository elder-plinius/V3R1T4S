# CW(208,81) does not exist

## What

Original panel-confirmed scope:

> No circulant weighing matrix CW(208,81) exists, because every sequence fixed by multiplication by 3 was enumerated and none has periodic autocorrelation 0 at every nonzero shift.

Here “every sequence” means all candidates satisfying the weight-81 contraction constraints, as derived in PROOF.md; the all-zero row is not a candidate.

No circulant weighing matrix CW(208,81) exists: no length-208 row over {-1,0,1} of weight 81 has zero periodic autocorrelation at every nonzero shift. The prime-power multiplier theorem makes the multiplication-by-3 invariant family sufficient for the entire existence question. An exact exhaustion of that family finishes with zero solutions. This is a nonexistence result for one parameter pair, not a new construction or general classification.

See PROOF.md for the normalization, contraction, orbit partition and completeness argument. Both proper and improper possibilities are included.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Requires Python 3, NumPy, and a C compiler. No network access is used by verification. The compiled executable is temporary; no shipped binary is trusted. See RUN_IT_YOURSELF.md for setup, controls, expected counts and limits.

The command runs verifier regression tests, compares the exact contraction sets from three sources (the object, Python and C), exercises successful and rejected C controls, completes the C search, then runs a separately written exact-integer Python search with known positive and negative controls. Expected final line: PASS.

## Compared to / novelty limitation

Original La Jolla snapshot: key CW(208,9), status Open, comment empty. Fetch 2026-11-13T07:36:30Z, HTTP 200. URL https://raw.githubusercontent.com/dmgordo/circulant-weighing-matrices/main/cwm.json. SHA256 d86aab619852a6e77a1aa3304dcb7e18f6f192b25caa80cdb470dc081815602d. The key uses the square root of the weight: 9 means weight 81. The repository was checked again during the 2026-11-14 review and still marked this entry Open.

No prior resolution or directly applicable short obstruction was found in the literature checked during that review. The result appears to resolve a currently open repository entry; this bounded search is not a guarantee of priority. The multiplier/contraction method is established, not claimed as new. A final live table and competing-claim check is still required immediately before submission.

## Verification revision, 2026-11-14

The original C search and an independently written exact checker agreed on zero solutions. Review nevertheless found a defective, vacuous self-test: stale candidate state contaminated its join setup. The revised self-test explicitly resets state and includes nonempty successful joins and rejected cases. The contraction equations were simplified, and independent case-set comparison, completion checks and calibration were added. These repairs do not change the claim, object or search scope.

The panel files and preregistration are retained as the original run's historical records, not rewritten as if they had reviewed this revision. The novelty wording above qualifies the original panel's categorical language. See verify-it-yourself/RECEIPTS.md for revision verification evidence.

## Not claimed

No first row. No other order. No formal DRAT/LRAT proof or proof-assistant certification. No assertion that a finite literature search establishes novelty conclusively. The seven within-group shifts in the C join are only filters; the complete remaining autocorrelations are checked before accepting a candidate. No request that the external repository be edited.

## Credits and references

- Dan Gordon, La Jolla Circulant Weighing Matrices Repository: https://dmgordon.org/circulant-weighing-matrices/ and https://github.com/dmgordo/circulant-weighing-matrices.
- Ming Ming Tan, Character and Multiplier Obstructions for Circulant Weighing Matrices, https://arxiv.org/html/2608.18468v2, Result 2.3 (multiplier normalization); Theorem 1.1 concerns eight other cases.
- K. T. Arasu, D. M. Gordon and Y. Zhang, New nonexistence results on circulant weighing matrices, Cryptography and Communications 13 (2021), 775–789: https://arxiv.org/html/1908.08447v3, Theorem 2.2 and contraction framework.
- Ming Ming Tan, Group Invariant Weighing Matrices: https://arxiv.org/html/1610.01914. Theorem 4.14 does not exclude this cell: its parameter w is 3 and the required inequality k < w-2 fails at k=9.
- K. T. Arasu, Kyle Bayes and Ali Nabavi, Nonexistence of two circulant weighing matrices of weight 81, Transactions on Combinatorics 4 (2015), 43–52.
- Bernhard Schmidt and Ken W. Smith, Circulant weighing matrices whose order and weight are products of powers of 2 and 3, Journal of Combinatorial Theory A 120 (2013), 275–287; order 208 also involves prime 13, so its restricted classification is not applicable.
