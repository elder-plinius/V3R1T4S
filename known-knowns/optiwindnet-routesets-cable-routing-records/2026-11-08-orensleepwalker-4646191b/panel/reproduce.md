# REPRODUCE review: claim-la7 (London Array.1_OSS, capacity 7, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Reviewer role: REPRODUCE skeptic. I read only files in the claim folder (plus the installed optiwindnet 0.3.2 library source, to learn its storage format and validator). The claim folder contains no author code, so my checker could not have been influenced by it. Work files are in `panel-la7/work-reproduce/`: `my_checker.py` (stdlib only, exact rational geometry), `official_check.py` (optiwindnet), `shapely_check.py`, and their `*.out` logs, including a second run of each.

## Criterion implemented (quoted from criterion.txt)

> "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference data

- `references/optiwindnet-routesets-r26.10-v4.sqlite.xz`: I copied it to my work folder. sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a matches the claim. md5 85faffb2e13600b017f1b583b259edd7 and size 28464808 both match the file entry in `status/zenodo-latest.json`. I decompressed it with `xz -dk`; the decompressed sqlite has sha256 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1.
- `status/zenodo-latest.json` (as saved by the author) shows record 23537067, published 2026-10-21, with `relations.version[0].is_last = true`. I did not re-query Zenodo, so I cannot say whether a newer version appeared after the snapshot.
- Nodeset row `London Array.1_OSS` (the name has no '!' prefix): T=175, R=1, B=9. VertexC is a (185,2) float64 .npy blob, which I parsed with my own stdlib .npy reader. constraint_groups = [9] and constraint_vertices = 175..183, so the instance has one border polygon and no obstacles.
- I read every routeset row with this nodeset's digest and capacity 7. There are 4:
  - id 9627: 173966.441999 m, radial, feeders [25], baselines.hgs
  - id 45872: 173966.441999 m, radial, feeders [25], MILP.pyomo.cplex (ties with 9627)
  - id 2792: 174227.816277 m, branched, feeders [26], MILP.pyomo.cplex
  - id 8904: 188458.032615 m, radial, feeders [25], baselines.lkh
- No other rows exist under a London Array 1_OSS-like handle with a different nodes_id. All 4 stored sets load through optiwindnet's G_from_routeset. Their recomputed lengths equal the stored lengths, which confirms the stored `length` uses the same convention (Euclidean, detours included), and each passes validate_routeset with [].

## Own checker results (`my_checker.py`, exact Fraction arithmetic)

- **Endpoints:** all 180 segments in `object/segments.json` have endpoints that are bitwise equal to VertexC[prime(node)]. Clone nodes 184..188 are mapped through clone2prime [109,91,73,109,55]. Segment count 180 = T + C + D = 175 + 0 + 5.
- **Agreement between object files:** the edge multiset of `object/routeset-packed.json` (parent array) equals the edge multiset of segments.json. There are no duplicate segments.
- **Length:** the recomputed sum is 173753.9532429035 m, both with plain summation and with fsum. This equals segments.json `length_sum_euclid_m` and the packed `length`, and matches the claimed 173753.9532 m.
- **Topology:** every clone node has degree 2 and no border vertex is used as a cable node. After contracting the clones:
  - The node set is exactly the 175 turbines plus root -1, connected by 175 edges.
  - Every turbine is reachable from the root, there are no cycles, and each turbine has exactly one upstream link.
  - There are 25 feeders and every feeder subtree holds exactly 7 turbines, which sums to 175. No subtree exceeds 7.
  - The turbine degree histogram is {1: 27, 2: 146, 3: 2}, so the maximum degree is 3 and the network is branched, consistent with X = branched.
- **Crossings** (all 16110 segment pairs, exact orientation tests):
  - 0 proper crossings.
  - 0 cases of an endpoint lying on another segment's interior.
  - 0 cases of a segment interior passing through any VertexC point.
  - 6 collinear coincident runs, explained under "Doubtful points" below.
