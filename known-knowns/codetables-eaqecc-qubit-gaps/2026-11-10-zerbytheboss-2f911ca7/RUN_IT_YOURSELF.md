# Run It Yourself

## 1. Verify the Stabilizer Matrix From Definition (`< 1` second)

From this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
Negative control rejected single-bit stabilizer perturbation (cross_orth=False, d_pert=8).
Verified S shape = 26 x 38, rank_GF2(S) = 26, rank_GF2(S Omega S^T) = 18 => n=19, k=2, c=9.
Enumerated all 2^12 = 4096 vectors in S^{perp_s}: |S cap S^{perp_s}| = 256 (min nonzero radical weight = 4), |S^{perp_s} \ S| = 3840.
Coset weight distribution: [(11, 192), (12, 528), (13, 408), (14, 1152), (15, 552), (16, 528), (17, 360), (18, 96), (19, 24)]
Exact non-catalytic d_EA = 11 > 10 = d_lower(19, 2, 9) (degenerate EAQECC: d_EA = 11 > 4 = d(S^{perp_s})); Griesmer bound rules out all l' in {0, 1, 2} classical (non-degenerate) quaternary hull ancestors.
PASS
```

## 2. Rebuild the Code From Scratch (`< 2` seconds)

Compile and run the deterministic C99 solver (`how-we-built-it/search_gf4_hull.c`, fixed Xorshift64 seed `0x243f6a8885a308d3ULL`):

```sh
cc -O3 -std=c99 -Wall -Wextra how-we-built-it/search_gf4_hull.c -o search_gf4_hull
./search_gf4_hull
```

It prints `HIT! [[19, 2, 11; c=9]]_2` and writes `hit_n19_k2_d11_c9.tsv` after passing internal binary RREF, symplectic Gram rank, and full `4,096`-vector dual enumeration checks.
