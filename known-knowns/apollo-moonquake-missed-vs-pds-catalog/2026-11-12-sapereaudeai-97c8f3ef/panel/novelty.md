# Panel: NOVELTY skeptic

context: subagent (fresh context, Claude Code Agent tool, subagent_type novelty)

target: apollo-moonquake-missed-vs-pds-catalog
claim judged: partial win p2 (claim/CLAIM.md). A detector built from 1972 data (S12 MH1/MH2/MHZ, stack of 21 aligned 1972 A1 events) runs blind over the whole of 1971. At a frozen theta = 0.10898 it recovers 63 of 67 catalogued 1971 A1 events (T2 = A, N2 = 1 in levent.1008weber.csv). Its measured false-alarm rate is 1.196 per scanned day (400 time-reversed detections over 334.54 scanned day-equivalents). Files: results/p2.json, results/p2.md, frozen/A1_s12_dev1972_templates.npz, code/scripts/score_p2.py.

novelty: CONFIRMED for p2 as worded (no published object found that meets the p2 bar or makes this one a trivial edit). Recall alone is not a record (see "Neighbouring cells" below).

## Status source (one honest request each, User-Agent naming V3R1T4S, no retries)

- URL: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/
  - fetched 2026-11-12T21:07:16Z, HTTP 200, 4,211 bytes, sha256 593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f. This is byte-identical to the scout's 18:42:41Z copy (data/catalog_data_index.html).
  - value read: levent.1008weber.csv 890,253 bytes, dated 6/4/2019 8:06 AM (label 10/13/2020). The other tables (gagnepian_2006, lognonne_2003, nakamura_1979/1983/2005, weber_2011) are dated 2018-2020. Nothing changed.
- Primary table re-fetched live: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/levent.1008weber.csv
  - fetched 2026-11-12T21:15:48Z, HTTP 200, 890,253 bytes, sha256 f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c. This is identical to data/catalog/levent.1008weber.csv.
  - my own count: 443 A1 events in total, 67 of them in 1971 (per year: 1969 7, 1970 58, 1971 67, 1972 54, 1973 57, 1974 41, 1975 43, 1976 57, 1977 59). This matches the claim's denominator.

## This repository

