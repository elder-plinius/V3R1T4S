# Novelty review: Hornsea One.1_OSS, capacity 5, branched

context: subagent (Claude Code Agent tool, fresh context, saw only the claim folder and the public web)

## Claim under review
- Instance: nodeset `Hornsea One.1_OSS` (174 turbines, 1 substation, border with 25 vertices, no obstacles), capacity 5, topology X = branched. Release: OptiWindNet RouteSets r26.10-v4.
- Object: `object/segments.json` and `object/routeset-packed.json`, length 506483.6421 m, 35 feeders.
- Stated seed: stored radial set id 44834 (MILP.pyomo.cplex, 507652.1192 m, feeders [35]). It was improved by fix-and-optimise LNS with OR-Tools CP-SAT.

## Status source (fetched once, no retries)
- URL: https://zenodo.org/api/records/23537067/versions/latest
- Fetched 2026-11-07T09:06:24Z (UTC).
- Response: HTTP 301, body `{"status": 301, "message": "Redirecting...", "location": "https://zenodo.org/api/records/23537067"}`. The latest version therefore resolves to record 23537067 itself.
- I followed that single redirect at 2026-11-07T09:06:34Z: HTTP 200, id 23537067, DOI 10.5281/zenodo.23537067, publication_date 2026-10-21, single file `optiwindnet-routesets-r26.10-v4.sqlite.xz` (28464808 bytes, md5 85faffb2e13600b017f1b583b259edd7).
- Local reference `references/optiwindnet-routesets-r26.10-v4.sqlite.xz`: sha256 c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a and md5 85faffb2e13600b017f1b583b259edd7, which match the latest record.
- The concept's version list holds only 23537067 (r26.10-v4, 2026-10-21) and 20053479 (r26.05-v4, 2026-05-06). No newer release exists.

## Stored sets for the cell (r26.10-v4, nodeset `Hornsea One.1_OSS`, capacity 5)
| id | creator | topology | length (m) | feeders | MILP bound |
|---|---|---|---|---|---|
| 44834 | MILP.pyomo.cplex (warm start HGS) | radial | 507652.1192 | [35] | 495997.48 |
| 2798 | MILP.pyomo.cplex | branched | 507673.2764 | [35] | 497716.26 |
| 9633 | baselines.hgs | radial | 509207.2549 | [35] | - |
| 8921 | baselines.lkh | radial | 527587.2778 | [35] | - |

- Shortest stored set of any topology: 507652.1192 m (id 44834, feeders [35]). The object has 506483.6421 m with 35 feeders.
- The margin is 1168.4771 m (0.2302% relative), well above the 1e-6 threshold. This is not a tie.
- My recomputed length from `object/segments.json` (204 segments, Euclidean sum) is 506483.642108 m.
- Rebuilding G from `object/routeset-packed.json` with optiwindnet 0.3.2 gives the same length; `validate_routeset` returns []. Turbine-level checks: 174 turbines, 35 feeders, max turbine degree 3, largest feeder subtree 5. Containment was not re-checked here; it is the reproduction reviewer's job.

## Comparison with the seed and trivial edits
Turbine-level parent links (detour clones collapsed) were compared with every stored set of the instance.
- **vs seed 44834 (radial):** 151 of 174 links are shared and 27 turbines have a different parent. The symmetric difference is 46 links (23 removed, 23 added) in 7 connected groups (sizes 28, 4, 3, 3, 3, 2, 2). The object is branched (max degree 3); the seed is a path forest (max degree 2). 30 of 35 feeder turbines are shared.
- **vs 2798 (branched MILP):** 119 links shared, 56 turbines with a changed parent.
- **vs 9633 (HGS):** 146 links shared, 31 turbines with a changed parent.

These are multi-link reassignments plus new branching, not one of the listed trivial edits:
- Deletion, restriction and relabelling do not apply: the nodeset and coordinates are fixed, and all turbines must be served.
- Symmetry does not apply either: no symmetric image of a stored set exists for this geometry.

The one admissible local numerical polish is re-routing detours. I tested it by re-running optiwindnet PathFinder on the stored topologies, both with defaults and with iterations_limit=50000, traversals_limit=10:

| id | stored (m) | re-polished, own topology (m) | re-polished with branched re-hooking (m) |
|---|---|---|---|
| 44834 | 507652.1192 | 507652.1192 | 507652.1192 |
| 2798 | 507673.2764 | 507673.2764 | 507673.2764 |
| 9633 | 509207.2549 | 509207.2549 | 508431.3775 |

