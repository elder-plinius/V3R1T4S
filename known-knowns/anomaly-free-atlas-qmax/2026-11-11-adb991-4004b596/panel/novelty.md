# Novelty skeptic: SM-only anomaly-free U(1) census, Q_max 41 and 42

Claim under review: SM-only (no nu_R) census in the Allanach-Davighi-Melville (ADM) convention, |F| <= 41: 66526761,
|F| <= 42: 79174540. Question: is this cell already covered by published or posted work, or trivially derivable from it?

Every request below used User-Agent "V3R1T4S-research-bot". Raw bytes and the full request log (44 requests: UTC
time, attempt, HTTP code, sha256, URL) are in panel_work/novelty/raw/ and panel_work/novelty/log.tsv.

## Sources

| URL | fetched (UTC) | HTTP | sha256 | what it says |
|---|---|---|---|---|
| https://arxiv.org/abs/1812.04602 | 2026-11-11T09:46:56Z | 200 | e0d5ff800478a38c38113f8b7e251180ad36d8daf14379cdd7c0f401420490e0 | Versions v1 (2018-12-11) .. v5 (2020-01-08); no v6. Byte-identical to the run scout's 09:19:08Z fetch (status.md). The v5 text in source/atlas states the lists cover "Qmax ≤ 10 in the SM and Qmax ≤ 10 in the SMνR"; Table 2 ends at SM Q_max 10 = 23800. |
| https://zenodo.org/api/records/3345889 | 2026-11-11T09:48:45Z | 200 | 040fb4490a241d77cd248ee178f46637d687746b5ba30eb42363ddbc54880435 | The atlas dataset (v1.1.0, 2018-12-12): files SMcharges0..SMcharges10, SMnuRcharges0..10, searchU1.cpp. Nothing past Q_max 10. |
| https://zenodo.org/api/records/3345889/versions?size=25 | 2026-11-11T09:48:48Z | 200 | 5ec79b498ecec36b4fe00ac3d0e47e9526655153ed443cd159b255bc50a907d0 | Two versions only (1.0.0, 1.1.0, both 2018-12-12); no later extension. |
| https://zenodo.org/api/records?q=%22anomaly-free%20atlas%22&size=25&sort=mostrecent | 2026-11-11T09:48:51Z | 200 | 3b196867c31fb7a767935a39ca668f5514b2706c2a413d46083a49e8ad5d03c5 | 1 hit: record 5062067, the nu-supersymmetric atlas (MSSM content, Q_max 10); different field content. |
| https://zenodo.org/api/records?q=66526761&size=25 / ?q=79174540&size=25 | 09:48:57Z / 09:48:59Z | 200 / 200 | 04b30b20235cd314d1ca8a45b4a7cba7e110dff3bd8e5c841f56991770cbe3a8 / 4283856b13ac19148306885b5bdc06d1df1c9ed4bd18f3e9575f74c9c501d2c1 | 0 hits each. |
| https://inspirehep.net/api/literature/1708575 | 2026-11-11T09:48:00Z | 200 | d3a92c0fedd06a829d61323737e4735ff2aa0d4cb8da4ea02777ae0f2fd77f7b | The atlas record, 121 citations. |
| https://inspirehep.net/api/literature?q=refersto:recid:1708575&size=250&sort=mostrecent | 2026-11-11T09:48:03Z | 200 | c45440cee149d1aa10a3107519726c6d372492fa6e3fd91d93bb69df5aa621a7 | All 121 citing records (newest 2026-10-19). Titles screened; candidates checked below. None extends the census. |
| https://inspirehep.net/api/literature?q=fulltext:%2221546920%22 (positive control) | 2026-11-11T09:48:22Z | 200 | b918d049f41a74f88cc63180566410a4672c52be8e5a4604db893d9ece9772e8 | 2 hits: the atlas (1812.04602) and a 2020 thesis (recid 1776324). The control works. Second control fulltext:"9587085": the same 2 hits (91778e568eb7957271f0d7ca01db41dcaee6f0affa6c2b51ed29bd14a0d58fc8). |
| https://inspirehep.net/api/literature?q=fulltext:%2266526761%22 | 2026-11-11T09:48:27Z | 200 | fef70f7b12c5ce20765194cc2a8a73a44f098c6db1f94e8086bd22a2f58dc4f0 | 0 hits. |
| https://inspirehep.net/api/literature?q=fulltext:%2279174540%22 | 2026-11-11T09:48:30Z | 200 | ee5b889c87a41ab12b09798890c1114e974f7b6ac069a77d3d7bd219079c3bce | 0 hits. |
| export.arxiv.org API, 8 queries plus 2 id_list lookups (see Searches) | 09:47:11Z-09:52:04Z | all 200 | e.g. q1 eb3ab3969048b01989cd4c08d7a9017950b51f9fb4de6aa0e362c6ffbbe7a447, q8 27cc7be252d5cf069c38da7e9539be667206a53e6049c35c77400b15858d2244 | No paper extends the SM census past Q_max 10 (details below). |
| https://api.github.com/search/code?q=%22anomaly-free+atlas%22 (text positive control) | 2026-11-11T09:51:04Z | 200 | d658c49cb33d23e703d7330c4c0d107fdeb3aca3a322c0476ec4e27d971b2293 | 19 hits, all bibliographies, CVs and metadata that cite the paper. Code search is reachable and works. |
| https://api.github.com/search/code?q=66526761 / ?q=79174540 | 09:49:28Z / 09:50:05Z | 200 / 200 | 0ef36ec16fdba9af1e06a2e6528b492d1d128aaa7085173037991031c02b2df8 / 79e1bfab28f2eb4af81f7c6f00d981f924f2ebe896022c4eb399da863f1fedd1 | 3061 and 95 hits. The pages read are unrelated numeric data files (CFD, point clouds, EoS tables, pi digits). Narrowed with "+anomaly": 8 and 4 hits, all unrelated (time-series anomaly detection CSVs and similar). |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:pr+anomaly&per_page=50 | 2026-11-11T09:51:09Z | 200 | 3f1293b3572dd3afb35a3df05603e4c4811d762442efe13645fd9eafb2b6c3d4 | The only census PRs are #989-#993 (this contributor's own, all open): Q_max 11 for both contents; SMnuR 12-20; SM 12-38. None covers SM 41 or 42, and no other contributor posted census rows. |

