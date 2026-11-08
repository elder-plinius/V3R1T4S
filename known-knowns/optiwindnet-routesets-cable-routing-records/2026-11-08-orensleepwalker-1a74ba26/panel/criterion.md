# Criterion review: optiwindnet-routesets-cable-routing-records, run 2026-11-08-1554

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Claimed: the full success criterion, one instance, topology X = branched. Nodeset "Hornsea Two West", capacity 9.
Scripts: panel/work-criterion/{q1,q2,q3,check.py,val.py,parity.py}. These are my own scripts; the claim ships none. They ran with the optiwindnet 0.3.2 venv, python -I, PYTHONDONTWRITEBYTECODE=1 and OMP_NUM_THREADS=1. I deleted the decompressed SQLite after use. There is no __pycache__ in the claim folder.

## Reference identity
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz has sha256 c78c8f3c...05e3a, which equals the bank value. Its md5 is 85faffb2e13600b017f1b583b259edd7, which equals the file checksum in status/zenodo-latest.json. The decompressed SQLite has md5 5ad6bf0449dcbd9939f1ae03bee19016, which equals the 26.10-v4 row of the release table in the record description.
- Latest-ness: status/zenodo-latest.json describes record 23537067 (26.10-v4) with `relations.version[0].is_last = true`. The snapshot carries no fetch timestamp, and I took no outward action, so I can confirm latest-ness only as of that snapshot.

## Clause-by-clause
1. **Nodeset name has no '!' prefix.** Pass. Exactly one nodeset is named 'Hornsea Two West'. The 120 other "Hornsea Two West" nodesets all start with '!'. The nodeset has T=110, R=1, B=9, constraint_groups [10] and 0 obstacles. The substation (-1) is itself a vertex of the border polygon.
2. **Topology X = branched.** Pass. I contracted the 2 detour clones and got 110 electrical links that form a single tree from the root, with every turbine reached exactly once and no cycles. The 13 feeder subtrees have sizes 6, 5 and eleven of 9, all <= 9. Seven turbines have degree 3, so the set is genuinely branched and not a radial set relabelled. The validator infers `branched` from the edges.
3. **Stored sets for (Hornsea Two West, capacity 9).** There are 4 rows, and I counted all of them because radial counts for branched:
   - 4305 baselines.hgs, radial, 192886.72928393926, feeders [13]
   - 44553 MILP.pyomo.cplex, radial, 192886.72928393926, feeders [13] (tied for shortest)
   - 100 MILP.pyomo.cplex, branched, 193222.83416271958, feeders [13]
   - 4181 baselines.lkh, radial, 194384.99910752499, feeders [13]

   All 4 pass validate_routeset, and the length recomputed from each graph equals its stored value.
4. **Strictly shorter than every stored set by more than 1e-6 relative.** Pass. The claim length is 191786.95446995908. The margin is 1099.7748 m (5.70e-3 relative) to the shortest stored set and 1435.88 m (7.43e-3) to the best stored branched set.
5. **Feeders at each substation <= the shortest stored set's feeders_per_root.** Pass. The claim uses 13 feeders. Both tied shortest sets also have [13], and so do all four stored sets. 13 = ceil(110/9) is the minimum possible, so the result does not come from relaxing the feeder limit.
6. **Same nodeset.** Pass. The VertexC in G.pickle is bit-identical to the DB blob (shape 120x2). The pickle's border index list equals the DB's constraint_vertices, and it has no obstacles. Every endpoint in segments.json equals the VertexC coordinate of its node, or of the clone's prime (max deviation 0). The link set in segments.json equals the link set in routeset-packed.json, which equals the edge set of G.pickle (112 links).
7. **validate_routeset reports no violations.** Pass. I got [] for G.pickle and [] for a G rebuilt from routeset-packed.json plus the DB NodeSet through G_from_routeset. That rebuild records no length_mismatch_on_db_read.
8. **Inside the border and outside obstacles.** Pass. With shapely, all 112 segments are `contains`-ed by the border polygon, which is valid with area 2.71e8 m². There are no obstacles, so that half is vacuous. My own pairwise check finds no proper crossings. The only contacts are at clone/prime coincident points (turbines 49 and 46). There is one collinear overlap: feeder 47 routes via a clone at turbine 46 and shares the corridor of cable 46 to the root.

   Null model: the stored best sets 4305 and 44553 have the identical clone pattern (clone2prime [49,46], clones adjacent to -1/35 and -1/47, edge (46,-1) present). The claim uses no convention the stored sets do not use, and the doubled corridor adds length rather than saving it.
9. **The compared length is the Euclidean segment sum.** Pass. The sum from VertexC plus the packed links is 191786.954470. The sum from segments.json is 191786.954470. The stored `length`, the pickle `size(weight='length')` and `length_sum_euclid_m` all match with a difference of 0.000.
10. **Sanity checks against bounds.** The claim's straight-line objective of 191680.09 is at or above the release's best branched MILP bound of 186907.20 (id 100). The claim's length sits 2.54% above that bound. Nothing is inconsistent.

## Wording
CLAIM.md is accurate as written. Its numbers (lengths, ids, solvers, feeders, 0.570%, 1099.7748 m) all reproduce. It explicitly disclaims optimality, a new method and any other instance.

## Misleading metadata in the packed object (defect; does not change the criterion verdict)
routeset-packed.json and G.pickle carry metadata from the final 30 s CP-SAT sub-solve of the fix-and-optimise search, not from the search as a whole:
- creator "MILP.ortools.cp_sat"
- runtime 0.284761 s
- misc.termination "OPTIMAL" and solver_details.strategy "OPTIMAL"
- misc.relgap 7.3e-12
- misc.bound 191680.0877

Read with the release's own semantics (bound/relgap = certified gap), this presents the route set as a near-zero-gap, proven-optimal CP-SAT solve. That is false: the only global branched bound is 186907.20, a gap of about 2.5%. If the object were ingested with store_G, gap statistics would be corrupted. Before reuse, these fields should be stripped or relabelled (LNS, total runtime, no global bound).

A minor point: the handle is "Hornsea_Two_West", while the DB stores "hornsea2w" for this instance.

The criterion constrains the route set (nodeset, topology, length, feeders, validity, containment), not misc metadata. I therefore record this as a required correction, not a failure.

## Verdict
Every clause of the full success criterion holds literally for X = branched. The win is not subsumed by any stored set of this instance, and the margin is 5.7e-3 relative, far above 1e-6. The scope is limited to this instance and release, with latest-ness as of the shipped snapshot only.

confirmed_scope: For release r26.10-v4 (record 23537067, latest per the shipped status snapshot), instance (Hornsea Two West, capacity 9), the claimed branched route set has Euclidean length 191786.9545 m, which is 1099.7748 m (0.570%) shorter than the shortest of all four stored route sets (radial ids 4305/44553, 192886.7293 m); it uses 13 feeders (equal to their [13]), passes validate_routeset with no violations, and lies within the border of the unchanged nodeset, which has no obstacles. This confirms no optimality, and the bound/relgap/OPTIMAL fields in the packed object are sub-solve artefacts, not a certificate.

pass: true
