# Reproduce

Run everything from a copy of this folder (scripts compile and write files next to themselves). Needs Python 3 with
numpy, scipy and mpmath, and any C compiler; below, `CC` is that compiler (for example `cc`, `gcc`, or
`python -m ziglang cc` from the ziglang pip package). `PY` is the Python. Times are for one core of a 2018 desktop.

## 0. Integrity
    python -c "import hashlib;[print('BAD',l.split()[1]) for l in open('MANIFEST.sha256') if hashlib.sha256(open(l.split()[1],'rb').read()).hexdigest()!=l.split()[0]];print('manifest checked')"

## 1. The lattice is #23 (vertex types, fractions, zbar, orbits; also rejects near misses) - seconds
    $PY evaluator-first/code/test_lattices.py
Expected among the lines: `ok    #23: fractions {'3^3.4^2': Fraction(1, 2), '4^4': Fraction(1, 2)}, zbar 9/2, 2 orbits`
and the last line `TESTS: PASS (0 failures)`. Compare with row 23 in table/table_record.md.

## 2. Build the evaluators
    cd exact-polynomial/code && $CC -O2 -o tmcrit.exe tmcrit.c && $PY make_stream.py && $CC -O2 -o tmcrit_stream.exe tmcrit_stream.c && cd ../..
    cd evaluator-first/code && $CC -O2 -o nzwrap.exe nzwrap.c && $CC -O2 -o nzwrap2.exe nzwrap2.c && cd ../..
(The scripts call the programs by these names on every system. Add `-lm` if your compiler needs it.)

## 3. Method A (transfer matrix)
Regression net (published sequences and exactly solvable thresholds, including kagome site and (3,12^2) site) - about a minute:
    $PY exact-polynomial/code/regress.py
Expected last line `REGRESSION: PASS`.
Recompute the smallest bases of #23 (deterministic; n <= 8 takes under a minute, n = 10 a few minutes):
    $PY exact-polynomial/code/run_series.py "#23" site 1 8 r23_site_check.txt
    $PY exact-polynomial/code/run_series.py "#23" bond 1 6 r23_bond_check.txt
Each `pc` must equal the line with the same n in exact-polynomial/out/r23_site_series.txt (bond: r23_bond_series.txt).
Extrapolate (the frozen rule; prints every fit of the family, then p_TM and sigma_TM):
    $PY exact-polynomial/code/extrapolate.py exact-polynomial/out/r23_site_series.txt
Expected last line `p_TM 0.57176453954634  sigma_TM 1.04e-7  (24 estimates)`. Bond:
    $PY exact-polynomial/code/extrapolate.py exact-polynomial/out/r23_bond_series.txt
Expected `p_TM 0.45844602208062  sigma_TM 3.75e-8`. Calibrations of the same rule against published values:
    $PY exact-polynomial/code/calib_rule.py exact-polynomial/out/jacobsen_table2_square_site.txt 0.59274605079210 10 21
    $PY exact-polynomial/code/calib_rule.py exact-polynomial/out/st_bond_series.txt 0.41964035886369 6 12
    $PY exact-polynomial/code/extrapolate.py exact-polynomial/out/st_site_series.txt
The streamed program gives bit-identical roots (optional, a few minutes): `$PY exact-polynomial/code/test_stream.py`.

## 4. Method B (Monte Carlo), from the saved histograms - each command a minute or less
    $PY timeline-aligner/code/agreement.py exact-polynomial/out/r23_site_series.txt timeline-aligner/mc/r23_site 0.5720 2e-4
Expected: `primary L2>=16     p_MC 0.571766679 +- 0.000001393`, `stability: ... STABLE`, `(a) ... AGREE`, `(b) ... WITHIN`.
    $PY timeline-aligner/code/analyze_mc.py "timeline-aligner/mc/r23_site_check/*.hist"
Expected `p_L 0.571764522 +- 0.000022729` (the 2048 x 512 torus, not in the fit).
    $PY timeline-aligner/code/agreement.py exact-polynomial/out/r23_bond_series.txt timeline-aligner/mc/r23_bond 0.45844622 4e-7
Expected `primary L2>=16     p_MC 0.458445217 +- 0.000001553` (criterion (c): within 3 sigma of 0.45844622, sigma <= 2e-6).
Calibrations with exactly known thresholds:
    $PY timeline-aligner/code/fss_mc.py timeline-aligner/mc/kagome_site --exact 0.65270364466614 > kagome_fit.txt
    $PY timeline-aligner/code/fss_mc.py timeline-aligner/mc/square_site --exact 0.59274605079210 > square_fit.txt
    $PY timeline-aligner/code/common_offset.py kagome_fit.txt square_fit.txt outputs/triangular_test_output.txt
    $PY evaluator-first/code/triangular_test.py timeline-aligner/mc/triangular_site 10
    $PY timeline-aligner/code/agreement.py exact-polynomial/out/st_site_series.txt timeline-aligner/mc/st_site 0.550213 3e-6
Expected: kagome +0.57 sigma, square -0.76 sigma, `D +4.216e-07 +- 6.472e-07 (+0.65 sigma) -> PASS`,
`TRIANGULAR ESTIMATOR TEST: PASS`, (3^3,4^2) site `(a) ... AGREE`. All expected values: outputs/one_look_output.txt.

## 5. Monte Carlo with fresh seeds (statistical, minutes to an hour)
Each block is about 4.5e9 site visits (about 3 minutes on one idle core, about 7 minutes on a loaded machine):
    $PY timeline-aligner/code/mc_worker.py "#23" site 1 4 16 4 77000 fresh_mc nzwrap2.exe
    $PY timeline-aligner/code/analyze_mc.py "fresh_mc/*.hist"
(L1 x L2 = 64 x 16, seed 77016, 4 blocks.) Compare with the saved L2 = 16 value p_L 0.571766140 +- 0.000001740.
With so few blocks the jackknife error of the fresh run is itself very uncertain; the spread of single-block crossings
in the saved L2 = 16 data is a standard deviation of about 1.35e-5 per block (so about 6.8e-6 for the mean of 4
blocks). Any other size and seed works the same way (L1 = 4 L2). mc_worker.py writes the lattice file to
evaluator-first/lat/. The faster nzwrap2 is byte-identical to nzwrap: `$PY evaluator-first/code/test_nzwrap2.py work`.
