# Run it yourself

## Verify (fresh shell, from this folder; Python 3 standard library only)

    shasum -a 256 -c SHA256SUMS            # or: sha256sum -c SHA256SUMS
    sh verify-it-yourself/run_checks.sh

The second command runs `python3 -I -B verify-it-yourself/check_p2.py` and exits with status 0 on PASS, 1 on FAIL.
Expected output (verify-it-yourself/RECEIPTS.md has the real run this was copied from; the per-step seconds and the
last few bits of the recomputed roots may differ on your machine, every "ok" line and the last line must not):

```
V3R1T4S p2 checker: bond threshold of row #22, (2/3)(3^3,4^2) + (1/3)(4^4), row word TSS
python 3.14.2

[0] object files
      object/TSS_bond_roots.tsv sha256 ed0b5fed4861c42b0acb4e91b3cc64916917819bd977f2ceaeb2e2368ef9b157
ok    object/TSS_bond_roots.tsv matches SHA256SUMS
      object/p2_value.json sha256 51d575bafaa6558f1f65bd6cd46f1fd2bc113e4717d93994d9bbbdeccec68c23
ok    object/p2_value.json matches SHA256SUMS
ok    INDEX.csv sha256 of object/p2_value.json

[1] lattice identity: row tiling TSS built from its definition
      torus W=6 x 6 rows: V=36 E=84 F=48 face sizes [3, 4]
      vertex configurations {'3^3.4^2': '2/3', '4^4': '1/3'}
      z-bar = 2E/V = 14/3
ok    Euler characteristic V - E + F = 0 (torus)
ok    faces are triangles and squares, 360 degrees at every vertex
ok    fractions (2/3) 3^3.4^2 + (1/3) 4^4, as in row #22
ok    z-bar = 14/3 (table: 4 2/3)
ok    JSON names table row 22, word TSS, lattice (2/3)(3^3,4^2) + (1/3)(4^4)
ok    JSON names bank target site-percolation-2-uniform-lattices-thresholds, partial win p2
ok    control: word S gives only 4^4
ok    control: word T gives only 3^6
ok    control: word TS gives only 3^3.4^2

[2] transfer matrix (Lambda_open = Lambda_closed on W x infinity cylinders)
ok    square bond W=2 root 0.50000000000000000 vs 1/2 = 0.50000000000000000 (diff 0.0e+00, 0.0s)
ok    square bond W=3 root 0.50000000000000011 vs 1/2 = 0.50000000000000000 (diff 1.1e-16, 0.1s)
ok    square bond W=4 root 0.50000000000000000 vs 1/2 = 0.50000000000000000 (diff 0.0e+00, 0.3s)
ok    square bond W=5 root 0.50000000000000011 vs 1/2 = 0.50000000000000000 (diff 1.1e-16, 1.6s)
ok    triangular bond W=2 root 0.34729635533386077 vs 2 sin(pi/18) = 0.34729635533386066 (diff 1.1e-16, 0.0s)
ok    triangular bond W=3 root 0.34729635533386061 vs 2 sin(pi/18) = 0.34729635533386066 (diff -5.6e-17, 0.4s)
ok    triangular bond W=4 root 0.34729635533386061 vs 2 sin(pi/18) = 0.34729635533386066 (diff -5.6e-17, 2.3s)
ok    TSS bond W=2 root 0.44528826191126114 vs tsv 0.44528826191126109 (diff 5.6e-17; 0.1s)
ok    TSS W=2 largest state spaces open 25, closed 28 = tsv columns 4-5 (25, 28); period states 3
ok    TSS bond W=3 root 0.44529702219858164 vs tsv 0.44529702219858214 (diff -5.0e-16; 0.4s)
ok    TSS W=3 largest state spaces open 111, closed 118 = tsv columns 4-5 (111, 118); period states 10
ok    TSS bond W=4 root 0.44529105331797153 vs tsv 0.44529105331797153 (diff 0.0e+00; 1.8s)
ok    TSS W=4 largest state spaces open 424, closed 448 = tsv columns 4-5 (424, 448); period states 35
ok    TSS bond W=5 root 0.44528839219117400 vs tsv 0.44528839219117405 (diff -5.6e-17; 7.4s)
ok    TSS W=5 largest state spaces open 1597, closed 1673 = tsv columns 4-5 (1597, 1673); period states 126
ok    TSS bond W=6 root 0.44528752047593861 vs tsv 0.4452875204759385 (diff 1.1e-16; 29.1s)
ok    TSS W=6 largest state spaces open 6014, closed 6263 = tsv columns 4-5 (6014, 6263); period states 462
ok    calibration TS bond W=2 root 0.41961541967036320 vs how-we-built-it/data/tm/TS_bond.tsv 0.41961541967036314 (diff 5.6e-17; 0.0s)
ok    calibration TS bond W=3 root 0.41964553371975327 vs how-we-built-it/data/tm/TS_bond.tsv 0.41964553371975533 (diff -2.1e-15; 0.3s)
ok    calibration TS bond W=4 root 0.41964456822376600 vs how-we-built-it/data/tm/TS_bond.tsv 0.41964456822376661 (diff -6.1e-16; 1.6s)

[3] object/TSS_bond_roots.tsv against object/p2_value.json
ok    sequence_tm equals the tsv (W and p strings), 9 widths
ok    widths are consecutive from 2
ok    tsv columns 3-5 are non-negative times and state counts

[4] PREREG rule 4 and PREREG.v2 from the sequence
      last four widths [7, 8, 9, 10]: differences -9.5827e-08, -3.8782e-08, -1.8846e-08
ok    last four monotone with shrinking steps: rule 4 main branch
      E1 (W=8..10) = 0.445287065459697  D = 5.4386
      E2 (W=7..9) = 0.445287072207185  D = 6.1510
      E3 (pc + A W^-4 + B W^-6 + C W^-8, W=7..10) = 0.445287058166765
      sigma_B = max(|E1-E2| 6.7475e-09, |E1-E3| 7.2929e-09) = 7.2929e-09
      E1 by window end W=7,8,9,10: 0.445287048235348, 0.445287075128411, 0.445287072207185, 0.445287065459697
      drift_3 = 1.7224e-08   2.87 sigma_B = 2.0931e-08   sigma_v2 = 2.0931e-08
ok    JSON value 0.445287065459697 = E1 to its printed digits (diff 9.5e-17)
ok    JSON sigma_rule4 7.293e-09 = sigma_B rounded (7.293e-09)
ok    JSON sigma_v2 2.093e-08 = sigma_v2 rounded (2.093e-08)
ok    JSON sigma is the PREREG.v2 sigma
ok    JSON method: E1 of PREREG rule 4 on W=8,9,10, sigma by PREREG.v2
      calibration: TS E1 (W=8..10) = 0.419640362745204  D = 4.5323; reference 0.41964035886369
ok    JSON TS calibration value 0.419640362745204 = E1 of how-we-built-it/data/tm/TS_bond.tsv to its printed digits
ok    JSON TS reference '0.41964035886369(2) Scullard-Jacobsen 2020'
ok    JSON TS calibration delta 3.882e-09 = value - reference (3.882e-09), within 5e-8 (PREREG rule 9)

[5] p2 bar and table comparison
ok    the-record-we-beat/cell.json table value 0.44528611(40)
ok    JSON table_value 0.44528611(40)
ok    stated sigma 2.093e-08 <= 5e-8 (PREREG rule 9, '7 digits')
      this value  0.445287065(21)   [E1 = 0.445287065459697, sigma 2.093e-08]
      table value 0.44528611(40)  [Wikipedia, row #22 bond, 'citation needed']
      delta = +9.5546e-07   combined sigma = 4.0055e-07   delta / combined = 2.385
      |delta| / table sigma = 2.389   (|delta| > the table's stated 4e-7)
      reading: within 3 combined sigma (rule 9 'confirms'); difference larger than the table's stated error bar

checks failed: 0   time 47 s
PASS
```

