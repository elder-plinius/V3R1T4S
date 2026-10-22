# The record we compare against

One honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the orchestrator.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| Andw.html | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:39:47Z | 200 | 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 | A(36,12,12) = LB:836 |

Live cell text: `836` (a lower-bound-only listing). The upper-bound part of the cell is not printed (the tool finds no printed upper bound for (36,12,12) or its mirror). The raw row or table block is in andw_cell_excerpt.txt.

## Table-implied upper bound

Save the page with `curl -A 'V3R1T4S-research (honest client; curl)' -o Andw.html https://aeb.win.tue.nl/codes/Andw.html` and run, from this folder:

```sh
python3 -I the-record-we-beat/tools/andw_cells.py Andw.html 36,12,12
python3 -I the-record-we-beat/tools/implied_ub.py Andw.html --extra 32,10,7=131 --extra 33,10,7=145 --extra 31,12,10=197 --extra 31,12,11=380 --extra 32,12,10=245 --extra 32,12,15=2511 --extra 32,12,16=2652 36,12,12
```

Expected (page with the sha256 above): `A(36,12,12) printed None implied 4275`. The script takes the minimum of the printed upper bound, the extra inputs, and the two Johnson rules A(n,d,w) <= floor(n/w * A(n-1,d,w-1)) and A(n,d,w) <= floor(n/(n-w) * A(n-1,d,w)) applied recursively. The extra inputs are merged V3R1T4S bounds: A(32,10,7) <= 131, A(33,10,7) <= 145, and the five cells of known-knowns/bigger-codes/INDEX_delsarte.csv at origin/main 04fdfba48c6e277fe083b6811f1a5deb3c52b74e (A(31,12,10) <= 197, A(31,12,11) <= 380, A(32,12,10) <= 245, A(32,12,15) <= 2511, A(32,12,16) <= 2652). The value depends on the page; if the live page has changed since the fetch above, compare the current output with the one recorded here.

Compared: certified bound 3613 against table-implied bound 4275 (direction: min).