The best any of these edits alone gives is 507652.1192 m. The object beats that by 1168.48 m. The gain is in the topology: the straight-line objective is 502825.92 m (object) vs 503967.17 m (seed rebuilt), and detours are 3657.7 m vs 3685.0 m. The claim names its seed (44834), so the seeded-object condition is met.

## Neighbouring cells
- **Capacity 4:** best stored set 591151.3395 m (id 42471, feeders [45]). Capacity-4 sets are feasible at capacity 5 but are far longer and use more than 35 feeders.
- **Capacities 6-12:** these route sets break the capacity-5 limit, so they cannot be used here. The capacity-6 best is 450092.35 m.
- **`Hornsea One` (3 substations):** a different instance. Its capacity-5 set (id 67, 309816.26 m) cannot be turned into a 1-substation set by deletion or relabelling.
- **Augmented `!Hornsea One.1_OSS!...` nodesets:** turbine subsets (56-173 turbines), so they are not complete solutions of this instance.

## Earlier DTU datasets and other sources (last 24 months)
- **Zenodo 20053479 (RouteSets r26.05-v4):** the same 4 capacity-5 sets with identical lengths; best 507652.1192 m.
- **Zenodo 18864643 (paperdb.v3, 2025-03-28) and its newer version 19798734 (paperdb.v4):** I matched the nodeset by turbine geometry under a similarity transform, and by substation position. Both carry the same nodeset under the name `Hornsea One.1_OSS` (scale 1). The only capacity-5 sets are 2798 (507673.2764 m, branched MILP) and 9633 (508431.3775 m, HGS with branched detours). Neither is shorter than 507652.1192.
- **MILP_model_comparison v3/v4 in the same records:** no 174-turbine nodeset.
- **Zenodo 20140812 (thesis artifacts, 2026-05-12):** two zips of notebooks, scripts and ML models, with no route-set database. The notebooks analyse the r26.05 RouteSets data.
- **OptiWindNet:**
  - GitHub mirror DTUWindEnergy/OptiWindNet: releases v0.1.6 to v0.3.2, whose assets are only the wheel and sdist.
  - The repository tree holds no stored Hornsea One.1_OSS route sets. The notebooks mention only `Hornsea One` with 3 substations (capacity 7) and an Hornsea One.1_OSS capacity-8 count table.
  - The older repo mdealencar/interarray holds only the site YAML.
- **Preprint wes-2026-124:**
  - Posted 2026-07-28, discussion open until 2026-11-18, with one referee comment RC1 dated 2026-09-03.
  - The PDF text and the landing page give no Hornsea One / Hornsea One.1_OSS route-set lengths.
- **GitHub code search:** "Hornsea One.1_OSS" and "Hornsea_One_1_OSS" return no hits.
- **Web search:** no published Hornsea One single-substation capacity-5 cable-routing result.
- **V3R1T4S repo:**
  - At main 6bb0dcf (2026-11-06T20:24:57Z), TROPHY_CASE.md has no optiwindnet, cable or Hornsea entry.
  - Neither main nor the pinned commit f3b19b4 has a known-knowns/optiwindnet-routesets-cable-routing-records/ directory.
  - Of 924 PRs (open and closed) and 39 issues, the only items for this target are open PRs 962, 963, 964, 967 and 968. Their cells are:
    - 962: Cazzaro-2022G-210.solid.1_OSS cap 6
    - 963: Cazzaro-2022G-210.solid.1_OSS cap 7
    - 964: Yi-2019.1_OSS cap 11
    - 967: Hornsea One.1_OSS cap 10 branched
    - 968: Hornsea One.1_OSS cap 8 branched
  - Their INDEX.csv files list only those cells. None claims Hornsea One.1_OSS at capacity 5.

## Verdict
- The object is 506483.6421 m with 35 feeders, branched, and validator-clean.
- It strictly beats every known route set for Hornsea One.1_OSS at capacity 5, in r26.10-v4, r26.05-v4, paperdb v3/v4, the OptiWindNet repository and releases, the preprint, and the V3R1T4S repo and its PRs.
- The best known set is 507652.1192 m (id 44834); the object wins by 1168.4771 m (0.230%). This is not a tie.
- It is seeded from the named set 44834 and is not reachable by the trivial edits. Detour re-polishing of any stored set gives at best 507652.1192 m.
- The change is a 23-link reassignment with added branching.

novelty: PASS (strictly beats everything known; not a trivial edit of a published object)

pass: true
