# OptiWindNet RouteSets: a shorter branched cable network for Hornsea One.1_OSS, capacity 12

## What
For release r26.10-v4 (sha256 c78c8f3c...e3a, the latest Zenodo version per status/zenodo-latest.json), instance "Hornsea One.1_OSS" with capacity 12, the branched route set in object/ has a recomputed Euclidean length of 307472.1191 m, detours included, which is shorter than all four stored route sets of that instance (best: radial id 45373, 309220.7062 m, by 0.5655%) while using 15 feeders (cap 15), passing validate_routeset with no violations, and lying entirely inside the site border (the nodeset has no obstacles); no optimality is established, and the object's misc "OPTIMAL/relgap 0/bound" fields refer only to a restricted sub-solve.

Status: CONFIRMED_SOLUTION for this one (nodeset, capacity) instance, topology branched, under the bank's full success criterion (compared with every stored route set, since radial counts for branched). Three fresh AI-agent contexts passed (panel/). Computational result; no human or maintainer review yet.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. Python 3 standard library only; seconds with internet access on the first run (downloads the hash-pinned 28.5 MB release from Zenodo once, cached in the OS temporary directory; no downloaded code is executed). The official optiwindnet 0.3.2 validate_routeset also returns no violations (run in the panel reports; rebuild the graph from object/routeset-packed.json with optiwindnet's storage functions).

## Compared to
| Route set | Topology | Length (m) | Feeders | Source |
|---|---|---:|---|---|
| **This object** | branched | **307472.1191** | see panel | own CP-SAT fix-and-optimise search |
| stored id 45373 | radial | 309220.7062 | [15] | MILP.pyomo.cplex |
| stored id 2805 | branched | 311308.1399 | [16] | MILP.pyomo.cplex |
| stored id 9645 | radial | 312888.3176 | [15] | baselines.hgs |
| stored id 8929 | radial | 318718.8555 | [15] | baselines.lkh |

Release: OptiWindNet RouteSets r26.10-v4, https://doi.org/10.5281/zenodo.23537067 (re-checked by the novelty reviewer at 2026-11-07T09:06:25Z; see panel/novelty.md). See the-record-we-beat/record.md.

## Not claimed
No optimality, no new solver (a standard MIP-based large-neighbourhood search around OR-Tools CP-SAT, as wrapped by optiwindnet), nothing about other instances. Seeded from stored set id 45373 (CPLEX, radial). Disclosed: the packed object's misc fields (bound, relgap 0, OPTIMAL, runtime, creator, warmstart labels) describe only the last pinned 30-s CP-SAT window sub-solve and must not be read as an instance certificate (the release's branched bound for this instance is 297640.80 m); the packed handle string differs cosmetically from the database handle; one bend sits on a border vertex, as in the stored sets. Seeded from stored set id 45373 (CPLEX, radial).
Additional disclosure: G.pickle (not shipped in the package) may contain a local file path; the package ships only segments.json and routeset-packed.json.

## Credits
- Mauricio Souza de Alencar, Tuhfe Gocmen and Nicolaos A. Cutululis (DTU Wind): OptiWindNet and the RouteSets dataset (preprint wes-2026-124; Zenodo 10.5281/zenodo.23537067; https://github.com/DTUWindEnergy/OptiWindNet), including the validator, PathFinder, the stored CPLEX route sets and the CP-SAT model wrapper.
- Site: Hornsea One offshore wind farm (UK North Sea, built; 174 turbines), the release's single-offshore-substation variant '.1_OSS', layout as distributed with OptiWindNet.
- Google OR-Tools (CP-SAT solver).
- OrenSleepwalker, with Claude Code (search, verification, packaging) and three separately started AI review contexts.
