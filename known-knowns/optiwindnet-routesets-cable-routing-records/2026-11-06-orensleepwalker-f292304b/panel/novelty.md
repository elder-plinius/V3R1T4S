# Novelty review: claim-ho10 (Hornsea One.1_OSS, capacity 10, branched)

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

Claimed object: a branched route set of 332729.3443 m with 18 feeders, seeded from stored routeset id 45802 (radial, MILP.pyomo.cplex, 336086.4654 m, feeders [18]).

## 1. Status source (fetched once, no retries)
- URL: https://zenodo.org/api/records/23537067/versions/latest
- HTTP: 200. Redirected to https://zenodo.org/api/records/23537067
- Fetched 2026-11-06T16:06:46Z to 16:06:47Z UTC
- Latest record id: 23537067 (concept 20053478), DOI 10.5281/zenodo.23537067, publication_date 2026-10-21, created 2026-10-21T15:29:56Z
- Single file: optiwindnet-routesets-r26.10-v4.sqlite.xz, 28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7
- The claim's references/optiwindnet-routesets-r26.10-v4.sqlite.xz has the same md5 and the claimed sha256 c78c8f3c...e3a. It matches status/zenodo-latest.json (same id and date). No newer version exists.
- Zenodo lists two versions in total: 23537067 (r26.10-v4) and 20053479 (r26.05-v4, 2026-05-06).

## 2. Stored sets for this cell (reference DB, nodeset 'Hornsea One.1_OSS', T=174, R=1, B=25, capacity 10)
| id | length (m) | feeders | topology | method |
|---|---|---|---|---|
| 45802 | 336086.4654 | [18] | radial | MILP.pyomo.cplex (min_plus1, 6 h, warm-started from 9644; bound 322681.89) |
| 9644 | 340159.1949 | [18] | radial | HGS-CVRP |
| 2804 | 342349.2849 | [19] | branched | MILP.pyomo.cplex (unlimited feeders; bound 322779.29) |
| 8928 | 350931.2830 | [18] | radial | LKH-3 |

The best stored set is 336086.4654 m with feeders [18]. The claimed object is 332729.3443 m with 18 feeders. That is 3357.1211 m (0.9989%) shorter, far above the 1e-6 relative threshold. I recomputed the length as the sum of Euclidean lengths over the 180 segments in object/segments.json, and it matches. The object stays above the best stored branched bound (322779.29), so the claim is consistent with the release's bounds.

The prior release r26.05-v4, which I downloaded from Zenodo, holds the identical four sets for this instance (same ids and lengths). The nodeset digest is the same in both releases.

## 3. Neighbouring cells and trivial edits
- **Lower capacities (2 to 9):** a set with smaller capacity is also valid at capacity 10 (a valid propagation rule). The shortest stored capacity-9 set is 353604.67 m with [20] feeders. It is longer than the object and also breaks the 18-feeder cap.
- **Higher capacities (11, 12):** the shortest stored sets are 319646.12 m ([16]) and 309220.71 m ([15]). Neither can be restricted to capacity 10: with at most 17 feeders, 174 turbines force some subtree above 10 (174/17 > 10). Turning one into a valid capacity-10 set needs a real re-optimisation, not a deletion or restriction.
- **The 3-substation 'Hornsea One' nodeset:** this is a different instance (different substations), so it is not comparable.
- **Edit distance from the seed (45802):** I compared links after resolving clones to their prime nodes. The object shares 149 of 174 links with 45802 and replaces 25 of them, about 14%. The replaced links lie in several regions: 3 feeders changed, plus about 22 inter-turbine links. The object also introduces degree-3 branching, which a radial set does not have.
- **Distance from the other stored sets:** 153 shared links with 9644, 114 with 2804, 108 with 8928.
- **Why no trivial edit reaches the object:** deletion, restriction, relabelling and symmetry cannot change the link structure. Turbine positions are fixed, so there is nothing to polish numerically. Re-running PathFinder on 45802 keeps its links. So no trivial edit of a published set yields this object. The provenance in CLAIM.md (an LNS with CP-SAT sub-solves) is consistent with what I see: a combinatorial change of 25 links worth 3.36 km.

## 4. Sanity checks (supporting, not my main role)
- The object is a spanning forest: 174 prime links covering all 174 turbines, 18 feeders, largest subtree 10, so it fits capacity 10.
- object/G.pickle carries VertexC identical to the stored nodeset blob (200x2, max difference 0.0).
- optiwindnet 0.3.2 validate_routeset(G) returned [], and G's total length is 332729.34431381547.
- I did not check border or obstacle containment. That is left to the other panelists.

## 5. Literature, code and repo search (last 24 months)
- **V3R1T4S repo (elder-plinius/V3R1T4S, via the GitHub API, 2026-11-06):**
  - TROPHY_CASE.md (main) has no entry mentioning optiwindnet, Hornsea, routeset or cable.
  - known-knowns/ has no optiwindnet-routesets-cable-routing-records folder, either on main or at the pinned commit f3b19b4 (404 or absent from the listing). The only repo file for this target is known-unknowns/optimization-benchmarks/optiwindnet-routesets-cable-routing-records.md. It names Hornsea One.1_OSS only for capacity 8 and says "Shorter route sets on these instances are open."
  - A search of issues and PRs for "Hornsea" returned 0. A search for "optiwindnet" returned 3 open claim PRs (#962, #963, #964), all for other instances (Cazzaro-2022G-210.solid.1_OSS capacities 6 and 7, Yi-2019.1_OSS capacity 11). None covers this instance.
- **OptiWindNet code (GitHub DTUWindEnergy/OptiWindNet):**
  - Release assets v0.1.6 to v0.3.2 (latest 2026-10-12) are only the wheel and sdist, with no route-set data.
  - The repo tree contains Hornsea One.yaml (the layout only). The docs notebook lo21_hgs runs HGS on the 3-substation Hornsea One at capacity 7 (282390 m), which is a different instance.
  - The p03 notebook reports no Hornsea One.1_OSS capacity-10 set.
- **wes-2026-124 preprint page:** no Hornsea numbers. Its data and code links point to Zenodo 20053479 (checked above) and 20140812. In the 20140812 thesis artifacts, optiwindnet_routesets.zip contains analysis notebooks and figures only, with no Hornsea One route sets.
- **Web searches** (Hornsea One cable routing, MILP, collection system, 2025-2026): no published inter-array route set for this exact single-substation variant ('.1_OSS' is an OptiWindNet-derived instance), and no length below 332729.34 m.

## Verdict
- The status source is reachable and confirms r26.10-v4 (record 23537067) is still the latest.
- The object is strictly shorter than every stored set for this cell of any topology, by 3357.12 m (0.999%). It respects the feeder cap of 18. It is not reachable by trivial edits of any published object in this cell or the neighbouring cells.
- It names its seed (45802) and beats it, and everything derivable from it, by a substantive combinatorial change.
- I found no shorter published set in the literature, code, releases, the repo's TROPHY_CASE.md, known-knowns/, or its PRs and issues.
- It is not a tie. Novelty is confirmed.

novelty: NEW (strictly beats all known; 332729.3443 m < 336086.4654 m)
pass: true
