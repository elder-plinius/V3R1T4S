# CRITERION skeptic verdict

Target: ccd-quantum-lj-zpe-rare-gas-clusters. Claim: one object (`object/N38_Ne.xyz`), one cell (N = 38, Ne, q = 0.095).
What I read: only `claim/` (CLAIM.md, REPRODUCE.md, checker/check_lj_zpe.py, data/, object/).
Scripts I wrote are in `panel/criterion_work/`: `indep_check.py` (independent exact-rational E_LJ/gradient, a
from-scratch analytic Hessian checked against finite differences, eigenvalues, ZPE, and the gradient of the
quantum-corrected surface), `calib_nopolish.py`, `make_variants.py`, `null_search.py`. Nothing in `claim/` was modified.
Python run with `-I`, numpy only.

## Hashes
- `object/N38_Ne.xyz` sha256 = 31155172b650ba08dc63be96d76a7f189e754612e2d6e7183a744ac6c1270fe1 (matches `object/SHA256.txt`).
- `data/table.html` sha256 = 5e8632e8ab257910961ae596019c6a7fa9335c68e4d7c08e8552f0fb1751177b (matches CLAIM.md).

## Clause by clause

1. **"an N with rows on the live table ... re-fetched immediately before claiming"**: PASS.
   `data/table.html` has exactly two N = 38 rows, 38A (line 383) and 38B (line 397). There is no 38C. The claimant fetched it
   at 2026-10-31T19:16:16Z (HTTP 200, 27710 bytes). I made one plain GET of the same public URL myself: response header
   `Date: Sat, 31 Oct 2026 19:40:18 GMT`, `Last-Modified: Mon, 26 Feb 2018 16:57:01 GMT`, 27710 bytes, and sha256
   5e8632e8...1177b, identical to the claimant's copy. So the bar is the live one.

2. **"Coordinates (>= 12 digits)"**: PASS. The checker printed `min significant digits = 18 (need >= 12): ok`, and my independent
   count is also `18`. Informative only: if every coordinate is rounded to 12 significant digits, the checker gives
   `gradient norm (decimal) = 3.929e-09 ... FAIL`. The certificate therefore depends on the digits after the 12th. The object as
   submitted has 18, which is what the criterion asks for.

3. **Certified classical minimum (gradient norm < 1e-9; analytic Hessian of that E_LJ; exactly 6 |lambda| < 1e-6; none below -1e-6)**: PASS.
   - Checker, object as written, no polish: `E_LJ (50-digit decimal) = -168.984987247422`, `gradient norm (decimal) = 1.641e-13`,
     `Hessian: 6 eigenvalues with |lambda| < 1e-6 (need exactly 6), lowest eigenvalue -9.652857e-14 ... max |zero mode| 9.653e-14,
     lowest nonzero 8.097800e-01: ok`, `certified classical minimum: YES`.
   - Independent code: `E_LJ (exact rational) = -168.984987247421827`, `gradient norm (exact rational) = 1.641e-13`,
     `gradient norm (float64, indep) = 1.811e-13`.
   - Hessian: my Hessian is analytic, written from scratch, and checked against central differences of the analytic gradient:
     `max |H_analytic - H_fd| = 4.76e-08 (max |H| = 6.77e+02)`. Results: `eigenvalues |lambda| < 1e-6: 6 ; lowest = -8.147626e-14 ;
     any < -1e-6: False`, `lowest 5 nonzero eigenvalues: 0.80978003 3.85758931 ...`, `count nonzero = 108`. Projecting out the
     rigid-body modes changes the nonzero spectrum by at most `1.59e-12`. Between the zero modes (about 1e-13) and the lowest
     nonzero eigenvalue (0.81) there is a gap of about 13 orders of magnitude, so the count of 6 cannot depend on where the
     1e-6 cutoff falls.
   - Selftest of the checker: `SELFTEST: PASS`.

4. **ZPE rule (q/2) sum sqrt(lambda) over the 3N-6 nonzero eigenvalues, q = 0.095**: PASS.
   My code gives `sum sqrt(lambda) over 3N-6 = 1264.3168655999` over the 108 nonzero eigenvalues and `E_Ne = -108.92993613`.
   The checker prints `E_Ne = E_LJ + (0.095/2) * sum sqrt(lambda) = -108.929936`. The formula uses unit masses; the
   calibration (clause 7) confirms this is the table's convention.

5. **"STRICTLY LOWER by at least 5e-4 than the lowest tabulated value in that species' column for that N (minimum over the A/B/C rows)"**: PASS.
   I read the Ne column for N = 38 myself: 38A = -106.47765 and 38B = -107.42431 (underlined). The minimum is -107.42431.
   - Checker: `record test Ne: bar -107.42431, E_sp -108.929936, bar - E_sp = 1.505626 (need >= 5e-04 on a certified minimum): BEATS BAR`, `RESULT: PASS`.
   - Independent: `bar - E_Ne = 1.50562613 ; >= 5e-4: True`.
   - The margin is about 3000 times the required 5e-4, and about 1e5 times the worst calibration error (1.09e-5).

