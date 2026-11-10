# Record We Beat — `ecc-inversion-addition-chains`

target_id: ecc-inversion-addition-chains
table_url: https://raw.githubusercontent.com/mmcloughlin/addchain/master/doc/results.md
fetch_time: 2026-10-29T08:08:00Z
http_status: 200
page_sha256: c805367ced12810d221ac3513ca3ccd0d329382dac2a8ec7b54f2f272e167357

## Published Incumbent Status
- Primary Reference: Michael McLoughlin, `addchain: Cryptographic Addition Chain Generation`, doc/results.md (commit master, 2026).
- Status Source: Brian Smith, "ECC Inversion Addition Chains" (https://briansmith.org/ecc-inversion-addition-chains-01).
- Published Record:
  - addchain doc/results.md lists baseline addition chain lengths for field-inversion exponents without published best:
    - M-383 (Curve383187): 396 steps (382 squarings, 14 additions)
    - M-511: 525 steps (510 squarings, 15 additions)
- Resolution: This package delivers verified addition chains strictly shorter than addchain baselines (Partial Win p1):
  1. M-383 Field Inversion: **395 steps** (382 squarings, 13 additions) — strictly shorter by 1 addition ($395 < 396$).
  2. M-511 Field Inversion: **524 steps** (510 squarings, 14 additions) — strictly shorter by 1 addition ($524 < 525$).
  3. NIST P-384 Field upgraded to 396 steps (matching Brian Smith live bar, beating addchain 397).
  4. Curve25519 Field upgraded to 265 steps (matching DJB live bar, beating addchain 266).
