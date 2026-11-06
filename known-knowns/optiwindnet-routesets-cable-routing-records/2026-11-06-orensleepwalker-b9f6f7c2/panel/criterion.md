# Criterion skeptic review: claim-ho8 (OptiWindNet RouteSets, Hornsea One.1_OSS, capacity 8, X = branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

## What I checked and how
I wrote my own scripts before reading any author code (the claim ships none). They are in work-criterion/: `check_indep.py`, which uses no optiwindnet and reads only the DB and `object/segments.json`, and `check_own.py`, which runs the official validator, does the object cross-checks and applies the null model to the stored sets. Their outputs are in `indep.out` and `own.out`. The DB was decompressed from `references/optiwindnet-routesets-r26.10-v4.sqlite.xz` into the work folder and deleted afterwards.

## Clause-by-clause (success criterion, read literally)
1. **Release r26.10-v4.** sha256 of the `.xz` file is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which equals the bank value. Its md5 is 85faffb2e13600b017f1b583b259edd7, which equals the file checksum in `status/zenodo-latest.json`. The md5 of the uncompressed file is 5ad6bf0449dcbd9939f1ae03bee19016, which equals the r26.10-v4 entry in the record description. `status/zenodo-latest.json` is record 23537067 with `relations.version[0].is_last = true`, so it shows r26.10-v4 as the latest version. This is the author's snapshot. I made no live Zenodo call (no outward actions).
2. **Nodeset name without '!'.** The name is `Hornsea One.1_OSS`, with no '!' prefix. It has T=174, R=1, B=25, and constraint_groups = [25]: one border polygon and 0 obstacles.
3. **Topology X = branched.** The network is a single tree of 189 nodes and 188 edges, connected, with no duplicate edges. All 14 detour/contour clones have degree 2. After the clones are contracted, 11 turbines have degree 3, so the network is genuinely branched (not radial). The validator's topology field also reads `branched`.
4. **Same nodeset.** Every segment endpoint is a VertexC point. Turbine labels match `VertexC[i]` exactly, the root matches the last row, and all 174 turbines are present. The graph rebuilt from `object/routeset-packed.json` over the DB `NodeSet` has the same geometry and labels as `object/segments.json`. `object/G.pickle` has the same VertexC as the DB blob and the same edge set.
5. **validate_routeset.** It returns `[]` for the graph rebuilt from the packed JSON over the DB nodeset, and `[]` for `object/G.pickle`.
6. **Capacity.** There are 22 feeder subtrees with sizes 6 and 21×8 (max 8, sum 174).
7. **Containment.** Every segment is covered by the border polygon; the length outside is 0. Four segments touch the border line through contour nodes on border vertices 175 and 184, which is allowed. There are no obstacles. My own pairwise check found no proper crossings and no touches at non-endpoints. 11 segment pairs overlap collinearly: shared corridors leaving the root, and feeders that bend at detour nodes on turbines 88, 93 and 94. This is the release's own convention. Null model: every stored cap-8 set has the same kind of overlap (13 to 21 pairs) and also passes the validator.
8. **Length metric.** The sum of Euclidean segment lengths is 377034.6924851112 m. It is identical whether computed from the coordinates, from the labels, from the edge `length` attribute, or read from the header. Null model: for all four stored sets, the Euclidean segment sum recomputed with the same method equals the DB `length` (difference < 1e-9 relative). So the compared quantities are like-for-like and include detours.
9. **Strictly shorter than every stored set of topology branched or more restrictive.** Capacity 8 has four stored sets, all radial or branched, so all of them count:
   - 45794: radial, CPLEX, 380296.0542 m, [22] feeders
   - 2800: branched, CPLEX, 381105.3514 m, [22] feeders
   - 9636: radial, HGS, 383497.6637 m, [22] feeders
   - 8923: radial, LKH, 385884.6735 m, [22] feeders

   The claim beats all four by more than 1e-6 relative. The margin over the shortest is 3261.3617 m (0.8576% relative).
10. **Feeders.** At the single substation the claim uses 22 feeders, which equals the 22 of the shortest stored set (45794), so it does not exceed the limit. The count of 22 is the same whether taken from the validator graph's root degree or from my clone-contracted tree.
11. **Partial-win routing.** The claim is the full criterion (X = branched), not p1 or p2.

## Wording in CLAIM.md
Every number checks out: 377034.6925, 380296.0542, 381105.3514, the margin 3261.3617 m (0.858%), the feeders [22], and "174 turbines, 1 substation(s), 0 obstacle(s)". "Strictly shorter than every stored route set for that instance of any topology" is literally true, because all four stored cap-8 sets are radial or branched. CLAIM.md correctly disclaims optimality.

One caveat about the object's metadata (not the claim sentence): the `misc` of `object/routeset-packed.json` has `creator` MILP.ortools.cp_sat, `bound` 376712.81, `relgap` 0.0, `termination` OPTIMAL and `runtime` 0.31 s. Those describe only the last fixed-neighbourhood sub-solve. They are not a global bound, gap or runtime and must not be read as certifying optimality. The global branched bound in the release is still 362862.42 m, so the indicative gap remains about 3.8%.

The bank's pinned commit f3b19b4… was not checked, because I read the bank file only. criterion.txt reproduces the bank entry verbatim (I checked by string containment): the statement, success criterion, verification method, p1, p2, all three pitfalls and the status source.

## Verdict
The full success criterion for topology X = branched is met literally. The win is not subsumed: it beats the shortest stored set of any topology, not just the branched ones. The release is the latest version according to the shipped status snapshot.

confirmed_scope: For OptiWindNet RouteSets release r26.10-v4 (xz sha256 c78c8f3c…e3a), instance Hornsea One.1_OSS at capacity 8, the branched route set in object/ (174 turbines, 22 feeders at the single substation) passes validate_routeset with no violations, lies inside the site border (the site has no obstacles), and has a summed Euclidean length of 377034.6925 m, which is 3261.3617 m (0.858%) shorter than the shortest of the four stored capacity-8 route sets (id 45794, radial, 380296.0542 m, 22 feeders); optimality is not shown.

pass: true
