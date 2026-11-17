# NOVELTY skeptic: apollo-moonquake-missed-vs-pds-catalog, p1, nest A39 member at S14, onset 1971-09-05 01:26:14 UTC
context: subagent (fresh context, Claude Code Agent tool, subagent_type novelty)

Object judged: claim/CLAIM.md, a new S14 member of catalogued deep-moonquake nest A39, onset 1971-09-05 01:26:14 UTC (1971 day 248), template window 01:25:44.150 to 01:33:14.150 UTC (450 s). Evidence used from the claimant: claim/ only. All fetches below are mine: one plain GET each, User-Agent "V3R1T4S-novelty-skeptic/1.0 (panel check)", with a timeout. Nothing was refused (no 401/403/429/503 or reset) and nothing was retried.

## 1. Status source (PDS Apollo seismic event catalogue, data folder)

| URL | HTTP | UTC | value found |
|---|---|---|---|
| https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ | 200 | 2026-11-13T05:57:39Z | 4211 bytes, sha256 593e0315...2e2f, the same as claim/data/catalog_data_index.html. 11 csv tables + inventory, latest file date 11/10/2020, no new table |
| .../data/collection_data_inventory.csv | 200 | 05:57:47Z | 874 bytes, lists the 11 products |
| .../data/gagnepian_2006_catalog.csv | 200 | 05:57:48Z | sha256 e79df3f3..., same as claim copy; no 1971-09 entry |
| .../data/levent.1008weber.csv | 200 | 05:57:49Z | 890253 bytes, sha256 f95743b2...b93c, same as claim copy; 13057 rows |
| .../data/lognonne_2003_catalog.csv | 200 | 05:57:50Z | sha256 3c78c5b1..., same; no 1971-09 entry |
| .../data/nakamura_1979_sm_locations.csv | 200 | 05:57:51Z | same; 1971 rows only on days 107, 140, 192 |
| .../data/nakamura_1983_ai_arrivals.csv | 200 | 05:57:51Z | same; artificial impacts only |
| .../data/nakamura_1983_ai_locations.csv | 200 | 05:57:52Z | same; nearest 1971 entry is day 215 (15 LM) |
| .../data/nakamura_1983_m_arrivals.csv | 200 | 05:57:53Z | same; 1971 rows on days 143, 163, 293 |
| .../data/nakamura_1983_sm_arrivals.csv | 200 | 05:57:53Z | same; 1971 rows on days 107, 140, 192 |
| .../data/nakamura_2005_dm_arrivals.csv | 200 | 05:57:54Z | same; per-nest relative times, no event dates |
| .../data/nakamura_2005_dm_locations.csv | 200 | 05:57:55Z | same; per-nest locations, no event dates |
| .../data/weber_2011_dmq_s_picks.csv | 200 | 05:57:55Z | same; per-nest S picks, no event dates |
| .../data/levent.1008weber.xml (label) | 200 | 06:07:48Z | field E: "Signal stop time in hours and minutes; 9999 if signal continues to next event." |

All 11 tables are byte-identical to claim/data/catalog/ (sha256 checked one by one). I parsed them myself:
- levent.1008weber.csv has no row on 1971 days 247 or 248. The nearest starts are 1971-246 22:57 (26.5 h before the onset, A1, no stop time) and 1971-249 19:12 (41.8 h after). No row lies within +/- 5 min of the onset or of the window start.
- Start-stop spans: no span contains the onset or overlaps the window. One row (1971-245 06:40, A223) has stop 9999. Read literally as a clock time, that would be a spurious multi-day span. Under the label's own definition it means the signal runs on to the next event, which is 1971-245 07:08, so the span ends 2.8 days before the onset. In total 888 rows use this sentinel.
- The other tables either have no event times (nest tables) or have no entry within weeks of the onset.

Status: no catalogued event within +/- 5 min, and the onset lies in no levent span. The status source was read (not PENDING).

## 2. Glitch catalogue named by the claim (Liu, Xiao and Li 2025, JGR Planets 130, e2025JE009277)

