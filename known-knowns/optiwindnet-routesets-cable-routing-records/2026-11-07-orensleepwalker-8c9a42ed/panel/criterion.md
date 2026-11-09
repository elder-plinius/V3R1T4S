# Criterion review: claim-ho5 (Hornsea One.1_OSS, capacity 5, topology X = branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Role: criterion skeptic. My scripts are in work-criterion/ (check_segments.py, validate.py, nullmodel.py). I wrote them before reading any author code; the claim ships none. The decompressed database copies I worked from have been deleted. Rebuild them from references/optiwindnet-routesets-r26.10-v4.sqlite.xz.

## Criterion text
- criterion.txt quotes the bank entry `optiwindnet-routesets-cable-routing-records` verbatim. I checked this by substring match against repo/bank/targets.json for the success criterion, statement, verification method, p1, p2, all three pitfalls and the status source. The bank repo HEAD is f3b19b47..., the same as the pinned commit.
- Claimed level: the FULL success criterion with X = branched. No partial win is claimed or needed.

## Clause-by-clause check (literal)
1. **Release identity.** sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz is c78c8f3c...05e3a, matching the bank. Its MD5 (85faffb2...) matches the file checksum in status/zenodo-latest.json. The decompressed MD5 is 5ad6bf0449dcbd9939f1ae03bee19016, matching the 26.10-v4 row of the Zenodo release table.
2. **Latest release.** In status/zenodo-latest.json, record id 23537067 has `relations.version[0].is_last = true`, and the record was modified 2026-10-21. Limit: the snapshot carries no retrieval timestamp, and I made no live request, so "latest" holds only as of that snapshot.
3. **Nodeset name.** The nodeset is 'Hornsea One.1_OSS', which has no '!' prefix. It has T=174, R=1, B=25, and constraint_groups [25], so it has a border and 0 obstacles. The nodeset name is unique (unique index).
4. **Stored comparison set.** The release stores 4 route sets for (Hornsea One.1_OSS, capacity 5), and all count for X = branched:

   | id | topology | creator | length (m) | feeders |
   |---|---|---|---|---|
   | 44834 | radial | MILP.pyomo.cplex | 507652.1192 | [35] |
   | 2798 | branched | MILP.pyomo.cplex | 507673.2764 | [35] |
   | 9633 | radial | baselines.hgs | 509207.2549 | [35] |
   | 8921 | radial | baselines.lkh | 527587.2778 | [35] |

   No ringed or other topology is stored, so the "more restrictive" quantifier is fully covered. Each stored length equals its recomputed Euclidean polyline length, which confirms that stored lengths include detours.
