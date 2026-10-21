# Sorting networks: fewer comparators than the best known for n = 16..32

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

S(n) is the minimum number of comparators in a network that sorts every input on n channels. Optimality is proven only for n <= 12 (size) and for n <= 17 (depth). For n=16, the best known size is 60, which has stood since Green in 1969. For n=17..32, the best known sizes from Dobbelaere's SorterHunter table are: 17: 71, 18: 77, 19: 85, 20: 91, 21: 99, 22: 106, 23: 114, 24: 120, 25: 130, 26: 138, 27: 147, 28: 155, 29: 164, 30: 172, 31: 180, 32: 185. Best known depths: n = 13-16: 9 (optimal), 17: 10 (optimal), 18-20: 11, 21-24: 12, 25-28: 13 (27 and 28 lowered from 14 to 13 by Chengu Wang, arXiv:2511.04107), 29-32: 14. The table also records Pareto (size, depth) pairs. Any network with fewer comparators than listed for some n, with smaller depth than the best listed depth, or with a (size, depth) pair not dominated by a listed pair, is a record. OPEN as of 2026-10-20. Dobbelaere's extended page was last updated 13 Oct 2026: on 2026-10-10 a redundant comparator was removed from the 27-input 13-layer network (now the Pareto pair (152, 13); merged networks for 53-55 also changed), and on 2026-10-13 Justin Lyson removed one comparator each from the N38D16, N43D17, N45D18, N46D18 and N53D20 networks. Best sizes for n = 16..32 and best depths are unchanged. The previous update (7 Nov 2025) added Chengu Wang's depth-13 networks for 27 and 28 channels (arXiv:2511.04107). An arXiv API scan found no 2026 size records. EinsteinArena lists 'Sorting Network (16 inputs): under 60 comparators' as a new problem with no score yet. Dobbelaere's extended page covers n = 2..64 with (size, depth) pairs.

## What counts as a win

Success means a list of comparators (i,j), 0 <= i < j < n, standard min-to-i form, with 13 <= n <= 32, that sorts all 2^n binary inputs (0-1 principle), checked exhaustively, and that is STRICTLY BETTER (direction: min for both size and depth) than the live Dobbelaere table at https://bertdobbelaere.github.io/sorting_networks_extended.html at verification time in at least one of these ways: (a) its comparator count is strictly smaller than the table's smallest size for that n; (b) its depth (greedy layering) is strictly smaller than the table's best depth for that n, at any size; or (c) its (size, depth) pair is not dominated by any pair listed for that n, i.e. no listed (s', d') has s' <= size and d' <= depth. For n=16 it must also beat the live EinsteinArena leaderboard, and it must beat any newer arXiv/GitHub claim (context on 2026-10-03: n=16 size 60, n=32 size 185; best depths 9 for n=13-16, 10 for 17, 13 for 25-28, 14 for 29-32). A network below a proven lower bound listed on the page for 13 <= n <= 32 (the min size or min depth bound columns, e.g. depth below 9 for n=13-16 or below 10 for n=17) means a bug, not a record. n <= 12 sizes are proven optimal; a smaller network there means a bug.

## Partial wins

- **p1:** A Pareto (size, depth) improvement for some n in 33..64 on Dobbelaere's extended table at verification time, verified exhaustively by the 0-1 principle (bit-sliced over 2^n inputs, or by an exact prefix/output-set method the skeptic re-runs).
- **p2:** A new optimal-size proof: a SAT-based proof, with a DRAT certificate checked by drat-trim, that no sorting network on n channels (13 <= n <= 16) has fewer comparators than a given bound strictly above the best published lower bound for that n.

## How a win is checked

Use an independent C or numpy bit-sliced simulator. Represent the 2^n inputs as n bit-vectors across 64-bit words. Each comparator (i,j) does a_i, a_j = a_i & a_j, a_i | a_j. At the end, check that each channel row is monotone (sorted output means every input word maps to a pattern 0..01..1, i.e. a_k <= a_{k+1} bitwise). For n=32 that is 2^32 inputs times about 185 comparators over 64-bit words, which takes minutes in C. Compute depth by greedy ASAP layering. Calibrate on a Dobbelaere network for the same n.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://bertdobbelaere.github.io/sorting_networks_extended.html>

## Sources

- <https://bertdobbelaere.github.io/sorting_networks_extended.html>
- <https://bertdobbelaere.github.io/sorting_networks.html>
- <https://einsteinarena.com/>
- <https://github.com/bertdobbelaere/SorterHunter>
- <https://arxiv.org/abs/2511.04107>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Run SorterHunter-style evolutionary search with a prescribed prefix (e.g. a Green-type filter or reflection-symmetric first layers) and stochastic suffix completion. Target n=21..30 where the table cites only SorterHunter.
- Do symmetric (reflection-invariant) network search, which halves the variables. Many records are symmetric.
- Use SAT for the last layers: fix the first k layers from a good prefix, compute the set of reachable unsorted outputs (much smaller than 2^n), and ask a SAT solver for the minimum completion (Bundala-Ehlers/Codish technique).
- For n=16 below 60 (moonshot), use prefix-optimization with exact SAT completion over the outputs remaining after a 4-layer Green filter.
- Get depth records via Wang's 2025 technique, extended to n=29..32 or n=33..40.
- SorterHunter-style evolution (prefix plus greedy completion), seeded with the newest Wang25 depth-13 networks, while targeting a size reduction at fixed depth.
- Symmetric (reflection-invariant) networks: Wang's depth-13 networks were reflection-symmetric. Enforce symmetry to halve the search, and combine high-quality 16- and 12-channel prefixes as in 2511.04107.
- SAT-based suffix optimization: fix the first d layers, compute the set of unsorted outputs that remain, and solve the minimal-size suffix exactly with CaDiCaL plus subsumption-based pruning (the Codish-style 'prefix + SAT' approach).
- Target n values where the size-depth Pareto front has visible gaps relative to neighbouring n (interpolate from n-1 and n+1 records).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Testing only random permutations is not a proof. Use the exhaustive 0-1 principle.
- Comparator orientation: reversed comparators (i > j) are non-standard networks and are not accepted.
- n <= 12 sizes are proven optimal, so beating them means a bug.
- The Dobbelaere page has not been updated since Nov 2025, so also grep arXiv/GitHub and the EinsteinArena leaderboard for newer claims.
- Testing random inputs instead of all 2^n binary vectors. Only the exhaustive 0-1 check is a proof.
- Miscounting depth when comparators in one layer share a channel.
- Comparing against an old copy of the page. Re-fetch it at verification time.
- Comparators with i>j (reverse comparators) make the network non-standard. Normalize or reject them.
- Depth is proven optimal for n <= 17 (9 for 13-16, 10 for 17), and the page lists size and depth lower bounds for every n. A result below a listed lower bound is a checker bug, not a record.
- A (size, depth) pair that ties a listed pair, or is dominated by one, is not a record. Check every listed pair for that n, not only the smallest-size one.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/sorting-network-size-records.md
```

Already set up? Say `run V3R1T4S on sorting-network-size-records`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `sorting-network-size-records`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
