# Criterion skeptic: claim-yi11 (Yi-2019.1_OSS, capacity 11, topology X = radial)

Inputs read: CLAIM.md, criterion.txt, REPRODUCE.md, object/segments.json, object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz, status/zenodo-latest.json (all relative to the claim folder), plus bank entry `optiwindnet-routesets-cable-routing-records` in repo/bank/targets.json. criterion.txt's success criterion and partial wins match the bank entry word for word.
My own checkers (written before looking at any author code; the claim ships none): ../panel-yi11/work-criterion/scripts/check.py, val.py, obs.py. All run with OMP_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1, `python -I`, on my own decompressed copy of the database. I modified nothing in the claim folder.

## Release identity
- sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches the pin). md5 85faffb2e13600b017f1b583b259edd7 matches the md5 in status/zenodo-latest.json.
- status/zenodo-latest.json: record 23537067, published 2026-10-21, relations.version `is_last: True`, one file. This is a snapshot saved in the claim folder. I made no live query because outward actions were not allowed.
- Release topology values (whole DB): `branched` 14452, `radial` 34752. No other value appears, so nothing in the release is more restrictive than radial.

## Clause-by-clause
1. **Nodeset name does not start with '!':** `Yi-2019.1_OSS` passes. The criterion's only eligibility filter is the '!' prefix, and the bank statement explicitly counts "literature sites and their '.1_OSS' or '.solid' variants" among the non-'!' nodesets. The literature-site `.1_OSS` variant is therefore eligible.
2. **Topology X = radial:** the claim's G.graph topology is `radial`, and so is the topology rebuilt from routeset-packed.json. My independent check on segments.json, after collapsing the 13 detour/clone nodes, finds:
   - a tree over 120 nodes and 119 edges;
   - all 119 turbines present, with maximum turbine degree 2;
   - 11 strings of sizes [9, 11×10] (max 11, sum 119);
   - every string is a path attached to the root at one end.
3. **Comparator set ("every stored route set ... of topology X or more restrictive"):** the instance has 3 stored rows at capacity 11:
   - id 21564, radial, baselines.hgs, 135339.3765 m, feeders [11], no MILP bound;
   - id 21911, branched, MILP.pyomo.cplex, 130862.0948 m, feeders [12];
   - id 22551, branched, MILP.pyomo.gurobi, 127958.8646 m, feeders [12], bound 126046.4794.

   The parenthetical "(radial counts for branched)" brings radial sets in when X = branched. It never brings branched sets in when X = radial. Branched is less restrictive than radial, and no stored set is more restrictive than radial. So the comparator set for X = radial is exactly {21564}.
4. **Strict improvement > 1e-6 relative:** 129717.3657 vs 135339.3765. The difference is −5622.0108 m (−4.154010%), far beyond 1e-6. For context, the claim is +1758.5011 m (+1.374271%) longer than branched 22551 and −1144.7291 m (−0.874760%) shorter than branched 21911. Neither branched set is a comparator for X = radial.
5. **Feeders:** the shortest (and only) comparator, 21564, has feeders_per_root [11]. The claim uses 11 (packed [11], G degree of root −1 = 11, and 11 in my segment count). 11 ≤ 11 holds, and 11 = ceil(119/11) is also the minimum possible.
6. **Same nodeset:** G.pickle's VertexC is bit-identical to the DB VertexC blob (273×2, float64). The border (10 vertices) and all 17 obstacle polygons are identical to the DB constraint_groups and constraint_vertices. All 132 segment endpoints in segments.json equal the DB coordinates of their nodes, with clones mapped through clone2prime: 0 mismatches.
7. **validate_routeset:** optiwindnet 0.3.2 returns `[]` both on object/G.pickle and on a G I rebuilt with `G_from_routeset` from routeset-packed.json plus the DB nodeset row (same edge set as the pickle). The validator is not vacuous: forcing capacity = 10 on a copy gives 1 violation (`κ = 10, max_load = 11`).
8. **Border and obstacles:** all 132 segments are covered by the border polygon (0 outside). 0 segments touch the border line: the minimum distance from any segment to the border ring is 173.21 m, so the question of segments lying on the border line does not arise.

   Obstacles: 0 segments enter any obstacle interior, tested against the obstacle shrunk by 1e-6 m. 16 segments touch an obstacle boundary: 13 at a single point (detours via obstacle vertices) and 3 running along an obstacle edge.

   My reading: the obstacle boundary does not count as inside the obstacle, so boundary contact is "outside". This is the same contour-hugging convention the stored PathFinder sets use.
9. **Length recomputed:** the sum of Euclidean lengths over the 132 segments in segments.json is 129717.36569882005 m. The packed length is 129717.36569882008 and the G edge-length sum is 129717.36569882008. The value compared is the recomputed one.

Note on overlaps: my own crossing scan finds 2 collinear overlaps, both segmented feeders sharing a corridor from the root through a turbine location:
- (−1,72)/(−1,283): 866.6 m;
- (−1,93)/(−1,279): 4173.7 m.

These are not crossings under the validator. The stored sets use the same convention: 21564 has 5 such overlaps, 21911 has 2 and 22551 has 4, all with validator `[]`. So they are not a defect.

## Literal decision
- **Full criterion:** met literally for X = radial. The criterion explicitly offers "topology X (radial or branched)" and limits the comparison to stored sets of X or more restrictive topology. A radial set that beats every stored radial set but not the branched best is exactly the case the text defines as a full win for X = radial. A shorter branched set does not subsume the result, because the criterion does not compare a radial result with less-restrictive sets.
- **Hidden quantifiers checked:**
  - "every stored route set": there is exactly one radial row, and nothing is more restrictive.
  - "at each substation": R = 1.
  - "the shortest such stored route set": 21564.
  - "same nodeset": exact match.
- **Caveat (not disqualifying):** the only radial comparator is a 120 s HGS heuristic run with no MILP bound. The result is not shorter than the instance's overall best stored route set. It must not be described as beating the instance's stored best, nor as closing the branched gap.
- **p2:** also applies. The radial best 21564 has no MILP bound, and the instance is a non-'!' literature-site variant; whether this counts as a "real site" is arguable, but it is moot. p2 is subsumed by the full win for X = radial (p2 is "by the full-win rule" plus extra conditions), so the full criterion governs and p2 adds nothing. p1 does not apply (no '!' prefix).
- **Null test:** I agree a statistical null test is not needed. The criterion is a deterministic comparison of one object against stored values and a validator. As a non-vacuity check, I confirmed the validator and my containment checks can fail: capacity = 10 is flagged, and obstacle contacts are classified rather than ignored.

confirmed_scope: For release r26.10-v4 instance Yi-2019.1_OSS at capacity 11, the claimed radial route set (object/) has recomputed length 129717.3657 m, 5622.0108 m (4.154%) shorter than the only stored radial route set (id 21564, baselines.hgs, 135339.3765 m), with 11 feeders (≤ 11); it uses the identical nodeset, passes validate_routeset with no violations, and stays inside the border and outside every obstacle interior. It is not shorter than the stored branched best (id 22551, 127958.8646 m), so it is a full-criterion win for topology X = radial only.

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)
pass: true
