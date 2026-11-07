# REPRODUCE review: claim-ho7 (Hornsea One.1_OSS, capacity 7, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read: CLAIM.md, REPRODUCE.md, criterion.txt, object/segments.json, object/routeset-packed.json, object/G.pickle (in the optiwindnet venv only), references/optiwindnet-routesets-r26.10-v4.sqlite.xz, status/zenodo-latest.json. Nothing else in the workspace was read. Scripts and outputs are in work-reproduce/ (mycheck.py, packed_geom.py, official.py and their .out files).

## Reference database
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches the claim and the criterion). md5 85faffb2e13600b017f1b583b259edd7 matches the md5 in status/zenodo-latest.json for that file (28,464,808 bytes).
- My decompressed copy (work-reproduce/db/rs.sqlite) has sha256 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1. I opened it read-only.
- Nodeset 'Hornsea One.1_OSS' (no '!' prefix, unique name index): T=174, R=1, B=25. constraint_groups=[25], so there is one border group of vertices 174..198 and no obstacles. VertexC is a .npy v3 blob, '<f8', shape (200,2) = T+B+R.
- status/zenodo-latest.json is a saved snapshot of versions/latest. It shows record 23537067 (published 2026-10-21), so it is the same release. I did not re-fetch it (no network).

## Own checker (work-reproduce/mycheck.py, stdlib only, written before using any optiwindnet code)
Criterion implemented (verbatim excerpt): "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). ... every route segment must stay inside the site border and outside every obstacle polygon ..., and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

Results:
- Endpoints: each of the 195 segment endpoints exactly equals (bit for bit) the VertexC coordinate of its node. Roots are negative indices, clones 199..219 map to their prime through clone2prime. No raw border index is used as a node.
- Length: math.fsum of Euclidean segment lengths = 407209.0155536414 m. This matches segments.json, packed `length` 407209.01555364137 and the CLAIM value 407209.0156.
- Structure: 196 nodes (174 turbines, the root and all 21 clones C=2+D=19) and 195 edges. The graph is connected, so it is a spanning tree with no cycles. Every clone has degree 2 (pass-through only). After contracting the clone chains, the turbine-level tree has 174 edges. Turbine degree histogram: {1:30, 2:140, 3:4}, so the maximum degree is 3 and the topology is branched.
- Capacity: the root has 26 feeders. Subtree sizes are 3, 5, 5 and 23 subtrees of 7, summing to 174. Every turbine is connected exactly once, and every subtree has <= 7 turbines.
- Crossings: I tested all 18,915 segment pairs with exact rational orientation tests. There are 0 proper crossings and 0 T-touches (an endpoint lying inside another segment). No segment passes through a turbine or substation point in its interior.
- Border: I tested the segments against the closed border polygon with exact arithmetic, including endpoint tests, edge-crossing tests and midpoint tests between contact points. 0 segments leave the border. 4 endpoints lie on the border boundary, at border-vertex contour clones. Obstacles: there are none in this nodeset, so that check is vacuous. Shapely (`border.covers`) agrees: 0 segments not covered. The border polygon is valid.
- Stored route sets for (nodeset, capacity 7): there are exactly 4, and all were read.
  - id 45791 radial MILP.pyomo.cplex: 408102.5795348772 m, feeders [26]. It is the shortest stored set. Diff 893.5640 m (0.218956%).
  - id 2801 branched MILP.pyomo.cplex: 411304.2675846244 m, feeders [25]. Diff 4095.2520 m (0.996%).
  - id 9637 radial baselines.hgs: 414178.6097 m, feeders [25]. Diff 1.68%.
  - id 8924 radial baselines.lkh: 419780.0637 m, feeders [25]. Diff 2.99%.

  The claim beats all four by far more than 1e-6 relative. Every stored set is radial or branched, so all of them count for X = branched. Feeder cap: 26 <= 26, the feeders_per_root of the shortest stored set (id 45791).
- Determinism: a second run gave byte-identical output.

## Packed and segment objects
- work-reproduce/packed_geom.py decodes the packed `edges`/`clone2prime` with stdlib only. The decoded node-pair set equals the segments.json node-pair set, and the geometry is bit-identical.
- Using the same decoding, I recomputed all 4 stored routesets' Euclidean lengths and they equal the stored `length` (diff 0 or 1.7e-10). This confirms that stored lengths include detours and use the same measure as the claim.

## Official validator (optiwindnet 0.3.2, work-reproduce/official.py)
- object/G.pickle: validate_routeset returns []. Its length is 407209.01555364137. Graph data: T=174, R=1, B=25, C=2, D=19, capacity 7, topology branched, root degree 26, has_loads True. Its VertexC equals the DB blob, its border equals the DB constraint vertices, it has no obstacles, and its name is 'Hornsea One.1_OSS'.
- I rebuilt G from object/routeset-packed.json with optiwindnet.db.storage.G_from_routeset, using the DB nodeset row and a stub method record. validate_routeset returns [] and there is no length_mismatch_on_db_read.
- Consistency: the edge geometry is the same in G.pickle, the packed rebuild and segments.json, and the pickle and the rebuild have the same node-pair edge set.
- Positive control: stored id 45791 rebuilt the same way gives [].
- Negative control: I re-attached the feeder turbine of a 3-turbine subtree to a 7-turbine subtree. The validator reports 10 violations, including "max_load = 10" and crossings, so it is not trivially permissive.
- A second run gave byte-identical output.

## Doubtful points
1. Collinear overlaps. The object has 21 segment pairs that are collinear and overlap with positive length. For example, root->89 and root->clone(89) at 202, 206 and 216 are geometrically identical segments, which means several feeders run in the same corridor. This is how optiwindnet represents PathFinder detours through clones. Stored set 45791 has the same count (21), and 2801, 9637 and 8924 have 20, 31 and 14. The official validator, which checks overlaps, accepts it. It is not a proper crossing under the criterion, so I accept it, but it is a convention reviewers should know about.
2. G.pickle is a pickle, so loading it can run arbitrary code. I loaded it only inside the optiwindnet venv. The independent stdlib checks used segments.json and the packed JSON, and all three objects agree.
3. The Zenodo "latest" status is a saved snapshot, not re-fetched here.
4. Packed misc fields (strategy OPTIMAL, relgap 1.7e-11, runtime 0.82 s) describe only the last CP-SAT sub-solve with the other links pinned. They are not a global bound, and the claim does not assert optimality. They are irrelevant to the criterion.

None of these is a mismatch. Every property and the claimed value reproduce exactly from the saved files.

pass: true
