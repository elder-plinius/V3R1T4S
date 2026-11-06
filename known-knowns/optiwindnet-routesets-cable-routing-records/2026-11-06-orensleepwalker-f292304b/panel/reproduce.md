# REPRODUCE review: claim-ho10 (Hornsea One.1_OSS, capacity 10, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Inputs read: claim/CLAIM.md, claim/criterion.txt, claim/REPRODUCE.md, claim/object/segments.json,
claim/object/routeset-packed.json, claim/object/G.pickle, claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz,
claim/status/zenodo-latest.json. I read nothing else in the workspace and did not see any author code.
Object hashes (sha256): segments.json f292304b…4f, routeset-packed.json 586af42a…a6, G.pickle d315b4b5…fa.
The claim folder was not modified (read-only and no `__pycache__`); I ran Python with `-I` and `PYTHONDONTWRITEBYTECODE=1`, and the venv runs used `OMP_NUM_THREADS=1`.

## Definition implemented (quoted from claim/criterion.txt)
"a route set of topology X with strictly smaller total length than every stored route set for that instance of
topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation
no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all
turbines, substations, borders and obstacles from its VertexC blob). It must pass
optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route
segment must stay inside the site border and outside every obstacle polygon (checked separately, since the
validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must
be the value compared."

## Reference data
- sha256 of claim/references/…sqlite.xz = c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a. This matches the claim. Its MD5 is 85faffb2…edd7, which matches the Zenodo file checksum in claim/status/zenodo-latest.json.
- I decompressed my own copy to work-reproduce/db/rs.sqlite. Its MD5 is 5ad6bf0449dcbd9939f1ae03bee19016, which matches the release table's MD5 for the uncompressed file.
- Nodeset row 'Hornsea One.1_OSS' (no '!' prefix): T=174, R=1, B=25, and the VertexC .npy blob has shape (200, 2) float64. The constraint data are constraint_groups=[25] and constraint_vertices=174..198, so there is a border and no obstacles.
- The status file is a frozen snapshot: record 23537067 with `is_last: true`. I did not re-query Zenodo because no network was used, so I could not check whether a newer version now exists.

## Independent checker (work-reproduce/scripts/my_checker.py)
This checker uses only the standard library. It parses the .npy blob itself, and every geometric predicate uses exact rational arithmetic (`fractions.Fraction` built from the floats).
- **Endpoints:** every endpoint of the 180 segments equals VertexC[prime(node)] bit-exactly. Clones 199..204 map through clone2prime to [175, 184, 87, 94, 89, 95], i.e. 2 border-contour clones and 4 detours at turbines.
- **Length:** the sum of Euclidean segment lengths (fsum of hypot) is 332729.34431381547. This equals the length_sum_euclid_m in segments.json, the packed length and the claimed 332729.3443.
- **Topology:**
  - Every clone node has degree 2.
  - Contracting the clones gives 174 logical links on the 174 turbines plus the root. All turbines are reachable from the substation, the graph is acyclic (|E| = |V| - R), there are no root-root links and no duplicate segments.
  - There are 18 feeders. Subtree loads are [6, 9, 9, 10×15]: max 10 ≤ capacity 10, sum 174.
  - The maximum turbine degree is 3, so the network is branched.
- **Crossings (exact pairwise check of all 180 segments):** no proper crossings and no T-touches.
  - 3 pairs of segments are identical: (-1,89)/(-1,203), (-1,94)/(-1,202), (-1,95)/(-1,204). Each is a direct feeder to a turbine plus a second feeder that bends at a detour node on that same turbine. See the notes for why I accept this.
- **Containment:** every segment lies in the closed border polygon. The test is exact: no proper crossing with any border edge, and every contact point and every sub-interval midpoint is inside or on the border.
  - 4 segments end on border vertex 175 or 184 through contour clones.
  - There are no obstacles.
  - Cross-check with shapely: `Polygon(border).covers(segment)` holds for all 180 segments, and the border polygon is valid.
- **Stored sets (capacity 10, read with sqlite3; all 4 rows):**

  | id | creator | topology | length (m) | feeders_per_root | relative margin |
  |---|---|---|---|---|---|
  | 45802 | MILP.pyomo.cplex | radial | 336086.4654425699 | [18] | 0.998886% |
  | 9644 | baselines.hgs | radial | 340159.19493730477 | [18] | 2.184% |
  | 2804 | MILP.pyomo.cplex | branched | 342349.2848876512 | [19] | 2.810% |
  | 8928 | baselines.lkh | radial | 350931.2829630522 | [18] | 5.187% |

  - All four margins are far above 1e-6.
  - The difference to the best stored set is 3357.1211 m, as claimed. The shortest stored branched set is id 2804, as claimed.
  - The feeder cap is 18, the feeders_per_root of the shortest set (45802). The object uses [18], so the cap holds.
- Result: all checks OK (work-reproduce/my_checker.out).

## Official validator (work-reproduce/scripts/official_check.py, optiwindnet 0.3.2)
- **claim/object/G.pickle:**
  - `validate_routeset(G)` returns `[]`.
  - The graph has 181 nodes and 180 edges; capacity=10, topology=BRANCHED, name 'Hornsea One.1_OSS'.
  - G.graph['VertexC'] is `np.array_equal` to the DB blob, and the border indices are identical to the DB; there are no obstacles.
  - Its edge set equals the (u,v) set in segments.json, and its length, recomputed via fnT, is 332729.34431381547.
- **G rebuilt from claim/object/routeset-packed.json:** I used `G_from_routeset` on a stand-in record carrying the packed fields plus the DB NodeSet row.
  - `validate_routeset` returns `[]` and there is no length_mismatch_on_db_read.
  - Its edge set equals both segments.json and G.pickle, its fnT equals G.pickle's, and its length is identical.
- **Same network:** the packed, pickle and segment objects therefore describe the same network.
- **Determinism:** I ran the script twice and the outputs are byte-identical.
- **Stored sets:** the validator returns 0 violations for each of the four stored sets.

## Doubtful points (none changes the verdict)
1. **Coincident feeder segments.** Under the u/v labels, three feeders share a segment with another feeder (the same root-to-turbine corridor), and a fourth feeder (root→201→146) bends on turbine 87's location.
   - This is the dataset's own "detour node on the turbine" convention, described in the 26.10-v4 release notes.
   - Stored sets 45802, 9644 and 2804 contain the same kind of coincident root segments at turbines 87/89/94/95, 6 such pairs in the case of 45802.
   - The validator, which checks overlaps, accepts it.
2. **Misleading packed metadata.** The `misc` of routeset-packed.json reports termination OPTIMAL, relgap 2e-11, bound 332665.74 and runtime 0.129 s. These describe the last CP-SAT sub-solve only and are not a global bound: the stored MILP branched bound is 322779.29.
   - This is metadata only and is not part of the criterion. It should not be presented as an optimality certificate if the object is ever stored.
3. **Handle.** The handle in packed/G is 'Hornsea_One_1_OSS', while the DB routesets use 'hornsea_1'. This is cosmetic and not part of the criterion.
4. **Release currency.** That this is the latest Zenodo version rests on the frozen status snapshot (no live check).

## Verdict
Every property in the criterion reproduces from the saved files with my own exact checker and with the official validator on both G.pickle and the rebuilt-from-packed graph:
- the length is recomputed, not taken from the files;
- the network is a capacitated branched forest with 18 feeders against a cap of 18;
- there are no proper crossings;
- every segment lies inside the border, and there are no obstacles;
- the nodeset is exact;
- the set is strictly shorter than all 4 stored sets of any topology.

There were no mismatches, no missing objects and no non-determinism.

pass: true
