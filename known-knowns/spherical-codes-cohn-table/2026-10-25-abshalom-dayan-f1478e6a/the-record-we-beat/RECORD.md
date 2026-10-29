# The record we beat

Table: spherical-codes.org (Henry Cohn's Table of Spherical Codes; archived data set
https://hdl.handle.net/1721.1/153543). Cell: d = 6, N = 256.

| page | URL | UTC fetch time | HTTP | bytes | sha256 of the page |
|---|---|---|---|---|---|
| HTML index | https://spherical-codes.org/ | 2026-10-25T06:26:36Z | 200 | 4,668,044 | 69a54be57593369dd9d36002a32107c342e0441b1c6298c2d3c5617a538472ea |
| /plain | https://spherical-codes.org/plain | 2026-10-25T06:26:38Z | 200 | 377,006 | 7d965100bfb54727ec3eaa4ef7e23558b5c048eca94b6b6281b3f02c80669f62 |

Selected response headers: index `HTTP/2 200`, `content-type: text/html; charset=utf-8`,
`date: Sun, 25 Oct 2026 06:26:37 GMT`, `server: gunicorn`; /plain `HTTP/2 200`, `content-type: text/plain;
charset=utf-8`, `date: Sun, 25 Oct 2026 06:26:39 GMT`; no cookies set. One request each, User-Agent
"V3R1T4S-research-agent (honest single fetch)", no retries. The same /plain line is in every /plain read saved in the
workspace (27 reads since 2026-10-24; the earliest with a fetch-log line is 2026-10-24T18:04:59Z), including
05:50:24Z and 06:05:40Z in this run.

Extracted cell, index (lines 29331-29336): `<td>6</td>` | `<td><a href="/data/6/256">256</a></td>` (no `&ast;`) |
`<td>0.704931969352</td>` | `<td>Pavlos Moros, 2026.</td>` (no "needs more optimization").
Extracted cell, /plain (line 3237): `6,256,0.704931969352`.

Table cosine compared against: 0.704931969352. The posted code for the cell (https://spherical-codes.org/data/6/256,
fetched 2026-10-25T05:52:42Z, sha256 c5866a15cdabfe6f593fd878d690a9339d502f9720a7122f39d594a60b27992b, the same bytes
as the copy fetched 2026-10-24T17:37:11Z that the polish started from) has max cosine 0.7049319693516105, which
reproduces the table value (the table rounds up).

Other sources compared: no listed code with d' <= 6 and N' >= 256 (which would give a (6, 256) code by deleting
points or padding with zeros) has cosine at or below the claimed value, in the table or in the three tables of
arXiv:2610.19988 (Ilmari Vahteristo; Zenodo record 23270586), whose own (6, 256) values are 0.7049931928409804
(combined), 0.7050249538274573 (per instance) and 0.7053373293588499 (global). ImprovEvolve (arXiv:2602.10233) has
no row with d' <= 6 (its 90 cells are in d = 8 to 16). Earlier versions of the row: 0.705181763211 on 2026-08-02 and
0.705119115483 on 2026-09-23 (credited to Antoine Jay), in the snapshots recorded by arXiv:2610.19988's data.

## Re-read before filing (2026-10-28)

The 2026-10-25 records above are kept as history. Before filing, each page was read again with one GET each, User-Agent "V3R1T4S filing check (curl)", no retries. Server `date:` headers: index Wed, 28 Oct 2026 18:23:47 GMT, /plain 18:23:50 GMT, /data/6/256 18:23:52 GMT.

| page | URL | UTC fetch time | HTTP | bytes | sha256 of the page |
|---|---|---|---|---|---|
| HTML index (re-read before filing) | https://spherical-codes.org/ | 2026-10-28T18:23:47Z | 200 | 4,602,989 | f4902419f69013e2c4f302f58843eb4f0c3206da4df27e002b83e53bff7fa3a7 |
| /plain (re-read before filing) | https://spherical-codes.org/plain | 2026-10-28T18:23:50Z | 200 | 372,021 | 122b4cf231faf197003b6dd1bd6582ba2bd6713a2893967f7b7ffeb270c23789 |
| /data/6/256 (re-read before filing) | https://spherical-codes.org/data/6/256 | 2026-10-28T18:23:52Z | 200 | 30,711 | c5866a15cdabfe6f593fd878d690a9339d502f9720a7122f39d594a60b27992b |

Both the index and /plain changed between 2026-10-25 and 2026-10-28 (different sha256 values); the (6, 256) row (index lines 29331-29336, /plain line 3237) did not: index `<td>6</td>` | `<td><a href="/data/6/256">256</a></td>` (no `&ast;`) | `<td>0.704931969352</td>` | `<td>Pavlos Moros, 2026.</td>` (no "needs more optimization"); /plain `6,256,0.704931969352`. The posted code /data/6/256 has the same sha256 as the copy the polish started from. Among the rows with d' <= 6 and N' >= 256 (2,966 in the index; (6, 256) itself is the lowest, then (6, 257) at 0.705350637779) none is at or below c* + 1e-10.
