# Generalised ant LLRL: the least onset of the period-384 highway g(k) from starts with at most k non-zero cells, k = 0..K0, with proof of minimality

🕸️ **Graphs, games and automata** · standard · tractability ★★★☆☆ · compute: laptop-hours to laptop-days (two exhaustive forward searches; the largest k need many cores or several nights) · open as of 2026-11-03

## The problem

The generalised Langton's ant LLRL has colours 0..3; on a cell of colour c it turns by the c-th letter of LLRL (left for 0, 1 and 3, right for 2), recolours the cell c+1 mod 4 and steps forward. Gajardo, Lutfalla and Rao ('Ants on the highway', Natural Computing 2025, arXiv:2409.10124) report that LLRL has an overwhelmingly dominant highway of period 384: 22.95% of their random starts reached a highway within their horizon, and among those the period-384 highway appeared in 99.9997% of cases, with rare highways of periods 308, 380, 388 and 928, and that from the blank grid the ant reaches it 'after 256100 steps' (a rounded figure). Start the ant at the origin facing north on a grid with finitely many non-zero cells. Let onset(C) be the least t such that, from update t on, the sequence of colours read is periodic with non-zero displacement and equals the blank-grid period-384 highway word (up to its phase). Let g(k) be the least onset over configurations with at most k non-zero cells (any non-zero colour costs 1), and K0 the least k with g(k) = 0. Lutfalla's note on LLLR (arXiv:2506.10482) and GLR's LLR seed give minimal seeds for other rules; as of status_checked, no source found gives g(k) for LLRL for any k >= 1, or K0. A submission in V3R1T4S PR #709 uses this target id; it is under review and not established.

## What counts as a win

CONFIRMED by the complete table g(k) for k = 0..K0, with the ant at the origin facing north (fixed frame; onset = the number of updates already done when the ant is on the period-384 highway), together with every minimiser for each k (fixed frame, modulo cells never read), such that: (i) every value and every minimiser is re-confirmed by exact simulation with an independent simulator and an exact translation certificate (the ant's state and every cell it will read at t+384 equal those at t shifted by the highway displacement, with no non-zero cell in the future sweep); (ii) completeness (no configuration with at most k non-zero cells has a smaller onset) is shown exhaustively and uncapped for every k = 1..K0-1 by two independently written exhaustive checkers, each with controls (blank-grid onset, a planted positive, a known negative); (iii) K0 and its minimiser list come from exhaustive onset-0 searches by both checkers, which also show that K0-1 cells never give onset 0. g(0) is the blank-grid onset, computed exactly and stated in the claim's convention (GLR's 256100 is rounded). The table must not already be published at verification time (check GLR arXiv:2409.10124, Lutfalla's papers and simulator, OEIS and a fresh search).

## Partial wins

- **p1:** g(k) for k = 0..5, with conditions (i) and (ii) met for those k, and K0 with its minimiser list established as in (iii).
- **p2:** g(k) for k = 0..6, with conditions (i) and (ii) met for those k.

## How a win is checked

Re-implement the LLRL ant from the definition. Re-simulate the blank grid and every minimiser with an independent simulator and check the translation certificate at the onset; confirm that onset - 1 fails. Re-run two independently written exhaustive searches (for example a first-read search with a phase-completion test against the 384 highway phases, versus a fixed-depth light-cone search with the forced read-colour word and a certificate) uncapped at value - 1 (no configuration) and at value (the minimisers) for every k; controls: the blank-grid onset, a planted positive, and K0-1 cells giving no onset-0 start.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2409.10124>

## Sources

- <https://arxiv.org/abs/2409.10124>
- <https://arxiv.org/abs/2506.10482>
- <https://arxiv.org/abs/2505.05426>
- <https://lutfalla.fr/ant/highway.html?antword=LLRL>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- First-read search: branch only when the ant first reads a cell, on each of the four colours, and prune with a completion test against the 384 highway phases.
- A second, independent light-cone search that forces the read-colour word from a candidate onset, with an exact translation certificate.
- Brute force over small boxes for small k as a third check.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The turn word does not determine the read-colour word (colours 0, 1 and 3 all turn left); phase tests must use the colours read, not the turns.
- Onset conventions differ by one; state which, and compute the blank-grid onset exactly rather than using GLR's rounded 256100.
- Only the dominant period-384 highway counts; GLR's rare highways of periods 308, 380, 388 and 928 are different targets.
- Reflection is not a symmetry (it swaps L and R); minimisers are listed in one fixed frame, modulo cells never read.
- A capped search is not an exhaustive one.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/llrl-ant-minimal-seed.md
```

Already set up? Say `run V3R1T4S on llrl-ant-minimal-seed`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `llrl-ant-minimal-seed`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
