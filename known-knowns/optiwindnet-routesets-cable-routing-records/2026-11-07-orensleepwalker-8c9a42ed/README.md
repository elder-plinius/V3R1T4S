# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 5

## What
For the r26.10-v4 instance (Hornsea One.1_OSS, capacity 5), the branched route set in object/ has a recomputed Euclidean length of 506483.6421 m, 1168.4771 m (0.230%) shorter than all four stored route sets (best: id 44834, radial, 507652.1192 m), uses 35 feeders (equal to that set's 35), carries the identical nodeset, passes validate_routeset with no violations, and stays inside the border (no obstacles exist), with release latest-ness established only by the shipped Zenodo snapshot and the object's bound/relgap/OPTIMAL metadata not valid as instance bounds.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **506483.6421** | see panel | own CP-SAT fix-and-optimise search |
| stored id 44834 | radial | 507652.1192 | [35] | MILP.pyomo.cplex |
| stored id 2798 | branched | 507673.2764 | [35] | MILP.pyomo.cplex |
| stored id 9633 | radial | 509207.2549 | [35] | baselines.hgs |
| stored id 8921 | radial | 527587.2778 | [35] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer at 2026-11-07T09:06:24Z; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored set id 44834 (CPLEX, radial). Disclosed: the packed object's misc fields (bound, relgap 0, OPTIMAL, runtime, creator and warmstart labels) describe only the last pinned 30-s CP-SAT window sub-solve and must not be read as an instance certificate (the release's branched bound for this instance is 497716.26 m); the packed handle string differs cosmetically from the database handle; 43 collinear segment overlaps (feeders bundled along one corridor through a turbine position) follow the stored sets' convention and are accepted by the validator; G.pickle (not shipped in the package) contains a local file path. Seeded from stored set id 44834 (CPLEX, radial).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One offshore wind farm (UK North Sea, built; 174 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
