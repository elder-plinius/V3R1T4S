# REPRODUCE skeptic: claim-cazzaro7

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Instance: Cazzaro-2022G-210.solid.1_OSS, capacity 7, topology radial (release r26.10-v4).
Files named relative to the claim folder. My own scripts and outputs are in `../panel-cazzaro7/work-reproduce/`: checker.py, validate.py, stored.py and corridors.py, with outputs checker_out1/2.txt, validate_out/2.txt, stored_out.txt and corridors_out.txt. Settings were OMP_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1 and `python -I`. I installed nothing and used no network.

## Definition implemented (written before reading any author code; I read no author code)

From criterion.txt (verbatim):
> "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

From REPRODUCE.md step 2 (verbatim): "check the network is a radial capacitated forest rooted at the substation (each turbine reached once, every string <= 7 turbines, turbine degree <= 2), count feeders at the substation, check pairwise segment non-crossing, and check every segment lies inside the border polygon."

My checker (checker.py) reads only object/segments.json and the database rows. It does the following:
- Matches every segment endpoint exactly to a VertexC row and checks that the labels agree with the coordinates.
- Contracts clone (detour) nodes, which must have degree 2, into logical edges.
- Checks the radial forest by walking each string from the root.
- Tests every segment pair for proper crossings, collinear overlaps and T-touches with exact rational orientation tests.
- Tests containment in the closed border polygon (shapely `covers`). It also counts exact proper crossings with the border edges and segments that run along the border.

corridors.py checks whether the coincident (shared-corridor) segments hide a crossing. It searches every left-to-right cable order of each shared corridor. At each junction point it tests local planarity: no two pass-through chords interleave, and no chord separates the cable ends at that point. I tested it on synthetic cases first: the no-cross case gave True and the hidden-cross case gave False.

## (1) Reference database and nodeset

| item | measured | claimed / expected |
|---|---|---|
| sha256 of references/…sqlite.xz | c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a | c78c8f3c…e3a (matches) |
| md5 of .xz | 85faffb2e13600b017f1b583b259edd7 | status/zenodo-latest.json: md5:85faffb2e13600b017f1b583b259edd7 (matches) |
| sha256 of my decompressed .sqlite | 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1 (still the same after the run) | – |
| nodeset rows named Cazzaro-2022G-210.solid.1_OSS | 1 (T 210, R 1, B 19, VertexC 230x2, constraint_groups [19]) | 210 turbines, 1 substation |
| obstacles | 0 (one constraint group, the border) | – |

Zenodo status: status/zenodo-latest.json is a saved snapshot (record 23537067, modified 2026-10-21). Without network access I could not re-check for a newer version.

## (2) Own checker on object/segments.json

| property | measured (checker_out1.txt) | claimed |
|---|---|---|
| segments | 228 (210 logical edges + 18 clone hops) | – |
| endpoints not at an instance point | 0; label/coordinate inconsistencies 0 | "endpoints coincide" (implicit) |
| clone (detour/contour) nodes | 18: 6 at border vertices, 12 at turbine points; all degree 2 | – |
| total Euclidean length (m) | 360354.074553 | 360354.0746 |
| zero-length / duplicate segments | 0 / 0 | – |
| turbines present | 210 of 210, each visited exactly once | 210 |
| logical edges | 210 (= T, so a forest) | – |
| turbine degree histogram | {1: 30, 2: 180} (max 2) | radial |
| strings | 30, all simple paths, every size 7 (max 7, sum 210) | ≤ 7 |
| substation feeders | 30 | [30] |
| proper crossings (exact) | 0 | 0 |
| T-touches (an endpoint inside another segment) | 0 | – |
| collinear overlapping segment pairs | 11, all identical segments, in 7 shared corridors with 9 extra copies | – |
| hidden crossing in shared corridors | none: a crossing-free order exists for every corridor group (each group has exactly 1 valid order) | – |
| border polygon | valid, area 263107447.881 m² | – |
| segments not covered by the closed border | 0 | 0 ("every segment lies inside") |
| exact proper crossings with border edges | 0 | – |
| segments running along the border | 0 | – |
| obstacle polygons | none in the nodeset | – |
| determinism | a second run gave byte-identical output (cmp) | – |

Shared corridors and pass-throughs:
- All 7 shared corridors are coincident runs of segments. Six start at the substation. The seventh (labels 118–230, 237–238 and 242–243) runs between turbine 118's point and border vertex 217 and carries 3 cables.
- 12 of the 18 clones sit at turbine coordinates (33, 77, 69×2, 118×3, 102, 120, 119, 73×2). A few feeder detours therefore bend exactly at another string's turbine point. This is optiwindnet's detour-clone convention.
- The stored sets do the same:
  - 25104 has 17 clones at turbine points, 8 shared corridors and 39 coincident pairs.
  - 25281 has 16 clones at turbine points, 7 shared corridors and 38 coincident pairs.
- My corridor search finds no hidden crossing in the claim or in either stored set.

## (3) Official validator (optiwindnet 0.3.2, .venv-optiwindnet)

| check | measured (validate_out.txt, stored_out.txt) | claimed |
|---|---|---|
| validate_routeset(G) on object/G.pickle | [] | [] |
| G.VertexC == DB VertexC; G.border == DB border | True; True | same nodeset |
| G edges vs segments.json | 228 vs 228; same label set True; coordinate mismatches 0; length-attribute mismatches 0 | match |
| sum of G edge lengths | 360354.07455296343 | 360354.0746 |
| G max load / root load / root degree | 7 / 210 / 30 | – |
| object/routeset-packed.json decoded with TerseLinks | edges == G.pickle True; fnT equal True; length 360354.07455296343; validate [] | – |
| determinism | a second run gave identical output | – |

## (4) Comparison with stored route sets (all rows, nodeset digest and capacity 7)

| stored set | topology | stored length (m) | recomputed from decoded G | validate | feeders_per_root | claim shorter by | relative |
|---|---|---|---|---|---|---|---|
| 25104 baselines.hgs | radial (the only radial row) | 364573.2688482088 | 364573.2688482088 | [] | [30] | 4219.194295 m (claimed 4219.1943) | 1.157297% (claimed 1.157%) |
| 25281 MILP.pyomo.cplex | branched (the only branched row) | 363836.6317543705 | 363836.6317543705 | [] | [30] | 3482.557201 m (claimed 3482.5572) | 0.957176% |

- The database has 2 stored rows for this instance: 1 radial and 1 branched.
- The claim is shorter than every radial row by more than 1e-6 relative: True.
- Feeders: the claim uses 30 and the radial best uses [30], so 30 ≤ 30 holds.
- The claim is also shorter than the branched row by more than 1e-6 relative: True. This goes beyond the radial criterion and is not required by it.

## Verdict

Every claimed number matches my own recomputation:
- length 360354.0746 m
- 4219.1943 m (1.157%) shorter than the stored radial best (id 25104)
- 3482.5572 m shorter than the stored branched best (id 25281)
- 30 feeders against 30

All criterion properties hold:
- same nodeset
- radial, with every string 7 or fewer turbines
- the official validator reports no violations
- no proper crossings, and no hidden crossing in the shared corridors
- every segment inside the closed border
- no obstacles in the nodeset

The comparison covered every stored row for the instance. Both scripts gave identical output on a second run. I found no mismatch and no missing object. Remaining caveats: I could not check Zenodo for a newer version (no network). Some detours bend at another string's turbine point, an optiwindnet convention that the stored sets also use.

pass: true
