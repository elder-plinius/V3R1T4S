# NOVELTY panel verdict: apollo-moonquake-missed-vs-pds-catalog (full criterion)

object: one event, onset 1973-11-26T07:46:28.641Z (template window start 07:45:58.641Z), Apollo S14 and S16, claimed as a new member of nest A100 (claim/CLAIM.md)
question: is any event within +/- 5 min (or a span containing the onset or window start) already listed in the live PDS catalogue tables or in any published event list, including expanded deep-moonquake lists from the last 24 months?
context: subagent (fresh context, Claude Code Agent tool, subagent_type novelty)
verdict written: 2026-11-13T09:42Z. Checks ran 09:28-09:42Z. All code is mine: panel_work/novelty/code/ (my own BIFF8 and xlsx readers, R6 checker, fetch script); outputs are in panel_work/novelty/out/.

## 1. Live fetch (immediately before this verdict)

I made one GET per URL with User-Agent "V3R1T4S-novelty-skeptic/1.0 (claim verification; one request per URL; no retries)", 3 s apart, with no retries. The full log is panel_work/novelty/dl_pds_live/fetch_log.tsv. The base URL is https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/

| UTC (date -u) | file | HTTP | bytes | sha256 |
|---|---|---|---|---|
| 09:40:32Z | data/ (index) | 200 | 4211 | 593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f |
| 09:40:36Z | collection_data_inventory.csv | 200 | 874 | 760f8db68daca4f7e374ccb61e9ed4eced5efd5ab829603035b3b7ce0e18946a |
| 09:40:40Z | gagnepian_2006_catalog.csv | 200 | 3405 | e79df3f30efa927d730f873085a7b60307c4e94913a1e5584489d6d6f6c14459 |
| 09:40:44Z | levent.1008weber.csv | 200 | 890253 | f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c |
| 09:40:49Z | lognonne_2003_catalog.csv | 200 | 5832 | 3c78c5b130e521193e581e8a63ff9254ffe3251f072d9fcd0c62eb35e7bc3d1d |
| 09:40:53Z | nakamura_1979_sm_locations.csv | 200 | 933 | 151307757fd66017c3e71dda2db27be4f27c58012a869b56763c0305d86759b5 |
| 09:40:57Z | nakamura_1983_ai_arrivals.csv | 200 | 430 | e3e3b102ed4e9b74d1694268b57bbe83e6115217570a432883526b745c4e2541 |
| 09:41:01Z | nakamura_1983_ai_locations.csv | 200 | 330 | f3fa3ce4837c4d5ad355a189968e25cb974fba9c4da84dbbf41f59d2fb459776 |
| 09:41:05Z | nakamura_1983_m_arrivals.csv | 200 | 2717 | 63fe558b00830850b52265e0345bf32d7999789ebcca8959d9937e8e1f56ae8b |
| 09:41:09Z | nakamura_1983_sm_arrivals.csv | 200 | 2128 | 221c34ea914663397a2e01d2be6ed5c1ed2669f4bfbbb6019f1de9bb50760b4b |
| 09:41:13Z | nakamura_2005_dm_arrivals.csv | 200 | 4708 | 2c677fe71e618c77b81d7f01752f8f0e5bbc2c57dd6511cf82a0b2e08c57c4e1 |
| 09:41:17Z | nakamura_2005_dm_locations.csv | 200 | 3651 | 539e3c6481c1050c78d7dc0042ceb0036c8173fd56ef46db0ebab76a7d58d485 |
| 09:41:21Z | weber_2011_dmq_s_picks.csv | 200 | 670 | 1374ea5645d90207390d2492f801da944c605a77f52d8c11a29637323e70da0f |
| 09:41:25Z | levent.1008weber.xml (label, for the E=9999 definition) | 200 | 39107 | dedaa62f7580f761f9b02dbf9db9a14acf03c7c0c360ad221faff37fa7ef0eb7 |

- The index lists 12 CSVs, and every one was fetched. The index sha256 equals the claim's 04:29Z copy (claim/data/catalog_data_index.html). All 12 CSVs are byte-identical to claim/data/catalog/.
- I also fetched the bundle root once (09:40:27Z, HTTP 200). It contains only data/, document/, the bundle label, readme and md5, with dates from 2019-2020, so no newer collection exists.
- The label defines E as "stop time in hours and minutes; 9999 if signal continues to next event".