More widths: `python3 -I -B verify-it-yourself/check_p2.py --wmax 7` adds W = 7 (on the build machine under load,
W = 7 alone took about 225 s wall clock and gave 0.44528724327564667 against the tsv's 0.44528724327564689).

To compare with the live table: fetch https://en.wikipedia.org/wiki/Percolation_threshold once with a plain client,
find row 22 in the section "2-uniform lattices" and compare its bond cell with the-record-we-beat/cell.json
("0.44528611(40) [citation needed]" on 2026-10-16T07:52:05Z). If the cell changed, edit nothing here; the comparison
in this package is with the value as fetched.

## Rebuild the object (how it was found)

how-we-built-it/COMMANDS.md has the exact commands (clang, clang++ and python3; no other dependencies):
build code/tm/tm.cpp and code/eig/eig.c, compute the TSS bond roots p(W) for W = 2..10 with tm (W = 10 takes about
5-30 minutes and 1-2 GB) and cross-check them with eig, then run code/tm/extrap.py (PREREG rule 4: E1, E2, E3,
sigma_B) and code/check/sigma_v2.py (PREREG.v2) on the root table. object/TSS_bond_roots.tsv is the tm root table
(columns: W, p(W), seconds, largest open-sector and closed-sector state counts) and object/p2_value.json records the
value, the two sigmas and the sequence those scripts produce. Reruns of the roots agree with the saved table to a few
units in the 15th decimal, not bit for bit (panel/reproduce.md: worst 2.72e-15 over 38 values).