6. **"... and lower by at least 5e-4 than any published harmonic-ZPE value for the same N and q that the skeptic finds"**:
   NOT CHECKED BY ME. This is the novelty skeptic's job, and I did no literature search. The claim as worded only compares
   against the table, which is within the criterion's literal scope. It makes no assertion about other literature. My pass
   covers every clause except this one.

7. **Calibration: 17A, 31B, 38A, 38B reproduced to 5e-5 with the same code**: PASS.
   The `--expect` values in REPRODUCE.md match `data/table.html` for all four rows; I checked each, including 31B at lines
   189-195. Checker runs, all `RESULT: PASS`:
   - 17A: diffs -3.36e-06, -7.61e-07, 2.69e-06
   - 31B: diffs -2.42e-06, -3.34e-06, 3.68e-06
   - 38A: diffs 5.91e-06, 9.09e-07, 7.16e-06
   - 38B: diffs 4.13e-06, 1.07e-06, -6.38e-06

   For calibration the checker first applies `--polish`, a Newton polish on the classical surface. It moved atoms by at most
   `4.964e-06`, because the posted files carry only 6 to 14 digits. The energy, Hessian and ZPE code (`certify`) is the same
   path used, without polish, on the object.

   Without polish, the checker's eigenvalue-count gate fails on the posted files (gradient about 1e-4), as expected. My
   independent no-polish evaluation (`calib_nopolish.py`) still matches all 12 tabulated values within 5e-5 (largest |diff|
   `1.09e-05`, 38A Ne). So the polish is not what makes the calibration pass.

8. **"Structures re-optimised on the quantum-corrected surface do not count"**: PASS. The object is stationary on the
   classical surface: classical gradient 1.641e-13, checked as written with no polish. At the same point, the gradient of the
   Ne quantum-corrected surface E_LJ + (0.095/2) sum sqrt(lambda) has norm `6.3992e+01`. The object is therefore a classical
   minimum with its harmonic ZPE added, not a minimum of the quantum-corrected surface.

## Null models and checker discrimination
- The table's own structures do not pass the record test.
  - 38B (polished) against its own bar: `bar - E_sp = 0.000006 ... does not beat bar`, `RESULT: FAIL`.
  - 38A against the Ne bar: `bar - E_sp = -0.946667`, `RESULT: FAIL`.
- Shifting one coordinate of the object by 1e-7 gives `gradient norm (decimal) = 2.164e-05 ... FAIL`, `RESULT: FAIL`. Rounding to 12 digits gives `3.929e-09 ... FAIL`. The gate catches points that are not stationary.
- Naive search baseline (informative, small sample): random-start quenches plus classical basin hopping on LJ38 for 150 s,
  seed 20261031. Result: `distinct certified minima evaluated: 12`, `lowest E_LJ found: -173.252378`,
  `lowest 5 E_Ne found: -106.72435 (-173.25238) ...`, `count with E_Ne < -107.42431 - 5e-4: 0`.
  A cheap search does not reach the bar trivially.

## Scope and wording
- **One object, one cell:** yes. There is a single xyz file and a single cell (N = 38, Ne). The checker also prints
  E_Xe = -162.663403 and E_Ar = -150.020234, but neither beats its column (38A: Xe -166.82835, Ar -152.62818), and the claim
  does not assert them. Nothing is bundled.
- **Words wider than the evidence:**
  - "Calvo-Doye-Wales table": the page in `data/table.html` is signed only "Florent Calvo". The three-author attribution comes
    from outside the package. This is cosmetic and does not change the bar.
  - Nothing in the claim says "global minimum" or "new record versus the literature", and it must not be restated that way.
    The evidence shows only a lower value than the table's lowest N = 38 Ne entry.
  - "certified" means certified against the criterion's numerical thresholds with a double-precision Hessian. Given the
    13-orders-of-magnitude gap in clause 3, that is adequate.

## Verdict
Every clause I could check is met literally, with large margins and independent reproduction: live-table N, digits,
certified classical minimum with an analytic Hessian, the ZPE rule, beating the minimum over the A/B rows by at least 5e-4,
calibration on 17A/31B/38A/38B, and classical rather than quantum re-optimisation. This is a full-criterion win, not a
partial win, on the clauses I checked. The published-harmonic-ZPE clause is outside what I checked, and the overall
acceptance depends on the novelty skeptic.

confirmed_scope: The 38-atom configuration in object/N38_Ne.xyz (sha256 31155172...0fe1), as written with 18 significant digits, is a certified local minimum of the classical Lennard-Jones energy (E_LJ = -168.984987247422, gradient norm 1.641e-13, exactly 6 |lambda| < 1e-6, lowest eigenvalue -9.65e-14), and its harmonic Ne energy E_LJ + (0.095/2) sum sqrt(lambda) over its 108 nonzero eigenvalues is -108.929936, which is 1.505626 below -107.42431, the lowest Ne value (row 38B) for N = 38 on the LJZPE table at www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html (unchanged as of 2026-10-31T19:40Z), with the table convention reproduced on rows 17A, 31B, 38A and 38B to within 1.1e-5; comparison against other published harmonic-ZPE values was not checked by this skeptic.
context: subagent (Claude Code Agent tool, fresh context)
pass: true
