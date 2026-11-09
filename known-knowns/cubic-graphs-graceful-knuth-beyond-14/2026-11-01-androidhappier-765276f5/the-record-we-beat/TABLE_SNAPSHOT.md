# The record we compared against: Gallian, A Dynamic Survey of Graph Labeling (DS6), Section 2

Status source (bank target cubic-graphs-graceful-knuth-beyond-14): https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
PDF linked from it: https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/

## Extracted cell
| quantity | DS6 value (edition "DS6: Oct 30, 2025", 28th edition) | best other source | this package |
|---|---|---|---|
| largest n such that every connected cubic graph on n vertices (all even orders up to n) is known to be graceful | 14 (Knuth) | 16 (Knuth, pre-fascicle 7A, answer to ex. 96; Kennedy 2021) | 22 |

Quoted from DS6, Section 2 (as read by the scout and the novelty skeptic): "Knuth [1863] proved by way a computer
search that all cubic graphs on 4, 6, 8, 10, 12, or 14 vertices, except 2K4 and 3K4 , which was proved by Kotzig,
are graceful. He conjectures that that every connected cubic graph is graceful."

Quoted from Knuth, pre-fascicle 7A (Section 7.2.2.3, dated Dec 5, 2024), answer to exercise 96: "With considerably
more computation, the results of exercise 95 can be extended to the 204,154,267,353 graceful labelings of cubic
graphs on 16 vertices. There are 4207 such graphs, of which 4060 are connected."

## Fetches (one GET each, plain curl, User-Agent "V3R1T4S-research-agent", no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-01T15:17:13Z | run scout | DS6 article page | 200 | 1bb693d6d91737e4310f2df4d14417c2e5a42f60dbe5ca87e87bad5c49736a93 |
| 2026-11-01T15:17:14Z | run scout | DS6 PDF | 200 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| 2026-11-01T15:18:14Z | run scout | https://www-cs-faculty.stanford.edu/~knuth/fasc7a.ps.gz | 200 | 24ab2d899b0ab91c25c1d760b3ba5afef09e89dbc7c80c94047fed26cfcb255d |
| 2026-11-01T16:56:19Z | novelty skeptic (panel) | DS6 article page | 200 | 4acc9fa4dcea3c7c804e2765f7091641ae7be7ffff7b1ffbcf0d7137e763cdb5 |
| 2026-11-01T16:56:20Z | novelty skeptic (panel) | DS6 PDF | 200 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| 2026-11-01T16:56:23Z | novelty skeptic (panel) | fasc7a.ps.gz | 200 | 24ab2d899b0ab91c25c1d760b3ba5afef09e89dbc7c80c94047fed26cfcb255d |
| 2026-11-01T17:26:55Z | packaging re-check | DS6 article page | 200 | 48459fca8619aef2f352b6ec6c7e32067e9af38e46694c3a76c8741e7bc12ac7 |

The DS6 article-page copies differ by fetch (dynamic OJS page). All three read "DS6: Oct 30, 2025". The PDF
and the pre-fascicle hashes did not change between the scout and the panel.

Selected response headers of the packaging-time fetch:

    HTTP/1.1 200 OK
    Date: Sun, 01 Nov 2026 17:26:57 GMT
    Server: Apache
    Cache-Control: no-store
    Content-Type: text/html; charset=utf-8

The number of connected cubic graphs per order comes from OEIS A002851. Its b-file
(https://oeis.org/A002851/b002851.txt) was fetched at 2026-11-01T15:17:17Z, HTTP 200, sha256
75ac8779e418c63d6ca09e330683b23594df2b06383b9d6d6156a2dac83064f4. Values used: 1, 2, 5, 19, 85, 509, 4060, 41301,
510489, 7319447 for 4..22 vertices.

The pages, the PDF and the PostScript file are not included (third-party content). Anyone can re-fetch the URLs above.