- **Containment:** every segment lies inside the closed border polygon. I tested this exactly by splitting each segment at its intersections with the border and running a point-in-polygon test at every cut point and every midpoint. No segment runs along the border, and every turbine and the root are strictly inside. A shapely 2.2.0 cross-check agrees: the border polygon covers every segment, and the minimum segment-to-border distance is 124.06 m. The instance has 0 obstacles, so the obstacle check is vacuous.
- **Comparison with stored sets:** X = branched, so the object is compared against all stored sets, radial and branched. The object is shorter than every one of the 4 stored sets. The shortest stored set is 173966.441999 m (ids 9627 and 45872, both with feeders [25]). The improvement over it is 212.488756 m, or 1.2214e-3 relative, well above 1e-6. The feeder cap is the shortest stored set's feeders_per_root, [25], and the object uses [25]. The shortest stored branched set is id 2792 at 174227.8163 m with feeders [26]. All of these figures match CLAIM.md.

## Official validator (`official_check.py`, optiwindnet 0.3.2)

- `validate_routeset(G.pickle)` returns [].
- I rebuilt a graph from `object/routeset-packed.json`, using the DB nodeset through L_from_nodeset and TerseLinks.to_routeset. `validate_routeset` on it also returns [].
- G.pickle and the rebuilt graph describe the same network:
  - identical node and edge sets, fnT, link loads and feeders per root [25]
  - equal lengths: 173753.9532429035 m in both
  - `pack_G(G.pickle)` reproduces the packed edges and clone2prime exactly
- G.pickle carries the same nodeset as the database: its VertexC is exactly equal to the DB blob, its border equals the DB border, it has no obstacles, and T, R, B and capacity = 7 all match.
- `find_geometric_crossings(include_touches=True)` reports only 5 items, all of kind 'touch'.

## Determinism

I ran each checker twice. Both outputs were byte-identical between runs (`*.run2.out` vs `*.out`). I left no __pycache__ in the claim folder (PYTHONDONTWRITEBYTECODE=1, python -I) and confirmed the claim folder is still read-only and unchanged.

## Doubtful points / notes (none invalidates the claim)

1. **Coincident cable runs.** `my_checker.out` prints two FAIL lines, which I resolved as follows. This is the first.
   - The exact test finds 6 collinear overlapping segment pairs. In each pair, a detour clone route shares a straight corridor with another cable:
     - root–55 with root–188 (188 is a clone of 55)
     - root–73 with root–186 (clone of 73)
     - root–109 with root–184 and with root–187 (both clones of 109), and root–184 with root–187
     - 73–91 with 185–186 (clones of 91 and 73)
   - So 3 cables leave the substation along the same line toward turbine 109, and the detours bend at turbine positions.
   - This is optiwindnet's standard detour/shared-corridor convention. The official crossing finder classifies these runs as 'touch', not as violations. Every stored set uses the same convention: 9627 and 45872 have 7 such overlaps, 2792 has 4 and 8904 has 30.
   - These runs are not proper crossings and the validator accepts them. I therefore do not count them as a failure. A reader who wants physically separated cable corridors should know they exist.
2. **Handle label.** This is the second FAIL line. The packed and G handle is 'London_Array_1_OSS', while the stored rows use 'london_1'. The handle is only a label. The nodeset identity (VertexC, border, digest join) matches exactly.
3. **Misleading solver metadata.** The object's misc/graph metadata (`bound` = `objective` = 173707.43, `relgap` 0.0, `termination` OPTIMAL, `warmstart` baselines.hgs, runtime 13.5 s) describes the last CP-SAT sub-solve of the large-neighbourhood search, not a global bound. 173707.43 is the model's straight-line objective, and it is lower than the detoured length. Anyone reading `misc` could take it as a certified optimality bound. CLAIM.md explicitly does not claim optimality.
4. **Zenodo snapshot.** The "latest version" status comes from the saved snapshot only, and I made no network check.
5. **What is and is not verified.** The provenance (the LNS procedure) is not verified and is not needed. The object itself is verified directly.

## Verdict

Every property in the criterion holds for the frozen object, checked by my own exact checker, by shapely, and by the official validator on both object representations:

- recomputed length 173753.9532 m, below every stored set (radial or branched) by more than 1e-6 relative
- feeders 25 against a cap of 25
- valid capacitated branched forest, with every turbine connected once and every subtree at most 7
- no proper crossings
- every segment inside the border, with no obstacles in the instance
- endpoints exactly at VertexC coordinates
- same nodeset as the database
- both object files describe the same network

pass: true
