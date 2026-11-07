# Criterion review: claim-ho7 (OptiWindNet RouteSets, Hornsea One.1_OSS, capacity 7, X = branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

## Method
I wrote my own checkers before looking at any author code. The claim ships no code. Scripts are in panel-ho7/work-criterion/scripts/:
- check_geom.py: uses only the DB nodeset and object/segments.json, plus numpy and shapely.
- check_own.py: rebuilds G from object/routeset-packed.json and the DB nodeset using optiwindnet 0.3.2 `G_from_routeset`, runs `validate_routeset`, compares with object/G.pickle and rebuilds all stored sets.
- overlap_stored.py: a null-model check of the overlap convention in the stored sets.

The DB was decompressed from references/optiwindnet-routesets-r26.10-v4.sqlite.xz into the work folder and read with Python's stdlib sqlite3. It was deleted afterwards.

## Clause-by-clause
1. **Criterion text.** criterion.txt quotes the bank entry `optiwindnet-routesets-cable-routing-records` verbatim: the success criterion, both partial wins, the statement, the verification method and the pitfalls all match.
2. **Release identity.**
   - sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches the bank.
   - Its md5 is 85faffb2e13600b017f1b583b259edd7, which matches the file checksum in status/zenodo-latest.json.
   - In status/zenodo-latest.json, record 23537067 is published 2026-10-21, `relations.version[0].is_last = true` and `links.latest` points to itself. So r26.10-v4 is the latest version as of that snapshot.
   - The snapshot carries no fetch timestamp, and I made no outward request. "Latest" is therefore confirmed only as of the snapshot.
3. **Nodeset name has no '!' prefix.** The nodeset is "Hornsea One.1_OSS": T=174, R=1, B=25, constraint_groups [25] (border only, 0 obstacles). It is the only nodeset with that exact name. The "!Hornsea One.1_OSS!..." rows are separate augmented nodesets and correctly do not count.
4. **Stored route sets for (nodeset, capacity 7).** All 4 rows are radial or branched, so all are "branched or more restrictive". There are no ringed sets.

   | id | creator | topology | length (m) | feeders_per_root | feeder_limit |
   |---|---|---|---|---|---|
   | 45791 | MILP.pyomo.cplex | radial | 408102.5795 | [26] | min_plus1 |
   | 2801 | MILP.pyomo.cplex | branched | 411304.2676 | [25] | unlimited |
   | 9637 | baselines.hgs | radial | 414178.6097 | [25] | |
   | 8924 | baselines.lkh | radial | 419780.0637 | [25] | |

   For each stored set, the stored length equals the recomputed geometric length, and validate_routeset returns [].
5. **Topology X = branched.** The collapsed logical graph has degree histogram {1: 30, 2: 140, 3: 4}. That is 4 branching turbines, and optiwindnet infers the topology as branched. It is therefore a branched route set, not radial.
6. **Strictly shorter by more than 1e-6 relative than every stored set.**
   - The claim's length is 407209.015554 m.
   - The shortest stored set is 45791 at 408102.579535 m. The difference is 893.564 m, which is 2.19e-3 relative and above 1e-6.
   - The claim is therefore also shorter than the other three stored sets.
7. **Feeders at each substation ≤ the shortest such stored set's feeders_per_root.**
   - The shortest qualifying stored set is 45791, with [26]. The claim uses [26] (26 feeders at the single root), so the clause passes literally.
   - Caveat on reading: every other stored set uses 25, which is the minimum, ceil(174/7). The branched-only best (2801) uses 25. The claim matches the cap set by the radial min_plus1 run, which is exactly what the criterion and pitfall specify ("the shortest stored route set's count"). It does not relax beyond that cap.
8. **Same nodeset.**
   - All 195 segment endpoints coincide with VertexC rows. Clones are mapped through clone2prime: 0 mismatches.
   - All 174 turbines and the substation are present.
   - G.pickle has VertexC equal to the DB blob and the same border, with no obstacles. Its edge set equals the one rebuilt from the packed JSON.
9. **Forest, capacity and loads.**
   - My own check: 174 logical edges, all 174 turbines reached exactly once from the root, no cycles, 26 subtrees, maximum subtree size 7 (equal to the capacity, allowed).
   - optiwindnet `validate_routeset` returns [] on G rebuilt from routeset-packed.json + DB nodeset, and [] on object/G.pickle.
10. **Crossings.** My pairwise shapely test finds 0 proper crossings.
    - There are 21 pairs of collinear overlapping segments: detour clones that run along an existing feeder corridor and bend at turbine positions. These come from optiwindnet's PathFinder detour convention (D=19, C=2).
    - Null model: stored sets 45791 and 2801 have 21 and 20 such pairs respectively. This is the release's convention, not an artefact of the claim. Each overlapping cable is counted separately in the length.
11. **Border and obstacles.** All 195 segments are covered by the border polygon (with a 1e-6 m buffer). The smallest distance from a segment midpoint to the border is 49.6 m. There are no obstacles, so the obstacle clause holds vacuously.
12. **Compared length is the Euclidean sum.**
    - The sum of the 195 segment lengths in segments.json is 407209.015554 m. This equals `length_sum_euclid_m`, the packed `length`, and G.size(weight='length').
    - This is the value I compared in step 6, not misc.objective (406663.29).

## Wording and metadata
- CLAIM.md "strictly shorter than every stored route set for that instance of any topology": accurate, because all 4 stored sets are radial or branched.
- "outside every obstacle": vacuous, since there are 0 obstacles.
- The provenance (LNS with CP-SAT; seeds 7, 8 and 9 reaching the identical set) is unverified. It is labelled as provenance, not evidence.
- The packed object's metadata can mislead:
  - `creator` "MILP.ortools.cp_sat", `runtime` 0.82 s, `termination` "OPTIMAL", `solver_details.strategy` "OPTIMAL", `relgap` 1.7e-11 and `bound` 406663.29 describe only the last pinned sub-solve. They are not a certificate for the instance.
  - That bound is not a lower bound on the instance. The stored MILP bounds are 390330.39 (radial) and 393633.86 (branched).
  - `warmstart` "MILP.ortools.cp_sat" hides the actual start, stored set 45791.
  - If these fields were stored into the release as they are, they would wrongly present this set as certified optimal.
  - G.pickle's method_options also carry a local absolute funfile path.
  - CLAIM.md itself does not claim optimality.

## Partial wins
None is needed or applicable. The instance is not '!'-prefixed, so p1 does not apply. The set is branched, not radial, so p2 does not apply. The full criterion is met for X = branched.

confirmed_scope: For release r26.10-v4 instance "Hornsea One.1_OSS" at capacity 7 (no '!' prefix; latest Zenodo version per the bundled status snapshot), the claimed branched route set, with 26 feeders (equal to the cap from the shortest stored set), the identical nodeset, no validate_routeset violations and every segment inside the border (no obstacles), has a Euclidean segment-sum length of 407209.0156 m, which is 893.56 m (0.219%) shorter than the shortest of the four stored radial or branched sets (id 45791, radial, 408102.5795 m), with no optimality established.

pass: true
