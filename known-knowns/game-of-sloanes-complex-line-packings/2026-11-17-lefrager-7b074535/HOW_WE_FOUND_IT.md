> Note: contributor text, unverified narrative of how the optimization pipeline was discovered and executed; independent verification artifacts live in `verify-it-yourself/` and `panel/`.

# How We Found It — `(3, 34)` Complex Line Packing

## 1. Auditing All 104 Unclaimed Open Rows

Live reconnaissance of `gnikylime/GameofSloanes` (`3 <= d <= 7`) identified `218` table rows, `10` active pull requests claiming `71` cells, and `104` completely unclaimed open rows (`not provably optimal`, `not conjecturally optimal`, `no open PR`). Testing direct Augmented Lagrangian minimax polishing and small-to-moderate perturbations (`sigma in {0, 1e-4, ..., 0.25}`) across all `104` merged `.txt` files yielded **0** improvements `>= 5e-9`: every existing record already sat in a locally rigid minimum.

To test whether local vector surgery could escape upstream [`CurrentBestPackings/3x34_jrr.txt`](https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x34_jrr.txt) (`SHA-256: 159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e`, `mu = 0.7568347972536282...`), we ran delete-`k` (`k in {2, 3, 4}`) Chebyshev re-insertion + LSE + ALM across `64` trials directly from `3x34_jrr.txt`: every run collapsed right back to `0.7568347973`.

## 2. Why Standard Smooth Optimizers Stall, and How Three Ideas Solved `(3, 34)`

Generic random-start optimization in $\mathbb{C}^{3 \times 34}$ (`DOF = 128`) faces two bottlenecks:
1. **Spectral basin trapping:** Pure smooth LogSumExp (`LSE`) gradient descent frequently locks into clustered contact graphs above the true minimax optimum (`~0.7570+`).
2. **Nonsmooth minimax kinks:** Even after entering a better basin, smooth surrogates (`LSE` at high $\beta$, $L_p$-homotopy) become ill-conditioned long before all `DOF + 1 = 129` active overlaps equilibrate.

We combined three complementary mechanisms:
- **$O(d n^2)$ Subspace-Iteration Gram RRR (`how-we-built-it/fast_rrr_turbo.cpp`):** Replaced full $O(n^3)$ Hermitian Jacobi eigendecompositions inside Elser's Relax-Reflect-Reflect (`RRR`) projection with `3`-step $O(d n^2)$ subspace power iteration and $3 \times 3$ Rayleigh-Ritz diagonalization. Across `2,400` diverse RRR + LSE multi-starts, this discovered a strictly deeper basin at `mu = 0.7565178377501368`.
- **Augmented Lagrangian $(\Phi, t)$ L-BFGS (`how-we-built-it/gram_alm.cpp`, `how-we-built-it/fine_alm_ld.cpp`):** Introducing an explicit minimax epigraph variable $t$ and dual weights $\lambda_{jk} \ge 0$ converts the nonsmooth $\max_{j<k} |\langle \phi_j, \phi_k \rangle|^2$ problem into $C^1$ smooth L-BFGS rounds ($\rho \to 10^9$). Running two double-precision passes and one 80-bit `long double` pass equilibrated all `129 = DOF + 1` active pairs to `< 1e-10`, reaching **`mu = 0.75649479818227170516...`** (`+0.0003400018...` improvement over the live record).

## 3. Distinctness From the Prior Record

Spectral and contact-graph analysis confirms `object/3x34_new.txt` is a distinct packing in a strictly lower basin, not a unitary gauge or phase tweak of upstream `CurrentBestPackings/3x34_jrr.txt`:
- Gram singular values (`G = V^H V`): `[11.4823, 11.4565, 11.0612]` (ours) vs `[11.5955, 11.3262, 11.0783]` (`3x34_jrr.txt`).
- Pairwise overlap median/min: `0.49452 / 0.16284` (ours) vs `0.46707 / 0.12724` (`3x34_jrr.txt`).
- Non-isomorphic `1e-8` contact graphs on `129` active pairs (`deg` min `5` vs `3`).
