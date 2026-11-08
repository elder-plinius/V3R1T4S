# OptiWindNet RouteSets: a shorter branched cable network for London Array.1_OSS, capacity 7

## What
For OptiWindNet RouteSets r26.10-v4 instance (London Array.1_OSS, capacity 7), the branched route set in object/ has a Euclidean segment-sum length of 173753.9532 m, 212.49 m (0.122%) shorter than every one of the 4 stored route sets (shortest: radial ids 9627 and 45872 at 173966.4420 m), uses 25 feeders (cap 25), is on the identical stored nodeset, passes optiwindnet 0.3.2 validate_routeset with no violations, and lies wholly inside the site border (no obstacles exist), with release identity checked against the hashes and a captured Zenodo latest-version snapshot rather than a live query.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **173753.9532** | see panel | own CP-SAT fix-and-optimise search |
| stored id 9627 | radial | 173966.4420 | [25] | baselines.hgs |
| stored id 45872 | radial | 173966.4420 | [25] | MILP.pyomo.cplex |
| stored id 2792 | branched | 174227.8163 | [26] | MILP.pyomo.cplex |
| stored id 8904 | radial | 188458.0326 | [25] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from the shortest stored set (radial; ids 9627 baselines.hgs and 45872 MILP.pyomo.cplex tie). The improvement is shallow: two local swaps changing 6 of 175 links. Disclosed: the improvement is shallow: the object keeps 169 of the seed's 175 links and changes 6 in two local swaps (-55.33 m and -157.10 m); polishing the seed's detours alone cannot reach it (seed straight-line length 173919.86 m). The packed object's misc fields describe only the last pinned window sub-solve (the release's branched bound is 170760.98 m); six collinear detour corridors as in the stored sets; cosmetic handle difference; G.pickle (not shipped) may contain a local path. Seeded from the shortest stored set (radial; ids 9627/45872 tie).
Scope limit: a win for topology X = branched. No optimality.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: London Array (Thames Estuary, UK; built; 175 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