- TROPHY_CASE.md: the pinned copy and the live raw file are identical (fetched 2026-11-12T21:08:37Z, HTTP 200, 31,306 bytes). Neither has an Apollo, moonquake, lunar or seismic entry.
- known-knowns/: no Apollo, moonquake or lunar folder, either in the pinned copy or in the live GitHub listing (31 entries).
- Pull requests (GitHub web search pages, 2026-11-12 about 21:08Z):
  - is:pr apollo: 0 open, 0 closed
  - is:pr moonquake: 0 open, 0 closed
  - is:pr lunar: 0 open, 0 closed
  - is:pr seismic: 1 open (#785), which is a ComCat claim for a different target
- Issues matching "apollo OR moonquake": 0.
- The only Apollo item in the repo is the target's own known-unknowns page.

## Literature and code (last 24 months searched, plus the classics the catalogue builds on)

The cell is one nest (A1), one year (1971), the recall of its catalogued events at a measured false-alarm rate, by a saved, re-runnable detector. I found no published object in that cell. The nearest objects:

- **Bulow, Johnson and Shearer 2005 (JGR 110, E10003).** A blind cross-correlation scan for A1 found 123 new events next to 323 catalogued.
  - Per search snippets of the paper (Table 1), their selection keeps 17-71% of catalogued A1 events on the horizontal-channel stacks and at most 39% on the vertical. The re-identification of known A1 events is said to be "in good agreement" with those percentages.
  - No false-alarm rate per day was found.
  - The full text could not be read: the UCSD PDF gave a connection reset; Wiley and Semantic Scholar returned 403. Each was tried once, with no retry.
  - Bulow et al. 2007 (JGR 112, E09003) found 503 new events in 8 nests. No per-nest recall or false-alarm rate was found.
- **Nakamura 2003 (PEPI) and 2005 (JGR).** These cross-correlate catalogued events against each other. They are not blind detectors with a false-alarm rate.
- **Shi, Li, (Zhang), Meng: Zenodo 10.5281/zenodo.18476476 (v2, 2026-02-04) and 10.5281/zenodo.22113858 (v3, 2026-08-26), CC BY 4.0.** This is the closest recent object. I downloaded IndividualEventsAndArrivalTimesFromMatchedFilter.xlsx once (60,500 bytes, sha256 d7bb62d4931e03493a31bd61b7f2144f4766c8b4e2a2a6ffd5d1ed6618063425) and parsed it with my own script.
  - It has 2,604 rows of (cluster, station, catalogue minute, Ts), including 373 A1 rows on S12.
  - All 914 A1 rows fall within +/-5 min of a catalogued A1 event, and none fall outside. All 65 S12 rows for 1971 sit exactly on the catalogue start minute. So the list is an arrival-time measurement keyed to catalogue times, not a blind scan, and it reports no false-alarm rate.
  - On S12 in 1971 it covers 65 of 67 catalogued A1 events (97.0%), and 34 of 67 on S15. That includes the four events the claim misses (1971-08-06 07:20, 09-27 04:00, 09-30 20:33, 12-18 20:41). It lacks 1971-08-15 05:11 and 10-29 01:42.
- **Li, Wang, Yu, Shi: Zenodo 10.5281/zenodo.22741655 (v2, 2026-09-14).** GitHub lijialongnju/Lunar_Seismology has 2 commits and no releases.
  - code.zip (61,014 bytes, md5 e84a2669f06e2eaea039eae7429bd79b) was listed but not run. It holds STA/LTA plus a MultiRocket deep-moonquake versus impact classifier.
  - It is class-level, with no per-nest recall or false-alarm rate published in the record.
- **planetary-seismic-triage (GitHub, 2026; results/archive_scan/B3_FINDINGS.md).** An S12 archive scan with class-level deep-moonquake recall 0.522 (1849/3544) at 15.4 unmatched detections per station-day (threshold 0.10 / 120 s). It is not nest-specific.
- **Knapmeyer-Endrun and Hammer 2015 (JGR Planets).** A hidden Markov model detector on S16: 78% of deep moonquakes detected, 23% of deep-moonquake detections false.
- **Not detection, or not deep moonquakes:**
  - Majstorovic et al. 2024 (JGR ML&C) classifies nests from orbital parameters.
  - LPSC 2022 #2393 is a CNN classifier for A1/A8 at 70.1% or less.
  - Al-Qadasi and Waheed 2026 (ESS) is a Fourier neural operator detector, class-level, with F1 0.75-0.85.
  - Kim et al. 2026 (GRL) is single-station location.
  - Onodera 2024 (JGR Planets, Zenodo 8373651) and 2026 (GRL) work on short-period and shallow events.
  - Turner et al. 2025 covers shallow events and impacts; Tamama et al. 2025 covers thermal events.
  - None of these gives a one-nest, one-year recall at a measured false-alarm rate.

## Trivial-edit test

- The object is a blind, full-year scan. Its detections come from the scan's forward peaks: code/scripts/score_p2.py reads fwd_peaks from the scan file and does not read catalogue times as detections. Its templates and threshold were fixed on 1972 data.
- It is seeded from the published catalogue (data/catalog/levent.1008weber.csv, 1972 A1 times), and it names that catalogue.
- No deletion, restriction, relabelling, symmetry, propagation rule or numerical polish of any published list yields a false-alarm rate measured on a blind scan:
  - not of the catalogue;
  - not of the Shi et al. targeted list, which has no detections outside catalogue minutes and so no false-alarm operating point;
  - not of Bulow 2005.

## Neighbouring cells, stated plainly for the gate

- Published operating points that carry a false-alarm measure are all below the claim's 0.940 recall at 1.196 per day:
  - class-level S12 scan: 0.522 at 15.4 per day;
  - hidden Markov model: 78% detected, 23% false;
  - Bulow per-channel: 17-71%.
- The only higher figure for the same nest, year and station is the Shi et al. targeted list (65/67 = 0.970 on S12). It has no false-alarm rate and is not a detector operating point, so it is not a p2 object and the claim is not a trivial edit of it.
- Recall by itself is therefore not a record. The claim is new as a p2 package: at least 90% recall of one nest-year from a blind detector with a measured false-alarm rate, saved and re-runnable. No such package was found anywhere.

## Verdict

The status source was read (unchanged since 2020). The repo has no prior entry, PR or issue on this target. The literature of the last 24 months and the classic papers contain no published one-nest, one-year recall of at least 90% at a measured false-alarm rate. No published object gives this one by trivial edits.

pass: true
