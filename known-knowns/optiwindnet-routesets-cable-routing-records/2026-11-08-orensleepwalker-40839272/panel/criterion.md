# Criterion skeptic report: claim-la9

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Target: optiwindnet-routesets-cable-routing-records. Claimed: the FULL success criterion, topology X = branched, instance "London Array.1_OSS", capacity 9.
Scripts (own, written fresh; the claim ships none): panel-la9/work-criterion/q.py, check.py, stored.py. Run with .venv-optiwindnet python -I (optiwindnet 0.3.2), PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1. Database decompressed into the work folder (rs.sqlite); the claim folder was not written to and has no __pycache__.

## Reference and release identity
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: sha256 c78c8f3c...e3a (matches the bank), md5 85faffb2... (matches the files entry in status/zenodo-latest.json); the decompressed SQLite md5 is 5ad6bf0449dcbd9939f1ae03bee19016, which matches the r26.10-v4 row in the record description.
- status/zenodo-latest.json: id 23537067, relations.version is_last = true, file key optiwindnet-routesets-r26.10-v4.sqlite.xz. According to this file, r26.10-v4 is the latest version. Limitation: the claim author supplied this file and it carries no fetch timestamp. I made no outward request, so I could not re-check latest-ness independently.
- criterion.txt: the success criterion, partial wins, statement, verification method and pitfalls each match the bank entry word for word.

## Clause-by-clause check (literal)
1. Nodeset name has no '!' prefix: "London Array.1_OSS" (exactly one nodeset row with that name; T=175, R=1, B=9, constraint_groups [9], so one border polygon and no obstacles). PASS.
2. Topology X = branched: misc.topology = "branched". In my own graph from the edges, the maximum turbine degree is 3 (4 turbines have degree >= 3), so the set is a genuine tree and not just a path set. PASS.
3. Comparison set: every routeset row with nodes_id = that nodeset and capacity = 9. There are 4 rows, all topologies counted, because radial counts for branched. I rebuilt each one and recomputed its Euclidean length, which agrees with the stored length field:
   - 44577 MILP.pyomo.cplex radial 154359.160373 m, feeders [20], relgap 1.05%
   - 9629 baselines.hgs radial 154359.160373 m, feeders [20] (ties with 44577 to about 1e-10 m)
   - 2794 MILP.pyomo.cplex branched 154403.535043 m, feeders [20], bound 151435.06, relgap 1.91%
   - 8917 baselines.lkh radial 158074.869212 m, feeders [20]
   The new set is 153957.988867 m. Its relative margin over the shortest stored set (44577 and 9629) is 2.598948e-3 (401.1715 m), far above 1e-6. Over 2794 it is 445.5462 m. PASS (strictly shorter than every stored set).
4. Feeders: the new set has [20] at the single substation. The shortest stored set's feeders_per_root is [20]. 20 = ceil(175/9) is also the minimum possible, so no feeder relaxation is involved. PASS.
5. Same nodeset: VertexC in object/G.pickle (185x2) equals the DB VertexC blob element for element, and its border equals constraint_vertices[:9]. Every endpoint in object/segments.json is a DB VertexC point: all 175 turbines, the root (index 184), and detour clones that sit on turbine positions 73, 91, 73 and 140. object/routeset-packed.json rebuilt on the DB nodeset (TerseLinks, same path as G_from_routeset) gives the same geometric edge set as the pickle and as segments.json. PASS.
6. validate_routeset: returns [] on the pickle and on the graph rebuilt from the packed JSON. PASS.
7. Independent structure check (my own code, on the graph rebuilt from the packed JSON, cross-checked with segments.json): 180 nodes and 179 edges forming a single connected tree; the 20 feeder subtrees hold 7, 8, 8, 8 and 16 x 9 turbines, which sum to 175 with a maximum of 9. PASS.
8. Crossings: a pairwise shapely check finds no proper crossings. It does find 4 collinear overlaps: three cables run root to turbine-73 position, two of them bending at detour nodes there, and two run 73-position to 91-position. Stored sets 44577, 9629 and 2794 have the same pattern: the same clone2prime [73, 91, 73] and 4 overlaps each. The release itself describes this convention (a feeder bending at a detour node on a turbine), and the validator accepts it. So the overlaps are not a new device for gaining length. No segment passes within 1 m of a turbine that is not one of its endpoints. PASS.
9. Border and obstacles: border polygon valid (area 1.224e8 m2); all 179 segments are covered by it, with 0.0 m of length outside. There are no obstacle polygons. PASS.
10. Length = Euclidean segment sum: 153957.9888674163 m from segments.json. This equals G.size(weight='length'), the packed "length" and segments.json length_sum_euclid_m, with a difference of 0.0. Stored lengths were recomputed the same way. PASS.

Null-model and stretch checks:
- No relaxed feeder limit (20 is the minimum).
- No different length accounting (both sides recomputed identically, detours included).
- No instance alias: the 2-substation "London Array" and the '!'-augmented nodesets are different instances.
- Consistent with bounds: 153957.99 is above the stored branched CPLEX bound 151435.06, and the gain of 0.26% is inside the stored 1.05% to 1.91% gaps, so the result is plausible and not suspicious.
- This is the full criterion, not a partial win, and it is not subsumed: no stored set for the instance is as short.

## Wording and metadata problems (do not break a criterion clause, but must be fixed or disclosed)
- Misleading metadata in object/routeset-packed.json and in the G.pickle graph attributes:
  - creator "MILP.ortools.cp_sat", runtime 4.951049 s, misc.termination "OPTIMAL", solver_details.strategy "OPTIMAL", bound 153949.5129, relgap 2.95e-11, warmstart "MILP.ortools.cp_sat".
  - These come from the final 30 s restricted large-neighbourhood sub-solve, in which most links were pinned. They are not a run on the whole instance.
  - The bound is NOT a valid lower bound for the instance; the only stored instance bound is 151435.06. Read as written, the object claims certified optimality (gap about 0), which contradicts CLAIM.md's "Not claimed: optimality".
  - The runtime understates the search effort.
  - Anyone loading this object into the RouteSets schema would get a false certified-optimal record.
- The packed handle "London_Array_1_OSS" differs from the release's handle for this nodeset's route sets ("london_1"). This is cosmetic.
- The pickle method_options embed a local absolute path (funfile). This is cosmetic.
- CLAIM.md wording: every number I checked matches (153957.9889; 154359.1604, id 44577; 401.1715 m; 0.260%; 154403.5350, id 2794; feeders [20]; 0 obstacles). I found no overstatement in CLAIM.md. Optimality is explicitly disclaimed there.

## Verdict
Every clause of the full success criterion holds literally for topology X = branched. Release latest-ness rests on the author-supplied status/zenodo-latest.json (is_last = true). The misleading optimality and bound metadata in the packed object must be stripped or relabelled before anyone stores or publicises the object. Optimality must not be stated.

confirmed_scope: For OptiWindNet RouteSets release r26.10-v4 instance "London Array.1_OSS" with capacity 9 (175 turbines, 1 substation, no obstacles), the branched route set in object/ has a Euclidean segment-sum length of 153957.9889 m with 20 feeders, passes optiwindnet 0.3.2 validate_routeset with no violations, lies inside the site border, and is 401.1715 m (0.2599%) shorter than the shortest of the 4 stored route sets for that instance (radial ids 44577 and 9629, 154359.1604 m, feeders [20]), with no optimality established; the packed object's bound, relgap, termination and runtime fields describe only a final restricted sub-solve.

pass: true
