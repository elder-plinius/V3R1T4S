# OptiWindNet RouteSets: a shorter cable network for Cazzaro-2022G-210.solid.1_OSS, capacity 6

## What
For release r26.10-v4 instance Cazzaro-2022G-210.solid.1_OSS (a non-'!' literature-site variant) at capacity 6, the radial route set in claim/object has recomputed Euclidean length 396403.7269 m with 36 substation feeders, which is strictly shorter by more than 1e-6 relative than both stored route sets for the instance (radial best id 25098 at 401553.2842 m, 36 feeders; branched best id 25278 at 399738.0433 m, 36 feeders), passes validate_routeset with no violations, uses the instance's exact VertexC and border, and lies within the closed site border (10 segments run along border edges, none outside), meeting the full success criterion for X = radial (and for X = branched under "radial counts for branched").

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance under the bank's full success criterion. Three fresh AI-agent contexts passed (panel/). This is a computational result; no independent human or benchmark-maintainer review has occurred.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; about 20 seconds with internet access on the first run (it downloads the hash-pinned 28.5 MB release file from Zenodo once and caches it in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validator (validate_routeset) also returns no violations; it needs third-party packages and is run in the panel reports (rebuild the graph from object/routeset-packed.json with optiwindnet's own storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---:|---|
| **This object** | radial | **396403.7269** | 36 | own HGS-CVRP run (see how-we-built-it/) |
| stored id 25278 | branched | 399738.0433 | 36 | CPLEX via optiwindnet MILP, 6-h limit reached; bound 384837.74 |
| stored id 25098 | radial | 401553.2842 | 36 | HGS-CVRP baseline, ~120 s |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (status re-checked 2026-11-06T00:20Z: still the latest version). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new method (the same HGS-CVRP heuristic run longer with another seed), nothing about other instances, and no built-wind-farm claim: the site is a literature benchmark layout (Cazzaro & Pisinger 2022) in DTU's '.solid' border, single-substation variant, eligible as a non-'!' instance. Disclosed interpretive points: ten segments (five cables) run along border edges where the border bends inward (inside the closed site region; these detours were produced by optiwindnet's own PathFinder); several cables share corridors collinearly, as in the stored sets, with no crossings (accepted by the official validator). Novelty coverage gaps: the base paper's tables could not be opened (HTTP 403); its own G-210 instance differs (3 substations, capacity 7, balanced), so it holds no comparable value.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder and the HGS-CVRP wrapper used here.
- Davide Cazzaro and David Pisinger: the G-210 layout ("Balanced cable routing for offshore wind farms with obstacles", Networks 80 (2022) 386-406).
- Thibaut Vidal: HGS-CVRP.
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
