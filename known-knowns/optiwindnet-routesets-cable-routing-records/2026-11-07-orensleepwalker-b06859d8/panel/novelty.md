# Independent novelty review: Hornsea One.1_OSS, capacity 6

context: fresh subagent

This review examined the immutable `claim-ho6` object and independently retrieved public sources. It did not use another panel's work, prior reviewer conclusions, or author search/checker code. Review execution began on 2026-11-07 around 10:18 UTC, was interrupted by a usage limit, and resumed at 13:38 UTC. Completion and resumed checks have their actual timestamps; the earlier primary-status response was reused, not backdated or fetched again.

**Verdict:** the explicit route set survives the bounded novelty challenges below. The supported result is a shorter feasible object for this one benchmark cell. This is neither worldwide novelty proof nor an optimality, solver, method, runtime, or search-yield claim.

## Object and fixed-table comparison

Own code decoded the stored parent arrays and clone coordinates, independently of the author's implementation. Summing all 201 physical segments, including contours and detours, gives **449188.82031142124 m**. The physical graph is a tree containing all 174 turbines and the single root; it has 30 root feeders and maximum feeder-subtree load 6. Its `VertexC` equals the database array exactly. Every segment is covered by the site's closed border, checked with a 1e-7 m numerical buffer; the site has no obstacles. There are zero proper transverse crossings. There are 45 positive-length collinear overlap pairs: these are shared clone corridors permitted by the benchmark, not a basis for rejection. Separately, `optiwindnet.validating.validate_routeset` on the supplied graph returned `[]`.

The r26.10-v4 archive SHA-256 is `c78c8f3c0543468a48c24d02a08a9a71f9b385389b1e82b6af6bd5bbfdd05e3a`; its MD5 `85faffb2e13600b017f1b583b259edd7` matches the freshly fetched primary metadata. All four capacity-6 records are:

| id | stored physical length, m | feeders | creator |
|---|---:|---:|---|
| 45811 | 450092.351727352 | 30 | MILP.pyomo.cplex |
| 2799 | 451220.99185956945 | 30 | MILP.pyomo.cplex |
| 9634 | 452600.50812744885 | 29 | baselines.hgs |
| 8922 | 464173.546237935 | 30 | baselines.lkh |

Thus the object improves the shortest stored result by **903.5314159307745 m**, or **0.2007435612854177%**, and satisfies the relative 1e-6 threshold, **450091.90163500025 m**. All 44 stored route sets on the matching geometry were also decoded and checked at actual capacity 6 and feeder limit 30, irrespective of their declared capacity. Exactly those four rows met both load and feeder constraints. Shorter rows at higher capacities therefore do not silently transfer into this cell. No straight-objective or MILP bound was used as a physical-length comparator.

## Earlier DTU artifacts, aliases, and public neighboring objects

Fresh public API metadata for Zenodo 18864643, 19798734 and thesis-artifact record 20140812 authenticated all six supplied legacy raw archives by their published MD5 checksums. The earlier downloads were used as public data, not trusted as independent metadata. Both paperdb versions contain the identical Hornsea single-root geometry, with eight rows at capacities 2–5; their minimum is **507673.2763563798 m**, id 2798, capacity 5. The model-comparison databases have no matching 174-turbine, one-root geometry.

Geometry matching examined every nodeset with T=174 and R=1 in these databases and both benchmark releases. It matched root-relative radial distances followed by the complete pairwise turbine-distance matrix, so translations, rotations, reflections and relabeling were included. The target's radial distances are distinct (minimum separation **0.12185676058470563 m**), avoiding ambiguous order within tolerance. Only `Hornsea One.1_OSS`, with digest `cc0b8615dad646d5f4cbc7b079e021b0120da295fb6e213ccd27b5129f26e7b0`, matched. Its border/root/turbine array is identical. This is a bounded check over retrieved datasets, not a claim about all possible aliases elsewhere.

