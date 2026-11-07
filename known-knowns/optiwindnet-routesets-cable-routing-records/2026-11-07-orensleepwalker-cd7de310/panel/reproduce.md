context: subagent (fresh fork, claim only)

The supplied capacity-11 branched network for Hornsea One.1_OSS satisfies the stated fixed-release success criterion. This assessment used only ../claim/ as scientific evidence. No other run outputs, search scripts, or reviewer reports were consulted.

Before examining the objects or implementation, I wrote an independent checker from ../claim/criterion.txt. The relevant rule is: “a route set of topology X with strictly smaller total length than every stored route set for that instance of topology X or more restrictive (radial counts for branched), by more than 1e-6 relative, using at each substation no more feeders than the shortest such stored route set (feeders_per_root), and carrying the same nodeset (all turbines, substations, borders and obstacles from its VertexC blob).” It also requires no official-validator violations, segment containment, and recomputed Euclidean length.

I hashed ../claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz and obtained c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a, exactly the criterion's SHA256. I independently decompressed it into work-reproduce/reference.sqlite and queried the nodeset and every capacity-11 routeset attached to its digest. There is exactly one nodeset named Hornsea One.1_OSS; its name has no augmentation prefix. This verifies the archived release specified by the criterion; the saved status metadata does not independently establish live latest-version status.

The archive's VertexC contains exactly 174 turbine coordinates, 25 border vertices, and one substation coordinate. Its constraint groups are [25], with no obstacle groups. All VertexC entries in ../claim/object/G.pickle match the archive exactly, as does the complete ordered border. The object has no obstacle polygons. Every coordinate endpoint in ../claim/object/segments.json matches its archive coordinate exactly, including all four contour-clone mappings [175, 180, 182, 184]. The pickle's full vertex mapping was checked, including root indexing. T, R, B, capacity, clone counts, topology, and graph vertex and edge sets were also checked.

The complete physical network has 179 vertices and 178 unique undirected segments: 174 turbines, one substation, and four contour vertices. It is connected and acyclic, contains every turbine exactly once, and has exactly one substation in its connected component. An independent traversal checked the turbine count below every edge against capacity 11. The maximum turbine degree is 3, consistent with a branched topology. The substation has 16 feeders, equal to the shortest comparator's permitted count [16]. No feeder relaxation is involved.

All 178 cable segments lie in the closed site-border polygon, checked with polygon covers without a tolerance buffer. Obstacle exclusion is vacuous for this nodeset because the archive specifies zero obstacles. Every pair of segments was examined: 15,753 pairwise comparisons found no proper crossings, overlaps, or contacts except common graph endpoints. Each stored pickle edge length and each independently reconstructed edge length agrees with its Euclidean endpoint distance within 1e-8 m. Summing every physical segment gives 318217.6792903231 m, agreeing with both JSON length declarations and the pickle's summed edge lengths.

The database contains exactly four eligible comparison routesets; none was omitted. Radial sets were included for this branched claim. I also reconstructed each archived comparator and independently recomputed its full physical length, including contour and detour segments. Every result agrees with its stored length within 1e-7 m, and each stored feeder count agrees with the reconstructed graph.

| Routeset | Topology | Stored length (m) | Recomputed length (m) | Feeders |
|---|---|---:|---:|---:|
| 45874 | radial | 319646.1210316831 | 319646.1210316831 | 16 |
| 2803 | branched | 320947.13822234643 | 320947.1382223465 | 17 |
| 9639 | radial | 327712.9880414819 | 327712.9880414819 | 16 |
| 8926 | radial | 360256.15838726517 | 360256.15838726517 | 16 |

The candidate satisfies length < (1 - 1e-6) times each of these lengths. Against the shortest set, the improvement is 1428.4417413600022 m, or 0.44688223862989285%.

Using optiwindnet 0.3.2, I ran optiwindnet.validating.validate_routeset separately on ../claim/object/G.pickle and on a fresh graph reconstructed from ../claim/object/routeset-packed.json using the independently read archive nodeset. Both returned []. The reconstruction used the packed parent links and clone mapping; it did not reuse the pickle graph. Both graphs have exactly the same physical vertices, coordinates, and segments as ../claim/object/segments.json.

Invalid controls were rejected by the independent checks: a missing turbine, a cycle, capacity reduced to 10, feeder cap reduced to 15, a synthetic proper crossing, a segment leaving a closed border, and a segment entering an obstacle interior. Separate official-validator controls rejected capacity 10, an edge falsely stating load 999, and deletion of a root feeder. These checks exercise both structural failure detection and the separate geometric conditions absent from the official border/obstacle validator.

All numerical verification used the designated Python environment with OMP, OpenBLAS, and MKL threads set to one and bytecode writing disabled. Scratch checker work-reproduce/independent_check.py is NOT INCLUDED in the publication package ../claim/. Its machine-readable results are work-reproduce/result.json; its independently decompressed reference is work-reproduce/reference.sqlite. These are reviewer scratch artifacts, not additional scientific evidence supplied by the author. No claim files were changed.

pass: true
