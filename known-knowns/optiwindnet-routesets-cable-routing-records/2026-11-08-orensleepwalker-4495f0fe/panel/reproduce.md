# REPRODUCE review: claim-h27 (Hornsea Two West, capacity 7, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read: CLAIM.md, REPRODUCE.md, criterion.txt, object/segments.json, object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz, status/zenodo-latest.json. The claim folder contains no author code. I wrote nothing there and it holds no __pycache__ (all runs used PYTHONDONTWRITEBYTECODE=1, python -I, OMP_NUM_THREADS=1).
Work files are in panel-h27/work-reproduce/: scripts/own_checker.py, scripts/official.py, scripts/controls.py, own_checker.out, own_checker.run2.out, official.out, controls.out.

## 1. Reference database
- I copied references/optiwindnet-routesets-r26.10-v4.sqlite.xz into my work folder and ran `xz -dk` on the copy.
- The .xz sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches CLAIM.md and the criterion.
- The .xz md5 is 85faffb2e13600b017f1b583b259edd7, which matches the files[] checksum in status/zenodo-latest.json.
- The md5 of the uncompressed .sqlite is 5ad6bf0449dcbd9939f1ae03bee19016, which matches the release table in the Zenodo description for 26.10-v4.
- The routeset table has 49,204 rows, as the statement says.
- Nodeset 'Hornsea Two West' (no '!' prefix) is a single row: T=110, R=1, B=9, VertexC (120,2) float64, constraint_groups [10] (a border and no obstacles).
- The border's constraint_vertices are [110,111,112,113,-1,114,115,116,117,118]. The substation is itself a border vertex.

## 2. Own checker (written before reading any author code; it does not import optiwindnet)
Criterion implemented (quoted from criterion.txt): "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

Results of scripts/own_checker.py on object/segments.json (112 segments):

**Endpoints**
- Every endpoint equals a VertexC row bit for bit, and each turbine or root label sits at its own coordinate.
- Labels 119 and 120 are detour (clone) nodes at the exact coordinates of turbines 49 and 50.

**Length**
- math.fsum of the Euclidean segment lengths is 217395.35402025303 m. This equals the claimed value (difference 0.0) and the value in segments.json.

**Topology**
- Both clones have degree 2. I contracted them into logical links.
- The result has 110 logical links, no root-root link and no cycle, and all 110 turbines are reachable from root -1. It is a single tree, which is a valid capacitated forest.
- Feeders at the root: 16.
- Turbine counts in the subtree under each feeder: fifteen subtrees of 7 and one of 5, which sum to 110. The maximum is 7, which does not exceed the capacity of 7.
- The maximum turbine degree is 3, so the set is branched.

**Crossings** (exact rational arithmetic over all 6,216 segment pairs)
- No proper crossings.
- No T-touches and no collinear overlaps.
- No segment passes through a VertexC point (turbine, root or border vertex) that it does not end at.

**Containment**
- The border polygon is valid.
- Shapely `covers` holds for all 112 segments, and `contains` also holds for all of them, so no segment runs along the boundary.
- As a separate exact check, no segment properly crosses any border edge, and every segment midpoint is inside the border.
- There are no obstacles.

**Comparison with stored sets**
All 4 stored route sets for (nodeset 'Hornsea Two West', capacity 7):

| id | topology | creator | length (m) | feeders_per_root | margin (m) | relative margin |
|---|---|---|---|---|---|---|
| 3689 | radial | baselines.hgs | 217712.18494496983 | [16] | 316.8309 | 1.455e-3 |
| 44466 | radial | MILP.pyomo.cplex | 217712.18494496983 | [16] | 316.8309 | 1.455e-3 |
| 98 | branched | MILP.pyomo.cplex | 218384.3987299083 | [16] | 989.0447 | 4.529e-3 |
| 4178 | radial | baselines.lkh | 234134.8716544603 | [16] | 16739.5176 | 7.150e-2 |

