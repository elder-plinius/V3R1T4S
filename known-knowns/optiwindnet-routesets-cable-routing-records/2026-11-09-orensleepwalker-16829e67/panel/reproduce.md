# REPRODUCE review: Race Bank.1_OSS, capacity 3, X = radial

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

I read only files inside the claim folder. My scripts and outputs are in panel/work-reproduce/: dbread.py, mycheck.py, official.py and neg.py, plus the outputs mycheck_out.json, official_out.txt and o45770.json. The claim folder has no author code. I wrote my checker from criterion.txt and did not look at any author implementation. I ran Python with `-I` and `PYTHONDONTWRITEBYTECODE=1`. No `__pycache__` was created in the claim folder, and its files still have their original mtimes and read-only permissions.

## Criterion implemented (quoted from criterion.txt)
"For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!', and topology X (radial or branched), a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference database
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: the sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches. The md5 is 85faffb2e13600b017f1b583b259edd7, which matches the md5 checksum in status/zenodo-latest.json for the same file. The size is 28464808 bytes, which also matches.
- I decompressed my own copy to work-reproduce/db/rs.sqlite (sha256 9aa8214c...45e1, 79,986,688 bytes) and read it with Python sqlite3 in read-only mode.
- I did not query Zenodo, because there is no network. status/zenodo-latest.json is a snapshot showing record 23537067, revision 4, `published`, and `is_last: true`.
- The nodeset row 'Race Bank.1_OSS' (no '!' prefix) has T=91, R=1, B=12, VertexC (104,2) float64, constraint_groups [12] and constraint_vertices 91..102. That means the border is one ring and there are 0 obstacles.
- Every routeset row with nodes_id = this digest and capacity = 3. There are 4 rows, all with handle `race_1`, and no other nodeset carries a Race Bank handle at capacity 3:

| id | topology | creator | length (m) | feeders_per_root |
|---|---|---|---|---|
| 45770 | radial | MILP.pyomo.cplex (min_plus1, segmented) | 155036.8792851718 | [31] |
| 9504 | radial | baselines.hgs | 155036.87928517183 | [31] |
| 8812 | radial | baselines.lkh | 155172.6133007654 | [31] |
| 2743 | branched | MILP.pyomo.cplex (unlimited, segmented) | 156071.65277105573 | [31] |

## Independent checker (mycheck.py, on object/segments.json)
- **Endpoints.** All 214 endpoints lie exactly, by float equality, on VertexC rows. Turbines 0..90 sit at their own rows and the root -1 sits at VertexC[-1]. The 16 bend nodes (ids 103..118) are 15 detour points at turbine coordinates and 1 contour point at border vertex 93. Each node has a single consistent coordinate.
- **Length.** The fsum of the 107 Euclidean segment lengths is 153796.94115396673 m. This equals the stored `length_sum_euclid_m`, the packed `length` and G.size(weight='length'). There are no zero-length segments.
- **Topology.** I contracted the 16 bend nodes; each has degree exactly 2. The result is 91 turbine-level edges over 92 nodes. A BFS from the root reaches all 91 turbines, so the network is connected and has no cycle, and each turbine has exactly one parent.
  - The maximum turbine degree is 2, so the network is RADIAL. No feeder turbine has more than one child.
  - There are 31 feeders at the substation.
  - String sizes are 30×3 and 1×1, so every string is at most the capacity of 3, and the sizes sum to 91.
- **Crossings.** I tested all segment pairs in exact rational arithmetic (Fraction) on the float coordinates.
  - Proper crossings: 0.
  - An endpoint lying in the interior of another segment: 0.
  - Partial collinear overlaps: 0.
  - Identical segments: 8 pairs. Examples are root→41 drawn the same as root→109 and root→113, and 17→110 drawn the same as 106→107. These are shared cable corridors produced by optiwindnet detours. They are the benchmark's convention: the stored set 45770 has 43 such identical pairs, and the validator accepts both.
- **Border and obstacles.** The border polygon is valid. Shapely `covers` holds for all 107 segments. An exact check finds no proper crossing between any segment and any border edge. Segments 65 and 70 touch the ring at border vertex 93; this is the contour bend 45→103→38, which is allowed. There are no obstacles.
- **Comparison.** 153796.94115 is lower than every stored radial set:
  - id 45770 by 1239.9381 m (0.7998%)
  - id 9504 by 1239.9381 m (0.7998%)
  - id 8812 by 1375.6721 m (0.8865%)

  All of these exceed the 1e-6 relative threshold.
