# Binary constant-weight codes A(n,d,w): new lower bounds in Brouwer's table

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

A(n,d,w) is the maximum number of binary words of length n and weight w with pairwise Hamming distance >= d. Brouwer's tables (d = 4..18, n up to 28 in the main tables and further for some) list best known lower and upper bounds. A code larger than the tabulated lower bound is a new record. Active as of 2026-10-20 (Brouwer's reference list cites emailed codes dated up to 2026-10-20). Lysenstoen (arXiv:2607.19550, Jul 2026; values polished further in Brouwer's table) and Echols (arXiv:2608.13906, Aug 2026, 124 improved cells via tabu search; Brouwer's reference list now says 'with 126 new codes'). Lower bounds are still being pushed. Brouwer's live cells already carry polished Lysenstoen values (e.g. A(23,6,10) >= 2992, A(23,6,11) >= 3588, A(24,6,10) >= 4237; the A(24,6,8) cell, polished to 1859 by Lysenstoen, now reads 1915 credited to Echols), larger than the arXiv abstract's numbers.

## What counts as a win

Success means an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER (direction: max) than the lower bound shown at verification time in the (n,d,w) cell of https://aeb.win.tue.nl/codes/Andw.html (also checking the mirror cell A(n,d,n-w)), and also strictly greater than any value for that cell in arXiv:2608.13906 (Echols, 124 improved cells), arXiv:2607.19550 (Lysenstoen) or any newer arXiv paper. M must not exceed the tabulated upper bound; exceeding it means a bug.

## Partial wins

- **p1:** A first explicit certificate: for a cell whose live lower bound has no surviving explicit code listing (a bare 1990-era citation), an explicit code of size equal to the tabulated lower bound, verified exactly. The skeptic confirms on the live page and in arXiv:2607.19550 / 2608.13906 that no explicit code for that cell is already published.
- **p2:** An improved upper bound: an exact rational dual certificate (Delsarte LP or Schrijver-type SDP, verified in rational arithmetic) proving A(n,d,w) <= U for U strictly below the live tabulated upper bound for some cell.

## How a win is checked

Use an independent script. Store the words as Python ints and assert popcount == w for each, all distinct, and popcount(x ^ y) >= d for all pairs: M^2/2 popcounts, vectorized in numpy (uint64) or with bitset blocks. Re-fetch aeb.win.tue.nl/codes/Andw.html at check time and read the cell. Also check the equivalent cell under complement symmetry, A(n,d,w) = A(n,d,n-w). Claim only if the strict improvement holds.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://aeb.win.tue.nl/codes/Andw.html>

## Sources

- <https://aeb.win.tue.nl/codes/Andw.html>
- <https://arxiv.org/abs/2607.19550>
- <https://arxiv.org/abs/2608.13906>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Build codes from group orbits. Choose a group G acting on coordinates (cyclic of order n or n-1, PSL(2,q) on q+1 points, affine groups) and take the code as a union of G-orbits of weight-w words. Find a maximum compatible orbit set by max-weight clique search on the orbit graph (networkx or a custom bitset B&B). Few orbits make exact search feasible.
- Use Lysenstoen's split-coordinate decomposition. Fix half of the coordinates to a known good code and optimize the complementary half with CP-SAT.
- Look for cells where the lower bound is a bare citation to 1990 Brouwer-Shearer-Sloane-Smith with no surviving code listing, and reconstruct then beat them.
- Use partitioning constructions: (u|u+v)-style, or partition-and-combine from codes with weights w1 + w2 = w on split coordinates. Sweep all splits automatically.
- Run large-scale local search (e.g. 1-opt add/remove with tabu) on the conflict graph restricted to a random G-invariant subspace.
- Auditor note: Echols' seeded bit-swap tabu search just swept 124 cells, so prefer group-orbit / structured constructions over plain local search, and target cells that paper did not improve.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Brouwer's table uses even d. Odd d reduces to d+1, so check the convention.
- Equivalent cells: A(n,d,w) = A(n,d,n-w), so make sure the improved cell is not already beaten in its mirror.
- The table moved from win.tue.nl/~aeb to aeb.win.tue.nl, so read the live page.
- arXiv abstracts can lag Brouwer's table (polished values are larger), so always read the live cell.
- Echols' 124 improvements may not all be reflected in the table yet, so check arXiv:2608.13906's tables too.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/constant-weight-codes.md
```

Already set up? Say `run V3R1T4S on constant-weight-codes`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `constant-weight-codes`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
