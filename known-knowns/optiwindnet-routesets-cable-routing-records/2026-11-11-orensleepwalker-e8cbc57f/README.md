# OptiWindNet RouteSets: a shorter radial cable network for Hornsea One.1_OSS, capacity 2

## What
For the r26.10-v4 instance (nodeset "Hornsea One.1_OSS", capacity 2), the route set in `object/` is a structurally radial network (87 feeders, each a path of exactly 2 turbines) carrying the release's exact VertexC and border, of total Euclidean length 1030454.2878 m, which is 896.1118 m (8.689e-4 relative) shorter than the shortest of all four route sets stored for that instance (id 42234, radial, 1031350.3996 m, 87 feeders), passes optiwindnet 0.3.2 validate_routeset with no violations and lies entirely inside the site border; nothing is established about optimality, other instances, or releases later than Zenodo record 23537067.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **1030454.2878** | see panel | own CP-SAT fix-and-optimise search |
| stored id 42234 | radial | 1031350.3996 | [87] | MILP.pyomo.cplex |
| stored id 9595 | radial | 1031350.3996 | [87] | baselines.hgs |
| stored id 8881 | radial | 1032129.6496 | [87] | baselines.lkh |
| stored id 2782 | branched | 1032792.2112 | [88] | MILP.pyomo.cplex |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Branched fix-and-optimise LNS (CP-SAT windows, seed-selected) from the shortest stored route set; run 2026-11-09-1540 Disclosed: the packed object and G.pickle label the topology "branched" (the search model's label; the object itself is radial), and claim criterion.txt/REPRODUCE.md say X = branched (template) while CLAIM.md says radial (both hold); the packed object carries misc fields (bound, relgap 0.0, OPTIMAL, runtime) from the last pinned window sub-solve, which describe that sub-solve and not the instance; its handle differs from the release's "hornsea_1" (cosmetic); collinear overlaps where feeders share detour runs, as in the stored sets (benchmark convention, accepted by the validator); G.pickle may contain a local path. Hornsea One.1_OSS is the single-substation variant. Seeded from the shortest stored set. Reviewer limits: the novelty skeptic did not read the preprint PDF's full text; the criterion skeptic notes status/zenodo-latest.json carries no retrieval timestamp (the run's data/status-fetch-utc.txt holds it; the novelty skeptic fetched the status live).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One.1_OSS (174 turbines, 1 substation), capacity 2, topology radial
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
