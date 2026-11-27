# How We Built It (Contributor Text — Unverified)

- `hs_mod.py`: Decomposition 1 — cell-by-cell broken-profile boustrophedon dynamic programming with MSB-first recursive `[0+V(n-1), 10+V(n-2)]` Fibonacci string indexing modulo `37` 31-bit primes in `[2147482819, 2147483647]` subset `(2^30, 2^31)`, plus Chinese Remainder Theorem (CRT) reconstruction and a held-out check prime per width.
- `far.py`: Decomposition 2 — cell-by-cell sliding-window dynamic programming with LSB-first reversed-rank `(prev_cell, curr_row_mask)` indexing modulo `38` disjoint 30-bit primes in `[1073740933, 1073741789]` subset `(0, 2^30)`, plus CRT reconstruction and a held-out check prime per width.
- `indep_transfer.py`: Decomposition 3 — full-column compatible-pattern transfer matrix in exact Python big-integer arithmetic (no modular arithmetic or CRT) for widths `w = 0..16`.
- `PREREG.md`: Pre-registered acceptance and two-run agreement rules frozen prior to harvest.
