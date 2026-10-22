# constant-weight-codes: A(28,8,11) >= 3802 (table 3785)

## What

A word list of 3802 distinct binary words of length 28, weight exactly 11 and minimum pairwise distance 8 (>= 8, d even) was verified exactly, so A(28,8,11) >= 3802, strictly above the lower bound 3785 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 11896; the page has no mirror cell A(28,8,17); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.

The object `object/A28_8_11_3802.txt` (sha256 9bec8e442ef7b35ee427a3dd311c77ae66677b1a0e38cd95d03756e1ea4ae335) is that word list: one word per line, a 0/1 string of length 28.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (numpy is optional and adds a second check).
- **Rough laptop time**: under one minute (measured 0.5 seconds).
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| Brouwer, Bounds for binary constant weight codes (Andw.html) | A(28,8,11) | lower 3785 (label Pl), upper 11896; ours **3802** | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z |
| Echols, arXiv:2608.13906 (124 improved cells) | A(28,8,11) | not listed | https://arxiv.org/abs/2608.13906 | 2026-10-18T17:55:12Z |
| Lysenstoen, arXiv:2607.19550 | A(28,8,11) | not among the cells in its abstract | https://arxiv.org/abs/2607.19550 | 2026-10-18T17:54:45Z |
| V3R1T4S `known-knowns/bigger-codes/INDEX.csv` (merged family; the source of the live cell's code) | A(28,8,11) | 3785 | https://github.com/elder-plinius/V3R1T4S/blob/main/known-knowns/bigger-codes/INDEX.csv | 2026-10-18T17:55:29Z |

The page sha256 was 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 on every fetch. The table has no cell for the mirror A(28,8,17). The panel's novelty skeptic read the Echols table in full (this cell is not in it), checked the V3R1T4S trophy case and pull request pages 1 to 5, and found no competing value for this cell; its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Nothing is claimed for any other cell, for an upper bound, or for a cell of a different n, d or w. One cell per package.
- The margin is 17 over the live table value 3785, which is itself a polished code from the merged bigger-codes family. Records in this table move often; the comparison holds for the table version recorded here.
- The comparison with the two arXiv papers rests on their values as read by the panel's novelty skeptic (Echols) and the abstract-level search (Lysenstoen); papers other than Echols were not read in full.
- The code was found by a randomised search whose exact run commands were not recorded (`how-we-built-it/README.md`). The object does not depend on the search: it is checked on its own.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here. The table maintainer has not been sent the code by this package.

## Filing history

No earlier filing of this cell by the contributor is known; the panel's novelty report found no earlier pull request for it.

## Credits

- **Andries E. Brouwer**, *Bounds for binary constant weight codes*, https://aeb.win.tue.nl/codes/Andw.html: the table of record and the code archive this cell's values come from.
- **Seed of the live cell's code**: Brouwer archive code a28.8.11.3773H (unlabelled, 2010), as recorded for A(28,8,11) in the V3R1T4S bigger-codes family (`INDEX.csv`, seed and credit). The live cell's code is from the merged V3R1T4S bigger-codes family (https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/bigger-codes, label Pl), which polished archive codes by Jordan Boisclair, William Echols, Andries Brouwer and others; this object is a further improvement of that code, so please credit them too.
- **William Echols**, arXiv:2608.13906, and **Lysenstoen**, arXiv:2607.19550: the recent papers compared against.
- **Argon**, the contributor's AI search agent (Gemini), author of `how-we-built-it/cwc_search.c`; contributor credit: `calgulbenkian`.
