# REPRODUCE skeptic verdict: claim N = 38, Ne (q = 0.095)

context: subagent (Claude Code Agent tool, fresh context)

Scope: I read only the claim package (claim/CLAIM.md, claim/REPRODUCE.md, claim/object/, claim/data/, and claim/checker/ after my own checker was written and run). My own code and its raw outputs are in panel/reproduce_work/ (read_table.py, my_check.py, object_run1.txt, object_run2.txt, calib_polished_run1.txt, calib_polished_run2.txt, calib_unpolished.txt, author_run1.txt, author_run2.txt). Nothing inside claim/ was modified.

## Definition I checked against (quoted from the success criterion in claim/CLAIM.md)

> "Coordinates ( > = 12 digits) of N atoms, for an N with rows on the live table (...), that form a certified local minimum of the classical E_LJ = 4 sum (r^-12 - r^-6): gradient norm < 1e-9, analytic Hessian of that E_LJ with exactly 6 eigenvalues of magnitude < 1e-6 and none below -1e-6. In addition, E_sp = E_LJ + (q/2) sum sqrt(lambda_i) over the 3N-6 nonzero eigenvalues, with q = 0.01 (Xe), 0.03 (Ar) or 0.095 (Ne), must be STRICTLY LOWER (direction: min) by at least 5e-4 than the lowest tabulated value in that species' column for that N (minimum over the A/B/C rows) (...). The checker must first reproduce the table rows 17A, 31B, 38A and 38B from their posted point files to 5e-5 with the same code. Structures re-optimised on the quantum-corrected surface do not count: the convention is a classical minimum plus its harmonic ZPE."

## My independent checker (written before opening claim/checker/check_lj_zpe.py)

- Coordinates parsed as exact decimal strings (Fortran D exponents accepted). Significant digits counted on each coordinate string.
- E_LJ, the gradient and the analytic Hessian (pair sum over i < j, V = 4(r^-12 - r^-6), unit masses) all computed in Python Decimal at 60 digits. Hessian pair block: K = a I + b d d^T, with a = V'/r = -48 r^-14 + 24 r^-8 and b = (V'' - V'/r)/r^2 = 672 r^-16 - 192 r^-10.
- Internal cross-checks: the gradient against central finite differences of E (Decimal, h = 1e-12): max deviation 4.9e-22. The Hessian against central finite differences of the analytic gradient: max deviation 1.4e-20.
- Eigenvalues from numpy eigh on the Hessian rounded to float64. Cross-checks: numpy eigvals (max diff 4.1e-12); Decimal Rayleigh quotients with the eigh eigenvectors (max diff 6.8e-13); |H v| for the 6 analytic rigid-body vectors (<= 8.5e-14); the projected Hessian's nonzero spectrum against eigh (max diff 1.0e-12). The sum of sqrt(lambda) is also computed from the Decimal Rayleigh quotients.
- Bar: read by my own stdlib HTML parser (panel/reproduce_work/read_table.py) from claim/data/table.html. It found 77 data rows. N = 38 has rows 38A (Ne -106.47765) and 38B (Ne -107.42431). **Lowest Ne for N = 38 = -107.42431 (row 38B)**, which matches the value the claim uses.

## Object: claim/object/N38_Ne.xyz (checked as written, no polish), copied from my program's output

- atoms read: 38; significant digits per coordinate: min 18, max 18 (0 coordinates below 12)
- geometry: min pair distance 1.031582, max pair distance 4.149025, max nearest-neighbour distance 1.102179 (one connected cluster)
- E_LJ (Decimal 60) = -168.984987247421833
- gradient 2-norm = 1.641070e-13 (max |component| 5.385048e-14); requirement < 1e-9: OK
- the 6 near-zero eigenvalues: -3.082503e-15, -2.220145e-14, 2.248148e-14, -2.516913e-14, 6.109552e-14, 1.859784e-13
- count |lambda| < 1e-6: 6; count lambda < -1e-6: 0; nonzero eigenvalues: 108 (= 3N-6)
- lowest nonzero eigenvalue = 8.097800344288e-01; largest = 1.258550638482e+03 (no eigenvalue anywhere near the 1e-6 thresholds)
- sum sqrt(lambda) over the 108 nonzero eigenvalues = 1264.316865599853 (float64 and Decimal-RQ agree to all printed digits)
- certified classical minimum: YES (it is a stationary point of the classical surface to 1.6e-13, so not a quantum-surface re-optimisation)
- E_Xe = -162.6634029194, E_Ar = -150.0202342634, **E_Ne = -108.9299361314** (claimed -108.929936: matches)
- **bar = -107.42431 (38B); bar - E_Ne = 1.5056261314** (claimed 1.505626: matches); required margin 5e-4: BEATS

