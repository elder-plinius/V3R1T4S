# Queens graph Q_12: a domatic 21-partition (dom(Q_12) >= 21)

## What
The file claim/dom-Q12-21-partition.txt (sha256 e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e on its raw CRLF bytes) partitions all 144 squares of the 12 x 12 board into 21 nonempty classes (labels 0..20), each dominating the queens graph Q_12. This gives dom(Q_12) >= 21, one more than the lower bound 20 in Table 1 of Lauri's Corrigendum (Discrete Math. Lett. 18 (2026) 34-35), and it meets the named partial win p1 for the (dom, n = 12) cell.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh`. Expected last line: `PASS`. Time: under a second on a laptop.

## Compared to
| table | cell | value there | value here | source | fetched (UTC) |
|---|---|---|---|---|---|
| Table 1 of J. Lauri, Corrigendum, Discrete Math. Lett. 18 (2026) 34-35 | dom(Q_12), lower end of 20-21 | 20 | 21 | https://doi.org/10.47443/dml.2026.195 | 2026-11-11T17:27:34Z |

OEIS A292192 (domatic number of the n x n queen graph) lists terms only up to n = 10.

## Not claimed
- No upper bound is proved here. The upper bound dom(Q_12) <= 21 is Lauri's (same table); with it, this partition
  gives dom(Q_12) = 21, but that equality rests on Lauri's bound, not on this package.
- Nothing about idomatic or total domatic numbers, or about other board sizes.
- The lists used to find the object (8 dominating 6-sets, 6,712 minimal dominating 7-sets of Q_12) are not claimed
  to be complete; the object is checked on its own.

## Credits
- Juho Lauri, Improved bounds on the domatic numbers of queens graphs, Discrete Math. Lett. 16 (2025) 94-99,
  https://doi.org/10.47443/dml.2025.112, and its Corrigendum, Discrete Math. Lett. 18 (2026) 34-35,
  https://doi.org/10.47443/dml.2026.195 (definitions, Table 1, the eight dominating 6-sets of Q_12 used as calibration).
- Overlap with published objects, found by the panel's novelty skeptic: three classes of this partition (two dominating
  6-sets and one 7-set) are identical to classes of the domatic 20-partition of Q_12 printed in Lauri 2025, Fig. 3.2(c);
  the 7-set also appears in Fig. 3.3(c). No published partition was used as a seed (see panel/gate.md).
- Hedetniemi, Hedetniemi, Hedetniemi and Hedetniemi, On the domatic numbers of queens graphs, Congr. Numer. 235
  (the counting upper bound dom(Q_12) <= 21, as reported by the novelty skeptic).
- OEIS A292192 (Eric W. Weisstein; extended by Andrei Zabolotskii from Lauri's paper).
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S). Credit for this package: mohand-h-max.
