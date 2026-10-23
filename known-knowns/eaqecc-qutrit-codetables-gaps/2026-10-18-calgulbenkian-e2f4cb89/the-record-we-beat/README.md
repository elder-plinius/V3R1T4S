# The record we beat (metadata only)

No third-party page is copied here. The table is the live qutrit table of entanglement-assisted codes; one cell is compared.

| Source | URL | UTC fetch time | HTTP | bytes | sha256 | Extracted cell |
|---|---|---|---|---|---|---|
| qutrit.php (panel novelty skeptic, the most recent fetch) | https://eaqecc.codetables.de/qutrit.php | 2026-10-18T14:23:13Z | 200 | 628039 | 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c | [[16,4,7-9;4]]_3: d_lower = 7, d_upper = 9 |
| qutrit.php (orchestrator, before the panel) | https://eaqecc.codetables.de/qutrit.php | 2026-10-18T13:53:54Z | 200 | 628039 | 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c | same cell |

The page footer reads "Last change: 10.07.2025". Both fetches have the same sha256. The skeptic reports are in `panel/novelty.md` (fetch details) and `panel/criterion.md`.

The details below are the original record written before the panel.


One honest GET (curl, User-Agent naming V3R1T4S, no retries, no browser) by the orchestrator. No page is copied here, only the one cell.

| Source | URL | UTC fetch time | HTTP | bytes | sha256 |
|---|---|---|---|---|---|
| qutrit.php | https://eaqecc.codetables.de/qutrit.php | 2026-10-18T13:53:54Z | 200 | 628039 | 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c |

Argon's own earlier copy of the page (taken by the author, not by the orchestrator; the author's claimed time is 2026-10-18 about 04:25Z) has the identical sha256, so the page did not change between the two fetches.

## How the cell was read

The page is one HTML table. Each parameter cell is a TD element whose title attribute gives the table's stated origin of the entry and whose text is [[n,k,d_lower-d_upper;c]] followed by a subscript 3 (a single number instead of a range means d_lower = d_upper). The cell was found by searching the saved page text for the pattern with n = 16, k = 4, c = 4, a range 7-9; it occurs exactly once. The element's two fields, exactly as they appear on the page, are saved in cell.txt in this folder:

```
title attribute: increasing dimension of [[16,0,7;0]] from codetables.de
text: [[16,4,7-9;4]]_3
```

Extracted values for the cell (n,k,c) = (16,4,4): d_lower = 7, d_upper = 9.

Compared cell: [[16,4,7-9;4]]_3. Reference lower bound: 7. This object: d = 8 with c = 4.
