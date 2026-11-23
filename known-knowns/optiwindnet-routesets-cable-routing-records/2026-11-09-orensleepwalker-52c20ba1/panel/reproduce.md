# REPRODUCE review: claim-so4 (Sofia, capacity 4, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder)

Reviewer role: REPRODUCE skeptic. I read only files in the claim folder. All work is in `panel-so4/work-reproduce/`. Python ran with `-I` and `PYTHONDONTWRITEBYTECODE=1`, with OMP_NUM_THREADS=1. The claim folder is read-only, and I left no `__pycache__` in it.

## Criterion implemented (quoted from criterion.txt)

> For one (nodeset, capacity) instance of release r26.10-v4 whose nodeset name does not start with '!', and topology X (radial or branched), a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob). It must pass optiwindnet.validating.validate_routeset with no violations (topology, capacity, loads, crossings), every route segment must stay inside the site border and outside every obstacle polygon (checked separately, since the validator does not test this), and its length, recomputed as the sum of Euclidean segment lengths in metres, must be the value compared.

## Reference data

- `references/optiwindnet-routesets-r26.10-v4.sqlite.xz`: sha256 is c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, which matches CLAIM.md and the criterion. md5 is 85faffb2e13600b017f1b583b259edd7, which matches the file checksum in `status/zenodo-latest.json`. That snapshot has record 23537067 with `is_last: true` and updated 2026-10-21. I made no network check of a newer version, so the "latest" status depends on the saved snapshot.
- My own decompressed copy (`work-reproduce/db/rs.sqlite`) has sha256 9aa8214c43a78f22978000aca1833f8428b0dc9c8ace8dab0f4ba3182e4245e1. It holds 49,204 routesets over 13,954 (nodeset, capacity) pairs, which matches the statement.
- Nodeset `Sofia`: there is exactly one row and the name has no '!' prefix. T=100, R=1, B=6. VertexC is a 107x2 float64 array. constraint_groups is [6] and constraint_vertices are [100..105], so there is one border hexagon and 0 obstacles. The border is valid and convex (I checked exact orientation signs).
- The routeset rows with nodes_id equal to the Sofia digest and capacity=4 are exactly 4. No other non-'!' nodeset has handle sofia at capacity 4.

| id | topology | creator | length (m) | feeders_per_root |
|---|---|---|---|---|
| 46020 | radial | baselines.lkh | 378587.2597106476 | [25] |
| 25155 | branched | MILP.pyomo.cplex | 378897.56575920776 | [25] |
| 35902 | radial | MILP.pyomo.cplex | 379237.6114224883 | [25] |
| 25008 | radial | baselines.hgs | 379237.7078552921 | [25] |

## Own checker (`work-reproduce/scripts/own_check.py`, does not import optiwindnet)

The checker works on `object/segments.json` (113 segments) plus the nodeset from the database. It uses `object/routeset-packed.json` only for clone2prime and C/D. Results:

- **Endpoints:** every segment endpoint equals VertexC of its node exactly (bitwise float equality). For detour clones (indices 106..118), it equals the clone's prime from clone2prime. No border vertex is used as a route node.
- **Length:** math.fsum of hypot over the 113 segments gives 377027.9309567514 m. This equals the value in segments.json and the packed length exactly.
- **Topology:**
  - Every clone has degree 2 (a pass-through bend point). Collapsing each clone chain into one electrical link gives 100 links on 101 nodes.
  - A traversal from the root reaches all 100 turbines with no cycle, so every turbine is connected exactly once and the network is a tree.
  - Every feeder subtree holds exactly 4 turbines (25 subtrees of size 4), so the capacity of 4 is respected.
  - The substation has 25 feeders, which matches packed feeders_per_root.
  - The maximum turbine degree is 3, so the network really is branched.
- **Crossings:** I used exact rational arithmetic (Fraction) over all segment pairs. I found 0 proper crossings, 0 partial collinear overlaps, 0 T-touches, and no segment passing through a vertex that is not its endpoint.
- **Border and obstacles:** every segment is strictly inside the border. shapely `covers` and `contains` both hold, and no segment touches the boundary. The exact convex test also passes: every endpoint is inside every edge half-plane. There are no obstacles in the nodeset.
- **Comparison:** the claim is strictly shorter than all 4 stored sets of any topology. The relative differences are 0.411881% (46020), 0.493441% (25155), 0.582664% (35902) and 0.582689% (25008), all far above 1e-6.
  - The cap is 46020's feeders_per_root of [25], and the claim uses [25], which is ≤ the cap.
  - The claimed difference of 1559.3288 m (0.412%) to 46020 is confirmed.
