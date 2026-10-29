# Table record

- URL: https://eaqecc.codetables.de/qutrit.php
- Fetched 2026-10-25T09:53:51Z to 2026-10-25T09:53:52Z (UTC, `date -u` before and after), one plain GET with curl,
  User-Agent "V3R1T4S-research-agent (honest single fetch)", no retries; http_code=200 size=628039 (qutrit.result).
- Later fetches by the panel, each one plain GET, HTTP 200, 628039 bytes, same sha256 (`panel/novelty.md`, `panel/criterion.md`): NOVELTY skeptic 2026-10-25T11:27:14Z; CRITERION skeptic 2026-10-25T13:58:02Z (started) to 13:58:03Z.
- The claim's copy of the page is not included in this package (never the page itself); its response headers, start time and end time were `qutrit.headers.txt`, `qutrit.time_start` and `qutrit.time_end` in the run's claim folder,
  sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. Page footer: "Last change: 10.07.2025".
- Selected response headers of that fetch: `HTTP/2 200`, `content-type: text/html; charset=UTF-8`,
  `date: Sun, 25 Oct 2026 09:53:51 GMT`, `server: Apache`.
- Row (n, k) = (23, 4), every listed cell verbatim from the page (row_23_4.txt in this folder, made by
  this folder's `extract_row.py` as `python3 extract_row.py qutrit.php 23 4`, which prints every `<TD ...>[[23,4,...]]<sub>3</sub></TD>` cell):

```html
<TD NOWRAP bgcolor="#66ff00" class="EAQECC" title="from codetables.de">[[23,4,7-9;0]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ccff" class="EAQECC" title="reducing length of [[24,4,8;0]] from codetables.de">[[23,4,8-11;1]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[23,1,9;0]] from codetables.de">[[23,4,9-12;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[23,4,10-16;4]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[19,4,11;9]] quantum shortening of [[20,3,12;9]] from arXiv:2207.05647">[[23,4,11-18;9]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[20,4,12;10]] increasing dimension of [[20,3,12;9]] from arXiv:2207.05647">[[23,4,12-18;10]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ffff" class="EAQECC" title="from arXiv:2207.05647">[[23,4,13-18;11]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[21,4,14;13]] increasing dimension of [[21,2,14;11]] from arXiv:2207.05647">[[23,4,14-19;13]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[25,2,17;15]] from arXiv:2207.05647">[[23,4,15-19;15]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[21,4,16;17]] increasing dimension of [[21,1,16;14]] from arXiv:2207.05647">[[23,4,16-19;17]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[22,4,17;18]] increasing dimension of [[22,1,17;15]] from arXiv:2207.05647">[[23,4,17-19;18]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#00ff99" class="EAQECC" title="quantum shortening of [[24,3,19;19]] increasing dimension of [[24,0,19;16]] from arXiv:2207.05647">[[23,4,18-20;19]]<sub>3</sub></TD>
```

- row (23,4), 12 cells; c: d_lower-d_upper: 0: 7-9; 1: 8-11; 3: 9-12; 4: 10-16 (using teleportation); 9: 11-18; 10: 12-18; 11: 13-18; 13: 14-19; 15: 15-19; 17: 16-19; 18: 17-19; 19: 18-20
- The claimed cell (23,4,9) is listed as [[23,4,11-18;9]]: d_lower 11, d_upper 18.
- Neighbouring rows from the same page (c: d_lower-d_upper; full cells in this folder's row_*.txt files):
  - row (23,3), 10 cells; c: d_lower-d_upper: 0: 7-9; 1: 8-11; 2: 9-12; 3: 12-18 (using teleportation); 11: 13-20; 12: 14-20; 14: 15-20; 16: 16-20; 17: 17-20; 18: 18-20
  - row (23,5), 9 cells; c: d_lower-d_upper: 0: 7-9; 2: 8-11; 4: 9-12; 6: 10-15; 9: 11-17; 11: 12-17; 12: 13-17; 14: 14-18; 16: 15-18
  - row (22,4), 11 cells; c: d_lower-d_upper: 0: 7-9; 2: 8-11; 4: 9-15 (using teleportation); 6: 10-16; 9: 11-17; 10: 12-17; 12: 13-18; 13: 14-18; 15: 15-18; 17: 16-18; 18: 17-19
  - row (24,4), 11 cells; c: d_lower-d_upper: 0: 8-10; 3: 9-12; 4: 11-17 (using teleportation); 10: 12-19; 11: 13-19; 13: 14-20; 14: 15-20; 16: 16-20; 18: 17-20; 19: 18-20; 20: 19-21
- The cells (23,3,3) and (23,4,4), verbatim (titled "using teleportation"):
```html
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[23,3,12-18;3]]<sub>3</sub></TD>
<TD NOWRAP bgcolor="#ffff00" class="EAQECC" title="using teleportation">[[23,4,10-16;4]]<sub>3</sub></TD>
```
- The claim needs a live re-read of the page ("re-fetched live immediately before claiming").
