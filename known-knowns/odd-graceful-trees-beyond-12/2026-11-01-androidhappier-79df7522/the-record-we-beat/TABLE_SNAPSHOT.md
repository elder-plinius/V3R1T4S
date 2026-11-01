# The record we compared against: Gallian, A Dynamic Survey of Graph Labeling (DS6), Section 3.6

Status source (bank target odd-graceful-trees-beyond-12): https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
PDF linked from it: https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/

## Extracted cell
| quantity | DS6 value (edition "DS6: Oct 30, 2025") | this package |
|---|---|---|
| largest order n such that every tree on at most n vertices is known to be odd-graceful | 12 (Barrientos; Gnanajothi had 10) | 22 |

Quoted from DS6, Section 3.6 (Odd-Graceful Labelings), p. 86: "She conjectures that all trees are odd-graceful and
proves the conjecture for all trees with order up to 10. Barrientos [488] has extended this to trees of order up to
12." No higher bound for all trees appears elsewhere in the survey.

## Fetches (one GET each, plain curl, User-Agent "V3R1T4S-research-agent", no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-01T02:26:39Z | run scout | article page (above) | 200 | 1794453fe928c59d0beacf964983639c3af6af768a1fe5ba4ed16b6b74234aed |
| 2026-11-01T02:26:53Z | run scout | PDF (above) | 200 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| 2026-11-01T03:00:08Z | novelty skeptic (panel) | article page | 200 | (not recorded; page reads "This Version DS6: Oct 30, 2025") |
| 2026-11-01T03:00:15Z | novelty skeptic (panel) | PDF | 200 | b1b5d8ba828b3fcd7eb4d73402b63252bd06b59bdcfb4f32f558f8af5898842e |
| 2026-11-01T03:12:12Z | honesty gate | article page | 200 | cf4cea9032753842d2ecd4ff74616919036dfcd0f2afe14f6a5aba8244a492af |

The two article-page copies differ only in the per-session csrfToken value; both read "DS6: Oct 30, 2025".

Selected response headers of the gate-time fetch:

    HTTP/1.1 200 OK
    Date: Sun, 01 Nov 2026 03:12:15 GMT
    Server: Apache
    Cache-Control: no-store
    Content-Type: text/html; charset=utf-8

The number of trees per order comes from OEIS A000055 (https://oeis.org/A000055, fetched as
https://oeis.org/search?q=id:A000055&fmt=text at 2026-11-01T02:27:40Z, HTTP 200, sha256
70ba2faf6049442ce286fd6173346fb4cd3ff13e2b9079e32fcb58f9fe8e1731); the checker also recomputes it from Otter's
formula.

The pages and the PDF are not included (third-party content). Anyone can re-fetch the URLs above.
