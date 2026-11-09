# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 10

## What
For OptiWindNet RouteSets release r26.10-v4 (sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, the latest Zenodo version per the frozen status/zenodo-latest.json snapshot), instance "Hornsea One.1_OSS" at capacity 10, the claim's branched route set (174 turbines, 1 substation, max turbine degree 3, 18 feeders, identical VertexC) has Euclidean-sum length 332729.3443 m, passes optiwindnet 0.3.2 validate_routeset with no violations, lies wholly inside the site border (no obstacles exist), and is strictly shorter by more than 1e-6 relative than all 4 stored route sets for that instance, the shortest being id 45802 (radial, MILP.pyomo.cplex, 336086.4654 m, 18 feeders), by 3357.1211 m (0.999%); no optimality is established, and the packed object's bound/relgap/OPTIMAL metadata refer only to a pinned sub-solve.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **332729.3443** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45802 | radial | 336086.4654 | [18] | MILP.pyomo.cplex |
| stored id 9644 | radial | 340159.1949 | [18] | baselines.hgs |
| stored id 2804 | branched | 342349.2849 | [19] | MILP.pyomo.cplex |
| stored id 8928 | radial | 350931.2830 | [18] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer on 2026-11-06; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored set id 45802 (CPLEX, radial). Disclosed: the packed object's misc fields (bound, relgap, OPTIMAL, runtime) describe only the last pinned 30-s CP-SAT window sub-solve, not the whole route set, and must not be read as a certificate; three feeder pairs share a straight corridor where a cable bends on a turbine position (same convention as the stored sets, accepted by the validator); the packed handle string differs cosmetically from the database handle. Seeded from stored set id 45802 (CPLEX). Hornsea One.1_OSS is the release's single-substation variant of the built Hornsea One farm.
Extra downgrade check by the main session (after the London Array novelty skeptic found DTU's earlier dataset Zenodo 18864643): its paperdb.v3.sqlite holds Hornsea One.1_OSS (VertexC and digest identical to the release) only at capacities 2-5, and no 174-turbine nodeset there has route sets at capacity 8 or 10; MILP_model_comparison.v3.sqlite has no Hornsea site. No downgrade.
Layout note (2026-11-06T16:30Z): after the panel, claim-ho10/ and panel-ho10/ were renamed to the run's primary claim/ and panel/ (kit layout; every file's sha256 unchanged); compatibility symlinks claim-ho10 and panel-ho10 keep the reviewers' scripts runnable. The reviewer reports are unchanged.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One offshore wind farm (UK North Sea, built; 174 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
