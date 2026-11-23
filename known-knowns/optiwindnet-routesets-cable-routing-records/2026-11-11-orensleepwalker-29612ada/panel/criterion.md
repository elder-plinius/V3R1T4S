# Criterion skeptic report: claim-ho3

context: OptiWindNet RouteSets r26.10-v4, nodeset "Hornsea One.1_OSS" (174 turbines, 1 substation, 25-vertex border, 0 obstacles), capacity 3, claimed topology X = radial (also counted for branched); full success criterion of bank target `optiwindnet-routesets-cable-routing-records`; checked 2026-11-10 with my own scripts in `panel-ho3/work-criterion/` (own_check.py: sqlite3 + numpy + shapely only; official.py and cross.py: optiwindnet 0.3.2).

confirmed_scope: For the r26.10-v4 instance (nodeset "Hornsea One.1_OSS", capacity 3), the route set in object/ is a radial network on the release's exact nodeset with 58 feeders at the single substation and a Euclidean length of 735605.4808 m, which is 343.2720 m (4.66e-4 relative) shorter than the shortest of the four stored route sets for that instance (id 40884, radial, 735948.7528 m, feeders [58]), passes validate_routeset with no violations and lies entirely inside the site border; no optimality is established, and release latest-ness is shown only by the frozen snapshot status/zenodo-latest.json.

## Clause-by-clause (all recomputed independently)

| Clause | Result | Evidence |
|---|---|---|
| Instance of r26.10-v4, name not starting with '!' | holds | nodeset row "Hornsea One.1_OSS" exists; T=174, R=1, B=25; VertexC 200x2 |
| Route set of topology X = radial | holds | from object/segments.json: 243 nodes, 242 edges, connected tree; turbine degrees {2: 116, 1: 58}; all 68 clone nodes degree 2; each of the 58 root subtrees is a simple path with exactly 3 turbines (feeder attaches at a path end) |
| Strictly shorter than EVERY stored set of topology X or more restrictive, by > 1e-6 relative | holds | stored sets for the instance (all 4, none with missing topology): 40884 radial 735948.7528; 9597 radial 738034.6339; 2784 branched 739768.9053; 8885 radial 753634.9352. For X = radial (3 sets) and X = branched (4 sets) the comparator is the same, id 40884. Margin 343.2720 m = 4.664e-4 relative, about 466 times the threshold |
| Feeders at EACH substation <= the shortest such stored set's feeders_per_root | holds | 58 edges at the one substation; cap [58] (id 40884). 58 is also the minimum possible (174/3), so no feeder relaxation is involved |
| Same nodeset (turbines, substations, borders, obstacles) | holds | every endpoint coordinate in object/segments.json equals the DB VertexC entry exactly (max deviation 0), clones mapped through clone2prime; all 174 turbines and the substation present; object/G.pickle VertexC and border array are identical to the DB row; no obstacles in the nodeset |
| validate_routeset returns no violations | holds | [] for the graph I rebuilt from object/routeset-packed.json plus the DB nodeset, labelled radial and labelled branched; [] for object/G.pickle as shipped (branched label) and relabelled radial; pickle edge set equals the rebuilt edge set. Negative controls: capacity set to 2 gives 1 violation, a long chord gives 32 violations, so the validator is not vacuous. The 4 stored sets also return [] |
| Every segment inside border, outside obstacles | holds | shapely: border polygon valid (407.35 km2); all 242 segments covered by it with the exact predicate, length outside 0; 0 obstacles. 4 detour nodes sit on border vertices, 64 on turbine positions; no turbine or substation lies within 1 m of a segment not incident to it |
| Length is the Euclidean sum, and that value is compared | holds | sum over 242 segments = 735605.480807 m from the file's coordinates and from DB coordinates; equals the packed `length` and the validator graph's length. Stored lengths recomputed from the stored graphs equal the DB `length` column, so the comparison is like for like (detours included on both sides) |
| Release identity | holds | references/optiwindnet-routesets-r26.10-v4.sqlite.xz sha256 c78c8f3c...e3a (bank value); md5 85faffb2... equals the Zenodo file checksum in status/zenodo-latest.json; uncompressed md5 5ad6bf04... equals the value in the record description; 49,204 route sets, 12,814 nodesets |
| Latest-ness | holds as of the snapshot only | status/zenodo-latest.json: record 23537067, published 2026-10-21, relations.version is_last = true, single file as above. The JSON carries no retrieval timestamp (file mtime 2026-11-10 is copy time); I did not query the network |

## Null models and hidden quantifiers

- Crossings: my own census finds 0 transversal crossings and 134 collinear overlapping segment pairs (369.6 km). These are feeders drawn on coincident coordinates where they bend at the same turbine. The stored sets show the same convention under the same census (40884: 83 pairs; 9597: 88; 2784: 87; 8885: 317; all 0 transversal), so this is the benchmark's representation and not a defect peculiar to the claim; the official validator, which resolves the ordering of such bundles, reports nothing.
- Bound sanity: the claim's straight-line objective (734346.41) and length are above the release's radial bound (732175.40) and branched bound (733051.42) for the instance; nothing impossible is claimed.
- "Every stored set of any topology": true, 4 of 4. No other nodeset row shares the name; the only relative without '!' is "Hornsea One" (3 substations), a different instance.
- Size of the win: 0.047%, small but real; the stored best carried a 0.34% gap, so there was room.
- Partial wins are not needed; p2 would not apply anyway (the stored radial best has a MILP bound).

## Wording and metadata defects (none change the verdict)

1. criterion.txt says "Claimed: ... topology X = branched" while CLAIM.md says X = radial. Both hold with the same comparator and feeder cap, but the files should agree.
2. object/routeset-packed.json and object/G.pickle label the object `misc.topology: "branched"` although it is radial. Validation passes under either label; the label should be "radial" if X = radial is the claim.
3. The packed `misc` has `termination: "OPTIMAL"`, `relgap: 0.0`, `bound == objective == 734346.41`, `strategy: "OPTIMAL"`, `runtime: 1.30`, `creator: "MILP.ortools.cp_sat"`. These describe the last 30-second windowed sub-solve of a fix-and-optimise search, not the whole problem. Read as a database record they say the route set is proven optimal, which is false and which CLAIM.md itself disclaims. They must be removed or relabelled before the object is shared upstream.
4. Packed `handle` is "Hornsea_One_1_OSS"; the release uses "hornsea_1" for this nodeset's route sets.
5. CLAIM.md's numbers (735605.4808, 735948.7528, 343.2720 m, 0.047%, ids 40884 and 2784, feeders [58] and [59]) all reproduce.

## Verdict

Every clause of the full success criterion holds literally for X = radial, and therefore also for X = branched. The win is genuine and not subsumed by any stored set. Defect 3 is a misleading-metadata issue in the packed object that should be fixed, but the claim text does not assert optimality.

pass: true
