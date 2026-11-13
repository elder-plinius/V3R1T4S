# Record compared against

## PDS Apollo seismic event catalogue (status source)

- Status source: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ fetched
  2026-11-12T23:17:17Z for the original claim, HTTP 200, 4211 bytes, sha256
  593e03154b8cc632dca240575d6e3b17f2c05fb464a3915b45e56804bcca2e2f; fetched again for this rebuild at
  2026-11-13T08:39:57Z, HTTP 200, 4211 bytes, same sha256.
- Table: levent.1008weber.csv (and the other dated tables of that directory), fetched 2026-11-12T21:04:14Z, HTTP 200,
  levent sha256 f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c; re-fetched by the original NOVELTY
  panelist at 2026-11-12T23:49Z (byte-identical) and for this rebuild at 2026-11-13T08:40:01Z, HTTP 200, 890253 bytes,
  same sha256.
- Re-fetched live by this package's NOVELTY panelist (panel/novelty.md) just before its verdict: the index at
  2026-11-13T09:18:15Z, HTTP 200, 4211 bytes, same sha256; all 12 CSV tables at 09:18:20Z to 09:19:17Z, HTTP 200, each
  byte-identical to the copies used (levent.1008weber.csv sha256 f95743b280692b81299b23fecf25979fb96a67f7717f85399fa859c0a0b9b93c).
- Extracted cell: catalogue rows near 1971-05-13 18:40 UTC: nearest levent 71-133 1603 T2=C N2=nan (157.1 min away;
  its stop time, 16:40, is 120 min before the onset); none within +/- 5 min, none whose start-stop span contains the
  onset.

## Acceleration-glitch catalogue (Liu, Xiao and Li 2025)

- Record: https://zenodo.org/api/records/15715187 (doi:10.5281/zenodo.15715187) fetched 2026-11-13T08:32:05Z, HTTP 200:
  version v1.0.1, published 2025-06-22, licence cc-by-4.0, one file lunar_ACC-v1.0.1.zip, 109655361 bytes, md5
  38e162c8e4407e750de3c5cb126fdcfd.
- Archive fetched 2026-11-13T08:32:39Z to 08:33:09Z, HTTP 200, 109655361 bytes, md5 38e162c8e4407e750de3c5cb126fdcfd,
  sha256 7278ac65c926e88d14748ee6a2ff32c17fb6fde84b3ecf20fbec5a6fcd12566d.
- Files used by the gates: catalogs/S14_ACC-Spike_MH1_all.csv, sha256
  78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1, and catalogs/S14_ACC-Spike_MH2_all.csv, sha256
  1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9. Both are byte-identical to the copies the gate run
  used, which were fetched from the code repository behind the record on 2026-11-13T05:29:30-32Z.
- Paper: https://doi.org/10.1029/2025JE009277 (metadata read from https://api.crossref.org/works/10.1029/2025JE009277
  at 2026-11-13T08:44:58Z, HTTP 200: Journal of Geophysical Research: Planets 130(10), e2025JE009277, published
  online 2025-10-16).
- Extracted cell: intervals of S14 ACC-Spike MH1/MH2 overlapping the 450 s window from 1971-05-13 18:39:33.735 UTC:
  none. The nearest spikes start 3013.925 s (MH2) and 7347.963 s (MH1) after the onset. Descriptive: no interval of
  the other seven S14 files overlaps the window, and there is no MH1/MH2 interval of any type from 09:39:24.528 to
  19:08:36.981 UTC that day.
