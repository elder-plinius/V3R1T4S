# Table snapshot: https://codetables.de/BKLC/BKLC.php?q=9&n=29&k=19

- URL: https://codetables.de/BKLC/BKLC.php?q=9&n=29&k=19 (Markus Grassl, bounds on the minimum distance of linear
  codes, cell [29,19] over GF(9))
- Fetches (one plain GET each, curl, User-Agent naming V3R1T4S, no retries):
  - before the claim (the run's scout): 2026-10-27T01:50:01Z
  - the panel's NOVELTY skeptic: 2026-10-27T02:00:51Z
  - the panel's CRITERION skeptic: 2026-10-27T02:09:43Z
  - just before packaging: 2026-10-27T02:21:50Z
- HTTP status: 200 (all four)
- Selected headers (02:21:50Z fetch): `content-type: text/html; charset=UTF-8`, `date: Tue, 27 Oct 2026 02:21:50 GMT`,
  `server: Apache`
- Page size: 3136 bytes (all four)
- Page SHA-256: fe750485b053225286430c77f5fa80a4686c4ea13208407331b2a126f5f63cf3 (all four)
- Page footer: "Last change: 30.12.2011"; the cell's construction: "last modified: 2001-12-17"
- Range page n = 28..36 (https://codetables.de/BKLC/Tables.php?q=9&n0=28&n1=36&k0=1&k1=36), one GET at
  2026-10-27T01:32:25Z and one by the NOVELTY skeptic at 2026-10-27T02:01:00Z, HTTP 200, SHA-256
  5a413ef3c4e0b0049207c144c0dd01cfac053bfba30bfe8f76456e0229fc75fa (both): the cell reads `7-9`.

## Extracted cell for (q, n, k) = (9, 29, 19)

```html
<H3>Bounds on linear codes [29,19] over GF(9)</H3><TABLE><TR><TD>lower bound:</TD><TD>7</TD></TR><TR><TD>upper bound:</TD><TD>9</TD></TR></TABLE>
```

- Listed lower bound: 7 (a [37,28,7] subcode of a punctured Reed-Solomon code over GF(81) by Xing and Ling,
  shortened to [29,20,7], then a [29,19,7] subcode)
- Listed upper bound: 9 (from Brouwer's table, via Ub(21,11) = 9)
- Our value: d = 8 (8 > 7, 8 <= 9)
- Neighboring cells on the range page (lower-upper): [28,18] 8-9, [28,19] 7-9, [29,18] 8-10, [29,20] 7-9,
  [30,19] 8-10, [30,20] 7-9. The panel's NOVELTY skeptic checked all 288 cells of the range page under shortening,
  puncturing, subcode and zero-column rules: the best d they imply at (29,19) is 7 (`panel/novelty.md`).
