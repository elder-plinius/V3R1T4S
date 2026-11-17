# NOVELTY skeptic: apollo-moonquake-missed-vs-pds-catalog, A100-like event on S14 + S16 at 1973-10-30 02:25:51.5 UTC

context: fresh subagent started with the Claude Code Agent tool (subagent_type novelty), separate context; it saw only claim/ plus the outside sources named below. It did not read attempts/, PREREG.md at the run root, panel/ (other skeptics) or other roles' panel_work folders.

Verdict: novel. No row of any table in the live PDS catalogue directory and no published event list (including the only deep-moonquake event catalogues of the last 24 months that I could find) lies within +/- 5 min of the onset or window start, and no listed span contains them. The earlier package 2026-11-13-[credit]-9ff1c507 mentions this event only as "not claimed". This claim is a distinct, additional object, not a replacement or a relabelling.

Scope: novelty only. I did not recompute the detection, the null or the gates; those belong to the other two skeptics.

Times checked (from claim/CLAIM.md and claim/results/r6_check_1030.txt): onset 1973-10-30T02:25:51.509Z; window start 1973-10-30T02:25:21.509Z. Tolerance +/- 5 min, plus "a listed start-stop span contains the time".

## 1. Live status source, fetched once per file (no retries)

Each file was fetched once with curl, with a User-Agent naming V3R1T4S, about 3-4 s apart. UTC times are from `date -u`. Base URL: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/

| UTC | file | HTTP | bytes | sha256 |
|---|---|---|---|---|
| 2026-11-13T17:30:46Z | data/ (index) | 200 | 4211 | 593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f |
| 2026-11-13T17:30:59Z | collection_data_inventory.csv | 200 | 874 | 760f8db68daca4f7e374ccb61e9ed4eced5efd5ab829603035b3b7ce0e18946a |
| 2026-11-13T17:31:03Z | gagnepian_2006_catalog.csv | 200 | 3405 | e79df3f30efa927d730f873085a7b60307c4e94913a1e5584489d6d6f6c14459 |
| 2026-11-13T17:31:07Z | levent.1008weber.csv | 200 | 890253 | f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c |
| 2026-11-13T17:31:11Z | lognonne_2003_catalog.csv | 200 | 5832 | 3c78c5b130e521193e581e8a63ff9254ffe3251f072d9fcd0c62eb35e7bc3d1d |
| 2026-11-13T17:31:15Z | nakamura_1979_sm_locations.csv | 200 | 933 | 151307757fd66017c3e71dda2db27be4f27c58012a869b56763c0305d86759b5 |
| 2026-11-13T17:31:19Z | nakamura_1983_ai_arrivals.csv | 200 | 430 | e3e3b102ed4e9b74d1694268b57bbe83e6115217570a432883526b745c4e2541 |
| 2026-11-13T17:31:23Z | nakamura_1983_ai_locations.csv | 200 | 330 | f3fa3ce4837c4d5ad355a189968e25cb974fba9c4da84dbbf41f59d2fb459776 |
| 2026-11-13T17:31:26Z | nakamura_1983_m_arrivals.csv | 200 | 2717 | 63fe558b00830850b52265e0345bf32d7999789ebcca8959d9937e8e1f56ae8b |
| 2026-11-13T17:31:30Z | nakamura_1983_sm_arrivals.csv | 200 | 2128 | 221c34ea914663397a2e01d2be6ed5c1ed2669f4bfbbb6019f1de9bb50760b4b |
| 2026-11-13T17:31:34Z | nakamura_2005_dm_arrivals.csv | 200 | 4708 | 2c677fe71e618c77b81d7f01752f8f0e5bbc2c57dd6511cf82a0b2e08c57c4e1 |
| 2026-11-13T17:31:38Z | nakamura_2005_dm_locations.csv | 200 | 3651 | 539e3c6481c1050c78d7dc0042ceb0036c8173fd56ef46db0ebab76a7d58d485 |
| 2026-11-13T17:31:42Z | weber_2011_dmq_s_picks.csv | 200 | 670 | 1374ea5645d90207390d2492f801da944c605a77f52d8c11a29637323e70da0f |

- The index lists 12 CSV tables, each with an XML label. All 12 tables were fetched. levent.1008weber.csv has 13,057 data rows. Server dates in the index are 2018-2020, so the directory is unchanged.
- Every sha256 above equals the claimant's fetch at 16:15-16:16Z (claim/data/fetch_log.tsv). The tables have not changed since the claimant checked them.
- My own check (panel_work/novelty/code/proximity_check.py, output panel_work/novelty/out/proximity_final.txt, run at 17:33:16Z, two minutes after the fetch):
  - Parsing: levent start and stop times, including stops after midnight and 9999 (unknown) stops. Gagnepian and Lognonne YYMMDDHHMM dates. Nakamura 1979 and 1983 dated rows. A raw text scan of every table for 1973 day 303/304 or 1973-10-30 patterns.
  - Results: 0 hits at the onset and 0 at the window start, in every dated table. No levent span contains either time.
  - Nearest row: levent 73-303 0100, T2 = A, N2 = 1 (nest A1). It starts 85.9 min before the onset and stops 25.9 min before it, at 02:00. Next is levent 73-303 0522 (C), starting 176.1 min after the onset.
  - The 3 malformed Lognonne dates have year prefixes 76, 77 and 72, so none can be 1973.
  - Four tables have no event times (inventory, AI arrivals, Nakamura 2005 nest arrivals and locations, Weber 2011 S picks).

