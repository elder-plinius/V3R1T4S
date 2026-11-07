# Independent criterion review: Hornsea One.1_OSS, capacity 6

context: fresh subagent (claim-ho6 and bank entry only)

This review was performed by a fresh subagent assigned the criterion-skeptic role. Scientific inputs were confined to the frozen `runs/2026-11-07-0928/claim-ho6/` package and the `optiwindnet-routesets-cable-routing-records` entry in `repo/bank/targets.json`. No other panels, earlier review conclusions, search outputs, or other run results were read. An independent checker was written before consulting OptiWindNet implementation code; no author search code was read. The frozen claim was not modified.

confirmed_scope: The frozen branched route set for Hornsea One.1_OSS at capacity 6 satisfies the full cell criterion against all four stored route sets for that instance in release r26.10-v4 as identified by the supplied status snapshot, without establishing global optimality or optimizer superiority.

The binding criterion is existential over one instance and one topology, but universal over every stored route set with that topology or a more restrictive topology. For a branched claim the comparison includes both radial and branched records. It does not require the candidate to remain radial merely because the shortest stored record is radial. This candidate is genuinely branched: its maximum turbine degree is 3. Its name has no `!` prefix, so neither partial-win provision is needed.

The reference archive has SHA-256 `c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a`, matching the binding entry. Its MD5 is `85faffb2e13600b017f1b583b259edd7`, matching the file in `claim-ho6/status/zenodo-latest.json`. That snapshot identifies record 23537067, revision 4, DOI `10.5281/zenodo.23537067`, last modified 2026-10-21T15:29:56.915326+00:00. This is a fixed-release, supplied-snapshot conclusion; it makes no assertion that the snapshot remains the live latest version after it was captured.

The SQLite query selected the unique nodeset named `Hornsea One.1_OSS`, then every routeset whose `nodes_id` equals that nodeset's digest and whose capacity is 6. Exactly four records matched; none was discarded by topology, solver, bound, feeder count, or method. Their complete comparison is:

| Stored ID | Topology | Stored full length (m) | Feeders | Candidate improvement (m) |
| --- | --- | ---: | --- | ---: |
| 45811 | radial | 450092.351727352 | [30] | 903.531415931 |
| 2799 | branched | 451220.991859569 | [30] | 2032.171548148 |
| 9634 | radial | 452600.508127449 | [29] | 3411.687816028 |
| 8922 | radial | 464173.546237935 | [30] | 14984.725926514 |

Every row separately satisfies `candidate_length < (1 - 1e-6) * stored_length`. The tightest threshold is 450091.90163500025 m, leaving 903.081323579012 m of strict-threshold margin. The improvement over the shortest stored set is 903.5314159307745 m, or 0.20074356128541768%. These are comparisons of full stored `length`, including detours, rather than `misc.objective` or a MILP lower bound.

The feeder bound is the per-root count of the shortest eligible stored route set, ID 45811: `[30]`. The candidate uses `[30]`, satisfying that bound. Record 9634's smaller count `[29]` does not replace the binding criterion's explicitly specified shortest-record bound. This distinction matters: requiring the candidate to satisfy every comparator's feeder count would be a different criterion.

Independent checks establish exact instance identity. The archived VertexC blob has SHA-256 and nodeset digest `cc0b8615dad646d5f4cbc7b079e021b0120da295fb6e213ccd27b5129f26e7b0`. It contains 174 turbine coordinates, 25 border vertices, and one substation coordinate, with shape `(200, 2)` and all coordinates finite. The sole constraint group has 25 vertices and defines a valid site polygon; there are no obstacle polygons. The pickle's full coordinate array equals the decoded archive array exactly, and its border indices equal the archive's constraint vertices. Every segment endpoint equals the corresponding archived prime coordinate exactly, including contour and detour clones. No turbine, substation, border, or obstacle has been substituted or dropped.

The explicit segment network has 202 vertices and 201 edges: 174 turbines, one substation, two contour clones, and 25 detour clones. It is one connected acyclic component containing exactly one root; every turbine occurs once as its own graph vertex. All clone vertices have degree two. Independently traversing away from the root and counting only real turbines gives 30 feeder subtrees: 28 carry six turbines, one carries five, and one carries one, summing to 174. Every non-root subtree and every cable load is at most 6. All stored node loads and edge loads agree with these independent counts.

All 201 cable segments are covered by the closed archived border polygon. Obstacle avoidance is vacuous because this exact instance has zero obstacles. An exhaustive pairwise segment check found no proper segment crossings. It also recorded 45 coincident segment-pair overlaps and 142 point contacts between edges with distinct graph endpoints. These contacts cannot be hidden by describing the drawing as disjoint: they arise in the clone representation of segmented routes. OptiWindNet 0.3.2 checks complete route polylines and their local ordering through shared runs, including overlap crossings, branch splits, and self-intersections; its rules permit a shared corridor that does not exchange sides. The full official validator returned `[]` on both the frozen pickle and a fresh reconstruction from the packed object plus the archived nodeset. Thus the required crossing check passes under the specified validator's route semantics, alongside the independent border and proper-crossing checks.

The three object representations agree. The parent-vector interpretation of `object/routeset-packed.json` was independently expanded using turbine IDs followed by contour/detour clone IDs; its undirected edge set exactly equals both `object/segments.json` and `object/G.pickle`. A separate official `G_from_routeset` reconstruction, supplied the archived nodeset rather than the pickle's coordinates, also agrees on edges, coordinates, clone mapping, loads, and individual segment lengths. Both official validations returned no violations with OptiWindNet version 0.3.2.

The value used for comparison was independently recomputed with `math.fsum(math.dist(a,b) for each segment)`, yielding **449188.82031142124 m**. Every cable segment is counted, including distinct cables occupying coincident geometric corridors; the length is not the length of their geometric union. The recomputation agrees with the segment JSON's recorded total, the packed length, each pickle edge's Euclidean length, and the fresh reconstruction's full length.

The frozen object hashes are:

| Object | SHA-256 |
| --- | --- |
| `object/segments.json` | `b06859d806e341c850264459f1f0f8bb0fa7c2039b253da4e3b803f1273f6395` |
| `object/routeset-packed.json` | `38e89fe442554d209a8e5d4d17bdd0546dc8e19294c60e30707101f76b8b4b44` |
| `object/G.pickle` | `830846712933194587af3a23234781c9a77423a881ec25f520ed97bd21de9e41` |

The preregistered null-test exemption is appropriate for this precise claim: a frozen explicit feasible network is shorter than fixed archived values by a deterministic inequality. Selecting the shortest qualifying object from several seeds does not turn that inequality into a statistical claim or require a search-yield null distribution. This review does not verify a general algorithmic advantage, expected seed performance, runtime advantage, significance, or global optimality. Packed solver bounds, gap values, termination labels, and runtimes from a restricted sub-solve provide none of those conclusions and were not used as criterion evidence.

Independent scripts and machine-readable receipts are in `panel-ho6/work-criterion/check.py`, `panel-ho6/work-criterion/check_official.py`, `panel-ho6/work-criterion/independent-results.json`, and `panel-ho6/work-criterion/official-results.json`, relative to this run directory. Both checks completed successfully with bytecode disabled and numerical threads capped at one. All scratch code, the decompressed scratch database, and scratch receipts are explicitly excluded from any future contribution package; this review is the publishable technical evidence. No outward write or publication was performed.

pass: true
