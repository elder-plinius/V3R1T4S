# Record compared against

- Status source: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ fetched live by
  the NOVELTY panelist 2026-11-13T17:30:46Z, HTTP 200, 4211 bytes, sha256
  593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f (equal to the claimant's fetch of 16:15:33Z). The index
  lists 12 CSV tables; all 12 fetched 17:30:59-17:31:42Z, HTTP 200, each byte-identical to the claimant's 16:15-16:16Z copies.
- Table: levent.1008weber.csv fetched 2026-11-13T17:31:07Z, HTTP 200, 890253 bytes, sha256
  f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c (13,057 rows).
- Extracted cell: catalogue rows near 1973-10-30 02:25:51.5 UTC. Day 73-303 holds 01:00-02:00 (A1), 05:22-06:00 (C,
  meteoroid impact), 07:39-08:10 (A8), 22:06 (M) and 23:42 (A285). The nearest row starts 85.9 min before the onset and
  stops 25.9 min before it. No row of any table lies within +/- 5 min of the onset or the window start, and no
  start-stop span contains them.
- Published lists also checked: Knapmeyer-Endrun and Hammer (2015) Tables S1-S3 (Apollo 16, 1972-05-06 to 1975-06-27;
  nearest 1973-10-26 09:06:07.6, -89.3 h); Bulow, Johnson and Shearer (2005) Table 2 (nearest 1973-11-05 05:03,
  +146.6 h); Onodera SP windows (Zenodo 8373651; nearest S16 06:06, +220.1 min); Shi, Li and Wang (2025) catalogues
  (Zenodo 15420872 and 16809589; nearest the catalogued A1 event); one 2026 GitHub machine-learning scan of the Apollo
  archive (nearest S16 detection +62.3 h): no row within +/- 5 min (panel/novelty.md).
- Glitch catalogue (Liu, Xiao and Li 2025, lunar_ACC v1.0.1, Zenodo 15715187): no Spike, Step-Up or Step-Down
  interval on MH1, MH2 or MHZ overlaps the S14 or the S16 window (how-we-built-it/results/glitch_gates_A100_1030.json;
  file hashes in how-we-built-it/glitch_catalogue_SHA256SUMS.txt).
