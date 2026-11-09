# REPRODUCE review: Hornsea One.1_OSS, capacity 9, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read: CLAIM.md, REPRODUCE.md, criterion.txt, object/segments.json, object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz, status/zenodo-latest.json. Nothing outside the claim folder was read apart from the installed optiwindnet 0.3.2 package source (storage.py and validating.py, to call G_from_routeset and validate_routeset correctly). Scripts and outputs are in panel/work-reproduce/ (check_segments.py, validate.py, extra.py, db_read.py and their .out files). All runs used `python -I`, PYTHONDONTWRITEBYTECODE=1 and OMP_NUM_THREADS=1. No __pycache__ was created in the claim folder.

## Reference data
- sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches the claim. md5 85faffb2e13600b017f1b583b259edd7 matches the file checksum in status/zenodo-latest.json (record 23537067, published 2026-10-21). I decompressed my own copy (sha256 of the .sqlite is 9aa8214c...45e1).
- Nodeset 'Hornsea One.1_OSS' (no '!' prefix): one row, T=174, R=1, B=25. VertexC is (200,2) float64. constraint_groups=[25], so there is a border and no obstacles.
- Routesets for this nodeset with capacity 9: 4 rows, all T=174 and R=1.
  - 9638 baselines.hgs, radial, 353604.67462349357, feeders [20]
  - 45718 MILP.pyomo.cplex, radial, 353604.67462349357, feeders [20]
  - 2802 MILP.pyomo.cplex, branched, 358653.04772392014, feeders [20]
  - 8925 baselines.lkh, radial, 372903.67104268767, feeders [20]

## Own checker (check_segments.py), written from criterion.txt before running any author code
Criterion implemented (verbatim excerpt): "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). ... every route segment must stay inside the site border and outside every obstacle polygon ... and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

Results on object/segments.json (184 segments):
- Endpoints: every endpoint exactly equals (float equality) a row of the DB VertexC. Each label maps to that row: turbines and border vertices map to themselves, the root (-1) maps to VertexC[-1], and clones 199..208 map through clone2prime [175,186,184,88,109,102,80,88,95,87].
- Length: the sum of math.dist over segments is 351584.0138106073. This equals the value in segments.json and the packed 'length'.
- Structure: no self-loops and no duplicate edges. All 174 turbines are present. Edges = nodes - components, so there are no cycles. There is one component, and it contains the single root. Every clone has degree 2 (pass-through). There are 20 feeders at the root. Each feeder subtree holds 1..9 turbines and none exceeds 9. The maximum turbine degree is 3, so the set is branched.
- Crossings: I tested all 16,836 segment pairs with exact rational orientation tests. There are 0 proper crossings, and no endpoint lies in the interior of another segment.
- Containment: I split each segment at its intersections with the border edges and classified the pieces exactly against the polygon. 0 segments leave the border. There are no obstacles to test. As an independent second check, shapely Polygon(border).covers(segment) holds for all 184 segments.
- Comparison: the claimed set is shorter than every stored set by more than 1e-6 relative.
  - 9638: 0.571446% shorter
  - 45718: 0.571446% shorter
  - 2802 (branched): 1.970995% shorter
  - 8925: 5.717202% shorter
- The margin over the shortest stored set is 2020.6608 m. Feeders [20] are within the cap [20] set by the shortest stored set (9638/45718 tie, both [20]). All stored sets have feeders [20].

## Official validator
- object/G.pickle: validate_routeset returns []. It has topology BRANCHED, capacity 9, C=3, D=7, has_loads=True, and maximum feeder load 9. Its VertexC equals the DB blob exactly, and its border indices equal constraint_vertices. Edge-weight length and the Euclidean recomputation via fnT both give 351584.0138106073.
- Graph rebuilt from object/routeset-packed.json: I passed the packed fields plus the DB nodeset row to optiwindnet.db.storage.G_from_routeset (method metadata was stubbed). validate_routeset returns [] and length_mismatch_on_db_read is not set.
- Consistency across the three objects:
  - The G.pickle edge set equals the packed edge set (184 edges), and fnT and VertexC are identical.
  - The segments.json edge set equals the G.pickle edge set, and every segment's coordinates equal VertexC[fnT[u]] and VertexC[fnT[v]].
  - pack_G(G.pickle) reproduces every field of routeset-packed.json.
- Determinism: I ran both scripts twice and got byte-identical outputs.

## Doubts / notes
- Detour clones 202..208 have turbines as primes (88, 109, 102, 80, 88, 95, 87). For example, feeder -1 -> 205 -> 75 passes through turbine 80's coordinate. This is optiwindnet's PathFinder detour convention: the stored best sets 9638 and 45718 use exactly the same detour primes. The validator accepts it, and segments meeting there share only endpoints. Under the criterion I do not treat it as a defect.
- packed misc reports a CP-SAT sub-solve 'OPTIMAL' with an objective of 351371.33. That is the straight-line model objective of the final sub-solve, not a global bound, and it is not claimed as such.
- Zenodo latest-version status rests on the bundled status/zenodo-latest.json (record 23537067). I could not re-check it online (no network).

pass: true
