# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 6

## What
The frozen branched route set for Hornsea One.1_OSS at capacity 6 satisfies the full cell criterion against all four stored route sets for that instance in release r26.10-v4 as identified by the supplied status snapshot, without establishing global optimality or optimizer superiority.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **449188.8203** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45811 | radial | 450092.3517 | [30] | MILP.pyomo.cplex |
| stored id 2799 | branched | 451220.9919 | [30] | MILP.pyomo.cplex |
| stored id 9634 | radial | 452600.5081 | [29] | baselines.hgs |
| stored id 8922 | radial | 464173.5462 | [30] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked during this run and by its novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored route set id 45811 (CPLEX, radial). Disclosed: seed stored id45811 (CPLEX radial); maximum turbine degree3; two contour clones and25 detour clones;45 coincident segment pairs and142 endpoint contacts between distinct graph nodes, accepted by the official shared-corridor/local-ordering semantics. Every separate cable is counted even where geometric corridors coincide; no proper crossings or border departures. Packed OPTIMAL/bound/zero-gap/runtime/creator/warmstart fields refer only to the final restricted window solve. Handle text may differ cosmetically. G.pickle stays local because it may include a local path; package only plain JSON. Original neighborhood-search code credited to Claude Code; DTU dataset/model/validator and Google OR-Tools credited.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://gitlab.windenergy.dtu.dk/TOPFARM/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One.1_OSS is the single-substation benchmark variant of the built Hornsea One farm.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Codex (this run, verification, packaging), Claude Code (original neighborhood-search implementation), and three separately started AI review contexts.
