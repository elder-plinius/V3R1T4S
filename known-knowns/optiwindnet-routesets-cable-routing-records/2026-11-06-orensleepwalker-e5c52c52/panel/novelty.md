# Novelty skeptic: OptiWindNet RouteSets r26.10-v4, Cazzaro-2022G-210.solid.1_OSS, capacity 6, radial

context: subagent (Claude Code Agent tool, fresh context, saw only claim/ and the public web)

Claim under review: claim/CLAIM.md. A radial route set (claim/object/) with length 396403.7269 m, against the stored radial best 401553.2842 m (id 25098) and the stored branched best 399738.0433 m (id 25278).

Working files are in panel/work-novelty/ (fetched/, db/, scripts/compare.py, comparison.txt).

## 1. Status source (fetched once, plain GET, no retry)

- URL: https://zenodo.org/api/records/23537067/versions/latest
- Fetch time: 2026-11-06T00:20:12Z (UTC). HTTP 200. The URL redirected to https://zenodo.org/api/records/23537067.
- Values read:
  - Record id 23537067, DOI 10.5281/zenodo.23537067, concept DOI 10.5281/zenodo.20053478.
  - publication_date 2026-10-21; created/modified 2026-10-21T15:29:56Z; revision 4; status published.
  - `metadata.relations.version = [{index: 1, is_last: true}]`. The description states "Release 26.10-v4" and has a "Changes in 26.10-v4" section.
  - Only file: `optiwindnet-routesets-r26.10-v4.sqlite.xz`, size 28464808, checksum `md5:85faffb2e13600b017f1b583b259edd7`.
  - Uncompressed MD5 listed in the description for 26.10-v4: `5ad6bf0449dcbd9939f1ae03bee19016`.
- Our fetched JSON is byte-identical to claim/status/zenodo-latest.json (sha256 dc186a60...e99b8).
- Release file check, on my own copy of claim/references/optiwindnet-routesets-r26.10-v4.sqlite.xz:
  - .xz sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a
  - .xz md5 85faffb2e13600b017f1b583b259edd7, matching Zenodo
  - decompressed md5 5ad6bf0449dcbd9939f1ae03bee19016, matching Zenodo
- **Conclusion: r26.10-v4 is still the latest version at 2026-11-06T00:20Z. The reference file is the published one.**

## 2. Stored route sets for the instance (release r26.10-v4)

Nodeset `Cazzaro-2022G-210.solid.1_OSS` has T=210, R=1, B=19 and no obstacles. Its capacity-6 rows:

| id | solver | topology | length (m) | feeders | straight-line objective | notes |
|---|---|---|---|---|---|---|
| 25278 | CPLEX (pyomo) | branched | 399738.0433 | [36] | 393908.25 | 6 h limit (21600 s), maxTimeLimit; bound 384837.74; relgap 2.30%; warm start rs_id 25098; feeder_limit min_plus1 |
| 25098 | HGS-CVRP | radial | 401553.2842 | [36] | 394783.71 | timeLimit 120 s; method options seed 20241113 |

There are no other capacity-6 rows (no LKH, no Gurobi).

**Strongest known value for this instance and capacity: 399738.0433 m (id 25278, branched). The strongest radial value is 401553.2842 m (id 25098).**

The claimed 396403.7269 m is:
- 3334.3164 m (0.834%) below the branched best;
- 5149.5573 m (1.282%) below the radial best.

Both margins are far above the 1e-6 relative threshold. The claim uses 36 feeders, equal to the cap of 36.

The CPLEX bound (384837.74) bounds the model's straight-line objective, not the detoured length. The claim sits 3.0% above it, so nothing contradicts it.

## 3. V3R1T4S repository (https://github.com/elder-plinius/V3R1T4S)

Each page was fetched once.