- **Determinism:** I ran the checker twice and the outputs are byte-identical (`own_check.run1.out`, `own_check.run2.out`). The result is PASS.

**Note on my first run** (`own_check.first-run-unrefined.out`): it failed on "collinear overlaps", in 13 pairs.
- On inspection, every one of these pairs is a geometrically identical segment, meaning the same two endpoint coordinates. Examples: root→62 / root→clone109 / root→clone112 (both clones have prime 62), and 35–44 / clone106–clone107.
- These are shared corridors produced by the optiwindnet detour (clone) model. They are not partial overlaps or crossings.
- I then split the check into identical-geometry (allowed) and partial overlap (fail), and found no partial overlaps.
- This split is justified by the stored sets: all 4 stored sets of this instance contain the same feature (6–8 duplicate-geometry segments each, see below), and the official validator accepts them. The claim has 11.

## Official validator (`work-reproduce/scripts/official_check.py`, optiwindnet 0.3.2)

- **Loading `object/G.pickle`:** I first listed its pickle globals with pickletools. They are only networkx, numpy, bitarray and optiwindnet.types classes. I then loaded it through a whitelisting unpickler.
  - `validate_routeset(G.pickle)` returns `[]`.
  - Its VertexC is bitwise-identical to the database blob. Its border is [100..105] and it has no obstacles.
  - name is Sofia, capacity is 4 and the topology is branched.
- **Rebuilt graph:** I rebuilt G from `object/routeset-packed.json` with `optiwindnet.db.storage.G_from_routeset`, using the database Sofia nodeset row and a stub method record.
  - `validate_routeset(rebuilt)` returns `[]`.
  - The rebuilt length is 377027.9309567514, with no length_mismatch_on_db_read.
- **Same network in all three objects:**
  - The pickle and the rebuilt graph have identical node sets.
  - They also have identical edge sets, compared as (node id, prime coordinate) pairs over 113 edges.
  - `pack_G(G.pickle)` reproduces the packed json's R, T, C, D, capacity, feeders_per_root, edges, clone2prime, num_diagonals and length exactly.
  - The segments.json edge set equals the pickle edge set.
  - Root load is 100, max_load is 4, and there are 25 feeders in both graphs.
- **Stored sets:** for context, I ran the same validator on all 4 stored sets. Each returns `[]` and each recomputed length equals its stored length.
- **Determinism:** two runs are byte-identical.

## Doubtful or noteworthy points (none breaks the criterion)

1. **Shared corridors and pass-over bend points.** Detour clones sit at turbine coordinates, so some cables are routed over turbine positions, and up to 3 feeders share the same root-to-turbine corridor (root→62 and root→43). This is the same modelling convention used in every stored set of the instance (6–8 duplicate-geometry segments each), and validate_routeset accepts it. If a reader treats parallel cables in one corridor as overlap, it would affect the stored sets equally.
2. **Misleading metadata in the packed object.** `misc` contains creator `MILP.ortools.cp_sat`, termination `OPTIMAL`, `bound` 375860.98 and `relgap` 8e-12.
   - These describe the last LNS sub-solve, which had the other turbines pinned. They are not a global lower bound for the instance.
   - The stored full-instance branched MILP bound is 373560.51 (id 25155), which is lower.
   - CLAIM.md correctly disclaims optimality, but if this object were stored as is, the misc fields would misstate a certified optimum.
   - This is not part of the criterion. It is a documentation and caveat issue.
3. **Zenodo version.** I relied on the saved snapshot `status/zenodo-latest.json`. I could not confirm with a live re-check that no newer Zenodo version exists today.
4. **Cosmetic difference.** The packed handle is "Sofia" while the database handles are "sofia". This has no effect.
5. **No slack in the feeder cap.** The cap of 25 equals ceil(100/4), and every subtree is full (4 turbines). The feeder constraint is satisfied with no slack, which is expected.

## Verdict

From the saved files I independently confirmed every property in the criterion:
- the same nodeset
- the recomputed length
- the capacitated branched forest
- the feeders compared with the cap
- no crossings
- border and obstacle containment
- endpoints at VertexC
- the strict comparison against all 4 stored sets

The official validator returns [] on both the pickle and the graph rebuilt from the packed json. All three object files describe the same network, and every result is deterministic.

pass: true
