# Novelty review: Hornsea One.1_OSS, capacity 3 (claim-ho3)

context: fresh novelty reviewer; inputs were only the panel brief, the frozen claim folder (read-only) and public web sources (Zenodo, GitHub, Copernicus, PyPI). No other workspace file was read. Work files: panel-ho3/work-novelty/ (analyse.py, extra.py, status.json, gh/, dl/). The session was interrupted once by a usage limit and resumed; the status source was fetched once, before the interruption.

## 1. Status source (fetched once, no retry)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time: 2026-11-10T14:57:09Z, HTTP 200, resolved to https://zenodo.org/api/records/23537067
- Value: latest version is still record 23537067, "OptiWindNet RouteSets", release 26.10-v4, publication date 2026-10-21, modified 2026-10-21T15:29:56Z; single file optiwindnet-routesets-r26.10-v4.sqlite.xz, 28,464,808 bytes, md5 85faffb2e13600b017f1b583b259edd7.
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz has that md5 and sha256 c78c8f3c...05e3a (as in CLAIM.md and criterion.txt); uncompressed md5 5ad6bf0449dcbd9939f1ae03bee19016 equals the value in the Zenodo release table. status/zenodo-latest.json differs from my fetch only in the view/download counters.
- The version list (https://zenodo.org/api/records/23537067/versions) shows exactly two versions: 20053479 (26.05-v4, 2026-05-06) and 23537067 (26.10-v4). No newer table exists.

## 2. The object

Rebuilt from object/routeset-packed.json on the stored nodeset (object/G.pickle was not loaded), optiwindnet 0.3.2:

- validate_routeset: [] (no violations); 242 segments; length 735605.4808 m from the rebuilt graph and from object/segments.json (sum of Euclidean segment lengths); every segment endpoint is a vertex of the stored VertexC.
- 58 feeders, maximum turbine degree 2 (radial), 174 logical links, straight-line length 733579.7566 m.

## 3. Published values for this cell

Instance (Hornsea One.1_OSS, capacity 3); the nodeset digest/VertexC is byte-identical (cc0b8615...e7b0) in all four databases below, so there is no renamed or rotated variant to reconcile.

| Source | id | solver, topology | feeders | length (m) |
|---|---|---|---|---|
| r26.10-v4 (Zenodo 23537067) and r26.05-v4 (20053479), same values | 40884 | CPLEX, radial | 58 | 735948.7528 |
| same | 9597 | HGS, radial | 58 | 738034.6339 |
| same | 2784 | CPLEX, branched | 59 | 739768.9053 |
| same | 8885 | LKH, radial | 58 | 753634.9352 |
| paperdb.v3 / paperdb.v4 (Zenodo 18864643 / 19798734, 2025) | 9597 | HGS | 58 | 737190.3548 |
| same | 2784 | CPLEX, branched | 59 | 739768.9053 |

- Shortest published length anywhere: 735948.7528 m (id 40884). The object is 343.2720 m shorter (4.66e-4 relative, above the 1e-6 threshold), with the same 58 feeders.
- The older 737190.3548 m for id 9597 (2025 paper databases) is the branched re-hooking of the HGS topology (I reproduce exactly that value by re-running PathFinder with branched topology); it is also longer than the object.
- MILP_model_comparison.v3/v4 (same Zenodo records) contain no Hornsea nodeset. Zenodo 20140812 (thesis code: optiwindnet_routesets.zip, data_driven_hybrid.zip) contains notebooks, figures and models, no route sets for this instance.
- Stored MILP bounds (straight-line objective): 732175.40 (radial run), 733051.42 (branched run); the object's straight-line length 733579.76 is above both, so no contradiction and no optimality is implied.

Neighbouring cells: capacity 2 stored sets (best 1031350.40 m, 87 feeders) are feasible for capacity 3 but far longer; capacity 4 stored sets (best 591151.34 m) all contain 4-turbine strings and are infeasible for capacity 3. The 3-substation nodeset "Hornsea One" is a different instance. The '!Hornsea One.1_OSS!...' augmented nodesets have other turbine sets.

## 4. Trivial-edit test against the named seed

CLAIM.md names the seed: id 40884 (shortest stored set).

- Logical links (detours contracted): 154 common, 20 only in the object, 20 only in the seed. Against id 9597: 25/25 differ; id 2784: 60/60; id 8885: 89/89.
- String partition: 47 of 58 strings identical; 11 strings covering 33 turbines are re-partitioned, 7 feeder hook turbines change. The changes form one connected region (no string keeps its membership with different internal links), i.e. a joint re-assignment, not a single swap.
- Straight-line saving 212.06 m (733791.81 -> 733579.76); detour overhead also drops 131.22 m (2156.94 -> 2025.72); total 343.27 m.
- What trivial edits of the seed give: recomputing detours with PathFinder 0.3.2 on the unchanged seed topology returns 735948.7528 m for both radial and branched feeder hooking (no gain). The same re-pathing of the other stored sets gives 737190.35 (9597, branched hook), 739768.91 (2784), 753378.04 (8885). Relabelling and symmetry do not apply (fixed coordinates, one substation); deletion/restriction cannot shorten a set that must connect all 174 turbines. The best trivial-edit value is therefore 735948.7528 m, and the object beats it by 343.27 m through 20 changed links.
- Re-pathing the object's own topology returns 735605.4808 m, so its length is not an artefact of a non-standard detour.

Not tested: whether a simpler published heuristic started from the seed would find the same links; this does not affect the comparison with published objects.

## 5. Repository, code and literature search

- github.com/elder-plinius/V3R1T4S (main at fb516440, 2026-11-09T19:54Z; checked 2026-11-10T23:00Z via the public API): TROPHY_CASE.md has no optiwindnet/Hornsea/cable entry; known-knowns/ has no directory for this target (31 targets, none cable routing); the target exists only as known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md.
- Pull requests, open and closed (issue search for Hornsea, optiwindnet, cable, routesets, "capacity 3", wind farm; plus the full list of PRs 836-1052, which covers everything since 2026-10-29): 18 claims on this target, all open drafts: #962, #963, #964, #967, #968, #977-#982, #998, #1027-#1030, #1036, #1037. Hornsea One.1_OSS appears at capacities 5-12 only (#967, #968, #977-#982). No pull request, open or closed, for Hornsea One.1_OSS capacity 3 (the only capacity-3 claim is Race Bank.1_OSS, #1036). The neighbouring Hornsea One.1_OSS claims start at capacity 5, whose strings exceed 3 turbines, so none restricts to this cell.
- OptiWindNet (github.com/DTUWindEnergy/OptiWindNet, last push 2026-10-19; releases v0.1.6 to v0.3.2): release assets are only wheels and sdists; the tree holds location files (optiwindnet/data/Hornsea One.yaml) and four paper route-set pickles for Cazzaro/Taylor sites, no Hornsea route set. PyPI latest is 0.3.2.
- Preprint wes-2026-124 (https://wes.copernicus.org/preprints/wes-2026-124/, in review, discussion open until 2026-11-18, one referee comment of 2026-09-03): reports only relative statistics, no per-instance lengths, no Hornsea One value, no comment offering shorter solutions.
- Web searches (Hornsea One cable routing with OptiWindNet/RouteSets; improved RouteSets solutions; 174-turbine Hornsea inter-array benchmarks) returned only the dataset, the preprint and unrelated work (e.g. a KIT cycle-cancelling study on a Hornsea-like instance with a different model and coordinates). No published route set for this nodeset and capacity other than the DTU records above. GitHub code search needs authentication and was not run.

## 6. Verdict

The object is strictly shorter (by 343.2720 m, 0.047%) than every published route set for (Hornsea One.1_OSS, capacity 3) in the current release, the previous release and the 2025 paper databases, at the same feeder count; it differs from its named seed by 20 of 174 links and beats what re-pathing, re-hooking, relabelling or restriction of any stored set gives; no competing or prior claim for this cell exists in the repository. Limits: validity and border containment are the other reviewers' subjects (only validate_routeset and length were re-run here); the improvement is small and no optimality is claimed.

novelty: beats all known for this cell
pass: true
