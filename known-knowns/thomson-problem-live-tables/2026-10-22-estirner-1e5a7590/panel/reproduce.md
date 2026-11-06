# REPRODUCE skeptic report: thomson-problem-live-tables, N = 743

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

Scope: only the files in claim/ (CLAIM.md, REPRODUCE.md, object/, inputs/, tools/). No network. claim/ was not
modified (15 files before and after; the author's commands were run in a scratch copy of the package).
injection_suspected: none (no file in the package contains instructions addressed to the reviewer).

## 1. Definition my checker was written from (verbatim, CLAIM.md "Success criterion")

> Success means N points on the unit sphere (coordinates to >= 20 digits) for some N <= 1500 listed in at least one
> live table, such that E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER
> (direction: min) than the minimum energy for that N over ALL of: Deeter's table (https://deetour.net/oppp/thomson/,
> N = 4..524), CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table (site/s_1/index.html), the
> Wikipedia table and (for N = 282) EinsteinArena, each re-fetched live immediately before claiming, by at least 1e-6
> in absolute energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to
> gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from
> every posted table configuration for that N: polishing each table's own point file (Deeter e.<N>.txt, CCD
> xyz/<N>.xyz, Riesz dat/points_<N>_1.dat) with the same routine must give an energy higher than E* by >= 1e-6.

## 2. My own checker (written before opening tools/)

A new script next to claim/ (not in the package), using numpy, scipy and mpmath (gmpy backend):
- `info`: N, columns, significant digits of every coordinate, max ||x|-1|.
- `energy FILE DPS`: parse strings at DPS digits, normalise each point in mpmath, E = sum_{i<j} 1/|xi-xj| (row sums
  with mpmath.fsum).
- `grad FILE DPS`: mpmath Euclidean gradient, tangent projection g_i - (x_i.g_i) x_i, 2-norm.
- `hess FILE`: float64 Euclidean Hessian (blocks 3dd^T/r^5 - I/r^3), Riemannian Hessian B^T H B - diag(x_i.g_i) in an
  orthonormal tangent basis (2N x 2N), the 3 rotation generators e_k x x_i removed with scipy null_space, eigvalsh of
  the (2N-3) x (2N-3) block.
- `polish FILE OUT`: float64 L-BFGS on y -> y/|y|, float64 Riemannian Newton (6 steps), then mpmath (dps 40) Newton
  steps with the mpmath tangent gradient and the float64 reduced Hessian, retraction by renormalisation in mpmath,
  until |g_T| < 1e-28; then E at dps 30 and dps 50, |g_T| and Hessian of the written result.
Self-tests before use: N = 12 icosahedron E = 49.1652530576288, 21 = 2N-3 positive reduced eigenvalues (min
0.907163890); finite-difference checks of the Euclidean Hessian (max error 1.1e-9 on entries up to 24.9), gradient,
and Riemannian Hessian quadratic form (22.990139570 FD vs 22.990139956); N = 20 random start polished to
E = 150.88156833375650338840139772 (the known N = 20 minimum 150.881568334), reduced Hessian 37 positive eigenvalues.

## 3. Results of my checker (copied from command output)

File integrity: sha256 of object/thomson_743.txt = 1e5a75909e58d1a4347aaaad37053aa7e22cd164f8da0d8fd26cc2870d78471b,
inputs/points_743_1.dat = 68ac9c8d...b3df9a, inputs/merged125_cand_743.txt = 9293bcd2...689d14, and all 8 files in
inputs/tables/ match the sha256 values in the CLAIM.md table record.

| quantity | claim | my result |
|---|---|---|
| N, format | 743 lines "x y z" | N=743 columns={3} |
| digits per coordinate | 30 significant | sigdigits min=30 max=30, count(<20)=0; max||x|-1| = 7.994e-31 |
| E* (mpmath dps 30, normalised) | 264837.4538033452076921018 | 264837.453803345207692101835864 (dps 30); 264837.45380334520769210183586395214947705707197943 (dps 50) |
| tangent-gradient norm at saved coordinates | about 4.48e-24 (< 1e-20) | 4.47657e-24 (dps 30), 4.47645e-24 (dps 50) |
| non-rotational tangent-Hessian eigenvalues | 1483 = 2N-3, all > 0 | n_eigs=1483 n_positive=1483 |
| smallest eigenvalue | 4.042259 | 4.042259181 (2nd 4.594075417, max 4454.117513) |
| rotation modes | - | full 2N spectrum: 3 smallest |eig| 7.3e-13, 3.8e-12, 1.3e-11; 4th 4.042259 |
| margin below CCD Riesz s=1 cell 264837.5858504 | 0.1320470548 | 0.132047054792308 |
| margin below #125 value 264837.5287041150 | 0.0749007698 | 0.0749007697923079 (vs full 264837.5287041150044362828: 0.0749007697967442) |
| polished Riesz file - E* | 0.1320470169 | my polish: E(dps 30) = 264837.585850362060967712922635, gap 0.132047016853276 |
| polished #125 file - E* | 0.0749007698 | my polish: E(dps 30) = 264837.528704115004436282821702, gap 0.0749007697967442 |

