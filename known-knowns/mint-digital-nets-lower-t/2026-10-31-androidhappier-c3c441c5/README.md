# A digital (11,24,17)-net over F_2 (MinT constructive value: t = 13)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> The 17 explicit 24x24 F_2 matrices in claim/net_F2_t11_m24_s17.txt (sha256 c3c441c5…) generate a digital (11,24,17)-net over F_2, verified exhaustively over all 67,863,915 compositions by two independently implemented checkers, which is strictly below the MinT "Constructive and digital" value t=13 and at or above the lower bound t=8 as recorded for (b,m,s)=(2,24,17) on 2026-10-31, with literature novelty (criterion 4) not assessed here.

## Criterion 4: literature search

The novelty panel reports searches on October 31, 2026 of the web, arXiv, OEIS, GitHub, MinT, and this repository. Its queries included "digital (11,24,17)-net", binary digital nets, improved t-values and MinT, ordered orthogonal arrays, and GitHub matrix generators; the exact queries and results are in panel/novelty.md. The report found no earlier binary digital (t,24,17)-net with t <= 12. On that basis we submit criterion 4 for maintainer assessment. The original gate did not certify this search, and a search cannot rule out an overlooked or unindexed source; the repository release page timed out.

The submitted matrices were reproduced on November 7, 2026 using how-we-built-it/gvgreedy2.c with seed 101 and pad_full.py. Windows text output used CRLF; after conversion to LF both files matched the packaged files byte for byte, including their SHA-256 values. The earlier novelty note naming gvgreedy4 describes the original report and is corrected below.

The file named claim/net_F2_t11_m24_s17.txt in the run is object/net_F2_t11_m24_s17.txt in this package (same
bytes, full sha256 c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618).
object/net_F2_t11_m24_s17_first13rows.txt holds rows 1..13 of each matrix, which are the only rows the t = 11
condition uses.

Format: lines starting with '#' are comments; 17 blocks separated by blank lines; block i is C_i, one row per line,
row 1 first, 24 digits 0/1, column 1 first.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. It takes about 2 minutes on a laptop: about 85 s for the Python checker and about 20 s
for the C checker, if a C compiler is present. Python 3 standard library only. Details and expected output are in
RUN_IT_YOURSELF.md and verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | MinT value | this package | fetched (UTC) |
|---|---|---|---|---|
| MinT, base 2, Constructive and digital | (m, s) = (24, 17) | t = 13 (s-reduction of a (13,24,24) shift-net) | t = 11 | 2026-10-31T14:58Z; re-fetched 16:09Z and about 16:15Z, unchanged |
| MinT, base 2, Lower bound on t | (m, s) = (24, 17) | t = 8 | 11 is at or above it | same fetches |

URL: http://mint.sbg.ac.at/query.php?b=2&m=24&s=17&p=smt. The snapshot record (fetch times, hashes, the
extracted cell) is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Literature novelty (criterion 4 of the target) was not certified by the original gate. The panel's novelty skeptic
  searched (literature since 2008, code, this repository's PRs) and found no prior digital (t,24,17)-net over F_2
  with t at most 12. That search is recorded in panel/novelty.md but is not certified here.
- No claim about MinT's digital existence value, about any other cell, or about cells derived from this one by
  propagation rules, e.g. (11,23,17) or (11,24,16). Other cells found in the same run are not part of this package.
- Rows 14..24 of each C_i are a unit-vector completion to nonsingular matrices. They play no part in t = 11.
- No claim of optimality: MinT's lower bound is 8, and nothing here says t = 11 is best possible.
- The construction is a randomized greedy search with a fixed seed. It is not a new algebraic construction.

## Credits

- MinT, the online database of (t,m,s)-net parameters by Rudolf Schürer and Wolfgang Ch. Schmid (University of
  Salzburg): http://mint.sbg.ac.at/. It supplies the record compared against (shift-nets, via s-reduction) and the
  lower bound.
- Digital nets and the (t,m,s)-net definition: H. Niederreiter. The Gilbert-Varshamov-style greedy idea follows the
  classical existence arguments that MinT cites for digital nets.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: credited through the GitHub account that submits this folder.
