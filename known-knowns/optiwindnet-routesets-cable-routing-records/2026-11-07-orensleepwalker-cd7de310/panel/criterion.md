# Criterion skeptic report

Context: subagent in a fresh fork, given only the fixed claim artifacts and the bank entry `optiwindnet-routesets-cable-routing-records` as scientific inputs. I did not read other workspace notes, search outputs, or reviewer reports. I wrote an independent checker for the explicit segments, graph, database quantifiers, and geometry; no author checking or search code was supplied in the claim. The installed OptiWindNet implementation was used only to interpret its storage format and run its required official validator.

confirmed_scope: The fixed branched route set for the non-augmented Hornsea One.1_OSS instance at capacity 11 satisfies the full bank success criterion against every stored route set for that instance in the hash-pinned r26.10-v4 release, with release status supported by the supplied latest-version snapshot.

The verdict is true for that deterministic, explicit-object scope. It does not establish an instance-wide optimum, search success probability, method superiority, or a live latest-version state beyond the supplied snapshot.

## Identity and completeness

The reference archive in [the claim](../claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz) has SHA256 `c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a`, exactly the bank's specified release hash. Its decompressed SQLite MD5 is `5ad6bf0449dcbd9939f1ae03bee19016`, agreeing with the release description in [the status snapshot](../claim/status/zenodo-latest.json). The table contains 49,204 route sets.

Exactly one nodeset row is named `Hornsea One.1_OSS`; its name does not begin with `!`. Its digest is `cc0b8615dad646d5f4cbc7b079e021b0120da295fb6e213ccd27b5129f26e7b0`. It has 174 turbine coordinates, 25 border coordinates, one substation coordinate, and no obstacle polygons. The full 200-by-2 `VertexC` array in the submitted graph is element-for-element equal to the database blob, including every border and substation coordinate. The ordered border indices and empty obstacle collection also agree exactly.

The [segments](../claim/object/segments.json), [packed representation](../claim/object/routeset-packed.json), and [graph](../claim/object/G.pickle) have the same edges, endpoint coordinates, instance dimensions, capacity, and branched topology. Four routing clones map to border vertices 175, 180, 182, and 184. All 178 segment endpoints are exactly the appropriate database coordinates under that mapping. Packing the submitted graph again reproduces the entire packed JSON object exactly, including all metadata fields.

Object SHA256 values are:

| Artifact | SHA256 |
| --- | --- |
| `object/segments.json` | `cd7de310ffc41ffd63056ba2cd56109a52f26713561732f9ba0661bfc9d14e8b` |
| `object/routeset-packed.json` | `3dec320cc5f234d905de30df0a5818300d6bbe48a00deade6ceb7e788a4066b9` |
| `object/G.pickle` | `13ad17a0c752214a5554bc3709ddcfcca773776fcba26130015e32a16d17982d` |

## Every comparator and each feeder constraint

I queried all rows matching the nodeset digest and capacity 11 without filtering by topology or solver. There are exactly four; all are radial or branched and therefore all enter the branched criterion:

| Stored id | Topology | Stored length, m | Feeders | Relative improvement of object |
| --- | --- | ---: | --- | ---: |
| 45874 | radial | 319646.1210316831 | [16] | 0.0044688223862989285 |
| 2803 | branched | 320947.13822234643 | [17] | 0.008504387816452193 |
| 9639 | radial | 327712.9880414819 | [16] | 0.02897446576013292 |
| 8926 | radial | 360256.15838726517 | [16] | 0.1166905217807599 |

The independently recomputed Euclidean sum over all 178 submitted segments, including the routing-clone bends, is **318217.6792903231 m**. Every stored edge length and both submitted total-length fields agree with that sum within `1e-7 m`; the comparison uses stored `length`, not `misc.objective`. The shortest stored row is id 45874. The improvement is 1428.4417413600022 m, or approximately 0.44688224%. Its relative margin is strictly greater than `1e-6`; since it is the minimum margin over all four rows, the quantified comparison passes for every stored set.

The graph has 179 vertices and 178 distinct nondegenerate edges. Independent forest and connectivity checks find one tree with exactly one substation, all 174 turbines, and four degree-two routing clones. Every turbine occurs exactly once. The maximum turbine degree is 3, so its actual shape is branched. Independently recomputed descendant loads agree with all stored node and edge loads. The 16 root-feeder subtrees comprise fourteen loads of 11 and two loads of 10, totaling 174; each meets capacity 11. The sole substation uses 16 feeders, exactly its individual cap of 16 from the shortest stored row. Thus neither a relaxed feeder allowance nor omission of a root-specific constraint explains the improvement.

## Geometric and official validation

The border polygon is valid. Shapely's closed-set `covers` test accepts every full segment with no buffer or containment tolerance. The instance has no obstacle polygons, making the obstacle-interior exclusion universal condition vacuous. Pairwise checks of all 15,753 segment pairs find no proper crossings, overlaps, or contacts away from a shared graph endpoint. All endpoint coordinate checks are exact.

`optiwindnet.validating.validate_routeset` from installed version 0.3.2 returns `[]` on the submitted graph. This corroborates, rather than replaces, the independent structural, capacity, load, intersection, and containment checks.

## Status and interpretation

The supplied status snapshot identifies published, submitted, completed record 23537067, DOI `10.5281/zenodo.23537067`, with its version marked `is_last: true`. Its archive filename, size of 28,464,808 bytes, and compressed-file MD5 `85faffb2e13600b017f1b583b259edd7` match the supplied archive. The snapshot SHA256 is `a1eb5479cd7a9ccde50311ad180aa7451d9ddefe70c23f253759299713637bad`. Its record modification timestamp is 2026-10-21T15:29:56.915326+00:00; that timestamp is not a reviewer observation time. No live external request was made under the claim-and-bank-only input restriction. The confirmed comparison is explicitly to r26.10-v4 and the supplied latest-version snapshot.

Packed `termination: OPTIMAL`, `strategy: OPTIMAL`, zero `relgap`, equal objective/bound, runtime, creator, and warmstart fields are internally consistent across the packed and graph artifacts. Per the claim's explicit disclosure, they describe only the last pinned restricted sub-solve. They provide no full-instance optimality certificate. The provenance of that sub-solve is an author assertion, unnecessary to and not independently established by this deterministic feasibility-and-improvement check.

The explicit-object null exemption applies: the proposition concerns fixed coordinates, fixed edges, and fixed release table values. No statistical significance, success-rate, selection-adjusted inference, or global-optimum inference is asserted or needed. Selection among five declared workers does not weaken these literal deterministic checks and supplies no evidence for broader claims.

The independent scratch files [check.py](work-criterion/check.py), [results.json](work-criterion/results.json), and `work-criterion/release.sqlite` are **NOT INCLUDED in the publication package**. The checker ran with bytecode disabled and numeric-library thread counts set to one. All 44 checks passed; no required clause within the stated confirmed scope remains unresolved.

pass: true
