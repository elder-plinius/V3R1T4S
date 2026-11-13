# Panel: NOVELTY skeptic (p1, apollo-moonquake-missed-vs-pds-catalog)

context: subagent (fresh context, Claude Code Agent tool, subagent_type novelty)
written: 2026-11-13T00:03Z
object judged: one new member of nest A38 on S14 MH1/MH2, onset 1971-05-13 18:40:03.7 UTC (template window start
18:39:33.7 UTC), as stated in CLAIM.md and results/seed_checks_final.json.
scope: novelty only (is the event already in the PDS catalogue, in any other published moonquake list, or in an earlier
claim in this repository). Whether the detection is real (CC, null, gap/glitch/thermal) is for the other two skeptics.

## 1. Status source, fetched live once (no retries)

- URL: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/
- time: 2026-11-12T23:48:59Z, one GET, User-Agent naming V3R1T4S, HTTP 200, 4211 bytes,
  sha256 593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f (identical to data/catalog_data_index.html).
- value: 12 CSV tables listed, newest listing date 11/10/2020; levent.1008weber.csv 890,253 bytes dated 6/4/2019.
- Every CSV table re-fetched once each, 3-4 s apart, 2026-11-12T23:49:12Z to 23:49:52Z, all HTTP 200. Each is
  byte-identical (sha256) to the claim's copy in data/catalog/; levent.1008weber.csv fetched 23:49:19Z,
  sha256 f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c, 13,057 rows.

## 2. PDS tables vs the candidate (own parser, not the claimant's code)

