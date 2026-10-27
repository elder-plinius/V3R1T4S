# Site percolation threshold of 2-uniform lattice #23: p_c = 0.57176454(10)

## What
Confirmed scope (panel/gate.md, status CONFIRMED_SOLUTION), quoted word for word:

> For 2-uniform lattice #23, (1/2)(3^3,4^2)+(1/2)(4^4), the site percolation threshold is 0.57176454 +- 0.00000010 by the frozen transfer-matrix extrapolation (n <= 16), and it agrees within 1.53 combined sigma with an independent Monte Carlo wrapping-probability value of 0.5717667 +- 0.0000014 on tori up to 512 x 128 cells, while the same transfer-matrix code reproduces the table's citation-needed #23 bond value 0.45844622(40) to 2e-7 and the exact kagome and (3,12^2) site thresholds, the value lies 1.2 table sigma from the table's 0.5720(2), and the recorded literature search found no published #23 site value more precise than 2e-4.

Target: site-percolation-2-uniform-lattices-thresholds (V3R1T4S bank), full success criterion. One cell: row 23 of
the "2-uniform lattices" table on Wikipedia's "Percolation threshold" page, lattice (1/2)(3^3,4^2) + (1/2)(4^4)
(rows of squares and triangles in the pattern S S S T), site column. The table lists 0.5720(2) (Neher, Mecke and
Wagner 2008); this value has a one-sigma uncertainty about 1900 times smaller and lies 1.2 of the table's sigma below
it.

The object: object/threshold_23_site.json (sha256 cfa04190dfd6667063f64bce3c3ac85bf679bed0e6dd4b67dda75229728efadb),
with the transfer-matrix root series it is extrapolated from (object/tm/) and the Monte Carlo block histograms of
#23 site, #23 bond and kagome site at every fitted torus size (object/mc/: 1080 files, each listed with its sha256 in
the JSON, packed in 18 .tar.xz archives, one per lattice and torus size, listed in object/mc/ARCHIVES.sha256). NUMERICAL: the uncertainty of the transfer-matrix value is a convergence spread of a frozen family of
fits, calibrated on published sequences, not a rigorous bound.

## Check it yourself
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (about a minute on a laptop; Python 3 standard library only, no numpy, no compiled code).
The checker hashes every data file, rebuilds the lattice from geometry and checks its vertex types, extrapolates the
root series by the frozen rule in exact rational arithmetic, recomputes every Monte Carlo crossing, jackknife error and
finite-size fit from the histograms, and checks the criterion's numeric conditions and the claimed value. Its real
output is in verify-it-yourself/RECEIPTS.md. Recomputing the roots themselves and new Monte Carlo data:
RUN_IT_YOURSELF.md.

Packaging (2026-10-26, at the maintainer's request in PR #391): the Monte Carlo histograms of object/mc/ and the
calibration data of how-we-built-it/timeline-aligner/mc/ are packed in .tar.xz archives (how-we-built-it/pack_mc.py),
so that the package has under 100 files, each under 1 MB. No data changed: every histogram has the sha256 listed in
object/threshold_23_site.json (unchanged, sha256 cfa04190...), the checker reads them from the archives, and
verify-it-yourself/unpack_mc.py restores the original folders.

## Compared to
| table | cell | table value | this value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| Wikipedia, "Percolation threshold", section "2-uniform lattices" | row 23, (1/2)(3^3,4^2) + (1/2)(4^4), site | 0.5720(2) | 0.57176454(10) | https://en.wikipedia.org/wiki/Percolation_threshold | 2026-10-18T05:11:54Z (NOVELTY panelist, raw wikitext, HTTP 200, sha256 588b98d38a819a6712a7b3b497a8df7e5a955285ba0b7bc3bace199f2c742ba3); also 2026-10-17T23:58:23Z (same bytes) |

Literature: no site value for this lattice newer or more precise than Neher, Mecke and Wagner 2008 (arXiv API and web
searches by the run and again by the NOVELTY panelist; details in the-record-we-beat/TABLE_RECORD.md and
panel/novelty.md).

## Not claimed
- No rigorous bound: sigma_TM = 1.04e-7 is the spread of the frozen extrapolation family. On Jacobsen's square-site
  sequence the same rule's error is at most 0.02 sigma at every cut n_max = 10..21. The independent Monte Carlo value
  0.5717667(14) tests it only at the 1.4e-6 level, and lies 1.53 combined sigma above it.
- The Monte Carlo fit uses tori up to 512 x 128 cells. The bank's "tori up to L >= 2048" is read as an example (it
  follows "for example"); the one 2048 x 512 torus is a low-statistics consistency check (sigma 2.3e-5), not in the fit.
- Criterion (c), bond half: the bond value reproduced is the table's 0.45844622(40) for row 23, which the table marks
  "citation needed"; no paper is named for it.
- No values for the other two-uniform lattices are claimed here. Interim transfer-matrix values for rows 20-22 are
  in how-we-built-it/ only as run outputs. The row 22 bond value is the subject of a separate submission by another
  contributor (PR #239), not of this one.

## Credits
- Kaust-a-laut, with Claude Code (Anthropic) running claude-opus-5-5, using the V3R1T4S kit.
- Table value: R. A. Neher, K. Mecke and H. Wagner, J. Stat. Mech. (2008), https://arxiv.org/abs/0708.3250 (table in
  https://arxiv.org/abs/0708.3251).
- Transfer-matrix eigenvalue form of the critical-polynomial root: J. L. Jacobsen, https://arxiv.org/abs/1507.03027;
  critical polynomials: C. R. Scullard and J. L. Jacobsen, https://arxiv.org/abs/1209.1451, and J. L. Jacobsen,
  https://arxiv.org/abs/1401.7847. Square-site sequence used for calibration: Jacobsen 2015 (above).
- Wrapping-probability Monte Carlo: M. E. J. Newman and R. M. Ziff, https://arxiv.org/abs/cond-mat/0005264.
- Calibration values: (3^3,4^2) bond, Scullard and Jacobsen (above); (3^3,4^2) site, P. N. Suding and R. M. Ziff,
  https://arxiv.org/abs/cond-mat/9811416; kagome and (3,12^2) site exact values as listed on the Wikipedia page.
