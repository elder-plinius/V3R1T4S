# CLAIM — Langton's ant, 6x6 box: every starting pattern is captured by a highway (bank partial win p1)

target id: langton-ant-highway (V3R1T4S bank). Credit: anonymous.

## One-sentence claim
Every one of the 2^36 = 68,719,476,736 initial patterns of black cells inside the 6x6 box below (all other cells white, ant at (0,0) facing north) reaches the period-104 diagonal highway within 2,000,000 steps, each with an exact highway-capture certificate; this exhaustive run was re-checked by an independently written simulator with a different certificate on a seeded uniform random 1.000057% sample (687,234,013 masks) and on all 4096 per-chunk hardest masks, with no failure and exact agreement wherever compared.

## Criterion (verbatim from the V3R1T4S bank, repo/bank/targets.json)
success_criterion: "CONFIRMED only for (a) a finite initial configuration of black cells together with a machine-checkable proof that the ant never produces the highway (e.g. a proven different eventual behaviour verified by exact simulation to a provably repeating state), or (b) a formal (Lean/Isabelle) proof of the conjecture. Long transients without the highway are never counterexamples."
partial win claimed — p1: "Exhaustive verification of all initial configurations in a 6x6 (or larger) box under a stated symmetry reduction, each with a highway-capture certificate (window at t equals window at t+104 shifted by (+-2,+-2), ant beyond all black cells, and no initial black cell anywhere in the future sweep of the highway) re-checked by an independent simulator on a random 1% sample plus all hard cases."
bank verification_method: "Exact integer simulation by an independent implementation. For highway detection, verify that the ant's local window at time t equals the window at time t+104 shifted by (+-2,+-2), and that the ant is beyond all initial black cells in the drift direction, so the future is provably periodic. For exhaustive claims, re-run a random 1% sample plus all hard cases with the independent simulator."
Only p1 is claimed. The full success criterion (a counterexample or a formal proof) is NOT claimed.

## Convention (exact)
- Box 6x6. Mask bit b (0..35) is the cell (x, y) = (b mod 6 - 2, floor(b/6) - 2), so x, y in -2..3. Bit set = black. Every other cell is white.
- Ant starts at (0,0) with heading 0 (north). Directions: 0:(0,+1), 1:(+1,0), 2:(0,-1), 3:(-1,0).
- One step: g = colour of the ant's cell; heading d = (d + 1 + 2g) mod 4 (white: turn +1 = right/clockwise in these coordinates, black: turn -1); flip the cell; move one cell in direction d.
- Cap: 2,000,000 steps (a mask counts as captured only if the certificate holds from a step T_cap <= 2,000,000).
- All 2^36 masks were enumerated, mask 0 .. 2^36-1.

## Symmetry reduction (stated)
None. Every one of the 2^36 patterns of the box is simulated. The start position (0,0) inside the box and the start heading (north) are part of the convention, not a reduction: the same box with the ant starting east/south/west is, after rotating the plane, the ant starting north in a rotated 6x6 placement (e.g. x in -3..2), which is a different set of patterns and is NOT claimed here. Mirror images are not identified (reflection swaps the ant's chirality).

## Evidence (all in this folder)
1. The exhaustive run: data/user-chunk-sums/chunk_0..4095.sum — 4096 chunks of 2^24 masks from an exhaustive run of lant4 (code/lant4pkg, derived from the earlier lant2/lant.c) on a 24-thread desktop, ~40 h. Each line: range, lines, CAP/UNCAP/OOB counts, maxtcap and its mask, number of (vx,vy,dir) classes, overflow fix-ups, and sha256 of the full per-mask output (the ~70 GB per-mask output itself was not kept). Totals: 68,719,476,736 CAP, 0 UNCAP, 0 OOB, 0 fix-ups; max T_cap 375,545 at mask 40920836116.
2. Independent simulator lantx2 (code/lantx2/lantx2.c), written from the specification without the lant code, with a different, simulation-based certificate (METHOD.md). Its T_cap equals lant's T_cap on all 65,536 4x4 masks and all 33,554,432 5x5 masks (data/validation/), so exact per-mask agreement is the comparison standard.
3. Hard cases: all 4096 per-chunk maxtcap masks — lantx2 captures all 4096 with T_cap identical to the summaries (data/hard-cases/).
4. Random sample: seeded hash rule frozen before the run (data/sample/README.md): 687,234,013 masks, all captured by lantx; in all 16,384 sample units the sample max T_cap <= the chunk's maxtcap (data/sample/).
5. Cross-checks of the exhaustive engine: lant4 rebuilt from source agrees per mask with lantx2 on 3 x 2^20 masks; full chunks 0, 2439 and 4095 rerun with lant4 reproduce the run's sha256 exactly, and lantx2 captures all 3 x 16,777,216 masks of those chunks with the same maxtcap (data/validation/lant4_vs_lantx2.txt, fullchunks.txt, fullchunk4095_cleancopy.txt).

## What is NOT claimed
- Not a proof of the highway conjecture; a finite search is evidence, not proof (label: NUMERICAL).
- The exhaustive coverage rests on the lant4 run's summaries; per-mask output exists only as per-chunk sha256 values. The independent re-check is a 1% sample plus the hard cases (as p1 asks), not a second exhaustive run.
- "Hard cases" = the maximum-T_cap mask of each of the 4096 chunks, not the global top-4096 masks by T_cap.
- Other placements of the 6x6 box relative to the ant (equivalently, other start headings) are not enumerated.
- Both certificates have full proofs in METHOD.md (lantx2's X in section 1, lant4's C(s) in section 2). Every sampled and hard-case mask is certified by lantx2's certificate as well.
