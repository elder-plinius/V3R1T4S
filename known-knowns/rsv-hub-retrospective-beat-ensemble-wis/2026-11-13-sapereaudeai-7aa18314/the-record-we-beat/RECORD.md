# The record we beat (snapshot record; the pages themselves are not copied)

Comparator (route (a)): the hub-ensemble's own 2024-25 model-output in HopkinsIDD/rsv-forecast-hub, re-scored (the hub
publishes no scores file, so the bank says the recomputed ensemble value is the bar).
- Repository commit: 6bf251ac3fc798e55ed95d0b7269f5f5781c0207 (main), https://github.com/HopkinsIDD/rsv-forecast-hub
- Live re-check before the gate: GET https://api.github.com/repos/HopkinsIDD/rsv-forecast-hub/git/trees/main?recursive=1
  at 2026-11-13T02:23:01Z, HTTP 200, 171791 bytes; 300 model-output files and the target file unchanged by git blob SHA;
  then one GET per 2024-25 hub-ensemble file from https://raw.githubusercontent.com/HopkinsIDD/rsv-forecast-hub/main/
  (02:23:04Z .. 02:23:30Z), HTTP 200 each, byte-identical to the scored copies.
- sha256 of each comparator input (all 15 2024-25 hub-ensemble files and the target file; checked by
  verify-it-yourself/check_claim.py): verify-it-yourself/pinned_inputs.txt, copied below from that file.
- Extracted cell: hub-ensemble season-average WIS 99.7021 on 3,065 scored tasks over 14 reference dates (2024-10-27 ..
  2025-04-06; the 2024-12-01 file has 0 rows).

Bank status source: https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble, fetched
2026-11-13T01:04:37Z, HTTP 200, page sha256 aac8860cb01b3b74a2ab0cbe2bb5216da7ad65ef6487e39275e24072b8b008cd
(36 RSVHub-ensemble files, no scores file); NOVELTY skeptic re-fetch 2026-11-13T02:06:47Z, HTTP 200, same 36 files.

```
7d0deb3fd66ea49506125f82e565d5f05a0cce2b15c7606b0436dcea5971847d  model-output/hub-ensemble/2024-10-27-hub-ensemble.parquet
4d549ef0d15adaa0f61b39d098dffdf10afb686032074ac37bab7737881d12a3  model-output/hub-ensemble/2024-11-03-hub-ensemble.parquet
8346caf7e8c4a5a1ca1c7940f0cc24bfdad037cf30f9e3f3438f22dfd8f7b46f  model-output/hub-ensemble/2024-11-10-hub-ensemble.parquet
2581c5e997ed85abf73aa4254d825ae98f2a7a65311792a0cfee2faee8a9fd5f  model-output/hub-ensemble/2024-11-17-hub-ensemble.parquet
be9039feb964a3e3a92f83289ae2caead1633f44db534dc64de43e3f601aaca5  model-output/hub-ensemble/2024-11-24-hub-ensemble.parquet
27ab70f0a36ae28ab000546eb4789bb9073c1dca40cd88793d0feaa794562f04  model-output/hub-ensemble/2024-12-01-hub-ensemble.parquet
99dc353719cd65bce70ee7aba663d70187dd8b58586df8a19fc54e85e7247caa  model-output/hub-ensemble/2024-12-08-hub-ensemble.parquet
6de7902b067cafb91c85557a3d0399ebd44c26331f60fd86a29cda36aa27dfc4  model-output/hub-ensemble/2024-12-15-hub-ensemble.parquet
aa52bcfb6251f69ee7788f7d8a2db1f5be2a34e323a286baf0134c990666630e  model-output/hub-ensemble/2024-12-29-hub-ensemble.parquet
92ae8ad37a80565f2cbaa7304eb6d77d5dcb6c3856484ef0fd5d598a7eb13c9f  model-output/hub-ensemble/2025-01-05-hub-ensemble.parquet
43bf324413f583c300bf44cfce53b06463f843841aec9f11a71164ba7f55d889  model-output/hub-ensemble/2025-01-12-hub-ensemble.parquet
69bdbbff3588ea39a372b1c6b7a5a2ec148df8b74f6da456c3c58eab6f538f56  model-output/hub-ensemble/2025-01-26-hub-ensemble.parquet
ff46c72b1e3d9f6480d0dbfb51df32a284a7e7892c99de56bf16e397f097a08b  model-output/hub-ensemble/2025-02-09-hub-ensemble.parquet
0dc635010b7fb082c6345e522feef9f428dfd6c369868b2a8ca9f1cce83f0a51  model-output/hub-ensemble/2025-02-16-hub-ensemble.parquet
28879d81ed8bf334a007674ae67ad2f1c20742ef7a40c4c10841f39897637a25  model-output/hub-ensemble/2025-04-06-hub-ensemble.parquet
047b9f53ca549ed2fe824018598480a9d4e7db0099a0bcec2371e7733329eaf7  target-data/2026-06-05_rsvnet_hospitalization.csv
```
