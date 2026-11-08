# Criterion skeptic report: claim-la7

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Target: optiwindnet-routesets-cable-routing-records. Claimed: full success criterion, instance (London Array.1_OSS, capacity 7), topology X = branched.
My scripts (in work-criterion/): verify.py (length, coordinates, containment), topo.py (own forest/capacity/feeder/crossing checks), official.py (optiwindnet 0.3.2 rebuild + validate_routeset), dup.py (same-geometry nodesets, margins), q1.py/q2.py (raw sqlite reads). The decompressed SQLite was deleted afterwards.

## Release identity and latest-ness
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: sha256 c78c8f3c...05e3a (matches bank), md5 85faffb2...edd7 (matches status/zenodo-latest.json file checksum); uncompressed md5 5ad6bf0449dcbd9939f1ae03bee19016 (matches the 26.10-v4 row in the Zenodo description).
- status/zenodo-latest.json: record 23537067, DOI 10.5281/zenodo.23537067, relations.version is_last = true, single file = this .xz. Consistent with the bank's pinned record. Caveat: this is a captured snapshot with no fetch timestamp; I made no outward request, so latest-ness is as of that snapshot only.

## Clause-by-clause (literal)
1. Nodeset name without '!': "London Array.1_OSS" (no '!' prefix; a real-site .1_OSS variant). T=175, R=1, B=9, constraint_groups [9] = border only, 0 obstacles. PASS.
2. Topology X = branched: own contracted graph is a single tree over 175 turbines + root; turbines 3 and 19 have degree 3 (not radial). Rebuilt G carries topology 'branched'. PASS.
3. Stored sets for (London Array.1_OSS, 7) — exactly 4 rows: 9627 baselines.hgs radial 173966.44199878 [25]; 45872 MILP.pyomo.cplex radial 173966.44199878 [25] (tie for shortest); 2792 MILP.pyomo.cplex branched 174227.81627684 [26]; 8904 baselines.lkh radial 188458.03261499 [25]. All radial and branched rows count (radial is more restrictive).
4. Strictly shorter by > 1e-6 relative than EVERY stored set: claimed 173753.9532429 m; margin vs shortest (9627/45872) 212.4888 m = 1.2214e-3 relative (0.122%); vs best branched 2792 473.86 m (0.272%). PASS.
5. Feeders <= shortest stored set's feeders_per_root: cap = [25] (both tied shortest sets have [25]); claim uses 25 at root -1 (25 subtrees of exactly 7 turbines; 25 = ceil(175/7) is also the minimum possible). PASS. (Branched 2792 used 26; correctly not used as the cap.)
6. Same nodeset: every segment endpoint in object/segments.json coincides exactly (distance 0) with a VertexC entry of the stored nodeset; turbine/root labels match their VertexC coordinates; the 5 extra labels 184-188 are detour clones of turbines 109, 91, 73, 109, 55 (clone2prime), each degree 2. object/G.pickle VertexC is array-equal to the stored blob, border = vertices 175..183, obstacles None. PASS.
7. validate_routeset: G rebuilt by G_from_routeset from object/routeset-packed.json + the stored NodeSet -> []; object/G.pickle -> []; pickle and packed edge sets identical, pack_G(pickle) reproduces packed edges and length. The four stored sets also validate [] (sanity). PASS.
8. Own topology/capacity: 181 nodes/180 edges, connected tree; every turbine present once; max subtree 7 <= capacity 7. Own pairwise crossing check: no proper crossings; the only intersections are collinear overlaps of feeders routed through clone nodes on turbines 109, 73, 55, 91 (the release's "bend at a detour node on the turbine" convention; stored set 9627 uses clones on the same turbines 109, 55, 91, 73). No segment passes within 1 mm of a non-endpoint turbine. PASS.
9. Inside border / outside obstacles (shapely): all 180 segments covered by the border polygon (tol 1e-6 m), none touches the boundary; no obstacles exist. PASS.
10. Length = Euclidean segment sum: own sum over segments.json = 173753.953243 m, identical (diff 0.0) to packed length, segments.json length_sum_euclid_m, rebuilt G.size(weight='length') and the pickle. This is the value compared. PASS.

## Null models / subsumption
- Only other nodeset with identical turbine coordinates is "London Array" (R=2, a different instance; its capacity-7 best is 165931.24 m branched with [12,14]); not the same (nodeset, capacity) instance, so it does not subsume the win.
- Claimed length is 1.75% above the release's best branched MILP bound for the instance (170760.98, straight-line), so no inconsistency with a known lower bound.
- The win is not obtained by relaxing feeders (minimum 25 used) or by changing the nodeset.

## Wording
- CLAIM.md is accurate: numbers, ids, ties (9627/45872, disclosed in provenance), feeders, 0 obstacles, degree 3 all reproduce. "Detours included" is correct (5 clone segments are in the sum). No optimality claimed. No overstated wording found.

## Misleading metadata in object/routeset-packed.json (caveat, not a criterion clause)
- creator "MILP.ortools.cp_sat", misc.termination "OPTIMAL", solver_details.strategy "OPTIMAL", relgap 0.0, bound = objective = 173707.43, runtime 13.5 s, warmstart "baselines.hgs" describe only the final fix-and-optimise CP-SAT sub-solve (most links pinned), not the whole search. If ingested as a dataset record, it would read as a certified optimum with instance bound 173707.43; no such global bound exists (the release's branched bound is 170760.98), and the runtime/warmstart do not reflect the LNS run. These fields should be stripped or relabelled before any submission upstream. The route set itself is unaffected.

## Partial wins
Not applicable: full criterion claimed and met; p1 (augmented '!' instance) and p2 (radial) do not describe this result.

confirmed_scope: For OptiWindNet RouteSets r26.10-v4 instance (London Array.1_OSS, capacity 7), the branched route set in object/ has a Euclidean segment-sum length of 173753.9532 m, 212.49 m (0.122%) shorter than every one of the 4 stored route sets (shortest: radial ids 9627 and 45872 at 173966.4420 m), uses 25 feeders (cap 25), is on the identical stored nodeset, passes optiwindnet 0.3.2 validate_routeset with no violations, and lies wholly inside the site border (no obstacles exist), with release identity checked against the hashes and a captured Zenodo latest-version snapshot rather than a live query.

pass: true
