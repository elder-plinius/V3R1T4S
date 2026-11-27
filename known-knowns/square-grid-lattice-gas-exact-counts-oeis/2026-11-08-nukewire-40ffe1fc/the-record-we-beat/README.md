# The record we beat (table snapshot)

| source | URL | fetched (UTC) | HTTP | sha256 |
|---|---|---|---|---|
| OEIS A210662 b-file | https://oeis.org/A210662/b210662.txt | 2026-11-08T19:49Z, 20:12Z, 20:40Z, 21:10Z (byte-identical) | 200 | 05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d |
| OEIS A210662 entry page | https://oeis.org/A210662 | 2026-11-08T21:15Z | 200 | (page HTML; the load-bearing FORMULA line extracted to a210662_formula_line.txt) |

Live state at every fetch: 378 terms = triangular rows 1..27, last term
T(27,27); rows 28 and 29 absent. The FORMULA line maps columns 1-11 and the
diagonal to A000045, A030186, A033506..A033514, A028420 — nothing beyond;
the entry's other A-numbers are OEIS mechanical context/adjacent neighbors.
The compared-against record for this claim is therefore: the b-file (all 378
cells reproduced exactly by both runs) plus the published column/diagonal
sequences (the eleven disclosed k=1..11 cells match them exactly; the 17
claimed cells have no corresponding sequence — see panel/novelty.md).