- levent.1008weber.csv: nearest rows are 1971-133 16:03 (stop 16:40, type C), 2 h 37 min before the onset (stop 2 h 00 min
  before), and 1971-134 00:30 (A209), 5 h 50 min after. No row within +/- 5 min; the onset lies inside no start-stop span
  (9999 rows resolved to the next event's start).
- Tables with event times, nearest |dt|: nakamura_1979_sm_locations 600,306 s; nakamura_1983_sm_arrivals 600,476 s;
  nakamura_1983_m_arrivals 877,196 s; nakamura_1983_ai_locations, gagnepian_2006_catalog, lognonne_2003_catalog about
  6.66e6 s (three malformed lognonne dates, 1972/1976/1977, skipped). nakamura_2005_dm_arrivals, nakamura_2005_dm_locations
  and weber_2011_dmq_s_picks are per-nest tables with no event times; collection_data_inventory.csv has none.
- Catalogued A38 events in 1971: days 081, 106, 186, 187, 242 (two), 270, 297 (two), 324, 351. None on or near day 133, so
  the candidate is not a relabelled, re-timed or re-typed catalogue row. It falls 27 days after day 106 and 53-54 days
  before days 186-187, in the gap of the nest's monthly sequence.

## 3. Other published lists (last 24 months, plus older lists that cover S14 in 1971)

Each file below was fetched once and checked by time (+/- 5 min) with my own code; none has an event near the candidate.

- Nunn et al. 2020 electronic supplement (Zenodo 7787610): levent.1008c (Dec 2018 minor revision; 13,058 lines) has the
  same rows around 1971-133 as levent.1008weber, nearest 16:03; Nunn19_LunarCatalog_v1.xlsx has no 1971-05-13 row.
- Onodera 2023/2024 SP catalogue (Zenodo 8373651): the claim's data/lit/onodera_S1[456]_New_MQ_SP.csv have the same md5 as
  the Zenodo files; the nearest S14 window is 1971-133 23:03-23:38 (+4 h 23 min). Onodera 2026 (GRL, repeating shallow
  moonquakes) builds on that data set.
- Shi 2026, Zenodo 22113858 v3 (2026-08-26), IndividualEventsAndArrivalTimesFromMatchedFilter.xlsx: 2,604 rows over 17
  clusters (A1, A6, A18, A20, ...; no A38). The nearest is 1971-133 10:28 (A7, a levent time), 8.2 h away. (The claim calls
  this list A1-only; in fact it spans 17 clusters, but that does not change the result.)
- Shi 2025, Zenodo 16809589, 11_CatalogueForDifferentCriteria (four catalogues built from levent.1008c onsets): A38 appears
  only on catalogued days (e.g. 1971-270, 297, 324). The nearest row of any cluster is 10.6 days away.
- Zenodo 14781554 (2025-01-31, ML classification of impacts and deep moonquakes), events_catalog.csv, 273 rows: on
  1971-133 only 10:51 (impact).
- Zenodo 22741655 (2026-09-14, automated detection/classification of deep moonquakes and impacts): the release has code only
  (STA/LTA, MultiRocket); I checked its file listing. It publishes no detection list. Training set (1.5 GB) not downloaded.
- Zenodo 23610362 (2026-10-24, A01 tidal modulation): event_times.npy (1.6 kB) holds A01 events only, so it is not an
  expanded list (judged from the file listing).
- Zenodo 21361572 (LunaSeis-1, 2026-07-14; GitHub releases v0.1.0 and v0.1.1): its release-claims document reports a
  negative continuous-scan result and claims no new events.
- Supplementary, not a moonquake list: Liu et al. 2025 acceleration-glitch catalogues (Zenodo 15715187; repository catalogs/
  S14 MH1/MH2 spike, step-up and step-down CSVs, fetched once each). There is no catalogued glitch on S14 MH1/MH2 between
  17:00 and 19:08:36 UTC on 1971-05-13. The first is an MH2 step-down at 19:08:36, after the template window and the
  claim's +/- 10 min check span.
- These lists cannot contain a 1971 S14 event: Knapmeyer-Endrun and Hammer 2015 (S16 only, from 1972), Kawamura 2015 (Apollo
  17 LSG), Civilini 2021/2023, Tamama 2025 and Al-Qadasi 2026 (Apollo 17 LSPE or methods only), Majstorovic 2024 (nest
  classification of catalogued events).
- Searches: web searches (template matching, ML catalogues, A38, 2025-2026 deep-moonquake papers); the arXiv API
  ("moonquake", 8 hits, no event list); the Zenodo API ("moonquake OR moonquakes", all 35 records reviewed by title and
  file list). I found no published expanded deep-moonquake list from the last 24 months that contains this event, and no
  list that contains any A38 member on 1971-133.

## 4. This repository

- TROPHY_CASE.md: the pinned local copy (commit cf68067f) and the live main fetched 2026-11-12T23:52:15Z (HTTP 200) have
  no Apollo, moonquake or lunar entry.
- known-knowns/: the local copy and the live tree (fetched 23:52:19Z) have no Apollo folder.
- Pull requests, searched over the web, open and closed: "moonquake" 0/0 (23:51:23Z), "apollo" 0/0 (23:51:28Z),
  "lunar" 0/0 (00:01:18Z). "seismic" returns 1 open PR (#785, a terrestrial ComCat claim, unrelated). A positive control
  ("gold") returned results, so the search works. An issues search for "moonquake" showed no results.
- The bank entry exists only under known-unknowns/ (open). No earlier claim covers this event.

## 5. Trivial-edit comparison

The object is a single event time for a catalogued nest. The template is seeded from six catalogued 1971 A38 events,
which the claim names. No published entry for any nest or event type lies within 2 h of the onset, so no deletion,
restriction, relabelling or re-timing of a published row produces it. It is strictly new compared with everything
listed above. This is an existence claim, not a score claim, so the tie rule does not apply.

## Verdict

novelty: confirmed. The status source was read live and the claim's statement holds: no row of any PDS table lies within
90 minutes (in fact within 2 h 00 min of any start or stop). The event is not in any other published list I could find,
and no earlier claim in this repository covers it. Limits: unreleased detection outputs (e.g. the 2026 automated-method
paper) and hackathon repositories cannot be searched exhaustively. This verdict covers novelty only.

pass: true
