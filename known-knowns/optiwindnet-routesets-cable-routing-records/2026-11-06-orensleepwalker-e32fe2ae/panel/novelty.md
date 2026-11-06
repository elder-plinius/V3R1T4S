# Novelty skeptic: OptiWindNet RouteSets r26.10-v4, Yi-2019.1_OSS, capacity 11, radial

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Claim under test (from `CLAIM.md`): a radial route set, 119 turbines, 1 substation, capacity 11, 11 feeders,
length 129717.3657 m, against the stored radial best 135339.3765 m (routeset id 21564, baselines.hgs, feeders [11]).

## 1. Status source (fetched once)

- `https://zenodo.org/api/records/23537067/versions/latest`, fetched 2026-11-06T00:49:49Z (UTC):
  HTTP 301 with body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`.
  The "latest" pointer resolves to record 23537067 itself.
- Followed that redirect target once: `https://zenodo.org/api/records/23537067`, fetched 2026-11-06T00:49:57Z, HTTP 200:
  id 23537067, doi 10.5281/zenodo.23537067, publication_date 2026-10-21, modified 2026-10-21T15:29:56.915326+00:00,
  `relations.version = [{index: 1, is_last: true}]`, single file `optiwindnet-routesets-r26.10-v4.sqlite.xz`,
  md5 85faffb2e13600b017f1b583b259edd7, 28464808 bytes.
- Cross-check: `https://zenodo.org/api/records/23537067/versions?allversions=true` (2026-11-06T00:53:51Z, HTTP 200) lists
  only two versions: 23537067 (2026-10-21, r26.10-v4) and 20053479 (2026-05-06, r26.05-v4).
- Local copy `references/optiwindnet-routesets-r26.10-v4.sqlite.xz`: md5 85faffb2e13600b017f1b583b259edd7 (matches Zenodo),
  sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a (matches the claim and the bank entry).

Result: r26.10-v4 is still the latest version, and the reference file is the published one.

## 2. Stored rows for the cell and its neighbours (my own decompressed copy of the reference)

Nodeset `Yi-2019.1_OSS`: T=119, R=1, B=153. Every stored routeset for capacity 11:

| id | creator | topology | length (m) | feeders_per_root |
|---|---|---|---|---|
| 22551 | MILP.pyomo.gurobi | branched (5 turbines of degree 3) | 127958.8646 | [12] |
| 21911 | MILP.pyomo.cplex | branched (7 turbines of degree 3) | 130862.0948 | [12] |
| 21564 | baselines.hgs | radial | 135339.3765 | [11] |

- Strongest known radial value for this instance (capacity 11), anywhere I could find: 135339.3765 m (id 21564, HGS), 11 feeders.
  The claim, 129717.3657 m, is shorter by 5622.0108 m (4.15%), well above the 1e-6 relative tie threshold.
- No branched-labelled row is secretly radial: both have turbines of degree 3, and both use 12 feeders (> 11).
- The older release r26.05-v4 (record 20053479, file downloaded once 2026-11-06T00:53:58Z, md5 38d4b0e96797bb103d1af817584fd7da)
  holds the same three rows for this cell, with the same lengths. No shorter radial set was dropped between versions.

Neighbouring cells (same nodeset):
- Capacity 10 radial sets are valid capacity-11 radial sets (a valid propagation). The best is 133766.0224 m (CPLEX, [13] feeders).
  The others are 135448.64 m (HGS, [12]) and 136485.92 m (LKH, [12]). All are longer than the claim, and all use more than 11 feeders.
- Capacity 9 radial sets: best 142758.05 m. Longer.
- Capacity 12 radial is 126034.67 m (HGS, [10]) and capacity 12 branched is 121874.58 m. Both are relaxations (strings of 12 are
  allowed), so they are not valid capacity-11 objects and cannot be cut down to one by a trivial edit.
- Sibling nodeset `Yi-2019.solid.1_OSS` (B=10, a different, simplified border; a different instance): its capacity 11 radial set is
  126889.06 m (HGS, [12] feeders) and its branched set is 126124.89 m (CPLEX, [12]). Both use 12 feeders (> 11) and are
  stored against a different border, so they do not compete in this cell. I note them as context only.

