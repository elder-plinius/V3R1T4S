# Criterion skeptic report

context: Target `optiwindnet-routesets-cable-routing-records`; claim = FULL success criterion, instance (nodeset "Hornsea One.1_OSS", capacity 4), topology X = branched, release r26.10-v4. I read only the claim folder and the bank entry; all checks below were run with my own scripts in `panel/work-criterion/` (`own_check.py`, `bundle_check.py`, `official.py`, outputs `*.out`), python `-I`, `PYTHONDONTWRITEBYTECODE=1`. Claim folder hashes unchanged after my run; no `__pycache__` in it.

confirmed_scope: For the OptiWindNet RouteSets r26.10-v4 instance (nodeset "Hornsea One.1_OSS", 174 turbines, 1 substation, no obstacles; capacity 4), the route set in `object/routeset-packed.json` / `object/segments.json` is a valid branched network on the identical nodeset with 45 substation feeders and total Euclidean length 589790.5176 m, which is 1360.8220 m (0.2302 %) shorter than the shortest of the four route sets stored for that instance (id 42471, radial, 591151.3395 m, 45 feeders), passes optiwindnet 0.3.2 `validate_routeset` with no violations and stays inside the site border; it is not shown to be optimal and does not improve on the 44-feeder stored sets' feeder count.

## Clause-by-clause (literal)

| Clause | Result | Evidence (mine) |
|---|---|---|
| Release identity | met | `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` sha256 c78c8f3c...e3a (= bank entry), md5 85faffb2... (= file checksum in `status/zenodo-latest.json`); uncompressed md5 5ad6bf04...9016 (= release table in the record description). 49,204 route sets, 12,814 nodesets. |
| Latest-ness | met as far as the snapshot shows | `status/zenodo-latest.json`: record 23537067, `relations.version[0].is_last = true`, single file, published 2026-10-21. The snapshot carries no fetch timestamp of its own and I had no network access, so "latest on the claim date" rests on the author's snapshot. |
| Nodeset name has no '!' | met | name is exactly `Hornsea One.1_OSS`; one nodeset row with this name; no other nodeset has the same VertexC blob. |
| Topology X = branched | met | tree rooted at the substation, 206 segments on 207 nodes, acyclic, all 174 turbines reached; max turbine degree 3 (2 turbines of degree 3), so branched and not radial (the validator rejects it when declared radial: "radial subtrees must be simple paths"). |
| Capacity | met | 45 subtrees, largest holds 4 turbines, sum 174. |
| Strictly shorter than EVERY stored set of topology branched or radial, > 1e-6 relative | met | The instance has exactly 4 stored sets (all radial or branched, so all count): id 42471 radial CPLEX 591151.3395 m [45]; 9601 radial HGS 595070.4239 m [44]; 2787 branched CPLEX 596799.9297 m [45]; 8898 radial LKH 604020.3250 m [44]. Claim 589790.5176 m; relative margins 2.30e-3, 8.87e-3, 1.17e-2, 2.36e-2. My decoder reproduces all four stored `length` values from their edges to < 1e-9 m, so like is compared with like (detours included). |
| Feeders at each substation <= shortest such stored set's feeders_per_root | met, with equality | shortest such stored set = id 42471, feeders [45]; claim has 45 segments at the substation. Note: 44 is the minimum (ceil(174/4)) and two stored (longer) sets use 44; the criterion's literal cap is 45, so this is compliant but is not an improvement at 44 feeders. |
| Same nodeset | met | all 412 segment endpoints in `object/segments.json` are bitwise equal to VertexC entries (turbines, substation, and detour points mapped through `clone2prime` to 2 border vertices and turbine positions); all turbines and the substation are present; edge set of `segments.json` == edge set decoded from `routeset-packed.json`. |
| `validate_routeset` no violations | met (on rebuilt graph) | G rebuilt from `object/routeset-packed.json` + the DB nodeset via `G_from_routeset`: `[]`. Controls: the 4 stored sets also give `[]`; 102 tree-preserving random link swaps of the claim were all flagged. I did NOT load `object/G.pickle` (unpickling was blocked in my sandbox); static opcode inspection shows only networkx/numpy/bitarray/optiwindnet globals. The pickle is therefore unverified by me and is not needed for the verdict. |
| Inside border / outside obstacles | met | border = 25-vertex polygon (407.35 km2), 0 obstacles (`constraint_groups = [25]`). shapely `covers` is true for all 206 segments exactly (0 m excursion); independent orientation test: 0 proper crossings with border edges. |
| Length = Euclidean sum, the value compared | met | fsum over raw coordinates in `segments.json`: 589790.517568 m; same from packed edges; equals `length` in the packed object. |
| Crossings (own check) | met | 0 proper segment crossings, 0 touching of non-shared points; own bundled-corridor test (root paths sharing points/sub-chains, feeders passing over a turbine): 0 crossings, 0 branch splits; same test gives 0 on the 4 stored sets. |

## Hidden quantifiers, stretched definitions, null models

- "Every stored set" is only 4 sets and the binding one is a radial CPLEX run stopped at a 0.5 % MIP gap; the win is real but modest (0.23 %). It is larger than the release's detour-recomputation noise (up to 0.13 %) and is a genuine topology change: 18 of 174 turbine links differ from id 42471.
- Convention inherited from the benchmark, not a stretch by the author: feeders share collinear corridors and pass over turbine positions via detour nodes (40 coincident segment pairs and 30 feeder-over-turbine passes in the claim; the stored sets have 52-131 and 33-50). The criterion delegates this to `validate_routeset`, which accepts it.
- Not optimal: my straight-line recomputation of the claim's links is 588554.28 m against the release's best branched bound 587091.72 m (about 0.25 % above; indicative only). `CLAIM.md` correctly disclaims optimality.
- Not subsumed: no stored set of the instance is as short; no partial win is needed (p1/p2 do not apply: real-site name, branched).
- Wording in `CLAIM.md`: numbers (589790.5176, 591151.3395, 1360.8220 m, 0.230 %, id 42471/2787, feeders [45], max degree 3) all reproduce. No overstatement found.

## Misleading metadata in `object/routeset-packed.json` (does not affect the criterion, must not be propagated)

- `misc.termination: "OPTIMAL"`, `misc.relgap: 0.0`, `misc.bound == misc.objective == 588695.96`, `solver_details.strategy: "OPTIMAL"`: these describe the last 30 s windowed sub-solve with most links pinned, not the instance. Read as stored-format fields they assert a proven-optimal solution, which is false (release bound 587091.72). `misc.objective` also does not equal my straight-line sum of the final links (588554.28).
- `creator: "MILP.ortools.cp_sat"`, `runtime: 22.02`: the route set is the product of a multi-hour fix-and-optimise search started from stored id 42471, not a 22 s CP-SAT solve.
- `handle: "Hornsea_One_1_OSS"` differs from the release's handle for this nodeset (`hornsea_1`).
- `feeders_lb: 44` is correct and makes plain that 45 is not the minimum.

## Limits of this review

- `object/G.pickle` not loaded (see above).
- No network: latest-ness is taken from the author's `status/zenodo-latest.json` only.
- My bundled-corridor crossing test has no negative control that isolates a corridor-only crossing; the mutation controls were caught (by both my test and the official validator), mostly as ordinary crossings.

pass: true
