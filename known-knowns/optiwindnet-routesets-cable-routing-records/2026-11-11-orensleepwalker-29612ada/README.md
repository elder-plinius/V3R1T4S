# OptiWindNet RouteSets: a shorter radial cable network for Hornsea One.1_OSS, capacity 3

## What
For the r26.10-v4 instance (nodeset "Hornsea One.1_OSS", capacity 3), the route set in object/ is a radial network on the release's exact nodeset with 58 feeders at the single substation and a Euclidean length of 735605.4808 m, which is 343.2720 m (4.66e-4 relative) shorter than the shortest of the four stored route sets for that instance (id 40884, radial, 735948.7528 m, feeders [58]), passes validate_routeset with no violations and lies entirely inside the site border; no optimality is established, and release latest-ness is shown only by the frozen snapshot status/zenodo-latest.json.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **735605.4808** | see panel | own CP-SAT fix-and-optimise search |
| stored id 40884 | radial | 735948.7528 | [58] | MILP.pyomo.cplex |
| stored id 9597 | radial | 738034.6339 | [58] | baselines.hgs |
| stored id 2784 | branched | 739768.9053 | [59] | MILP.pyomo.cplex |
| stored id 8885 | radial | 753634.9352 | [58] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Branched fix-and-optimise LNS (CP-SAT windows, seed-selected) from the shortest stored route set; run 2026-11-09-1540 Disclosed: the packed object and G.pickle label the topology "branched" (the search model's label; the object itself is radial), and claim criterion.txt/REPRODUCE.md say X = branched (template) while CLAIM.md says radial (both hold); the packed object carries misc fields (bound, relgap 0.0, OPTIMAL, runtime) from the last pinned window sub-solve, which describe that sub-solve and not the instance; its handle differs from the release's "hornsea_1" (cosmetic); collinear overlaps where feeders share detour runs, as in the stored sets (benchmark convention, accepted by the validator); G.pickle may contain a local path. Hornsea One.1_OSS is the single-substation variant. Seeded from the shortest stored set. Reviewer limits: the novelty skeptic did not run GitHub code search (needs authentication).

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One.1_OSS (174 turbines, 1 substation), capacity 3, topology radial
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
