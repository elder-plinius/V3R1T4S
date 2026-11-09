# Criterion review: optiwindnet-routesets-cable-routing-records, run 2026-11-07-0826

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Role: criterion skeptic. I wrote my own checks before looking at anything the author produced. The claim ships no code. My scripts are in panel/work-criterion/: q_stored.py, check_geom.py, check_validator.py and null_ew.py. They read the release from references/optiwindnet-routesets-r26.10-v4.sqlite.xz, decompressed into work-criterion/db/ and opened read-only with Python sqlite3. The claim folder was not modified and contains no __pycache__.

## Criterion text
criterion.txt matches bank entry `optiwindnet-routesets-cable-routing-records` word for word. I checked these fields: statement, success_criterion, partial_wins p1 and p2, verification_method, all three pitfalls, and status_source.

## Clause-by-clause check (claimed: full criterion, topology X = branched)

1. **Release identity.** The sha256 of the .xz file is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches the criterion. Its md5 is 85faffb2e13600b017f1b583b259edd7, which matches the file checksum in status/zenodo-latest.json. That status file is record 23537067, revision 4, and has `relations.version[0].is_last = true`, so it is the latest version as of the snapshot. The DB holds 49,204 routeset rows, matching the release description. Limitation: the status file carries no fetch timestamp, and I made no outward request, so "latest" is confirmed only as of that snapshot.
2. **Nodeset without '!'.** The nodeset is `Hornsea One.1_OSS`, with T=174, R=1, B=25, constraint_groups [25] and landscape_angle 3.4. It has one constraint group, the border (vertices 174-198), and no obstacles. Under optiwindnet's L_from_nodeset, obstacles exist only when there is more than one group.
3. **Stored sets for (nodeset, capacity 12).** There are exactly four:
   - 45373: radial, MILP.pyomo.cplex, 309220.7062 m, feeders [15], feeder_limit min_plus1
   - 2805: branched, MILP.pyomo.cplex, 311308.1399 m, feeders [16], feeder_limit unlimited
   - 9645: radial, HGS-CVRP, 312888.3176 m, feeders [15]
   - 8929: radial, LKH-3, 318718.8555 m, feeders [15]

   For X = branched, all four count, because radial is more restrictive. The shortest is 45373, so the feeder cap is 15. This matches CLAIM.md.
4. **Topology.** After contracting the one border clone, the object is a spanning forest: 175 nodes, 174 logical edges, no cycle, all 174 turbines reached from the root. Turbine degrees are deg1: 24, deg2: 141, deg3: 9, so it is a genuinely branched tree. The official validator accepts it as branched. When I relabelled the same object as radial, the validator rejected it ("radial subtrees must be simple paths"), which shows the validator does test the shape.
5. **Strictly shorter by more than 1e-6 relative.** The recomputed length is 307472.119088 m. It is the same value whether computed from the coordinates in segments.json, from the DB VertexC, or from G.size(weight='length'), and it equals the stated value. Margins against each stored set:
   - 45373: 1748.5872 m (0.5655%)
   - 2805, the shortest stored branched set: 1.232%
   - 9645 and 8929: larger still

   All exceed 1e-6.
6. **Feeders.** The object has 15 feeders at the single substation. Subtree loads are 10, 10, 11, 11 and eleven subtrees of 12, summing to 174, all at most capacity 12. 15 is at most the cap of 15, which is set by the shortest stored set, 45373. The shortest stored branched set uses 16, but the cap is correctly taken from 45373, and the claim does not use 16.
7. **Same nodeset.** Every segment endpoint matches the DB VertexC exactly, with maximum deviation 0. The one clone, node 199, maps to border vertex 175, as given by clone2prime. VertexC in G.pickle is array-equal to the DB blob, and the pickle's border is vertices 174..198 with obstacles None. segments.json, the packed edges and G.pickle all have the same 175-edge set.
8. **validate_routeset.** I rebuilt G two ways and ran optiwindnet 0.3.2 `validate_routeset` on each:
   - DB nodeset plus routeset-packed.json, through optiwindnet.db.storage.G_from_routeset: [] (no violations).
   - G.pickle, loaded with a restricted unpickler that allows only networkx, numpy, optiwindnet.types and bitarray classes: [] (no violations).

   As a control, the four stored sets also validate with [], and their recomputed lengths equal their stored `length` exactly. So stored and claimed lengths are measured the same way, detours included.
