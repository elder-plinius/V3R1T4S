# OptiWindNet RouteSets: a shorter branched cable network for Hornsea Two West, capacity 9

## What
For release r26.10-v4 (record 23537067, latest per the shipped status snapshot), instance (Hornsea Two West, capacity 9), the claimed branched route set has Euclidean length 191786.9545 m, which is 1099.7748 m (0.570%) shorter than the shortest of all four stored route sets (radial ids 4305/44553, 192886.7293 m); it uses 13 feeders (equal to their [13]), passes validate_routeset with no violations, and lies within the border of the unchanged nodeset, which has no obstacles. This confirms no optimality, and the bound/relgap/OPTIMAL fields in the packed object are sub-solve artefacts, not a certificate.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **191786.9545** | see panel | own CP-SAT fix-and-optimise search |
| stored id 4305 | radial | 192886.7293 | [13] | baselines.hgs |
| stored id 44553 | radial | 192886.7293 | [13] | MILP.pyomo.cplex |
| stored id 100 | branched | 193222.8342 | [13] | MILP.pyomo.cplex |
| stored id 4181 | radial | 194384.9991 | [13] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from the shortest stored set (radial; ids 4305 baselines.hgs and 44553 MILP.pyomo.cplex tie). Disclosed: the packed object's misc fields (bound, relgap, OPTIMAL, runtime, creator/warmstart labels) describe only the last pinned 30-s window sub-solve (the release's branched bound for this instance is 186907.20 m); detour points on turbines 49/46 and one shared substation corridor follow the stored sets' convention; the packed handle differs cosmetically; G.pickle (not shipped) may contain a local path. Seeded from the shortest stored set (radial; ids 4305/44553 tie).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea Two West (Hornsea Project Two, west area; UK North Sea, built; 110 turbines), single substation, layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
