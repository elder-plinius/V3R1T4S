# Criterion skeptic report: optiwindnet-routesets-cable-routing-records, Hornsea One.1_OSS, capacity 9, X = branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Scripts (my own, written before seeing any author code; the claim ships none): ../panel/work-criterion/q.py (DB rows), check.py (independent geometry/topology/length checker on object/segments.json with numpy+shapely), val.py (official validator on the claim and on all four stored sets, plus overlap null-check). The decompressed SQLite copy was deleted after use. Nothing was written to the claim folder; no __pycache__ there.

## Criterion text
criterion.txt quotes the bank entry's success_criterion, both partial_wins, statement, verification_method, status_source and all three pitfalls verbatim (substring-checked against repo/bank/targets.json).

## Release identity
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches criterion), md5 85faffb2e13600b017f1b583b259edd7 (matches the Zenodo file checksum in status/zenodo-latest.json).
- status/zenodo-latest.json: record 23537067, version relation is_last = true, state published, modified 2026-10-21. The snapshot carries no fetch timestamp and I made no live call, so "latest" holds as of whenever that snapshot was taken.

## Clause-by-clause
1. Nodeset 'Hornsea One.1_OSS' has no '!' prefix. T=174, R=1, B=25, constraint_groups [25] (border only, 0 obstacles). PASS.
2. Topology: object misc.topology = branched; the forest has 9 turbines of degree 3 (max 3), so it is branched, not radial. PASS.
3. Stored sets for (nodeset, capacity 9): exactly 4 rows: 9638 baselines.hgs radial 353604.67462 [20]; 45718 MILP.pyomo.cplex radial 353604.67462 [20]; 2802 MILP.pyomo.cplex branched 358653.04772 [20]; 8925 baselines.lkh radial 372903.67104 [20]. All are radial or branched, so all count. The claim's length 351584.0138106073 is below each; the smallest relative margin is 0.0057145 (vs 9638/45718), far above 1e-6. Absolute margin 2020.6608 m. PASS.
4. Feeders: the claim uses 20 at its single substation; both tied shortest sets (9638 and 45718) have feeders_per_root [20]. 20 <= 20. PASS.
5. Same nodeset: every segment endpoint in object/segments.json equals VertexC from the DB blob exactly (max diff 0), with clones 199-208 mapped via clone2prime (3 border-vertex contour clones, 7 turbine detour clones). The G.pickle VertexC is array-equal to the DB blob, its border equals the DB border, it has no obstacles, name/T/R/B/capacity match. segments.json edge set == G.pickle edge set == G unpacked from routeset-packed.json (184 edges). PASS.
6. My own topology check: one tree rooted at -1 containing all 174 turbines (184 edges, 185 nodes, acyclic); clone nodes all degree 2 (pass-through); feeder subtree loads [4, 8, 9 x 18], max 9 = capacity, sum 174. No proper crossings; no segment passes through a non-endpoint turbine. PASS.
7. optiwindnet.validating.validate_routeset (0.3.2): [] for G.pickle and for G rebuilt from routeset-packed.json via G_from_routeset. PASS.
8. Border/obstacles: every one of the 184 segments is covered by the border polygon (valid polygon); no obstacles exist. PASS.
9. Length: sum of Euclidean segment lengths = 351584.0138106073 m, identical to segments.json, the packed 'length', and G.size(weight='length'); this is the value I compared. PASS.

## Null-model and definition checks
- There are 6 collinear overlaps between feeder segments (root->turbine and root->detour clone at the same turbine position). The same PathFinder detour convention appears in every stored set (6, 23, 6, 6 overlaps in 2802, 8925, 9638, 45718), and the validator accepts all of them, so it is not a stretched definition peculiar to the claim. Overlapping lengths are counted twice in both the claim and the stored lengths.
- The four stored sets all pass the same validator with lengths equal to their Euclidean sums, so the comparison is like-for-like.
- The stored best branched MILP bound is 341271.12 (from 2802). The claim's straight-line objective 351371.33 lies above it, so nothing contradicts a stored certified bound.
- The feeder cap is not relaxed: the claim uses exactly the shortest set's 20.

## Wording and metadata
- CLAIM.md's numbers check out: 2020.6608 m, 0.571 %, ids, creators, feeders, degree 3, 0 obstacles. "every stored route set for that instance of any topology" is accurate here because only radial and branched sets are stored. Provenance (CP-SAT LNS, seeds 7 and 8 converging) is unverified and is not evidence.
- Misleading metadata in object/routeset-packed.json and object/G.pickle: misc.bound 351371.33, relgap 3.8e-12, termination "OPTIMAL", solver_details.strategy "OPTIMAL", runtime 0.0768 s, creator and warmstart "MILP.ortools.cp_sat", method_options time_limit 30 / mip_gap 0. All of these describe only the last restricted CP-SAT sub-solve, which had most links pinned. They do not describe the full instance. If ingested into RouteSets, they would read as a certified ~0 % optimality gap for Hornsea One.1_OSS capacity 9, which CLAIM.md itself disclaims ("Not claimed: optimality"). The proven gap against the best stored bound is about 2.9 % ((351584.01-341271.12)/351584.01, on lengths). These fields must be stripped or relabelled before any submission. This does not affect the criterion, which judges length, validity and geometry only.
- Cosmetic: the handle is Hornsea_One_1_OSS where the DB uses hornsea_1, and the pickle's method_options embeds a local absolute funfile path.

## Verdict
Every clause of the full success criterion holds literally for X = branched. This is a genuine full win, not one of the partial wins and not subsumed by a stored set. The only reservations are the misleading optimality metadata inside the object and the fact that "latest release" rests on the shipped status snapshot rather than a live check.

confirmed_scope: For OptiWindNet RouteSets r26.10-v4 (sqlite.xz sha256 c78c8f3c…e3a, Zenodo record 23537067, marked latest in the shipped status snapshot), instance 'Hornsea One.1_OSS' with capacity 9, the branched route set in object/ has Euclidean length 351584.0138 m with 20 feeders, passes validate_routeset with no violations, lies inside the border (no obstacles exist), and is shorter by 2020.66 m (0.571 %) than the shortest of the four stored radial-or-branched sets (ids 9638 and 45718, 353604.6746 m, 20 feeders); its internal bound/relgap/OPTIMAL metadata covers only a restricted sub-solve and certifies nothing about the instance.

pass: true
