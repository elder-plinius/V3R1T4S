# OptiWindNet RouteSets: a shorter branched cable network for Sofia, capacity 4

## What
For release r26.10-v4 instance (Sofia, capacity 4), the submitted branched route set (25 feeders, validate_routeset [], all segments inside the border, no obstacles present) has a recomputed Euclidean length of 377027.9310 m, which is 1559.33 m (0.412%) shorter than the shortest of the 4 stored route sets (46020, radial LKH, 378587.2597 m, 25 feeders) and 1869.63 m shorter than the stored branched CPLEX set (25155); no optimality is established, and its straight-line objective (375860.98 m) is above that of set 25155.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **377027.9310** | see panel | own CP-SAT fix-and-optimise search |
| stored id 46020 | radial | 378587.2597 | [25] | baselines.lkh |
| stored id 25155 | branched | 378897.5658 | [25] | MILP.pyomo.cplex |
| stored id 35902 | radial | 379237.6114 | [25] | MILP.pyomo.cplex |
| stored id 25008 | radial | 379237.7079 | [25] | baselines.hgs |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored set id 46020 (LKH-3, radial). The gain comes from shorter detours: on straight-line length the object is 423.6 m longer than the stored branched CPLEX set 25155, but its detour-inclusive length (the criterion's measure) is 1869.63 m shorter. Disclosed: the gain comes from shorter detours: the object's straight-line (model) objective 375860.98 m is 423.6 m LONGER than that of the stored branched CPLEX set 25155, while its detour-inclusive length (the criterion's measure) is 1869.63 m shorter; re-routing the stored sets with PathFinder leaves their lengths unchanged. The packed object's misc fields (bound, relgap, OPTIMAL, runtime) describe only the last pinned window sub-solve and its "bound" is contradicted by set 25155; 13 shared corridors as in the stored sets; cosmetic handle difference; G.pickle (not shipped) may contain a local path. Seeded from stored set id 46020 (LKH-3, radial).
Scope limit: a win for topology X = branched. No optimality.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Sofia offshore wind farm (Dogger Bank, UK North Sea, built; 100 turbines), single substation, layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
