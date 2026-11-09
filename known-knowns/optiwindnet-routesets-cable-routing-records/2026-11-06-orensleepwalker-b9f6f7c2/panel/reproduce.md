# REPRODUCE skeptic report: claim-ho8 (Hornsea One.1_OSS, capacity 8, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read (all inside the claim folder): claim/CLAIM.md, claim/criterion.txt, claim/REPRODUCE.md,
claim/object/segments.json, claim/object/routeset-packed.json, claim/object/G.pickle,
claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz, claim/status/zenodo-latest.json.
No author code exists in the claim folder and I read nothing else in the workspace. The only
library code I read was optiwindnet 0.3.2's own `validate_routeset` and `db/storage.py`
(`L_from_nodeset`, `G_from_routeset`), to rebuild G from the packed form.
Work files: panel-ho8/work-reproduce/ (my_checker.py, own_validate.py, negctl.py, *.out, *.out2).

Object hashes (sha256): claim/object/segments.json b9f6f7c2...00da, claim/object/routeset-packed.json
976ed7d1...ed89, claim/object/G.pickle 3613b5d8...f6e2.

## Criterion I implemented (quoted from claim/criterion.txt)
"For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!',
and topology X (radial or branched), a route set of topology X with strictly smaller total length than
every stored route set for that instance of topology X or more restrictive (radial counts for branched),
by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route
set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles
from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations
(topology, capacity, loads, crossings), every route segment must stay inside the site border and outside
every obstacle polygon (checked separately, since the validator does not test this), and its length,
recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

## Reference database
- I copied claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz to my work folder and ran `xz -dk` there.
  The .xz sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches the claim.
  Its md5 is 85faffb2e13600b017f1b583b259edd7, which matches the checksum in claim/status/zenodo-latest.json
  (record 23537067, file size 28464808). The decompressed .sqlite sha256 is 9aa8214c...45e1. The file has
  49,204 routesets, which matches the statement.
- Nodeset 'Hornsea One.1_OSS' has exactly one row (the name index is unique), with no '!' prefix. It has
  T=174, R=1 and B=25. VertexC is a 200x2 '<f8' array. constraint_groups is [25], which is the border
  (VertexC rows 174..198) and no obstacles.
- I read every routeset row with nodes_id equal to this nodeset's digest and capacity 8. There are 4 rows,
  and every one I read is listed here:
  - 45794: 380296.0541832061, radial, MILP.pyomo.cplex, feeders [22] (the shortest)
  - 2800: 381105.35144719895, branched, MILP.pyomo.cplex, feeders [22]
  - 9636: 383497.66370056797, radial, baselines.hgs, feeders [22]
  - 8923: 385884.67345649144, radial, baselines.lkh, feeders [22]

  All 4 are radial or branched, so all 4 are eligible comparators for X = branched.

## Own checker (claim/object/segments.json; stdlib only, exact Fraction geometry): all PASS
- **Endpoints and nodeset.** All 188 segments have both endpoints bit-equal to the VertexC coordinate of
  their label. Turbine labels are 0..173 and the root is -1. Clones 199..212 resolve through
  routeset-packed.json clone2prime: C=2 clones of border vertices 175 and 184, and D=12 detour clones of
  turbine positions. Every endpoint is a VertexC row.
- **Length.** The recomputed length, math.fsum of the Euclidean segment lengths, is 377034.6924851112 m.
  This equals the segments.json value, the packed `length`, and the claimed 377034.6925.
- **Topology.** I contracted the clone chains; every clone has degree 2. That gives 174 electrical
  edges, all turbines reachable from root -1, and no cycles: a spanning forest rooted at the substation.
  - There are 22 feeders at the root.
  - Feeder subtree loads are 21 x 8 and 1 x 6, so the maximum is 8, which equals the capacity. They sum to 174.
  - The maximum turbine degree is 3, with 11 branching turbines, so the topology is branched.
- **Crossings.** Across all 188x187/2 segment pairs (exact orientation tests) there are no proper
  crossings and no collinear overlaps. No endpoint touches another segment except at a shared endpoint.
  No segment passes through a turbine or substation in its interior.
- **Border and obstacles.** Every segment lies inside the closed border polygon (exact test: no proper
  crossing with any border edge, and every sub-piece midpoint inside or on the border). There are no
  obstacles to test against. A shapely `covers` cross-check agrees (0 segments not covered).
- **Comparison.** The set is shorter than the shortest stored set (45794, radial) by 3261.361698 m
  (0.8576%), and shorter than the shortest stored branched set (2800) by 4070.66 m. The relative margin
  is far above 1e-6 against every one of the 4 rows.
- **Feeder cap.** The object uses [22] feeders, which is <= [22], the feeders_per_root of the shortest stored set 45794.

## Official validator (optiwindnet 0.3.2, .venv-optiwindnet)
- **claim/object/G.pickle.**
  - It has 189 nodes and 188 edges, with name 'Hornsea One.1_OSS', T/R/B/C/D = 174/1/25/2/12,
    capacity 8 and topology branched.
  - Its VertexC is bit-identical to the DB nodeset blob, its border indices match the nodeset, and it has
    no obstacles.
  - `validate_routeset(G) == []`.
- **Graph rebuilt from claim/object/routeset-packed.json.** I rebuilt it with optiwindnet's own
  `db.storage.G_from_routeset`, using the DB nodeset row and the packed edges, clone2prime, C and D.
  - `validate_routeset == []`.
  - G_from_routeset did not raise its length-mismatch flag.
  - Its length is 377034.6924851112.
- **Same network across all three objects.** The G.pickle edge set equals the rebuilt edge set, and fnT
  is identical. The (u,v) set in segments.json equals the G edge set, and its coordinates equal
  VertexC[fnT[node]] at both ends. The lengths from all three objects agree exactly.
- **Negative controls on copies of G.pickle.** Setting capacity to 7 gives a violation
  ('κ = 7, max_load = 8'). Moving turbine 0 gives crossing violations. So the validator is not vacuous here.
- **Determinism.** I re-ran both checkers; the outputs are byte-identical (cmp). No __pycache__ was
  created in the claim folder, and the claim folder was not modified.

## Doubtful / notes (none affects the criterion)
- **Detours through turbine positions.** 12 detour clones place cable bends exactly at turbine positions
  (108, 121, 81, 88x2, 96, 84, 93x2, 94x2, 102), mostly on detoured feeders. A cable therefore touches a
  turbine coordinate without being electrically connected there. This is optiwindnet's standard
  PathFinder detour representation, the stored sets use the same scheme (e.g. 2800 has D=17 with clones
  of 93 and 94), and the validator accepts it. I note it but do not hold it against the claim.
- **Misleading `misc` in the packed object.** creator 'MILP.ortools.cp_sat', termination OPTIMAL,
  relgap 0.0, bound 376712.81 and runtime 0.31 s describe only the last neighbourhood sub-solve. The
  bound is not a bound for the full instance. This metadata should not be read as an optimality
  certificate, and CLAIM.md correctly does not claim optimality.
- **Handle differs.** The packed handle is 'Hornsea_One_1_OSS', while the stored rows use 'hornsea_1'.
  The instance is identified by the nodeset digest and name, which match, so this does not matter.
- **Zenodo status snapshot.** claim/status/zenodo-latest.json resolves versions/latest to record 23537067
  (the r26.10-v4 record itself). I did not re-query Zenodo (no network), so I cannot rule out a newer
  version after the snapshot.
- **Scope of this review.** This report does not establish the three-reviewer panel or the kit's
  mechanical gate. I did not update workspace report or log files; the caller owns those.

pass: true
