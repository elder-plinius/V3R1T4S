# PREREG: ccd-quantum-lj-zpe-rare-gas-clusters, run 2026-10-31-1915

frozen_at: 2026-10-31T19:19:19Z (from date -u when this file was saved; written before any lens ran and before any attack output existed)

null_test: not needed because every possible claim is an explicit object (coordinates) that a deterministic checker judges against a table value, with a fixed 5e-4 margin. No search statistic, period or "beats chance" claim is made.

## Criterion (verbatim from bank/targets.json)

Coordinates ( > = 12 digits) of N atoms, for an N with rows on the live table (https://www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html, re-fetched immediately before claiming), that form a certified local minimum of the classical E_LJ = 4 sum (r^-12 - r^-6): gradient norm < 1e-9, analytic Hessian of that E_LJ with exactly 6 eigenvalues of magnitude < 1e-6 and none below -1e-6. In addition, E_sp = E_LJ + (q/2) sum sqrt(lambda_i) over the 3N-6 nonzero eigenvalues, with q = 0.01 (Xe), 0.03 (Ar) or 0.095 (Ne), must be STRICTLY LOWER (direction: min) by at least 5e-4 than the lowest tabulated value in that species' column for that N (minimum over the A/B/C rows), and lower by at least 5e-4 than any published harmonic-ZPE value for the same N and q that the skeptic finds. The checker must first reproduce the table rows 17A, 31B, 38A and 38B from their posted point files to 5e-5 with the same code. Structures re-optimised on the quantum-corrected surface do not count: the convention is a classical minimum plus its harmonic ZPE.

Partial wins p1 and p2: verbatim in `target.md`.

## Judge (fixed now)

- Checker: `checker/check_lj_zpe.py` (sha256 3df1b7a13e7f62039b3c252eb892dc3f33f26bc85a1267f8567fe372f7c10711), unchanged from
  the dry run. It runs on the candidate file as written (no `--polish`), with `--bar <species>=<bar> --margin 5e-4`.
- Bars: `tools/bars.tsv`, the minimum per N and species over the A/B/C rows of the table fetched at
  2026-10-31T19:16:16Z (`data/table.html`, sha256 5e8632e8ab257910961ae596019c6a7fa9335c68e4d7c08e8552f0fb1751177b),
  parsed by `tools/parse_table.py`.
- Calibration gate (before any candidate counts): the same checker, with `--polish` allowed only for calibration,
  must reproduce rows 17A, 31B, 38A and 38B from the posted point files in `data/points/` to 5e-5 in every
  species column. If any of the four fails, no claim is made this run.
- Thresholds: gradient norm < 1e-9; exactly 6 eigenvalues |lambda| < 1e-6, none below -1e-6; bar - E_sp >= 5e-4.
  Coordinates written with at least 15 significant digits.
- A candidate found by a search is ranked by the fast evaluator (`tools/ljfast.py`). Only the decimal checker above
  decides whether it beats a bar. Each claim covers one (N, species) cell.
- No baseline step (kit/RUN.md step 3c): this is an explicit object checked against a table value, not a score on data.
- Novelty bar beyond the table: published harmonic-ZPE values for the same N and q (for the NOVELTY skeptic). A
  structure that a later paper already identified for that N and q is a published object.
