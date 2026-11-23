# Reproduce check, claim-ho3 (Hornsea One.1_OSS, capacity 3)

context: fresh REPRODUCE skeptic subagent of a three-person panel; started with only the brief and the frozen claim folder claim-ho3/; wrote its own checker (work-reproduce-v3/chk.py, touch.py) before reading any author code; python -I, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1.

Definition used (REPRODUCE.md step 2/4, criterion.txt): total length = sum of Euclidean segment lengths; capacitated forest rooted at the substation, every turbine once, every feeder subtree <= 3 turbines; no crossings; every segment inside the border and outside obstacles; endpoints at VertexC; strictly shorter (> 1e-6 relative) than every stored set of the instance (any topology); feeders <= shortest stored set's feeders_per_root; validate_routeset == [].

## Reference database
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz sha256 = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches CLAIM.md). Own decompressed copy opened read-only.
- Nodeset 'Hornsea One.1_OSS' (one row): T=174, R=1, B=25, VertexC shape (200,2); constraint_groups [25] = border only, 0 obstacles; border polygon valid.
- Routesets for this nodeset with capacity 3: 4 rows (44 for all capacities): 40884 radial 735948.7528 [58] MILP.pyomo.cplex; 9597 radial 738034.6339 [58] hgs; 2784 branched 739768.9053 [59] cplex; 8885 radial 753634.9352 [58] lkh. Shortest = 40884, cap = 58 feeders.

## Own checker, from object/segments.json (242 segments)
- Endpoints not in VertexC: 0. Segment ids map consistently to coordinates; turbine ids match VertexC; root matches.
- Length: 735605.4808072001 m (plain sum and fsum agree; equals length_sum_euclid_m and the packed 'length').
- Nodes: 174 turbines, root, 68 clone/detour nodes (all degree 2; 64 located at turbine coordinates, 4 at border vertices). After contracting them: 174 logical edges, 174 turbines present, forest ok (no cycle, each turbine reached once), 58 feeders at the single substation, 58 subtrees of exactly 3 turbines (max 3).
- Turbine degree in the logical tree: 116 with degree 2, 58 with degree 1; max 2, so radial as stated in CLAIM.md (the packed misc.topology label says 'branched', the search topology; consistent with the claim text).
- Crossings (exact Fraction arithmetic, all 29,161 pairs): 0 proper crossings. No endpoint lies in the interior of another segment and no partial collinear overlaps. 134 pairs of segments have identical geometry (stacked cables through shared corridors via clones of turbine vertices, 19 distinct geometries, e.g. root-to-turbine 89 five times). These are not crossings; the stored sets use the same representation (D = 57..103 clones in ids 40884, 2784, 9597, 8885). Noted for transparency.
- Border/obstacles (shapely): 0 segments not covered by the border (also 0 at 1e-6 tolerance); 0 obstacles, 0 violations.

## Comparison
- Claimed value 735605.4808 vs shortest stored 735948.7528: difference 343.2720 m, relative 4.664e-4 (0.047%); against each of the 4 stored sets (radial and branched) (stored - mine)/stored > 1e-6 holds for all.
- Feeders 58 = shortest stored set's 58.

## Official validator
- Graph rebuilt from object/packed (object/routeset-packed.json) via TerseLinks.to_routeset on a nodeset built from the DB row (G.pickle not loaded). optiwindnet 0.3.2 validate_routeset(G) returned [].
- Rebuilt G: 242 edges, length 735605.4808072001, 58 feeders. Edge multiset equals object/segments.json both by node ids (u,v) and by coordinates.

Determinism: repeated runs of the checker gave identical output. No __pycache__ in the claim folder. No mismatch or missing object found.

pass: true