## Calibration gate with my code (polished on the classical surface; calibration only)

Each posted point file was Newton-polished (Decimal gradient, float64 pseudo-inverse step with the 6 rigid-body modes dropped). Each converged in 2 to 3 steps to gradient < 1e-30. The max coordinate displacements were 6.7e-7 (17A), 2.1e-6 (31B), 2.0e-6 (38A) and 4.1e-6 (38B). Every polished point is a certified minimum (6 zero modes, none negative). Diffs (mine - table):

| row | E_LJ (mine) | Xe diff | Ar diff | Ne diff |
|---|---|---|---|---|
| 17A | -61.317994660111 | -3.361e-6 | -7.614e-7 | +2.686e-6 |
| 31B | -133.293821966342 | -2.425e-6 | -3.342e-6 | +3.677e-6 |
| 38A | -173.928426590629 | +5.909e-6 | +9.090e-7 | +7.158e-6 |
| 38B | -168.519989335395 | +4.133e-6 | +1.070e-6 | -6.383e-6 |

All 12 diffs are below 5e-5 (max |diff| 7.16e-6): CALIBRATION PASS. For reference, without polishing, 17A, 31B and 38A fail (Ne diffs up to 2.7e-4). Their posted coordinates are not stationary (gradient about 1e-4), so the rotational modes are not zero modes. This is why the polish is needed. It is used only for calibration and never for the object.

## Author's commands (claim/REPRODUCE.md), run after my own checks

- All four calibration commands: `RESULT: PASS`, exit 0. Their diffs are identical to mine to the printed digits (for example 38A Ne +7.16e-06 and 38B Ne -6.38e-06). Minor note: the author's polish stops at its 60-iteration cap for 31B/38A/38B because its double-precision gradient bottoms out near 1e-13, above its 1e-13 tolerance. The final gradients are about 1e-13, so this has no effect.
- Object command: min significant digits 18, E_LJ -168.984987247422, gradient norm 1.641e-13, 6 zero modes (max |zero mode| 9.653e-14), lowest nonzero 8.097800e-01, E_Ne -108.929936, bar - E_sp = 1.505626, `certified classical minimum: YES`, `BEATS BAR`, `RESULT: PASS`, exit 0.
- `--selftest`: PASS.
- The author's formulas (pair sum over i < j, phi'/r, 672 s^-8 - 192 s^-5 block term, (q/2) sum sqrt over the 3N-6 nonzero eigenvalues) agree with mine. Every author number matches mine.

## Integrity and determinism

- sha256(claim/object/N38_Ne.xyz) = 31155172b650ba08dc63be96d76a7f189e754612e2d6e7183a744ac6c1270fe1, which equals claim/object/SHA256.txt.
- sha256(claim/data/table.html) = 5e8632e8ab257910961ae596019c6a7fa9335c68e4d7c08e8552f0fb1751177b with size 27710 bytes. Both match the scout record in claim/CLAIM.md and the Content-Length in claim/data/table_headers.txt.
- Determinism: I ran my checker twice on the object and twice on the calibration set, and the author's full command set twice. Each pair of outputs is byte-identical.

## Mismatches / caveats

- No mismatch in any number or property I checked.
- Cosmetic: claim/CLAIM.md gives the fetch time as 19:16:16Z, while the server Date header in claim/data/table_headers.txt reads 19:16:21 GMT. A 5 s clock offset does not matter.
- Outside this role's file-only scope:
  - I did not search the literature. The criterion's clause "lower by at least 5e-4 than any published harmonic-ZPE value for the same N and q that the skeptic finds" therefore has to come from another panel member.
  - I could not confirm that the table and point files match the live site, because I was told not to fetch anything. The saved table matches its recorded hash. The calibration reproduces all 12 tabulated values to <= 7.2e-6, which is strong internal evidence that the point files and the formula are genuine.

Verdict: every property I was asked to check holds when computed from the saved files by my own code, and the author's commands reproduce the same numbers:
- at least 12 digits per coordinate
- gradient norm < 1e-9
- exactly 6 |lambda| < 1e-6 with none below -1e-6
- E_Ne = -108.929936
- bar -107.42431 read from the table
- margin 1.505626 >= 5e-4
- calibration gate to 5e-5
- sha256
- determinism

pass: true
