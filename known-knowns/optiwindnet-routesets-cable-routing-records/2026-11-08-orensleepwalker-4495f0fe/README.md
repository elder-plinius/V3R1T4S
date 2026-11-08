# OptiWindNet RouteSets: a shorter branched cable network for Hornsea Two West, capacity 7

## What
For OptiWindNet RouteSets r26.10-v4 instance "Hornsea Two West" (no '!' prefix, 110 turbines, 1 substation, 0 obstacles) at capacity 7, the branched route set in object/ has a Euclidean segment-sum length of 217395.354 m, 316.831 m (0.146%) shorter than the shortest of the four stored route sets (radial ids 3689 and 44466, tied at 217712.185 m) and 989.045 m shorter than the only stored branched set (id 98), uses 16 feeders at the single substation (equal to the stored best's [16]), carries the release's nodeset unchanged, returns no violations from optiwindnet 0.3.2 validate_routeset, and stays inside the site border; no optimality is established (the 'OPTIMAL', relgap and bound fields in the packed object refer only to a final restricted sub-solve).

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **217395.3540** | see panel | own CP-SAT fix-and-optimise search |
| stored id 3689 | radial | 217712.1849 | [16] | baselines.hgs |
| stored id 44466 | radial | 217712.1849 | [16] | MILP.pyomo.cplex |
| stored id 98 | branched | 218384.3987 | [16] | MILP.pyomo.cplex |
| stored id 4178 | radial | 234134.8717 | [16] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from the shortest stored set (radial; ids 3689 baselines.hgs and 44466 MILP.pyomo.cplex tie). Disclosed: the only stored branched run is a 2023 CPLEX run stopped at its time limit (gap 2.4%), a weak branched baseline; the packed object's misc fields describe only the last pinned window sub-solve; detour points on turbines 49/50 as in the stored sets; cosmetic handle difference; G.pickle (not shipped) may contain a local path. Seeded from the shortest stored set (radial; ids 3689/44466 tie).
Scope limit: a win for topology X = branched. No optimality.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea Two West (Hornsea Project Two, west area; UK North Sea, built; 110 turbines), single substation, layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
