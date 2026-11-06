# OptiWindNet RouteSets: a shorter radial cable network for Yi-2019.1_OSS, capacity 11

## What
For release r26.10-v4 instance Yi-2019.1_OSS at capacity 11, the claimed radial route set (object/) has recomputed length 129717.3657 m, 5622.0108 m (4.154%) shorter than the only stored radial route set (id 21564, baselines.hgs, 135339.3765 m), with 11 feeders (≤ 11); it uses the identical nodeset, passes validate_routeset with no violations, and stays inside the border and outside every obstacle interior. It is not shorter than the stored branched best (id 22551, 127958.8646 m), so it is a full-criterion win for topology X = radial only.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial, under the bank's full success criterion. It is NOT shorter than the stored branched best (127958.8646 m, MILP.pyomo.gurobi); this is a radial-topology record only, not the instance's overall best. Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; about 20 seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **129717.3657** | see panel | own HGS-CVRP run |
| stored id 22551 | branched | 127958.8646 | [12] | MILP.pyomo.gurobi |
| stored id 21911 | branched | 130862.0948 | [12] | MILP.pyomo.cplex |
| stored id 21564 | radial | 135339.3765 | [11] | baselines.hgs |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked 2026-11-06T00:49Z: still the latest). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new method (the same HGS-CVRP heuristic run longer with another seed), nothing about other instances, no built-wind-farm claim (literature benchmark layout, non-'!' variant). Disclosed: 16 segments touch obstacle boundaries (3 run along obstacle edges), as stored routes do; 2 shared corridors (substation to turbines 93 and 72) without hidden crossings; cables passing through turbine positions as detour points are accepted by the official validator. Literature-benchmark variant (Yi, Scutariu and Smith 2019), not a built farm.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder and the HGS-CVRP wrapper.
- Base layout: X. Yi, M. Scutariu and K. Smith, Optimization of offshore wind farm inter-array collection system, IET Renew. Power Gener. 13 (2019) 1990-1999, doi 10.1049/iet-rpg.2018.5805.
- Thibaut Vidal: HGS-CVRP.
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
