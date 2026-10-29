# Novelty skeptic: tsunami-tide-gauge-signal-not-in-ncei, partial win p3 (completeness map)

context: subagent (Claude Agent tool, fresh context, model claude-opus-5-5)

Read: claim/CLAIM.md, claim/result/map_summary.txt, the scout's saved NCEI listing (claim/data/ncei_events_2015_2026_p1.json
and _p2.json, hashes only plus event count), and the repository's TROPHY_CASE.md. Nothing else in the run folder was read.

## Bottom line

p3 has not been claimed, confirmed or merged in this repository, and the last 24 months of literature has no gauge-based
completeness map of this population. The closest prior work is the map posted as data in issue #253. That map is not
panelled, its author says it is not claimed, and no saved code was posted for its latest version (run 4). Its numbers
differ from this claim's, so it does not tie or subsume the claim. The claim does not beat #253 run 4 on every axis,
though (see "Relation to the closest prior numbers").

## Status source (one honest GET)

| URL | UTC time | HTTP | bytes | sha256 | value read |
|---|---|---|---|---|---|
| https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search | 2026-10-24T21:43:20Z | 200 | 1765 | 3fec2a9935a8d6d3f351d6c2a0c49ccf4a904016e5ac2820e48c55e1122987b6 | JavaScript app shell, title "NCEI Global Historical Hazard Database"; no listing rows in the HTML |

The sha256 is identical to the scout's fetch at 2026-10-24T19:20:24Z (claim/CLAIM.md), so the page has not changed
since then. The page holds no table values; the listing it fronts is the events API. That API was not among my allowed
fetches, so I did not re-fetch it. Instead I re-hashed the scout's saved copies: claim/data/ncei_events_2015_2026_p1.json
(bdc6a6b4...b0f9) and _p2.json (64745d27...220a) match the sha256s in claim/CLAIM.md. They hold 230 events for
2015-2026 (totalItems 230; 200 + 30 rows), and the newest is event 6193 (2026-10-09, Isla Canas, Panama). For a
completeness map there is no single record cell: the NCEI listing is the reference the map is scored against, not a
number to beat. Saved as panel/work_novelty/status_event-search.html.

## Fetch record (all with User-Agent 'V3R1T4S-research (honest client)', one GET per URL, no retries)

| # | URL | UTC time | HTTP | bytes | sha256 | saved as (panel/work_novelty/) |
|---|---|---|---|---|---|---|
| 1 | https://www.ngdc.noaa.gov/hazel/view/hazards/tsunami/event-search | 2026-10-24T21:43:20Z | 200 | 1765 | 3fec2a9935a8d6d3f351d6c2a0c49ccf4a904016e5ac2820e48c55e1122987b6 | status_event-search.html |
| 2 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+tsunami&per_page=100 | 2026-10-24T21:43:36Z | 200 | 43830 | 5ae00103515fa9cc3199e8607cf08ab4c60fcc26bf3e64eed8dda2ef976542db | gh_search_tsunami.json |
| 3 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+%22completeness+map%22&per_page=100 | 2026-10-24T21:43:59Z | 200 | 79 | c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0 | gh_search_completeness_map.json |
| 4 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+NCEI&per_page=100 | 2026-10-24T21:43:59Z | 200 | 43830 | 5ae00103515fa9cc3199e8607cf08ab4c60fcc26bf3e64eed8dda2ef976542db | gh_search_ncei.json |
| 5 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+%22tide+gauge%22&per_page=100 | 2026-10-24T21:43:59Z | 200 | 43830 | 5ae00103515fa9cc3199e8607cf08ab4c60fcc26bf3e64eed8dda2ef976542db | gh_search_tide_gauge.json |
| 6 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+SLSMF+OR+ComCat+OR+meteotsunami&per_page=100 | 2026-10-24T21:44:13Z | 200 | 47903 | 4b14a97774a09f1ef189a61abae1b67d15d0251473a0fd9805ac8b148bec8aee | gh_search_slsmf_comcat.json |
| 7 | https://api.github.com/repos/elder-plinius/V3R1T4S/issues/253/comments?per_page=100 | 2026-10-24T21:44:13Z | 200 | 15693 | 23b2c8b808500c44bc4ebf192a92a0f31c52c0841e43fde8a9088b77d296ccb5 | gh_issue253_comments.json |
| 8 | https://api.github.com/repos/elder-plinius/V3R1T4S/issues/642/comments?per_page=100 | 2026-10-24T21:44:14Z | 200 | 9963 | 09e8ac05ed7977501787e2a1aaab21f8148604972acbd8f63b81340c862f452b | gh_issue642_comments.json |
| 9 | https://api.github.com/repos/elder-plinius/V3R1T4S/issues/371/comments?per_page=100 | 2026-10-24T21:44:14Z | 200 | 9775 | d07601ccee584f3f953634a1c6f0d04cb2feeec6b5909d2a133aedd9b99ab924 | gh_issue371_comments.json |
| 10 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+completeness&per_page=100 | 2026-10-24T21:50:43Z | 200 | 45768 | 4740692493f82ee0eaaf2838aa8a4f2f48b8b19e0d3921aab7f4764bd8ca33cc | gh_search_completeness.json |
| 11 | https://hazards.colorado.edu/uploads/poster_session/Wright_2024NHWPoster.pdf (WebFetch tool) | about 2026-10-24T21:46:54Z (tool cache file time) | not exposed by the tool | 1854018 | 530b641a77cf887499063a2db1d22bd8222b2fa14056f17e86c0464ae1add17d | wright_2024_nhw_poster.pdf (copied from the tool's own cache) |
| 12 | https://nhess.copernicus.org/articles/26/2415/2026/ (WebFetch tool) | about 2026-10-24T21:47Z | not exposed by the tool | not saved | not saved | (text summarised by the tool only) |

