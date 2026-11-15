# REPRODUCE skeptic: Cazzaro-2022G-210.solid.1_OSS, capacity 6, radial

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Files read: claim/CLAIM.md, claim/criterion.txt, claim/REPRODUCE.md, claim/object/segments.json, claim/object/routeset-packed.json, claim/object/G.pickle (loaded only in the optiwindnet venv), claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz, claim/status/zenodo-latest.json. The claim folder contains no author code; the checker below was written from the definition before any optiwindnet code was inspected. Scripts and raw outputs are in panel/work-reproduce/ (my_checker.py, my_bundle_check.py, run_validator.py, unpack_sets.py, dump_db.py and their *.out files). Settings: OMP_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1, python -I.

## Definition implemented (verbatim from claim/criterion.txt)

> For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!', and topology X (radial or branched), a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared.

## Step 1: reference file and instance data

- sha256 of the .xz: `c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a`. This matches the claimed value. The md5 `85faffb2e13600b017f1b583b259edd7` also matches the checksum in status/zenodo-latest.json, and that record is version index 1 with `is_last: True`. The decompressed sqlite has sha256 `9aa8214c…45e1`.
- Nodeset row `Cazzaro-2022G-210.solid.1_OSS` (the name has no '!' prefix and is unique): T=210, R=1, B=19, VertexC shape (230, 2). constraint_groups=[19], which is the border only, with no obstacle groups. Border order: constraint_vertices [210,211,212,226,213,…,225]. The substation is the last row (119326.6833, 117131.5167).
- Routeset rows for this nodeset with capacity=6. There are exactly 2. The DB handle is `cazzaro_2022G210_solid_1`, which differs from the object's handle string. That difference is cosmetic, because the nodeset identity is proven by an exact VertexC match (see below).

| id | topology | creator / solver | length (m) | feeders_per_root | D |
|---|---|---|---|---|---|
| 25098 | radial | baselines.hgs / HGS-CVRP, timeLimit 120 | 401553.2841814422 | [36] | 27 |
| 25278 | branched | MILP.pyomo.cplex, time_limit 21600, feeder_limit min_plus1 | 399738.04328672175 | [36] | 25 |

## Step 2: independent checker (my_checker.py, from segments.json + DB VertexC)

| property | my result | claimed |
|---|---|---|
| segments | 248 | 248 (in G and in packed) |
| total length, sum of Euclidean segment lengths | 396403.726914 (fsum 396403.7269139845) | 396403.7269 |
| endpoint coincidence with nodeset coordinates (exact) | 496 endpoints: 424 turbine, 36 substation, 36 border vertex; 0 unmatched | endpoints at turbines/substation/border |
| turbine coordinates missing | none (210/210 turbine labels present) | all turbines |
| label→coordinate consistency (turbine i → VertexC[i], -1 → substation, clone → VertexC[clone2prime]) | 0 mismatches | n/a |
| detour clones | 38 (D=38): 20 at turbine positions, 18 at border vertices; all degree 2 | D=38 |
| labelled graph | 249 nodes, 248 edges, connected, a tree | n/a |
| turbine electrical degree (clones contracted) | {1: 36, 2: 174}, so radial | radial |
| radial paths from substation | ok; covers 210 turbines; string sizes {3: 2, 6: 34}; max 6 ≤ 6 | capacity 6 |
| feeders at substation | 36 (36 root-incident segments) | 36 |
| proper crossings (interior points) | 0 | 0 (validator) |
| endpoint touching another segment's interior | 0 | n/a |
| segment passing through a non-endpoint turbine/substation | 0 | n/a |
| partial collinear overlaps | 0 | n/a |
| collinear overlaps with identical endpoints (shared corridors) | **87 segment pairs** in 9 corridors | not mentioned |
| shared-corridor topological crossings (my_bundle_check.py: 36 feeder polylines; for each shared run or point, does B enter on one side of A and leave on the other?) | 0 crossings (1 interior contact tested, 632 contacts at a polyline end, of which 630 are the common root) | n/a |
| polyline revisiting a coordinate | none | n/a |
| border polygon (19 vertices) | valid, area 263107447.9 m² | n/a |
| segments not covered by the border polygon (shapely covers, closed set) | 0 of 248; 10 segments run along the boundary itself | all inside |
| obstacles | none in the nodeset | "site has no obstacles" |
| determinism | rerun output byte-identical | n/a |

