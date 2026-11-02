# Table snapshot: https://eaqecc.codetables.de/qutrit.php

- URL: https://eaqecc.codetables.de/qutrit.php (Markus Grassl, bounds on entanglement-assisted qutrit codes)
- Fetches (one plain GET each, curl, User-Agent naming V3R1T4S, no retries):
  - before the claim: 2026-10-25T09:45:36Z
  - the panel's NOVELTY skeptic: 2026-10-25T11:05:08Z
  - the panel's CRITERION skeptic: 2026-10-25T11:22:04Z (byte-identical to the claim's copy)
- HTTP status: 200 (all)
- Selected headers (09:45:36Z fetch): `content-type: text/html; charset=UTF-8`, `date: Sun, 25 Oct 2026 09:45:36 GMT`,
  `server: Apache`
- Page size: 628039 bytes (all)
- Page SHA-256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c (all; the same hash as the
  snapshots recorded by the earlier packages in this family)
- Page footer: "Last change: 10.07.2025"

## Extracted row (n=24, k=4)

Every listed cell (n=24, k=4, c), verbatim; the claimed cell is the c = 10 one.

```html
<TD NOWRAP bgcolor="#66ff00" class="EAQECC" title="from codetables.de">[[24,4,8-10;0]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[23,4,9;3]] increasing dimension of [[23,1,9;0]] from codetables.de">[[24,4,9-12;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[24,4,11-17;4]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff6600" class="EAQECC" title="subcode of [[24,6,12;10]] from arXiv:2207.05647">[[24,4,12-19;10]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[23,4,13;11]] from arXiv:2207.05647">[[24,4,13-19;11]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[21,4,14;13]] increasing dimension of [[21,2,14;11]] from arXiv:2207.05647">[[24,4,14-20;13]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[25,3,16;14]] from arXiv:2207.05647">[[24,4,15-20;14]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[25,3,17;16]] increasing dimension of [[25,2,17;15]] from arXiv:2207.05647">[[24,4,16-20;16]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[22,4,17;18]] increasing dimension of [[22,1,17;15]] from arXiv:2207.05647">[[24,4,17-20;18]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[23,4,18;19]] quantum shortening of [[24,3,19;19]] increasing dimension of [[24,0,19;16]] from arXiv:2207.05647">[[24,4,18-20;19]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[24,0,19;16]] from arXiv:2207.05647">[[24,4,19-21;20]]<sub>3</sub></TD>
row (24,4), 11 cells; c: d_lower-d_upper: 0: 8-10; 3: 9-12; 4: 11-17 (using teleportation); 10: 12-19; 11: 13-19; 13: 14-20; 14: 15-20; 16: 16-20; 18: 17-20; 19: 18-20; 20: 19-21
```

- Listed d_lower-d_upper by c: 0: 8-10; 3: 9-12; 4: 11-17 (using teleportation); 10: 12-19; 11: 13-19; 13: 14-20;
  14: 15-20; 16: 16-20; 18: 17-20; 19: 18-20; 20: 19-21.
- The cell (24,4,10): `[[24,4,12-19;10]]_3`, titled "subcode of [[24,6,12;10]] from arXiv:2207.05647". Our code:
  `[[24,4,13;10]]_3`, d = 13 > d_lower 12 and <= d_upper 19.
- The teleportation cells nearby, verbatim: `[[24,3,13-19;3]]` and `[[24,4,11-17;4]]`, both titled "using teleportation".
- The page's six propagation rules applied to every listed cell other than the "using teleportation" cells, plus
  every code named in this repository's open pull requests (including draft PR #739) and the literature, give at most
  12 at (24,4,10); the row first lists d_lower 13 at c = 11.
