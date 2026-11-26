# The record we beat: A(30,12,9)

Fetched with one plain curl request; the page itself is not included. Times are UTC.

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/Andw.html |
| fetched (UTC) | 2026-11-26T20:13:38Z |
| HTTP status | 200 |
| Date header | Thu, 26 Nov 2026 20:13:39 GMT |
| Last-Modified header | Thu, 26 Nov 2026 15:24:18 GMT |
| ETag header | "1fa41-6612f897b6fb5" |
| Content-Length header | 129601 |
| sha256 of the fetched page | 7429c8d2567123d043a5881bf67a3f1344b268b94a63af794eceefde2c165604 |

An earlier fetch the same day (2026-11-26T19:58:24Z) returned byte-identical content (same sha256).

## Extracted cell

Section "Bounds on A(n,12,w)": columns are w = 7, 8, 9, ..., 16, rows are n. An open cell is printed `lb-ub`; a single number is exact. The row for n = 30, as it appears in the page source (first four cells):

```
<th>30</th>
<td><a href="cwc/d12/a30.12.7.9">9</a></td>
<td><a href="cwc/d12/i30.8">30</a><sup>c</sup></td>
<td><span class="nw"><a href="cwc/d12/a30.12.9.44">44</a></span>-74<sup>Po</sup></td>
<td><a href="cwc/d12/a30.12.10.101">101</a><sup>E</sup>-159<sup>L</sup></td>
```

Column w = 9: lower bound **44** (code file `cwc/d12/a30.12.9.44`), upper bound **74** (label Po: Polak, arXiv:1703.05171). The mirror cell A(30,12,21) is not listed separately (the table lists w <= n/2).

The only note on the page that names the cell:

- `A(30,12,9) ≥ 44 was obtained by polishing the 43 found by [R].` ([R] = Rosin, arXiv:2603.00174.)

No note gives a value above 44 for this cell.

## The seed code

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44 |
| fetched (UTC) | 2026-11-26T20:13:59Z |
| HTTP status | 200 |
| Last-Modified header | Fri, 06 Mar 2026 14:40:17 GMT |
| sha256 | 56d5cb3304998a0322d495e97dbb128b8c3710a8201bcdd080d75c0d72d2f4cd |
| content | 44 lines, each 30 characters 0/1 |

## Bounds that neighbouring cells imply for A(30,12,9)

Computed by the claimant from the hosted code files (the 215-word A(32,12,11) file returned 404 and could not be checked):

| source cell (table value) | operation | implies |
|---|---|---|
| A(31,12,9) >= 50 | keep the words with 0 at the best coordinate, delete it | 38 |
| A(31,12,10) >= 109 | keep the words with 1 at the best coordinate, delete it | 38 |
| A(32,12,9) >= 60 | 0 at the best pair of coordinates | 35 |
| A(32,12,10) >= 123 | 1 at one coordinate, 0 at another, best pair | 29 |
| A(29,12,9) >= 42 | append a 0 coordinate | 42 |
| A(29,12,8) >= 22 | append a 1 coordinate | 22 |
| A(32,14,10) = 32 | A(n-2,d-2,w-1) >= A(n,d,w) | 32 |
| A(30,14,9) = 10 | any d = 14 code is a d = 12 code | 10 |

None reaches 45.

## Re-fetched immediately before filing

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/Andw.html |
| fetched (UTC) | 2026-11-26T20:27:26Z |
| HTTP status | 200 |
| Date header | Thu, 26 Nov 2026 20:27:27 GMT |
| Last-Modified header | Thu, 26 Nov 2026 20:15:27 GMT |
| ETag header | "1fbaf-661339abbc70a" |
| sha256 of the fetched page | 506f50d9bfb116c1ce98f218eec6a9e1a43f1db70271095bd6df15b6d5ab00a7 |

The page content changed between the reviewers' fetches (20:17 UTC, which still returned the page with sha256 7429c8d2...) and this one; its Last-Modified header now reads 20:15:27 GMT. The change adds the reference "Di: Kerem Dilker, email 2026-11-26 with 31 new bounds", renames the reference label BJLÖ to BHLÖ, and changes 23 cells, all with d at most 10 (for example A(23,10,10) from 54 to 56 and A(23,10,11) from 65 to 66). No cell in the d = 12 section changed. The A(30,12,9) cell still reads `44-74` (Po), and the only note naming the cell is still the one quoted above; no note gives 45 or more.
