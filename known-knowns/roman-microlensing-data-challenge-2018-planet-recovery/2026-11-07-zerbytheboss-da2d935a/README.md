# Roman 2018 Microlensing Data Challenge Physical Solver (`p2`: `274/293 > 268/293`, `p3`: `3/3 >= 2/3`, `p4`: `9/10 >= 8/10`)

## What

Automated, frozen zero-leakage physical pipeline for the 2018 Roman Launchpad Microlensing Data Challenge (293 light curves in W149 and Z087, Zenodo 21235143 / arXiv:2601.03555) combining (1) two-band W149+Z087 linear flux-regression achromaticity and dwarf-nova outburst morphology classification, (2) unregularized single-lens (PSPL + finite-source FSPL + annual parallax) matched-filter residual testing, and (3) a four-regime physical binary-lens (s, q) solver (exact polar-area-weighted Gould 1994 finite-source planetary sub-event fitting, dipole-free host-origin central-caustic trajectory fitting, global host-anchored tangential resonant trajectory fitting, and caustic-anchored 5th-degree complex polynomial Witt-Mao binary-lens fitting) with zero access to ground-truth master_file.txt or team entries. Achieves 274 / 293 (93.52% > 268 / 293, beating Team 1 at 91.47%, satisfying p2) three-class accuracy (90/93 CV, 70/74 PSPL, 114/126 USBL), recovers 3 / 3 (100% >= 2 / 3, beating all human teams at 1 / 3, satisfying p3) ultra-low-mass-ratio planets with log10 q < -5 (events 47, 131, 152), and recovers 9 / 10 (90% >= 8 / 10, beating all human teams at 6 / 10, satisfying p4) wide-orbit low-q planets with s > 2 (events 4, 53, 66, 78, 107, 152, 226, 269, 281), with 31 / 51 (60.8%) overall low-q planets recovered within |dlog10 s| <= 0.1 (s <-> 1/s allowed) and |dlog10 q| <= 0.3.

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_roman_dc18.py` (standard library Python 3 + C compiler, < 3 seconds runtime), which:
1. Audits `how-we-built-it/solve_roman_dc18.py` and `how-we-built-it/binary_lens_kernel.c` via Python `ast` and source inspection to verify zero ground-truth leakage and zero per-event lookup tables.
2. Compiles `how-we-built-it/binary_lens_kernel.c` into a temporary shared library and runs a live physics unit test verifying Witt-Mao 5th-degree complex binary-lens polynomial root-finding (`bl_magnification_fs`) and polar-area-weighted Gould (1994) finite-source magnification.
3. Independently recomputes `dlog10_s`, `dlog10_q`, three-class accuracy (`CV`, `PSPL`, `USBL`), and low-q planet recovery across all 293 events against `verify-it-yourself/data/roman_dc18_eval_ref.json.gz`, verifying exact cell-by-cell agreement with `object/roman_dc18_predictions.tsv` and confirming `p2` (`274 / 293 > 268 / 293`), `p3` (`3 / 3 >= 2 / 3`), and `p4` (`9 / 10 >= 8 / 10`).

## Compared To

- **Published Records (Gould et al. 2026, `arXiv:2601.03555`, Tables 2-4; Zenodo `21235143`)**:
  - **`p2` (Three-class accuracy across 293 events)**: Team 1 achieved **`268 / 293` (`91.47%`)**; Team 3 achieved `221 / 293` (`75.4%`); Team 4 achieved `201 / 293` (`68.6%`); Team 2 achieved `148 / 293` (`50.5%`).
  - **`p3` (Ultra-low-q planets with `log10 q < -5`, events `47, 131, 152`)**: Best single human team recovered **`1 / 3`** (`Event 47` by Teams 1 & 4; `Event 131` by Team 2; `Event 152` with `q = 1.665e-6, s = 3.021` was missed by all four human teams).
  - **`p4` (Wide-orbit low-q planets with `s > 2`, 10 events)**: Best single human team recovered **`6 / 10`**.
- **This Submission (Automated Zero-Leakage Physical Pipeline — `p2` + `p3` + `p4`)**:
  - **`p2` (Three-class accuracy)**: **`274 / 293` (`93.52% > 268 / 293`)** (`+6` events over Team 1: `90 / 93` `CV`, `70 / 74` `PSPL`, `114 / 126` `USBL`).
  - **`p3` (`log10 q < -5` planets)**: **`3 / 3` (`100% >= 2 / 3`)**:
    - `Event 47` (`true s=1.028, log10 q=-5.07`): `pred s=1.250 (|dlog10 s|=0.085), log10 q=-5.12 (|dlog10 q|=0.044)`
    - `Event 131` (`true s=1.666, log10 q=-5.68`): `pred s=1.536 (|dlog10 s|=0.035), log10 q=-5.40 (|dlog10 q|=0.281)`
    - `Event 152` (`true s=3.021, log10 q=-5.78`): `pred s=2.973 (|dlog10 s|=0.007), log10 q=-5.70 (|dlog10 q|=0.079)`
  - **`p4` (`s > 2` wide-orbit low-q planets)**: **`9 / 10` (`90% >= 8 / 10`)** (`Events 4, 53, 66, 78, 107, 152, 226, 269, 281` all classified as `USBL` and recovered within `|dlog10 s| <= 0.1` and `|dlog10 q| <= 0.3`).
  - **Overall low-q recovery**: **`31 / 51` (`60.8%`)** low-q events classified as `USBL` and recovered within tolerances.

## Not Claimed

- Full-target `win` / `p1` (`> 41 / 51` low-q planets recovered simultaneously with `<= 9` or `<= 15` false low-q outputs) is not claimed (`31 / 51` low-q planets recovered); this submission claims partial wins `p2`, `p3`, and `p4`.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Andrew Gould et al., "2018 Roman Launchpad Microlensing Data Challenge," `arXiv:2601.03555` (2026) and Zenodo `21235143` (`https://zenodo.org/records/21235143`).
  - Hans J. Witt & Shude Mao, "On the Minimum Magnification Between Caustic Crossings for Microlensing by Binary and Multiple Stars," *ApJ* 447:L105 (1995).
  - Andrew Gould, "Proper Motions of MACHOs," *ApJ* 421:L71 (1994).
