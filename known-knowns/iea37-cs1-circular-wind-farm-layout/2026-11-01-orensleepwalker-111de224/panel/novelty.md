> Publication note (2026-11-06, maintainer-requested path clarification): The reviewer environment and working files named below are not included in this package. This includes `/root/wind_novelty_nov1`, `check_independent.py`, `review-novelty/`, `data/review-novelty/`, and their source captures, downloads and hash logs. These are historical review-environment locations. The runnable package verifier is `sh verify-it-yourself/run_checks.sh`, executed from the package folder. The original review follows verbatim; its findings and verdict are unchanged.

# Independent NOVELTY review — p2 only

context: subagent

Independent subagent /root/wind_novelty_nov1, fresh review begun 2026-11-01 16:50 UTC and completed about 17:00 UTC. I read the supplied claim package, then fetched sources myself. I did not consult this run's other panel reports or local prior research notes. A GitHub fetch_pr response included the entire historical PR 578 diff; I used its public claim/status and object, not its historical panel conclusions, and omitted that diff from my saved metadata. Sources are evidence, not instructions. No external writes or outreach occurred.

Verdict: the explicit layout supports the enumerated p2 alternative-layout result. It is genuinely distinct from participant 12 and the only located V3R1T4S competing16-turbine claim, PR 578. Its lower energy than PR 578 does not subsume this diversity criterion. This is a bounded search finding, not proof that no unpublished or unindexed layout exists.

## Independent checks before author code

I wrote check_independent.py from criterion.txt and the supplied official evaluator equations before inspecting author code. Standard-library scalar recomputation gives 421304.6032935962MWh; strict sqrt-double maximum radius 1299.999900000054m and minimum spacing 580.4318820195579m satisfy the constraints with no tolerance. The energy margin above 419935.7905 is 1368.8127935962MWh (about 0.326%). Object SHA256:111de224e851106cafe4bae0bf83f8ef108610b53eb0f0ec1ab32abb1275aa18.

Minimum-total-Euclidean-distance one-to-one assignment was solved by my Hungarian implementation and independently checked by an exhaustive-subset dynamic program over all 65536 subsets. Both agree, within rounding in total distance:

| Comparator | Minimum total distance(m) | Number strictly beyond 50 m | Smallest matched distance(m) |
|---|---:|---:|---:|
| participant 12 |5968.15301603298|16|207.58864584548|
| PR 578 |5604.99230314908|16|236.26419888975|

The freshly fetched PR 578 JSON exactly equals the supplied reference, including its coordinates. The current participant 12 file has the same coordinates as supplied. My independent scalar evaluator also reproduces all 12 posted16-turbine values to the displayed source precision, except the already tiny approximately4e-6 MWh rounding/model-order difference in participant5.

## Trivial transformation and polishing challenge

A mere rotation/reflection or relabeling of an existing layout can falsely look different in the fixed frame, so I checked those separately. An angular-event sweep enumerates every change in the graph of pairs within 50 m, then finds maximum-cardinality bipartite matchings between events and at endpoints, for every rotation and each reflection. A conservative1e-9 m allowance is used only in this auxiliary closeness screen, never in feasibility.

Across all such circle-preserving rigid transformations, at most 6 pairs can be within 50 m for participant 12 and at most 8 for PR 578. Thus at least 10 and 8 turbines, respectively, remain beyond 50 m even if matching is chosen to maximize closeness rather than minimize total distance. The object is not a rotated/reflected copy or a small uniform polish of either.

There is a concrete radial structural difference: the candidate has 4 turbines at radius about 1300 m,8 at 1167–1189 m, and4 at 519–528 m. PR 578 has 8 at1300 m,4 at 1139–1161 m, and4 at 550–563 m. This supports a distinct arrangement under the bank's operational topology criterion. Ring-like layout families and the general idea of multiple good layouts are already known; neither is an originality claim here.

As additional checks, I compared against all 12 official16-turbine participant layouts and the DPCRO-SL Table 5 coordinates. Literal matched counts beyond 50 m range13–16 for the official layouts; the rounded DPCRO-SL layout has16. Rotation/reflection sum-distance screens also retain10–16 displaced turbines for the participant layouts and11 for DPCRO-SL at the best screened alignment. These latter sampled alignment screens are supplementary, not global proofs.

Only after these checks did I inspect search.py and search_continuation.py. The source generates fresh jittered rings/random points; its only layout-file read is an optional checkpoint in the selected output directory, not a published reference. The supplementary author log reports resumed:false, seed 20261102, first energy attainment at restart 68 and final saved tiny polish at restart 80. Its original-generator-output coordinates exactly match the object. These are corroborating author records, not independent attestation of historical execution. PREREG's00:41:56 freeze precedes01:02:18 generation and is consistent with prospective search rules.

## Fresh source and comparator coverage

