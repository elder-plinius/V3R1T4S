# Node-Kayles on Lattice Graphs: 5 Newly Resolved Table 1 Cells (`2026-11-13-rainrat-6b05f2a3`)

## What
Claimed Criterion (2) scope covers 5 newly resolved open cells of Brown et al. (2020) Table 1 (`L_{5x8}=0`, `L_{6x7}=3`, `L_{5x9}=4`, `L_{7x7}=1`, `L_{5x10}=1`) via two distinct exact solvers (`nk_solver.cpp` and `pn_solver.cpp`), with `REPRODUCE.md` explicitly calibrating `A316632` (`n=1..17`), odd `A316533` (`n=5..25`), and Table 1 shaded entries `L_{5x5}`, `L_{5x6}`, `L_{5x7}`.

## Check it yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (rough laptop time: ~90 seconds).

## Compared to
- **Brown et al. (2020), Table 1** (`https://cs.uwaterloo.ca/journals/JIS/VOL23/Wong/wong24.pdf`, fetched `2026-11-13T01:01:20Z`): `L_{5x8}`, `L_{6x7}`, `L_{5x10}` were blank (unsolved); `L_{5x9}` and `L_{7x7}` were `> 0` only (exact nimbers unknown).
- **OEIS A316632** (`https://oeis.org/A316632`, fetched `2026-11-13T01:01:19Z`): `n = 1..17` (`2, 1, 1, 0, 3, 3, 2, 2, 2, 3, 3, 5, 2, 4, 1, 3, 2`).
- **OEIS A316533** (`https://oeis.org/A316533`, fetched `2026-11-13T00:52:31Z`): `n = 5..26`.

## Not claimed
- Extensions of OEIS A316632 (`n >= 18`) or A316533 (`n >= 27`) are not part of this confirmed claim (Criterion 1).
- Remaining open Table 1 cells (`L_{6x9}`, `L_{7x8}`, `L_{7x9}`, `L_{7x10}`, `L_{8x9}`, `L_{9x9}`, `L_{9x10}`) are not claimed here.

## Credits
- Contributed by RainRat.
- Builds on Sierra Brown, Spencer Daugherty, Eugene Fiorini, Barbara Maldonado, Diego Manzano-Ruiz, Sean Rainville, Riley Waechter, and Tony W. H. Wong, *Nimber Sequences of Node-Kayles Games*, Journal of Integer Sequences, Vol. 23 (2020), Article 20.3.5 ([wong24.pdf](https://cs.uwaterloo.ca/journals/JIS/VOL23/Wong/wong24.pdf)), and OEIS [A316632](https://oeis.org/A316632) / [A316533](https://oeis.org/A316533) (including extensions by Max Fan and Alex Towell).
