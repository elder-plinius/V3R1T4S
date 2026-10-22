# How we built it

Scheme: 12x13x16, class Z, rank 1516. The contributor's AI search agent (Gemini, "Argon") built it on 2026-10-17 by **base substitution** into a Perminov Q scheme. The agent's own result line (`results/RESULTS.md`, section 2): `7 x <4,4,4> base sub (1509 Q -> 1516 Z)`.

## Parent scheme

- File: `schemes/results/Q/12x13x16_m1509_Q.json` in Perminov's repository, rank 1509 over Q.
- URL (pinned to the commit the agent worked from, 2026-10-13): https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/f0efd4f67f6ff09bf0418af75c2a209c8cf814b3/schemes/results/Q/12x13x16_m1509_Q.json
- sha256 of that file: `f4343e3746fd8f64a7ec7db07eefe65b470feb00d593e4897d24d755c000eef4` (3042492 bytes). It is not redistributed here.
- Perminov's README (fetched sha256 `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`) gives these rows for the format: `| `12x13x16` | 1556 (`Q`) | [1509](schemes/results/Q/12x13x16_m1509_Q.json) (`Q`) | **2.807000642** |`; `| `12x13x16` | 1548 (?) | 1544 (?) | 1509 (1556) | **2.807000642** |`. The README gives no per-file author line beyond these tables and its publication list (https://github.com/dronperminov/FastMatrixMultiplication#publications); which of its papers produced this parent file is not stated there.

## Base schemes used

- Rational base <4,4,4> rank 48: `schemes/known/tensor/4x4x4_tensor.mpl` in the same repository, sha256 `4aa4f7bc77259ca853bbd1074ae37dcd8b6272d58053b8992392fb4344320068`.
- Integer-coefficient replacement <4,4,4> rank 49: `schemes/results/ZT/4x4x4_m49_ZT.json`, sha256 `8b3d86d816f70f34b4dc47437ff1a724ebec67302dc91edc8805aae0d9789f33`.
- The agent matched 7 blocks of 48 consecutive terms in the parent, solved the exact linear maps from the rational base to each block over the rationals, and substituted the rank-49 scheme transported through those maps. Rank change: 1509 + 7 x 1 = 1516, then flip reduction. The reduced scheme has rank 1516.

## Commands

The snapshot has no run log. The invocation below is inferred from the script's relative paths and is not a recording:

```sh
# from {WORKDIR}/attacks/fmm, which holds data/FastMatrixMultiplication (a clone of Perminov's repository at the commit above),
# data/bases/ (the base files listed above) and bin/zt_flip_reduce (compiled from tools/zt_flip_reduce.c)
python3 tools/run_q_upgrades.py
```

The script runs over a list of Q parents (this one is in it), writes `results/new_upgrades/{format}_m{rank}_{class}.json`, and calls `./bin/zt_flip_reduce STEPS SEED MAXC` with 50000 steps, seed 1337 and the maximum coefficient found so far (100000 steps, maximum 1, for a ZT split). The compile command for `zt_flip_reduce.c` is not recorded; it is a single C file with no dependencies beyond the C library.

## Included here

- `PREREG.md`: the run's pre-registration (method text for base substitution and flip reduction). Its section on additive complexity concerns other claims. Local paths in it are replaced by `{WORKDIR}`.
- `tools/run_q_upgrades.py`: the driver. `tools/upgrade_schemes.py`: its helpers `load_mpl_raw`, `solve_linear_map`, `optimize_block` (the rest of that file is a different route and was not used). `tools/unfold_z_to_zt.py`: only its function `run_c_opt` (the call into the flip binary) was used; its `__main__` block is the separate Z-to-ternary unfolding route. `tools/zt_flip_reduce.c`: the flip-graph reduction. Sources are copied unchanged; they contain no local paths.

## Not included

- `tools/verify_z_brent.py`: the agent's own build-time helper, which the three scripts import (`load_reference_bounds`, `verify_scheme`). It is included only so they run as recorded; it is not this package's checker. The checker in `../verify-it-yourself/` was written independently of it, and the panel did not use it.
- The Perminov repository, the parent and base files (named and hashed above), the compiled binary, and the run log.
- I did not rerun this construction when building the package; the object is checked by `../verify-it-yourself/`, not by rebuilding.
