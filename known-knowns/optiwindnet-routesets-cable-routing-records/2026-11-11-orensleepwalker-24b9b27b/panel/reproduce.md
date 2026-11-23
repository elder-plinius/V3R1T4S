# Reproduce panel report (v3, fresh)

context: fresh-context REPRODUCE skeptic, started with only the brief and the frozen claim folder; own checker written from the REPRODUCE.md definition before any author code was read (no author code exists in the claim folder); claim folder read-only, PYTHONDONTWRITEBYTECODE=1, python -I, OMP_NUM_THREADS=1.

## Reference database
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz sha256 = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches CLAIM.md/criterion.txt). Own decompressed copy (79,986,688 bytes) used.
- nodeset 'Hornsea One.1_OSS': T=174, R=1, B=25, VertexC 200x2, constraint_groups [25] (border only, 0 obstacles); border polygon valid.
- All routeset rows for this nodeset: 44; with capacity = 4: 4 rows (all read):
  - 42471 radial MILP.pyomo.cplex 591151.3395249809 feeders [45]
  - 9601 radial baselines.hgs 595070.4239063956 [44]
  - 2787 branched MILP.pyomo.cplex 596799.9296729249 [45]
  - 8898 radial baselines.lkh 604020.324967396 [44]
- Shortest stored set is 42471, feeders_per_root [45] = the feeder cap.

## My checker (object/segments.json, 206 segments)
Definition used (REPRODUCE.md step 2): recompute length as sum of Euclidean segment lengths; capacitated forest rooted at the substation, each turbine once, subtree per feeder <= 4; count feeders; pairwise non-crossing; inside border, outside obstacles; endpoints at nodeset coordinates.
- Endpoints: all 412 segment endpoints equal, bit-exactly, VertexC of the node (clones mapped through routeset-packed.json clone2prime, clone ids start at T+B): 0 mismatches.
- Length: sum = 589790.5175683427 m (claim 589790.5175683424; difference 3e-10). 
- Structure: 207 nodes (174 turbines, 1 root, 32 detour/contour clones), 206 edges, connected from the root, no cycle (a tree), all 174 turbines present once.
- Feeders at the substation: 45 (= cap 45). Feeder subtree loads: 43 feeders with 4 turbines, 2 with 1 turbine; max 4 <= capacity 4; total 174.
- Topology: with detour/contour nodes contracted, turbine degree histogram (incl. parent link) {1:47, 2:125, 3:2}. Two turbines have degree 3, so the set is branched and not radial (consistent with CLAIM.md, max degree 3).
- Crossings: pairwise test on coordinates (segments sharing an endpoint coordinate allowed to touch only there): 0 proper crossings, 0 T-touches or other non-shared contacts. 1247 shared-endpoint contacts. 40 pairs overlap collinearly; all are stacked parallel cables (feeders from the substation to clones of the same turbine, or a detour hop shared by clones), i.e. the segmented-feeder construction of the optiwindnet model; their lengths are counted in the total once per cable. For comparison the stored best set 42471 has 68 such overlapping pairs. The official validator accepts this (below).
- Containment: all 206 segments covered by the border polygon (no tolerance needed; 0 uncovered strictly); no obstacles exist.
- Note: my first draft of the crossing test keyed on node ids and falsely flagged contacts between distinct clones sharing a coordinate (output "proper crossings 134000000" in an early run of mycheck.py is that bug, not a finding). It was replaced by the coordinate-based test above, which is the one reported.

## Comparison with every stored set (strict, > 1e-6 relative)
Relative improvement of 589790.5175683 versus: 42471 0.23020% (1360.8220 m); 9601 0.88727%; 2787 1.17450% (7009.4121 m); 8898 2.35585%. All > 1e-6, so strictly shorter than every stored set of any topology (radial or branched). Feeders 45 <= shortest set's 45.

## Official validator
Graph rebuilt from object/routeset-packed.json (L_from_nodeset on the DB nodeset + TerseLinks.to_routeset, no G.pickle loaded): 207 nodes, 206 edges; G.size('length') = 589790.5175683424; topology branched. optiwindnet.validating.validate_routeset(G) (optiwindnet 0.3.2) returns []. Rebuilt edge set (node ids) equals object/segments.json's (u,v) set: True (206 = 206). As a sanity control, stored 42471 rebuilt the same way has length equal to its DB value and also validates [].

## Determinism
mycheck.py and official.py were each run twice; identical outputs. No __pycache__ in the claim folder.

## Files
Work folder: panel/work-reproduce-v3/ (mycheck.py, official.py, ref.sqlite).

pass: true
