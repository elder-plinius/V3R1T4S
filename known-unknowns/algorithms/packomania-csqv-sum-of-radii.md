# Packomania csqv: circles in the unit square with maximised sum of radii (AlphaEvolve problem), beat a table entry

⚡ **Algorithms** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

Place N circles of variable radii inside the unit square, non-overlapping, maximising the sum of radii: AlphaEvolve's 'packing circles to maximise sum of radii' problem (N=26, 32). Packomania (E. Specht) revived the csqv table on 23 Jul 2026; it is the primary record table, covering N=1..500 except N = 493 (no row on csqv.html or in txt/sumradii.txt, and csqv493.txt returns 404, 2026-10-18) plus 84 larger N up to 10000, last update 30-Sep-2026 (per the page), with coordinates at csqv/txt/csqv<N>.txt and a one-column digest csqv/txt/sumradii.txt. Records now come from LLM-evolved optimisers (OpenEvolve/ShinkaEvolve, Haowei Lin, Jason Liang's circle-packing-sota, Wes Sander's MoltFire, Jean-Rene Denoual's 200+ entries in Sep 2026, arXiv:2609.05093 'Breaking 10 Packomania records for $28'). Live values 2026-10-08: N=26: 2.635983084919, N=27: 2.685978684198, N=30: 2.842668747462, N=32: 2.939572771205, N=46: 3.539571078547, N=48: 3.616465058812. CRITICAL FREEZE: packomania.com/pending-requests.html states that all csqv submissions in October 2026 are saved but not processed until November 2026, and lists Jason Liang's 05-Oct-2026 submission of 472 candidates for N=63..10000; his public repo (jasonzliang/circle-packing-sota, commits 2026-10-04/05) claims 462 wins above N=100 versus the 2026-10-05 table and publishes the coordinates. So for N>62 the live table is NOT the frontier; the public repos are the admissible secondary record sources and must be beaten too.

## What counts as a win

Success means an explicit list of N circles (x_i, y_i, r_i) with N <= 200, such that (1) every circle lies inside [0,1]^2 and every pair is interior-disjoint, certified rigorously (exact rational arithmetic on the saved decimal coordinates, or interval arithmetic with a positive margin after shrinking radii by the rounding error), and (2) the sum of radii computed from the certified (possibly shrunken) radii is STRICTLY GREATER (direction: max), by at least 1e-11, than the 'sum of radii' value for that N in https://www.packomania.com/csqv/csqv.html re-fetched live immediately before claiming, AND strictly greater by at least 1e-11 than the best value for that N in the live public repositories https://github.com/jasonzliang/circle-packing-sota (every sota/*/comparison.md and every .pck for that N, re-fetched live and re-certified with the same exact checker) and https://github.com/RasimAbiyev/circle-packing-explorations, AND for N=26 also strictly greater than the live EinsteinArena leaderboard best. Ties, improvements below the table's 12-decimal precision, and improvements over the frozen table that do not also beat the public repositories are not wins. The claim is for the verified construction; emailing Packomania needs explicit permission from the human.

## Partial wins

