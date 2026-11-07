# REPRODUCE review: claim-ho5 (Hornsea One.1_OSS, capacity 5, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Scope: I read only files inside the claim folder (CLAIM.md, REPRODUCE.md, criterion.txt, object/*, status/zenodo-latest.json, references/*.sqlite.xz). The claim folder contains no author code. Work folder: panel-ho5/work-reproduce/ (scripts/ and *.out logs). The claim folder was not modified; no __pycache__ or .pyc exists in it after the run. All Python ran with -I and PYTHONDONTWRITEBYTECODE=1, and OMP_NUM_THREADS=1.

## Criterion implemented (verbatim, criterion.txt)

"For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!', and topology X (radial or branched), a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference data

- I copied references/optiwindnet-routesets-r26.10-v4.sqlite.xz to the work folder. Its sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches CLAIM.md and REPRODUCE.md. Its md5 is 85faffb2e13600b017f1b583b259edd7, which matches the Zenodo file checksum in status/zenodo-latest.json. Decompressing it with `xz -dk` gives a .sqlite file with sha256 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1. I read it through Python sqlite3 in read-only mode.
- Nodeset 'Hornsea One.1_OSS' has exactly one row. The name has no '!' prefix. T=174, R=1, B=25. VertexC is an .npy v3 blob with shape (200,2) float64. constraint_groups is [25], which means one border polygon and no obstacles. No other nodeset has an identical VertexC blob or an identical set of turbine coordinates.
- There are 4 stored routesets for this nodeset with capacity 5. I read all of them, not a sample:
  - id 44834: radial, MILP.pyomo.cplex, length 507652.11923526326, feeders_per_root [35]. This is the shortest stored set.
  - id 2798: branched, MILP.pyomo.cplex, length 507673.2763563798, feeders_per_root [35].
  - id 9633: radial, baselines.hgs, length 509207.2549157095, feeders_per_root [35].
  - id 8921: radial, baselines.lkh, length 527587.2778280491, feeders_per_root [35].
  All 4 are radial or branched, so all 4 count for X = branched.

## Own checker (scripts/own_checker.py: standard library only, exact rational arithmetic for geometry)

Results on object/segments.json, which holds 204 segments:
- Endpoints: every segment endpoint is bit-exactly equal to the VertexC coordinate of its node. For a clone node I used the coordinate of its prime from clone2prime in routeset-packed.json. Clones are numbered T+B onward; C=2 contour clones and D=28 detour clones. The primes are 27 turbines and 3 border vertices.
- Same network in two encodings: I decoded routeset-packed.json `edges` myself. Its edge set is identical to the (u,v) set in segments.json (204 = T+C+D). No pair is duplicated.
- Length: the recomputed sum of Euclidean segment lengths is 506483.64210765 with math.fsum and 506483.6421076504 with naive summation. This equals the length in segments.json, the packed length and the 506483.6421 in CLAIM.md. No segment has zero length.
- Forest structure:
  - Every turbine 0..173 and the root appear. No raw border index is used as a network node.
  - Every clone has degree 2, as an intermediate point on a path.
  - After contracting the clone chains there are exactly 174 links. 20 of them contain clones.
  - A search from the substation reaches all 174 turbines without finding a cycle, so each turbine is connected exactly once.
  - Subtree sizes off the feeders are 34 feeders of 5 turbines and 1 feeder of 4 (sum 174), so every subtree is at most 5.
  - The substation has 35 feeders, which matches the packed feeders_per_root [35].
  - Maximum turbine degree is 3 (6 turbines have degree 3), so the set is branched and not radial.
- Comparison with stored sets (strict, > 1e-6 relative): the claimed set is shorter than every stored set.
  - id 44834: 1168.4771 m shorter (0.230173% relative).
  - id 2798: 1189.6342 m shorter (0.234331% relative).
  - id 9633: 2723.6128 m shorter (0.534873% relative).
  - id 8921: 21103.6357 m shorter (4.000027% relative).
  - The feeder count [35] is at most the shortest stored set's [35]. 35 is also ceil(174/5), so it cannot be lower.
- Crossings: I tested all 20706 segment pairs with exact orientation tests.
  - No pair crosses properly.
  - No segment endpoint lies in the interior of another segment.
  - No segment passes through a turbine or substation in its interior.
  - 43 pairs of segments overlap along a collinear stretch of positive length. These are discussed under "Doubts" below.
