# Kissing number lower bounds in dimensions 9-23

📊 **Record tables** · moonshot (famous, long odds) · tractability ★☆☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Find more unit spheres touching a central unit sphere without overlapping, i.e. a set of nonzero vectors of equal norm with pairwise angle >= 60 degrees, in dimensions 9-23. Cohn's table (checked 2026-10-20): d9 306, d10 510, d11 604, d12 841, d13 1154, d14 1932, d15 2564, d16 4320, d17 5730, d18 8358, d19 12460, d20 19448, d21 31560, d22 49896, d23 93150. Attributions: d11 592 (Ganzhinov 2025) -> 593 (AlphaEvolve) -> 604 (Bianchi-Kwon-Pappu-Zou, arXiv:2606.10402, EinsteinArena, 'recently solved, certified'); d12 840 -> 841 (Takhanov-Assylbekov-Yun, arXiv:2606.18984); d14 1932 (Ganzhinov 2025); d18 7654 -> 8358 (A. Kravatskiy 2026, github.com/alexlegeartis/KissingNumbers); d19 11948 (Ho, arXiv:2603.10425) -> 12460 and d21 29768 -> 31560 (K. Li 2026, 'Improved kissing numbers in nineteen and twenty-one dimensions', preprint, listed by Cohn as 'hexagon: 2610.00248'). Sep 2026 work (arXiv:2609.35051, 2609.21591) only improved d >= 25; the d18, d19 and d21 gains reached Cohn's table after 2026-10-03.

## What counts as a win

Success means K vectors in R^d (9 <= d <= 23) given exactly (integer/rational coordinates or exact algebraic numbers in a specified field), all with identical squared norm N and every pair with <x,y> <= N/2, verified in exact arithmetic, no two coinciding, with K STRICTLY GREATER (direction: max) than the lower bound for dimension d at https://cohn.mit.edu/kissing-numbers/ at verification time (and any newer arXiv claim). Floating-point configurations with tiny overlap loss do NOT qualify unless exactified.

## Partial wins

- **p1:** An exact kissing configuration in a dimension d >= 24 listed in Cohn's table, verified in exact arithmetic, with size strictly greater than the live table value for that d (several were moved in Sep 2026, so re-check).
- **p2:** A rigorous upper-bound improvement: an SDP/LP certificate verified in exact rational or interval arithmetic proving a kissing-number upper bound strictly below the live Cohn-table upper bound for some d in 9..23.

## How a win is checked

Use exact integer arithmetic. Scale the coordinates to integers, compute all Gram entries as Python ints, and assert the diagonal is constant and the off-diagonal entries are <= diag/2. For K ~ 600-12000, the Gram matrix is up to 1.4e8 entries, so use numpy int64 with overflow checks or chunked object arithmetic. Check that no two vectors coincide.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://cohn.mit.edu/kissing-numbers/>

## Sources

- <https://cohn.mit.edu/kissing-numbers/>
- <https://einsteinarena.com/problems/kissing-number-d11>
- <https://arxiv.org/abs/2609.35051>
- <https://arxiv.org/abs/2606.10402>
- <https://arxiv.org/abs/2606.18984>
- <https://arxiv.org/abs/2603.10425>
- <https://github.com/alexlegeartis/KissingNumbers>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start from the structure of the 604 d11 configuration (480 vectors from D11+ orbits plus extras) and apply analogous 'lattice orbit plus deep-hole insertion' in d13 and d14 from laminated lattices Lambda_13 and K_13.
- Use Ganzhinov's symmetric-search method: prescribe a large group (e.g. a subgroup of W(E8) x W(A_k)), so candidates are unions of orbits. Solve the max-clique of compatible orbits exactly.
- Project or slice the Leech lattice and Barnes-Wall configurations and look for antipodal-pair swaps that free room, certified exactly.
- Do continuous optimization with an energy term, then snap to a rational lattice (LLL on the scaled coordinates) to obtain an exact certificate.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A near-zero overlap loss is not a proof. Exact certification is mandatory.
- Cohn's table is the source of truth, and d11/d12 moved in 2026.
- Vectors must have equal norm exactly, not only up to rounding.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/kissing-number-low-dim.md
```

Already set up? Say `run V3R1T4S on kissing-number-low-dim`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `kissing-number-low-dim`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