| URL | HTTP | UTC | value |
|---|---|---|---|
| https://zenodo.org/api/records/15715187 | 200 | 05:59:05Z | v1.0.1, 2025-06-22, one asset <acct>/lunar_ACC-v1.0.1.zip (109655361 B) |
| https://zenodo.org/api/records/15715186/versions?size=20 | 404 | 05:59:17Z | wrong endpoint (not a block); I used the next row instead |
| https://zenodo.org/api/records/15715187/versions?size=20 | 200 | 05:59:24Z | 1 version only |
| https://api.github.com/repos/<acct>/lunar_ACC/git/trees/HEAD?recursive=1 | 200 | 05:59:32Z | HEAD 73d055e2; catalogs/ has S14 Spike, Step-Up and Step-Down for MH1, MH2 and MHZ |
| https://api.github.com/repos/<acct>/lunar_ACC/releases | 200 | 05:59:33Z | release v1.0.1 (2025-06-22), no extra assets |
| https://api.github.com/repos/<acct>/lunar_ACC/commits?per_page=10 | 200 | 05:59:34Z | later commits (2025-08) add deep-cluster code only |
| https://api.github.com/repos/<acct>/lunar_ACC/git/trees/v1.0.1?recursive=1 | 200 | 06:07:34Z | all 36 catalog blobs are identical at tag v1.0.1 and at HEAD, so the release asset holds the same catalogues |
| https://raw.githubusercontent.com/<acct>/lunar_ACC/73d055e2.../catalogs/S14_ACC-{Spike,Step-Up,Step-Down}_{MH1,MH2,MHZ}_all.csv (9 files) | 200 each | 06:00:01Z to 06:00:15Z | Spike MH1 and MH2 are byte-identical to claim/data/lit/S14_ACC-Spike_MH1_all.csv and _MH2_all.csv |

My own interval test against the window [01:25:44.150, 01:33:14.150]:
- Spike MH1, MH2 and MHZ: no overlap. Nearest: MH1 00:37:10 and 01:51:01 (+1487 s from onset); MH2 1971-09-04 21:52:54 (-12799 s) and 05:18:34; MHZ 00:44:48 and 01:43:12 (+1018 s).
- Step-Up MH1, MH2 and MHZ: no overlap. The nearest is a Step-Up MH1 interval at 01:36:35 to 01:37:00, 621 s after the onset and 201 s after the window ends. It lies outside the window, and is noted here for the glitch check.
- Step-Down MH1, MH2 and MHZ: no overlap. Nearest: MH1 01:15:13 to 01:15:43 (ends 10 min before the window starts) and 01:49:54; MH2 00:30:23 and 03:47:38; MHZ 1971-09-04 18:49 and 09-05 16:42.

The claimed signal therefore carries no glitch label (spike or step) in the published catalogue on any S14 component.

## 3. Other published lists (last 24 months, plus older ones that were cheap to check)

Searches: web searches for recent expanded or new deep-moonquake catalogues (template matching, matched filter, machine learning), for "A39" nest papers, and for the date itself. Zenodo API searches q=moonquake, q=moonquakes and q="deep moonquakes" (sorted most recent, 06:03:07Z to 06:03:10Z, HTTP 200). Earlier queries with size=50 returned 400 (page-size limit, not a block) and were re-issued as different URLs with size=25. Lists checked:

