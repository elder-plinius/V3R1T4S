# REPRODUCE review: Hornsea Two West, capacity 9, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read: the files in the claim folder (CLAIM.md, REPRODUCE.md, criterion.txt, object/segments.json, object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz, status/zenodo-latest.json). The claim folder contains no author code, so the "write your own checker first" step had nothing to come before. I opened the installed optiwindnet 0.3.2 library only to call `G_from_routeset`, `pack_G` and `validate_routeset`. The claim folder was not modified and has no `__pycache__` (checked with find). All Python ran with `-I`, `PYTHONDONTWRITEBYTECODE=1` and `OMP_NUM_THREADS=1`.

Work files (in panel/work-reproduce/): `mycheck.py`, `mycheck.out1`, `mycheck.out2` (my own checker), `runval.py`, `runval.out`, `runval.out2` (official validator and object comparison), `shapely_check.py`, `shapely.out`, `db/rs.sqlite` (my own decompressed copy).

## 1. Reference database
- The sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz is `c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a`, which matches CLAIM.md, REPRODUCE.md and criterion.txt. Its md5 `85faffb2e13600b017f1b583b259edd7` matches the file checksum in status/zenodo-latest.json (record 23537067, `is_last: true` in that snapshot). I had no network access, so I could not re-query Zenodo for a newer version. The status file is a frozen snapshot.
- I decompressed my own copy with `xz -dc`. It is 79,986,688 bytes, with sha256 `9aa8214c…45e1`. I opened it read-only with Python sqlite3.
- Nodeset `Hornsea Two West` (exactly one row; no '!' prefix): T=110, R=1, B=9. VertexC is an (120,2) float64 .npy array. `constraint_groups=[10]`, so there is one group: the border `[110,111,112,113,-1,114,…,118]`. The substation vertex -1 is a corner of the border polygon. There are 0 obstacles.

## 2. Own checker (mycheck.py), written from the criterion
Criterion implemented (quoted from criterion.txt): "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

The checker uses only stdlib and numpy. All geometric predicates use exact rational arithmetic (`fractions.Fraction`) on the stored float coordinates. Results from object/segments.json (112 segments):
- **Endpoints.** Every turbine and substation endpoint is bitwise equal to its VertexC row. The 2 clones (119, 120) sit exactly at the VertexC points of turbines 49 and 46, which equals the packed `clone2prime=[49,46]`. C+D = 2.
- **Length.** The fsum of hypot over all segments is **191786.95446995908 m**. This equals the CLAIM value 191786.9545, the packed `length` and the segments.json field.
- **Structure.** No duplicate segments and no self-loops. Each clone is a degree-2 bend point. After contracting the clones there are 110 logical links, all between turbines and the substation, with no cycles. Every turbine is reached exactly once from root -1, so this is a tree. The 13 feeder subtree sizes are [5,6,9,9,9,9,9,9,9,9,9,9,9], all ≤ 9 and summing to 110. Feeders at the substation: [13]. Maximum turbine degree is 3, so the network is branched.
- **Crossings.** I checked all 6216 segment pairs exhaustively (exact arithmetic). There are 0 proper crossings and 0 T-touches (a vertex lying in the interior of another segment). My checker flagged one item, a full-length collinear overlap, which I discuss under "Doubtful / notes" (first item).
- **Containment.** The border polygon is simple. I split each segment at every intersection with the boundary and classified every sub-piece and endpoint by exact point-in-polygon. All 112 segments lie in the closed border polygon. The only boundary contact is at the substation vertex (13 feeders), and no piece runs along the border. The shapely 2.2.0 cross-check agrees: `covers` holds for 112/112 and `contains` holds for 112/112. There are no obstacles, so nothing to test there.
- **Determinism.** Two runs produced byte-identical output.

## 3. Comparison with every stored route set (all rows, not a sample)
The database stores 4 route sets for nodes_id = this nodeset and capacity = 9:

| id | length (m) | feeders | topology | creator |
|---|---|---|---|---|
| 4305 | 192886.72928393926 | [13] | radial | baselines.hgs |
| 44553 | 192886.72928393926 | [13] | radial | MILP.pyomo.cplex |
| 100 | 193222.83416271958 | [13] | branched | MILP.pyomo.cplex |
| 4181 | 194384.99910752499 | [13] | radial | baselines.lkh |

- Both topologies count against a branched claim, so all 4 rows apply. The claim is shorter than every one of them by more than 1e-6 relative.
- The margin against the shortest (4305 and 44553, tied) is 1099.7748 m, which is 0.5702% (relative 5.70e-3). These figures match CLAIM.md.
- The shortest stored branched set is id 100 at 193222.8342 m, which also matches CLAIM.md.
- Feeder cap: the shortest stored set's feeders_per_root is [13], and both tied rows agree. The object uses [13], which is ≤ 13.
- All rows have T=110 and R=1.

## 4. Official validator (runval.py, optiwindnet 0.3.2)
- **object/G.pickle.** Before loading, I listed the pickle's globals with pickletools: only networkx, numpy, bitarray and optiwindnet classes. `validate_routeset(G) -> []`. The graph has 112 edges, length 191786.95446995908, capacity 9, topology branched. VertexC is bitwise equal to the database VertexC, and the border is equal to the database constraint vertices.
- **Graph rebuilt from object/routeset-packed.json.** I rebuilt it with `optiwindnet.db.storage.G_from_routeset`, using the database nodeset row. `validate_routeset -> []`. The length is 191786.95446995908, with no `length_mismatch_on_db_read` flag.
- **Same network across the three objects.**
  - G.pickle and the rebuilt graph have identical edge sets, identical endpoint coordinates and equal lengths.
  - segments.json has the same edge set and coordinates as G.pickle.
  - `pack_G(G.pickle)` reproduces the packed `edges`, `clone2prime`, `feeders_per_root` and `length` exactly.
- **Determinism.** Two validator runs produced byte-identical output.

## Doubtful / notes
1. **Collinear corridor overlap.** The segments (-1,46) and (-1,120) are the same straight line from the substation to turbine 46's position. Clone 120 is a detour bend placed at turbine 46, and from there the cable goes on to turbine 47. So the feeder for 47 shares the substation–46 corridor and passes through turbine 46's coordinate.
   - This is not a proper crossing, and the official validator accepts it.
   - I do not count it as a failure. The same pair (46,-1)/(120,-1) appears in the stored reference sets 4305 and 44553 for this exact instance. Across all 43 stored route sets of this nodeset, 33 contain such collinear corridor overlaps and 38 use clones of turbines. Every one of them validates as [].
   - This is the standard optiwindnet detour representation, so the claim is held to the same standard as the reference.
   - Apart from this overlap, node 46's other links all lie on one side of the route through clone 120. The route through clone 119, at turbine 49, does not separate 49's links.
2. **Metadata in routeset-packed.json is misleading if filed as is.** `misc.bound=191680.09`, `relgap=7.3e-12`, `termination=OPTIMAL`, `runtime=0.28 s` and `creator=MILP.ortools.cp_sat` describe only the last CP-SAT sub-solve, in which most links were pinned. They are not a global bound or certificate; the database's stored branched MILP bound for this instance is 186907.20. The `handle` is `Hornsea_Two_West`, while the database uses `hornsea2w`. None of this affects the criterion, but it should not be presented as an optimality certificate. CLAIM.md itself does not claim optimality.
3. **Release status.** Whether this is still the latest release was confirmed only against the frozen status/zenodo-latest.json snapshot, not live.

No mismatch, missing object or non-determinism was found for any property the criterion requires.

pass: true