What I found about endpoints and overlaps: every endpoint is exactly a turbine, substation or border-vertex coordinate. Detours bend at border vertices and also at other turbines' positions, through clones of turbines 69, 73, 87, 101, 140. Several feeders therefore run along the same straight corridor, which appears as identical collinear segments: 87 such pairs. Taken literally, the requirement "no two segments overlap except at shared endpoints" is not met. However, this is how the benchmark itself represents parallel cables in a shared corridor:

- The stored sets contain the same pattern. My checker, run on them after unpacking with optiwindnet's G_from_routeset, finds 51 identical-overlap pairs in radial set 25098 and 35 in branched set 25278, also through turbine-position clones.
- The validator explicitly classifies coincident runs and accepts them unless the runs cross (`overlap_cross`).
- My own side-of-exit test finds no topological crossing in any shared corridor.

I therefore treat the overlaps as consistent with the criterion, which asks about crossings, and not as a violation. The 10 boundary-running segments lie on the border (inside the closed polygon). The stored sets have 0 such segments.

My checker discriminates correctly on the controls: on 25098 it confirms radial, 36 feeders, length 401553.284181; on branched 25278 it reports `radial paths ok: False` (degree-3 turbines), as it should.

## Step 3: official validator (optiwindnet 0.3.2, .venv-optiwindnet)

| check | result |
|---|---|
| validate_routeset(G from object/G.pickle) | `[]` |
| G: T, R, B, capacity, topology, D | 210, 1, 19, 6, radial, 38 |
| G.graph['VertexC'] == DB VertexC (exact, all 230×2) | True |
| G edges == segments.json (undirected, labels and coordinates) | True (248 = 248) |
| G.size(weight='length') / Euclidean sum over G edges | 396403.726914 / 396403.726914 |
| G fnT for clones == packed clone2prime | True |
| G degree of substation | 36 |
| G rebuilt independently from object/routeset-packed.json through optiwindnet.db G_from_routeset on the DB nodeset | 248 edges, length 396403.726914, no length-mismatch flag, validate → `[]`, root degree 36; segments identical to segments.json |
| validate_routeset on stored 25098 / 25278 (control) | `[]` / `[]`; recomputed lengths 401553.284181 / 399738.043287 equal the stored lengths |
| determinism | rerun output byte-identical |

## Step 4: comparison with the criterion

| comparison | stored length | object length | difference (m) | relative | > 1e-6 rel | feeders object ≤ stored | claimed |
|---|---|---|---|---|---|---|---|
| radial best, id 25098 (the only stored radial set) | 401553.2841814422 | 396403.7269139845 | 5149.5572674578 | 1.282409% | True | 36 ≤ 36 True | 401553.2842, 5149.5573, 1.282% |
| branched best, id 25278 (context) | 399738.0432867217 | 396403.7269139845 | 3334.3163727373 | 0.834125% | True | 36 ≤ 36 True | 399738.0433, 3334.3164 |

No stored set is more restrictive than radial, so the radial comparison covers every set required. The object is also shorter than every stored set of any topology. All claimed numbers match my output to the precision stated.

## Verdict

Every criterion property is confirmed from the saved files and the release DB:
- the nodeset is identical;
- the set is radial with strings ≤ 6 and all 210 turbines connected;
- it uses 36 feeders, which is ≤ 36;
- the validator returns `[]`;
- there are no crossings, by my independent geometric and shared-corridor checks;
- every segment lies in the border, and there are no obstacles;
- the recomputed length 396403.7269 m is the value compared;
- it is strictly shorter than stored radial 25098 by 1.28% (and than branched 25278 by 0.83%).

The one literal deviation from the panel's wording is that shared-corridor collinear overlaps exist (87 identical pairs). This is the benchmark's own convention: the stored sets have the same pattern and the validator accepts it. It is not a crossing.

pass: true