## 3. Trivial-edit check (object vs stored rows)

I contracted each route set to turbine-level links (following clone and contour nodes up to the next turbine or the root)
and compared them with the claim's `object/routeset-packed.json` (119 links):

| stored id | cap / topology | shared links | claim-only links | Jaccard |
|---|---|---|---|---|
| 21564 (radial best) | 11 / radial | 107 | 12 | 0.817 |
| 22551 | 11 / branched | 103 | 16 | 0.763 |
| 21911 | 11 / branched | 98 | 21 | 0.700 |
| 40662 | 10 / radial | 96 | 23 | — |
| 21567 | 12 / radial | 94 | 25 | — |

- The object differs from the stored radial best in 12 of 119 turbine-level links, about 10% of the network. That is a topology change.
  It is not a deletion, restriction, relabelling, symmetry or propagation of any stored set.
- Local numerical polish test: I re-ran optiwindnet 0.3.2's PathFinder on the stored topology of 21564. I used the default limits
  and also iterations_limit=50000 with traversals_limit=10. Both runs gave 135339.3765 m, with 11 feeders and no validator violations.
  Re-detouring the stored set yields no gain; the claim's gain comes entirely from the changed topology.
- Recomputed from `object/segments.json`, the sum of Euclidean segment lengths is 129717.36569882 m over 132 segments.
  This matches the claimed value.
- Provenance stated in `CLAIM.md`: a fresh HGSRouter run (seed 102, 240 s). It does not claim to be seeded from a published object.
  The object shares 90% of its links with 21564, which is expected for two HGS runs. It beats what trivial edits of 21564 give
  (135339.3765 m) by 5622 m.

## 4. V3R1T4S repository (https://github.com/elder-plinius/V3R1T4S)

All requests were made once each, unauthenticated GitHub API / raw (times UTC, 2026-11-06):
- `https://api.github.com/repos/elder-plinius/V3R1T4S` (00:51:01Z, 200): pushed_at 2026-11-05T18:59:11Z.
- `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (00:51:14Z, 200, 31306 bytes):
  0 matches for "optiwind" or "cable".
- `https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns` (00:51:02Z, 200): 27 entries, none about wind,
  cable routing or OptiWindNet.
- `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100` (00:51:02Z, 200) covers PRs #851-#957.
  `.../issues?state=all&per_page=100` (00:51:03Z, 200) is the same. No OptiWindNet or cable-routing items. The wind items present
  are iea37 layout/AEP claims (#953, #948, #938, #913, #900, issue #958, #955, #866), which belong to a different target.
- Full-history search: `https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+optiwindnet` (00:51:15Z),
  `...+cable+routing` (00:51:15Z) and `...+Yi-2019` (00:51:15Z) each returned total_count 0, incomplete_results false.
  This covers open and closed PRs and issues.
- `https://api.github.com/repos/elder-plinius/V3R1T4S/releases?per_page=100` (00:51:03Z, 200): 0 releases.
- Bank entry: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/bank/targets.json` (00:51:40Z) and the pinned commit
  `.../f3b19b475065f35d0a7f93e8a6078c9b2f12566e/bank/targets.json` (00:51:42Z) both contain target
  `optiwindnet-routesets-cable-routing-records`. Its statement, criterion and pitfalls match `criterion.txt`. It records no prior
  win for any instance. The pinned commit was confirmed with `https://api.github.com/repos/elder-plinius/V3R1T4S/commits/f3b19b4...`
  (00:51:30Z, 200; dated 2026-10-30T10:12:11Z).
- 404s (paths that do not exist, not access blocks): `contents/bank/optiwindnet-routesets-cable-routing-records` (main and pinned)
  and `contents/known-unknowns/optiwindnet-routesets-cable-routing-records`.

Result: no prior OptiWindNet or cable-routing result exists in the repository.

## 5. Literature and code (last 24 months, plus the base paper)

