# Panel: NOVELTY skeptic (p1 rebuild, apollo-moonquake-missed-vs-pds-catalog)

context: subagent (fresh context, Claude Code Agent tool, subagent_type novelty)
pds_fetch_utc: 2026-11-13T09:18:15Z
written: 2026-11-13T09:20Z

- object judged: one claimed new member of nest A38 on S14 MH1/MH2.
  - Onset: 1971-05-13 18:40:03.735 UTC.
  - Template window: 18:39:33.735 UTC + 450 s.
  - Sources: CLAIM.md, results/seed_checks_final.json.
- scope: novelty only. Is the event already in a PDS table or in any other published list? Could it be a relabelled
  published object (including a published glitch)? Does this repository already hold a claim for it? Whether the
  detection is real (CC, null, gap/glitch/thermal) is for the other two skeptics.
- method: my own code, not the claimant's, kept in the panel scratch folder. Each URL got one GET with a User-Agent
  naming V3R1T4S, a few seconds apart, with no retries.

## 1. Status source, fetched live just before this verdict

- URL: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/
- Fetched 2026-11-13T09:18:15Z: HTTP 200, 4211 bytes, sha256
  593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f. This is the same as
  data/catalog_data_index_2026-11-13T083957Z.html and data/catalog_data_index.html.
- The page lists 12 CSV tables. The newest listing date is 11/10/2020. levent.1008weber.csv is 890,253 bytes, dated
  6/4/2019.
- Every CSV was fetched once, 5 s apart, from 09:18:20Z to 09:19:17Z. All returned HTTP 200, and every one is
  byte-identical (sha256) to the claim's copy in data/catalog/:

| table | fetched (UTC) | bytes | sha256 |
|---|---|---|---|
| collection_data_inventory.csv | 09:18:20Z | 874 | 760f8db68daca4f7e374ccb61e9ed4eced5efd5ab829603035b3b7ce0e18946a |
| gagnepian_2006_catalog.csv | 09:18:25Z | 3405 | e79df3f30efa927d730f873085a7b60307c4e94913a1e5584489d6d6f6c14459 |
| levent.1008weber.csv | 09:18:30Z | 890253 | f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c |
| lognonne_2003_catalog.csv | 09:18:36Z | 5832 | 3c78c5b130e521193e581e8a63ff9254ffe3251f072d9fcd0c62eb35e7bc3d1d |
| nakamura_1979_sm_locations.csv | 09:18:41Z | 933 | 151307757fd66017c3e71dda2db27be4f27c58012a869b56763c0305d86759b5 |
| nakamura_1983_ai_arrivals.csv | 09:18:46Z | 430 | e3e3b102ed4e9b74d1694268b57bbe83e6115217570a432883526b745c4e2541 |
| nakamura_1983_ai_locations.csv | 09:18:51Z | 330 | f3fa3ce4837c4d5ad355a189968e25cb974fba9c4da84dbbf41f59d2fb459776 |
| nakamura_1983_m_arrivals.csv | 09:18:56Z | 2717 | 63fe558b00830850b52265e0345bf32d7999789ebcca8959d9937e8e1f56ae8b |
| nakamura_1983_sm_arrivals.csv | 09:19:01Z | 2128 | 221c34ea914663397a2e01d2be6ed5c1ed2669f4bfbbb6019f1de9bb50760b4b |
| nakamura_2005_dm_arrivals.csv | 09:19:06Z | 4708 | 2c677fe71e618c77b81d7f01752f8f0e5bbc2c57dd6511cf82a0b2e08c57c4e1 |
| nakamura_2005_dm_locations.csv | 09:19:11Z | 3651 | 539e3c6481c1050c78d7dc0042ceb0036c8173fd56ef46db0ebab76a7d58d485 |
| weber_2011_dmq_s_picks.csv | 09:19:17Z | 670 | 1374ea5645d90207390d2492f801da944c605a77f52d8c11a29637323e70da0f |

