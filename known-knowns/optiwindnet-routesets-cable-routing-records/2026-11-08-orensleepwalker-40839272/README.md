# OptiWindNet RouteSets: a shorter branched cable network for London Array.1_OSS, capacity 9

## What
For OptiWindNet RouteSets release r26.10-v4 instance "London Array.1_OSS" with capacity 9 (175 turbines, 1 substation, no obstacles), the branched route set in object/ has a Euclidean segment-sum length of 153957.9889 m with 20 feeders, passes optiwindnet 0.3.2 validate_routeset with no violations, lies inside the site border, and is 401.1715 m (0.2599%) shorter than the shortest of the 4 stored route sets for that instance (radial ids 44577 and 9629, 154359.1604 m, feeders [20]), with no optimality established; the packed object's bound, relgap, termination and runtime fields describe only a final restricted sub-solve.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **153957.9889** | see panel | own CP-SAT fix-and-optimise search |
| stored id 44577 | radial | 154359.1604 | [20] | MILP.pyomo.cplex |
| stored id 9629 | radial | 154359.1604 | [20] | baselines.hgs |
| stored id 2794 | branched | 154403.5350 | [20] | MILP.pyomo.cplex |
| stored id 8917 | radial | 158074.8692 | [20] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from the shortest stored set (radial; ids 44577 MILP.pyomo.cplex and 9629 baselines.hgs tie). The stored record is soft: a plain local search from it already gets below it; this route set beats that local search by about 181 m. Disclosed: the stored record is soft: a local search of single-subtree moves and leaf swaps from the seed reaches 154130.49 m (straight-line measure), already below the record; the object beats that by about 181 m on the same measure.
Scope limit: a win for topology X = branched. No optimality.
Disclosed: the packed object's misc fields (bound, relgap, OPTIMAL, runtime) describe only the last pinned window sub-solve (the release's branched bound is lower); 4 collinear detour corridors through turbine 73's position as in the stored best set; cosmetic handle difference; G.pickle (not shipped) may contain a local path. Seeded from the shortest stored set (radial; ids 44577/9629 tie).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: London Array (Thames Estuary, UK; built; 175 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
