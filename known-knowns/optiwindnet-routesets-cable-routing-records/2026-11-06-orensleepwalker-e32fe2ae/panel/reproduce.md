# REPRODUCE skeptic: claim-yi11 (Yi-2019.1_OSS, capacity 11, radial)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read: `CLAIM.md`, `criterion.txt`, `REPRODUCE.md`, `object/segments.json`, `object/routeset-packed.json`, `object/G.pickle`, `references/optiwindnet-routesets-r26.10-v4.sqlite.xz`, `status/zenodo-latest.json`. No other workspace file was read. The claim folder was not modified (PYTHONDONTWRITEBYTECODE=1; no new files appeared in it). My scripts and raw outputs are in `panel-yi11/work-reproduce/` (`scripts/`, `checker_run1.txt`, `checker_run2.txt`, `validator_run1.txt`, `validator_run2.txt`, `compare_run.txt`, `tamper_run.txt`).

## Definition implemented (quoted from `criterion.txt`)

> "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

My checker (`scripts/my_checker.py`) was written from this text before looking at any author code (none is in the claim folder). It checks: Euclidean length sum; segment endpoints equal nodeset points and agree with the u/v ids (clones resolved via `clone2prime`); id-graph is a tree connected to the root; clone (detour) nodes have degree 2; after contracting detour chains every turbine has degree <= 2 and each feeder walk is a simple path (radial) of <= 11 turbines; every turbine appears exactly once; feeders at the substation; pairwise proper crossings with exact integer orientation tests (all coordinates are integers); collinear overlaps and interior touches; points shared by several ids, with an angular ray-interleaving test for hidden crossings; shapely `border.covers(segment)`, DE-9IM obstacle-interior test, length on the border line, obstacle-boundary contacts; and an exact proper-crossing test against every border/obstacle edge.

## 1. Reference database

| Item | Claimed | Mine |
|---|---|---|
| sha256 of `.xz` | c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a | c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a |
| md5 of `.xz` vs `status/zenodo-latest.json` (record 23537067, published 2026-10-21) | 85faffb2e13600b017f1b583b259edd7 | 85faffb2e13600b017f1b583b259edd7 |
| sha256 of decompressed `.sqlite` (my copy) | (not stated) | 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1 |
| nodeset rows named Yi-2019.1_OSS | 1 | 1 |
| T / R / B | 119 / 1 / (not stated) | 119 / 1 / 153 |
| VertexC shape | - | (273, 2), all integer-valued |
| substation (last row) | - | (13119, 6300) |
| constraint groups | border + obstacles | 18 groups: border 10 vertices, 17 obstacles (sizes sum to 153 = B) |

Latest-version check is limited to the saved `status/zenodo-latest.json` snapshot (no network allowed).

## 2. Own checker on `object/segments.json` (run twice, outputs byte-identical)

| Property | Claimed | Mine |
|---|---|---|
| segments | - | 132 (133 nodes: 119 turbines, 1 root, 13 clones; tree = True) |
| total Euclidean length (m) | 129717.3657 | 129717.36569882008 |
| `length_sum_euclid_m` in segments.json | 129717.36569882008 | 129717.36569882008 |
| `length` in routeset-packed.json | - | 129717.36569882008 |
| endpoint mismatches (coords vs nodeset / ids) | - | [] |
| turbines present / missing | 119 / - | 119 / [] |
| each turbine in exactly one string | - | True (119 turbines in strings) |
| connected to root | - | True |
| clone degrees | - | [2] (pure pass-through detour nodes) |
| max turbine degree (after contracting detours) | radial | 2 |
| string sizes | <= 11 | [9, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]; max 11 |
| feeders at substation | [11] | [11] |
| proper crossings (exact) | none | [] |
| collinear overlaps | - | 2: (-1,72)&(-1,283), (-1,93)&(-1,279) |
| interior touches | - | 1: (44,43)&(43,42) collinear end-to-end at shared turbine 43 (straight string, benign) |
| segments through a turbine/root location in their interior | - | [] |
| segments not covered by closed border | none | [] |
| segments entering an obstacle interior (DE-9IM) | none | [] |
| segment length lying on the border line | - | [] (none on the border line) |
| exact proper crossings with any border/obstacle edge | - | [] |
| segments touching obstacle boundaries | - | 16 (detour legs to obstacle corners; 3 run along an obstacle edge: (273,274) 91.787799 m on obstacle 7, (277,278) 219.020547 m on obstacle 15, (281,282) 972.770271 m on obstacle 13) |

