# Criterion skeptic report: optiwindnet-routesets-cable-routing-records, run 2026-11-09-0835

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Scope of review: CLAIM.md, REPRODUCE.md, criterion.txt, status/zenodo-latest.json, object/segments.json, object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz (all named relative to the claim folder), and the bank entry. I wrote every check myself; the claim ships no checker. Scripts and outputs are in panel/work-criterion/ (check.py, overlap.py, extra.py, nullpath.py and their .out files). The decompressed database was deleted afterwards; `xz -dc` the reference into work-criterion/rs.sqlite to rerun. Interpreter: .venv-optiwindnet (optiwindnet 0.3.2), run with `-I`, PYTHONDONTWRITEBYTECODE=1 and OMP_NUM_THREADS=1. No __pycache__ was created in the claim folder.

## Release identity and latest-ness
- sha256 of references/...sqlite.xz is c78c8f3c...e3a, which matches the bank. The md5 of the .xz is 85faffb2e13600b017f1b583b259edd7, which matches the file checksum in status/zenodo-latest.json. The md5 of the decompressed SQLite is 5ad6bf0449dcbd9939f1ae03bee19016, which matches the 26.10-v4 row in the record description.
- status/zenodo-latest.json gives record 23537067 (DOI 10.5281/zenodo.23537067), published 2026-10-21, `relations.version[0].is_last = true`. By that snapshot, r26.10-v4 is the latest version. Caveat: the snapshot has no retrieval timestamp, and I did not query Zenodo myself (no outward actions). So latest-ness holds only as far as this file shows.

## Instance
- The nodeset row named exactly `Race Bank.1_OSS` (first character 'R', so no '!' prefix) has T=91, R=1, B=12, constraint_groups [12], which means a border and no obstacles. The stored digest equals fingerprint(VertexC). This is the single-substation '.1_OSS' variant of Race Bank, not the as-built two-substation site. The criterion allows it literally (no '!'), and the bank statement explicitly counts '.1_OSS' variants among the non-'!' instances.
- Stored route sets for (nodeset, capacity 3): 4 in total.
  - 45770, MILP.pyomo.cplex, radial, length 155036.8792851718, feeders [31], relgap 0.333%, bound 153293.229, feeder_limit min_plus1
  - 9504, baselines.hgs, radial, length 155036.87928517183, feeders [31]. This ties 45770 for shortest. CLAIM.md does not mention it, but it changes nothing.
  - 8812, baselines.lkh, radial, length 155172.6133, feeders [31]
  - 2743, MILP.pyomo.cplex, branched, length 156071.6528, feeders [31], bound 153480.920, feeder_limit unlimited
- No other topology values exist for this instance.

## Clause-by-clause check (X = radial; X = branched also reported)
1. **Non-'!' nodeset:** yes.
2. **Topology of the object:** I took the 107 segments in segments.json and contracted the 16 clone nodes (1 contour, 15 detours, each of degree 2) to get a turbine-level graph. That graph is a tree on 92 nodes: all 91 turbines plus root -1. The maximum turbine degree, root link included, is 2 (31 turbines at degree 1, 60 at degree 2). Removing the root leaves 31 subtrees: 30 of 3 turbines and 1 of 1 turbine. Each subtree is a simple path hooked to the root at one end. **The object is genuinely radial**, and therefore also branched.
3. **Strictly shorter, by more than 1e-6 relative.** The Euclidean sum is 153796.94115396668 m.
   - Against the radial sets: 45770 and 9504 by 1239.9381 m (0.79977% of stored), 8812 by 1375.6721 m (0.887%).
   - Against the branched set: 2743 by 2274.7116 m (1.457%).
   - Every margin is far above 1e-6, so the object is shorter than every stored set of either topology.
4. **Feeders:** the object has 31 at root -1. The shortest stored set's feeders_per_root is [31], whether that set is taken as 45770 or 9504, and whether the comparison is radial-only or includes branched. 31 <= 31 holds.
5. **Same nodeset:** every segment endpoint equals VertexC of its node, or of its prime for clones, with 0.0 deviation. The pickle's VertexC equals the database blob exactly, and its border indices equal constraint_vertices. Its name is the same, with no obstacles, as in the nodeset. The packed record rebuilds against this nodeset with nodeset_digest enforced.
6. **validate_routeset:** I rebuilt G from routeset-packed.json with TerseLinks.to_routeset against the database nodeset.
   - It returns [] under both RADIAL and BRANCHED labels.
   - G.pickle returns [] as stored (BRANCHED) and [] after I relabelled it RADIAL. The RADIAL label adds the degree check.
   - The pickle, packed and segments edge sets are identical (107 links).
