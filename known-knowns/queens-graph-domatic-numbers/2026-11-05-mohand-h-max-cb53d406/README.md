# Queens graph Q_11: a domatic 19-partition (dom(Q_11) >= 19)

## What
The file with sha256 cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4 is an explicit partition of all 121 squares of the 11x11 board into 19 classes, each dominating Q_11, which proves dom(Q_11) >= 19, one above the lower bound 18 in Table 1 of Lauri's Corrigendum (DML 18 (2026) 34-35), and says nothing about the upper bound 20.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh`. Expected last line: `PASS`. Time: under a second on a laptop.

## Compared to
| table | cell | value there | value here | source | fetched (UTC) |
|---|---|---|---|---|---|
| Table 1 of J. Lauri, Corrigendum, Discrete Math. Lett. 18 (2026) 34-35 | dom(Q_11), lower end of 18-20 | 18 | 19 | https://doi.org/10.47443/dml.2026.195 | 2026-11-05T01:24:39Z |

OEIS A292192 (domatic number of the n x n queen graph) lists terms only up to n = 10.

## Not claimed
- No upper bound: this package proves only dom(Q_11) >= 19, not dom(Q_11) = 19. (The contributors also computed an
  exact certificate that Q_11 has no domatic 20-partition, from exhaustive lists of minimal dominating 5- and 6-sets and
  a rational LP dual; it is not in the DRAT/LRAT form the bank requires and it is not part of this package.)
- Nothing about idomatic or total domatic numbers, or about Q_12.

## Credits
- Juho Lauri, Improved bounds on the domatic numbers of queens graphs, Discrete Math. Lett. 16 (2025) 94-99,
  https://doi.org/10.47443/dml.2025.112, and its Corrigendum, Discrete Math. Lett. 18 (2026) 34-35,
  https://doi.org/10.47443/dml.2026.195 (definitions, Table 1, the counts of minimum dominating sets used as calibration).
- OEIS A292192 (Eric W. Weisstein; extended by Andrei Zabolotskii from Lauri's paper).
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S). Credit for this package: mohand-h-max.
