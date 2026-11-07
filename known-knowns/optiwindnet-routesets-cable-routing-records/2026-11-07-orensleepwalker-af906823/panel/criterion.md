# Criterion skeptic report: optiwindnet-routesets-cable-routing-records, Yi-2019.1_OSS, capacity 12, topology radial

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the bank entry)

## Inputs and method
- I read CLAIM.md, REPRODUCE.md, criterion.txt, object/*, status/zenodo-latest.json, and the bank entry `optiwindnet-routesets-cable-routing-records` in bank/targets.json.
- I wrote my own scripts before looking at any author code. The claim ships no author code. The scripts are in panel/work-criterion/: cmp_bank.py, q.py, check_geom.py and official.py. I decompressed the SQLite into the work folder and deleted it afterwards.
- I ran everything with the optiwindnet 0.3.2 venv, `python -I`, PYTHONDONTWRITEBYTECODE=1. Nothing was written to the claim folder, and it contains no `__pycache__`.

## Criterion text
- criterion.txt quotes the bank entry verbatim: success_criterion, statement, verification_method, the 3 pitfalls, status_source and the p1/p2 statements all match as exact substrings.

## Release identity and latest status
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz has sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a. This equals the bank value. Its md5 is 85faffb2e13600b017f1b583b259edd7, which equals the checksum in the Zenodo file entry.
- status/zenodo-latest.json is the record that the `/versions/latest` endpoint returns. It is record 23537067 (conceptrecid 20053478, revision 4, status published, created and updated 2026-10-21), and its only file is this .xz. So r26.10-v4 was the latest version when the file was fetched.
- The file has no fetch timestamp. "Latest" is therefore shown only as of an unknown fetch time, which is at the latest the claim freeze on 2026-11-07.

## Clause-by-clause check
1. **Non-'!' nodeset:** the name is `Yi-2019.1_OSS`. It is a literature site with an OSS variant. It has T=119, R=1, B=153, and constraint_groups [10, 4, 17, ...], which is 1 border plus 17 obstacles. Met.
2. **Topology X = radial; the object really is radial.**
   - In my own graph built from segments.json there are 133 edges and 134 nodes: 119 turbines, 1 root and 14 clones.
   - The graph is connected and is a tree. Every clone has degree 2. Turbine degrees are {2: 109, 1: 10}.
   - Each of the 10 root-incident strings is a simple path with no branching. String loads are [11, 12×9], which sum to 119; the maximum is 12, equal to the capacity.
   - optiwindnet rebuilds G from routeset-packed.json with topology `radial`. Met.
3. **The comparison set "topology X or more restrictive".**
   - The release has only two topology values (radial: 34,752 rows; branched: 14,452). For X = radial, "more restrictive" therefore adds nothing, and the comparison set is every radial row for this (nodeset, capacity).
   - In the SQLite this instance has exactly 2 rows at capacity 12: id 21567 (radial, baselines.hgs, HGS-CVRP with timeLimit 120 s, length 126034.67154227255, feeders [10], no bound in misc) and id 21894 (branched, MILP.pyomo.cplex, length 121874.57973449383, feeders [11], bound 120868.25).
   - So the comparison set is {21567}.
4. **Strictly shorter by more than 1e-6 relative:** 126034.671542 − 125848.932131 = 185.739411 m, which is 1.4737e-3 relative. Met. The object is not shorter than the branched 21894. The criterion does not require that for X = radial.
5. **Feeders:** 10 at the root, which is ≤ the feeders_per_root [10] of 21567. Met.
6. **Same nodeset:**
   - All 266 segment endpoints equal VertexC rows from the release nodeset blob. Clones resolve through clone2prime.
   - G.pickle has VertexC, border and 17 obstacle arrays identical to L_from_nodeset of the release row, and its edge set is identical to the G rebuilt from the packed JSON. Met.
7. **validate_routeset:** returns [] both for G.pickle and for G rebuilt from object/routeset-packed.json through optiwindnet's G_from_routeset against the release nodeset. As a null check, it also returns [] for stored rows 21567 and 21894. Met.
8. **Border and obstacles** (shapely, my own check): every segment is covered by the border polygon. No segment interior meets the interior of any of the 17 obstacles; 14 segments only touch obstacle boundaries at detour vertices. All 18 polygons are valid. Met.
9. **Length:** the sum of Euclidean segment lengths is 125848.932131 m. This equals segments.json `length_sum_euclid_m`, packed `length`, and G.size(weight='length'). That is the value compared. Met.

## Crossing and overlap check (independent)
- My checker finds 0 point crossings. It does find 10 collinear overlaps, where several feeders share the corridors root→T72, root→T51 and T72→(16175, 8330), passing through turbine positions by way of turbine-primed clones. These are "segmented feeders".
- I treat these as the release's own convention, not a defect, for three reasons:
  - The stored radial best 21567 has the same 10 overlaps on the same corridors.
  - 38,941 of the 40,075 stored route sets that have clones use turbine-primed clones.
  - The official validator accepts them.

## Null models and quantifiers
- The baseline beaten is a single 120-s HGS run. The claim used the same heuristic family for 240 s, with seed reruns. The win is legitimate under the criterion, but it is a heuristic-vs-heuristic improvement of 0.147%, not evidence about optimality. No radial MILP bound exists for this instance.
- No hidden quantifier fails:
  - "every stored route set" ranges over one radial row.
  - The feeder cap is respected.
  - The nodeset is identical, including the obstacles.
- The branched record (121874.58 m) is 3.16% shorter and stays the best route set for the instance overall. That is outside the radial scope and does not make the radial result void.

## Full criterion or p2
- Literally, the full success criterion explicitly allows X = radial, and every clause is met. So this is a full win for X = radial.
- p2 states the same rule with one extra condition: the radial best has no MILP bound. 21567 has no bound, so the result also has the p2 shape. Whether a literature layout counts as a "real-site" is ambiguous.
- p2 is literally a subset of the full criterion, so it does not compete with the full-win reading. Still, p2 is the more informative description. Any summary should say "radial-topology record; the instance's overall best (branched) is unchanged" and should not imply the instance's best length was beaten.

## CLAIM.md scope wording
- The radial-only scope is stated clearly enough. The first sentence says "radial route set ... shorter than every stored radial route set". It says explicitly that the object is NOT shorter than the stored branched best 121874.5797 m, "so the claim is for topology X = radial only". criterion.txt's header repeats "topology radial".
- All numbers in CLAIM.md match my recomputation: 125848.9321, 126034.6715, 185.7394 m (0.147%), id 21567, id 21894, [10] feeders and 17 obstacles.
- Suggestion: name p2 in CLAIM.md as the matching enumerated case.

confirmed_scope: For release r26.10-v4 instance Yi-2019.1_OSS with capacity 12 and topology radial, the claimed route set (10 substation feeders, 0 validate_routeset violations, inside the border and outside all 17 obstacles) has a Euclidean segment-sum length of 125848.932131 m, which is 185.739 m (1.47e-3 relative) shorter than the only stored radial route set (id 21567, 126034.671542 m, 10 feeders), while the stored branched route set (id 21894, 121874.579734 m) remains shorter.

pass: true
