# report — extender-r2 lens, run 2026-11-06-0918

claim level: partial_win_claim (exhaustive, uncapped verification for a stated range of (n, k); single-context,
unpanelled)

## Result
For every k = 26, 27, 28, the complete enumeration of run 2026-10-29-0821's pipeline (deep_rig.py, bytes unchanged;
QEXP = 495, 1040 digits, η = 0.001, X0 = 10^6) finds **0 product solutions**. The ratio loop was split over 4
processes by code/shard_rig.py.

| k | ratios | enumerated pairs | window candidates | product solutions |
|---|---|---|---|---|
| 26 | 21262 | 1989788 | 490397 | 0 |
| 27 | 16402 | 417007 | 411576 | 0 |
| 28 | 21262 | 2241996 | 553418 | 0 |

Sums are from code/sum_shards.py (out/shard_sums.txt). For k = 26 and 27 they equal the unsharded run of 2026-10-29
exactly, which checks that the split covers each ratio once. k = 28 had timed out at 3 h on one core then; the four
shards took 5681–5732 s for it. With the small-X step (out/search_N1.1e6.txt: COMPLETE, K = 147, 0 exact-equal) and
the rigor lens's ratio and margin checks, every step of the PREREG holds.

The claim ("for every k with 26 ≤ k ≤ 28, every n ≤ 10^494 and every m ≥ n + k, M(m,k) ≠ M(n,k)") is assembled in
../../claim/. Status: PROMISING, single-context, unpanelled. The panel is a later run's first job.

dead lines:
- **One process per k:** k = 28 did not finish in 3 h on 2026-10-29. Superseded by the 4-way ratio split.
- **k ≥ 29 with this pipeline:** 114817 ratios at k = 29 and 30, about 5× k = 28's cost even split 4 ways (> 6 h).
  Dead for standard runs.
- **Kernel-checking the enumeration:** not attempted. The result stays computer-assisted, like the confirmed k ≤ 25
  claim.