The two thesis ZIPs contain notebooks, model artifacts and dataset accessors, rather than an additional route-set database. Their text references benchmark **20053479**. I freshly downloaded its public r26.05-v4 raw archive (MD5 `38d4b0e96797bb103d1af817584fd7da`, SHA-256 `2669af38133cbb650a9225f856259def18163cd9aee25afe8a014dfc6f9453d2`). On this geometry its four capacity-6 rows and minimum are exactly the four listed above; this closes the explicit thesis-linked earlier-release comparison.

The public V3R1T4S main-tree snapshot was not truncated and contained the open-problem page but no OptiWindNet known-known object. Its trophy file had no OptiWindNet/Hornsea/cable entry, and its releases endpoint returned an empty list. Qualified GitHub REST searches, with explicit `is:pull-request` and `is:issue`, across both open and closed states found five OptiWindNet PRs and zero issues. The PRs are 962, 963, 964, 967 and 968; all five were open. The first three concern different geometries. I independently downloaded actual `segments.json` objects from the immutable public heads of the two Hornsea PRs, without using their reviewer reports:

| public object | actual physical length, m | actual maximum feeder load | feeders |
|---|---:|---:|---:|
| [PR 967](https://github.com/elder-plinius/V3R1T4S/pull/967), head b9c576cdc2b6a0effa4a901afa59f92cd2368f4a | 332729.34431381547 | 10 | 18 |
| [PR 968](https://github.com/elder-plinius/V3R1T4S/pull/968), head 976f514a511bd46f6f1972795f520cb4b379ad7a | 377034.6924851112 | 8 | 22 |

Both are valid neighboring capacity cells, and both fail this cell's actual capacity-6 constraint unchanged. Their segment-file SHA-256 hashes are respectively `f292304bf4816358b3363e26ff182745e8383881f255c8684f8370ee3e745f4e` and `b9f6f7c2d9b31f747f7a1920abc5f56ae458bcd0ff9c6e64cb63157229f400da`.

## Cheap independent challenges

Seed 45811 is acknowledged prior work. My checker retained existing physical polylines, contracted electrical links through degree-two clones, and independently enumerated subtree reattachments to every root/turbine endpoint. It screened tree structure, actual capacity 6, feeder limit 30, border containment and proper crossings, allowing collinear corridors. Direct new links were charged their full length; all retained detours remained charged.

The best single replacement from the seed measured **449923.6311412617 m**. Best-improvement iteration accepted five replacements and reached **449352.63599459274 m**. From that endpoint, every pair of disjoint logical links was considered with both endpoint reconnections, subject to a strict improvement filter; 296 length-promising candidates were screened and none improved it. All 35 possible contiguous contour/detour shortcuts at that endpoint were screened without improvement. A separate check of all 36 such shortcuts on the original seed likewise found no improvement. The submitted object is **163.8156831715 m** shorter than the strongest of these cheap baselines.

These are explicitly bounded move families. The greedy endpoint is not a global lower bound. The two-link test does not enumerate arbitrary new endpoints unrelated to the two removed links, nor all coordinated rerouting of multiple cables. The result establishes superiority to the cheap edits actually tested, not the impossibility of another simple improvement.

## Recent literature and public code

Searches covered the last 24 months using `OptiWindNet`, `Hornsea`, `1_OSS`, cable-routing, benchmark and GitHub combinations. Primary relevant sources were the [2026 RouteSets preprint](https://wes.copernicus.org/preprints/wes-2026-124/), the [2026 framework article](https://doi.org/10.1016/j.ejor.2025.07.069), and the October 2026 [multi-stage inter-array cabling paper](https://wes.copernicus.org/articles/11/3887/2026/). The latter's Hornsea I case has three substations, so its length is not a same-cell comparator; its separate routing benchmark's public `parks_torque.zip` was downloaded and indexed and contains HornSeaTwo, not the 174-turbine Hornsea One single-root cell. The code-and-data metadata at Zenodo 18846347 and 18937430 was inspected. The 93 MB WES results archive was not downloaded; no claim is made that every object in every literature archive was exhaustively searched.

The OptiWindNet GitHub release list was inspected, including release assets. The current v0.3.2 wheel was independently downloaded and indexed: it has source and location data, including Hornsea One YAML, but no SQLite route database or candidate route-set archive. No duplicate or better feasible same-cell published object was identified in these bounded primary-source checks. Existing frameworks and local optimization ideas already supply method precedent; this review assigns no method novelty.

## Status provenance and limitations

The required primary latest endpoint was fetched exactly once using the honest `V3R1T4S` user agent: `https://zenodo.org/api/records/23537067/versions/latest`. The saved transport headers show **HTTP 301 → HTTP 200**, final URL `https://zenodo.org/api/records/23537067`, server UTC **2026-11-07 10:18:41**. The body SHA-256 is `a1eb5479cd7a9ccde50311ad180aa7451d9ddefe70c23f253759299713637bad`; it names record 23537067 and archive r26.10-v4, updated 2026-10-21T15:29:56.915326+00:00. There was no 401/403/429/503 or challenge, and no retry. The interruption does not turn that response into a later status observation.

Own scratch code and downloaded evidence reside in `panel-ho6/work-novelty/` for this review and are **NOT INCLUDED in the claim package**. Reproducible numeric summaries are `check-result.json`, `legacy-result.json`, `final-checks.json`, `two-result.json` and `seed-shortcut-result.json` there. No external write or publication was performed. The claim folder was not modified.

The verdict concerns bounded evidence of a new explicit record against the fixed current release and the inspected prior objects. It cannot certify worldwide absence of an unindexed, private, or unexamined competing object. There is no global optimality assertion.

## Primary retrieval ledger

All entries below saved raw response bodies. UTC is request initiation; each response was HTTP 200 unless its saved redirect metadata says otherwise. SHA-256 hashes apply to raw bodies.

- 2026-11-07T10:19:16.594659+00:00 — https://zenodo.org/api/records/18864643 — HTTP 200, 5778 bytes — SHA-256 `c163c5591d8a7c9462ea61f95514853c422a290ff85ae2155a14c8a42cfb0173`.
- 2026-11-07T10:19:16.914198+00:00 — https://zenodo.org/api/records/19798734 — HTTP 200, 5920 bytes — SHA-256 `cd37e1b4752cd3cbc22363bbeb389e1173bed114ca799d306c0de2c330fc0435`.
- 2026-11-07T10:19:17.210603+00:00 — https://zenodo.org/api/records/20140812 — HTTP 200, 14830 bytes — SHA-256 `3487456ee2cb7635bea3a06d1a4640202384c9090b8c583e3e7844f068868a7a`.
- 2026-11-07T10:19:17.611723+00:00 — https://zenodo.org/api/records/20053479 — HTTP 200, 9907 bytes — SHA-256 `3b80d1680d8780bbae460e50e58f0260e9d8c25b309728b80cff2bdec8ad57d4`.
- 2026-11-07T10:19:17.948896+00:00 — https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md — HTTP 200, 31306 bytes — SHA-256 `83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113`.
- 2026-11-07T10:19:18.368341+00:00 — https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 — HTTP 200, 2126996 bytes — SHA-256 `ab3762505fcd8d9eb713be8a84b75e848b2889076ba305aee8f30cd5eae27880`.
- 2026-11-07T10:19:18.879060+00:00 — https://api.github.com/repos/elder-plinius/V3R1T4S/releases — HTTP 200, 2 bytes — SHA-256 `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
- 2026-11-07T13:38:55.019229+00:00 — https://zenodo.org/api/records/20053479/files/optiwindnet-routesets-r26.05-v4.sqlite.xz/content — HTTP 200, 28493876 bytes — SHA-256 `2669af38133cbb650a9225f856259def18163cd9aee25afe8a014dfc6f9453d2`.
- 2026-11-07T13:39:15.462309+00:00 — https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/967 — HTTP 200, 18308 bytes — SHA-256 `965cdac47c36de040b9417ad1247312962023ea82666a5866575bd2246135184`.
- 2026-11-07T13:39:19.445646+00:00 — https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/968 — HTTP 200, 18352 bytes — SHA-256 `478615939699ae666564743bf5a9f729def1b551fddd04a9cbdd1001004306c6`.
- 2026-11-07T13:40:32.428238+00:00 — https://api.github.com/search/issues?q=repo%3Aelder-plinius%2FV3R1T4S%20optiwindnet%20is%3Apull-request&per_page=100 — HTTP 200, 21034 bytes — SHA-256 `8a730c17043815bf417766f9b2056e0a1db25cd4fe613d483cf289b65f37f091`.
- 2026-11-07T13:40:33.030078+00:00 — https://api.github.com/search/issues?q=repo%3Aelder-plinius%2FV3R1T4S%20optiwindnet%20is%3Aissue&per_page=100 — HTTP 200, 79 bytes — SHA-256 `c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0`.
- 2026-11-07T13:40:33.634295+00:00 — https://api.github.com/repos/DTUWindEnergy/OptiWindNet/releases — HTTP 200, 75886 bytes — SHA-256 `e1b4a2eb105d8a41e6b96495f8e234e0109438d9e6302edebc2b7072b7f667ff`.
- 2026-11-07T13:40:33.975265+00:00 — https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/967/files?per_page=100 — HTTP 200, 161971 bytes — SHA-256 `3109a969a08ff7375b9966ef066d308e390361b85dadb3929cef754ee66369fd`.
- 2026-11-07T13:40:34.696112+00:00 — https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/968/files?per_page=100 — HTTP 200, 161151 bytes — SHA-256 `0fd35eb6bfa2d86d62240473483e537e9429fc4802dd43d9f363a8c631b45a6b`.
- 2026-11-07T13:40:35.100418+00:00 — https://wes.copernicus.org/articles/11/3887/2026/ — HTTP 200, 489115 bytes — SHA-256 `4aa9283aed781760470e20126578679f251f2dbd38532f99ae4af545d9746596`.
- 2026-11-07T13:41:25.786733+00:00 — https://raw.githubusercontent.com/OrenSleepwalker/V3R1T4S/b9c576cdc2b6a0effa4a901afa59f92cd2368f4a/known-knowns/optiwindnet-routesets-cable-routing-records/2026-11-06-orensleepwalker-f292304b/object/segments.json — HTTP 200, 28158 bytes — SHA-256 `f292304bf4816358b3363e26ff182745e8383881f255c8684f8370ee3e745f4e`.
- 2026-11-07T13:41:26.197890+00:00 — https://raw.githubusercontent.com/OrenSleepwalker/V3R1T4S/976f514a511bd46f6f1972795f520cb4b379ad7a/known-knowns/optiwindnet-routesets-cable-routing-records/2026-11-06-orensleepwalker-b9f6f7c2/object/segments.json — HTTP 200, 29413 bytes — SHA-256 `b9f6f7c2d9b31f747f7a1920abc5f56ae458bcd0ff9c6e64cb63157229f400da`.
- 2026-11-07T13:42:03.276966+00:00 — https://zenodo.org/api/records/18846347 — HTTP 200, 4582 bytes — SHA-256 `f2c87e34bd8eebb27a877eec3e4902e19dabead00143af902e9f3140b884e2eb`.
- 2026-11-07T13:42:03.623403+00:00 — https://zenodo.org/api/records/18937430 — HTTP 200, 6232 bytes — SHA-256 `3e12b55af436f0d05b6222a0ed167a0102a3487782e48cfdee82b903df540995`.
- 2026-11-07T13:42:30.645677+00:00 — https://zenodo.org/api/records/18846347/files/parks_torque.zip/content — HTTP 200, 9743000 bytes — SHA-256 `7ab06f50b992ce54a4b07cd6598455c72fbe4d5439d4cedb982d2956b8e3bf1a`.
- 2026-11-07T13:42:35.161722+00:00 — https://github.com/DTUWindEnergy/OptiWindNet/releases/download/v0.3.2/optiwindnet-0.3.2-py3-none-any.whl — HTTP 200, 615034 bytes — SHA-256 `f1838e8342f5863d1a86c65769004c3dee9299df744ea75f511676cb754012e7`.

Report completed UTC: 2026-11-07T13:44:59.649222+00:00

pass: true