- Border and obstacles: every segment lies inside the closed border polygon. I checked this exactly: no proper crossing with any border edge, and the midpoint of each sub-piece between boundary contacts is inside or on the border. All turbines and the substation are inside the border. There are no obstacles. Six segments have one endpoint on a border vertex: links to contour clones 199, 200 and 206 (pairs 43-206, 110-200, 167-200, 169-199, 172-199, 206-207). The cable touches the boundary at a vertex but never leaves the polygon.

## Official validator (scripts/official_validate.py: venv optiwindnet 0.3.2, networkx 3.7, shapely)

- Pickle safety: before loading object/G.pickle, I checked its globals with pickletools. I then loaded it with a restricted Unpickler. The only globals it uses are networkx graph and view classes, numpy, bitarray, optiwindnet.types.Topology and optiwindnet.types.FeederRoute.
- Rebuilt graph: I rebuilt G from object/routeset-packed.json plus the DB nodeset row, using optiwindnet's own db.storage.G_from_routeset. It reported no length mismatch.
- Both graphs pass: `validate_routeset(G)` returns [] for G.pickle and for the rebuilt G.
- Both graphs describe the claimed instance:
  - Total length is 506483.64210765.
  - capacity=5, T=174, R=1, B=25, C=2, D=28, topology=branched.
  - VertexC is identical to the DB blob, the border indices are identical to the DB, and there are no obstacles.
  - The root carries load 174 and has degree 35.
- All objects agree: G.pickle and the rebuilt G have the same edge set (204 edges), the same node coordinates through fnT and the same edge lengths. segments.json matches G.pickle edge for edge, and its coordinates match exactly.
- Shapely cross-check: the border polygon is valid and covers every segment. The minimum distance from a segment to the border boundary is 0 only for the 6 vertex-touching segments listed above; the next closest is 59.1 m.
- Control: the same pipeline rebuilds and validates all 4 stored sets (2798, 8921, 9633, 44834). Each gets 0 violations, and each rebuilt length equals its stored length. My standalone decoder (scripts/stored_compare.py) also reproduces every stored length to within 2e-10 m. This confirms that I decode the format correctly.

## Determinism

I ran all four scripts twice. The outputs were byte-identical, apart from the shell `time` line that was attached to the first own_checker run. Logs: own_checker.out, stored_compare.out, extra_checks.out, official_validate.out, and the r2_*.out copies of the second run.

## Doubts / notes

1. Collinear overlaps: 43 segment pairs overlap collinearly.
   - 39 of them are root-adjacent bundles: several feeders leave the substation along the same straight line to a turbine's location. One example is 8 segments from -1 to the point of turbine 90, through detour clones of 90. They continue from there.
   - 4 of them are detour clone chains running along a turbine-to-turbine link (22-91, 30-90, 91-90, 144-149).
   This is optiwindnet's PathFinder representation of detours, not a proper crossing. The stored sets use the same convention: id 44834 has 57 such overlaps, including the same 22-91, 30-90 and 91-90 cases, and 2798, 9633 and 8921 have 41, 69 and 115. The validator accepts all of them. Physically, these are cables sharing a corridor next to a turbine. The claim is held to the same standard as the reference sets.
2. Release status: status/zenodo-latest.json is the author's snapshot. It shows record 23537067 with is_last=true and the same file checksum. I did not query Zenodo live, as the brief allowed.
3. Bounds: the claimed straight-line objective (misc.objective 502825.92) is above the stored branched MILP bound for id 2798 (497716.26). This is consistent, not contradictory. The claim makes no claim of optimality.
4. Scope: the review covers this one frozen object only, identified by the sha256 values below.

Object hashes reviewed (sha256):
- object/G.pickle: d2faea3a42874a643c02fb3f27613f7209c9a699fb91448fc9917be1873f7c13
- object/routeset-packed.json: 84d6d76c0b1e5332bcc50726ceefd54ccb7421fcf1a5571fc151a517fc61b915
- object/segments.json: 8c9a42ed9fa8a3f8ea4e4f4024698772c344294cf8c18d523a9dc09272ba8278
- criterion.txt: 2e45c594742badc670f984796593dfb570abb6681190ee29c8bbd8ec7b666c63
- CLAIM.md: 742cce200538286422da5b1763d1204218d602cddd4a9cce9dee1f49d81b2e6a

Verdict: every property in the criterion holds for the frozen object, both in my own checker and in the official validator. The claimed value 506483.6421 m is reproduced exactly. The strict comparison holds against all 4 stored sets, and no mismatch, missing object or non-determinism was found.

pass: true
