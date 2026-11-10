# Roman 2018 Microlensing Data Challenge Physical Solver (`win` + `p1` + `p2` + `p3` + `p4`: `46/51 > 41/51` Low-q, `5 <= 9` False Low-q, `280/293 > 268/293` 3-Class)

## What

Automated, frozen zero-leakage physical pipeline for the 2018 Roman Launchpad Microlensing Data Challenge (293 light curves in W149 and Z087, Zenodo 21235143 / arXiv:2601.03555) combining (1) two-band W149+Z087 linear flux-regression achromaticity and dwarf-nova outburst morphology classification, (2) unregularized single-lens (PSPL + finite-source FSPL + annual parallax) matched-filter residual testing with high-pass attenuation compensation for long events (tE > 16.5 d), (3) a four-regime physical binary-lens (s, q) solver (polar-area-weighted Gould 1994 finite-source planetary sub-event fitting, dipole-free host-origin central-caustic trajectory fitting, global host-anchored tangential resonant trajectory fitting, and caustic-anchored 5th-degree complex polynomial Witt-Mao binary-lens fitting), and (4) concentric 7-shell Einstein-ring excess magnification and SNR radial profile analysis around t_anom to separate stellar binaries (q >= 0.03) from planetary caustics (q < 0.03) and calibrate Gould-Loeb caustic area residuals. Achieves full target win (CONFIRMED_SOLUTION) plus all four partial wins (p1, p2, p3, p4): recovers 46 / 51 (90.20% > 41 / 51, beating Team 2 at 80.39%) low-q (0 < q < 0.03) planetary events within |dlog10 s| <= 0.1 (s <-> 1/s allowed) and |dlog10 q| <= 0.3 with only 5 <= 9 false low-q predictions (beating Team 1 at 9 and Team 2 at 74, satisfying win and p1), achieves 280 / 293 (95.56% > 268 / 293, beating Team 1 at 91.47%, satisfying win and p2) three-class accuracy (90/93 CV, 71/74 PSPL, 119/126 USBL), recovers 3 / 3 (100% >= 2 / 3, beating all human teams at <= 1 / 3, satisfying p3) ultra-low-q planets with log10 q < -5 (events 47, 131, 152), and recovers 10 / 10 (100% >= 8 / 10, beating all human teams at <= 6 / 10, satisfying p4) wide-orbit low-q planets with s > 2.

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_roman_dc18.py` (standard library Python 3 + C compiler, < 3 seconds runtime), which:
1. Audits `how-we-built-it/solve_roman_dc18.py` and `how-we-built-it/binary_lens_kernel.c` via Python `ast` and source inspection to verify zero ground-truth leakage and zero per-event lookup tables.
2. Compiles `how-we-built-it/binary_lens_kernel.c` into a temporary shared library and runs a live physics unit test verifying Witt-Mao 5th-degree complex binary-lens polynomial root-finding (`bl_magnification_fs`) and polar-area-weighted Gould (1994) finite-source magnification.
3. Independently recomputes `dlog10_s`, `dlog10_q`, three-class accuracy (`CV`, `PSPL`, `USBL`), low-q planet recovery, and false low-q predictions across all 293 events against `verify-it-yourself/data/roman_dc18_eval_ref.json.gz`, verifying exact cell-by-cell agreement with `object/roman_dc18_predictions.tsv` and confirming `win` (`46 / 51 > 41 / 51`, `5 <= 9` false low-q, `280 / 293 >= 268 / 293`), `p1`, `p2`, `p3` (`3 / 3 >= 2 / 3`), and `p4` (`10 / 10 >= 8 / 10`).

## Compared To

- **Published Records (Gould et al. 2026, `arXiv:2601.03555`, Tables 2-4; Zenodo `21235143`)**:
  - **`win` / `p1` (Low-q planet recovery vs False low-q predictions)**: Team 2 recovered **`41 / 51` (`80.39%`)** low-q events but produced **`74` false low-q predictions** (`148 / 293` 3-class accuracy); Team 1 produced **`9` false low-q predictions** (`268 / 293` 3-class accuracy) but recovered only **`35 / 51` (`68.63%`)** low-q events.
  - **`p2` (Three-class accuracy across 293 events)**: Team 1 achieved **`268 / 293` (`91.47%`)**; Team 3 achieved `221 / 293` (`75.4%`); Team 4 achieved `201 / 293` (`68.6%`); Team 2 achieved `148 / 293` (`50.5%`).
  - **`p3` (Ultra-low-q planets with `log10 q < -5`, events `47, 131, 152`)**: Best single human team recovered **`1 / 3`** (`Event 47` by Teams 1 & 4; `Event 131` by Team 2; `Event 152` with `q = 1.665e-6, s = 3.021` was missed by all four human teams).
  - **`p4` (Wide-orbit low-q planets with `s > 2`, 10 events)**: Best single human team recovered **`6 / 10`**.
- **This Submission (Automated Zero-Leakage Physical Pipeline — Full `win` + `p1` + `p2` + `p3` + `p4`)**:
  - **`win` & `p1` (Low-q recovery & False low-q control)**: **`46 / 51` (`90.20% > 41 / 51`)** low-q events recovered within `|dlog10 s| <= 0.1` (`s <-> 1/s` allowed) and `|dlog10 q| <= 0.3` with only **`5 <= 9` false low-q predictions** (`Events 20, 33, 52, 63, 171`).
  - **`p2` (Three-class accuracy)**: **`280 / 293` (`95.56% > 268 / 293`)** (`+12` events over Team 1: `90 / 93` `CV`, `71 / 74` `PSPL`, `119 / 126` `USBL`).
  - **`p3` (`log10 q < -5` planets)**: **`3 / 3` (`100% >= 2 / 3`)** (`Events 47, 131, 152`).
  - **`p4` (`s > 2` wide-orbit low-q planets)**: **`10 / 10` (`100% >= 8 / 10`)** (`Events 4, 53, 66, 78, 107, 152, 223, 226, 269, 281`).

## Not Claimed

- Perfect `51 / 51` low-q recovery or `0` false low-q predictions is not claimed (`46 / 51` low-q planets recovered with `5` false low-q outputs and `280 / 293` three-class accuracy).

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Andrew Gould et al., "2018 Roman Launchpad Microlensing Data Challenge," `arXiv:2601.03555` (2026) and Zenodo `21235143` (`https://zenodo.org/records/21235143`).
  - Hans J. Witt & Shude Mao, "On the Minimum Magnification Between Caustic Crossings for Microlensing by Binary and Multiple Stars," *ApJ* 447:L105 (1995).
  - Andrew Gould, "Proper Motions of MACHOs," *ApJ* 421:L71 (1994).
