# Langton's ant: every starting pattern in a 6x6 box reaches the highway (V3R1T4S bank target langton-ant-highway, partial win p1)

## What
All 2^36 black-cell patterns of the 6x6 box x,y in -2..3, with the ant at (0,0) facing north, are reported by the lant4 exhaustive run (attested by per-chunk summaries and sha256, 3 chunks reproduced) to reach the period-104 (+-2,+-2) highway by T_cap <= 375,545 under a certificate I verified to be sound; the independent simulator lantx2, with its own sound certificate, re-captured a frozen hash-uniform 1.000057% sample and all 4096 per-chunk maximum-T_cap masks with no failure, which meets bank partial win p1 for this one box placement and heading.

In plain words: for this box, with the ant at (0,0) facing north, all 2^36 = 68,719,476,736 starting patterns lead to Langton's period-104 highway, each one certified exactly. Two independently written simulators checked this, each with its own capture certificate (proofs in object/docs/METHOD.md). The second simulator re-checked a frozen random 1.000057% sample and all 4096 hard cases with no failure, and so did the panel's own reproduce reviewer. This is evidence for the highway conjecture, not a proof of it.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (from this folder; needs sh, gcc, python3). Expected last line: `PASS`. Takes about 1.5-2 min on one laptop core. Longer optional checks (any sample unit, any full chunk of 2^24 masks with sha256 comparison) are in RUN_IT_YOURSELF.md.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| bank status source (arXiv 2505.05426, V. Lutfalla, "Sideways on the highways") | classical Langton highway conjecture | open; no exhaustive certified verification of a 6x6 (or larger) box found | https://arxiv.org/abs/2505.05426 | 2026-10-20T23:09:38Z (panel re-fetch 2026-10-21T01:08:18Z) |
Details and the other sources checked: the-record-we-beat/RECORD.md and panel/novelty.md.

## Not claimed
- Not a proof of the highway conjecture, and not a counterexample. The bank's full success criterion is not met. Only partial win p1 is claimed.
- One box placement, with the ant at (0,0) facing north. Other placements of the 6x6 box relative to the ant (equivalently, other start headings) are not enumerated. No symmetry reduction is used.
- The exhaustive part is the lant4 run. Its per-mask output (about 70 GB) was not kept. It is attested by per-chunk summaries and sha256 values, and 3 full chunks were reproduced bit for bit. The independent re-check is a 1% sample plus the hard cases, as p1 asks, not a second exhaustive run.
- "Hard cases" means the maximum-T_cap mask of each of the 4096 chunks. The run had no uncaptured, out-of-bounds or fixed-up masks. The global top-4096 masks by T_cap were not listed.
- The panel's first reproduce reviewer failed the earlier version of this claim (panel/reproduce.round1-fail.md): it covered only part of the sample, and the C(s) proof was a sketch. The proof was completed (object/docs/CHANGES.md), and a fresh reproduce reviewer then re-simulated the whole sample and passed.

## Credits
- Langton's ant: C. G. Langton, "Studying artificial life with cellular automata", Physica D 22 (1986).
- Unboundedness of the trajectory: L. A. Bunimovich and S. E. Troubetzkoy (1992); also attributed to Cohen and Kong in the V3R1T4S bank.
- Status source: V. Lutfalla, "Sideways on the highways", arXiv 2505.05426, https://arxiv.org/abs/2505.05426.
- Also read: Zenodo 10.5281/zenodo.21716510 (finite-support periodic highways, https://zenodo.org/records/21716510) and arXiv 2606.26677 (escape times from rectangles, https://arxiv.org/abs/2606.26677).
- Target and verification method: the V3R1T4S bank (https://github.com/elder-plinius/V3R1T4S).
- Contributor: anonymous. Code and checks by V3R1T4S agent runs. The exhaustive run was done on the contributor's own desktop.
