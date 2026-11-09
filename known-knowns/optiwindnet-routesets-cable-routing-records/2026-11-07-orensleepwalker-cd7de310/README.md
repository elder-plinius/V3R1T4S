# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 11

## What
The fixed branched route set for the non-augmented Hornsea One.1_OSS instance at capacity 11 satisfies the full bank success criterion against every stored route set for that instance in the hash-pinned r26.10-v4 release, with release status supported by the supplied latest-version snapshot.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **318217.6793** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45874 | radial | 319646.1210 | [16] | MILP.pyomo.cplex |
| stored id 2803 | branched | 320947.1382 | [17] | MILP.pyomo.cplex |
| stored id 9639 | radial | 327712.9880 | [16] | baselines.hgs |
| stored id 8926 | radial | 360256.1584 | [16] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked during this run and by its novelty reviewer; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored route set id 45874 (CPLEX, radial). Disclosed: seed stored id45874 (CPLEX radial); four border-routing clones; all detour lengths counted. Packed OPTIMAL/bound/relgap/runtime/creator/warmstart metadata describe the last pinned sub-solve, not full-instance optimality. Handle naming is cosmetic. G.pickle stays local because it may contain a local path; only plain JSON objects enter the public package. Original search implementation is credited to Claude Code, software/data to DTU and OR-Tools. AI panel approval is not maintainer acceptance.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://gitlab.windenergy.dtu.dk/TOPFARM/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One.1_OSS is the single-substation benchmark variant of the built Hornsea One farm.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Codex (this run, verification, packaging), Claude Code (original neighborhood-search implementation), and three separately started AI review contexts.