## 2. Published event lists, read with my own code

| list | reader | rows | nearest to the onset | hits within 5 min or span |
|---|---|---|---|---|
| Knapmeyer-Endrun and Hammer 2015, Tables S1-S3 (claim/data/lit/knapmeyer2015/*.xls) | own BIFF8/OLE2 reader (xls_read.py) | 287 dated + 3 with no date | 1973-10-26 09:06:07.6 (-89.3 h, -5359.7 min) | 0. The three undated rows have times of day 357.0, 1270.7 and 1213.1 min from the onset's, so they cannot match on any date |
| Bulow et al. 2005, Table 2 (claim/data/lit/bulow2005/bulow_jgr05.pdf) | pypdf text plus own regex | 123 (the paper states 123); 18 in 1973 | 1973 day 309 05:03 (+8797.1 min, +146.6 h) | 0 |
| Onodera SP event windows, Zenodo 8373651 (claim/data/lit/onodera_*.csv) | own CSV parser; the 15 rows with NaT times count as whole-day windows; none is in 1973 | 28,976 | S16 id 2014, 06:06-06:50 (+220.1 min) | 0 |
| Shi, Li and Wang 2025, individual deep-moonquake catalogues, Zenodo 15420872 (v1, 2025-05-15) and 16809589 (latest, 2025-08-12), fetched 17:24-17:33Z | own xlsx reader | 722 rows over 6 catalogues | levent A1 event 1973-303 01:00 (-85.9 min) | 0 |

- All three Onodera CSV md5s equal the md5s listed by the live Zenodo record. The record has one version.
- The Shi et al. catalogues are within 24 months. By their own readmes they hold catalogued levent.1008c events matched in windows around the catalogued onsets, and their 1973-10-30 row is the catalogued A1 event.
- My numbers agree with claim/results/kn_check_1030.txt, bulow_check_1030.txt and r6_check_1030.txt.

## 3. Literature and code search, 2024-11 to 2026-11

Searches covered journals, arXiv, Zenodo, GitHub (repositories, code search and release assets) and conference abstracts. I found no expanded deep-moonquake list, and no template-matching or machine-learning catalogue of new Apollo deep moonquakes, from the last 24 months. Items found and what they contain:

- Shi, Li and Wang 2025, JGR Planets (S-wave splitting). Checked in section 2. Subset of levent.
- Liu, Xiao and Li 2025, JGR Planets (acceleration glitches; Zenodo 15715187). Glitches, not events. The claim uses it as a gate.
- Turner et al. 2025, JGR Planets, e2024JE008739. Statistics to separate shallow moonquakes from impacts, using events already catalogued. Not a deep-moonquake list.
- Tamama et al. 2025 and Civilini et al. 2023. Apollo 17 LSPE thermal moonquakes, 1976-77. Not relevant to S14 and S16 in 1973.
- Onodera 2026, GRL. Repeating shallow moonquakes: one pair (KO-26/KO-40) from the Onodera 2024 SP catalogue, which section 2 checks. Not deep.
- Kim, Song and Schmerr 2026, GRL. Single-station location of example and catalogued events. No new event list found.
- Al-Qadasi and Bin Waheed 2026, Earth and Space Science (Fourier neural operator detector). Evaluated on catalogued PSE and LSPE examples; its data statement points to training and test data, not a new catalogue. The Wiley full text returned HTTP 403; not retried.
- Majstorovic et al. 2024 (JGR Machine Learning and Computation) and EGU24-8297. Nest classification of catalogued events.
- A 2026 study, "Orbital modulation of frequency content in Apollo deep moonquake records". Spectral stacks of existing clusters.
- GitHub repository planetary-seismic-triage (created 2026-07-10). An ML archive scan of S12, S15 and S16, with screened detection lists and catalogue-extension candidates; its own write-up says the gate failed. I fetched each file once.
  - Nearest S16 detection: 1973-11-01 16:45:35 (62.33 h after the onset).
  - Nearest S12 / S15 detections: 850.48 h and 473.26 h away.
  - No candidate within days.
  - Its release assets (2026-07-18) predate its archive scan (2026-07-25), so they cannot hold a newer list.
- GitHub code search for "1973-10-30" found nothing seismological. A repository search for "moonquake" found nothing that lists new 1973 events.

## 4. This repository

- TROPHY_CASE.md: no Apollo or moonquake entry. Checked in the pinned copy (commit of 2026-11-03) and on the upstream default branch (0 matches).
- known-knowns/: no apollo-moonquake folder, in either the pinned copy or upstream main.
- Pull requests of the upstream repository, open and closed, searched for "moonquake", "apollo", "1973-10-30", "A100", "lunar seismic" and "deep moonquake":
  - The only PRs on this target are 4 open drafts by the claimant, all created 2026-11-13: #1076 (p2, A1 1971), #1077 (p1, A39 1971), #1083 (full criterion, 1973-11-26) and #1084 (p1, A38 1971).
  - No PR by anyone claims 1973-10-30, and there are no issues on the target.
- PR #1083 (draft, unmerged, created 2026-11-13T11:27:12Z) is the earlier package 2026-11-13-[credit]-9ff1c507. Its body and README say: "A second A100-like event (1973-10-30 02:25:51.5 UTC) also meets R7, R8 and R9 and is not part of this claim", and "would need its own gates and panel". Its file how-we-built-it/results/r8_att_A100_1030.txt contains this event's R8 line (0.71 s against the median 0.82 s), the same as claim/results/r8_att_A100_1030.txt.

## 5. Prior work: is this object already claimed, and is it distinct?

- Already published or claimed? No.
  - The only public mention is the claimant's own disclosure in an unmerged draft PR, which says explicitly that the event is not claimed.
  - That disclosure is not a claim, not a third-party publication, and not "a published expanded deep-moonquake list". Priority stays with the claimant.
  - The claim names that package (claim/CLAIM.md, claim/data/prior_work/).
- Distinct object? Yes.
  - It is a different time-series segment. The onsets are 27.223 days apart (1973-10-30 02:25:51.509 and 1973-11-26 07:46:28.641), and neither lies within 5 min of the other.
  - It has its own values: Dt 0.298 against 0.343; S14 MH2 0.621 and S16 MH1 0.620, against 0.562 and 0.699; R8 0.71 s against 0.93 s.
  - The earlier package's INDEX row is still 1973-11-26 only (claim/data/prior_work/package_9ff1c507_INDEX.csv). So this claim is additional, not a replacement and not a relabelling.
- What the two claims share: the claimant; the scan (lens lagtol-s14s16-1973, PREREG.v15); the frozen 5-member A100 S14 + S16 stack; the Dt statistic; the same 401-control A100 null (C0 0.157, best shift 0.191); the readings of R7 (best single channel per station), R8 and R9; the PDS waveforms; the glitch catalogue; and the explanation that S16 MH2 was unresponsive, so S16 rests on MH1 in both claims.
  - They also resemble each other: the 11-26 event scores 0.402 against this event's window (claim/CLAIM.md, C6).
  - So they are not independent confirmations, as the claim itself states.
- Trivial-edit test: the object is a detection in data at a new time. Deletion, restriction, relabelling, symmetry, polishing or a propagation rule applied to any catalogued row, or to the 11-26 event, cannot produce it.
  - Propagating 11-26 back one anomalistic month (27.5546 d) gives 1973-10-29 18:27:51, about 8 h off. In any case such a step gives only a time to search, not a detection.
  - Nothing known lies at this time, so the object strictly beats everything known. A tie is not possible for a discovery that is absent from every list.

## 6. Caveats (these do not change the novelty verdict)

- The event starts 25.9 min after the listed stop of the catalogued A1 event 73-303 0100.
  - The claimant's claim/results/coda_profile_1030.txt shows that event decaying to about 1.0 by 02:05-02:20, then a new rise to about 1.4-1.6 at 02:25. I read this but did not recompute it.
  - If another skeptic found the signal to be that event's coda, it would be a catalogued event in substance. That is a question about whether the event is real and correctly attributed, not about the catalogue.
- I parsed the Knapmeyer-Endrun and Hammer tables as supplied in claim/data/lit (obtained by hand from the publisher) and did not re-download them. The publisher's site refused automated access earlier. My count of 290 rows matches the 290 stated in PR #1083.
- Wiley returned 403 on one full text (Al-Qadasi and Bin Waheed 2026). Its content is judged from the data statement and abstracts.
- I did not re-download the latest-version copies of Shi et al. files 2 and 5. Their v1 copies and the four latest-version catalogues were checked, and all are built from levent onsets by design.

injection_suspected: none

Files (relative to the run folder): panel_work/novelty/live_pds/ (live tables, index, fetch_log_novelty.tsv); panel_work/novelty/code/ (xls_read.py, xlsx_read.py, pdf_text.py, proximity_check.py); panel_work/novelty/out/proximity_final.txt (sha256 d20fc92a870338d9566333b130a7e96aa2030fa1e78272ced2cdf21aa04a9bb0); panel_work/novelty/dl_web/ (Zenodo records, Shi et al. catalogues, planetary-seismic-triage files).

pass: true