## 2. PDS tables vs the onset (own parser, run on the live copies at 09:19:23Z)

- **levent.1008weber.csv**: 13,057 dated rows, all parsed.
  - No row starts within +/- 5 min of the onset. I added 60 s of slack for the minute resolution.
  - The onset lies in no start-stop span. Spans crossing midnight were handled. A 9999 stop was resolved to the next
    row's start.
  - No span overlaps the 450 s window.
  - Last row before the onset: 71,133,1603,1640 (type C). It starts 157.1 min before the onset and stops 120.1 min
    before it.
  - First row after the onset: 71,134,0030 (A209), 349.9 min after.
  - The only 9999-stop rows that day are at 02:52, 03:00 and 03:50 UTC, all over 14 h earlier.
- **Other tables with event times.** Nearest |dt| to the onset:

| table | nearest row | nearest \|dt\| |
|---|---|---|
| nakamura_1979_sm_locations | 1971-140 17:25:10 | 600,306 s |
| nakamura_1983_sm_arrivals | 1971-140 1728 | 600,476 s |
| nakamura_1983_m_arrivals | 1971-143 2220 | 877,196 s |
| gagnepian_2006, lognonne_2003, nakamura_1983_ai_locations | 1971-07-29 20:58 (15 S-IVB) | about 6.66e6 s |

- Three lognonne_2003 Date values do not parse: 761142313, 7704712332 and 721081524. None can be a 1971 date.
- Tables with no event times: nakamura_1983_ai_arrivals, nakamura_2005_dm_arrivals, nakamura_2005_dm_locations,
  weber_2011_dmq_s_picks and collection_data_inventory.
- **Catalogued A38 rows in 1971**: days 081, 106, 186, 187, 242 (two), 270, 297 (two), 324 and 351. None is on day 133.
- **Mis-dated rows.** No levent row in 1971 days 100-165 starts at 18:35-18:45 on a nearby day in a way that would
  suggest a mis-dated copy of this event. The only ones are 1971-106 18:44 (A18) and 1971-159 18:40 (unclassified).
- Result: the claim's statement holds. No dated row of any PDS table lies within +/- 5 min, and the nearest stop is
  120 min before the onset.

## 3. Published lists, 2025-2026 first (each file fetched once and checked by time with my own code)

Each list is named with what it covers.

- **Shi et al. 2026, Zenodo 22113858** (2026-08-26), fetched 09:07:52Z-09:08:04Z.
  - IndividualEventsAndArrivalTimesFromMatchedFilter.xlsx: 2,604 rows over 17 clusters (A1, A6, A7, A11, A16-A18,
    A20, A25, A27, A30, A34, A40-A42, A44, A50). It has no A38.
  - Its rows on days 133-136 are A7 1971-133 10:28 (a levent time), then A1/A18 on day 134 and later. The nearest is
    8.2 h away.
  - Event_Catalogues.zip holds eight per-nest location tables (Nakamura, Bulow, Zhao, Gagnepain, Khan, Lognonne,
    Garcia, Hempel) with no event times.
- **Shi et al. 2025, Zenodo 16809589**, fetched 09:06:25Z-09:07:52Z.
  - Readme: the dates are "consistent with the levent.1008c catalog", so these are catalogued onsets.
  - File 5 EveCat_IndividualEvents.xlsx (118 rows): A38 rows only on S15 at 1971-270, 297, 324, 1972-013 and
    1977-173/200/227/254.
  - File 2 EveCat_IndividualEvents.xlsx (207 rows): no A38.
  - The four 11_CatalogueForDifferentCriteria catalogues: A38 only on the same catalogued days.
  - The nearest row of any cluster to the onset is A18 S14 1971-132 16:01 (in File 2 and in
    Catalogue_LowFreq_CC0.3_WL700s), 26 h 39 min before. The original NOVELTY panel said "10.6 days" for these
    catalogues. That figure is slightly off, but the correction does not change the result.
