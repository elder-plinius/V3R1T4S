# Pre-Registration — `codetables-eaqecc-qubit-gaps`

- `target_id`: `codetables-eaqecc-qubit-gaps`
- `frozen_utc`: `2026-11-10T18:50:00Z`
- `cell`: `(n, k, c) = (19, 2, 9)` in Markus Grassl's table of binary entanglement-assisted quantum error-correcting codes (`http://www.codetables.de/EAQECC/qubit.php`, non-catalytic setting, `c >= 1`)
- `criterion`: Explicit `(n - k + c) x 2n = 26 x 38` binary stabilizer matrix `S` over `GF(2)` in symplectic layout `[X | Z]` such that an independent Python standard-library verifier confirms: (1) `rank_GF2(S) = 26`, (2) symplectic Gram matrix `S * Omega * S^T` has `rank_GF2(S * Omega * S^T) = 2c = 18` (requiring `c = 9` ebits), and (3) exact full enumeration of all `2^(n + k - c) = 2^12 = 4,096` vectors in the symplectic dual `S^{perp_s}` establishes non-catalytic EA minimum distance `d_EA = min_{v in S^{perp_s} \ (S cap S^{perp_s})} wt_s(v) = 11 > 10 = d_lower(19, 2, 9)` in the live table (`[[19, 2, 10-17; 9]]_2`), with `11 <= 17 = d_upper`.
- `null_test`: `not needed because GF(2) matrix rank, symplectic Gram rank, and exact full enumeration of all 4,096 dual vectors are deterministic finite-field invariants`
