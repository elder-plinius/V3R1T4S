# Run It Yourself — `2026-11-10-zerbytheboss-194ffead`

## 1. Verify the Claimed Object (`< 1` second, Python 3.8+ stdlib only)

From the package root folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
Calibration (negative corrupted 8x16 copy rejected): OK
Rao/Hamming bound for k=8 verified: M >= 7457 > 3^8 = 6561 (so t >= 1, k <= 7)
Matrix ranks and orthogonality: rank(G)=8, rank(H)=8, G*H^T = 0 (mod 3): OK
Primal OOA check: all 1016 left-justified selections (sum d_i = 7) have rank 7 over F_3: OK
Dual NRT check: all 6560 nonzero codewords have RT weight >= 8 (d_RT = 8): OK
Comparison vs live MinT (b=3, T=2, m=8, s=8): k = 7 > 6 (t = 1 < 2), matching Rao bound t = 1
PASS
```

## 2. Rebuild the Object from Scratch (`~2` seconds, standard C99 compiler)

From the package root folder:

```sh
cc -O3 -std=c99 how-we-built-it/search_ooa_f3.c -o search_ooa_f3
./search_ooa_f3
rm -f search_ooa_f3
```

`search_ooa_f3.c` fixes a canonical `GL_8(F_3)` basis prefix across the first `floor(k/2) = 3` blocks plus block 3's first column, maintains an exact `3^8 = 6,561`-element minimum-selection-cost dynamic-programming table over `F_3^8`, restricts candidates to projective representatives in `PG(7, 3)`, and finds the explicit `OOA(3^8, 8, F_3, 2, 7)` on deterministic Xorshift64 restart `10`.
