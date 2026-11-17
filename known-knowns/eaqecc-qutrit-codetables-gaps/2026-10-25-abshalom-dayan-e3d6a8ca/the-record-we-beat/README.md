# Table snapshot: https://eaqecc.codetables.de/qutrit.php

- URL: https://eaqecc.codetables.de/qutrit.php (Markus Grassl, bounds on entanglement-assisted qutrit codes)
- Fetches (one plain GET each, curl, User-Agent naming V3R1T4S, no retries):
  - before the claim: 2026-10-25T02:35:12Z
  - the panel's NOVELTY skeptic: 2026-10-25T03:37:49Z
  - the panel's CRITERION skeptic: 2026-10-25T03:52:24Z
  - at the honesty gate: 2026-10-25T04:58:16Z
- HTTP status: 200 (all)
- Selected headers (04:58:16Z gate fetch): `content-type: text/html; charset=UTF-8`, `date: Sun, 25 Oct 2026 04:58:16 GMT`,
  `server: Apache`
- Page size: 628039 bytes (all)
- Page SHA-256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (all; the same hash as the
  snapshots recorded by the earlier packages in this family)
- Page footer: "Last change: 10.07.2025"

## Extracted cell for (n=35, k=7, c=14)

```html
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,7,15;14]] quantum shortening of [[28,6,16;14]] increasing dimension of [[28,5,16;13]] from arXiv:2207.05647">[[35,7,15-26;14]]<sub>3</sub></TD>
```

- Listed lower bound d_lower: 15
- Listed upper bound d_upper: 26
- Our value: d = 16 (16 > 15, 16 <= 26)
- The listed row (n, k) = (35, 7), d_lower-d_upper by c: c = 0: 9-13; 2: 10-16; 4: 11-17; 6: 12-18; 8: 13-23;
  12: 14-25; 14: 15-26; 15: 16-26; 17: 17-27; 19: 18-27; 21: 19-27; 22: 20-28; 24: 21-28; 25: 22-28; 27: 23-28.
- d = 16 was listed at (35, 7) only with c = 15 (`[[35,7,16-26;15]]_3`, lengthening of `[[28,7,16;15]]`).
- The page's six propagation rules applied to every listed cell other than the 124 "using teleportation" cells give
  15 at (35,7,14) (both the NOVELTY and the CRITERION skeptic computed this independently). Seeding the teleportation
  cells as well would give 27, but the same seeding pushes thousands of listed cells above their own upper bounds
  (for example (5,1,4) to 6 > 5), so the page does not propagate them.
