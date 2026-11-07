# REPRODUCE review: Hornsea One.1_OSS, capacity 12, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs I read: CLAIM.md, REPRODUCE.md, criterion.txt, status/zenodo-latest.json, object/segments.json,
object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz.
I read nothing else in the workspace. The claim folder contains no author code, so the checker is
my own, written from the criterion text. I ran Python with -I and PYTHONDONTWRITEBYTECODE=1. The claim
folder is unchanged and has no __pycache__.
Claim file sha256: object/G.pickle 0b95493a…0b60, object/routeset-packed.json 1bce7f80…4465,
object/segments.json ad2d0ad1…37f8.

## Criterion implemented (verbatim, from criterion.txt)
"For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!',
and topology X (radial or branched), a route set of topology X with strictly smaller total length than
every stored route set for that instance of topology X or more restrictive (radial counts for branched),
by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route
set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles
from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations
(topology, capacity, loads, crossings), every route segment must stay inside the site border and outside
every obstacle polygon (checked separately, since the validator does not test this), and its length,
recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference data
- I copied references/optiwindnet-routesets-r26.10-v4.sqlite.xz into my work folder and decompressed the copy there (xz -dk).
- .xz sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a: matches CLAIM.md and REPRODUCE.md.
- .xz md5 85faffb2e13600b017f1b583b259edd7: matches the file checksum in status/zenodo-latest.json.
- The uncompressed .sqlite md5 is 5ad6bf0449dcbd9939f1ae03bee19016. This matches the 26.10-v4 release table in the status record.
- Nodeset 'Hornsea One.1_OSS' (name is UNIQUE-indexed; exactly one row; no '!' prefix): T=174, R=1, B=25,
  VertexC = .npy <f8 (200,2) (turbines 0..173, border 174..198, root last), constraint_groups [25]
  (border only, 0 obstacles).
- I read all 4 stored routesets for this nodeset with capacity 12, selected by nodes_id = the nodeset digest:
  - 45373: radial, MILP.pyomo.cplex, length 309220.7062386733, feeders [15]
  - 2805: branched, MILP.pyomo.cplex, length 311308.1398986437, feeders [16]
  - 9645: radial, baselines.hgs, length 312888.3175614034, feeders [15]
  - 8929: radial, baselines.lkh, length 318718.8555241551, feeders [15]
  The shortest stored set is 45373, so the feeder cap is [15]. All four rebuild through optiwindnet's
  G_from_routeset to their stored lengths, and validate_routeset returns [] for each (control run).

## Own checker (work-reproduce/mycheck.py, stdlib only, exact rational geometry)
- Endpoints: all 350 segment endpoints are bit-identical to rows of the VertexC blob. Each turbine or root
  label maps to its own row. The only other label, 199, has degree 2 and sits on border vertex row 175
  (a contour bend on route 39–199–115).
- Length: math.fsum of Euclidean segment lengths = 307472.1190876585 m. This equals segments.json
  length_sum_euclid_m, the packed length, and the shapely sum.
- Topology: after contracting the bend there are 174 logical links over 174 turbines plus 1 root. A
  traversal from the root reaches every turbine exactly once and finds no cycle, so the network is a tree.
  - The root has 15 feeders. Their subtree sizes are 10, 10, 11, 11 and eleven of 12 (sum 174), so the
    maximum load is 12 <= capacity 12.
  - The maximum turbine degree is 3, so the network is branched.
- Crossings: I checked all 15,225 segment pairs exactly. There are 0 proper crossings, 0 touches away from
  a shared endpoint and 0 collinear overlaps. No segment passes through any other VertexC point.
- Containment: I split each segment at its contacts with the border edges and classified every piece and
  every contact point exactly. 0 segments leave the border. There are no obstacles. The only boundary
  contact is the bend endpoint at border vertex 175. This is the optiwindnet contour convention; stored
  sets 45373 and 8929 also carry contour nodes (C=3). Shapely Polygon(border).covers(segment) is True
  for all 175 segments.
- Comparison with all 4 stored sets (all count for branched). The relative margin is (stored − 307472.1191) / stored:
  - 45373: 1748.587151 m, 5.654819e-3
  - 2805: 3836.020811 m, 1.232226e-2
  - 9645: 5416.198474 m, 1.731033e-2
  - 8929: 11246.736436 m, 3.528733e-2
  Every margin is well above the 1e-6 threshold. The object uses feeders [15], which is within the cap [15].
- Negative controls: I fed the checker three altered copies of segments.json. It flagged each one:
  - a straight 39–115 link replacing the bend: "leaves the border"
  - a feeder rewired to another turbine: capacity exceeded, crossings
  - one coordinate perturbed by 1e-9: not an instance coordinate

## Official validator (work-reproduce/official.py, optiwindnet 0.3.2 venv)
- I listed the global references in object/G.pickle before loading it. They are only networkx, numpy,
  optiwindnet and bitarray types.
- G.pickle metadata matches the nodeset: name 'Hornsea One.1_OSS', T/R/B as in the database, capacity 12,
  topology branched. VertexC is bit-identical to the database blob, the border indices are equal, and
  there are no obstacles.
- validate_routeset(G.pickle) returned [].
- I rebuilt a graph from object/routeset-packed.json plus the database nodeset with
  optiwindnet.db.storage.G_from_routeset (method fields stubbed). The rebuild gave no
  length_mismatch_on_db_read, and validate_routeset on it returned [].
- G.pickle, the rebuilt graph and segments.json describe the same network:
  - Each has 175 edges, and the edge sets are identical both by node labels and by endpoint coordinates.
  - Clone 199 maps to vertex 175 (fnT).
  - All three give length 307472.1190876585 and feeders [15].
- Validator controls:
  - G.pickle with capacity set to 11 is rejected ('κ = 11, max_load = 12').
  - G.pickle with one feeder rewired produces 33 violations.

## Determinism
Both scripts were run three times and produced byte-identical outputs.

## Doubtful points (none blocking)
- status/zenodo-latest.json is a saved snapshot (it marks 23537067 as the latest version, is_last true).
  I had no network access, so I did not re-check whether a newer Zenodo version exists.
- The packed handle 'Hornsea_One_1_OSS' differs from the stored handle 'hornsea_1'. This is cosmetic:
  the nodeset identity was verified through the name, the coordinates and the border.
- The packed misc fields relgap 0.0 and OPTIMAL describe the last sub-solve, not global optimality.
  CLAIM.md correctly does not claim optimality. The claimed length is above the stored MILP bounds for
  this instance (radial 300763.46, branched 297640.80), so there is no contradiction with them.
- The bend touches the border at a vertex. Under a boundary-inclusive reading of "inside the border"
  (shapely covers) this is allowed, and stored routesets use the same convention.
- No exhaustive-search claim is made. Every segment, every segment pair and every stored routeset for
  the instance was checked, so nothing here is a sample.

All numbers in CLAIM.md reproduce: 307472.1191, 309220.7062 (id 45373, radial, [15]), 1748.5872 m
(0.565%), 311308.1399 (id 2805, branched, [16]), feeders [15], maximum degree 3.

pass: true
