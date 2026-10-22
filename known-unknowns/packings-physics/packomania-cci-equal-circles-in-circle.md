# Packomania: equal circles in a circle (cci), beat a per-N record radius

⚪ **Packings and physics** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Packomania's 'circles in a circle' table (cci) lists the best known radius r(N) of N equal circles packed in the unit circle for every N = 1..2600 plus selected larger N up to 5000 (2735 rows). Only N <= 13 and N = 19 are proven; on 11-Oct-2026 the cci history records two computer-assisted proofs announced for N = 15 (Zii Fave). Everything else is a putative record. Last table update 25-Dec-2024 (Basurto/Gurin/Odriozola/Specht); earlier waves by Lai-Hao et al. (2023-2024) and Zhou-He-Zheng-Li (2023). Packomania's pending-requests list (17-Oct-2026) now holds a cci submission (Vidit Patankar, 15-Oct-2026, 193 candidates in the range 652-3943), so for N in 652..3943 the live table may not be the frontier and those N are excluded by the QUEUE RULE; outside that range the live table is the frontier. Per-N values are machine-readable (txt/radius.txt, 30 decimals except 356 rows in N = 128..1000 that carry 12) and per-N coordinates are at cci/txt/cci<N>.txt (30 decimals in cci100.txt, but 12 in cci128.txt, one of the 12-decimal rows).

## What counts as a win

Success means a file of N centers (x_i, y_i) for one N listed in https://packomania.com/cci/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ), computed in mpmath at 50 digits directly from the submitted coordinates (no tolerance), is STRICTLY GREATER (direction: max) than the 30-decimal radius for that N re-fetched live immediately before claiming, by at least 1e-11, AND the configuration is not isometric to the posted cci<N>.txt one (sorted distance multisets differ), AND N does not appear in a History-of-updates line on the live cci.html newer than the one the scout fetched. QUEUE RULE (Packomania, checked 2026-10-20; cci N = 652..3943 queued since 15-Oct-2026): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. Packomania coordinate files are CENTERED (container centre at the origin: circle/sphere radius 1, square side 1 in [-1/2,1/2]^2, cube edge 1 in [-1/2,1/2]^3). No submission (email) is ever made; the claim is for the verified construction only.

## Partial wins

- **p1:** A configuration for some N in 1..2600 whose feasible radius r* equals the live table value to within 1e-11 but is certified non-isometric to the posted cci<N>.txt (different sorted distance multiset AND different contact graph, mpmath at 50 digits): a second optimum; not a record.
- **p2:** A certified improvement for one of the gap values N > 2600 that the table lists (e.g. N = 4495, 5000), where the record is a lattice-like seed by Specht rather than an optimized packing.
- **p3:** A certified improvement in the sibling regular-hexagon table chx (N <= 1261, 12-decimal https://packomania.com/chx/txt/radius.txt, so margin 1e-10) using the same mpmath feasible-radius rule, for an N not covered by any chx entry on the live pending-requests page (on 2026-10-08 chx N = 55 and 89 are queued).

## How a win is checked

Independent checker (< 2 minutes): (1) curl the live https://packomania.com/cci/txt/radius.txt and parse row N. (2) Load the claimed centers; mpmath mp.dps=50; r* = min(min pair distance / 2, 1 - max |c_i|). (3) Assert r* - r_table >= 1e-11. (4) Download cci/txt/cci<N>.txt, recompute its r (must reproduce the table to 1e-20; parser sanity) and compare sorted distance multisets. (5) Re-fetch cci<N>.html, the cci.html History of updates and pending-requests.html; apply the queue rule. (6) Compare the contact graph against txt/contacts.txt.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://packomania.com/cci/cci.html>

## Sources

- <https://packomania.com/cci/cci.html>
- <https://packomania.com/cci/txt/radius.txt>
- <https://packomania.com/cci/txt/author.txt>
- <https://packomania.com/cci/txt/cci100.txt>
- <https://packomania.com/cci/txt/cci_coords.tar.gz>
- <https://packomania.com/pending-requests.html>
- <https://packomania.com/hints.html>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Target N in 1000..2600: 2121 of 2735 rows are Specht's own (txt/author.txt), and the 2023-2024 Lai-Hao / Zhou-He / Basurto waves stopped near N = 1000, so the large-N rows have had far less competition. Use the N=1000..2600 coordinates as seeds and run perturb-and-repack (remove k circles, re-insert at largest holes, then re-jam).
- Hexagonal-core templates: take the chx (hexagon) hex-number packings, cut a circular window and relax the boundary layer; Cantrell's bound rows ('now meet Cantrell's bound') show where the frontier is already tight, so skip those N.
- Monotonic basin-hopping on a smooth penalty (sum of squared overlaps + squared protrusion) with L-BFGS, then an exact jamming step: solve the KKT system of the active contact set with mpmath to polish r to 30+ digits before comparing.
- Rattler exploitation: rows with many 'loose' circles (txt/loose.txt) have slack; move rattlers to open up a boundary contact and re-inflate.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Direction and normalization: cci fixes the container radius at 1 and maximizes r; some literature reports the container radius for unit circles (ratio = 1/r). Compare r to r, never ratio to r.
- Double-precision 'records' of +1e-13 are noise. The 1e-11 margin on the mpmath feasible radius is mandatory; a configuration with tiny overlaps that 'rounds' to a record is a false positive.
- Stale-table trap: Packomania has a queue of over 5,000 pending candidates (2026-10-08). cci was not in the queue on 2026-10-08, but the 17-Oct-2026 list has 193 cci candidates in 652..3943; re-check pending-requests.html and the per-N page immediately before claiming.
- Known-literature trap: an improvement may already be published (Lai-Hao 2024, Basurto 2024) but not yet uploaded; search arXiv for the N before claiming.
- Submitting to Packomania is by email (an outbound message on the human's behalf) and is asked not to happen in October 2026; claim the verified construction, not a submission.
- The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle matches their public release v2.2 (github.com/Hashirama1337s/moki-julio-circle-packing, commit 855d8f6838e9, 2026-09-25T22:41Z, '4,666 records in 15 tables': crt, ccq, cpd, cpt, crc_100 to crc_800, csc, csq, cxd). Neither v2.2 nor the current release (commit fd6316dd, 2026-10-18, 21 tables) has a cci table, and the regular hexagon (chx, partial win p3) enters only at v2.6 (commit 94083ac11d, 2026-09-26T23:42Z). So if the queued zip is v2.2 (the count and the timing agree; the zip itself is not public), it holds no cci or chx candidate (checked 2026-10-19).
- Free cells (2026-10-20): 193 rows, N in 652..3943, lie below the row of a larger N by at least 1e-11 (largest 5.81e-5, N = 1260 below 1261, reached from cci1261.txt with no search); they match, in count and range, the 15-Oct-2026 Vidit Patankar entry on pending-requests.html (193 cci candidates, 652..3943). In chx (partial win p3) one row is free and not queued: N = 266 lies 6.85e-7 below N = 267. Compare a claim with B(N) = max over listed N' >= N (kit/propagated_bar.py, PR #573).

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/packings-physics/packomania-cci-equal-circles-in-circle.md
```

Already set up? Say `run V3R1T4S on packomania-cci-equal-circles-in-circle`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `packomania-cci-equal-circles-in-circle`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
