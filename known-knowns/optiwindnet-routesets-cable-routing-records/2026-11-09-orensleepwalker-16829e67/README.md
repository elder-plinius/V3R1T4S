# OptiWindNet RouteSets: a shorter radial cable network for Race Bank.1_OSS, capacity 3

## What
For release r26.10-v4 (as recorded latest in status/zenodo-latest.json), instance nodeset "Race Bank.1_OSS" (the single-substation variant of Race Bank, no '!' prefix) with capacity 3, the route set in object/ is radial (every turbine has degree at most 2) with total Euclidean segment length 153796.9412 m, which is shorter than every stored route set for that instance (shortest stored radial 155036.8793 m, ids 45770 and 9504, by 1239.9381 m or 0.800%; shortest stored branched 156071.6528 m, id 2743), uses 31 feeders (equal to the shortest stored set's [31]), carries the same nodeset, passes optiwindnet 0.3.2 validate_routeset with no violations, and lies entirely inside the site border (no obstacles exist); no claim of optimality is confirmed, and the packed metadata's "branched" label and relgap 0.0 / OPTIMAL fields describe a restricted sub-solve, not the instance.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial (and therefore also branched), under the bank's full success criterion (it is shorter than every stored route set of either topology). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **153796.9412** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45770 | radial | 155036.8793 | [31] | MILP.pyomo.cplex |
| stored id 9504 | radial | 155036.8793 | [31] | baselines.hgs |
| stored id 8812 | radial | 155172.6133 | [31] | baselines.lkh |
| stored id 2743 | branched | 156071.6528 | [31] | MILP.pyomo.cplex |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from the shortest stored set (radial; ids 45770 MILP.pyomo.cplex and 9504 baselines.hgs tie). The result is itself radial (every turbine degree <= 2), although found by a branched search. Disclosed: the packed object and G.pickle label the topology "branched" (the search model's label; the object itself is radial) and carry misc fields (bound, relgap, OPTIMAL, runtime) from the last pinned window sub-solve; claim/criterion.txt's header line says X = branched (template) while CLAIM.md says radial (both hold); the object's straight-line objective lies 184.8 m below the 2024 branched run's stored bound, an inconsistency between the release's models, not a defect; 8 shared feeder corridors as in the stored sets; cosmetic handle difference; G.pickle (not shipped) may contain a local path. Race Bank.1_OSS is the single-substation variant. Seeded from the shortest stored set (radial; ids 45770/9504 tie).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Race Bank (UK North Sea, built; 91 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
