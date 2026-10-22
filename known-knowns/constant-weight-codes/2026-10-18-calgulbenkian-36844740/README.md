# constant-weight-codes: A(51,6,6) >= 11187 (table 11184)

## What

A word list of 11187 distinct binary words of length 51, weight exactly 6 and minimum pairwise distance 6 (>= 6, d even) was verified exactly, so A(51,6,6) >= 11187, strictly above the lower bound 11184 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 16660; the page has no mirror cell A(51,6,45); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.

The object `object/A51_6_6_11187.txt` (sha256 3684474037a4c99801649121c6515c307e50684c4652135eaba3767b5a1c1df5) is that word list: one word per line, a 0/1 string of length 51.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (numpy is optional and adds a second check).
- **Rough laptop time**: under one minute (measured 0.3 seconds).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| Brouwer, Bounds for binary constant weight codes (Andw.html) | A(51,6,6) | lower 11184 (label Pl), upper 16660; ours **11187** | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z |
| Echols, arXiv:2608.13906 (124 improved cells) | A(51,6,6) | not listed | https://arxiv.org/abs/2608.13906 | 2026-10-18T17:55:12Z |
| Lysenstoen, arXiv:2607.19550 | A(51,6,6) | not among the cells in its abstract | https://arxiv.org/abs/2607.19550 | 2026-10-18T17:54:45Z |
| V3R1T4S `known-knowns/bigger-codes/INDEX.csv` (merged family; the source of the live cell's code) | A(51,6,6) | 11184 | https://github.com/elder-plinius/V3R1T4S/blob/main/known-knowns/bigger-codes/INDEX.csv | 2026-10-18T17:55:29Z |

The page sha256 was 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 on every fetch. The table has no cell for the mirror A(51,6,45). The panel's novelty skeptic read the Echols table in full (this cell is not in it), checked the V3R1T4S trophy case and pull request pages 1 to 5, and found no competing value for this cell; its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Nothing is claimed for any other cell, for an upper bound, or for a cell of a different n, d or w. One cell per package.
- The margin is 3 over the live table value 11184, which is itself a polished code from the merged bigger-codes family. Records in this table move often; the comparison holds for the table version recorded here.
- The comparison with the two arXiv papers rests on their values as read by the panel's novelty skeptic (Echols) and the abstract-level search (Lysenstoen); papers other than Echols were not read in full.
- The code was found by a randomised search whose exact run commands were not recorded (`how-we-built-it/README.md`). The object does not depend on the search: it is checked on its own.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here. The table maintainer has not been sent the code by this package.

## Filing history

No earlier filing of this cell by the contributor is known; the panel's novelty report found no earlier pull request for it.

## Credits

- **Andries E. Brouwer**, *Bounds for binary constant weight codes*, https://aeb.win.tue.nl/codes/Andw.html: the table of record and the code archive this cell's values come from.
- **Seed of the live cell's code**: Jordan Boisclair [Bo] archive code a51.6.6.11156H, as recorded for A(51,6,6) in the V3R1T4S bigger-codes family (`INDEX.csv`, seed and credit). The live cell's code is from the merged V3R1T4S bigger-codes family (https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/bigger-codes, label Pl), which polished archive codes by Jordan Boisclair, William Echols, Andries Brouwer and others; this object is a further improvement of that code, so please credit them too.
- **William Echols**, arXiv:2608.13906, and **Lysenstoen**, arXiv:2607.19550: the recent papers compared against.
- **Argon**, the contributor's AI search agent (Gemini), author of `how-we-built-it/cwc_search.c`; contributor credit: `calgulbenkian`.