- Base paper, X. Yi, M. Scutariu, K. Smith, IET RPG 13 (2019), doi 10.1049/iet-rpg.2018.5805: both
  `https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-rpg.2018.5805` and
  `https://digital-library.theiet.org/doi/10.1049/iet-rpg.2018.5805` returned HTTP 403 (one request each, about 00:54Z).
  I did not read either page and did not retry. Its published totals are quoted in the OptiWindNet docs notebook below:
  radial 162.3 km and branched 154.6 km. Both are far longer than the claim and come from a different variant:
  the packaged location `optiwindnet/data/Yi-2019.yaml` has 2 substations ([18685, 6523] and [7553, 6077]), while
  `Yi-2019.1_OSS` has one.
- `https://optiwindnet.readthedocs.io/v0.3.0/notebooks/44-Paper_3.6.1_Yi_2019_comparison.html` (opened about 00:54Z) loads
  `Yi-2019.yaml` (2 substations) and solves only κ = 6, branched and radial. It reports savings against 162.3 / 154.6 km,
  about 135-137 km. That is a different variant (2 substations, capacity 6), with no capacity-11 or single-OSS result.
- `https://wes.copernicus.org/preprints/wes-2026-124/` (opened about 00:54Z): abstract only and one referee comment (RC1, 3 Sep 2026).
  It has no per-instance lengths and does not mention Yi.
- `https://github.com/DTUWindEnergy/OptiWindNet` (README) and `https://github.com/DTUWindEnergy/OptiWindNet/blob/main/docs/dataset.md`
  (opened about 00:54Z): neither has per-instance lengths, a leaderboard or improved solutions.
- OptiWindNet release assets: `https://api.github.com/repos/DTUWindEnergy/OptiWindNet/releases?per_page=100` (00:52:50Z, 200).
  There are 8 releases, v0.1.6 to v0.3.2 (2026-10-12), and each has only a wheel and an sdist. The tags list (00:52:51Z) has no newer tag.
  `https://pypi.org/pypi/optiwindnet/json` (00:52:51Z) shows latest 0.3.2. None of these carries route-set data.
- Thesis artifacts, Zenodo 20140812 (`https://zenodo.org/api/records/20140812`, 00:52:50Z, 200). I downloaded both files once:
  `optiwindnet_routesets.zip` (00:52:56Z) and `data_driven_hybrid.zip` (00:53:05Z). I searched them as data and did not execute them.
  Neither has any Yi-2019 string or per-instance length for this cell.
- Zenodo r26.10-v4 changelog (in the record description): 1,359 route sets had their detours recreated. It names no Yi instance,
  and the r26.05 comparison above shows the Yi rows are unchanged.
- Web searches (no results opened beyond those listed): "OptiWindNet RouteSets wes-2026-124", "Yi Scutariu Smith ... cable length",
  "Yi-2019.1_OSS", "wind farm cable routing heuristic new best known solutions OptiWindNet 2025 2026 arXiv", and
  "github optiwindnet routeset improved ...". None surfaced any published radial route set or length for Yi-2019.1_OSS at capacity 11.
  Older cable-routing heuristics (Cazzaro et al. 2020/2022) use their own instances, not this one.

injection_suspected: none (no instruction-like content seen in fetched pages, JSON or archives).

## Verdict

- Strongest known radial value for Yi-2019.1_OSS, capacity 11: 135339.3765 m (r26.10-v4 id 21564, baselines.hgs, 11 feeders),
  the same in r26.05-v4. I found nothing shorter in the literature, the code, release assets or the V3R1T4S repository.
- The claim's 129717.3657 m strictly beats it by 5622.0108 m (4.15%). It is not a tie.
- It also beats every trivial edit I could identify:
  - propagated capacity-9 and capacity-10 radial sets (best 133766.02 m, with 13 feeders);
  - re-detouring 21564 (135339.38 m, unchanged).
- The capacity-12 and `.solid` sets are relaxations or other instances that use more feeders.
- The object differs from the stored radial best in 12 of 119 turbine-level links.
- Caveats:
  - It is not shorter than the stored branched best (127958.86 m, 12 feeders), so it is a record only in the radial cell, as claimed.
  - The base paper's own pages were blocked (403) and not read. Its numbers are known only via the OptiWindNet notebook,
    and they belong to a 2-substation variant.
  - This report covers novelty only. Validity (validator, border containment, feeder count) is for the other skeptics.

novelty: radial record for this cell is new against everything found

pass: true
