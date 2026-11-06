# OptiWindNet RouteSets: a shorter radial cable network for Cazzaro-2022G-210.solid.1_OSS, capacity 7

## What
For release r26.10-v4 instance Cazzaro-2022G-210.solid.1_OSS at capacity 7, the radial route set in object/ has recomputed Euclidean length 360354.0746 m, 4219.1943 m (1.157%) shorter than the only stored radial set (id 25104, 364573.2688 m) and also shorter than the stored branched set (id 25281, 363836.6318 m), using 30 feeders (equal to both stored sets), on the bitwise-identical nodeset, with validate_routeset returning no violations and all 228 segments inside the closed border polygon (12 touch it only at border-vertex detour endpoints; the nodeset has no obstacles).

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial, under the bank's full success criterion. It is also shorter than the stored branched best. Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; about 20 seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **360354.0746** | see panel | own HGS-CVRP run |
| stored id 25281 | branched | 363836.6318 | [30] | MILP.pyomo.cplex |
| stored id 25104 | radial | 364573.2688 | [30] | baselines.hgs |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked 2026-11-06T00:49Z: still the latest). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new method (the same HGS-CVRP heuristic run longer with another seed), nothing about other instances, no built-wind-farm claim (literature benchmark layout, non-'!' variant). Disclosed: 12 segments touch the border only at concave border-corner detour endpoints (the stored sets have the same 12); 11 coincident segment pairs in 7 shared corridors with no hidden crossing (stored sets: 39 and 38); the novelty skeptic's context automatically included the workspace CLAUDE.md/AGENTS.md (one status line about this run), which it reports not using. Literature-benchmark variant (Cazzaro & Pisinger 2022), not a built farm; sibling instance (capacity 6) is a separate claim.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder and the HGS-CVRP wrapper.
- Base layout: D. Cazzaro and D. Pisinger, Balanced cable routing for offshore wind farms with obstacles, Networks 80 (2022) 386-406, doi 10.1002/net.22100.
- Thibaut Vidal: HGS-CVRP.
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