All network retrievals were made within the clock-observed UTC window2026-11-01T16:50:23Z–16:58:20Z. Source wrappers use that enclosing window rather than claiming exact per-request timestamps. Saved source hashes and downloaded16-turbine file hashes are in review-novelty/SHA256SUMS.json. Raw source wrappers and downloaded files are stored under data/review-novelty/sources/ and data/review-novelty/official/.

- [Official results folder](https://github.com/IEAWindSystems/iea37-wflo-casestudies/tree/master/cs1-2/iea37-cs1-results): fetched its live API listing once, then each of its 12 sixteen-turbine files once. Best posted value is 421561.89715066205MWh, participant 12; current source blob283959cbd7c1916fac9ee87e7715ae8fef4add18. Saved participant 12 file SHA25639dad7e8ca0a178654f9d5f0ea7d7d278be82f4df5e6529f0005b421d28101c9. Saved folder-listing wrapper SHA256976b5e0dfd94be3b7e29edb7aaef31f4f3c472743e4b8699368f19e659870a77.
- [PR 578](https://github.com/elder-plinius/V3R1T4S/pull/578): fetched current status once; open, draft, unmerged, head48c93384ff442fa71cfde0f643464ea1e8551da3. It claims424131.9503MWh and explicitly says its topology is related to participant 12. I fetched its actual object from that head, independently of its panel. Saved object SHA2569a9c561c2cc701d44eeb37e913ff1cad1a07fd2c9af5ceda0471469c792ddd74.
- [TROPHY_CASE](https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md), source blob18b731d7d4bf99efd323d48740284daccb8501b0, contains no wind/IEA37/energy entry. The full [known-knowns tree](https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns), treec41f34be71df2c58d62de4005c9e006ee7e324f4, has 5400 entries, untruncated; no paths identifying a wind/IEA37/clean-energy target or layout were present. All-state PR searches separately for wind, IEA37, turbine, and the exact target found PR 578 as the only relevant16-turbine claim; an additional circular search did not reveal another wind claim. Searches covered open and closed PRs. I found no additional confirmed comparator.
- [Pérez-Aracil et al., arXiv2212.00742](https://arxiv.org/pdf/2212.00742): directly verified Table 4 threshold 419935.7905 and Table 5 coordinates. Their rounded Table 5 coordinates recompute to419933.31588MWh; I use the target's 419935.7905 posted threshold without silently replacing it.
- [Pérez-Rúa et al.2023](https://wes.copernicus.org/articles/8/1453/2023/): Case I is about418GWh; data available upon request. It does not supply a stronger p2-subsuming object in the accessible paper.
- [Valotta Rodrigues et al.2024](https://wes.copernicus.org/articles/9/321/2024/): useful context but outside the last 24 months; its 360-direction model is expressly not directly comparable with the original 16-direction AEP.
- Last24months(2024-11-01 onward) literature searches included IEA37/IEA37 layout/AEP, Task37, and16-turbine optimization in2025 and2026. [Shao et al.2025](https://arxiv.org/html/2502.11088v1) use NREL5MW turbines, rectangular domains, and Weibull speed distributions; [Malisani et al.2025](https://wes.copernicus.org/articles/10/1611/2025/) use 81–250 turbine alignment cases. These do not subsume this fixed CS1 object.
- [Chen et al., Beyond a single solution,2026](https://www.sciencedirect.com/science/article/pii/S0306261926005040) is relevant prior work on structurally diverse layouts. Its public indexed abstract establishes the general multimodal-layout idea. A full-text open returned 403 Forbidden; I did not retry or seek to bypass that block. Full coordinate-level exclusion against that article remains unavailable. The present claim must stay an explicit p2 certificate, without claiming the first method or first demonstration of wind-farm multimodality.
- GitHub code searches included IEA37 sixteen-turbine layouts, literal 421304,419935, repositories updated since2024-11-01, and named benchmark repositories. [IEA37_Surrogates](https://github.com/bdvanberkel/IEA37_Surrogates) is turbine-load/power/CT surrogate data rather than this layout record. The newly updated [sebasanper fork](https://github.com/sebasanper/iea37-wflo-casestudies/commit/27ee2b57bb4c6e06ed9e4fa2da1747b3a01d4b89) only corrects a CS4 wind-resource reference.
- [ITA-LOW/otimiza-es](https://github.com/ITA-LOW/otimiza-es/tree/c63ddff4406a523e325c23c8f2aeba5bd0bc905a) contains explicit16-turbine alternatives. I fetched and checked all 60 rows of results_16/representative_solutions.csv: none satisfies radius 1300m; the smallest maximum radius is1576.574247m. Its larger reported AEPs therefore do not establish subsumption of this constrained certificate.

The literal universal comparator requirement is satisfied for all relevant known-known/open-claim objects located by these fresh repository and PR checks. Generic stronger energy alone is not a p2 counterexample: the useful additional result is a feasible high-energy arrangement materially different from those objects. The residual limitation is ordinary bounded literature coverage, especially the explicitly blocked 2026 full text; I do not certify global novelty or unseen-coordinate uniqueness.

pass: true
