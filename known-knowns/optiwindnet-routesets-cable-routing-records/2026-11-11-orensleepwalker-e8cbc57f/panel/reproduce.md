# Reproduce skeptic report (claim-ho2, v3 fresh)

context: fresh subagent with no prior context, given only the kit instruction, REPRODUCE.md and the claim folder; own checkers written from the definition before any author code was read (the author's code is not in the claim folder); python run with -I and PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1; the claim folder was not written to (no __pycache__ in it).

Instruction followed: "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism." Definition quoted from criterion.txt: "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root) ... must pass optiwindnet.validating.validate_routeset with no violations ... every route segment must stay inside the site border and outside every obstacle polygon ... its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference database
- sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches CLAIM.md/REPRODUCE.md). Own decompressed copy made in the work folder.
- Exactly one nodeset row named 'Hornsea One.1_OSS' (no '!' prefix): T=174, R=1, B=25, VertexC 200x2 (turbines 0..173, border 174..198, root 199), constraint_groups [25] so one border and 0 obstacles.

## Stored sets (capacity 2, this nodeset: 4 rows; 44 rows over all capacities)
- 42234 MILP.pyomo.cplex radial 1031350.3996093208 feeders [87]
- 9595 baselines.hgs radial 1031350.3996093209 feeders [87]
- 8881 baselines.lkh radial 1032129.6495922131 feeders [87]
- 2782 MILP.pyomo.cplex branched 1032792.2112339971 feeders [88]
Shortest stored = 42234; feeder cap = 87. Shortest stored branched = 2782. Matches CLAIM.md.

## Own checker results on object/segments.json (268 segments)
- Endpoints: every segment endpoint equals a nodeset VertexC coordinate exactly (0 misses); segment ids u/v map via clone2prime to the same coordinates (0 mismatches). Detour nodes: 94 clones (88 of turbine vertices, 6 of border vertices), all of degree 2.
- Length: sum of Euclidean segment lengths = 1030454.28782717 (claimed 1030454.2878271756; difference 5e-10 m).
- Topology: after contracting detour clones, 174 logical edges, 175 nodes, connected from the substation, a tree. All 174 turbines present once; logical turbine degree histogram {2: 87, 1: 87}, so max degree 2 = radial, as stated in CLAIM.md. 87 feeders at the one substation; 87 subtrees each of exactly 2 turbines (max 2 = capacity, total 174).
- Crossings: exact rational arithmetic over all 35778 segment pairs: 0 proper crossings, 0 touching without a shared endpoint. There are 225 collinear-overlap pairs (cables stacked along common corridors through detour vertices at turbine positions); the stored sets use the same convention (42234: 222 overlap pairs, 2782: 110) and the official validator accepts it.
- Border/obstacles: border polygon valid; all 268 segments and all turbines are covered by the border polygon (shapely covers); 0 obstacles.
- Strict comparison: 1030454.2878 vs shortest stored 1031350.3996: 896.1118 m shorter, relative 8.69e-4 > 1e-6; also shorter than the other 3 stored sets (and than the shortest branched 1032792.2112 by 2337.9 m). Feeders 87 <= cap 87.

## Official validator
Graph rebuilt with optiwindnet.db.G_from_routeset from object/routeset-packed.json plus the nodeset row of my own database copy (G.pickle not loaded). Rebuilt length 1030454.2878271756, no length-mismatch flag, validate_routeset returned [] (0 violations). Rebuilt edge multiset equals object/segments.json (268 = 268, equal). The stored sets 42234 and 2782 also give 0 violations with the same code path. Note: the packed misc topology reads 'branched' (as the search was branched); the claim's radial label was verified by the degree check above.

## Determinism
All checks are deterministic (exact arithmetic or fixed files); re-runs gave identical output.

No mismatch, missing object or non-determinism found.

pass: true
