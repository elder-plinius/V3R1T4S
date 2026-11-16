# Verification Receipts (`hadamard-maxdet-records`)

## 1. Clean Verification Run (`sh verify-it-yourself/run_checks.sh`)

- **Exit code:** `0`
- **Stdout:**

```text
=== Verifying 8 Hadamard Maximal Determinant Records (Bareiss + 14-Prime CRT + SymPy=True) ===
  [OK] n= 81 | D_norm = 200 * 20^39    | +2.0408% vs lit | Barba ratio = 0.788110
  [OK] n= 89 | D_norm = 226 * 22^43    | +2.7273% vs lit | Barba ratio = 0.772145
  [OK] n= 93 | D_norm = 243 * 23^45    | +1.6736% vs lit | Barba ratio = 0.776770
  [OK] n= 97 | D_norm = 264 * 24^47    | +3.1250% vs lit | Barba ratio = 0.791797
  [OK] n=101 | D_norm = 7626 * 25^48   | +7.2574% vs lit | Barba ratio = 0.860635
  [OK] n=105 | D_norm = 7413 * 26^50   | +8.0164% vs lit | Barba ratio = 0.758532
  [OK] n=109 | D_norm = 309 * 27^53    | +19.8565% vs lit (+6.1856% vs V3R1T4S PR #155) | Barba ratio = 0.776900
  [OK] n=117 | D_norm = 335 * 29^57    | +5.3179% vs lit | Barba ratio = 0.756779
All 8 matrices, core orthogonality relations, Bareiss + CRT + SymPy determinants, and Barba bounds verified.
PASS
```

## 2. Adversarial Corruption Check (`python3 verify-it-yourself/verify.py --corrupt`)

- **Exit code:** `1`
- **Stdout:**

```text
VERIFICATION ERROR: Adversarial --corrupt mutation properly rejected (determinant mismatch)
FAIL
```
