# Novelty review: Hornsea One.1_OSS, capacity 11, branched

Context: independent subagent, fresh fork. Scientific inputs were the claim directory and independently consulted public sources. This review concerns the submitted route set as a new benchmark entry, not a new optimization method or an optimality claim.

The supplied object is shorter than the relevant public objects located in this review, and the tested cheap transformations do not recover its improvement. No relevant novelty blocker remains after completing the current-release check below.

## Current public status

The first sandbox transport attempt at 2026-11-07T10:09:06.882843Z failed DNS resolution; it received no HTTP response. A single ordinary network-enabled request to `https://zenodo.org/api/records/23537067/versions/latest`, started at 10:10:06Z, returned HTTP 301 with the advertised Location `https://zenodo.org/api/records/23537067`. Its 99-byte response has SHA-256 `8ee7439c5f4b8da2a75cebc144d1625c51f98cac6ed8eaf64be5bac491bdd3d7`. Following that exact canonical Location at 10:13:09.946914Z returned HTTP 200; the raw JSON response has SHA-256 `a1eb5479cd7a9ccde50311ad180aa7451d9ddefe70c23f253759299713637bad`. The original endpoint was not requested again, and there was no denial or challenge response.

The response identifies record 23537067, release 26.10-v4, published 21 October 2026, and marks it as the last version in its version relation. The supplied compressed archive matches both its claimed SHA-256 `c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a` and the freshly obtained public MD5 `85faffb2e13600b017f1b583b259edd7`. Thus this check is resolved, not PENDING STATUS CHECK. [Current public record](https://zenodo.org/records/23537067).

## Independent object comparisons

I decompressed my own copies of the supplied SQLite archives, decoded the stored parent arrays and clone coordinates, and summed Euclidean cable-segment lengths. The packed claim and its independent segment list both yield **318217.6792903231 m**. The four capacity-11 rows for the exact nodeset in the current release recompute as follows:

| Route set | Recomputed length, m | Feeders |
|---|---:|---:|
| 45874, disclosed CPLEX radial seed | 319646.1210316831 | 16 |
| 2803, CPLEX branched | 320947.1382223465 | 17 |
| 9639 | 327712.9880414819 | 16 |
| 8926 | 360256.15838726517 | 16 |

The claimed gain over 45874 is **1428.4417413600 m**, approximately **0.44688%**. This comparison uses routed cable length, not a model objective or a stored gap.

The current APIs for [18864643](https://zenodo.org/records/18864643), [19798734](https://zenodo.org/records/19798734), and [20140812](https://zenodo.org/records/20140812) each returned HTTP 200. All six supplied legacy archive MD5s match the independently fetched metadata. Their latest-version pointers resolve 18864643 to 19798734, 19798734 to itself, and 20140812 to itself. I decompressed all four legacy SQLite files. Both paper databases contain the exact single-substation Hornsea geometry, including the same full VertexC SHA-256 `cc0b8615dad646d5f4cbc7b079e021b0120da295fb6e213ccd27b5129f26e7b0`, border indices, and root. Their Hornsea route sets cover capacities 2–5 only; neither supplies a capacity-11 predecessor. The two MILP-comparison databases contain no 174-turbine nodeset.

I inspected both thesis ZIP archives as data, including notebook saved outputs and manifests. They refer to the separate public benchmark release [20053479](https://zenodo.org/records/20053479), rather than embedding an additional Hornsea route-set database. I independently fetched that record and downloaded/decompressed release 26.05-v4. Its compressed MD5 matches `38d4b0e96797bb103d1af817584fd7da`; SHA-256 is `2669af38133cbb650a9225f856259def18163cd9aee25afe8a014dfc6f9453d2`. Its four capacity-11 Hornsea lengths recompute to the same four values listed above. No downloaded code was executed.

## Names, orientations, and neighboring capacities

I screened every 174-turbine nodeset in the six inspected databases by sorted pairwise-distance signatures, allowing scale, rotation, reflection, and relabeling, then fitted the matching coordinates. This finds the exact single-substation geometry in both legacy paper databases and both benchmark releases. The other matching turbine cloud is `Hornsea One`, with three substations; its nearest transformed root differs from the claimed root by 756.10 m. Its shorter routes solve a different instance.

Distinct turbine distance signatures in the target differ by at least 569.62 m in a signature component, excluding a hidden nonidentity rigid symmetry of this point cloud at the tested tolerance. Geometric edge sets were compared after coordinate canonicalization, independent of vertex labels. The claim differs from its disclosed seed by 12 removed and 12 added links. Suppressing degree-two contour clones leaves the same 12-link replacement count: the change is not merely another geometric embedding of the seed topology.

All four stored capacity-10 solutions use 18 or 19 feeders, exceeding this claim's cap of 16. All four capacity-12 solutions have multiple feeder trees of load 12, exceeding capacity 11: the counts of overloaded trees are 11, 13, 10, and 11 for route sets 2805, 9645, 8929, and 45373 respectively. A direct capacity relabeling therefore does not supply a valid shorter predecessor.

## Cheap-edit controls

I wrote independent comparison and exchange code. On seed 45874 it enumerates one-edge removals and reconnections between the resulting components, checking tree structure, subtree capacity, feeder count, containment, and segment intersections.

The best feasible single-link change saves **522.4561494880 m**, producing **319123.6648821952 m**. Repeated steepest feasible one-link changes take five steps and stop at **318767.7150777083 m**, still **550.0357873852 m** above the claim. All accepted intermediate networks pass these independent checks. This is a tested local-search endpoint, not a global bound or proof against other sequences of cheap edits.

I also tested shortcutting each of the seed's four degree-two contour clones; all four apparent length savings are geometrically infeasible. Enumeration of both standard reconnections for every pair of vertex-disjoint seed edges produced 86 positive-gain candidates, none feasible. These controls support an improvement beyond the tested trivial transformations; they do not establish a new algorithm.

## Public literature, code, and contributions

The literature search covered the preceding 24 months, 7 November 2024 through 7 November 2026, using OptiWindNet, Hornsea One/Hornsea I, cable routing, `Hornsea One.1_OSS`, and `wes-2026-124`, together with official sources and release metadata. The [dataset preprint](https://wes.copernicus.org/preprints/wes-2026-124/) links the earlier benchmark and thesis artifacts examined above. The [official dataset documentation](https://optiwindnet.readthedocs.io/stable/dataset.html) and [upstream changelog](https://gitlab.windenergy.dtu.dk/TOPFARM/OptiWindNet/-/blob/main/CHANGELOG.md) document solver and PathFinder developments; they do not identify an additional capacity-11 Hornsea object. The recent [multi-stage inter-array-cabling paper](https://wes.copernicus.org/articles/11/3887/2026/) uses Hornsea I with three substations, a different root specification. A separate wind-hydrogen joint-planning paper also uses Hornsea turbines but changes the planning variables and system specification; it supplies no identified exact-instance predecessor in this search.

The live [V3R1T4S TROPHY_CASE](https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md) and the complete recursive main-branch tree were checked. No OptiWindNet family appears in main's known-knowns tree at checked commit `6bb0dcfd1623abe2f827b90059d01a007eb310f0`.

Direct GitHub API searches used explicit `is:pull-request` or `is:issue`, separately covering open and closed states. The target repository has five open OptiWindNet PRs, zero closed OptiWindNet PRs, and zero matching open or closed issues. Two concern Hornsea: [PR 967](https://github.com/elder-plinius/V3R1T4S/pull/967), capacity 10, and [PR 968](https://github.com/elder-plinius/V3R1T4S/pull/968), capacity 8. Both are open and unmerged. Their public packed objects were independently fetched and decoded: 332729.34431381547 m with 18 feeders, and 377034.6924851112 m with 22 feeders, respectively. They differ from the claim by 39/38 and 62/64 geometric links respectively, and exceed this instance's feeder limit. They establish prior use of the disclosed general search approach, not prior publication of this capacity-11 object. Public upstream GitLab searches for Hornsea across all issue and merge-request states found no issue and one merged location-addition request, unrelated to this record.

The defensible novelty is a specific shorter feasible candidate for this benchmark instance, credited to the disclosed stored seed and existing software. It is not a claim of optimality, a new method, or a record for the original three-substation farm. Search coverage is finite; none of the identified sources supplies an unresolved relevant predecessor.

Scratch artifacts **NOT INCLUDED** in the publishable claim: `work-novelty/compare.py`, `work-novelty/extra_controls.py`, comparison JSON, decompressed databases, public API copies, and transport receipts. These retain the independent calculations and exact raw responses for this review.

pass: true