## Searches and findings

arXiv API (export.arxiv.org, sorted by submittedDate, newest first):
- all:"anomaly-free atlas": 2 results, the atlas and 2107.07926 (nu-supersymmetric atlas: MSSM plus up to 3 singlet superfields, Q_max <= 10). The second has different field content and the same range.
- abs: anomaly AND "family dependent" AND U(1): 17 results, all phenomenology or model building. No census.
- abs: "anomaly free" AND "integer charges": 1 result, 2107.07518 (phenomenology).
- abs: anomaly AND charges AND (enumerat* OR census OR classification OR scan) AND U(1): 47 results. None is an SM U(1) census.
- (au:Allanach OR au:Davighi) AND abs:anomaly: 49 results, newest 2026-09. These are general solutions (1912.04804, 1912.10022, 2006.03588) and phenomenology. No new counts.
- abs: "anomaly equations"/"anomaly cancellation conditions" AND U(1): 344 results (first 50 read). The recent arithmetic-geometry papers 2508.11583 ("Anomaly cancellation for a U(1) factor"), 2607.09879 ("... two U(1) factors") and 2610.26092 (degree-3 Prouhet-Tarry-Escott) were checked through their abstracts. They give parametrisations, not bounded counts.
- abs: "anomaly-free" AND "Standard Model" AND U(1) AND (solutions OR atlas OR charges): 248 results (first 50 read). No census.
- abs: anomaly AND (Qmax OR "maximum charge" OR "maximum absolute charge"): 4 results, the atlas, the nu-supersymmetric atlas, and 2206.11271 "Flatland". Flatland uses the atlas range (max charge ratio ±10).

