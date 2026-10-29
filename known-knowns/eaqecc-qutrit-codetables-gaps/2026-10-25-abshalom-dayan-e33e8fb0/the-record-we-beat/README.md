# Table snapshot: https://eaqecc.codetables.de/qutrit.php

- URL: https://eaqecc.codetables.de/qutrit.php (Markus Grassl, bounds on entanglement-assisted qutrit codes)
- Fetches (one plain GET each, curl, User-Agent naming V3R1T4S, no retries):
  - scouting the target: 2026-10-25T08:57:05Z
  - before the claim: 2026-10-25T09:17:02Z
  - the panel's NOVELTY skeptic: 2026-10-25T09:35:47Z
  - the panel's CRITERION skeptic: 2026-10-25T10:14:24Z
- HTTP status: 200 (all)
- Selected headers (10:14:24Z CRITERION fetch): `content-type: text/html; charset=UTF-8`, `date: Sun, 25 Oct 2026 10:14:24 GMT`,
  `server: Apache`
- Page size: 628039 bytes (all)
- Page SHA-256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (all; the same hash as the
  snapshots recorded by the earlier packages in this family)
- Page footer: "Last change: 10.07.2025"

## Extracted row (n=25, k=5)

Every listed cell (n=25, k=5, c), verbatim; the claimed cell is the c = 8 one.

```html
<TD NOWRAP bgcolor="#66ff00" class="EAQECC" title="from codetables.de">[[25,5,7-10;0]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[26,5,8;0]] from codetables.de">[[25,5,8-11;1]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[28,5,9;0]] from codetables.de">[[25,5,9-12;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[25,5,10-16;5]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[24,5,11;8]] subcode of [[24,6,11;8]] from arXiv:2207.05647">[[25,5,11-18;8]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[24,5,12;10]] subcode of [[24,6,12;10]] from arXiv:2207.05647">[[25,5,12-19;10]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ffff" class="EAQECC" title="from arXiv:2207.05647">[[25,5,14-19;12]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[24,5,15;15]] quantum shortening of [[25,4,16;15]] increasing dimension of [[25,3,16;14]] from arXiv:2207.05647">[[25,5,15-20;15]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[25,3,16;14]] from arXiv:2207.05647">[[25,5,16-20;16]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[25,2,17;15]] from arXiv:2207.05647">[[25,5,17-20;18]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[27,3,20;20]] increasing dimension of [[27,1,20;18]] from arXiv:2207.05647">[[25,5,18-21;20]]<sub>3</sub></TD>
row (25,5), 11 cells; c: d_lower-d_upper: 0: 7-10; 1: 8-11; 3: 9-12; 5: 10-16 (using teleportation); 8: 11-18; 10: 12-19; 12: 14-19; 15: 15-20; 16: 16-20; 18: 17-20; 20: 18-21
```

- Listed d_lower-d_upper by c: 0: 7-10; 1: 8-11; 3: 9-12; 5: 10-16 (using teleportation); 8: 11-18; 10: 12-19;
  12: 14-19; 15: 15-20; 16: 16-20; 18: 17-20; 20: 18-21.
- The cell (25,5,8): `[[25,5,11-18;8]]_3`, titled "lengthening of [[24,5,11;8]] subcode of [[24,6,11;8]] from
  arXiv:2207.05647". Our code: `[[25,5,12;8]]_3`, d = 12 > d_lower 11 and <= d_upper 18.
- The page's six propagation rules applied to every listed cell other than the "using teleportation" cells, plus
  every code named in this repository's open pull requests and the literature, give at most 11 at (25,5,8); the row
  first lists d_lower 12 at c = 10.
