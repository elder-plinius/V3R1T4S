# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 4

## What
For the OptiWindNet RouteSets r26.10-v4 instance (nodeset "Hornsea One.1_OSS", 174 turbines, 1 substation, no obstacles; capacity 4), the route set in `object/routeset-packed.json` / `object/segments.json` is a valid branched network on the identical nodeset with 45 substation feeders and total Euclidean length 589790.5176 m, which is 1360.8220 m (0.2302 %) shorter than the shortest of the four route sets stored for that instance (id 42471, radial, 591151.3395 m, 45 feeders), passes optiwindnet 0.3.2 `validate_routeset` with no violations and stays inside the site border; it is not shown to be optimal and does not improve on the 44-feeder stored sets' feeder count.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **589790.5176** | see panel | own CP-SAT fix-and-optimise search |
| stored id 42471 | radial | 591151.3395 | [45] | MILP.pyomo.cplex |
| stored id 9601 | radial | 595070.4239 | [44] | baselines.hgs |
| stored id 2787 | branched | 596799.9297 | [45] | MILP.pyomo.cplex |
| stored id 8898 | radial | 604020.3250 | [44] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Branched fix-and-optimise LNS (CP-SAT windows, seed-selected) from the shortest stored route set; run 2026-11-09-1540 Disclosed: the packed object carries misc fields (bound, relgap 0.0, OPTIMAL, runtime) from the last pinned window sub-solve, which describe that sub-solve and not the instance; its handle differs from the release's "hornsea_1" (cosmetic); collinear overlaps where feeders share detour runs, as in the stored sets (benchmark convention, accepted by the validator); G.pickle may contain a local path. Hornsea One.1_OSS is the single-substation variant. Seeded from the shortest stored set. Reviewer limits: the criterion skeptic could not unpickle object/G.pickle in its sandbox and validated the graph rebuilt from the packed JSON (the reproduce skeptic validated both); the novelty skeptic extracted the preprint PDF text only partly.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One.1_OSS (174 turbines, 1 substation), capacity 4, topology branched
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