INSPIRE: all 121 citers of recid 1708575 were screened. The closest ones were checked through their abstracts: 2206.09956 (Ising-machine annealing, which finds solutions but is not exhaustive), 2205.03428 (integer solutions for a different class of theories), 2007.08733, 2001.11991, 2408.15536, and the theses with recids 1877905, 3112315 and 3198853. None tabulates SM counts past Q_max 10. A title search (t "anomaly-free" and (t atlas or t "charge assignments")) returned only the two atlases. A full-text search for either claimed number returns 0 hits, while the positive controls on published values (21546920, 9587085) return the atlas.

Zenodo: the atlas dataset stops at SMcharges10, and its only versions date from 2018. Searches for "anomaly-free atlas", for each claimed number, and for title:anomaly AND title:"charge assignments" found nothing past Q_max 10. Limitation: the two number searches have no numeric positive control, because Zenodo indexes metadata, not file contents, and a "1812.04602" query also returned 0.

GitHub: the repository search control (V3R1T4S) works. Repository searches for "anomaly-free atlas" and "anomaly U(1) charges" return 0, and an in:readme,description search returns unrelated hits. Code-search results for the two numbers are unrelated (see the table). Limitation: no numeric positive control exists for code search. "21546920 anomaly" did not find the atlas files, which are not on GitHub. The text control does work.

Trivial derivability: no.
- The paper's own growth fit for the SM, 1 + a exp(bQ + cQ^2) - a with a=2.50, b=1.34, c=-0.043, gives about -1.5 at Q_max 41 and 42 (it peaks near Q ~ 15.6). It cannot produce or approximate these counts.
- The published program (searchU1.cpp) could in principle be rerun, and the paper invites this. Its fitted SM runtime, exp(-9.45 + 1.38Q - 0.014Q^2) s, extrapolates to about 1.8e10 s at Q_max 41 and 2.2e10 s at Q_max 42, roughly 560-700 years. That is a far extrapolation, but it shows the rows were not one cheap rerun away.
- No published recurrence or closed form gives bounded counts in this convention. The later general solutions (2006.03588, 1912.04804, 2508.11583) parametrise solutions and do not count them under a bound.

V3R1T4S checkout: TROPHY_CASE.md, known-knowns/ and known-unknowns/ contain no entry for this census. A grep of the whole checkout for "anomaly-free", "Allanach", "Davighi", "1812.04602", 66526761 and 79174540 finds nothing relevant. Nothing there lists SM 41 or 42. The workspace's earlier rows (SM <= 40, SMnuR <= 20, partly posted as draft PRs #989-#993) are the same contributor's work, so they are not prior art. In any case, the posted PRs stop at SM 38.

Protocol note: the URL https://api.github.com/search/code?q=79174540&per_page=100 got 3 requests instead of the allowed 2: one 408, then a manual re-request that got 503 and was auto-retried to 200. All three are in log.tsv. That URL only produced irrelevant numeric-file hits (302 total, first 100 read) and does not affect the verdict.

## Best published object for this cell

ADM atlas, arXiv:1812.04602 v5, JHEP 02 (2019) 082 plus erratum JHEP 08 (2019) 064, and Zenodo 10.5281/zenodo.3345889 v1.1.0. SM-only counts are published for Q_max <= 10, the last being Q_max 10 = 23800 (Table 2). No published or posted SM count exists for Q_max 11..42 from anyone other than this workspace's contributor, and none at all for 41 and 42.

## Verdict

Novel. No published or posted work covers SM-only Q_max 41 or 42 in the ADM convention, or in any other convention found. The values cannot be derived from published values, fits or general solutions without a fresh exhaustive computation. Within novelty, the claim extends the census past the published range, as the charter quarry requires. Correctness of the numbers is for the other skeptics.

context: subagent (fresh context, Claude Code Agent tool)

pass: true
