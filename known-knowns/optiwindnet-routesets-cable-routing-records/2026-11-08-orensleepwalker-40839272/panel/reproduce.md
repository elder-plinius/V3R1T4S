# REPRODUCE review: claim-la9 (London Array.1_OSS, capacity 9, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Reviewer role: REPRODUCE skeptic. Inputs read: only files in the claim folder (CLAIM.md, REPRODUCE.md, criterion.txt, object/*, references/*.xz, status/zenodo-latest.json). There is no author code in the claim folder; my checker was written from criterion.txt before anything else. To rebuild a graph from the packed JSON I looked at the signatures and source of two functions in the installed official library (optiwindnet 0.3.2 `optiwindnet.db.G_from_routeset` and `L_from_nodeset`). That is the official tool, not author code.
Work folder: panel-la9/work-reproduce/ (scripts my_checker.py, official_validate.py, control_overlaps.py; outputs *.out). Env: PYTHONDONTWRITEBYTECODE=1, python -I, OMP_NUM_THREADS=1.

## Criterion implemented (quoted from criterion.txt)
"For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!', and topology X (radial or branched), a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference database
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches the claim. Its md5 85faffb2e13600b017f1b583b259edd7 matches the file checksum in status/zenodo-latest.json (record 23537067, published 2026-10-21, latest-version endpoint). I decompressed my own copy to work-reproduce/db/routesets.sqlite (sha256 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1). It has 49,204 routesets and 12,814 nodesets, which matches the release description. The hash did not change after the library opened the database.
- Nodeset 'London Array.1_OSS' (no '!' prefix): T=175, R=1, B=9, VertexC is a (185,2) float64 .npy array, constraint_groups [9]. That means one border polygon (vertices 175-183) and 0 obstacles.
- Every stored routeset with this nodeset and capacity 9 (4 rows):
  - 44577 radial MILP.pyomo.cplex 154359.16037331126, feeders [20]
  - 9629 radial baselines.hgs 154359.16037331134, feeders [20]
  - 2794 branched MILP.pyomo.cplex 154403.53504258036, feeders [20] (branched MILP bound 151435.06)
  - 8917 radial baselines.lkh 158074.8692118387, feeders [20]

## Independent checker (my_checker.py, built on object/segments.json and the DB nodeset)
- Endpoints: every segment endpoint is bitwise equal to the VertexC coordinate of its node. Root -1 is the last row of VertexC. The detour clones 184-187 resolve to their prime nodes [73, 91, 73, 140] through clone2prime in routeset-packed.json.
- Length: math.fsum of the Euclidean lengths of 179 segments = 153957.9888674163 m. This equals segments.json length_sum_euclid_m, the packed length, the CLAIM.md value, and G.size(weight='length') for both graphs.
- Structure: 180 nodes (175 turbines, 1 root, 4 pass-through clones of degree 2) and 179 edges. Union-find finds no cycle and 1 component with exactly one root. Every turbine 0-174 is present exactly once. It is a tree, so it is a valid branched forest.
- Capacity: there are 20 feeders at the root. The turbine counts of the feeder subtrees are [7,8,8,8, 9 x16], sum 175, all <= 9. Maximum turbine degree in the graph is 3, which is consistent with branched topology as claimed.
- Crossings: I tested all 15,931 segment pairs with exact rational orientation tests. Result: 0 proper crossings, 0 T-junctions, and 0 segments passing through a turbine or substation position that is not one of their endpoints. There are 4 collinear overlaps, all identical detour corridors: (-1,73)/(-1,184)/(-1,186) and (91,184)/(185,186). See the notes below.
- Containment: the border polygon is valid (area 1.224e8 m^2). Shapely `covers` holds for every segment. My own check (ray-cast on every endpoint plus exact crossing tests against every border edge) also passes. The closest any segment comes to the border is 124.06 m. There are no obstacles to test.
- Comparison: the relative margin (L_stored - L)/L_stored is 2.5989e-3 vs 44577, 2.5989e-3 vs 9629, 2.8856e-3 vs 2794 and 2.6044e-2 vs 8917. All are > 1e-6, so the set is strictly better than every stored set of any topology, and radial is included. The improvement over the shortest stored set is 401.1715 m (0.2599%). The two shortest stored sets (44577 and 9629, a tie within 8e-11 m) both have feeders_per_root [20]. The object uses [20], which is <= the cap.
- Result: PASS, 0 failures.

## Official validator (official_validate.py)
- object/G.pickle: before loading it I listed the pickle's opcodes and strings with pickletools. They reference only networkx, numpy, bitarray and optiwindnet.types globals. validate_routeset(G) -> [].
- I rebuilt a graph from object/routeset-packed.json with optiwindnet.db.G_from_routeset, using the DB NodeSet row and the packed edges, clone2prime, C, D and misc. validate_routeset -> []. No length_mismatch_on_db_read flag was raised.
- Control: stored set 44577, loaded from the DB the same way, also gives [].
- Same network: the edge sets of G.pickle, the rebuilt graph and segments.json are identical (179 edges each). VertexC (185x2) is bitwise equal between G.pickle and the DB nodeset. fnT and border are equal. All per-edge lengths and loads are equal (0 differences). Both graphs report topology=branched, capacity=9, T=175, R=1, B=9, D=4.
- Determinism: I ran both scripts three times. The outputs were byte-identical each time (sha256 8216ffaf... for my checker, 9e454314... for the official run).

## Notes and doubts (none changes the verdict)
1. Overlapping corridors. The detour path for feeder -1 -> 184(pos 73) -> 91, the second detour -1 -> 186(pos 73) -> 185(pos 91) -> 108, and the plain edge -1 -> 73 share the substation-to-turbine-73 line. Two cables also share the 73-to-91 line. This is how optiwindnet routes around obstacles: it adds clones of existing nodes. The stored best set 44577 has exactly the same 4 identical corridors (clones [73,91,73]), and validate_routeset accepts both. The detour lengths are counted in the total, so this does not make the claimed length too low.
2. The packed misc fields bound=153949.51, relgap=2.9e-11, termination OPTIMAL, creator MILP.ortools.cp_sat and runtime 4.95 s describe only the last restricted CP-SAT sub-solve, in which most links were pinned. They are not a bound for the instance. Read naively they look like a certificate of optimality. The claim does not assert optimality. The instance's stored branched MILP bound (151435.06, id 2794) is below the object's straight-line objective (153949.51), which is consistent.
3. Release freshness: the "latest version" evidence is the saved snapshot status/zenodo-latest.json (revision 4, id 23537067). I did not query Zenodo live.
4. The feeder cap is unambiguous: all 4 stored sets have [20].

All checks pass: the length I recomputed equals the claimed value, the tree satisfies the capacity limit and stays inside the border, the feeder count is within the cap, there are no proper crossings, the official validator returns [] on both object files, the three object files describe the same network, and the set is strictly shorter than every stored set by more than 1e-6 relative. No __pycache__ exists in the claim folder and the hashes of its files are unchanged.

pass: true
