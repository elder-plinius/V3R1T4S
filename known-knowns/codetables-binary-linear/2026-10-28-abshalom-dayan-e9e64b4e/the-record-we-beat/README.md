# Table snapshot: https://codetables.de/BKLC/BKLC.php?q=9&n=32&k=19

- URL: https://codetables.de/BKLC/BKLC.php?q=9&n=32&k=19 (Markus Grassl, bounds on the minimum distance of linear
  codes, cell [32,19] over GF(9))
- Fetches (one plain GET each, curl, User-Agent naming V3R1T4S, no retries):
  - before the claim (the run's scout): 2026-10-28T01:01:59Z
  - the panel's NOVELTY skeptic: 2026-10-28T01:26:14Z
  - the panel's CRITERION skeptic: 2026-10-28T01:39:29Z
  - just before packaging: 2026-10-28T01:50:06Z
- HTTP status: 200 (all four)
- Selected headers (01:50:06Z fetch): `content-type: text/html; charset=UTF-8`, `date: Wed, 28 Oct 2026 01:50:07 GMT`,
  `server: Apache`
- Page size: 3395 bytes (scout and pre-packaging fetches)
- Page SHA-256: 046bcdd475bd50f284382faa704382c748885ef8b22f02f48c9a9038e1be7bca (scout, NOVELTY, CRITERION and
  pre-packaging fetches; the skeptics report their pages byte-identical to the scout's)
- Page footer: "Last change: 30.12.2011"; the cell's construction: "last modified: 2001-12-17"

## Extracted cell for (q, n, k) = (9, 32, 19)

```html
<H3>Bounds on linear codes [32,19] over GF(9)</H3><TABLE><TR><TD>lower bound:</TD><TD>9</TD></TR><TR><TD>upper bound:</TD><TD>12</TD></TR></TABLE>
```

- Listed lower bound: 9 (a [41,29,9] BCH code (d = 5, b = 34), its [41,28,9] subcode, shortened at 33..41)
- Listed upper bound: 12 (from Brouwer's table, via Ub(17,4) = 12, Marcugini, Milani and Pambianco)
- Our value: d = 10 (10 > 9, 10 <= 12)
- Neighboring cells on the n = 28..36 range page as read on 2026-10-27T01:32:25Z by the previous run (lower-upper):
  [31,18] 9-12, [31,19] 9-11, [32,18] 10-13, [32,20] 9-11, [33,19] 10-13, [33,20] 9-12.