- **p1:** A certified improvement for some N <= 50 (the heavily mined range where AlphaEvolve, Yiping Wang, Pokutta, Specht, Liang, Heap and Garg all compete), strictly above the live table value AND above every value for that N in the live jasonzliang / RasimAbiyev repositories by >= 1e-11, with the same exact-rational feasibility certificate.
- **p2:** A certified improvement for N = 26 or N = 32 (the two AlphaEvolve benchmark instances), strictly above the live Packomania value, above the live jasonzliang/RasimAbiyev values, and above the best value on the live EinsteinArena circle-packing leaderboard (https://einsteinarena.com/problems/circle-packing, currently 2.6359830849176076 for N=26), evaluated with the exact feasibility check (no 1e-6 or 1e-9 slack).
- **p3:** Certified improvements for three or more distinct N in 51..200 in one shift, each strictly above the live table value AND above every live jasonzliang/RasimAbiyev value for that N by >= 1e-11 (beating only the frozen table is explicitly NOT a win for N > 62: jasonzliang's public .pck files already beat it for most N > 100), with the solver code and seeds saved so the skeptic can re-run one of them.

## How a win is checked

Independent checker in pure Python with fractions.Fraction: read the saved coordinates as decimal strings, convert to exact rationals, check 0 <= x_i - r_i, x_i + r_i <= 1 (same for y), and (x_i-x_j)^2 + (y_i-y_j)^2 >= (r_i+r_j)^2 for all pairs, as exact inequalities (touching allowed). If the submitted radii violate by a tiny epsilon, the attacker must supply shrunken radii that pass exactly; the score is the exact sum of the passing radii. Compare with the live table value for that N parsed from csqv.html / sumradii.txt (12 decimals) and with csqv<N>.txt's radii summed exactly; then fetch every jasonzliang .pck / comparison.md value and RasimAbiyev table value for that N and apply the same exact checker to their coordinates (their verify_and_compare.py uses float64 with 1e-9 tolerance and is only a second opinion; solver-sm-radical-v6-n27/exact_check.py in that repo is their exact variant). Minutes on this Mac for N <= 200.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.packomania.com/csqv/csqv.html>

## Sources

- <https://www.packomania.com/csqv/csqv.html>
- <https://www.packomania.com/csqv/txt/csqv26.txt>
- <https://www.packomania.com/csqv/txt/csqv30.txt>
- <https://github.com/jasonzliang/circle-packing-sota>
- <https://github.com/RasimAbiyev/circle-packing-explorations>
- <https://arxiv.org/abs/2609.05093>
- <https://arxiv.org/abs/2509.19349>
- <https://einsteinarena.com/>
- <https://google-deepmind.github.io/alphaevolve_repository_of_problems/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start from the published csqv<N>.txt configuration, perturb (swap two circles, move one circle to a gap, change the contact graph) and re-solve the KKT system by sequential linear programming / SLSQP on (x, y, r) with the overlap constraints active; repeat with thousands of restarts across 10 cores.
- Contact-graph enumeration: the table lists 'contacts' per N; generate alternative rigid contact graphs near the record's and solve each graph's polynomial system exactly (Newton with exact refinement), which also yields exact certificates.
- Transfer structures between N: take the record for N+1 and delete the circle with the smallest 'marginal loss', or add a circle to the record for N-1 in the largest hole, then polish; the Sep 2026 'old favorites in new guises' entries came from exactly this.
- Evolutionary program search over the initialiser (OpenEvolve-style) is what broke 10 records for N=101-114 (arXiv:2609.05093); replicate with a cheap local LLM-free mutation operator library and the same penalty-method polisher.
- Exploit symmetry classes (D1, D2, D4 rows in the table): search symmetric ansatz families for N where the record has no symmetry and vice versa.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Float-tolerance 'records': OpenEvolve's 1e-6 slack produces infeasible packings whose sum exceeds the record; only an exact-rational or interval certificate counts, and shrinking radii to fix overlaps usually erases a sub-1e-6 'gain'.
- Comparing with the wrong objective: csq (equal circles, minimise container) and csqv (variable radii, maximise sum) are different pages; AlphaEvolve's 'sum of radii' uses the unit square, not the unit-diameter square.
- Reading the table wrong: it prints 12 decimals; improvements must exceed rounding (>= 1e-11) and be computed from the certified radii, not the solver's float output.
- Submitting to Packomania is by email; do not send anything without the human's explicit permission.
- The live table is frozen for October 2026 (pending-requests.html) with 472 queued candidates from Jason Liang for N=63..10000 and 462 public wins above N=100 in his repo: for N > 62 the frozen table is far below the public frontier, so beating the table alone is meaningless; always beat the public repos too.
- jasonzliang's repository is updated daily by automation; re-fetch at verification time and check every sota/* subdirectory for the N in question.
- Small circles can always be added, so the bar for N is the best sum at any N' <= N; at margin 1e-11 txt/sumradii.txt has no row below such a bar (checked 2026-10-20 with kit/propagated_bar.py --direction up, PR #573).

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/algorithms/packomania-csqv-sum-of-radii.md
```

Already set up? Say `run V3R1T4S on packomania-csqv-sum-of-radii`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `packomania-csqv-sum-of-radii`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