- Every relative margin is above 1e-6.
- The two shortest stored sets tie and both have feeders_per_root [16], so the feeder cap is [16]. The claim uses [16].
- The other 36 capacity-7 rows with handle 'hornsea2w' belong to '!'-augmented nodesets with T=50, so they are not part of this instance.

**Determinism and controls**
- A second run gave byte-identical output.
- Negative control: I rewired one link in a copy of segments.json. The checker then failed on length, cycle, reachability, capacity (subtree of 8), crossings and comparison, so it does detect violations.

## 3. Official validator (optiwindnet 0.3.2, scripts/official.py)
Before loading object/G.pickle I inspected its opcodes with pickletools. The only globals are networkx, numpy, bitarray and optiwindnet.types.

**Results on both objects**
- validate_routeset on object/G.pickle returns [].
- I rebuilt G from object/routeset-packed.json with optiwindnet.db.storage.G_from_routeset, using the database nodeset row and a placeholder method. validate_routeset on the rebuilt G also returns [].
- For both graphs:
  - The edge-length sum and the Euclidean length through fnT are both 217395.35402025303.
  - VertexC is identical to the database blob, the border is identical, and there are no obstacles.
  - Capacity is 7 and topology is BRANCHED.
  - There is no length_mismatch_on_db_read.
  - feeders_per_root is [16].

**Both object files describe the same network**
- G.pickle and the rebuilt G have identical labelled edge sets and identical edge geometry.
- segments.json matches G.pickle in both geometry and labels.
- pack_G(G.pickle) equals routeset-packed.json in R, T, C, D, capacity, length, feeders_per_root, edges, clone2prime, detextra, num_diagonals, handle, creator and misc.

**Harness sanity** (scripts/controls.py)
- I rebuilt the 4 stored sets the same way. Each validates to [], its Euclidean length equals its stored length with 0.0 difference (so stored lengths use the same detours-included Euclidean convention), and each lies within the border.
- Setting capacity to 6 makes the validator report 'κ = 6, max_load = 7'. Removing an edge makes it report connectivity violations.

## 4. Doubtful points / notes (none blocks the claim)
- **Detours bend exactly at turbine positions.** Feeder -1→35 bends at clone 119, which sits on turbine 49. Feeder -1→22 bends at clone 120, which sits on turbine 50. Turbine 49's own cables (bearings -57.9° and 38.2°) lie in one sector between the detour's legs (83.9° and -89.7°). The same holds for turbine 50 (cables at -101.3° and 45.7°, detour legs at 48.0° and -112.75°). This is the release's own convention ("bends at a detour node on the turbine"), and the stored sets 3689/44466 use the same clones [49,50]. The validator accepts it.
- **The substation is a border vertex.** Feeders start on the boundary, and `contains` still holds for every segment.
- **The misc fields could mislead.** misc in the packed record and in G.pickle carries termination 'OPTIMAL', bound 217262.67 and relgap 9e-12. These come from the last CP-SAT sub-solve with most links pinned (as CLAIM.md's provenance says). They are not a global bound, and they are the straight-line objective, not the detours-included length. The claim does not assert optimality. If the record is ever submitted, these fields should not be read as a certificate.
- **Handle differs from the release.** The object's handle is 'Hornsea_Two_West', while the release uses 'hornsea2w'. This is cosmetic, because instance identity comes from the nodeset name and the VertexC blob, and both match.
- **Latest Zenodo version not checked live.** status/zenodo-latest.json is a frozen snapshot (record 23537067, published 2026-10-21) and I did not query Zenodo for this review. Whether a newer version exists is for the panel's status check, not this reproduction.

## Verdict
Every property in the criterion reproduces from the saved files with my own checker and the official validator: length, endpoints, capacitated tree, feeders, crossings, containment, nodeset identity, and the strict comparison against all 4 stored sets with the feeder cap. The two object files describe the same network. I found no mismatch, no missing object and no non-determinism.

pass: true
