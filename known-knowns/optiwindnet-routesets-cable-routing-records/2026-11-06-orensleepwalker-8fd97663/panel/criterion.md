# Criterion skeptic: claim-cazzaro7

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

Inputs read: CLAIM.md, criterion.txt, REPRODUCE.md, status/zenodo-latest.json, object/segments.json, object/routeset-packed.json, object/G.pickle, references/optiwindnet-routesets-r26.10-v4.sqlite.xz; bank entry `optiwindnet-routesets-cable-routing-records` in repo/bank/targets.json. My scripts and outputs are in ../panel-cazzaro7/work-criterion/ (scripts/q.py, scripts/check.py, scripts/detail.py, scripts/stored.py; check.out, detail.out, stored.out, packed.out). I decompressed my own copy of the database there. Environment: OMP_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1, optiwindnet 0.3.2 venv python, shapely 2.2.0, networkx 3.7. Nothing was installed and the claim folder was not modified.

## Release identity
- sha256 of references/optiwindnet-routesets-r26.10-v4.sqlite.xz = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches the pin). md5 85faffb2e13600b017f1b583b259edd7 matches the md5 listed in status/zenodo-latest.json (record 23537067, published 2026-10-21). I did not re-query Zenodo because outward actions were not allowed, so "still the latest version" depends on the claim's snapshot.

## Clause-by-clause check
1. **Nodeset name doesn't start with '!'.** Met: the name is `Cazzaro-2022G-210.solid.1_OSS` (T=210, R=1, B=19). The criterion's only eligibility rule is the '!' prefix, so a literature-site variant qualifies under the literal wording. The bank's title says "for a real site", but the criterion itself does not require that. The statement also lists "literature sites and their '.1_OSS' or '.solid' variants" among the non-'!' instances.
2. **Stored sets for (nodeset, capacity 7).** There are exactly two (the nodeset has 20 route sets across all capacities):
   - id 25104: radial, length 364573.2688, feeders_per_root [30], baselines.hgs, no `bound`.
   - id 25281: branched, length 363836.6318, feeders_per_root [30], MILP.pyomo.cplex, bound 349122.5083, relgap 0.0282, terminated at maxTimeLimit.
3. **Strictly smaller by more than 1e-6 relative.**
   - Recomputed length (fsum of Euclidean lengths over the 228 segments in object/segments.json) = 360354.074553. This matches the sum of G's edge `length` values and the packed `length`.
   - X = radial: compared with the single stored radial set (25104), the difference is 4219.1943, or 1.157297e-02 relative. Met.
   - X = branched (radial and branched stored sets both count): compared with the best, 25281, the difference is 3482.5572, or 9.571761e-03 relative. It is also shorter than 25104. Met numerically.
   - Same-metric check: rebuilding both stored sets with optiwindnet's G_from_routeset and applying the same Euclidean recomputation reproduces their stored lengths exactly (364573.2688 and 363836.6318). Both also validate with [].
4. **Feeders.** The claim has 30 feeders at the single root. The shortest stored set is 25104 for X=radial and 25281 for X=branched, and both have feeders_per_root [30]. 30 <= 30, so this is met for both.
5. **Same nodeset.** G.graph VertexC has shape (230, 2) and is bitwise equal to the database VertexC blob. The G border equals the database constraint_vertices (19 vertices). constraint_groups = [19], which means one group: the border, with 0 obstacles. optiwindnet's L_from_nodeset agrees (obstacles None). Every segment endpoint in segments.json equals VertexC[fnT[node]] in G (0 mismatches). The set of segments equals G's edge set (228 = 228). pack_G(G) matches object/routeset-packed.json on edges, length, feeders_per_root, clone2prime, C, D, capacity, T and R.
6. **validate_routeset(G).** Returns [] (no violations). G.graph topology is RADIAL and capacity is 7.
7. **My own topology check.**
   - After contracting the 18 degree-2 clone nodes, the prime graph is a tree on 211 nodes with 210 edges and contains all turbines.
   - There are 30 strings. Each is a path of at most 7 turbines, and each attaches to the root at one end. The maximum turbine degree is 2.
   - Pairwise segment intersections other than at shared endpoints: 11 pairs. All 11 are exactly coincident segments (`equals` = True), where detour clones share a corridor (root to turbine 102/77/69/118/73 or border vertex 222, and turbine 118 to border vertex 217). None is a proper crossing.
   - The stored sets use the same detour-clone representation (D=21 and D=20).
8. **Border and obstacle containment, checked separately.**
   - My reading of "inside": covered by the closed border polygon, so the border line counts as inside.
   - Result: 228/228 segments are covered by the closed polygon, which is valid with area 263107447.9 m^2. 0 segments lie outside. There are no obstacles, so 0 segments hit an obstacle.
   - 12 segments touch the border line. Each touches at exactly one point, and that point is the segment's own endpoint at a border-vertex clone (concave corners 213, 217, 222). 0 segments run along the border with positive length. 216 segments lie strictly in the open interior. The smallest distance from a non-touching segment to the border is 0.349 m.
   - Under a strict open-interior reading those 12 segments would fail. However, both stored sets have the same pattern (12 border-touching segments each, all covered), so the closed reading is the release's own convention.

## Topology X, partial wins, null model
- **X = radial:** fully met. The object is radial and beats the only stored radial set.
- **X = branched:** the numbers are also met: it is shorter than both stored sets and uses no more feeders. This holds only if a radial set counts as a route set "of topology branched". The criterion's "radial counts for branched" supports that reading, but the wording applies it explicitly only to stored sets. I therefore anchor the win on radial and record the branched comparison as a fact, not as a separate claim.
- **p2** (radial beats the stored radial best, and that best has no MILP bound): its conditions hold, since 25104 has no `bound`. It is subsumed by the full win because it is the same object under a stricter instance filter. p1 does not apply (no '!' prefix).
- **Null model:** I agree a null test is not needed. This is one deterministic object checked against fixed stored values. The margin is 1.16% against a 1e-6 threshold, and the validity checks are exact.
- **Hidden quantifiers I checked:**
  - "every stored route set": all capacity-7 sets for this nodeset (2) were checked.
  - "at each substation": R=1.
  - "all turbines, substations, borders and obstacles": the comparison is bitwise.
  - "length recomputed ... must be the value compared": recomputed from segments.json, including detours.
- **Residual caveats:**
  - Whether Zenodo has a newer version was not re-checked live.
  - "Real site" in the bank title is not a term in the criterion.

confirmed_scope: For release r26.10-v4 instance Cazzaro-2022G-210.solid.1_OSS at capacity 7, the radial route set in object/ has recomputed Euclidean length 360354.0746 m, 4219.1943 m (1.157%) shorter than the only stored radial set (id 25104, 364573.2688 m) and also shorter than the stored branched set (id 25281, 363836.6318 m), using 30 feeders (equal to both stored sets), on the bitwise-identical nodeset, with validate_routeset returning no violations and all 228 segments inside the closed border polygon (12 touch it only at border-vertex detour endpoints; the nodeset has no obstacles).

pass: true
