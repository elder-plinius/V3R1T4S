# The family, by formula, and how its value changes with discretisation

Label for everything in this file below "The family": NUMERICAL. Exact values come from check_a.py at reach 6 on dyadic rounding at 30 bits.

## The family (PROVED-HERE that object/family/famgen.py reproduces object/measure.json with 0 differing numerators)

Parameters: Px, Py, m1; for each row j in {0,1}: anch_j, c_j, off_j, hl_j, M_j, integers n_j, L_j; for each level l: dy_l, w_l, phi_l. Row 0 has anch = 0, row 1 has anch = 1.

- Cell: Px x Py. Frame atoms: (0,0) with mass 1 and (Px/2,0) with mass m1.
- Per row: sp = 2 hl/n, tau_i = hl (2i+1-n)/n for i = 0..n-1, W = sum_l w_l, y_l = off + dy_l, mass per atom m_l = M w_l/(n W).
- anch = 0: t = c + tau_i + phi_l sp, atoms at (+-t, +-y_l), 4 per (i,l).
- anch = 1 (c ignored): t = tau_i + sgn(tau_i) phi_l sp with sgn(0) = +1, atoms at (t, +-y_l), 2 per (i,l).
- Atoms per cell: 2 + 4 n_0 L_0 + 2 n_1 L_1. L = 3 gives 2 + 108 + 234 = 344.

Rounding: Lx = round(Px 2^30), x_num = round(x 2^30) mod Lx, likewise y, m_num = round(m 2^30), each value first written with 15 significant digits.

Free real parameters: 10 + 6L, so 28 at L = 3 (2 redundant, one scale of w in each row), against 344 atoms. object/family/L3.par holds the object's values.

Start values, object/family/gen-style formula (how-we-built-it/gen.py), for strip height H = hi - lo: n = max(1, round(2 hl/(p H))); dy_l = (l-(L-1)/2)(1-sqrt m) H/(L-1); phi_l = -1/4 for even l, +1/4 for odd l; w_l = 1; M = n L m H^2; (m,p) from a tile table (how-we-built-it/brick.c, how-we-built-it/tile.c), found by a float search on one strip. Strip ends come from frame equations in how-we-built-it/gen.py, with frame 3.3, 2.75, 4.0. In words: each row of Tomar's kind is replaced by a band of L parallel rows with equal small atoms, alternate levels staggered by half a period. Tomar's measure is itself a member of this family formula, at L = 1, n = (6, 12), phi = 0 with his row values; the family's start values at L = 1 are a different member, with n = (2, 10).

## Value against the number of levels L (exact values)

No search: start values with frame 3.3, 2.75, 4.0, pure formula.

| L | atoms | value | cell area/mass |
|---|---|---|---|
| 1 | 30 | 1.692523379764 | 1.7181673244 |
| 2 | 150 | 1.703884260988 | 1.7192786857 |
| 3 | 344 | 1.706007457027 | 1.7265755319 |
| 4 | 642 | 1.706688614694 | 1.7272674003 |
| 5 | 992 | 1.707713593367 | 1.7288330309 |
| 6 | 1430 | 1.707709714920 | 1.7306739959 |

The same start values, then 180 s of float search over the free parameters, seed 1 (a fixed budget that buys far fewer evaluations at large L: 473158, 11910, 3027, 587, 314).

| L | atoms | value | cell area/mass |
|---|---|---|---|
| 1 | 30 | 1.697321491448 | 1.7130884644 |
| 2 | 150 | 1.708535097976 | 1.7112213104 |
| 3 | 344 | 1.711218535323 | 1.7140365348 |
| 4 | 642 | 1.711046951468 | 1.7155977880 |
| 5 | 992 | 1.711476164444 (third checker's lower end; no check_a run, memory) | 1.7144446209 |

The objects of this table for L = 3, 4 and 5 are not shipped.

The object here is a different search result at L = 3, from an earlier run: 1.711011823672, cell area/mass 1.7138227190 (exact, from the rounded object). The rerun above beats it by 0.000207, which measures how far the search is from converged at L = 3.

Limit. Not established. Above L = 3 the search values are limited by the search budget rather than by L, and the no-search values are not monotone (L = 5 to 6 falls by 3.9e-6). A least-squares fit of A + B/L gives, no search: A = 1.709823 on L >= 2 and 1.709682 on L >= 3 (residuals up to 2.6e-4); with search: A = 1.716272 on L >= 1, 1.713660 on L >= 2 and 1.711645 on L >= 3 (residuals up to 1.4e-3). The searched A moves by more than the residuals as points are dropped, and the residuals are as large as the late steps, so A is a description only, NUMERICAL. What the data do show: the first two thickenings give large gains (0.0114 then 0.0021 with no search), and later ones give about 0.001 or less. No value above any row's cell area/mass occurred.

## Value against columns n at L = 3 (exact)

Columns n_0, n_1 scaled, total row mass M fixed, nothing re-tuned:

| n_0, n_1 | atoms | start values | object's values (L3.par) |
|---|---|---|---|
| 5, 20 | 182 | 1.688246673622 | 1.694713857864 |
| 9, 39 | 344 | 1.706007457027 | 1.711011823672 |
| 18, 78 | 686 | 1.701816457333 | 1.708179492779 |

So at fixed L the value does not rise as n grows without limit: a row tends to a line, and the earlier single-row limit (L = 1, n to infinity) was about 1.6955 (capped search, excludes nothing). The tile's discreteness helps: fixed mass spread thinner loses.

## Rounding (exact)

The same parameters at 24, 26, 28, 30, 34 bits: 1.711011732550, 1.711011862265, 1.711011827618, 1.711011823672, 1.711011822549. Rectangle count 188898 at every width. No coincidence depends on the rounding.

## Commands

    python3 how-we-built-it/gen.py 3.3 2.75 4.0 3 > L3.in
    cc -O2 -o fam5 how-we-built-it/fam5.c -lm; ./fam5 L3.in out 180 6 SEED 0.005     # float search only, never evidence; rerun gives a similar and not an identical object
    python3 -I object/family/famgen.py out.par out.json 30
    python3 -I verify-it-yourself/check_a.py out.json 6
