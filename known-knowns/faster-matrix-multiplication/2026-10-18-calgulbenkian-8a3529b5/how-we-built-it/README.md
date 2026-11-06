# How we built it

Scheme: 11x14x16, class ZT, rank 1547. The contributor's AI search agent (Gemini, "Argon") built it on 2026-10-17 by **base substitution** into a Perminov Q scheme. The agent's own result line (`results/RESULTS.md`, section 2): `20 x <3,4,7> base sub + ZT split + flip`.

## Parent scheme

- File: `schemes/results/Q/11x14x16_m1520_Q.json` in Perminov's repository, rank 1520 over Q.
- URL (pinned to the commit the agent worked from, 2026-10-13): https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/schemes/results/Q/11x14x16_m1520_Q.json
- sha256 of that file: `d25c1c30000221c5f9d6028805ffba3efe9304f29b7c5a6aa13249b239450451` (3084807 bytes). It is not redistributed here.
- Perminov's README (fetched sha256 `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`) gives these rows for the format: `| `11x14x16` | 1571 (`Q`) | [1520](schemes/results/Q/11x14x16_m1520_Q.json) (`Q`) | 2.814428649 |`; `| `11x14x16` | 1550 (?) | 1550 (?) | 1520 (1571) | 2.814428649 |`. The README gives no per-file author line beyond these tables and its publication list (https://github.com/dronperminov/FastMatrixMultiplication#publications); which of its papers produced this parent file is not stated there.

## Base schemes used

- Rational base <3,4,7> rank 63: `schemes/known/tensor/3x4x7_tensor.mpl` in the same repository, sha256 `c2ae429b5bfbcfe451a52ccb018a19d10745eb4b53f52268fae4f715360825c7`.
- Integer-coefficient replacement <3,4,7> rank 64: `schemes/results/ZT/3x4x7_m64_ZT.json`, sha256 `229e7c5b145c27fe62565912cf68b28036a39a8f969868560344b16df696bacd`.
- The agent matched 20 blocks of 63 consecutive terms in the parent, solved the exact linear maps from the rational base to each block over the rationals, and substituted the rank-64 scheme transported through those maps. Rank change: 1520 + 20 x 1 = 1540, then flip reduction. The reduced scheme has rank 1547.

This ZT scheme is a second step on the Z scheme `11x14x16_m1540_Z` (the object of #410, shipped here as `start/11x14x16_m1540_Z.json`): `fast_split_to_zt` in `tools/run_q_upgrades.py` splits the 8 terms that have a coefficient of 2 into ternary parts (rank 1548), and `zt_flip_reduce` (100000 steps, seed 1337, maximum coefficient 1) then reduces the result to rank 1547. `rebuild.sh` reruns these two steps and reproduces the object byte for byte (2026-10-25; output in `../HOW_WE_FOUND_IT.md`).

## Commands

The snapshot has no run log. The invocation below, for the whole run, is inferred from the script's relative paths and is not a recording. The last two steps are rerun by `rebuild.sh`:

```sh
# from {WORKDIR}/attacks/fmm, which holds data/FastMatrixMultiplication (a clone of Perminov's repository at the commit above),
# data/bases/ (the base files listed above) and bin/zt_flip_reduce (compiled from tools/zt_flip_reduce.c)
python3 tools/run_q_upgrades.py
```

The script runs over a list of Q parents (this one is in it), writes `results/new_upgrades/{format}_m{rank}_{class}.json`, and calls `./bin/zt_flip_reduce STEPS SEED MAXC` with 50000 steps, seed 1337 and the maximum coefficient found so far (100000 steps, maximum 1, for a ZT split). The compile command for `zt_flip_reduce.c` is not recorded; it is a single C file with no dependencies beyond the C library.

## Included here

- `start/11x14x16_m1540_Z.json`: the rank-1540 integer composition (the object of #410), the input of steps 2 and 3.
- `rebuild_split.py`, `flip_io.py` and `rebuild.sh`: written for this package on 2026-10-25 to rerun the ternary split and the flip reduction from that file (the split uses the same rule and term order as `fast_split_to_zt`).
- `PREREG.md`: the part of the run's pre-registration that concerns this scheme (method text for base substitution and flip reduction), trimmed to this cell on 2026-10-25.
- `tools/run_q_upgrades.py`: the driver. `tools/upgrade_schemes.py`: its helpers `load_mpl_raw`, `solve_linear_map`, `optimize_block` (the rest of that file is a different route and was not used). `tools/unfold_z_to_zt.py`: only its function `run_c_opt` (the call into the flip binary) was used; its `__main__` block is the separate Z-to-ternary unfolding route. `tools/zt_flip_reduce.c`: the flip-graph reduction. Sources are copied unchanged; they contain no local paths.

## Not included

- `tools/verify_z_brent.py`: the agent's own build-time helper, which the three scripts import (`load_reference_bounds`, `verify_scheme`). It is included only so they run as recorded; it is not this package's checker. The checker in `../verify-it-yourself/` was written independently of it, and the panel did not use it.
- The Perminov repository, the parent and base files (named and hashed above), the compiled binary, and the run log.
- Step 1 (the block substitution) was not rerun here; the maintainer reproduced it for #410. Steps 2 and 3 were rerun on 2026-10-25 with `rebuild.sh`.
