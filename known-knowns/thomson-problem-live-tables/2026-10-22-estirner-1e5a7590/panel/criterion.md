# Criterion skeptic report: thomson-problem-live-tables, N = 743

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)

injection_suspected: none (scanned CLAIM.md, REPRODUCE.md, tools/, object/, inputs/ including all table HTML; nothing addressed to a reviewer)

## What was run (all inside a copy of claim/, outputs written outside it, one CPU job at a time)

- `tools/certify.py check object/thomson_743.txt` (no polish).
- `tools/certify.py polish` on object/thomson_743.txt, inputs/points_743_1.dat, inputs/merged125_cand_743.txt.
- `tools/verify_stdlib.py object/thomson_743.txt --bar 264837.5858504 --expect 264837.4538033452076921018 --others <polished riesz> <polished m125> inputs/points_743_1.dat inputs/merged125_cand_743.txt` (bar set to the live table cell, not to #125).
- An independent checker written by this skeptic (does not import the claim's tools): digit count, normalisation, energy at mp.dps 30 in two arithmetic forms (|x_i-x_j| and (2-2 x_i.x_j)^-1/2, mp.fsum) and at dps 50, tangent gradient at dps 30 and 50, its own float64 Riemannian Hessian (SVD tangent basis, full 2N spectrum, rotation modes identified by eigenvector overlap instead of projected out), and energies of all comparison configurations at dps 50.
- sha256 of every package file; parsing of every table page for N rows and posted-file links.

## Clause by clause

1. **"N points on the unit sphere (coordinates to >= 20 digits)"**: PASS. 743 lines, 2229 tokens, min significant digits = 30, min decimal places = 30; max | |x_i| - 1 | in the raw file (dps 60) = 7.9943e-31; min pair distance 0.12529905841283723; 743 distinct points.

2. **"for some N <= 1500 listed in at least one live table"**: PASS. N = 743 <= 1500; row present in inputs/tables/ccd_riesz_s1_index.html: `<TD>743</TD> <TD>264837.5858504</TD>` (C1, links dat/points_743_1.dat).

3. **"E* computed in mpmath at 30 digits from the normalized coordinates"**: PASS.
   - certify.py check: `E_mp30 = 264837.4538033452076921018`
   - independent, dps 30, |d| form: 264837.4538033452076921018; dot form: 264837.4538033452076921018
   - independent, dps 50: 264837.45380334520769210183586395215; |E30 - E50| = 3.5592e-26
   - verify_stdlib (decimal, 40 digits): E = 264837.4538033452076921018358640, |E - expected| = 3.586e-20

4. **"STRICTLY LOWER than the minimum energy for that N over ALL of: Deeter, CCD Thomson, CCD Thomson2, CCD Riesz s=1, Wikipedia, (N = 282) EinsteinArena ... by at least 1e-6"**: PASS.
   - Deeter (inputs/tables/deeter.html): 521 rows, N = 4..524, no 743 row; point-file links e.4.txt..e.524.txt only (521 links).
   - CCD Thomson table: 409 rows, N = 10..972, no 743 row (neighbours 732, 752).
   - CCD Thomson2 table: 36 rows, N = 400..4352, no 743 row (neighbour 752).
   - CCD Riesz index: one exponent (s = 1), 53 configurations, N 512 to 9913; s=1 page: 53 rows, 743 row = 264837.5858504.
   - Wikipedia: 234 rows, N = 2..470, no 743 row.
   - EinsteinArena: only for N = 282, not applicable.
   - Minimum over all listed tables for N = 743 = 264837.5858504 (single row). Margin table_min - E* = 0.1320470547923078981641360479 (>= 1e-6: True). verify_stdlib: `bar - E = 0.1320470548 (need >= 1e-6)`.
   - Null check (table rounding): the cell is rounded to 7 decimals; margin exceeds rounding by ~6 orders.

5. **"each re-fetched live immediately before claiming"**: satisfied on the record. All nine sha256 values in CLAIM.md's table match the files in inputs/ (checked: deeter cf138c88..., ccd_thomson 5466173..., ccd_thomson2 caf24199..., riesz index b28eed78..., riesz s1 eeac3235..., wikipedia 39da937f..., points_743_1.dat 68ac9c8d..., both 404 pages 9646e03a...). Fetch stamps 2026-10-22T01:59:59Z..02:00:07Z (tables, HTTP 200) and 02:06:16Z..02:06:17Z (two 404s); the package files are timestamped 2026-10-22 02:07Z, i.e. about 7 minutes after the last fetch. Caveat: CLAIM.md gives no explicit claim timestamp (file mtimes are the only evidence), and this role had no network, so liveness of the fetches is accepted from a complete, internally consistent record, not re-observed. Non-blocking.

6. **"certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0)"**: PASS.
   - Gradient at the saved coordinates: certify.py check `gT_mp30 = 4.47655e-24`; independent dps 30 = 4.47657e-24, dps 50 = 4.47645e-24 (not a precision artefact); verify_stdlib 4.476e-24.
   - mpmath Newton actually run (certify.py polish on the object): 1 mp step, `gT_final_mp30 = 7.64142e-27`, `E_star_mp30 = 264837.4538033452076921018`, `E_change_input_to_final = -8.27180612553e-25`, L-BFGS 0 iterations (object already at the minimum).
   - Hessian, claim's tool: n_eigs 1483 = expected 1483, min_eig 4.042259181123571, n_nonpositive 0, delta_bound 3.195798010861421e-07, rotation Rayleigh quotients ~1e-13, hessian_pass true (after polish: min_eig 4.042259181115254).
   - Hessian, independent build: dim 1486, lowest5 = [-1.279521354964889e-12, -4.650951372456415e-13, -2.171957795786231e-13, 4.042259181120501, 4.594075417363012]; rotation-span overlap of the three lowest eigenvectors = 1.0000000000000016, 0.9999999999999996, 1.0000000000000016 (4th, 5th: 4.3e-14, 1.1e-14); 1483 non-rotational eigenvalues, min 4.042259181120501, count <= 0: 0; spectral norm 4454.117512529888, eps*n*||H|| = 1.469672966352012e-09 << 4.04. Float64 is adequate for the sign with this margin; the criterion does not demand interval arithmetic.

7. **"different basin from every posted table configuration for that N: polishing each table's own point file ... with the same routine must give an energy higher than E* by >= 1e-6"**: PASS.
   - Posted files for N = 743: Deeter none (no row, no e.743.txt link); CCD Thomson xyz/743.xyz and Thomson2 xyz/743.xyz both HTTP 404 (inputs/tables/*_xyz_743.404.html are Apache 404 pages); Wikipedia posts no point files; Riesz dat/points_743_1.dat = inputs/points_743_1.dat. So the clause reduces to one file.
   - certify.py polish inputs/points_743_1.dat: E_input 264837.5858503620609750247, |g| 2.13618e-6 -> E_star 264837.5858503620609677129, gT 4.59704e-24, hessian_pass true (min_eig 2.234761350825306). Independent dps 50: 264837.585850362060967712922635, E - E* = 0.1320470168532756110867709132 (>= 1e-6: True). verify_stdlib: `E_other - E = 0.1320470169`.
   - Null check p1 (table integrity): raw posted file energy 264837.58585036206 reproduces the 7-decimal cell 264837.5858504; no integrity finding.

## Bundling, stretching, subsumption

- **Not subsumed by merged #125.** inputs/merged125_cand_743.txt (sha256 9293bcd2..., matches CLAIM.md) is itself a critical point: E 264837.5287041150044362828, |g| 1.57068e-24, after the same polish unchanged, hessian_pass true (min_eig 3.633597124296364). The claimed object is 0.07490076979674418096 lower (verify_stdlib `0.0749007698`), so it is a distinct, strictly lower minimum, not a re-claim. The link between that file and "#125" rests only on the sha256 stated in CLAIM.md.
- **Full vs p3.** p3 covers "N > 1500 or beating only that table" with weaker certification (|g| < 1e-15, Lanczos smallest eigenvalue). The full criterion explicitly admits any N <= 1500 "listed in at least one live table" and names the Riesz s=1 table among the tables; its only p3-only carve-out is "N > 1500". N = 743 is <= 1500 and was certified with the full criterion's stronger tests (|g| < 1e-20, full 1483-eigenvalue decomposition), so p3 is subsumed by the full result here, not an alternative to it.
- **Not bundled**: one N, one object file.
- **Stretched wording in CLAIM.md, excluded from scope**: "#125 ... the lowest previously known N = 743 value" and the Amore-Wales / Roshal literature values are not checkable from the package (no source files) and are not part of the criterion; they are left out of confirmed_scope.

criterion_met: full

confirmed_scope: The 743-point configuration object/thomson_743.txt (30-digit coordinates, unit norm to 8e-31) has mpmath dps-30 Coulomb energy 264837.4538033452076921018, tangent-gradient norm 4.48e-24 at the saved coordinates and 1483 = 2N-3 positive non-rotational tangent-Hessian eigenvalues in float64 (smallest 4.042259), which is 0.1320470548 below 264837.5858504, the only N = 743 row among the fetched tables in inputs/tables/ (ccd_riesz_s1_index.html), while polishing inputs/points_743_1.dat and inputs/merged125_cand_743.txt with tools/certify.py ends 0.1320470169 and 0.0749007698 above it.

pass: true