The log is also in panel/work_novelty/fetch_log.tsv. Searches 2, 4 and 5 returned byte-identical responses (the same three
items). Budget used: 6 of 6 GitHub searches and 3 of 4 item GETs. No HTTP 401, 403, 429 or 503 responses and no
challenge pages. Besides these, the WebSearch tool ran 6 queries (listed below). Note: the WebFetch tool keeps its own
copy of the PDF in the session's tool-results cache. I did not choose that location; it is outside my two write paths.

## Repository search

- TROPHY_CASE.md (repository commit 1ebdef41c30414cd2a036b00f5e81d0fc4c1dc25, sha256 b946f68e...71a1): six result
  families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP, RobustBench)
  and two cipher commitments, 53 rows in all. A grep for tsunami, tide, NCEI, NGDC, completeness, gauge, p3, seism,
  earthquake and IOC has no hits. **p3 is not in the trophy case.**
- GitHub searches (issues and pull requests, open and closed) for tsunami, NCEI, "tide gauge", SLSMF/ComCat/meteotsunami,
  "completeness map" and completeness. Every tsunami-related hit:
  - **#253** (issue, open, created 2026-10-16): https://github.com/elder-plinius/V3R1T4S/issues/253. A bank note about the
    wording of the ±10 min rule and p3's denominator. Body: "Not claimed: no win and no partial win." It contains the
    closest prior map (details below). It also says "A three-skeptic panel failed our p3 map".
  - **#371** (pull request, closed unmerged 2026-10-24): https://github.com/elder-plinius/V3R1T4S/pull/371. Bank pitfalls
    (travel-time error, solver check, p3 denominator: 264 quakes in water, and 6/21/42 with no IOC station within
    1500/1000/500 km). The maintainer closed it to apply the pitfall directly in the bank. These pitfalls are the ones
    claim/CLAIM.md quotes. It has no map.
  - **#642** (pull request, open, not merged): https://github.com/elder-plinius/V3R1T4S/pull/642. Claims **p1** for NCEI
    event 5942. Its "Not claimed" section says: "No claim about other events; no completeness fraction (p3)." Its three
    comments are about event 5942 only.
  - Other hits are unrelated targets: #633 (seismic-missed-events-vs-comcat), #703 and #201 (Kuhn poker), #216, #203, #370.
- **No issue or pull request claims, confirms or merges p3.** That matches the scout's record in claim/CLAIM.md.

## Literature, about 2024-10 to 2026-10

WebSearch queries: (1) global tide gauge tsunami detection catalogue earthquakes completeness NCEI database 2025;
(2) fraction of M6.5+ shallow submarine earthquakes producing tsunami signal on tide gauges systematic study;
(3) arXiv automatic tsunami detection IOC sea level monitoring facility tide gauges catalog of small tsunamis;
(4) tsunamis missing from NOAA NCEI historical tsunami database detected in sea level records 2015-2025 completeness;
(5) Zenodo OR GitHub dataset tsunami signals tide gauge records all earthquakes M6.5 2015-2025 IOC SLSMF detection
catalogue; (6) detectability of small tsunamis global tide gauge network statistical analysis earthquakes Pure and
Applied Geophysics 2025 2026.

Closest items found. None is a gauge-based completeness map of this population:
- Galan Perez et al., "The TSUSY Database", NHESS 26, 2415-2436 (29 May 2026),
  https://nhess.copernicus.org/articles/26/2415/2026/. It is **simulation-based**: USGS Mw >= 6 earthquakes, 1976-2023,
  labelled tsunamigenic by modelled wave height (0.15 m threshold) and compared with NOAA. About 63 % of NOAA events are
  labelled; 239 are common to both, 194 are TSUSY-only and 138 NOAA-only. It does not use tide-gauge detections, open
  gauges or a per-quake signal test, so it is a different object.
- Wright et al., "NCEI Tsunami Data: Capturing Tsunami Stories Through Global Observations", 2024 Natural Hazards Workshop
  poster, https://hazards.colorado.edu/uploads/poster_session/Wright_2024NHWPoster.pdf. A database overview: over 2,800
  events and 31,000 wave observations. It gives no completeness fraction.