Result of my own parser (panel_work/novelty/out/r6_live_novelty.txt) over the live tables:
- **levent.1008weber.csv** (13,057 rows, all parsed; 888 rows have E = 9999):
  - No start lies within +/- 5 min of the onset or the window start. The check allows +59 s, because the tables give times to the minute only.
  - No start-stop span contains either time. A 9999 span runs to the next event's start, and a stop earlier than the start rolls to the next day.
  - The nearest row is 73-330 06:36-07:05, A203. It starts 70.5 min before the onset and ends 41.5 min before it.
  - The next row is 14:38-16:20, A51.
  - All of 1973 day 330: 02:34 (A1), 04:48 (A20), 05:49 (A252), 06:36 (A203), 14:38 (A51).
- **gagnepian_2006, lognonne_2003, nakamura_1979_sm_locations, nakamura_1983_ai_locations, nakamura_1983_m/sm_arrivals**: no row within +/- 5 min.
  - The nearest of these rows is 1973-12-24 10:03 (gagnepian/lognonne).
  - Three lognonne Date values are malformed in the published file: 761142313, 7704712332 and 721081524. None of them is a 1973-11 date.
- **The other tables carry no event times**: collection_data_inventory, nakamura_1983_ai_arrivals, nakamura_2005_dm_arrivals/locations, weber_2011_dmq_s_picks.
- A generic text scan of every CSV for 731126 or 1973-day-330 patterns finds only the five levent rows listed above.
- **R6 hits: 0.**

## 2. Lists on disk in the claim, checked with my own code

- **Knapmeyer-Endrun and Hammer 2015** (claim/data/lit/knapmeyer2015/, Tables S1-S3, Apollo 16):
  - I parsed the .xls files directly with my own OLE2/BIFF8 reader rather than using the claim's tsv/ extraction.
  - There are 210 + 54 + 26 timed rows. Three undated rows in S2 take the date of the row above.
  - The rows run from 1972-05-06 to 1975-06-27.
  - No row lies within +/- 5 min of the onset or the window start, and no onset-to-onset+duration span contains either time.
  - The nearest row is 1973-11-28 14:40:37.5 (D, LPX, +54.90 h). This matches the claim's statement.
- **Bulow, Johnson and Shearer 2005** (claim/data/lit/bulow2005/, Table 2, 123 new A1 events):
  - The 1973 entries fall on days 10, 34, 36, 50, 155, 172, 175, 183, 187, 202, 309, 336, 337, 338, 338, 339, 350 and 351.
  - There is no day 330 entry. The nearest is day 336 (1973-12-02).
- **Onodera 2023 SP event windows** (claim/data/lit/onodera_S1{4,5,6}_New_MQ_SP.csv):
  - The md5 of each file equals the live Zenodo 8373651 record (S14 e5ec53a0..., S15 094f2138..., S16 72d0e03f...).
  - No window lies within +/- 5 min of either time or contains them. I checked both the date-string and the DOY reading; the published S15 file has DOY/date mismatches.
  - The nearest windows are S14 08:24-09:13 (start 37.5 min after the onset) and S16 13:51-14:25.

## 3. Literature, data and code from the last 24 months (and older public lists), searched 09:29-09:42Z

**Searches run:**
- Web searches covering 2025-2026 expanded or deep-moonquake catalogues, template matching, machine learning, Onodera 2026, A100 and "1973-11-26".
- Zenodo API queries: moonquake, "deep moonquakes", "Apollo seismic", "lunar seismic" catalog, "Apollo passive seismic", "shallow moonquakes", Onodera.
- The arXiv API, for moonquake papers since 2024-11. It returned only 2 unrelated papers.
- GitHub repository search (read-only gh) for moonquake, "deep moonquake", "apollo seismic" and "lunar seismic catalog".

**Event-level lists I downloaded and checked** (one GET each):
- **Yu 2025, Zenodo 14781554** (events_catalog.csv, 273 events, deep moonquakes and impacts): the only 1973-330 row is 01:34-04:33. No hit.
- **Shi, Li and Wang 2025 (S-wave splitting), Zenodo 16809589, the newer version of 15420872**:
  - Files read: 11_CatalogueForDifferentCriteria (4 catalogues, 400 rows), EveCat_IndividualEvents in file 5 (broad band, 118 rows) and in file 2 (low frequency, 207 rows), plus SwaveArrivalTime xlsx (nest stacks, no times).
  - All event times are levent.1008c onsets. There are no A100 rows and no 1973 day 320-339 rows. No hit.
- **Yang and Zhang 2026, Zenodo 23610362** (A01 tidal-modulation release, 228 MB):
  - Its A01 event list (create_moonquake_table.py) has 1973/11/26 02:31:22.480, which is the catalogued A1 event, 5 h 15 min before the onset. No hit.