9. **Border and obstacles (shapely).** The border polygon is valid, with area 407.35 km². Every turbine and the substation lie inside it. All 175 segments are covered by the polygon exactly, with no tolerance needed. No segment runs along the boundary. There are no obstacles, so that part is vacuous.
10. **Crossings (my own check).** Over all segment pairs I found no proper crossings or overlaps. No segment passes within 1 m of a turbine or substation that is not its own endpoint. The single detour, 115 -> border vertex 175 -> 39, is needed: the straight 115-39 chord leaves the border. The detour adds 19.03 m, and that is counted in the compared length.
11. **Length is the compared value.** Yes. The compared value is the sum of Euclidean segment lengths, including the detour.

## Null model
Cheap optiwindnet Esau-Williams baselines on the same location, segmented feeders, capacity 12, all valid:
- esau_williams: 341998 m, 16 feeders
- biased_EW: 342447 m, 17 feeders
- rootlust: 330385 m, 16 feeders

None of these comes close to the stored best, so a trivial heuristic does not reproduce the improvement. The weak point is the stored branched result. Its only entry, 2805, has a 4.4% stored relgap and a branched bound of 297640.80. The object is still 3.3% above that bound, so the win is real but not near a certified optimum.

## Wording and metadata
- The numbers and qualifiers in CLAIM.md are accurate: lengths, ids, feeders, the 0.565% margin, the "0 obstacle(s)" note, and "Not claimed: optimality".
- "Independent processes with different seeds reached the identical route set" is provenance only. I did not verify it, and it adds nothing to the evidence.
- **Misleading metadata in object/routeset-packed.json and G.pickle:**
  - The `misc` fields read `termination: "OPTIMAL"`, `relgap: 0.0`, `bound: 307472.119...` equal to `objective`, `solver_details.strategy: "OPTIMAL"`, `mip_gap: 0.0` and `runtime: 1.64` s.
  - CLAIM.md's own provenance says these describe only the last neighbourhood sub-solve, in which most links were pinned. They are not a global certificate. The release's own branched bound for this instance is 297640.80, and nothing in the claim certifies optimality.
  - If this object were ingested into a RouteSets-style database, gap analyses would wrongly count it as a proven-optimal branched solution.
  - `warmstart: "MILP.ortools.cp_sat"` and `creator: "MILP.ortools.cp_sat"` hide that the search started from the CPLEX set 45373.
  - The handle `Hornsea_One_1_OSS` differs from the release handle `hornsea_1`. This is cosmetic.

  None of this affects any clause of the criterion, but these fields should be removed or annotated before the object is shared.

## Verdict
Read literally, every clause of the full success criterion holds for X = branched. The binding comparison is with the radial CPLEX set 45373, which the criterion explicitly includes. The result is a full win, not one of the enumerated partial wins (p1 needs a '!' nodeset; p2 needs a radial set).

confirmed_scope: For release r26.10-v4 (sha256 c78c8f3c...e3a, the latest Zenodo version per status/zenodo-latest.json), instance "Hornsea One.1_OSS" with capacity 12, the branched route set in object/ has a recomputed Euclidean length of 307472.1191 m, detours included, which is shorter than all four stored route sets of that instance (best: radial id 45373, 309220.7062 m, by 0.5655%) while using 15 feeders (cap 15), passing validate_routeset with no violations, and lying entirely inside the site border (the nodeset has no obstacles); no optimality is established, and the object's misc "OPTIMAL/relgap 0/bound" fields refer only to a restricted sub-solve.

pass: true