- Repo metadata: https://api.github.com/repos/elder-plinius/V3R1T4S, 2026-11-06T00:21:54Z, 200. Default branch main, pushed_at 2026-11-05T18:59:11Z.
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/HEAD/TROPHY_CASE.md, 2026-11-06T00:21:54Z, 200, 31306 bytes. No match for optiwind, cable, wind, cazzaro, routeset or "route set". It lists other families only.
- known-knowns/: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns, 2026-11-06T00:21:55Z, 200. It has 27 entries and none concerns OptiWindNet or cable routing. The wind-related names in the repo are IEA37 layout entries, which are unrelated.
- Pull requests, open and closed: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100, 2026-11-06T00:21:55Z, 200. This page covers #851 to #957. Wind-related hits are only IEA37 layout claims and bank PRs (#900, #913, #938, #948, #953, #955, #958) and windmill-graph labelling claims (#894, #950). None is about OptiWindNet.
- Issues and PRs: https://api.github.com/repos/elder-plinius/V3R1T4S/issues?state=all&per_page=100, 2026-11-06T00:21:56Z, 200. This page covers #860 to #959, with no OptiWindNet hits.
- Full-history search (GitHub search API, issues and PRs, open and closed), each query run once at 2026-11-06T00:22:16-17Z, all HTTP 200:
  - `repo:elder-plinius/V3R1T4S optiwindnet`: total_count 0
  - `cazzaro`: 0
  - `cable routing`: 0
  - `routesets`: 0
  - `wes-2026-124`: 0
  - Control query `iea37` (00:22:23Z): 9 hits, so the search was working.
- bank/targets.json: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/HEAD/bank/targets.json, 2026-11-06T00:22:30Z, 200. Target `optiwindnet-routesets-cable-routing-records` exists, with status_checked 2026-10-30 and disclosure open. It records no prior result.

**Conclusion: no V3R1T4S trophy, known-known, PR or issue reports a result on this instance.**

## 4. Literature and code (base paper plus the last 24 months)

**Cazzaro and Pisinger, Networks 80 (2022) 386-406, doi 10.1002/net.22100**
- https://onlinelibrary.wiley.com/doi/full/10.1002/net.22100 (WebFetch): HTTP 403. Not read; no retry.
- Open-access PDF https://orbit.dtu.dk/files/302263821/Networks_2022_Cazzaro_Balanced_cable_routing_for_offshore_wind_farms_with_obstacles.pdf, 2026-11-06T00:24:33Z: HTTP 403, HTML returned. Not read; no retry.
- DTU Orbit record https://orbit.dtu.dk/en/publications/balanced-cable-routing-for-offshore-wind-farms-with-obstacles/ (WebFetch, read): abstract and metadata only, with no instance-G numbers.
- What I could establish about the paper's instance G-210 comes from OptiWindNet's documentation, below. A search-engine snippet of the paper also describes G as "210 turbines ... 30 root-branches", which implies capacity 7. I did not open that text myself, so this is not a cited value.
- **The paper's own instance is a different problem:** 3 substations (R=3), capacity 7, balanced constraints, and it is the original site rather than the `.solid` single-substation variant. Its numbers are not comparable to `.solid.1_OSS` at capacity 6.

**OptiWindNet docs v0.3.2**
- https://optiwindnet.readthedocs.io/v0.3.2/ (WebFetch): navigation, with no agent instructions.
- https://optiwindnet.readthedocs.io/v0.3.2/notebooks/p06_cazzaro_2022_g140_g210.html (WebFetch): reproduces Cazzaro G-210 at **κ = 7, balanced, radial MILP, feeders='min'** (Gurobi, 95 s). It reports objective 294123.1, bound 280249.41 and relgap 4.72%, and 2.40% shorter than the paper's route set. This is a different capacity, a different number of substations (3) and a different constraint set. **It is not comparable and is not a capacity-6 single-substation value.**
- https://optiwindnet.readthedocs.io/v0.3.2/notebooks/hi12_locations.html (WebFetch): table row `Cazzaro-2022G-210 | cazzaro_2022G210 | 3 | 210`, that is R=3 and T=210, which confirms the base site has 3 substations.
- https://optiwindnet.readthedocs.io/v0.3.2/dataset.html (WebFetch):
  - names release 26.05-v4 only, with no errata, leaderboard or best-known values;
  - defines `.solid` (removes obstacles) and `.1_OSS` (single substation);
  - says "Instances span 50-200 turbines". The release nevertheless contains this 210-turbine nodeset (and a 140-turbine one), a minor documentation inconsistency with no effect on novelty.

