# The record we compare against

No third-party page is copied here. Two plain GETs (curl, User-Agent naming V3R1T4S, no retries) of
https://aeb.win.tue.nl/codes/Andw.html on 2026-10-18 returned the same page. A third fetch on 2026-11-18 returned a changed page, which now lists 3801 (label Wu, Ken Wu, email of 2026-11-11) for this cell.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Andw.html (package author) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:39:47Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | A(52,8,7) = 3799Pl-7577; mirror A(52,8,45) = None |
| Andw.html (panel novelty skeptic, re-fetch) | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | anchor a52.8.7.3799H, shown as 3799 with source label Pl |
| Andw.html (live table, fetched for this update) | https://aeb.win.tue.nl/codes/Andw.html | 2026-11-18T14:05:56Z | 200 | aead90a9258c3dbdf728e431b235379833da646a32cd1ed73120a9e3eb4e5806 | A(52,8,7) = 3801Wu-7577, read from a text copy of the page (the table row for d=8, w=7, n=52); the page's source list says: Wu: Ken Wu, email 2026-11-11 with 27 new codes |

Compared cell: A(52,8,7). Live lower bound 3801 (label Wu, Ken Wu, email of 2026-11-11); live upper bound 7577. This object: 3802, margin 1. Dated note: on 2026-10-18 the cell listed 3799 (label Pl: a code from the merged V3R1T4S bigger-codes family), with the same upper bound.

Cell text is produced by `python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 52,8,7` on a page saved with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html`; expected output for the page of 2026-10-18 with the sha256 above: `52,8,7 | 3799Pl-7577 | mirror None`. The page has changed since: on 2026-11-18 the cell read `3801Wu-7577`. If the live page has changed again, compare the current cell text with these.

The page has no cell for the mirror A(52,8,45).
