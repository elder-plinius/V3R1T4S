# How We Found It (Contributor Text — Unverified)

*Note: contributor text, unverified (narrative summary of how the result was computed).*

OEIS `A089980` tabulates $T(m, n)$, the number of independent sets (hard-square lattice-gas configurations) on the $m \times n$ rectangular grid graph $P_m \times P_n$, read by antidiagonals $d = m + n$. The published OEIS b-file `b089980.txt` stops at `n = 3159`, the end of antidiagonal $d = 78$.

To compute and certify the complete next antidiagonal $d = 79$ (`80` entries $T(w, 79 - w)$ for $w = 0..79$, `b-file` indices `n = 3160..3239`, determined by the `40` canonical widths $w = 0..39$ under $T(w, m) = T(m, w)$) under the target's two-run and reproduction rules (`p2`):

1. **Decomposition 1 (`how-we-built-it/hs_mod.py`):** We factored the cell-by-cell broken-profile state at row $k$ of width $w$ into the Cartesian product $V(k+1) \times V(w-k-1)$ of Fibonacci strings ordered MSB-first (`[0 + V(n-1)]` followed by `[10 + V(n-2)]`), using a boustrophedon column sweep so column boundaries require zero state permutation. Every cell step is a pair of contiguous 2D slice additions modulo 31-bit primes $p \in (2^{30}, 2^{31})$ (`37` primes at $w = 39$, including one held-out check prime).
2. **Decomposition 2 (`how-we-built-it/far.py`):** Written in a fresh context without reading `hs_mod.py`, this solver uses a different state encoding — LSB-first reversed-rank `P-rank` `(prev_cell, curr_row_mask)` sliding-window transitions — and a completely disjoint set of 30-bit primes $p \in (0, 2^{30})$ (`38` primes at $w = 39$, including one held-out check prime), with `uint32` vectorization at widths $w \ge 33$ to keep peak RSS below `1.4 GB` per worker.
3. **Decomposition 3 (`how-we-built-it/indep_transfer.py`):** For widths $w = 0..16$, we also ran a full-column compatible-pattern transfer matrix in exact Python big-integer arithmetic (using no modular arithmetic or CRT).

Both `hs_mod.py` and `far.py` reproduced all `2,380` published cells $w + m \le 78$ across $w = 0..39$ with `0` mismatches, passed all `40/40` held-out check primes, and agreed to the last decimal digit on all `40/40` widths $w = 0..39$ (up to the `279`-digit peak $T(39, 40)$).
