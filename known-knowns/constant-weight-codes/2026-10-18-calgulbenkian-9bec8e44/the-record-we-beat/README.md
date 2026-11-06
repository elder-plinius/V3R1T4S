# The record we compare against

No third-party page is copied here. Two plain GETs on 2026-10-18 (curl, User-Agent naming V3R1T4S, no retries) of
https://aeb.win.tue.nl/codes/Andw.html returned the same page. A third GET on 2026-11-06, on maintainer review (#440), returned an updated page.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Andw.html (fetched by calgulbenkian while assembling this package) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:39:47Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | A(28,8,11) = 3785Pl-11896KT; mirror A(28,8,17) = None |
| Andw.html (panel novelty skeptic, re-fetch) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | anchor a28.8.11.3785H, shown as 3785 with source label Pl |
| Andw.html (fetched by calgulbenkian on maintainer review, #440) | https://aeb.win.tue.nl/codes/Andw.html | 2026-11-06T20:26:09Z | 200 | 91479623612b85a1782b729dc88563c3a944c65f7181b7965964a08de1a52e82 | A(28,8,11) = 3791Ol-11896KT; mirror A(28,8,17) = None |

Compared cell: A(28,8,11). Live lower bound 3791 on 2026-11-06 (label Ol: Antoine Olivier, emails 2026-10-10/19/22, per the page legend); it was 3785 on 2026-10-18 (label Pl: a code from the merged V3R1T4S bigger-codes family). Live upper bound 11896. This object: 3802.

Cell text is produced by `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 28,8,11` on a page saved with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html`; output for the page fetched 2026-11-06T20:26:09Z (third row): `28,8,11 | 3791Ol-11896KT | mirror None`; for the 2026-10-18 page (first two rows) it was `28,8,11 | 3785Pl-11896KT | mirror None`. If the live page has changed since, compare the current cell text with this one.

The page has no cell for the mirror A(28,8,17).
