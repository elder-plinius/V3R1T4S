# Langton's ant: the least highway onset g(k) from starts with at most k black cells, k = 0..11, with proof of minimality

🕸️ **Graphs, games and automata** · standard · tractability ★★★★☆ · compute: laptop-minutes to laptop-hours (two exhaustive forward searches over first reads, one core each) · open as of 2026-11-03

## The problem

Langton's ant (RL rule: on a white cell turn right, on a black cell turn left; flip the cell; step forward) starts at the origin facing north on a grid with finitely many black cells. Let onset(C) be the least t such that, from update t on, the ant's turn sequence is the period-104 highway word. From the blank grid the onset is 9977 (J. Propp; OEIS A126978, a(n) = 104n + 9977). Let g(k) be the least onset over all configurations with at most k black cells, and f(T) the least k with g(k) <= T. Jillhewar ('Finite-Support Periodic Highways of Langton's Ant', Research Square preprint, 2026, doi:10.21203/rs.3.rs-10516269/v1) proves a periodic-realisability criterion and gives an explicit 11-cell black seed on which the ant is on the highway at time 0, so g(11) = 0; minimality of 11 is not claimed there. H. Ke (github.com/kehao95/langtons-ant-core) gives a Lean-checked proof that the blank-grid highway, once entered, is permanent (Highway.blank_entry_permanent, used in one_black/lean/StandardTrace.lean), a Lean-checked proof with committed witness tables that every one-black state reaches the standard period-104 trace, and a four-cell boundary port (Zenodo doi:10.5281/zenodo.23402413, which resolves to v0.3.1 of 31 Oct 2026: from the boundary origin facing east, four black cells launch the standard highway while the ant stays in x >= 0). The port is a fixed pose in a half-plane, not the free-grid g(4). As of status_checked, no source found states g(k) for any 1 <= k <= 10, or proves that fewer than 11 cells cannot give onset 0; Ke's one-black witness tables were not checked for g(1). A submission in V3R1T4S PR #641 uses this target id; it is under review and not established.

## What counts as a win

CONFIRMED by the complete table g(k), k = 0..11, with the ant at the origin facing north (fixed frame; onset = the number of updates already done when the ant's future turn sequence equals the period-104 highway word, so the blank grid gives 9977), together with every minimiser for each k (fixed frame, modulo cells never read), such that: (i) every value and every minimiser is re-confirmed by exact simulation with an independent simulator; (ii) completeness (no configuration with at most k black cells has a smaller onset) is shown exhaustively and uncapped for every k = 1..10 by two independently written exhaustive checkers sharing no code, each with a planted-positive control and a blank-grid control (k = 0 is the classical blank-grid value; for k = 11 minimality is trivial since onset 0 is least possible, and the 11-cell minimiser list must come from an exhaustive onset-0 search over all 104 highway phases that also shows no 10-cell start is on the highway at time 0); and (iii) the persistence of the highway after the onset is either derived from a published proof (Ke's Lean theorem blank_entry_permanent, or Jillhewar's periodic-realisability criterion) or stated explicitly as an assumption in the claim, with the blank highway checked numerically for at least 30000 updates past 9977. The table must not already be published at verification time (check OEIS, Jillhewar's paper and repository, Ke's repository (including the one-black witness tables) and Zenodo records, and a fresh search).

## Partial wins

- **p1:** g(k) for k = 1..6 (and g(0) = 9977), with conditions (i)-(iii) of the success criterion met for those k.

## How a win is checked

Re-implement the RL ant from the definition. Re-simulate the blank grid (onset 9977, OEIS convention) and every minimiser; confirm the onset with a highway test (the ant's state and the cells it will read at t+104 equal those at t shifted by (+-2,+-2), and no black cell lies in the highway's future sweep) and confirm that onset - 1 fails. For completeness, re-run two independently written exhaustive searches (for example forward branching over the first read of each cell, with a grid-phase match against the 104 highway phases, versus a light-cone search with the forced turn word) uncapped at value - 1 (no configuration) and at value (the minimisers) for every k; controls: blank onset 9977, a planted positive reported one step above its onset, and no 10-cell start on the highway at time 0. Calibrate on Jillhewar's 11-cell seed (onset 0).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/kehao95/langtons-ant-core>

## Sources

- <https://oeis.org/A126978>
- <https://doi.org/10.21203/rs.3.rs-10516269/v1>
- <https://github.com/Atharva12456/langtons-ant-highway>
- <https://github.com/kehao95/langtons-ant-core>
- <https://doi.org/10.5281/zenodo.23402413>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Forward first-read search: branch only when the ant first reads a cell (black or white), counting black cells used, and prune with a completion cost against the 104 highway phases.
- A second, independent light-cone search that forces the highway turn word from a candidate onset and bounds how far back the transient can reach.
- Brute force over a small box for k <= 3 as a third check, and Jillhewar's criterion for the onset-0 case.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Onset conventions differ by one (blank 9977 updates done vs. index 9976); state which.
- Reflection is not a symmetry of the RL rule (it swaps L and R); g(k) is rotation-invariant, but minimisers must be listed in one fixed frame, modulo cells never read.
- Ke's four-cell port is for a fixed boundary pose in a half-plane; it is not a free-grid value of g(4).
- A capped search is not an exhaustive one.
- Ke's one-black witness tables cover every one-black start and may already give g(1); check them before claiming k = 1 as new.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/langton-ant-ft-minimal-seed.md
```

Already set up? Say `run V3R1T4S on langton-ant-ft-minimal-seed`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `langton-ant-ft-minimal-seed`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
