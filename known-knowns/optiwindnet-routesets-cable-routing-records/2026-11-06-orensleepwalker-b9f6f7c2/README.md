# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 8

## What
For OptiWindNet RouteSets release r26.10-v4 (xz sha256 c78c8f3c…e3a), instance Hornsea One.1_OSS at capacity 8, the branched route set in object/ (174 turbines, 22 feeders at the single substation) passes validate_routeset with no violations, lies inside the site border (the site has no obstacles), and has a summed Euclidean length of 377034.6925 m, which is 3261.3617 m (0.858%) shorter than the shortest of the four stored capacity-8 route sets (id 45794, radial, 380296.0542 m, 22 feeders); optimality is not shown.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **377034.6925** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45794 | radial | 380296.0542 | [22] | MILP.pyomo.cplex |
| stored id 2800 | branched | 381105.3514 | [22] | MILP.pyomo.cplex |
| stored id 9636 | radial | 383497.6637 | [22] | baselines.hgs |
| stored id 8923 | radial | 385884.6735 | [22] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer on 2026-11-06; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored set id 2800 (CPLEX, branched). Disclosed: the packed object's misc fields (bound, relgap, OPTIMAL, runtime) describe only the last pinned 30-s CP-SAT window sub-solve, not the whole route set, and must not be read as a certificate; 12 cable bends sit on turbine positions as detour points (same convention as the stored sets, accepted by the validator). Seeded from stored set id 2800 (CPLEX, branched). Hornsea One.1_OSS is the release's single-substation variant of the built Hornsea One farm.
Extra downgrade check by the main session (after the London Array novelty skeptic found DTU's earlier dataset Zenodo 18864643): its paperdb.v3.sqlite holds Hornsea One.1_OSS (VertexC and digest identical to the release) only at capacities 2-5, and no 174-turbine nodeset there has route sets at capacity 8 or 10; MILP_model_comparison.v3.sqlite has no Hornsea site. No downgrade.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One offshore wind farm (UK North Sea, built; 174 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
