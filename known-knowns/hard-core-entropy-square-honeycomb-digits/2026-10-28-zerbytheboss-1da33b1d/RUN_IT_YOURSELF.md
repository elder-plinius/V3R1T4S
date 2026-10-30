# Run It Yourself

## 1. Quick Verification (< 1s)
Run the standalone certificate verifier:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified 65 certified decimals of A085850: 1.5030480824753322643220663294755536893857810386103050620281017359
Verified agreement with 40 published digits of OEIS A085850: OK
Verified settlement of Baxter's flagged digits (decimals 41-43 = '810'): OK
Verified Collatz-Wielandt certificates for W=16, 18, 20 (gap < 1e-50): OK
Verified exact reproduction of OEIS A006506 for n=1..12: OK
PASS
```

## 2. Full Rebuilding (< 5 minutes)
Requires Python 3 with `mpmath` and `numpy`:

```sh
python3 how-we-built-it/baxter_ctm_solver.py
python3 how-we-built-it/cylinder_strip_solver.py
```
