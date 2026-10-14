# The record we compared against (snapshot, not the page)

Selected headers were not stored by the single honest fetch. Recorded below: URL, UTC fetch time, HTTP status and the sha256 of the page bytes. The pages and point files themselves are not included.

| source | URL | fetched (UTC) | HTTP | page sha256 | extracted cell, N = 550 |
|---|---|---|---|---|---|
| CCD Thomson2 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | 2026-10-14T14:56:23Z | 200 | caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794 | 144126.0927100 |

Posted point file used:

| file | URL | fetched (UTC) | HTTP | sha256 |
|---|---|---|---|---|
| 550.xyz (Thomson2) | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/xyz/550.xyz | 2026-10-14T07:21:41Z | 200 | 3ec7218c52bac398c2d02080a76049813adeb4ae01db38b5bee489e017ef8382 |

The page sha256 was identical to the earlier scout fetch (table unchanged). The novelty skeptic's live fetch is recorded in panel/novelty.md.
