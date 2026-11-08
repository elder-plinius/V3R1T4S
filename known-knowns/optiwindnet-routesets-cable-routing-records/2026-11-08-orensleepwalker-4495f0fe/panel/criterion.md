# Criterion skeptic report: claim-h27 (optiwindnet-routesets-cable-routing-records)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Target claimed: the FULL success criterion, instance nodeset "Hornsea Two West", capacity 7, topology X = branched.
My scripts (none shipped by the claim): panel-h27/work-criterion/{q.py, ns.py, rebuild.py, indep.py, pk.py}. The decompressed SQLite copy was deleted after use.

## Release identity and latest-ness
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: sha256 c78c8f3c...e3a (matches bank entry); md5 85faffb2e13600b017f1b583b259edd7 (matches the file checksum in status/zenodo-latest.json).
- status/zenodo-latest.json: record 23537067, DOI 10.5281/zenodo.23537067, conceptrecid 20053478, published 2026-10-21, relations.version is_last = true, single file optiwindnet-routesets-r26.10-v4.sqlite.xz. So r26.10-v4 is the latest per the shipped snapshot. Residual: the snapshot carries no retrieval timestamp and I made no outward request, so latest-ness is as of the snapshot only.
- criterion.txt reproduces the bank entry's success criterion, statement, verification method, partial wins and pitfalls verbatim (checked by substring match against targets.json).

## Clause-by-clause
1. Nodeset name has no '!' prefix: nodeset row named exactly 'Hornsea Two West' exists (T=110, R=1, B=9, constraint_groups [10] = border only, 0 obstacles; substation is a border vertex). The many '!Hornsea Two West!...' rows are separate augmented nodesets. PASS.
2. Stored sets for the instance (all routeset rows with nodes_id = that nodeset and capacity 7; 4 rows, topologies only radial/branched, so all count for X = branched):
   - id 3689 baselines.hgs radial 217712.18494496983 m, feeders [16]
   - id 44466 MILP.pyomo.cplex radial 217712.18494496983 m, feeders [16] (tie for shortest)
   - id 98 MILP.pyomo.cplex branched 218384.3987299083 m, feeders [16] (bound 212127.21)
   - id 4178 baselines.lkh radial 234134.8716544603 m, feeders [16]
   Null-model check: I rebuilt all four via optiwindnet.db.storage.G_from_routeset from the DB rows; each recomputes to its stored length exactly and validates with 0 violations, so the comparison set is sound.
3. Topology: rebuilt G has topology BRANCHED; independent check on object/segments.json: 112 segments, 113 nodes (110 turbines + root + 2 detour clones), connected, edges = nodes - 1 (tree), turbine degree histogram {1:21, 2:84, 3:5}, 5 turbines branch. It is a genuine branched (not radial) set. PASS.
4. Strictly shorter by > 1e-6 relative than every stored set: claimed length 217395.35402025303 m. Margins: vs 3689/44466 by 316.8309 m (1.455e-3 rel), vs 98 by 989.0447 m (4.529e-3), vs 4178 by 16739.52 m (7.15e-2). PASS.
5. Feeders at each substation <= shortest stored set's feeders_per_root: claim [16] vs [16] (both tied shortest sets have [16]); 16 = ceil(110/7) is also the minimum possible. Root loads: one string of 5, fifteen of 7. PASS.
6. Same nodeset: G rebuilt from object/routeset-packed.json on the DB nodeset row (VertexC, border, landscape_angle taken from the DB, not from the claim) reproduces length 217395.35402025303 with no length_mismatch flag; G.pickle VertexC[:120] equals the DB VertexC blob exactly; pickle edge set equals the rebuild edge set; segments.json geometry equals the rebuild geometry. PASS.
7. validate_routeset (optiwindnet 0.3.2): [] for the G rebuilt from the packed record and [] for object/G.pickle (pickle opcodes scanned first: only networkx/numpy/bitarray/optiwindnet globals). Repacking with pack_G reproduces the packed edges exactly. PASS.
8. Border/obstacles (shapely, my own check): every segment covered by the border polygon (valid, 271.47 km2); the only boundary contacts are single points at the substation, which is itself a border vertex; all non-root segments are strictly interior; 0 obstacles in the nodeset. PASS.
9. Length = Euclidean segment sum: my sum over segments.json = 217395.35402025303, identical to the packed 'length' and to G.size(weight='length'); detours included (the two feeder detours bend at the coordinates of turbines 49 and 50, the same clone2prime [49,50] convention as stored best 3689/44466). Independent pairwise crossing test: 0 crossings/overlaps. PASS.

## Wording and metadata
- CLAIM.md wording matches the evidence (lengths, ids, the 3689/44466 tie, feeders, 0 obstacles, max degree 3) and explicitly disclaims optimality. No overstated sentence found.
- Misleading metadata in object/routeset-packed.json and object/G.pickle: creator 'MILP.ortools.cp_sat', runtime 2.735 s, misc.termination 'OPTIMAL', solver_details.strategy 'OPTIMAL', relgap 9.1e-12, bound 217262.67, method_options mip_gap 0.0 / time_limit 30. These describe only the last 30-s CP-SAT sub-solve with most links pinned (per the claim's own provenance), not the instance. Read as an instance record they would assert a proven optimum and an instance lower bound (217262.67) that are not established (the release's own best branched bound is 212127.21), and a runtime that omits the LNS. This does not affect any criterion clause, but nothing beyond the length/validity facts should be taken from those fields, and the record should not be ingested as-is.

## Partial wins
Not applicable: the full criterion is met; p1 (augmented '!' instance) and p2 (radial) do not describe this result.

confirmed_scope: For OptiWindNet RouteSets r26.10-v4 instance "Hornsea Two West" (no '!' prefix, 110 turbines, 1 substation, 0 obstacles) at capacity 7, the branched route set in object/ has a Euclidean segment-sum length of 217395.354 m, 316.831 m (0.146%) shorter than the shortest of the four stored route sets (radial ids 3689 and 44466, tied at 217712.185 m) and 989.045 m shorter than the only stored branched set (id 98), uses 16 feeders at the single substation (equal to the stored best's [16]), carries the release's nodeset unchanged, returns no violations from optiwindnet 0.3.2 validate_routeset, and stays inside the site border; no optimality is established (the 'OPTIMAL', relgap and bound fields in the packed object refer only to a final restricted sub-solve).

pass: true
