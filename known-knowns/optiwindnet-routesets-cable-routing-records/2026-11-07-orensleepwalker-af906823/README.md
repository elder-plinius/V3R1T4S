# OptiWindNet RouteSets: a shorter radial cable network for Yi-2019.1_OSS, capacity 12

## What
For release r26.10-v4 instance Yi-2019.1_OSS with capacity 12 and topology radial, the claimed route set (10 substation feeders, 0 validate_routeset violations, inside the border and outside all 17 obstacles) has a Euclidean segment-sum length of 125848.932131 m, which is 185.739 m (1.47e-3 relative) shorter than the only stored radial route set (id 21567, 126034.671542 m, 10 feeders), while the stored branched route set (id 21894, 121874.579734 m) remains shorter.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology radial, under the bank's full success criterion. It is NOT shorter than the stored branched best (121874.5797 m, MILP.pyomo.cplex); this is a radial-topology record only, not the instance's overall best. Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; about 20 seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | radial | **125848.9321** | see panel | own HGS-CVRP run |
| stored id 21894 | branched | 121874.5797 | [11] | MILP.pyomo.cplex |
| stored id 21567 | radial | 126034.6715 | [10] | baselines.hgs |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (status re-checked 2026-11-07T16:18:49Z; still the latest). See the-record-we-beat/record.md.

## Not claimed
The improvement is a single local move: the stored radial best (id 21567) with turbines 11 and 27 exchanged between two adjacent strings; it is not shorter than the stored branched best (id 21894, 121874.58 m). Partial win p2 is not claimed: it requires a real-site instance, whereas Yi-2019 is a literature benchmark.
No optimality, no new method (the same HGS-CVRP heuristic run longer with another seed), nothing about other instances, no built-wind-farm claim (literature benchmark layout, non-'!' variant). DTU's older dataset (Zenodo 18864643) holds two shorter capacity-12 sets for this site, both branched (see panel/novelty.md); this is a radial-topology record only. Disclosed: the object equals the stored radial best 21567 with turbines 11 and 27 exchanged between two adjacent strings (115 of 119 edges shared): not a trivial edit in the kit's sense, but a single local move that the stored ~120-s HGS run missed; the object itself came from an independent 240-s HGS run (seed 101). 10 collinear feeder corridors through turbine positions as in the stored set; two segments run along obstacle edges with zero length inside them.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder and the HGS-CVRP wrapper.
- Base layout: X. Yi, M. Scutariu and K. Smith, Optimization of offshore wind farm inter-array collection system, IET Renew. Power Gener. 13 (2019) 1990-1999, doi 10.1049/iet-rpg.2018.5805.
- Thibaut Vidal: HGS-CVRP.
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
