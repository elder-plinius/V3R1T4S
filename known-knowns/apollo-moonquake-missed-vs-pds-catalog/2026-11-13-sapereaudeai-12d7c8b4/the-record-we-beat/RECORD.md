# Record compared against

- Status source: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ fetched
  2026-11-13T05:52:08Z, HTTP 200, sha256 593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f.
- Table: levent.1008weber.csv re-fetched 2026-11-13T05:52:09Z, HTTP 200, sha256 f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c (the 10 other tables of that
  directory fetched 05:15:22-05:16:01Z); all 11 tables re-fetched by the NOVELTY panelist at
  2026-11-13T05:57:47-05:57:55Z, byte-identical.
- Extracted cell: catalogue rows near 1971-09-05 01:26 UTC: nearest levent 71-246 2257 T2=A N2=1 (1589.2 min away); none within +/- 5 min, none
  whose start-stop span contains the onset.
- Glitch catalogue (Liu, Xiao and Li 2025, Zenodo 15715187, S14 ACC-Spike MH1/MH2): no interval overlaps the window;
  nearest spike start +1487 s (MH1) from the onset (how-we-built-it/glitch_gates_A39.json).
- NOVELTY also found no overlap in the Step-Up and Step-Down files (MH1, MH2, MHZ) or the Spike MHZ file of that
  catalogue (fetched 06:00:01-06:00:15Z).
- levent has no rows from 1971-09-03 22:57 to 1971-09-06 19:12 (days 247-248 empty); the absence is partly a
  catalogue-coverage gap. S14 and S12 data exist on day 248.