- **Feeder cap.** The shortest stored radial set is 45770, with feeders_per_root [31]. The object uses 31, so the cap holds (31 = ceil(91/3) is also the minimum possible).
- **Branched comparison.** The set is also shorter than the stored branched set 2743, by 2274.7116 m (1.457%). 45770 is the shortest stored set of any topology, so the claim also holds for X = branched.
- **Negative controls.** Each of these tampered inputs was correctly rejected:
  - one coordinate shifted by 1e-9
  - one segment dropped
  - a chord added between turbines 0 and 90 (3 proper crossings detected)
  - stored set 45770 run through the checker (rejected only for its length and the comparison)
- **Determinism.** Two runs gave byte-identical output (sha256 9df7ffc6...35d4bf).

## Official validator (official.py, optiwindnet 0.3.2)
- **object/G.pickle.** validate_routeset returns []. Its VertexC is array-equal to the DB blob, its border is [91..102], it has no obstacles, the length is 153796.94115396673 and the feeders are [31].
- **Rebuilt from object/routeset-packed.json.** I rebuilt the graph with optiwindnet.db.storage.G_from_routeset, using the DB NodeSet row as `nodes`. validate_routeset returns []. There is no length_mismatch_on_db_read and the length is 153796.94115396673.
- **Packed graph relabelled as radial.** The packed misc says topology 'branched', so the validator's default run only checks the branched rules. I relabelled the rebuilt graph's topology as RADIAL and validate_routeset still returns []. As a control, stored branched set 2743 relabelled as radial is rejected with "radial subtrees must be simple paths", so the radial check does real work.
- **Same network.** G.pickle, the packed rebuild and segments.json have identical coordinate edge multisets (107 edges). The node-labelled edge sets of the pickle and the packed rebuild are equal, and so are their fnT arrays. The u/v labels in segments.json equal the pickle's node labels.
- **Stored sets.** All 4 stored sets also validate to [] and their lengths reproduce from the DB. 45770, 9504 and 8812 have maximum turbine degree 2; 2743 has 3.

## Doubtful points (none changes the verdict)
1. **Topology labels.** The topology label inside both object files (packed misc.topology and G.graph['topology']) is 'branched', and method_options.topology is BRANCHED. The network itself is radial, as CLAIM.md says. criterion.txt's header line says "Claimed: ... topology X = branched" while CLAIM.md says X = radial. The object satisfies both; for branched it beats all 4 stored sets.
2. **Solver metadata.** The object's solver metadata describes only the last 30 s CP-SAT sub-solve with most links pinned, not the instance as a whole. It records creator MILP.ortools.cp_sat, runtime 1.55 s, termination OPTIMAL, relgap 0.0, and bound = objective = 153313.9147. If this were stored as is, it would wrongly suggest a certified optimum for the instance, so it should not be read as a bound.
3. **Bound inconsistency in the release.** The object's straight-line objective of 153313.91 is below the "bound" of stored branched MILP 2743 (153480.92, feeder_limit unlimited). It is above the radial bound of 45770 (153293.23). The radial bound being lower than the branched bound already shows that the release's bounds come from different models or link sets, so they are indicative only. This is not a criterion issue, because the criterion compares stored lengths.
4. **Handle.** The packed handle is "Race_Bank_1_OSS"; the DB handle is "race_1". The nodeset name and VertexC match exactly.
5. **Detours.** Detour bends lie at other turbines' coordinates and some feeder corridors are drawn identically. This is the same PathFinder convention the stored sets use, and the validator accepts it.
6. **Latest Zenodo version.** I could not check this live (no network). I relied on status/zenodo-latest.json.

## Verdict
I reproduced every property and the claimed value from the saved files and my own copy of the database. The value is 153796.9412 m, which is 1239.9381 m (0.800%) below the best stored radial set (id 45770, and the hash-equal-length 9504). The network is a valid radial capacity-3 forest with 31 feeders (cap 31), no crossings, and every segment inside the border. The validator returns [] on both object files, and both files describe the same network. I found no mismatches, missing objects or non-determinism.

pass: true