Detour chains: [24,276,47], [29,272,51], [30,275,31], [53,273,274,54], [98,277,278,99], [-1,279,108], [-1,283,282,281,280,86], [-1,284,26].

Shared corridors / hidden-crossing analysis (`scripts/shared_points.py`). Three clones sit on turbine locations (clone 279 = turbine 93, 283 = turbine 72, 284 = turbine 48):

| Point | Turbine rays (deg) | Clone-path rays (deg) | Result |
|---|---|---|---|
| (16886, 8097) | 93: to -1 205.5029, to 94 342.3863 | 279: to -1 205.5029, to 108 19.6401 | shared corridor to the root, identical segment; both routes end at the root, so they can be separated without crossing; no interleaving |
| (13642, 6991) | 72: to -1 232.8789, to 71 162.2964 | 283: to -1 232.8789, to 282 94.8671 | same: shared corridor ending at the root; no interleaving |
| (10476, 5852) | 48: to 49 342.0269, to 27 259.0677 | 284: to -1 9.6204, to 26 238.5321 | no shared ray; the clone path touches turbine 48's location without interleaving, so it does not cross there |

None of the collinear corridors hides a crossing. Note: two routes run through the positions of turbines 93, 72 and 48 (optiwindnet contour clones); the official validator accepts this (below).

## 3. Official validator (optiwindnet 0.3.2, `.venv-optiwindnet`, run twice, outputs byte-identical)

| Item | Claimed | Mine |
|---|---|---|
| `validate_routeset(G)` on `object/G.pickle` | [] | [] |
| G nodes / edges | - | 133 / 132 |
| G T, R, B, C, D | - | 119, 1, 153, 7, 6 |
| G capacity / name / topology | 11 / Yi-2019.1_OSS / radial | 11 / Yi-2019.1_OSS / radial |
| G VertexC == DB VertexC; border == DB; obstacles == DB (17) | same nodeset | True; True; True |
| G edge id set == segments.json; coords equal (via fnT) | - | True; True |
| G Euclidean length; `G.size(weight='length')` | 129717.3657 | 129717.36569882008; 129717.36569882008 |
| G feeders | [11] | [11] |
| packed `edges` (child-to-parent list, clones at T+B+i) == segments.json edges | - | True (132 edges) |
| validator sanity: copy of G with capacity set to 10 | - | 1 violation: `κ = 10, max_load = 11` (validator is not vacuous) |

## 4. Comparison with stored route sets (capacity 11; DB has 3 rows)

| Stored set | Topology | Length (m) | feeders | Claim's length minus stored | Relative | Claimed |
|---|---|---|---|---|---|---|
| 21564 baselines.hgs | radial (only radial row) | 135339.37650124528 | [11] | -5622.010802425197 | shorter by 0.04154009681264837 (> 1e-6) | 135339.3765, by 5622.0108 (4.154%) |
| 22551 MILP.pyomo.gurobi | branched | 127958.86459249683 | [12] | +1758.5011063232523 | longer by 0.013742706391803715 | branched best 127958.8646; not shorter |
| 21911 MILP.pyomo.cplex | branched | 130862.09481791781 | [12] | -1144.7291190977267 | shorter by 0.008747598918468397 | (not claimed) |

Feeders: claim [11] <= stored radial best [11]: True. No rows with null/other topology. For X = radial the only comparison set is the radial rows, and the claim beats all (one) of them by more than 1e-6 relative. It does not beat the branched best, matching the claim's own statement. Nodeset name has no '!' prefix.

## Verdict

Every property in the definition was checked from the saved files and confirmed: same nodeset, length recomputed exactly as stated, radial, capacity respected, 11 feeders (not more than the radial best's 11), no crossings (including the shared corridors), inside the border and outside all 17 obstacles, official validator returns [], and strictly shorter than the only stored radial set by 4.154%. Runs were deterministic. Caveats, which do not fail the criterion: the latest-version check uses the saved Zenodo snapshot only, and some routes pass through turbine positions as contour clones, which the official validator accepts.

pass: true
