# Binding success criterion and partial wins (from bank target llrl-ant-minimal-seed)

## Success criterion (bank)
CONFIRMED by the complete table g(k) for k = 0..K0, with the ant at the origin facing north (fixed frame; onset = the number of updates already done when the ant is on the period-384 highway), together with every minimiser for each k (fixed frame, modulo cells never read), such that: (i) every value and every minimiser is re-confirmed by exact simulation with an independent simulator and an exact translation certificate (the ant's state and every cell it will read at t+384 equal those at t shifted by the highway displacement, with no non-zero cell in the future sweep); (ii) completeness (no configuration with at most k non-zero cells has a smaller onset) is shown exhaustively and uncapped for every k = 1..K0-1 by two independently written exhaustive checkers, each with controls (blank-grid onset, a planted positive, a known negative); (iii) K0 and its minimiser list come from exhaustive onset-0 searches by both checkers, which also show that K0-1 cells never give onset 0. g(0) is the blank-grid onset, computed exactly and stated in the claim's convention (GLR's 256100 is rounded). The table must not already be published at verification time (check GLR arXiv:2409.10124, Lutfalla's papers and simulator, OEIS and a fresh search).

## Partial wins (bank)
- p1: g(k) for k = 0..5, with conditions (i) and (ii) met for those k, and K0 with its minimiser list established as in (iii).
- p2: g(k) for k = 0..6, with conditions (i) and (ii) met for those k.

## This package
This claim is partial win **p2** only, adding g(6)=139. Conditions (i) and (ii) for k = 6 are established in this package. g(0..5) and K0=12 were CONFIRMED_PARTIAL as p1 (run 2026-10-24-1605 / draft PR #709) and are cited as background, not re-opened here. The full success criterion (all k up to K0-1) is not met.

## Bank corrections reflected here
- GLR's 99.9997% figure is the share among random starts that reached a highway (22.95% did), not among all starts (statement background; not a claimed cell).
- Only the dominant period-384 highway counts; rare highways of periods 308, 380, 388 and 928 are out of scope (already stated in README Not claimed).