Polish details (my routine):
- inputs/points_743_1.dat: start f64 E=264837.585850362084, L-BFGS |gT| 1.274e-06, f64 Newton to ~5e-12, mp Newton
  |gT| 5.31381e-12 -> 2.81951e-24 -> 7.84203e-37; written file |g_T| 2.68078e-36; reduced Hessian 1483 positive,
  min 2.234761351.
- inputs/merged125_cand_743.txt: mp Newton 5.07394e-12 -> 3.20031e-24 -> 8.26249e-37; written |g_T| 2.65617e-36;
  1483 positive, min 3.633597124.
- object/thomson_743.txt (same routine, basin stability): E(dps 30) = 264837.453803345207692101835864 (unchanged),
  mp Newton 5.23678e-12 -> 3.26775e-24 -> 8.14924e-37; 1483 positive, min 4.042259181.

Tables (parsed from the saved HTML in inputs/tables/):
- ccd_riesz_s1_index.html: 53 rows, N 512..9913, N = 743 entries ['264837.5858504'] (one row).
- deeter.html: 521 rows, N 4..524, 743 absent; ccd_thomson_table.html: 409 rows, N 10..972, 743 absent;
  ccd_thomson2_table.html: 36 rows, N 400..4352, 743 absent; wikipedia_thomson.html: 234 rows, N 2..470, 743 absent.
  No page other than the s=1 page contains "264837". The two .404.html files are Apache "404 Not Found" pages.
So the Riesz s=1 cell is the only N = 743 row in the saved pages, and E* is below it by 0.132 >> 1e-6.

Determinism: a rerun of my Hessian check gave the same n_eigs=1483 n_positive=1483 min=4.042259181; the author's
`certify.py check` rerun was identical apart from the timing field (section 4); and E* was reproduced to all 25
printed digits by three independent routes (my mpmath, the author's mpmath, the author's decimal-40).

## 4. Author's REPRODUCE.md commands (run in a scratch copy of claim/, venv python, one thread)

Step 1 `certify.py check object/thomson_743.txt`: "E_mp30": "264837.4538033452076921018", "gT_mp30": "4.47655e-24",
"n_eigs": 1483, "min_eig": 4.042259181123571, "n_nonpositive": 0, "delta_bound": 3.195798010861421e-07,
"hessian_pass": true. Rerun: identical JSON apart from the timing field.

Step 2 `certify.py polish`:
- object: E* 264837.4538033452076921018, gT 7.64142e-27, gT_below_1e-20 True, n_eigs 1483, min 4.042259181115254, pass True
- Riesz points_743_1.dat: E_in 264837.5858503620609750247, E* 264837.5858503620609677129, gT 4.59704e-24, True,
  min 2.234761350825306, pass True
- #125: E* 264837.5287041150044362828, gT 7.49172e-27, True, min 3.633597124296364, pass True
All three match the REPRODUCE.md expectations exactly.

Step 3 `verify_stdlib.py` (decimal, 40 digits): E = 264837.4538033452076921018358640, tangent gradient norm =
4.476e-24, |E - expected| = 3.586e-20, bar - E = 0.0749007698, pol_riesz.txt E_other - E = 0.1320470169,
pol_m125.txt E_other - E = 0.0749007698, last line PASS (exit 0).

Step 4 grep: line 270-271 of inputs/tables/ccd_riesz_s1_index.html show cells 743 and 264837.5858504.

## 5. Mismatches and remarks

- No numeric mismatch: every number in the claim sentence (N = 743, 30 digits, E*, 4.48e-24 < 1e-20, 1483 = 2N-3
  positive eigenvalues, smallest 4.042259, margins 0.1320470548 and 0.0749007698, gaps after polish 0.1320470169 and
  0.0749007698) is reproduced by my independent checker and by the author's tools; my E* agrees with the claim in all
  25 printed digits.
- Cosmetic: certify.py "min_digits_in_file" prints 31 because it counts the leading "0" of values like 0.99...;
  the true significant-digit count is 30 (my count), which is what CLAIM.md states.
- Out of scope for this role (no network): whether the live tables still look as saved, and whether any value
  lower than 264837.5287041150 exists outside the package ("lowest previously known"). Against the saved pages and
  the values listed in CLAIM.md the statement holds.
- The Hessian positivity is a float64 computation, as the definition requires; the smallest eigenvalue 4.04 exceeds
  the author's rounding bound 3.2e-7 by seven orders of magnitude.

pass: true
