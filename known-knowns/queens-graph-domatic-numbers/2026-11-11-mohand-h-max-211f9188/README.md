# Queens graph Q_10: a total domatic 16-partition (tdom(Q_10) >= 16)

## What
The file claim/tdom-Q10-16-partition.txt (raw-byte sha256 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec) labels each of the 100 squares of the 10 x 10 board with one of 16 labels so that every one of the 16 classes totally dominates the queens graph Q_10 (open neighbourhoods: every square, members included, shares a row, column or diagonal with a different member of the class), hence tdom(Q_10) >= 16, one above the lower bound 15 listed for tdom(Q_10) in Table 1 of Lauri's Corrigendum (Discrete Math. Lett. 18 (2026) 34-35) as re-fetched on 2026-11-11.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh`. Expected last line: `PASS`. Time: under a second on a laptop.

## Compared to
| table | cell | value there | value here | source | fetched (UTC) |
|---|---|---|---|---|---|
| Table 1 of J. Lauri, Corrigendum, Discrete Math. Lett. 18 (2026) 34-35 | tdom(Q_10), lower end of 15-16 | 15 | 16 | https://doi.org/10.47443/dml.2026.195 | 2026-11-11T18:20:59Z |

## Not claimed
- No upper bound is proved here. The upper bound tdom(Q_10) <= 16 is Lauri's (same table); with it, this partition
  gives tdom(Q_10) = 16, but that equality rests on Lauri's bound, not on this package.
- Nothing about domatic or idomatic numbers, or about other board sizes.
- The list used to find the object (216 total dominating 6-sets of Q_10) is not claimed to be complete; the object
  is checked on its own.

## Credits
- Juho Lauri, Improved bounds on the domatic numbers of queens graphs, Discrete Math. Lett. 16 (2025) 94-99,
  https://doi.org/10.47443/dml.2025.112, and its Corrigendum, Discrete Math. Lett. 18 (2026) 34-35,
  https://doi.org/10.47443/dml.2026.195 (definitions, Table 1, total domination numbers used as calibration).
- Hedetniemi, Hedetniemi, Hedetniemi and Hedetniemi, On the domatic numbers of queens graphs, Congr. Numer. 235.
- Overlap with a published object, found by the panel's novelty skeptic: four classes of this partition are reflected
  copies of one total dominating 6-set printed in Lauri 2025, Fig. 3.3(a) (the published total domatic 15-partition of
  Q_10). No published partition was used as a seed (see panel/gate.md).
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S). Credit for this package: mohand-h-max.