- **Zenodo 14781554** (2025-01-31, ML classification of impacts and deep moonquakes). events_catalog.csv has 273 rows.
  On 1971-133 it has only row 88, start 1051 (an impact, type C, AP14), about 7.8 h before.
- **Zenodo 22741655** (2026-09-14, automated detection and classification of deep moonquakes and impacts).
  - code.zip (STA/LTA, MultiRocket) holds code only. The trigger CSVs it reads are not published.
  - training_dataset.zip (1.5 GB) was not downloaded. I read its central directory with one ranged GET of the last
    4 MB (HTTP 206).
  - Its 150 deep-moonquake and 236 impact windows are named by catalogue event number (evtNNNN_Sxx). The nearest
    S14 ids to day 133 are impacts evt1221 and evt1222.
  - Its 530 noise windows are named MM_DD_HH_MM_Sxx, and none is an S14 window on 05-13. The only 05-13 windows are
    01:19 (S16), 02:51 (S15) and 04:57 (S16).
  - It publishes no detection list.
- **Zenodo 23610362** (2026-10-24, tidal modulation of deep moonquakes, A01).
  - The Zenodo zip-preview endpoint (/files/opensource_release.zip/container) answered HTTP 403 at 09:10:03Z. I did
    not retry it, so that preview is unread.
  - I then downloaded the record's file itself once (09:10:22Z, HTTP 200, 228,641,775 bytes).
  - data/event_times.npy and output/results/*/ApolloA01Data_event_times.npy hold 180 A01 event times (Unix seconds).
    The nearest is 386,910 s (4.5 days) from the onset.
  - It is not an expanded list for any other nest.
- **LunaSeis-1, Zenodo 21361572 v0.1.1** (2026-07-14), fetched 09:08:51Z.
  - The GitHub releases (v0.1.0, v0.1.1) carry only the paper PDF and SHA256SUMS as assets.
  - Its trigger and score files (continuous_scanning_triggers_v0.1/v0.2, grade_c_challenge_triggers) have no entry on
    1971-05-13 at 18-19 UTC. Its S14 scan triggers start 1971-08-07.
  - Its 1971-05-13 entries are catalogue events (levent-01232..01238) and catalogue-negative background windows on
    S12 MH2 (18:00-18:10, 19:30-19:40).
  - Its release documents report negative scan results.
- **Onodera 2023/2024 SP catalogue, Zenodo 8373651.** S14_New_MQ_SP.csv was fetched at 09:12:35Z. Its sha256
  (160018f2...d1a9) matches data/lit/onodera_S14_New_MQ_SP.csv. The nearest S14 window is 1971-133 23:03-23:38,
  4 h 23 min after the onset.
- **Nunn et al. 2020 electronic supplement, Zenodo 7787610.**
  - levent.1008c (fetched 09:15:08Z): its day-133 rows match levent.1008weber (last 16:03-16:40, next 134 00:30
    A209).
  - Nunn19_LunarCatalog_v1.xlsx: no 1971-05-13 row (May 1971 rows only on 05-20 and 05-23).
- **planetary-seismic-triage** (GitHub, 2026; repository, releases and tree read at 09:11:48Z-09:12:16Z).
  - candidates_lunar.csv (282 candidates) covers only S12, S15 and S16 sample files, with no S14 and no 1971-05-13.
  - Its archive scan covers S12, S15 and S16. I did not open its two release assets: results-freeze-artifacts.zip
    and seed_variance_unet.json, both 2026-07-18 and older than the tree's archive-scan results.
- **lunar-seismic-fno, Zenodo 18773537** (Al-Qadasi et al. 2026, Earth and Space Science): code only, no event list.
- **arXiv API** (query moonquake / deep moonquake / Apollo seismic, newest first, 09:11:19Z): 10 entries, none an
  event list.
- **Zenodo API** (moonquake OR moonquakes OR "lunar seismic" OR "Apollo seismic", newest first, three pages of 25 at
  09:05:39Z-09:05:51Z): 51 records, all reviewed by title and file list. The data-bearing ones from the last 24 months
  are the records above. The others are abstracts, unrelated theory notes or older work.
  - The first attempt with size=100 returned HTTP 400, a page-size validation error and not a block. I re-queried
    with the allowed size.
- **Web searches** (template matching, ML or expanded deep-moonquake catalogues 2025-2026, "A38" nest, GitHub nest
  catalogues):
  - Onodera 2026 GRL (repeating shallow moonquakes): built on the SP catalogue above.
  - Kim et al. 2026 GRL (single-station location): no full-catalogue relocation and no new list.
  - Onodera and Kawamura 2026 (Apollo 17 LSG): no S14 1971 data.
  - Fernando et al. 2026 JGR Planets (impact flashes): no matches.
  - Tamama 2025 (Apollo 17 LSPE): not S14 data.
  - Majstorovic 2024 (classifies catalogued events only).
  - None publishes an expanded deep-moonquake list containing this event or any A38 member on or near 1971-133.
- **Older lists** (outside the bank's 24 months): Bulow et al. 2005/2007 are inside levent.1008weber, and
  Knapmeyer-Endrun and Hammer 2015 covers S16 from 1972 only.
  - Sun et al. 2019 (Earth and Planetary Physics 3, 290) reports one uncatalogued moonquake found by matched filter.
    Only its abstract page was readable, and it gives no time.
  - That paper is outside the 24-month window and is not an expanded list, but it is the one item I could not fully
    rule out.

## 4. Liu, Xiao and Li (2025) acceleration-glitch catalogue (Zenodo 15715187)

- **Archive**: lunar_ACC-v1.0.1.zip, downloaded once at 09:03:26Z (HTTP 200, 109,655,361 bytes).
  - sha256 7278ac65c926e88d14748ee6a2ff32c17fb6fde84b3ecf20fbec5a6fcd12566d and md5 38e162c8...fdcfd match the
    claim and the Zenodo record.
  - This is the only version. The Zenodo versions API (09:09:39Z) lists 1 version, and the GitHub releases list
    v1.0.1 only.
  - Later commits to the GitHub default branch (2025-08-02/04) add a deep-cluster folder and a test dataset. These
    were not in the release and I did not read them.
- **Member hashes**: the nine S14 files match data/glitch_catalogue_record/members_sha256.txt. Their row counts match
  results/glitch_catalogue_survey.json: Spike MH1/MH2/MHZ 52,458 / 50,810 / 28,754; Step-Up 187,802 / 141,474 / 522;
  Step-Down 160,766 / 106,460 / 462.
- **Overlap**: no interval in any of the nine S14 files overlaps the 450 s window, and none overlaps the window +/- 10 min.
  - The nearest after the window are Step-Down MH2 at +1713.2 s, Step-Down MH1 at +3010.5 s, Spike MH2 at +3013.9 s
    and Spike MH1 at +7348.0 s.
  - The nearest before the window are interval ends 32,439 s (about 9 h) or more before the onset.
  - The S12 files have no interval overlapping the window either.
  - So the object is not a relabelled published glitch.
- **Calibration commands**: the archive's command_for_calibration.csv has no S14 LP calibration command near the onset.
  - The nearest S14 commands are 1971-05-13 00:53:12 (17.8 h before, MAP 0) and 1971-05-14 19:06:25 and 19:07:55.
  - The catalogue's MHZ step entries at about 19:06:26.4 and 19:07:54.6 on 05-14 match those two commands within about
    1 s.
  - So the catalogue's time base agrees with absolute time on this date to about 1 s. No hour-scale offset could hide a
    glitch listed elsewhere that really falls in the window.
- **Coverage hole**: I confirmed that the catalogue has no S14 interval of any type on MH1 or MH2 from 09:39:24.5 to
  19:08:37.0 UTC on 1971-05-13.
  - Hours 10-18 are empty on all six MH1/MH2 files, and MHZ is also empty from 10 to 19 h.
  - S12 files do have intervals in those hours, so the hole is specific to S14. It most likely reflects a gap in the
    catalogue authors' S14 input or processing.
  - The catalogue therefore says nothing about glitches in this window. Passing G1 is uninformative, not
    confirmatory.
- **How the claim describes the catalogue**:
  - Accurate: the citation (verified live on Crossref at 09:17:54Z: JGR Planets 130(10) e2025JE009277; authors Liu,
    Xiao, Li), the DOI, the CC BY 4.0 licence, the archive and member hashes, the row counts and the nearest distances.
  - CLAIM.md states the coverage hole as facts. package/README.md "What G1 can and cannot show" also states it
    plainly: G1 does not show that the catalogue's detector covered this stretch, and on its own it is weak evidence.
  - package/object/glitch_catalogue_s14_acc_spike_mh[12]_1971d036-365.csv are verbatim start/end extracts. My
    comparison with the archive gives 9,361 and 11,394 rows, the same multisets.
  - The gate timing (pre-registered after the original panel, with G1 already seen) is disclosed.
  - One wording point for the filer: the one-sentence claim lists G1 as a pass without the coverage caveat, which
    appears only further down. This is not a novelty defect.

## 5. This repository (https://github.com/elder-plinius/V3R1T4S)

- TROPHY_CASE.md (live main, 09:12:48Z, HTTP 200, 100 lines): no Apollo, moonquake, lunar, seismic or A38 entry.
- Tree of main (09:12:52Z, not truncated, 7,438 entries):
  - known-knowns/ has 6,176 entries in 31 folders, with no Apollo, moon, lunar, seismic or quake folder or path.
  - The bank entry is still only at known-unknowns/earth-and-sky/apollo-moonquake-missed-vs-pds-catalog.md, read live
    at 09:13:06Z: "open as of 2026-10-15".
- Issues and pull requests, open and closed, searched through the GitHub search API at 09:13:12Z-09:14:05Z:

| query | results |
|---|---|
| "moonquake" | 0 |
| "apollo" | 0 |
| "lunar" | 0 |
| "A38" | 0 |
| "S14 1971" | 0 |
| "PDS catalog" | 0 |
| "seismic" | 2, both about the unrelated ComCat target (issue #633, PR #785) |
| "gold" (positive control) | 11 |

- No earlier claim covers this event.

## 6. Trivial-edit comparison

- The object is a single event time attributed to a catalogued nest.
- It is seeded from six catalogued 1971 A38 events. The claim names them through frozen/ and the template build.
- No published event row of any nest or type lies within 2 h of the onset. The nearest is the levent stop 120 min
  before it.
- The nearest published glitch interval starts 1713 s (28.6 min) after the onset, well outside the 450 s window.
- So no deletion, restriction, relabelling, re-timing or mis-dating of a published row produces it.
- It is an existence claim, so the tie rule does not apply. The event is absent from everything known, so the claim
  strictly beats everything known.

## Verdict

**novelty: confirmed.** The status source was re-fetched live just before this verdict and is byte-identical to the
claim's copies.

- No dated row of any PDS table is within +/- 5 min of the onset, and the onset lies in no levent span. The nearest row
  stops 120 min before the onset.
- No 2025-2026 list I could find contains this event or any A38 member near 1971-05-13 18:40 UTC.
- The Liu, Xiao and Li (2025) catalogue has no interval in or near the window, in any of its S14 files. The object is
  not a relabelled published glitch.
- The claim describes that catalogue, and its own relation to it, accurately, including the coverage hole that makes
  G1 uninformative.
- This repository holds no earlier claim of this event.

Limits:

- Sun et al. 2019 was read at abstract level only.
- The 1.5 GB training archive of Zenodo 22741655 was read by its file listing only.
- Unreleased detection outputs cannot be searched.
- This verdict covers novelty only.

pass: true
