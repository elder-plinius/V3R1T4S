# CVRPLIB VRPTW (Gehring-Homberger, DIMACS truncated-distance objective): beat an open best-known solution

🚚 **Optimization benchmarks** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

CVRPLIB re-hosts the 300 Gehring-Homberger VRPTW instances (200-1000 customers) since May 2026 under the DIMACS-2022 convention: single objective = total travel distance with each edge length truncated to one decimal (floor(10*d)/10), and travel times equal to those truncated distances; no vehicle-minimization hierarchy. Live on 2026-10-08: 193 of the 300 instances are Opt = no (all 200-customer instances are Opt = yes; most 400-1000 ones are open). The Updates page shows 23 new BKSs between Sept 26 and Sept 28 2026, all from one practitioner (Tobias Linke), on C1_10_*, R1_10_*, RC1_*, R1_6_2, RC1_4_9, RC2_10_8, including a 0.2 improvement on RC1_8_1 one day after his own previous value, so the table still has slack. No Gehring-Homberger update is listed after Sept 28 (checked 2026-10-18); on Oct 1 CVRPLIB announced a VRPTW Best Known Solution Challenge on a new XLTW set (1,000 to 10,000 customers; instances released when the competition starts). Find a feasible solution with truncated-distance total strictly below the listed UB for any Homberger instance with Opt = no.

## What counts as a win

A solution file in CVRPLIB format ('Route #k: c1 c2 ...' with customer ids exactly as in the Solomon-format instance file, depot = 0) for one Gehring-Homberger instance (names C1_/C2_/R1_/R2_/RC1_/RC2_ with _2_, _4_, _6_, _8_ or _10_ middle part) whose Opt column reads 'no' in the All Instances table at https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances, such that a standalone checker written from the Solomon format definition that (a) reads the instance (VEHICLE NUMBER and CAPACITY, then one line per customer: id x y demand ready due service), (b) computes per-edge distance d = floor(10 * euclid + 1e-9) / 10 (DIMACS truncation) and uses the same truncated value as travel time, (c) verifies each customer served exactly once, every route load <= CAPACITY, number of routes <= VEHICLE NUMBER, and time windows respected with arrival = max(departure_prev + d, ready) <= due at every customer and return to the depot by the depot's due time, service time added after arrival, and (d) sums the truncated edge lengths over every route including the depot legs, reports a total (to one decimal) strictly less than the UB for that instance in the All Instances table and consistent with the Updates log at https://galgos.inf.puc-rio.br/cvrplib/index.php/en/updates, both re-fetched live immediately before claiming. Before any claim the checker must accept the posted BKS files of C1_10_10 (instance id 685), RC1_8_1 (id 656) and R1_10_3 (id 698) as feasible and reproduce 39815.6, 29946.1 and 44673.3 exactly (verified by the vetter 2026-10-08; with double-precision travel times the posted RC1_8_1 and R1_10_3 files violate a time window by < 0.1, so truncated travel times are the only convention under which the table is self-consistent). The solution file, checker and table snapshot are saved together. Nothing is submitted to CVRPLIB; the write-up goes to the human.

## Partial wins

- **sintef-hierarchical-improve:** Improve the SINTEF hierarchical BKS (strictly fewer vehicles, or equal vehicles and strictly smaller double-precision distance by at least 0.01 after 2-decimal rounding) for any Gehring-Homberger 600/800/1000 instance listed at https://www.sintef.no/projectweb/top/vrptw/homberger-benchmark/<600|800|1000>-customers/ (rows: instance, vehicles, distance, reference, date; solution files linked per row), checked by the same route checker in hierarchical mode (double-precision distances and travel times) after reproducing the posted SINTEF solution file's vehicle count and distance (e.g. c1_10_2 -> 90 / 42222.96). SINTEF's table is re-fetched live at claim time. Separate objective from the headline; never mix the two.
- **open-tie-new-structure:** A solution for an open Homberger instance whose truncated-distance total equals the live CVRPLIB UB exactly but whose undirected edge set differs from the posted BKS file in at least 10% of edges (edge-set comparison by the same checker); independently checkable from the two files.
- **c2-r2-rc2-long-horizon-improve:** Strict CVRPLIB UB improvement (headline checker and re-fetch rule) on any C2_/R2_/RC2_ instance with Opt = no; recorded separately because, apart from RC2_10_8, the long-horizon classes were not touched in the Sept 2026 wave, so slack there is independent evidence.

## How a win is checked

Instance and BKS files via https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/<id> and .../download/bks/<id> (ids in the table HTML; 685 = C1_10_10, 656 = RC1_8_1, 698 = R1_10_3). The checker must first reproduce the posted BKS values and accept them as feasible under truncated distances and truncated travel times (C1_10_10: truncation 39,815.6; nearest-integer gives 39,775.0 and exact gives 39,851.34, so the convention is unambiguous). Then check the claimed solution. Minutes. Re-fetch the All Instances table with plain curl -L and parse the instance's <tr> (UB cell '$39{,}815.60$', Opt cell).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances>

## Sources

- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/updates>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/685>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/bks/685>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/656>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/bks/656>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/698>
- <https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/bks/698>
- <https://www.sintef.no/projectweb/top/vrptw/homberger-benchmark/1000-customers/>
- <https://www.sintef.no/projectweb/top/vrptw/homberger-benchmark/800-customers/>
- <https://www.sintef.no/globalassets/project/top/vrptw/homberger/1000/homberger_1000_customer_instances.zip>
- <https://www.sintef.no/contentassets/51a833740c45438b99b2935fd1c057d1/c1_10_2-90-42222.96.txt>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Run PyVRP / HGS-VRPTW (open source, built for the DIMACS truncated objective) and other open VRPTW HGS/ALNS codes with long time limits and many seeds, seeded from the posted BKS; most CVRPLIB VRPTW values are converted SINTEF hierarchical solutions, which were never optimised for distance-only, so distance-only search from them has real slack.
- Target instances whose BKS moved most recently by a single practitioner (RC1_8_1 moved twice in two days), and instances whose CVRPLIB UB equals a converted SINTEF hierarchical solution with a high vehicle count (distance-only can use more vehicles up to VEHICLE NUMBER).
- Exploit the truncation: moves whose exact delta is slightly positive but truncated delta is negative are improvements under this objective.
- Exact polishing of 2-4 neighbouring routes with a CP-SAT / set-partitioning model using truncated distances.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Two tables, two objectives: SINTEF (hierarchical, vehicles first, double precision, 2 decimals) vs CVRPLIB (distance only, truncated to 1 decimal, truncated travel times). A solution beating one is not a win against the other; the headline criterion is CVRPLIB only.
- Truncation must be applied per edge (floor(10*d)/10), not to the total, and the SAME truncated value is the travel time; using double-precision travel times rejects posted BKSs (RC1_8_1, R1_10_3) and using truncated distance with untruncated time is a mixed convention that matches nothing.
- Vehicle limit: the instance's VEHICLE NUMBER (250 for 1000-customer files, 200 for 800) is an upper bound; a solution with more routes is infeasible even though the objective ignores vehicle count.
- Re-fetch the All Instances table and the Updates page immediately before claiming; values moved on three consecutive days in Sept 2026.
- Do not treat Solomon 100-customer instances or the 200-customer Homberger instances (all Opt = yes on CVRPLIB) as targets.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/optimization-benchmarks/cvrplib-vrptw-gh-dimacs-bks.md
```

Already set up? Say `run V3R1T4S on cvrplib-vrptw-gh-dimacs-bks`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `cvrplib-vrptw-gh-dimacs-bks`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