- **Li, Wang, Yu and Shi 2026, "An Automated Method for Detection and Classification of Deep Moonquakes and Impact Events"** (Zenodo 22734945 v1 and 22741655):
  - The release holds code.zip, which is code only with no detection list, and training_dataset.zip (1.5 GB).
  - I read the training zip's central directory with one ranged GET. It holds 150 deep-moonquake MiniSEED files named by levent row index (evt66-evt13007), 530 noise windows and impacts. These are catalogued events; no event list or new detections are published. No hit.
- **Zenodo 21361572 (2026, ML detector prototype "LunaSeis-1")**:
  - The release explicitly reports negative continuous-scan results and prohibits detection claims. Its tables are levent audits and catalogue-negative background windows.
  - Its only 1973-11-26 06-08 h event row is levent-07354 (06:36, A203). No new-event list. No hit.
- **Zenodo 18773537 (2026, FNO detector)**: code only, with data kept out of the release. No list.
- **Nunn et al. 2020 electronic supplement, Zenodo 7787610** (older than 24 months, checked for completeness):
  - levent.1008c (Nakamura's base catalogue, 13,058 lines) has the same five day-330 rows as the Weber table.
  - Nunn19_LunarCatalog_v1.xlsx: its nearest row on 1973-11-26 is AW25 at 02:31. No hit.

**Papers with no event-level list for this time:**
- Onodera 2026 GRL: a repeating shallow pair taken from the Onodera 2024 set, which is already checked above.
- Onodera and Kawamura 2026 GRL: relocation of 3 shallow moonquakes.
- Kim et al. 2026 GRL: single-station location of catalogued events.
- Villanova and Yokoyama 2026: spectra of catalogued A1/A6/A8/A9/A10.
- Tamama et al. 2025: Apollo 17 LSPE, 1976-77.
- Liu, Xiao and Li 2025: a glitch catalogue, not events. The claim reports no S14/S16 window overlap; that is a criterion matter.

**Search result:** no 2025-2026 expanded deep-moonquake list containing, or coming within +/- 5 min of, this onset was found.

**This repository:**
- In the pinned copy (repo HEAD cf68067, 2026-11-03), TROPHY_CASE.md and known-knowns/ have no Apollo, moonquake or seismic entry. The only match is the open bank entry in known-unknowns/earth-and-sky/apollo-moonquake-missed-vs-pds-catalog.md.
- Pull requests (gh pr list, read-only, state all, at 09:35Z; latest PR #1074 created 08:31Z): searches for moonquake, apollo, lunar, "deep moonquake", PSE and "S14 S16" returned 0 results.
  - seismic: 1 result, #785, a terrestrial ComCat claim for a different target.
  - A100, 1973 and nest: only unrelated claims.
- Issues searched for moonquake and apollo: 0.
- GitHub repositories updated since 2024-11: only hackathon or visualisation apps built on the PDS catalogue, an Apollo 11 (1969) thermal-moonquake supplement, and a crater/seismology exploration repo (<acct>/...). None publishes an expanded deep-moonquake list. The "deep moonquake" query returned no repositories.

**Trivial-edit test:**
- The object is a time-stamped detection, so no deletion, restriction, relabelling or re-timing of a published event gives it. The nearest published event in any list ends 41.5 min before the onset (levent A203). The nearest A100-assigned published events are on other days.
- It is seeded from published objects, the catalogued 1973 A100 events used as the template stack, and claim/CLAIM.md names them.
- It adds a member that none of those lists contain, so it is not a tie with any known event.

## 4. Could not be read, or not read

- **Blocked:** nothing; every request returned 200 or 206.
- One Zenodo search URL returned HTTP 400 (validation error: size=100 exceeds the anonymous limit of 25). It was a parameter error, not a block, and I sent the corrected size=25 query as a different URL.
- **Not downloaded:**
  - The full Zenodo 22741655 training_dataset.zip (1.5 GB, waveforms); only its directory was read.
  - Zenodo 16809589 files 1, 3, 4, 6, 7, 8, 9 and 10: splitting measurements, synthetics (4.8 GB), plotting code and waveform data. The record's event lists are files 2, 5 and 11, all of which I read.
- **Not read directly:** the Bulow et al. 2007 tables (older than 24 months). By the bank's statement its events are in levent.1008weber, which I checked live.
- **Scope:** novelty only. Whether the detection is a real A100 event (the S16 MH2 response, glitches, the null test) is for the CRITERION and REPRODUCE skeptics.
- **injection_suspected:** none observed. Zenodo 21361572 contains an AGENTS.md file, which I did not open or follow.

pass: true