**OptiWindNet preprint wes-2026-124**
- https://wes.copernicus.org/preprints/wes-2026-124/ (WebFetch): received 14 Jul 2026, discussion open until 18 Nov 2026, with one referee comment. The landing page does not mention Cazzaro G-140/G-210 and gives no numbers for them. I did not open the PDF.

**OptiWindNet code on GitHub**
- https://api.github.com/repos/DTUWindEnergy/OptiWindNet, 2026-11-06T00:22:52Z, 200: pushed_at 2026-10-19.
- Releases: https://api.github.com/repos/DTUWindEnergy/OptiWindNet/releases?per_page=100, 00:22:52Z, 200. Releases v0.1.6 (2026-01-29) to v0.3.2 (2026-10-12). The only assets are the wheel and sdist. No route-set or benchmark assets, and no mention of Cazzaro or of improved route sets in the release notes.
- https://api.github.com/search/code?q=Cazzaro+repo:DTUWindEnergy/OptiWindNet, 00:22:53Z: HTTP 401 (code search needs authentication). Not retried.
- GitHub issues: https://api.github.com/repos/DTUWindEnergy/OptiWindNet/issues?state=all&per_page=100, 00:24:41Z, 200. Four closed issues, none relevant.

**OptiWindNet code on GitLab (primary repository)**
- https://gitlab.windenergy.dtu.dk/api/v4/projects/TOPFARM%2FOptiWindNet/issues?search=Cazzaro&scope=all&per_page=100, 00:24:40Z, 200: empty list.
- https://gitlab.windenergy.dtu.dk/api/v4/projects/TOPFARM%2FOptiWindNet/merge_requests?search=routeset&state=all&per_page=100, 00:24:40Z, 200: 16 MRs. Only !138 mentions Cazzaro, and that is the 50-turbine `cazzaro_2022` at κ=15, a bug repro. No route-set results for G-210.

**Framework paper: Souza de Alencar, Göçmen, Cutululis, "Flexible cable routing framework for wind farm collection system optimization", EJOR 329(3) (2026) 1037-1051, doi 10.1016/j.ejor.2025.07.069**
- Known only through search results; I did not open the full text.
- Its companion dataset is https://zenodo.org/api/records/18864643 (00:25:08Z, 200). I downloaded `paperdb.v3.sqlite.xz` once (00:25:15Z, 200, md5 d86c25efe3e34cc6b241107f0f6ef820, matching the record).
- That database has 14222 route sets and 6448 nodesets. Its only Cazzaro nodeset is `Cazzaro-2022` (T=50) and its only Cazzaro handle is `cazzaro_2022` (22 route sets). **There is no G-210 route set in it.**

**Thesis code archive (zenodo.org/api/records/20140812, 00:24:42Z, 200)**
- Files `optiwindnet_routesets.zip` and `data_driven_hybrid.zip`. The description lists them as analysis notebooks for 26.05-v4. I did not open the zips.

**Web searches (WebSearch)**
- Queries: Cazzaro and Pisinger instances; OptiWindNet RouteSets wes-2026-124; OptiWindNet docs Cazzaro-2022G-210; G-210 benchmark results 2025-2026; the EJOR DOI; "Cazzaro-2022G-210" capacity 6.
- None found a published total length or route set for Cazzaro G-210 `.solid.1_OSS` at capacity 6, radial or branched, outside the RouteSets release.

