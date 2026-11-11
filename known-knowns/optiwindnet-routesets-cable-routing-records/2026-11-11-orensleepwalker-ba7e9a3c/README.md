# OptiWindNet RouteSets: a shorter radial cable network for Noirmoutier, capacity 2

## What
For the OptiWindNet RouteSets r26.10-v4 instance (nodeset "Noirmoutier", 61 turbines, 1 substation, no obstacles; capacity 2), the route set in `object/routeset-packed.json` / `object/segments.json` is a radial network with 31 feeders, on the same turbine and substation coordinates, of total Euclidean length 150439.9933 m, which is 387.0468 m (0.2566%) shorter than the shortest of the four route sets stored for that instance (id 46244, radial, baselines.lkh, 150827.0401 m, 31 feeders), passes `validate_routeset` of optiwindnet 0.3.2 with no violations, and lies entirely inside the site border; nothing is established about optimality or any other instance.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **150439.9933** | see panel | own CP-SAT fix-and-optimise search |
| stored id 46244 | radial | 150827.0401 | [31] | baselines.lkh |
| stored id 27495 | radial | 150985.2106 | [31] | baselines.hgs |
| stored id 27564 | branched | 150985.2106 | [31] | MILP.pyomo.cplex |
| stored id 36274 | radial | 150985.2106 | [31] | MILP.pyomo.cplex |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Branched fix-and-optimise LNS (CP-SAT windows, seed 7, 37 min) from the shortest stored route set; run 2026-11-10-1803 Disclosed: the packed object and G.pickle label the topology "branched" (the search model's label; the object itself is radial), and claim criterion.txt/REPRODUCE.md say X = branched (template) while CLAIM.md says radial (both hold); the packed object carries misc fields (termination OPTIMAL, bound 150069.158, relgap) from the last pinned window sub-solve, which describe that sub-solve and not the instance (stored sets have a lower straight-line objective, 149999.638); its handle is "Noirmoutier" where the release uses "noirmoutier" (cosmetic); overlapping detour segments, as in the stored sets (accepted by the validator); G.pickle is a re-pickled copy of the saved graph, was not loaded by the skeptics and is not shipped. Reviewer limits: the criterion skeptic did not re-fetch Zenodo; the novelty skeptic did not check border containment (the other two did).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Noirmoutier (61 turbines, 1 substation), capacity 2, topology radial
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
