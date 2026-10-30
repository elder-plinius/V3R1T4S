# The record we beat

Table: spherical-codes.org (Henry Cohn's Table of Spherical Codes; archived data set
https://hdl.handle.net/1721.1/153543). Cell: d = 6, N = 575.

| page | URL | UTC fetch time | HTTP | bytes | sha256 of the page |
|---|---|---|---|---|---|
| HTML index | https://spherical-codes.org/ | 2026-10-25T00:04:42Z | 200 | 4,668,831 | 5f44f00d01d4971738177e7a37da2c3b086bea4971dc8f617575cc5fd3c5d663 |
| /plain | https://spherical-codes.org/plain | 2026-10-25T00:04:44Z | 200 | 377,882 | cab1729eb8aa0c2f1953c9680d3bfc849fb8ae8d05bcd0eea23042e0a3f63a54 |

Selected response headers: index `HTTP/2 200`, `content-type: text/html; charset=utf-8`,
`date: Sun, 25 Oct 2026 00:04:42 GMT`, `server: gunicorn`; /plain `HTTP/2 200`, `content-type: text/plain;
charset=utf-8`, `date: Sun, 25 Oct 2026 00:04:44 GMT`; no cookies set. One request each, User-Agent
"V3R1T4S-research-agent (honest single fetch)", no retries. The same row, with the same value and reference, was
read at 2026-10-24T17:25:57Z, 18:04:58Z, 18:43:18Z, 20:39:45Z, 20:47:09Z, 21:24:08Z, 22:54:03Z, 23:24:28Z and
23:45:04Z (the 23:45:04Z pages are byte-identical to the 00:04:42Z ones).

Extracted cell, index (lines 31833-31838): `<td>6</td>` | `<td><a href="/data/6/575">575</a></td>` (no `&ast;`) |
`<td>0.792780236785</td>` | `<td>Pavlos Moros, 2026.</td>` (no "needs more optimization").
Extracted cell, /plain (line 3515): `6,575,0.792780236785`.

Table cosine compared against: 0.792780236785. The posted code for the cell (https://spherical-codes.org/data/6/575,
sha256 a0b954a28ad0af6cc8ad9307c6239a0a5ee88e8facf7a0bf009ccd9082a33340) has max cosine
0.7927802367840796857136, which reproduces the table value (the table rounds up).

Other sources compared: no listed code with d' <= 6 and N' >= 575 (which would give a (6, 575) code by deleting
points or padding with zeros) has cosine at or below the claimed value, in the table or in the three tables of
arXiv:2610.19988 (Ilmari Vahteristo; Zenodo record 23270586), whose own (6, 575) values are 0.7932289977343617
(combined), 0.7932322927113262 (per instance) and 0.7932389659189362 (global).
