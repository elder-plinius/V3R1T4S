# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 7

## What
For release r26.10-v4 instance "Hornsea One.1_OSS" at capacity 7 (no '!' prefix; latest Zenodo version per the bundled status snapshot), the claimed branched route set, with 26 feeders (equal to the cap from the shortest stored set), the identical nodeset, no validate_routeset violations and every segment inside the border (no obstacles), has a Euclidean segment-sum length of 407209.0156 m, which is 893.56 m (0.219%) shorter than the shortest of the four stored radial or branched sets (id 45791, radial, 408102.5795 m), with no optimality established.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **407209.0156** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45791 | radial | 408102.5795 | [26] | MILP.pyomo.cplex |
| stored id 2801 | branched | 411304.2676 | [25] | MILP.pyomo.cplex |
| stored id 9637 | radial | 414178.6097 | [25] | baselines.hgs |
| stored id 8924 | radial | 419780.0637 | [25] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored set id 45791 (CPLEX, radial). The feeder cap (26) is that shortest stored set's; the other stored sets use 25. Disclosed: (1) the improvement over the seed id 45791 consists of four single-edge exchanges that create branch points (about -888 m straight-line, -6 m detours): more than the kit's trivial edits, but shallow (a plain one-edge local search would find it); (2) the feeder cap 26 is the shortest stored set's, as the criterion states; that set came from a CPLEX run with a min_plus1 feeder limit, while the other three stored sets use 25 feeders; (3) the packed object's misc fields (bound, relgap, OPTIMAL, runtime, creator/warmstart labels) describe only the last pinned window sub-solve; (4) 21 collinear corridor overlaps follow the stored sets' convention; the packed handle differs cosmetically. Seeded from stored set id 45791 (CPLEX, radial).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One offshore wind farm (UK North Sea, built; 174 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
