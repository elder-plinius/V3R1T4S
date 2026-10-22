# The record we compare against

No third-party page is copied here. Two plain GETs (curl, User-Agent naming V3R1T4S, no retries) of
https://aeb.win.tue.nl/codes/Andw.html returned the same page.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Andw.html (orchestrator, builds the claim folder) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:39:47Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | A(55,8,7) = 4426Pl-9617; mirror A(55,8,48) = None |
| Andw.html (panel novelty skeptic, re-fetch) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | anchor a55.8.7.4426H, shown as 4426 with source label Pl |

Compared cell: A(55,8,7). Live lower bound 4426 (label Pl: a code from the merged V3R1T4S bigger-codes family); live upper bound 9617. This object: 4432.

Cell text is produced by `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 55,8,7` on a page saved with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html`; expected output for the page with the sha256 above: `55,8,7 | 4426Pl-9617 | mirror None`. If the live page has changed since, compare the current cell text with this one.

The page has no cell for the mirror A(55,8,48).
