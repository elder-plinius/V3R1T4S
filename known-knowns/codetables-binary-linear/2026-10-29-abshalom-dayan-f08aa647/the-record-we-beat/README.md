# Table snapshot: https://codetables.de/BKLC/BKLC.php?q=9&n=31&k=17

- URL: https://codetables.de/BKLC/BKLC.php?q=9&n=31&k=17 (Markus Grassl, bounds on the minimum distance of linear
  codes, cell [31,17] over GF(9))
- Fetches (one plain GET each, curl, User-Agent naming V3R1T4S, no retries):
  - before the claim (the run's scout): 2026-10-29T01:01:18Z
  - the panel's NOVELTY skeptic: 2026-10-29T01:14:32Z
  - the panel's CRITERION skeptic: 2026-10-29T01:24:04Z
  - just before packaging: 2026-10-29T01:36:33Z
- HTTP status: 200 (all four)
- Selected headers (01:36:33Z fetch): `content-type: text/html; charset=UTF-8`, `date: Thu, 29 Oct 2026 01:36:34 GMT`,
  `server: Apache`
- Page size: 3510 bytes (scout and pre-packaging fetches)
- Page SHA-256: 920f1b71ab28952457d69a6f2ef2b422cba4790e647ba66d4f42f990965e524e (scout and pre-packaging fetches; the
  NOVELTY and CRITERION skeptics report their pages byte-identical to the saved page)
- Page footer: "Last change: 30.12.2011"; the cell's construction: "last modified: 2001-12-17"

## Extracted cell for (q, n, k) = (9, 31, 17)

```html
<H3>Bounds on linear codes [31,17] over GF(9)</H3><TABLE><TR><TD>lower bound:</TD><TD>10</TD></TR><TR><TD>upper bound:</TD><TD>13</TD></TR></TABLE>
```

- Listed lower bound: 10 (a [37,21,12] subcode of a punctured Reed-Solomon code over GF(81), punctured at {36..37}
  to [35,21,10], shortened at {32..35}; Brouwer: Lb(37,21) = 12, XL, Xing and Ling)
- Listed upper bound: 13 (from Brouwer's table, via shortening to Ub(18,4) = 13 and truncation to Ub(17,4) = 12,
  Marcugini, Milani and Pambianco)
- Our value: d = 11 (11 > 10, 11 <= 13)
- Neighboring cells on the n = 28..36 range page (https://codetables.de/BKLC/Tables.php?q=9&n0=28&n1=36&k0=1&k1=36,
  one GET 2026-10-29T01:07:43Z, HTTP 200, sha256 5a413ef3c4e0b0049207c144c0dd01cfac053bfba30bfe8f76456e0229fc75fa;
  lower-upper): [30,16] 11-13, [30,17] 10-12, [31,16] 11-14, [31,18] 9-12, [32,17] 11-14, [32,18] 10-13.