5. **Length.** My own sum of Euclidean segment lengths over object/segments.json (204 segments) is 506483.642108 m. This equals G.size(weight='length') from both the rebuilt packed object and G.pickle, the packed `length` field, and the segments.json field. Margin against the shortest stored set (44834) is 1168.4771 m, a relative margin of 2.3017e-3, which is above 1e-6. Against the stored branched best (2798) the relative margin is 2.343e-3. The compared value is the recomputed Euclidean length.
6. **Topology branched.** I contracted the 30 degree-2 clone/detour nodes and got 174 logical links for 174 turbines. All turbines are reachable from the root and there are no cycles, so the network is a forest. Every feeder subtree holds 4 or 5 turbines (capacity 5). The maximum turbine degree is 3, and 6 of the 35 feeder subtrees branch. So the object is a genuine branched set, not a relabelled radial one. The topology attribute is BRANCHED.
7. **Feeders.** The substation (-1) has 35 feeders. The shortest stored set (44834) has feeders_per_root [35], so 35 ≤ 35 holds. 35 = ceil(174/5) is also the minimum possible.
8. **Same nodeset.**
   - Every segment endpoint coincides exactly (zero deviation) with a VertexC point: a turbine, a border vertex or the root.
   - Each turbine and root label sits at its own VertexC coordinate.
   - G.pickle's VertexC is identical to the DB blob, and its fingerprint digest equals the nodeset digest. Its border array is identical, and it has no obstacles, as in the DB.
   - The geometry of segments.json, the packed object (rebuilt through optiwindnet's own G_from_routeset after I inserted it into a copy of the DB) and G.pickle are pairwise identical.
9. **validate_routeset.** It returns [] for the packed object rebuilt via G_from_routeset, and [] for G.pickle. I loaded the pickle with a restricted unpickler allowing only networkx, numpy, bitarray and optiwindnet. As a null model, all 4 stored sets also return [].
10. **Border and obstacles.** All 204 segments are covered by the border polygon (shapely covers, exact, no tolerance needed). There are no obstacles to test.
11. **Independent crossing check.** My pairwise check found 0 proper crossings and 0 T-touches. There are 43 collinear overlaps, in 10 shared corridors, for example 8 cables on the root-to-turbine-90 corridor. Null model: the stored sets show the same pattern (44834: corridor groups [8,7,3,2,...], 57 overlaps; 2798: 41 overlaps). This is the release's shared-corridor and detour convention, and the official validator accepts it. It is not a defect specific to this claim.
12. **Sanity against bounds.** The claimed straight-line objective (502825.92) and length are above the stored branched MILP bound for this instance (497716.26, id 2798). There is no sign of a relaxed model.

## Wording in CLAIM.md
- The numbers, ids, feeder counts, margin (1168.4771 m, 0.230%) and "every stored route set ... of any topology" are all accurate (4 stored sets).
- "independent processes with different seeds reached the identical route set" and the LNS description are provenance only and cannot be verified from the folder. They are labelled as provenance, and the criterion does not need them.
- CLAIM.md says it does not claim optimality, which is correct. It does not disclose the misleading metadata described in the next section.

## Metadata inside the packed object that could mislead (does not affect the criterion)
- `misc.bound` = `misc.objective` = 502825.92, `relgap` 0.0, `termination`/`strategy` "OPTIMAL", and `method_options.mip_gap` 0.0 (in G.pickle). These describe the last CP-SAT sub-problem, with most links pinned. They are not a bound for the instance. If someone stored the object in the database, it would read as a certified-optimal route set with a branched bound of 502825.92. That is about 1% above the release's real best branched bound (497716.26), and it would corrupt any gap statistic computed from bounds.
- `creator` "MILP.ortools.cp_sat" and `runtime` 22.07 s suggest one exact solve. The real process was a multi-iteration LNS.
- `warmstart` "MILP.ortools.cp_sat" contradicts the stated start from the CPLEX set 44834.
- `handle` is "Hornsea_One_1_OSS", while the release uses "hornsea_1" for this nodeset.
- G.pickle's `method_options.fun_fingerprint.funfile` contains a local path.
- The packed JSON carries no nodeset name or digest. Instance identity comes from segments.json and G.pickle, which both check out.

Before anyone stores or cites the object as a database record, the bound, relgap, termination and runtime fields should be stripped or corrected. None of these fields enter the success criterion, which compares recomputed length, feeders, validation and containment.

## Verdict
Every clause of the full success criterion holds literally for X = branched, and the claim is not subsumed: it beats every stored set, radial included. The pass depends on the shipped status snapshot being current. I did not re-check that live.

confirmed_scope: For the r26.10-v4 instance (Hornsea One.1_OSS, capacity 5), the branched route set in object/ has a recomputed Euclidean length of 506483.6421 m, 1168.4771 m (0.230%) shorter than all four stored route sets (best: id 44834, radial, 507652.1192 m), uses 35 feeders (equal to that set's 35), carries the identical nodeset, passes validate_routeset with no violations, and stays inside the border (no obstacles exist), with release latest-ness established only by the shipped Zenodo snapshot and the object's bound/relgap/OPTIMAL metadata not valid as instance bounds.

pass: true
