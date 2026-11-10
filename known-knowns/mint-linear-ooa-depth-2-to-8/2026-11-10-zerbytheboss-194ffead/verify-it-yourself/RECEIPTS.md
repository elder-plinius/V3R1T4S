# Verification Receipts — `2026-11-10-zerbytheboss-194ffead`

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Output (`exit 0`):

```text
Calibration (negative corrupted 8x16 copy rejected): OK
Rao/Hamming bound for k=8 verified: M >= 7457 > 3^8 = 6561 (so t >= 1, k <= 7)
Matrix ranks and orthogonality: rank(G)=8, rank(H)=8, G*H^T = 0 (mod 3): OK
Primal OOA check: all 1016 left-justified selections (sum d_i = 7) have rank 7 over F_3: OK
Dual NRT check: all 6560 nonzero codewords have RT weight >= 8 (d_RT = 8): OK
Comparison vs live MinT (b=3, T=2, m=8, s=8): k = 7 > 6 (t = 1 < 2), matching Rao bound t = 1
PASS
```
