# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 9

## What
For OptiWindNet RouteSets r26.10-v4 (sqlite.xz sha256 c78c8f3c…e3a, Zenodo record 23537067, marked latest in the shipped status snapshot), instance 'Hornsea One.1_OSS' with capacity 9, the branched route set in object/ has Euclidean length 351584.0138 m with 20 feeders, passes validate_routeset with no violations, lies inside the border (no obstacles exist), and is shorter by 2020.66 m (0.571 %) than the shortest of the four stored radial-or-branched sets (ids 9638 and 45718, 353604.6746 m, 20 feeders); its internal bound/relgap/OPTIMAL metadata covers only a restricted sub-solve and certifies nothing about the instance.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **351584.0138** | see panel | own CP-SAT fix-and-optimise search |
| stored id 9638 | radial | 353604.6746 | [20] | baselines.hgs |
| stored id 45718 | radial | 353604.6746 | [20] | MILP.pyomo.cplex |
| stored id 2802 | branched | 358653.0477 | [20] | MILP.pyomo.cplex |
| stored id 8925 | radial | 372903.6710 | [20] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from the shortest stored set (radial; ids 9638 baselines.hgs and 45718 MILP.pyomo.cplex tie). Disclosed: the packed object's misc fields (bound, relgap, OPTIMAL, runtime, creator and warmstart labels) describe only the last pinned 30-s CP-SAT window sub-solve and must not be read as an instance certificate; some detour points sit on other turbines' coordinates, as in the stored sets 9638/45718; the packed handle string differs cosmetically from the database handle; G.pickle (not shipped in the package) may contain a local path. Seeded from the shortest stored set (ids 9638/45718 tie).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One offshore wind farm (UK North Sea, built; 174 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
