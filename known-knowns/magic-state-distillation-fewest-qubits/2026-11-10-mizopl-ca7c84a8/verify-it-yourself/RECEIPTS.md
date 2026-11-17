# Verification Receipts (`magic-state-distillation-fewest-qubits`)

## 1. Object & Verifier Hashes

- `object/constructive_tightness_witnesses.json` sha256: `156cd6beb1c5740ef857caaabfca42896de2dff40ec6e8e2c8ca533fd782bb6b` (`47300` bytes)
- `object/p1_p2_lower_bound_certificates.json` sha256: `ca7c84a8ae14e82d353d8d6b5d101fe96cd32972718c53bdc94075d7dddb33c4` (`384330` bytes)
- `verify-it-yourself/verify.py` sha256: `24ff528e8d82ef9e4ff02081324874a5cd47e8727f4cee13ea157aebcaae5278` (`35009` bytes)

## 2. Clean Verification Run (`sh verify-it-yourself/run_checks.sh`)

```text
$ sh verify-it-yourself/run_checks.sh
[OK] Verified all 6 constructive tightness witnesses (W1..W6: exact F_2 Eqs. 18/19 & 40/42, Master Theorem 3a hyperplane parity split, and Master Theorem 4 parity-extension lift)
[OK] Verified Milestone p1 (N_CCZ(4) = 10 & N=7 T-to-T control across all 4,194,304 RM(2,6) codewords and 912 pointed supports)
[OK] Verified Milestone p2 (N_T(4) >= 9 across all 3,486 RM(3,7) orbits, 6,074,355 disjoint pairs, 2^64 orbit mass, and 446,208 shifted supports)
PASS
```

## 3. Adversarial Corruption Check (`python3 verify-it-yourself/verify.py --corrupt`)

```text
$ python3 verify-it-yourself/verify.py --corrupt
VERIFICATION ERROR: W1_48T_to_1CCZ_N10_d4: failed T-to-CCZ check: row 0 not orthogonal to check row 1
FAIL
(exit code: 1)
```
