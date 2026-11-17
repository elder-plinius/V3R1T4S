# report — extender-r3 lens, run 2026-11-09-0917

claim level: partial_win_claim (exhaustive, uncapped-in-m verification for k = 29, n <= 10^494; single-context,
unpanelled; depends on the rigor lens's margin for X >= 10^6)

## Result
The complete continued-fraction enumeration for k = 29 (deep_rig.py, bytes unchanged, sha256 0e7d7d72…; QEXP = 495,
1040 digits, η = 0.001, X0 = 10^6), split over 4 processes by shard_rig.py, finds **0 product solutions**.

| shard | admissible_r | enumerated pairs | window candidates | product solutions | time |
|---|---|---|---|---|---|
| 0 | 28705 | 833627 | 822606 | 0 | 5386 s |
| 1 | 28704 | 832852 | 821979 | 0 | 5390 s |
| 2 | 28704 | 833512 | 822638 | 0 | 5384 s |
| 3 | 28704 | 832536 | 821629 | 0 | 5402 s |
| sum (code/sum_shards.py, out/shard_sums.txt) | 114817 | 3332527 | 3288852 | 0 | |

The admissible_r counts add up to the full ratio list (114817, equal to the rigor lens's independent audit), so the
four shards cover every ratio exactly once.

dead lines:
- **The 2026-11-07 time forecast (0.9 h on 4 cores):** the run took 1.5 h. The per-ratio cost at k = 29 is about
  0.188 s, 1.6x the k = 27 rate the forecast used. Superseded by tonight's measurement.
- **k = 31 in a standard run** (344452 ratios): at this rate about 18 CPU-h of enumeration alone. Dead for standard
  effort.
- **Kernel-checking the enumeration:** not attempted; the result stays computer-assisted, like k <= 28.
