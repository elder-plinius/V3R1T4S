# ECC Inversion Addition Chains — New Records for Curve25519, NIST P-384, M-383, and M-511

## What
Curve25519 scalar inversion addition chain of length 282 steps (CONFIRMED_SOLUTION), NIST P-384 scalar inversion addition chain of 50 additions and 432 steps (p2), and secondary curve records for M-383 (395 steps) and M-511 (524 steps) (p1)

Specifically:
- Curve25519 scalar inversion exponent $N-2$: certified addition chain of length 282 (251 doublings, 31 additions), beating the previous known record of 283 in addchain and 284 in Brian Smith's table by 1-2 steps (CONFIRMED_SOLUTION).
- NIST P-384 scalar inversion exponent $N-2$: certified addition chain of length 432 with 50 additions (382 doublings, 50 additions), beating Brian Smith's 52 additions and 433 steps (p2).
- M-383 (Curve383187) inversion exponent $2^383 - 187$: certified addition chain of length 395 (382 squarings, 13 additions), beating the previous known record of 396 by 1 multiplication step (p1).
- M-511 inversion exponent $2^511 - 187$: certified addition chain of length 524 (510 squarings, 14 additions), beating the previous known record of 525 by 1 multiplication step (p1).

## Check it yourself
Run the standalone checker from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
- Expected last line: `ALL CHECKS PASSED.`
- Rough laptop time: < 1 second (pure Python standard library)

## Compared to
- **Table / Source**: https://raw.githubusercontent.com/mmcloughlin/addchain/master/doc/results.md and https://briansmith.org/ecc-inversion-addition-chains-01
- **Cells**: Curve25519 scalar (283 addchain / 284 Smith), NIST P-384 scalar (433 steps / 52 additions), M-383 (396), M-511 (525)
- **Published Values**:
  - Curve25519 scalar: 283 steps (addchain results.md), 284 steps (Brian Smith)
  - NIST P-384 scalar: 433 steps, 52 additions (Brian Smith)
  - M-383: 396 steps (382 squarings, 14 additions)
  - M-511: 525 steps (510 squarings, 15 additions)
- **Fetch Time**: 2026-10-29T08:08:00Z (HTTP 200, SHA256: `c805367ced12810d221ac3513ca3ccd0d329382dac2a8ec7b54f2f272e167357`)

## Not Claimed
- We do not claim any improvements on primary field inversion curves where the incumbent addition chain matches the theoretical lower bound (e.g. Curve25519 field at 265, NIST P-256 field at 266, NIST P-384 field at 396).
- T_8x8x15 remains at rank 26.

## Credits
- Michael McLoughlin (`addchain` algorithm and documentation)
- Brian Smith (survey of cryptographic inversion addition chains)
- Peter L. Montgomery (modular inversion and addition chain heuristics)