| list | fetch (HTTP, UTC) | result |
|---|---|---|
| Shi, Li and Meng (Zenodo 22113858, 2026-08-26), IndividualEventsAndArrivalTimesFromMatchedFilter.xlsx (2604 cluster-station rows) | 200, 06:03:39Z | no row within 6 h of the onset. The nearest is A1 1971-246-22-57, which is itself a levent event. One A39 row, not in 1971 |
| same record, Event_Catalogues.zip (8 published location compilations) | 200, 06:03:40Z | nest location tables only, no event times |
| Shi, Li and Wang (Zenodo 16809589, 2025-08-12; JGR Planets 2025), Readme, 11_CatalogueForDifferentCriteria.zip (4 tables), 2_ and 5_SeachedIndividualEvents (EveCat_IndividualEvents.xlsx, 207 and 118 rows) | 200 each, 06:03:42Z to 06:04:41Z | no row within 6 h; no A39 rows. Their dates follow levent.1008c, so these are catalogued events |
| Yu (Zenodo 14781554, 2025-01-31), events_catalog.csv | 200, 06:03:44Z | 22 rows in 1971, none on days 240-256 |
| Li, Wang, Yu and Shi (Zenodo 22741655, 2026-09-14), code.zip | 200, 06:03:45Z | code only, no detection list. The 1.5 GB training_dataset.zip was not fetched |
| Onodera SP catalogue (Zenodo 8373651; JGR Planets 2024), S14_New_MQ_SP.csv and S15_New_MQ_SP.csv | 200, 06:05:55Z and 06:05:56Z | byte-identical to claim/data/lit/onodera_*. S14 has no window between 1971-09-03 18:37 and 09-07 22:15; S15 has none between 09-04 18:58 and 09-08 19:18 |
| Nunn et al. 2020 supplement (Zenodo 7787610), levent.1008c and README | 200, 06:06:20Z and 06:06:21Z | Nakamura's Dec 2018 revision: also no row on 1971 days 247-248 (246 22:57, then 249 19:12) |
| LunaSeis-1 (2026), GitHub page via WebFetch | read | no new event list; reports a negative continuous scan |
| Al-Qadasi 2026 FNO; Yang and Zhang 2026 (A01 only); Kim 2026 GRL (A1 events); Onodera 2026 GRL (one repeating shallow pair, SP); Tamama 2025 (Apollo 17 LSPE, 1976-77); Orbital-modulation 2026 (catalogued clusters) | search results and Zenodo metadata | none publishes an S14 1971 deep-moonquake list that could hold this event |

Web searches for the date (1971-09-05 or day 248 with moonquake) returned nothing. I found no published expanded deep-moonquake list from the last 24 months that lists this time.

## 4. The bank repository

- TROPHY_CASE.md (local copy, and live raw main fetched 06:06:59Z, HTTP 200, 31306 B): no Apollo, moonquake or lunar-seismic entry.
- known-knowns/ (local copy, and live contents listing fetched 06:07:00Z, HTTP 200, 31 entries): none on Apollo, Moon or seismology.
- The bank repository's public pull-request search pages (WebFetch, about 06:01Z to 06:08Z): "apollo" 0 open / 0 closed; "moonquake" 0 / 0; "lunar" 0 / 0; "A39" 6 results, all OEIS A39xxxx claims unrelated to this target.

## 5. Comparison (trivial-edit test)

- Published objects for this cell are the catalogued events of nest A39 and of every other class in levent and the other lists above. The nearest catalogued event of any type is 26.5 h away. So no deletion, restriction, relabelling or time-polish of a published row yields this onset.
- The template is seeded from published A39 members: the S14 stack of 16 catalogued 1971 A39 events, which the claim names. What it adds beyond the seed is a detection at a time no list contains.
- Not a relabel of a sibling or other-nest detection. In the claimant's own scan (claim/results/s14_multinest_scan_1971.jsonl, day 248), all 24 other nests stay at D <= 0.19 within +/- 30 min of the onset, against A39's 0.644. The same lens's other objects are at different times: A38 at 1971-05-13 and A201 at 1971-08-17 (claim/results/seeds_summary.json).
- Not a catalogued glitch: no spike, step-up or step-down interval on S14 MH1, MH2 or MHZ overlaps the window.

## Concerns (not novelty defects, for the other skeptics)

- Every catalogue checked is blank around this date: levent (1008weber and 1008c) has no event on 1971 days 247-248, and Onodera's SP catalogue has no S14 window for about 4 days and no S15 window for about 4 days. That could be a quiet spell (levent also has 0 on day 235), or the original analysts may not have read these days. Either way it favours newness. It also makes the waveform gap and timing checks at this onset worth confirming independently.
- A Step-Up MH1 glitch starts 201 s after the window ends. It is outside the window, so it is relevant only to the glitch check.
- Not checked: Civilini et al. 2021 (CNN, GJI) and Yuan et al. 2021 cluster lists (both older than 24 months, so outside the criterion's window); Knapmeyer-Endrun and Hammer 2015 (Apollo 16 data, from 1972); the 1.5 GB training set of Zenodo 22741655.

Verdict: the claimed A39 member at 1971-09-05 01:26:14 UTC on S14 is absent from every table of the live PDS catalogue folder (re-fetched; identical to the claimant's copies), from every published list of the last 24 months I could find and read, and from all nine S14 files of the published glitch catalogue. It is not a trivial edit of any published object.

pass: true
