# Closed-Form `[binom(d, e-3)]` Coefficient of the Bond Perimeter Polynomial `D_e(q)`


## What

For bond percolation on Z^d, a constructive computer-assisted derivation, with no fitted parameters, gives the closed form of the binom(d, e-3) coefficient of D_e(q), e >= 4, as q^(2(e+1)d-2e) times six gamma terms (q^0..q^-3, q^-2d, q^-2d-1). It matches the published binom(d, e-3) coefficients of Mertens-Moore D_4..D_11 (48 of 48 numbers) and the published binom(d, 9) entry of D_12(1). It matches an independent brute-force animal enumeration at (d, e) = (1,4), (2,5), (3,6). It supplies the data for tasks (9,12) and (11,14) of Table 9 (their (d, e) tasks). It does not give b_13 or any sigma^-7 coefficient, and the package's earlier draft wording "for all d >= 3, e >= 3" was wider than what was shown, so this sentence states the narrower range.

## Check It Yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs in ~`45` seconds on a laptop using only the Python 3 standard library: constructively re-derives Mertens–Moore Theorems 5–6 and all 6 polynomial families of Theorem 7 from scratch across all `16,314` canonical excess-3 core multisets, checks against an independent brute-force lattice bond-animal enumerator for `(d, e) = (1, 4), (2, 5), (3, 6)`, and checks against Mertens–Moore Appendix A `D_11(q)` and `[binom(d, 9)] D_12(1) = 6199599459637248`).

## Compared To

- **Primary sources / status page:** Wikipedia *Percolation threshold* (https://en.wikipedia.org/wiki/Percolation_threshold, fetched `2026-11-18T05:50:23Z`, HTTP `200`, SHA-256 `809405d5d4879a9ce4c4754fdadf47ecbef6f085bb8f6661aea7fed1866ccfd5`) and S. Mertens and C. Moore, *Series expansion of the percolation threshold on hypercubic lattices*, J. Phys. A 51 (2018) 475001 (`arXiv:1805.02701`, TeX source SHA-256 `c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf`).
- **Cell:** Closed formula for `[binom(d, e-3)] D_e(q)` (partial win `p2`).
- **Existing status:** Mertens and Moore (2018) proved closed formulas only for `binom(d, e)`, `binom(d, e-1)`, and `binom(d, e-2)` (Theorems 4–6), leaving `(d, e) = (9, 12)` (`4.5` years) and `(11, 14)` (`133,800` years) as open enumeration tasks in Table 9.
- **Our certified formula:** Exact 6-term closed formula in `object/bond_perimeter_binom_d_e_minus_3_formula.json`, matching `48 / 48` published coefficients in `D_4..D_11` and `[binom(d, 9)] D_12(1) = 6199599459637248`.

## Not Claimed

- We do **not** claim the `sigma^-7` coefficient of `p_c^bond(d)` or `p_c^site(d)` (full moonshot target) or the full polynomial `b_13(d)` (`p1`), which still require the remaining lower-dimension enumerations `(d <= 8, e = 12)` or `(d <= 10, e = 14)` in Table 9.

## Credits

- **Stephan Mertens and Cristopher Moore**, *Series expansion of the percolation threshold on hypercubic lattices*, J. Phys. A: Math. Theor. 51 (2018) 475001 (https://arxiv.org/abs/1805.02701) — Theorems 1–6, Lemma 1, Table 9, and Appendix A `D_1..D_11`, `D_12(1)`.
- **David S. Gaunt, Michael F. Sykes, and Heather Ruskin**, J. Phys. A 9 (1976) 1899 (https://doi.org/10.1088/0305-4470/9/11/015) and **D. S. Gaunt and H. Ruskin**, J. Phys. A 11 (1978) 1369 (https://doi.org/10.1088/0305-4470/11/7/025) — foundational high-dimension percolation series and `D_1..D_8`.
- **W. F. Lunnon**, *Counting multidimensional polyominoes*, Computer J. 18 (1975) 366–367 — proper dimensional decomposition `binom(d, k)`.
- **Gill Barequet, Ronnie Barequet, and Gunter Rote**, J. Combin. Theory Ser. A 117 (2010) 1272–1286, and **G. Barequet and M. Shalah**, *Automatic proofs for formulas enumerating proper polycubes* (2017) — Cayley–Prufer forest counting and automated polycube enumeration without perimeter.
- **Sebastian Luther and Stephan Mertens**, *The Perimeter of Proper Polycubes* (https://arxiv.org/abs/1705.03688) — site polycube perimeter formulas for `k = n-1, n-2`.
- Contributor credit: `calgulbenkian`.
