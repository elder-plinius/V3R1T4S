# Reproduce report: Noirmoutier, capacity 2, topology branched (radial object)

context: fresh-context REPRODUCE skeptic subagent, started with only the brief and the claim folder; checker written from the definition (criterion.txt, REPRODUCE.md) before any author code was read (the claim contains no author search code; only data files). Run with python -I, PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1. Scripts in panel/work-reproduce/ (mycheck.py, logical.py, official.py, cmp.py).

## Reference database
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz sha256 = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches CLAIM.md). Decompressed own copy (deleted afterwards).
- nodeset 'Noirmoutier': T=61, R=1, B=5, VertexC 67x2 (turbines 0..60, border 61..65, substation 66 = id -1), constraint_groups [5], vertices [61..65]: one border, 0 obstacles (border valid, area 1.231e8 m2).

## Own checker (object/segments.json, 73 segments)
- Length: sum of Euclidean segment lengths = 150439.9933339027 m; equals claimed value exactly (150439.9933).
- Endpoints: every segment endpoint coordinate is exactly a VertexC row; node-id coordinates agree with VertexC; the 12 detour clone nodes (ids 66..77) sit exactly at their clone2prime vertex coordinates. 0 problems.
- Raw graph: 74 nodes, 73 edges, connected, acyclic (a tree); all 61 turbines reached exactly once.
- Feeders: root degree 31. Subtree turbine counts per feeder: thirty of 2, one of 1; max 2 <= capacity 2; sum 61.
- Topology: detour clone nodes form 10 chains, each with exactly 2 real neighbours; dissolving them gives 61 logical edges (logical.py). Logical turbine degrees: 31 of degree 1, 30 of degree 2, none higher; logical subtrees are paths: radial confirmed. (Contracting clones into their prime vertex instead merges coincident points and is not a meaningful logical tree; not used.) Note: several detour segments coincide exactly with the feeder to turbine 28 / 20 / 45 (collinear overlaps, shared endpoints). These are optiwindnet detour representation, reported by shapely as touching/overlapping, not proper crossings.
- Crossings: pairwise over all 73 segments, 0 proper crossings (20 collinear overlaps among the coincident detour segments, all sharing both endpoints coordinates, none a transversal crossing).
- Containment: every segment inside the border (1e-6 m tolerance), none touching or inside an obstacle (none exist). 0 violations.

## Official validator
Graph rebuilt from object/routeset-packed.json (G_from_routeset, duck-typed records; G.pickle not loaded): validate_routeset(G) = []. Rebuilt length 150439.9933339027 equals the packed length, no length mismatch flag. Rebuilt edge set equals the edge set of object/segments.json (73 = 73, no duplicates). (Graph topology attribute reads 'branched' from the packed misc; the object itself is radial by degree, which also counts for branched.)

## Comparison with every stored set (exhaustive, not a sample)
Nodeset has 42 routeset rows (capacities 2..12); all 4 with capacity = 2 read, lengths also recomputed from rebuilt graphs (equal to stored):
- id 46244 baselines.lkh radial, 150827.0401, feeders [31]  (shortest)
- id 27495 baselines.hgs radial, 150985.2106, [31]
- id 27564 MILP.pyomo.cplex branched, 150985.2106, [31]
- id 36274 MILP.pyomo.cplex radial, 150985.2106, [31]
Claim 150439.9933 < 150827.0401 by 387.0468 m = 0.2566% relative, far above 1e-6; shorter than all four. Feeders 31 <= cap 31 (shortest set's feeders_per_root). Same nodeset (coordinates all from the DB VertexC). Matches CLAIM.md numbers.

## Determinism
mycheck.py run twice, identical output hash. No __pycache__ in the claim folder; claim folder not modified.

No mismatch, missing object or non-determinism found.

pass: true
