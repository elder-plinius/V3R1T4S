# Small two-color Ramsey numbers: new lower bounds via explicit graphs

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Exhibit a graph on N vertices with no K_s and no independent set of size t, proving R(s,t) >= N+1 and beating the current best lower bound for some (s,t), or the analogous multicolor result. Very active as of 2026-10-03. Latest: Yu (arXiv:2608.18169 v2, 24 Aug 2026) and Coniglio-Furini-Ljubic-San Segundo-Thuerauf-Traversi (arXiv:2608.18769, 19 Aug 2026). An arXiv API scan of Ramsey papers from Sep 2026 showed no further small-cell lower-bound papers; since then Fritz Cremer (arXiv:2610.12122, 8 Oct 2026) proved R(6,8) >= 135 and R(8,10) >= 345, improving the 134 and 343 of the April 2026 DS1 revision. AlphaEvolve (arXiv:2603.09172 v5) also moved R(4,16) 170->174, R(4,18) 205->209, R(4,19) 213->219 and R(4,20) 234->237 (since superseded by Yu's 252); exact circulant Ramsey numbers R_C(3,n) for n=13..20 were computed in arXiv:2608.18769, so plain circulant search there is exhausted.

## What counts as a win

Success means an adjacency matrix of a graph G on N vertices, symmetric with zero diagonal, such that omega(G) < s and alpha(G) < t are certified exactly by two independent methods (exhaustive B&B and an UNSAT proof). N+1 must be STRICTLY GREATER (direction: max) than the best lower bound for R(s,t) at verification time, taken as the maximum over Radziszowski's dynamic survey DS1 (latest revision) and every 2026 paper or repository found by a fresh search (at minimum arXiv:2603.09172 v5, ScaleAutoResearch-Ramsey, arXiv:2608.18169 v2, arXiv:2608.18769, arXiv:2610.12122). Off-by-one: a graph on N vertices proves R(s,t) >= N+1.

## Partial wins

- **p1:** A multicolour classical Ramsey record: an explicit edge colouring of K_N with no monochromatic forbidden clique in each colour (e.g. a 4-colouring of K_51 with no monochromatic triangle, giving R(3,3,3,3) >= 52), verified exhaustively, with N+1 strictly above the best lower bound in DS1 and any newer arXiv paper for that multicolour cell.
- **p2:** A new exact circulant Ramsey number: the exact value of R_C(4,k) (or R_C(5,k)) for some k with no published value, certified by an exhaustive search over all circulant connection sets that the skeptic re-runs, together with an explicit extremal circulant graph checked by two exact clique methods.

## How a win is checked

Run two independent exact clique solvers on G and on its complement. One is a custom bitset branch-and-bound (Tomita/MCS style) or networkx max_weight_clique. The other is a pysat/CaDiCaL encoding asking 'is there a K_s?', which must come back UNSAT, and likewise for independent sets of size t. Both must agree. Hash the matrix. Then do a literature check on arXiv for the past 6 months for that (s,t). For circulant graphs, also verify the expanded full graph, not only the connection set.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1>

## Sources

- <https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 (Radziszowski dynamic survey; not opened this session)>
- <https://arxiv.org/html/2603.09172v2>
- <https://github.com/ypwang61/ScaleAutoResearch-Ramsey>
- <https://arxiv.org/abs/2608.18769>
- <https://arxiv.org/abs/2608.18169>
- <https://arxiv.org/abs/2610.12122>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Use circulant and block-circulant graphs on primes or near-primes, with connection sets from cyclotomic classes (Yu's quintic classes mod 251). Sweep all small-index cyclotomic constructions for (4,k) and (5,k) cells.
- Use Exoo-style 'one-vertex extension'. Take the current record graph on N-1 vertices and search for a neighbourhood vector of a new vertex with SAT (clauses forbidding the K_{s-1} in the neighbourhood and the independent (t-1)-set in the non-neighbourhood). Iterate with small perturbations of the base graph.
- Use the IP over projected distance space from 2608.18769, extended to two-orbit (bi-circulant) graphs. It was only applied to plain circulants and mostly R(3,n).
- Use tabu search on edge flips with an objective counting K_s plus independent t-sets, sampled by fast clique enumeration, starting from Paley-type or cyclotomic seeds.
- Try multicolor and hypergraph cells (R(3,3,4), R(3,3,3,3) >= 51 -> 52 is a moonshot), where AI pipelines have not swept.
- Auditor: plain circulant search for R(3,13..20) cannot beat R_C(3,n); use non-circulant or block-circulant graphs there.
- After any R(4,k) construction, check both R(4,20) and R(4,21) (Yu's order-251 circulants moved both).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Stale baseline. Several cells changed in Mar-Aug 2026, and DS1 may lag, so always grep arXiv for the specific R(s,t).
- A heuristic clique search that misses a clique gives a false positive. Require an exact UNSAT proof or exhaustive B&B.
- Off-by-one: a graph on N vertices proves R(s,t) >= N+1, i.e. R > N.
- Confusing the circulant Ramsey number R_C(3,n) with R(3,n).
- R_C(3,n) for n=13..20 is now exactly known, so exhaustive circulant search there cannot beat the circulant optimum. Use non-circulant or block-circulant graphs.
- R(4,16..20) were all moved by AlphaEvolve in 2026, so do not assume DS1 values are current.
- Yu's order-251 graphs raise R(4,21) too. Check both cells after any R(4,k) construction.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/small-ramsey-lower-bounds.md
```

Already set up? Say `run V3R1T4S on small-ramsey-lower-bounds`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `small-ramsey-lower-bounds`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
