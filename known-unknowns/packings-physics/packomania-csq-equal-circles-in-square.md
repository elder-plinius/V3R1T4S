# Packomania: equal circles in a square (csq), beat a per-N record radius

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Packomania's 'circles in a square' table (csq) lists the best known radius r(N) of N equal circles in the unit square for N = 1..1000 except 49 N in 786..1000 (no row on csq.html or in txt/radius.txt, 2026-10-18) and selected N up to 10000 (3147 rows, 12-decimal radius.txt, per-N coordinates at csq/txt/csq<N>.txt). Proven optimal only for N <= 30 and a few special N (36 etc.). Last update 10-Sep-2026 (two candidates N = 3000 and 9996 by ZeroThesis); the big 2022 wave by Lai-Hao-Xiao-Glover improved ~250 values of N in 106..400. IMPORTANT: the pending-requests page (17-Oct-2026) lists 557 csq candidates in 401..1000 and 250 in 1015..9996 (Zeeshan Tariq, Sept 2026) and 1813 in 501..9984 (Vidit Patankar, 15-Oct-2026), none processed yet, so the live table for N > 400 is probably about to move.

## What counts as a win

Success means N centers for one N listed in https://packomania.com/csq/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1/2 - max_i max(|x_i|,|y_i|) ) for the centered unit square [-1/2,1/2]^2, computed in mpmath at 50 digits with no tolerance, is STRICTLY GREATER (direction: max) than the live 12-decimal txt/radius.txt value for that N re-fetched immediately before claiming, by at least 1e-10, AND the configuration is not isometric to the posted csq<N>.txt one (sorted distance multisets differ), AND N is outside every csq range on the live pending-requests page (on 2026-10-20: 401..1000, 501..9984 and 1015..9996 are queued, so only N <= 400 and any listed N above 9996 can be claimed until the queue is processed; queued N is partial win p1). QUEUE RULE (Packomania, checked 2026-10-20): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. Packomania coordinate files are CENTERED (container centre at the origin: circle/sphere radius 1, square side 1 in [-1/2,1/2]^2, cube edge 1 in [-1/2,1/2]^3). No submission (email) is ever made; the claim is for the verified construction only.

## Partial wins

- **p1:** A certified improvement (same mpmath rule, margin 1e-10) for an N inside a csq pending-queue range: real but not novelty-safe; record the value and re-check against the live table when Packomania processes the queue.
- **p2:** A certified improvement to a sibling 2D equal-circle Packomania table that exists live (csc semicircle, crt triangle, ccq circles-in-circle-quarter) for an N OUTSIDE every pending-queue range for that category (on 2026-10-08 csc 41..250, crt 54..299, ccq 57..600 are queued), same mpmath rule against that table's live txt/radius.txt with margin 1e-10 for 12-decimal files and 1e-11 for 30-decimal files.
- **p3:** A second distinct optimal configuration for a proven-optimal N (N <= 30), i.e. equal r* to 1e-11 but non-isometric to the posted coordinates, verified by contact-graph non-isomorphism.

## How a win is checked

Checker (< 2 minutes): curl https://packomania.com/csq/txt/radius.txt live (tab-separated N, r), parse row N; load claimed centers; mpmath mp.dps=50; r* = min(half the minimum pairwise distance, 1/2 - max_i max(|x_i|,|y_i|)); assert r* - r_table >= 1e-10. Download csq/txt/csq<N>.txt, recompute its r (parser sanity) and compare sorted distance multisets. Re-fetch csq<N>.html, the csq.html History of updates and pending-requests.html; apply the queue rule. Report r* to 20 digits.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://packomania.com/csq/csq.html>

## Sources

- <https://packomania.com/csq/csq.html>
- <https://packomania.com/csq/txt/radius.txt>
- <https://packomania.com/csq/txt/records.txt>
- <https://packomania.com/csq/txt/author.txt>
- <https://packomania.com/csq/txt/csq100.txt>
- <https://packomania.com/csq/txt/csq_coords.tar.gz>
- <https://packomania.com/pending-requests.html>
- <https://arxiv.org/abs/2609.05093>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Work in 106..400 where the 2022 Lai-Hao wave set most rows: their algorithm was a single method; try a different family (event-driven Lubachevsky-Stillinger compression from random starts, then KKT polishing) and look for N where the table's contact count is low relative to 2N+1.
- Exploit density dips: txt/records.txt lists the density-record N (e.g. 188, 194, ...); the N just after a density-record often sits in a bad basin (e.g. a record packing minus circles, with freed rattlers). Attack N = record+1..record+3 with rattler-driven re-packing.
- Shifted-lattice families: for N near k^2 or k(k+1) try square/hexagonal hybrids with one or two skew rows, then optimize the skew angle continuously.
- Use the per-N coordinate files as seeds and run large-neighbourhood search: remove 5-10% of circles, re-insert at the largest empty circles (Voronoi vertices), re-jam, accept if r improves.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Queue-stale table: 2620 csq candidates are pending (N > 400): the 807 listed on 2026-10-08 and 1813 more on the 17-Oct-2026 list. A 'record' for N in those ranges may already be in Specht's inbox; the criterion forces N <= 400 or an explicit queue check.
- 12-decimal table: an apparent improvement in the 12th decimal can be the table's own rounding (Packomania truncates to 12 decimals on csq); require the 1e-11 margin against the exact posted value and prefer re-deriving the table radius from the posted coordinates (csq<N>.txt) in mpmath.
- Coordinate convention: Packomania files are centered at the origin with side length 1 (coordinates in [-0.5, 0.5]); do not test containment against [0, 1] without shifting.
- Submission is by email and asked to pause in October 2026; do not count a submission as a claim.
- The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle matches their public release v2.2 (github.com/Hashirama1337s/moki-julio-circle-packing, commit 855d8f6838e9, 2026-09-25T22:41Z, '4,666 records in 15 tables'). Its csq shelf has 2,345 records at N from 385 to 9996, and the only one at N <= 400 is N = 385, so for a claim at N <= 400 the bundle can matter only at N = 385 (the N list is in RESULTS_TABLE.md at that commit; the count and the timing agree, but the queued zip is not public; checked 2026-10-19).
- Free cells (2026-10-20): 1813 rows, N in 501..9984, lie below the row of a larger N by at least 1e-10 (largest 8.35e-4, N = 992 below 1003); deleting circles from the posted N' file reaches them with no search (N = 992 from csq1003.txt: r* = 0.0167080057180 against the row 0.015873015873). They match, in count and range, the 15-Oct-2026 Vidit Patankar entry on pending-requests.html (1813 csq candidates, 501..9984), so they are covered by the queue rule, not open. The sibling tables csc, crt and ccq (partial win p2) have no free cell. Compare a claim with B(N) = max over listed N' >= N (kit/propagated_bar.py, PR #573).

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/packomania-csq-equal-circles-in-square.md
```

Already set up? Say `run V3R1T4S on packomania-csq-equal-circles-in-square`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `packomania-csq-equal-circles-in-square`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
