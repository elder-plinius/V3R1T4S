# The record we beat

## coveringrepository.com, plain (v,k,t) table
- URL: https://coveringrepository.com/download_archive_vkt.aspx (tab-separated rows "v k t m (empty) blocks"; every
  row has m = t).
- Fetched 2026-10-15T23:10:40Z by the run (curl, User-Agent "V3R1T4S-research-agent (curl)", one request), HTTP 200,
  171741 bytes, sha256 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17.
- Fetched again 2026-10-16T02:08:27Z by the NOVELTY panelist (one request), HTTP 200, same size and sha256.
- Extracted cell (tabs written as [TAB]): `53[TAB]20[TAB]03[TAB]03[TAB][TAB]35`.

## La Jolla Covering Repository (D. M. Gordon)
- https://dmgordon.org/covering-designs/ fetched 2026-10-15T23:10:44Z and by NOVELTY at 2026-10-16T02:08:31Z, HTTP 200,
  sha256 a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3: no per-cell values; links to
  coveringrepository.com and the Zenodo dataset.
- Zenodo: https://zenodo.org/api/records/19472830/versions/latest answered 301 to records/19735294 (version 1.2,
  published 2026-04-24; fetched 2026-10-15T23:12:39Z and by NOVELTY at 2026-10-16T02:08:31Z, HTTP 200). Its
  coverdata.json (8319503 bytes, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87) has
  "C(53,20,3)": size 35, low_bd 30, history [35, "Simple construction from (54,20,3)", LJCR, 2009-01-21 20:06:16].
- GitHub dmgordo/LJCR coverings/coverdata.json (last commit 2022-12-19T18:10:24Z; 6517686 bytes, sha256
  0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef): "C(53,20,3)": size 35, low_bd 30.