- NHESS 25, 1169 (2025), "Tsunami detection methods for ocean-bottom pressure gauges",
  https://nhess.copernicus.org/articles/25/1169/2025/. It benchmarks detection algorithms on DART records for 18 events,
  not a population map.
- Older or regional work: Koshimura's 2012 Pacific tsunamigenic ratio (NHESS 12, 175) and the 2019 New Caledonia catalogue
  update (NHESS 19, 1471). Both are outside the 24-month window and differ in population.
- Zenodo and GitHub: no dataset matching this population, open IOC gauges and an NCEI comparison. The only hit for the
  2015-2025 M >= 6.5 ComCat population was this repository's #371.

## Relation to the closest prior numbers

| | #253 run 3 (issue body, 2026-10-16) | #253 run 4 (comment, 2026-10-16T19:58:51Z) | this claim (result/, v5 rules) |
|---|---|---|---|
| population | 265 (ETOPO1 1-arcmin water cell) | 265 | 264 (2-arcmin water cell) |
| scored / usable | 131 | 195 | 188 (221 before the 24 h overlap rule) |
| unscored | 134 | 70 | 76 (34 overlap, 17 no data, 25 no gauge) |
| fraction with signal | 36/131 = 0.275 | 60/195 = 0.308 | 26/188 = 0.138 |
| bounds over all quakes | 0.136-0.642 | 0.226-0.491 | 0.098-0.386 |
| chance rate | fake-origin null (number not posted in body) | 14/351 = 0.040 per window; best of 400 catalogues 0.065 | 0.027; best of 400 catalogues 0.0495 |
| NCEI-listed quakes passing | not posted | 45 of 82 covered | 24 of 86 scored |
| rules | frozen before scoring | frozen before scoring | v5 is a declared post-hoc repair; the frozen v4 rules give 35/221 = 0.158 |
| panel | "A three-skeptic panel failed our p3 map" | "this was not panel-reviewed" | this panel |
| saved code and data | issue-bundle.zip (about 100 KB): tables and summary code, no raw series. Its host was not among my allowed fetches, so I could not inspect it | none posted with the comment | code, raw IOC windows with provenance, travel-time validation (claim/CLAIM.md, Files) |
| claimed as p3 | no ("Not claimed") | no | yes |

- **Tie?** No. All three maps cover essentially the same population and network, but the tests differ, and so do the
  fractions and denominators.
- **Subsumed?** No.
  - Run 3 is the only prior map with posted code. The claim beats it on coverage: 188 against 131 quakes scored, and an
    interval over all quakes of width 0.288 against 0.506. Run 3 also failed its own panel.
  - Run 4 has no posted code and no panel. p3 explicitly requires a map "reproducible from saved code", so run 4 does not
    provide the p3 object.
- **Where the claim does not beat run 4**, stated plainly so the chair can weigh it:
  - Run 4's posted numbers detect far more of NCEI's listed tsunamis (45/82 = 0.55 against 24/86 = 0.28).
  - Run 4 scores more quakes under its headline (195 against 188).
  - Run 4's interval over all quakes is slightly tighter (width 0.265 against 0.288).
  - Run 4's rules were frozen before scoring, while the claim's headline rules are a declared post-hoc repair.
  - As a measure of "any tsunami signal" (p3's wording), run 4's looser test is closer. The claim itself says 0.138 is a
    test-pass fraction, not the fraction of quakes with an observable signal.
- **Where the claim is ahead of run 4:**
  - Its data reaches more quakes before the overlap rule (221 against 195).
  - Its chance rate is lower (0.027 against 0.040).
  - Its travel-time model is validated against held-out NCEI arrivals (a 0.468 miss rate, reported).
  - It has the stated denominator and explicit no-data counts the bank pitfall asks for.
  - It has a saved bundle.
- Whether the claim's test measures what p3 asks for is a criterion question, not a novelty one, and I do not judge it here.

## Judgement

Nothing in TROPHY_CASE.md, in this repository's issues or pull requests (open or closed), or in the 2024-2026 literature I
found claims, confirms, ties or subsumes a p3 map of this population. The only prior map that satisfies "reproducible from
saved code" (#253 run 3, if its bundle holds the code) has much less coverage and failed a panel. The higher-coverage
prior numbers (#253 run 4) were posted without code, unpanelled and unclaimed, and they are a different test at a
different operating point (more sensitive, less specific). Measured against p3 as specified, the claim is the first
reproducible completeness map of this population on open gauges against the NCEI listing. It is not a tie with anything
known. The novelty is in delivering p3 as specified, not in new numbers that dominate #253 run 4; the panel should weigh
the gap in listed-tsunami recall and the post-hoc headline rules under the criterion and rigor questions.

Limits of this check: I could not open #253's issue-bundle.zip (github.com/user-attachments is not an allowed host), and
I did not re-fetch the NCEI events API. The listing is taken from the scout's saved files, whose hashes I re-verified.

pass: true
