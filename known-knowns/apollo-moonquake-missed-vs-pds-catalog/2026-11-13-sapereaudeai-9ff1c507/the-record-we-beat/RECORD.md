# Record compared against

- Status source: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ fetched live by
  the NOVELTY panelist 2026-11-13T09:40:32Z, HTTP 200, 4211 bytes, sha256
  593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f (equal to the claim's copy of 04:29:26Z). The index
  lists 12 CSV tables; all 12 fetched 09:40:36-09:41:22Z, HTTP 200, each byte-identical to the claim's 04:29-04:30Z copies.
- Table: levent.1008weber.csv fetched 2026-11-13T09:40:44Z, HTTP 200, 890253 bytes, sha256
  f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c (13,057 rows).
- Extracted cell: catalogue rows near 1973-11-26 07:46:28.6 UTC. Day 73-330 holds 02:34 (A1), 04:48 (A20), 05:49 (A252),
  06:36-07:05 (A203) and 14:38-16:20 (A51). The nearest row starts 70.5 min before the onset and stops 41.5 min before it.
  No row of any table lies within +/- 5 min of the onset or the window start, and no start-stop span contains them.
- Published lists also checked: Knapmeyer-Endrun and Hammer (2015) Tables S1-S3 (Apollo 16, 1972-05-06 to 1975-06-27;
  nearest 1973-11-28 14:40:37.5, +54.9 h); Bulow, Johnson and Shearer (2005) Table 2 (nearest 1973-12-02 22:36);
  Onodera SP windows (Zenodo 8373651; nearest S14 08:24, +37.5 min); Yu 2025 (Zenodo 14781554), Shi, Li and Wang 2025
  (Zenodo 16809589), Yang and Zhang 2026 (Zenodo 23610362), Nunn et al. 2020 supplement (Zenodo 7787610): no row within
  +/- 5 min (panel/novelty.md).
- Glitch catalogue (Liu, Xiao and Li 2025, lunar_ACC v1.0.1, Zenodo 15715187, release zip md5
  38e162c8e4407e750de3c5cb126fdcfd equal to the record, read 2026-11-13T09:12:31Z): no Spike, Step-Up or Step-Down
  interval on MH1, MH2 or MHZ overlaps the S14 or the S16 window (how-we-built-it/results/glitch_gates_A100.json;
  file hashes in how-we-built-it/glitch_catalogue_SHA256SUMS.txt).
