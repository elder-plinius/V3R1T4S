# Verification Receipts — `[[19, 2, 11; 9]]_2`

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
Negative control rejected single-bit stabilizer perturbation (cross_orth=False, d_pert=8).
Verified S shape = 26 x 38, rank_GF2(S) = 26, rank_GF2(S Omega S^T) = 18 => n=19, k=2, c=9.
Enumerated all 2^12 = 4096 vectors in S^{perp_s}: |S cap S^{perp_s}| = 256 (min nonzero radical weight = 4), |S^{perp_s} \ S| = 3840.
Coset weight distribution: [(11, 192), (12, 528), (13, 408), (14, 1152), (15, 552), (16, 528), (17, 360), (18, 96), (19, 24)]
Exact non-catalytic d_EA = 11 > 10 = d_lower(19, 2, 9) (degenerate EAQECC: d_EA = 11 > 4 = d(S^{perp_s})); Griesmer bound rules out all l' in {0, 1, 2} classical (non-degenerate) quaternary hull ancestors.
PASS
```
