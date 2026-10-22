# The record we beat

## coveringrepository.com, plain (v,k,t) table
- URL: https://coveringrepository.com/download_archive_vkt.aspx (tab-separated rows "v k t m (empty) blocks"; every
  row has m = t).
- Fetched 2026-10-15T23:10:40Z by the run (curl, User-Agent "V3R1T4S-research-agent (curl)", one request), HTTP 200,
  171741 bytes, sha256 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17.
- Fetched again 2026-10-15T23:26:02Z by the NOVELTY panelist (one request), HTTP 200, same size and sha256.
- Extracted cell (line 8775 of the file, tabs written as [TAB]): `85[TAB]24[TAB]03[TAB]03[TAB][TAB]77`.
- Status page https://coveringrepository.com/ fetched 2026-10-15T23:10:38Z (HTTP 200, sha256
  a6f948b4a052b5d51f893da65f27094d0d39227292a616dac188913b75bda3b6) and by NOVELTY at 2026-10-15T23:26:04Z (HTTP 200):
  "(v,k,t)-covering designs Coverings online: 9.490 / 9.490", "Allowed values: 4 <= v <= 99, 3 <= k <= 25, 2 <= t <= 8".
- An extra request by the CRITERION panelist at 2026-10-15T23:28:41Z was answered with HTTP 403 (a Cloudflare block
  page) and was not retried.

## La Jolla Covering Repository (D. M. Gordon)
- https://dmgordon.org/covering-designs/ fetched 2026-10-15T23:10:44Z (and by NOVELTY at 23:27:16Z and CRITERION at
  23:28:42Z), HTTP 200, sha256 a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3: no per-cell
  values; links to coveringrepository.com and the Zenodo dataset.
- Zenodo: https://zenodo.org/api/records/19472830/versions/latest answered 301 to records/19735294 (version 1.2,
  published 2026-04-24; fetched 2026-10-15T23:12:39Z, HTTP 200). Its coverdata.json (8319503 bytes, sha256
  9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87, re-fetched by NOVELTY at 23:27:47Z and CRITERION
  at 23:29:59Z) has "C(85,24,3)": size 77, low_bd 61, history [77, "Simple construction from (86,24,3)", LJCR,
  2009-01-21 20:09:11].
- GitHub dmgordo/LJCR coverings/coverdata.json (last commit 2022-12-19T18:10:24Z; 6517686 bytes, sha256
  0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef, re-fetched by NOVELTY at 23:28:52Z and CRITERION
  at 23:30:17Z): "C(85,24,3)": size 77, low_bd 61.
