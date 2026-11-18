# Skeptic 1 — Reproducibility, Exhaustive Oracle Evaluation & Mutation Audit (`reproduce.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `nist-aes-circuit-records`
- `command_checked`: `sh verify-it-yourself/run_checks.sh`
- `corrupt_checked`: `sh verify-it-yourself/run_checks.sh --corrupt`

## Audit Findings

1. **Standalone Zero-Dependency Verification (`< 0.3s`):** `verify-it-yourself/verify.py` (`sha256: 8cd6e40c4333ee55034766b67030374b33d0a3fd6d69a1be7f00c1eb3eea62c8`) uses only the Python 3 standard library, derives FIPS 197 `SBox()`, `InvSBox()`, and the `32 x 32` `GF(2)` `InvMixColumns` linear map from `GF(2)[x]/(x^8 + x^4 + x^3 + x + 1)` without lookup tables, and verifies all `13` `%NCFF-0.1-2026` circuits in `object/` (`0` `NOT` gates, `0` constants, `0` `u == v` self-inputs, `0` dead gates).
2. **Exact Non-Isomorphism & Sub-Block Tightness (`T1..T6`):** Confirms `72 / 92` overlap (`symdiff = 40`) between the two `92@10` `InvMixColumns` witnesses, `T4` rank-`37/37` + `27/27` feeder Pigeonhole on `152@10`, `T5a` `P = 16` `[6, 45, 643, 33602]` middle Pigeonhole on `111@14`, and `T6` `0 / 2,040` conjugate `Zone_Top` screen on `111@14` and `109@15` against `object/00_nist_aes_gd10_and_barriers_certificate.json` (`sha256: 717e3701dc2a42b9966c099120b68c41b1633773141617d0cf8f97674554305d`).
3. **Corruption Rejection:** Both `sh verify-it-yourself/run_checks.sh --corrupt` and single-byte mutations across all `14` files in `object/` exit `1` with final line `FAIL`.

pass: true
