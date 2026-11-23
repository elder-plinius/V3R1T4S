# Novelty review: Hornsea One.1_OSS, capacity 4, branched, 589790.5176 m

context: fresh novelty reviewer; inputs were the brief and the frozen claim folder only (CLAIM.md, REPRODUCE.md, criterion.txt, object/, references/, status/), plus the public web. Nothing else in the workspace was read; the claim folder was not modified (no __pycache__ left). Scratch files are in panel/work-novelty/. The review was interrupted between the status fetch and the write-up; the status source was fetched exactly once and not re-fetched.

## 1. Status source (one fetch, no retry)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Time: 2026-11-10T14:57:11Z, HTTP 200, 12622 bytes (saved as work-novelty/zenodo-latest-live.json).
- Value: latest version is still record id 23537067 (concept 20053478), title "OptiWindNet RouteSets", publication_date 2026-10-21, modified 2026-10-21T15:29:56Z, single file `optiwindnet-routesets-r26.10-v4.sqlite.xz`, 28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7.
- It differs from status/zenodo-latest.json only in the view/download counters.
- references/optiwindnet-routesets-r26.10-v4.sqlite.xz: md5 85faffb2... (matches Zenodo), sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches CLAIM.md). The compared table is therefore the current one.

## 2. Stored sets for the cell (read from the reference file)

Nodeset `Hornsea One.1_OSS` (T=174, R=1, B=25), capacity 4, four stored route sets:

| id | length (m) | creator | topology | feeders |
|---|---|---|---|---|
| 42471 | 591151.3395 | MILP.pyomo.cplex | radial | [45] |
| 9601 | 595070.4239 | baselines.hgs | radial | [44] |
| 2787 | 596799.9297 | MILP.pyomo.cplex | branched | [45] |
| 8898 | 604020.3250 | baselines.lkh | radial | [44] |

Object: object/segments.json has 206 segments, all endpoints are VertexC points, recomputed sum 589790.5176 m; 45 feeders; object/G.pickle passes `validate_routeset` with `[]` (sanity check only; full reproduction belongs to another reviewer). Margin over the shortest stored set: 1360.82 m, 0.230 %, far above 1e-6 relative. Not a tie. The object stays above the stored lower bounds (branched bound 587091.72 from id 2787), so the figure is not implausible.

## 3. Earlier and neighbouring published objects

Same site searched by name and by a rotation/reflection-invariant signature (sorted turbine distances to the centroid) over every nodeset in each file:

| source | same nodeset found | best capacity-4 length |
|---|---|---|
| Zenodo 20053479, r26.05-v4 (the release cited by the preprint) | yes, identical | 591151.34 (id 42471), same four rows |
| Zenodo 18864643 paperdb.v3 / 19798734 paperdb.v4 (EJOR paper data) | yes, identical coordinates | 594104.67 (id 9601, hgs, 44 feeders); 596799.93 (id 2787) |
| MILP_model_comparison.v3/.v4 (same two records) | no (11 nodesets, none with this site) | n/a |
| Zenodo 20140812 (thesis code: two zip archives) | no route-set data; no "Hornsea" string in any member | n/a |

Note: id 9601 is 594104.67 m in the older files and 595070.42 m in the current release; both are longer than the claim (by 4314 m at least).

Neighbouring cells, same nodeset: capacity 3 best 735948.75 m (valid at capacity 4 by restriction, but far longer); capacity 5 best 507652.12 m (not valid at capacity 4). `Hornsea One` with 3 substations (capacity 4: 347235.45 m) is a different instance (other substation positions). The `!Hornsea One.1_OSS!...` augmented nodesets have fewer turbines; deleting turbines cannot produce the 174-turbine object.

Other sources (2026-11-10, about 15:00Z and 23:00Z):
- github.com/elder-plinius/V3R1T4S: issue/PR full-text search (all states) for "Hornsea One", "Hornsea", "optiwindnet", "589790", and the newest 100 pull requests (#943 to #1052) listed directly. Hornsea One.1_OSS pull requests exist for capacities 5 to 12 only (#967, #968, #977 to #982, all open drafts); none for capacity 4 (or 2, 3). TROPHY_CASE.md: no cable-routing entry. known-knowns/: 228 entries in 31 families, none for cable routing; the only repository path about this target is known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md.
- github.com/DTUWindEnergy/OptiWindNet (last push 2026-10-19): releases v0.1.6 to v0.3.2 carry only wheel and sdist assets; the tree holds the location file optiwindnet/data/Hornsea One.yaml and four paper route-set pickles for other sites (Cazzaro, Taylor), no Hornsea One route set; no issue or pull request mentions Hornsea.
- Preprint wes-2026-124 (page updated 10 Nov 2026, discussion open until 18 Nov 2026): one referee comment (RC1, 3 Sep 2026) with no competing solutions; no community or author comments. It cites Zenodo 20053479 and 20140812. Partial text extraction of the PDF (about 32k characters; the extraction was incomplete) contains no "Hornsea".
- Web searches for the instance name, the benchmark name and cable-routing heuristics on this site returned no other published route set or length for this instance.

## 4. Is the object more than a trivial edit of the seed?

CLAIM.md names the seed: stored id 42471 (radial, 591151.34 m). Comparing turbine-level links (detour and contour clones collapsed to their end nodes), 174 links each:

| compared with | links only in object | common |
|---|---|---|
| 42471 (seed) | 18 | 156 |
| 9601 | 16 | 158 |
| 2787 | 39 | 135 |
| 8898 | 71 | 103 |

Against the seed, 18 links are replaced by 18 others, in two regions (turbines 88 to 112 and 159 to 173); the feeder set changes (94, 106, 110, 163, 164 gain a feeder; 93, 101, 105, 166, 169 lose theirs) and two turbines (106, 167) get degree 3, so the object is branched while the seed is radial. This is a combinatorial re-optimisation, not a deletion, restriction, relabelling, symmetry or numerical polish.

What trivial edits alone give: re-routing the unchanged topology of each stored set with optiwindnet's PathFinder returns exactly the stored lengths (591151.3395, 595070.4239, 596799.9297, 604020.3250), so detour polish of the seed gains 0 m. Restriction from capacity 3 gives 735948.75 m. The best figure reachable by the listed edits is thus the seed's own 591151.34 m, and the object beats it by 1360.82 m.

## 5. Verdict

The table is current, no shorter or equal route set for this instance was found in the current release, the earlier DTU datasets, the OptiWindNet repository and releases, the preprint and its discussion, or this repository's pull requests, trophy case and known-knowns. The object is seeded from a named published set and differs from it in 18 of 174 links, beating what trivial edits give.

Limits: the preprint PDF text was only partly extracted; the literature search cannot exclude unpublished or unindexed results; the pull-request check is as of 2026-11-10T23:02Z.

novelty: no prior equal or better object found; strict improvement of 1360.82 m (0.230 %) over the best known 591151.3395 m
pass: true