**Previous release 26.05-v4: not downloaded.** Per the 26.10-v4 changelog, its route-set identifiers are the same. Its lengths differ only by detour recreation: shorter detours by at most 0.13% in 26.10-v4, and a few radial sets changed by -0.016% to +0.053%. It therefore cannot hold a value near 396403.73 for this instance.

**Strongest known value for the instance (all sources checked): 399738.0433 m (RouteSets r26.10-v4 id 25278, branched); radial 401553.2842 m (id 25098).** No published value for this variant and capacity is lower.

## 5. Trivial-edit / seeding analysis

Method:
- Script: panel/work-novelty/scripts/compare.py.
- Stored route sets were rebuilt with optiwindnet 0.3.2 `G_from_routeset`.
- The claim's graph was rebuilt from claim/object/routeset-packed.json through the same function. I did not load G.pickle.

Integrity of the object as delivered:
- Rebuilt claim graph: length 396403.72691398446, with no length mismatch.
- Its 217 distinct geometric segments equal the 248 segments of claim/object/segments.json; repeated segments are parallel runs along detours.
- The Euclidean sum of segments.json is 396403.72691398446.
- 210 logical links, 36 at the substation.

| comparison | vs radial best 25098 | vs branched best 25278 |
|---|---|---|
| distinct geometric segments shared / differing (each side) | 141 shared, 76 differ | 142 shared, 75 vs 76 differ |
| logical links (detour chains collapsed) shared / differing | 144 shared, **66 differ** | 141 shared, **69 differ** |
| strings (turbine sets per feeder) identical | **8 of 36** | 8 of 36 |
| straight-line length of collapsed links (indicative) | claim 392601.41 vs 393059.00 | vs 393054.71 |

Findings:
- About 31-33% of the links differ, and 28 of 36 strings are re-partitioned.
- This is not a deletion, a restriction, a relabelling, a symmetry image, a propagation rule or a local numerical polish of either stored set.
- The set is not seeded from a stored object. It came from an independent HGS-CVRP run (seed 101, 240 s) per the claim, which is consistent with the large structural difference.
- Most of the gain comes from smaller detour overhead (claim detextra 0.43%, D=38 detour nodes), on a slightly shorter straight-line topology.

Provenance remark (not my lens): the claim says "seed 1 reproduces [id 25098] exactly", but the stored method options for 25098 record `seed: 20241113`. This may be a seed mapping in the wrapper. It does not affect novelty, since the object is compared by length.

## 6. Access log and injection

- Blocked, each tried once and not retried:
  - Wiley full text (403)
  - Orbit PDF (403)
  - GitHub code search (401, authentication required)
- No page instructed agents. `injection_suspected: none`. The Orbit footer contains a rights notice reserving text and data mining; that is not an instruction to agents.
- No outward actions were taken, and claim/ was not modified.

## Verdict

- The status source was read: r26.10-v4 is the latest.
- No V3R1T4S entry, release asset, repository issue or merge request, docs page or paper found here reports a route set or length for `Cazzaro-2022G-210.solid.1_OSS` at capacity 6 below 396403.7269 m.
- The published G-210 numbers (Cazzaro and Pisinger 2022; OptiWindNet p06) are for a different variant: 3 substations, κ = 7, balanced.
- The object is not a trivial edit of either stored set: 66 and 69 of 210 links differ.
- It strictly beats the stored radial best by 1.282% and the stored branched best by 0.834%, with the same feeder count (36).
- Residual caveat: the base paper's full text was blocked (403), so its tables were not read directly. Its instance has 3 substations and κ = 7, per the OptiWindNet docs, so it cannot hold a comparable value.
- Validity, containment and crossing checks belong to the other skeptics.

novelty: NEW (strictly beats every known value for this instance; not a trivial edit of a published object)

pass: true
