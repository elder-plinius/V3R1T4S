# REPRODUCE panel report: Yi-2019.1_OSS, capacity 12, topology radial

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Scope: read only CLAIM.md, REPRODUCE.md, criterion.txt, object/*, references/*, status/zenodo-latest.json. No author code exists in the claim folder and none was read. Work files are in panel/work-reproduce/ (mycheck.py, validate.py, shp.py, dbdump.py, *.out). Python run with -I and PYTHONDONTWRITEBYTECODE=1, OMP_NUM_THREADS=1. The claim folder was unchanged (read-only, no __pycache__).

## Reference database
- I copied references/optiwindnet-routesets-r26.10-v4.sqlite.xz to work-reproduce/db/ and ran `xz -dk`. The .xz sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches the criterion's value. The uncompressed MD5 is 5ad6bf0449dcbd9939f1ae03bee19016, which matches the release's MD5 in status/zenodo-latest.json.
- nodeset 'Yi-2019.1_OSS' has exactly one row: T=119, R=1, B=153, VertexC (273,2) float64. constraint_groups = [10, 4,17,6,5,14,5,4,20,6,5,7,7,10,17,4,6,6]: a 10-vertex border followed by 17 obstacles. The name has no '!' prefix.
- The nodeset has 41 routeset rows in total. Two have capacity 12:
  - id 21567, baselines.hgs, radial, length 126034.67154227255, feeders_per_root [10]
  - id 21894, MILP.pyomo.cplex, branched, length 121874.57973449383, feeders_per_root [11] (relgap 0.005, bound 120868.25)

## Independent checker (work-reproduce/mycheck.py, written before looking at anything but the claim files)
Implemented definition (criterion.txt, verbatim): "a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). ... every route segment must stay inside the site border and outside every obstacle polygon ..., and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared."

All geometry predicates use exact rational arithmetic (Fraction of the stored float64 values). Results on object/segments.json:
- **Endpoints.** All 266 endpoint coordinates equal the VertexC entries exactly: turbines i -> VertexC[i], root -1 -> VertexC[272], and clones 272..285 -> VertexC[clone2prime[k-272]] from object/routeset-packed.json.
- **Length.** The fsum of the Euclidean lengths of the 133 segments is 125848.932131 m. This equals the claimed value and the packed length.
- **Structure.**
  - The raw graph has 134 nodes and 133 edges, is connected, and is therefore a tree.
  - All 14 clones have degree 2.
  - After contracting the clone chains, the turbine-level network has 119 links, and every turbine has degree 1 or 2 (root links included).
  - Walking each feeder from the root reaches every turbine exactly once. There are no branches, rings or isolated turbines.
  - 10 strings with sizes [11, 12×9]; the maximum is 12, which is within capacity 12.
- **Feeders.** 10 at the substation, both at turbine level and as raw segments at the root.
- **Crossings.** There are 0 proper crossings and 0 T-touches (an endpoint lying in the interior of another segment). No segment passes over a turbine or substation point in its interior.
- **Border and obstacles.** Each segment was split at every intersection with the polygon edges, and each piece midpoint and endpoint was classified exactly. 0 segments leave the border. 0 segments enter the interior of any of the 17 obstacles. 14 segments touch an obstacle boundary (obstacles 3, 4, 6, 7, 13 and 15), which is expected for contour clones at obstacle vertices. A separate shapely check (border.covers(segment), and the DE-9IM interior/interior relation 'F' for each obstacle) also found 0 violations. All polygons are valid.
- **Comparison with the stored sets.**
  - Against radial 21567 (the only stored radial or more restrictive set): 126034.671542 − 125848.932131 = 185.739411 m, relative 1.4737e-3, which is above 1e-6. Strict improvement confirmed.
  - Feeder cap = feeders_per_root of 21567 = [10]. The object uses [10], so it is within the cap.
- **Branched.** The object is 3974.352396 m longer than branched 21894 (MILP.pyomo.cplex, 121874.579734). The claim correctly limits itself to topology radial.

The checker's output is byte-identical across two runs (deterministic).

Discriminating power: I applied the same checker to the stored sets, rebuilt with G_from_routeset.
- For 21567 it reproduces the stored length 126034.671542, 10 strings with sizes [11, 12×9], and no crossings or containment violations.
- For branched 21894 it correctly reports degree-3 turbines (branches). This shows the radial test actually rejects non-radial networks.

## Official validator (optiwindnet 0.3.2)
- validate_routeset(object/G.pickle) returns [].
- validate_routeset on a graph rebuilt from object/routeset-packed.json returns []. The rebuild used L_from_nodeset(the db NodeSet), then TerseLinks(edges, topology=radial, T/R/B/C/D, clone2prime, the db nodeset digest), then to_routeset(capacity=12).
- For comparison, validate_routeset on the stored 21567 and on 21894 also returns [].
- validate.py output is byte-identical across two runs.

## Do the three objects describe the same network?
- G.pickle VertexC is array-equal to the db VertexC. fingerprint_coordinates(VertexC) equals the db nodeset digest. Its border and obstacles equal those from L_from_nodeset.
- G.pickle, the packed rebuild and segments.json have the identical edge set: 133 edges with identical endpoint ids and coordinates. fnT is equal between the pickle and the rebuild.
- All three give length 125848.93213086294 and feeders [10].

## Doubtful or noteworthy points (none of them is a failure)
1. **Shared feeder corridors.**
   - The object has 10 pairs of collinear overlapping segments. For example, root->72 overlaps root->clones 280, 283 and 285; root->51 overlaps root->clones 278 and 282; and segment 92-285 overlaps segment 279-280. In each case several feeders run along the same straight corridor to a detour node placed on a turbine.
   - These are not proper crossings, and the official validator accepts them.
   - The stored radial 21567 has the same pattern: 10 overlapping pairs at the same turbines 51, 72 and 92. The stored branched 21894 has 5 such pairs.
   - So this is the dataset's own convention, not something particular to this object. It still means "no crossings" here holds only in the sense of no proper crossings.
2. **Handle.** The packed record's handle is 'Yi_2019_1_OSS', while the stored records use 'yi_2019_1'. This is cosmetic: the instance is identified by the nodeset (name and digest), which matches.
3. **Release currency.** status/zenodo-latest.json is a frozen snapshot showing version index 1 with is_last=true (record 23537067, 2026-10-21). I had no network access and could not confirm that no newer Zenodo version exists today.
4. **Pickle.** object/G.pickle is a pickle file, which can execute code when loaded. I loaded it only inside the optiwindnet venv. The packed-JSON rebuild independently gives the same network and also validates.
5. **Exhaustiveness.** All stored capacity-12 routesets for this nodeset (2 rows) were read and compared. No sampling was involved.

pass: true
