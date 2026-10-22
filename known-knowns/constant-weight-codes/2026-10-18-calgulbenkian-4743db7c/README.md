# constant-weight-codes: A(52,8,7) >= 3802 (table 3799)

## What

A word list of 3802 distinct binary words of length 52, weight exactly 7 and minimum pairwise distance 8 (>= 8, d even) was verified exactly, so A(52,8,7) >= 3802, strictly above the lower bound 3799 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 7577; the page has no mirror cell A(52,8,45); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.

The object `object/A52_8_7_3802.txt` (sha256 4743db7cec4929d05cba257484e8cce16c1f304d94efdb0b82d6870f191e473c) is that word list: one word per line, a 0/1 string of length 52.

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
| Brouwer, Bounds for binary constant weight codes (Andw.html) | A(52,8,7) | lower 3799 (label Pl), upper 7577; ours **3802** | https://aeb.win.tue.nl/codes/Andw.html | 2026-10-18T17:54:24Z |
| Echols, arXiv:2608.13906 (124 improved cells) | A(52,8,7) | 3796 | https://arxiv.org/abs/2608.13906 | 2026-10-18T17:55:12Z |
| Lysenstoen, arXiv:2607.19550 | A(52,8,7) | not among the cells in its abstract | https://arxiv.org/abs/2607.19550 | 2026-10-18T17:54:45Z |
| V3R1T4S `known-knowns/bigger-codes/INDEX.csv` (merged family; the source of the live cell's code) | A(52,8,7) | 3799 | https://github.com/elder-plinius/V3R1T4S/blob/main/known-knowns/bigger-codes/INDEX.csv | 2026-10-18T17:55:29Z |

The page sha256 was 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349 on every fetch. The table has no cell for the mirror A(52,8,45). The panel's novelty skeptic read the Echols table in full, checked the V3R1T4S trophy case and pull request pages 1 to 5, and found no competing value for this cell; its report is `panel/novelty.md`. Snapshot metadata, with HTTP status and page sha256: `the-record-we-beat/README.md`.

## Not claimed

- Nothing is claimed for any other cell, for an upper bound, or for a cell of a different n, d or w. One cell per package.
- The margin is 3 over the live table value 3799, which is itself a polished code from the merged bigger-codes family. Records in this table move often; the comparison holds for the table version recorded here.
- The comparison with the two arXiv papers rests on their values as read by the panel's novelty skeptic (Echols) and the abstract-level search (Lysenstoen); papers other than Echols were not read in full.
- The code was found by a randomised search whose exact run commands were not recorded (`how-we-built-it/README.md`). The object does not depend on the search: it is checked on its own.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here. The table maintainer has not been sent the code by this package.

## Filing history

The contributor filed the same value as pull request #56, which was closed unmerged on 2026-10-14 in the bulk close of about thirty early pull requests during a handoff between sessions, not for a defect. This package is a refile.

## Credits

- **Andries E. Brouwer**, *Bounds for binary constant weight codes*, https://aeb.win.tue.nl/codes/Andw.html: the table of record and the code archive this cell's values come from.
- **Seed of the live cell's code**: Jordan Boisclair [Bo] archive code a52.8.7.3797H, as recorded for A(52,8,7) in the V3R1T4S bigger-codes family (`INDEX.csv`, seed and credit). The live cell's code is from the merged V3R1T4S bigger-codes family (https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns/bigger-codes, label Pl), which polished archive codes by Jordan Boisclair, William Echols, Andries Brouwer and others; this object is a further improvement of that code, so please credit them too.
- **William Echols**, arXiv:2608.13906, and **Lysenstoen**, arXiv:2607.19550: the recent papers compared against; Echols' value for this cell is 3796.
- **Argon**, the contributor's AI search agent (Gemini), author of `how-we-built-it/cwc_search.c`; contributor credit: `calgulbenkian`.
