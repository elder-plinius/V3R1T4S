# Spherical code d = 31, N = 64

## What

64 unit vectors in R^31 (object/31_64.txt) whose maximum pairwise inner product c* = 0.030319733375043224554 (minimal angle 88.26254097 degrees) is lower than the spherical-codes.org table cosine 0.030322662292 for (d, N) = (31, 64), read from /plain fetched 2026-11-01T14:32Z, by 2.93e-6; the index row has no proven-optimal mark and no 'needs more optimization' text, and no newer arXiv result for (31, 64) was found.

Conditions recorded by the panel gate: the arXiv check covered the newest 15 results for "spherical code" and for "Tammes" (2026-11-01T14:32Z); the posted code /data/31/64 was not fetched; no upload to spherical-codes.org was made.

## Check it yourself

From this folder, Python 3 standard library only (under 1 second on a laptop):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. The checker reads the coordinates as exact decimals, computes squared distances and inner
products exactly with `fractions`, and takes square roots with `decimal` at 50 digits, with no tolerance.

## Compared to

- Table: Henry Cohn, table of spherical codes, https://spherical-codes.org/ (plain CSV https://spherical-codes.org/plain)
- Cell: d = 31, N = 64, row `31,64,0.030322662292`; index row credits I. Vahteristo, arXiv:2610.19988.
- Fetched: 2026-11-01T14:32Z (sha256 b7c6a76fe07eab18f4da729f1162a65d1e5042678d7568013b1d49737df254c1).
- Our value: c* = 0.030319733375043224553889612958408072340355255022322 (50 digits, from object/31_64.txt), lower than the table cosine by 0.000002928916956775446110387041591927659644744977678.

## Not claimed

Not optimality, and nothing about any other (d, N). No upload to spherical-codes.org/upload-code was made. The
arXiv check covered the newest 15 results for "spherical code" and for "Tammes" at 2026-11-01T14:32Z; a paper using other
wording, or one posted later, would not have been seen. The posted code /data/31/64 was not fetched.

## Credits

- Henry Cohn, spherical-codes.org (https://spherical-codes.org/), maintainer of the table.
- Ilmari Vahteristo, "New spherical codes by tuning an annealing solver", arXiv:2610.19988, the table's entry for (31, 64).
- Bank target and criterion: V3R1T4S, `spherical-codes-cohn-table` (https://github.com/elder-plinius/V3R1T4S).
- Contributor: benmeadows.
