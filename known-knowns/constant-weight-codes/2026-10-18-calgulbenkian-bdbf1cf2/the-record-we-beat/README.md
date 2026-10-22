# The record we compare against

No third-party page is copied here. Two plain GETs (curl, User-Agent naming V3R1T4S, no retries) of
https://aeb.win.tue.nl/codes/Andw.html returned the same page.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Andw.html (orchestrator, builds the claim folder) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:39:47Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | A(27,8,10) = 1737Pl-4986; mirror A(27,8,17) = None |
| Andw.html (panel novelty skeptic, re-fetch) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | anchor a27.8.10.1737H, shown as 1737 with source label Pl |

Compared cell: A(27,8,10). Live lower bound 1737 (label Pl: a code from the merged V3R1T4S bigger-codes family); live upper bound 4986. This object: 1740.

Cell text is produced by `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 27,8,10` on a page saved with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html`; expected output for the page with the sha256 above: `27,8,10 | 1737Pl-4986 | mirror None`. If the live page has changed since, compare the current cell text with this one.

The page has no cell for the mirror A(27,8,17).
