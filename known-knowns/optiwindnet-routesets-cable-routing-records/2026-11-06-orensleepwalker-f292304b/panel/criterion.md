# Criterion skeptic report: claim-ho10 (OptiWindNet RouteSets, Hornsea One.1_OSS, capacity 10, X = branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

## Inputs and method
- I checked that `criterion.txt` matches the bank entry `optiwindnet-routesets-cable-routing-records` word for word. The success criterion, statement, verification method, p1, p2, pitfalls and status source all match the current `repo/bank/targets.json` and the pinned commit f3b19b47 (substring test: True).
- I wrote my own checkers before looking at any author code. The claim ships no code. My scripts are `check_own.py`, `check_validator.py` and `extra.py` in the panel's work-criterion folder. They ran under the optiwindnet 0.3.2 venv with `-I`, PYTHONDONTWRITEBYTECODE=1 and OMP_NUM_THREADS=1. I decompressed the release into the work folder, not the claim folder. No `__pycache__` exists in the claim folder.

## Clause-by-clause (literal)
| Clause | Finding | Verdict |
|---|---|---|
| Release r26.10-v4 identity | sha256 of `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, the same value as the bank. Its md5 85faffb2… matches the file checksum in `status/zenodo-latest.json`. The DB has 49,204 route sets, 12,814 nodesets and 13,954 (nodeset, capacity) instances, the same counts as the release description. | met |
| Latest version | `status/zenodo-latest.json` (record 23537067, relations.version is_last = true, modified 2026-10-21) says this is the latest version. Caveat: this is a frozen snapshot. I could not query Zenodo live because the task allowed no outward actions. | met as of snapshot |
| Nodeset has no '!' prefix | nodeset name "Hornsea One.1_OSS", T=174, R=1, B=25, constraint_groups [25], so a border and 0 obstacles | met |
| Topology X = branched | The claim's network is a capacitated tree (after contracting detour clones: 174 logical edges, all 175 nodes reachable from the root, no cycles). Turbine degree histogram: {1: 28, 2: 136, 3: 10}, so it is really branched. The packed record's topology field reads "branched". | met |
| Compared against every stored set of topology X or more restrictive | Capacity 10 has 4 stored sets, all radial or branched, so every one is in scope: 45802 radial CPLEX 336086.4654 m, 9644 radial HGS 340159.1949 m, 2804 branched CPLEX 342349.2849 m, 8928 radial LKH 350931.2830 m. No other nodeset has identical VertexC coordinates. | in scope = all 4 |
| Strictly shorter by more than 1e-6 relative | The claim is 332729.344314 m. Relative improvements: 9.989e-3 vs 45802, 2.184e-2 vs 9644, 2.810e-2 vs 2804, 5.187e-2 vs 8928. All exceed 1e-6. | met |
| Feeders at each substation <= the shortest stored set's feeders_per_root | Shortest stored set is 45802 with feeders [18]. The claim has 18 feeders (logical root degree 18, and G root degree 18). The stored branched set 2804 uses 19, but the cap correctly comes from the shortest set. | met |
| Same nodeset (turbines, substations, border, obstacles from VertexC) | The VertexC in `object/G.pickle` equals the DB blob exactly. Its optiwindnet coordinate fingerprint equals the DB nodeset digest, and the border index array is equal. All 180 segment endpoints in `object/segments.json` match VertexC exactly, with clones mapped through clone2prime [175, 184, 87, 94, 89, 95]. | met |
| validate_routeset, no violations | optiwindnet 0.3.2 `validate_routeset` returns [] on `object/G.pickle` and on G rebuilt with `G_from_routeset` from `object/routeset-packed.json` plus the DB nodeset. The edge sets of the pickle, the packed record and segments.json are identical. | met |
| Segments inside the border, outside obstacles | shapely: the border polygon (valid) covers all 180 segments, and none touches the boundary. There are 0 obstacles, so the obstacle clause holds trivially. | met |
| Length = sum of Euclidean segment lengths, and this is the compared value | My recomputed sum is 332729.344314 m. It equals the segments.json figure, the packed `length` and G.size(weight='length'). The stored lengths I recomputed from their own G also equal their DB values. | met |
| Feeder loads <= capacity 10 | Subtree loads: [6, 9, 9, then 10 x15], summing to 174 | met |

## Hidden quantifiers, stretched definitions, null models
- "Every stored route set ... of topology X or more restrictive": for branched this means all 4 stored sets. The claim beats all of them, not only the branched one (2804).
- Feeder cap: the claim takes it from the shortest stored set (18), not from the branched set's 19. No feeder relaxation is used.
- Shared feeder corridors: my own geometric check found 3 collinear overlaps. Root to 89 overlaps root to clone-of-89, and the same holds for 94 and 95. Each is a segmented feeder bending at a turbine's position while another feeder runs along the same corridor. This is not a loophole the claim invented. The same overlaps (often more of them) appear in all four stored sets, including 45802 and 2804, and the official validator accepts all of them. The criterion makes the validator the judge of crossings, so this is consistent with the benchmark's convention.
- Bounds sanity: the stored MILP bounds for capacity 10 are 322681.89 (radial run) and 322779.29 (branched run). Both are bounds on the straight-line objective. The claim's straight-line objective, 332665.74, sits above both, so it contradicts no certificate. The 3357 m gain is real, not a numerical artefact. A null-model start from 45802 (radial) is admissible as a branched solution, and the final object is genuinely branched (10 degree-3 turbines).
- The partial wins (p1, p2) are not needed. This is a full-criterion win on a non-'!' instance and is not subsumed by either partial.

## Wording in CLAIM.md
- The numbers check out: 332729.3443 m; 336086.4654 m (id 45802, radial, [18]); a difference of 3357.1211 m, which is 0.99889%, so "0.999%" is fine; branched best 342349.2849 m (id 2804, [19]); 174 turbines, 1 substation, 0 obstacles; maximum turbine degree 3.
- "Every segment lies ... outside every obstacle polygon" is true only trivially, because there are 0 obstacles. The claim does state "0 obstacle(s)".
- Overstatement risk in the shipped object, not in CLAIM.md's sentence: in `object/routeset-packed.json`, misc has creator "MILP.ortools.cp_sat", runtime 0.128917, bound 332665.74, relgap 2.06e-11, and termination/strategy "OPTIMAL". These describe the last large-neighbourhood sub-solve, in which most links were pinned. They are not a global optimality certificate, and the total runtime is not 0.13 s. CLAIM.md does say "Not claimed: optimality". Still, anyone who ingests this record into a RouteSets-style DB would record a false certified ~0% gap. Strip or relabel these fields before any outward use.
- Cosmetic: the packed handle "Hornsea_One_1_OSS" differs from the release's handle "hornsea_1". This is irrelevant to the criterion.

confirmed_scope: For OptiWindNet RouteSets release r26.10-v4 (sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, the latest Zenodo version per the frozen status/zenodo-latest.json snapshot), instance "Hornsea One.1_OSS" at capacity 10, the claim's branched route set (174 turbines, 1 substation, max turbine degree 3, 18 feeders, identical VertexC) has Euclidean-sum length 332729.3443 m, passes optiwindnet 0.3.2 validate_routeset with no violations, lies wholly inside the site border (no obstacles exist), and is strictly shorter by more than 1e-6 relative than all 4 stored route sets for that instance, the shortest being id 45802 (radial, MILP.pyomo.cplex, 336086.4654 m, 18 feeders), by 3357.1211 m (0.999%); no optimality is established, and the packed object's bound/relgap/OPTIMAL metadata refer only to a pinned sub-solve.

Verdict: the full success criterion is met for topology X = branched. Every clause holds literally under independent recomputation. The remaining caveats are the frozen latest-version snapshot and the misleading sub-solve metadata in the packed object. Neither breaks a clause.

pass: true