7. **Border and obstacles:** all 107 segments are covered by the border polygon (valid polygon, 1e-6 m tolerance). There are no obstacles, so that part is vacuous. All turbines and the substation are strictly inside the border, the closest turbine 105.5 m from it.
   - My pairwise intersection test found 7 collinear overlaps, all feeders sharing a corridor to a turbine position where they bend at a detour clone (segmented-feeder convention). Examples: root to turbine 41 shared by 3 cables, and a 17-32 corridor shared by 2. No segment crosses another, and none passes within 1 m of a turbine other than its endpoints.
   - Stored sets show the same convention (45770 has 43 such overlaps; all four stored sets pass validate_routeset), so this is accepted release practice, not a defect.
8. **Length:** the Euclidean segment sum is 153796.94115396668. The packed `length` is 153796.94115396673 and the G length is the same (relative difference 3e-16). This is the value I compared.

## Null models and sanity checks
- **Re-routing check:** I re-routed the stored 45770, 8812 and 2743 topologies with the 0.3.2 PathFinder. They reproduce their stored lengths exactly, so the win is not a PathFinder-version artifact. It comes from a different topology: 77 of 91 links shared with 45770.
  - The straight-line part also improves: the model objective goes from 153805.455 to 153313.915.
  - The detour overhead falls from 1231.4 m to 483.0 m.
- **Radial bound:** the object's terminal straight-line sum is 153296.104, which is 2.87 m above the radial MILP bound of 45770 (153293.229). That is consistent: the object does not beat a valid bound.
- **Branched bound:** the object's terminal straight-line sum is 184.8 m below the 2024 branched MILP bound of 2743 (153480.920). That bound therefore does not bound the feasible set accepted by the current validator. The difference likely comes from older model or link-set rules, which I did not investigate. This is a release-internal inconsistency, not a defect in the object, and the bank statement already calls such gaps indicative rather than certified.
- **Available links:** all 60 terminal-terminal links of the object are in the current available-link mesh A.

## Wording and metadata
- **X stated two ways:** CLAIM.md says X = radial in "Instance identity" and X = branched in the "Claimed:" line. The object satisfies both, so this is an inconsistency, not an overstatement. "Strictly shorter than every stored route set ... of any topology" is literally true for this instance. Not mentioning the tied HGS set 9504 is an omission with no effect.
- **Misleading metadata in the packed object and the pickle:**
  - **Topology label:** `misc.topology` / `graph['topology']` = "branched", although the object is radial. The label is a weaker true statement, but it disagrees with the X = radial claim and with segments.json, which says "radial". G_from_routeset would read it as branched and skip the radial degree check.
  - **Optimality fields:** `bound` = `objective` = 153313.91, `relgap` 0.0, `termination`/`strategy` "OPTIMAL", `creator` "MILP.ortools.cp_sat", `runtime` 1.55 s, and method_options mip_gap 0 / time_limit 30. These describe the last pinned fix-and-optimise sub-solve, not the instance. Stored as-is, they would assert a certified 0% gap that nobody has proven: the only valid bound is 45770's 153293.23, a gap of at least 0.013% on the straight-line objective.
  - None of these fields is part of the success criterion. They must not be cited, or stored as evidence, of optimality.

## Verdict
The full success criterion is met literally for instance (Race Bank.1_OSS, capacity 3) with X = radial, and also with X = branched. This is a full win, so no partial-win subsumption issue arises. The caveats are the misleading packed metadata (branched label, relgap 0 / OPTIMAL from a restricted sub-solve) and latest-ness resting on an undated snapshot. Neither changes whether the route set meets the criterion.

confirmed_scope: For release r26.10-v4 (as recorded latest in status/zenodo-latest.json), instance nodeset "Race Bank.1_OSS" (the single-substation variant of Race Bank, no '!' prefix) with capacity 3, the route set in object/ is radial (every turbine has degree at most 2) with total Euclidean segment length 153796.9412 m, which is shorter than every stored route set for that instance (shortest stored radial 155036.8793 m, ids 45770 and 9504, by 1239.9381 m or 0.800%; shortest stored branched 156071.6528 m, id 2743), uses 31 feeders (equal to the shortest stored set's [31]), carries the same nodeset, passes optiwindnet 0.3.2 validate_routeset with no violations, and lies entirely inside the site border (no obstacles exist); no claim of optimality is confirmed, and the packed metadata's "branched" label and relgap 0.0 / OPTIMAL fields describe a restricted sub-solve, not the instance.

pass: true
