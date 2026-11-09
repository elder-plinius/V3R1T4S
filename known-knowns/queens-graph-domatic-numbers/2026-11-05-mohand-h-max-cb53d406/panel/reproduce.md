# Panel: REPRODUCE skeptic

context: subagent (Claude Code Agent tool, fresh context)

Inputs read: `CLAIM.md`, `REPRODUCE.md`, `dom-Q11-19-partition.txt` (all in claim/). Nothing else was opened.
I did not reuse any existing script. I wrote my own checker from the definitions in CLAIM.md.
Paths below are relative to claim/. Python 3.14.2, always run as `python -I`.

## Code written (in ../panel/reproduce-code/)

- `check_dom.py`: strict parser (ASCII only, exactly 11 lines, exactly 11 tokens per line, single spaces, tokens
  matching `[0-9]+`, reports CRLF/BOM/tab/non-ASCII) plus three domination tests per label L:
  1. brute force from the definition: every square is labelled L, or there is a distinct square labelled L in the same
     row, the same column, or with |r-r'| = |c-c'|;
  2. a different method (sets of occupied rows, columns, r-c diagonals and r+c anti-diagonals), checked to agree
     square by square with method 1;
  3. a control that ignores diagonals (rook moves only), to see whether the diagonal part of the test is used at all.
  It also reports the number of distinct labels, whether they run 0..k-1, duplicate rows and class sizes.
- `sanity_adjacency.py`: checks the adjacency function against known facts about Q_n (edge count n(n-1)(5n-1)/3,
  corner degree 3(n-1), centre degree 4(n-1) for odd n), to catch an off-by-one in the diagonals.
- `make_broken.py`: writes two broken copies in the same folder: `broken_one_label.txt` (one label changed so that one
  class stops dominating) and `broken_missing_square.txt` (one square removed).

## 1. sha256

Command (Git Bash): `sha256sum dom-Q11-19-partition.txt`

```
cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4 *claim/dom-Q11-19-partition.txt
```

This matches the value in CLAIM.md (`cb53d406...2f56e4`). check_dom.py computes the same hash in Python.
Caveat: the file uses CRLF line endings (11 CRLF, 314 bytes). The stated hash is over those raw bytes. A copy with LF
endings (for example after a git checkout with autocrlf, or a copy-paste) hashes to
`3beb06dc4cb19d7e3e5f690deaf36bf54d222d7ebd62a1eb541dbf25f160e78e`. The content is the same either way, but anyone
re-checking the hash needs the exact CRLF bytes.

## 2. Checker on the claimed partition

Command (from ../panel/reproduce-code/): `python -I check_dom.py ../../claim/dom-Q11-19-partition.txt 11 19`

```
file: ../../claim/dom-Q11-19-partition.txt
  bytes: 314
  sha256_raw: cb53d4061c8e751eef8943e967c5f42f3ef47a3f8d46b7c975a5e8f6cd2f56e4
  sha256_lf: 3beb06dc4cb19d7e3e5f690deaf36bf54d222d7ebd62a1eb541dbf25f160e78e
  crlf_count: 11
  lone_cr: 0
  tabs: 0
  non_ascii: 0
  bom: False
grid: 11 rows x [11] cols
cells: 121
distinct labels: 19  min=0 max=18  contiguous 0..k-1: True
duplicate rows: 0
class sizes: 0:6 1:6 2:6 3:6 4:6 5:6 6:6 7:6 8:6 9:6 10:6 11:6 12:6 13:6 14:7 15:7 16:7 17:8 18:8
size histogram: 6 (x14), 7 (x3), 8 (x2)
sum of class sizes: 121
  class  0 size 6: dominates
  class  1 size 6: dominates
  class  2 size 6: dominates
  class  3 size 6: dominates
  class  4 size 6: dominates
  class  5 size 6: dominates
  class  6 size 6: dominates
  class  7 size 6: dominates
  class  8 size 6: dominates
  class  9 size 6: dominates
  class 10 size 6: dominates
  class 11 size 6: dominates
  class 12 size 6: dominates
  class 13 size 6: dominates
  class 14 size 7: dominates
  class 15 size 7: dominates
  class 16 size 7: dominates
  class 17 size 8: dominates
  class 18 size 8: dominates
classes dominating (brute-force pairwise): 19/19
classes dominating (row/col/diag line sets): 19/19
control, classes dominating with rook moves only (no diagonals): 0/19
RESULT: PASS
exit=0
```

Class sizes match REPRODUCE.md exactly: 6 (x14), 7 (x3), 8 (x2), total 121.
The control line shows that no class dominates with rows and columns alone, so the diagonal test is used for
every class. The result does not come from a test that is too loose.

## 3. Adjacency sanity check (off-by-one in diagonals)

Command: `python -I sanity_adjacency.py`

```
n=4: edges=76 (formula 76), corner deg=9 (3(n-1)=9), min deg=9, max deg=11
n=8: edges=728 (formula 728), corner deg=21 (3(n-1)=21), min deg=21, max deg=27
n=11: edges=1980 (formula 1980), corner deg=30 (3(n-1)=30), min deg=30, max deg=40, centre deg=40 (4(n-1)=40)
exit=0
```

The adjacency used by the checker is exactly the queens graph: 1980 edges for Q_11, as the closed formula gives.

## 4. Checker on deliberately broken copies (it must fail)

Command: `python -I make_broken.py ../../claim/dom-Q11-19-partition.txt .`

```
broken_one_label: square (row 0, col 0) 0-based, label 0 -> 1; class 0 now leaves [(0, 0), (0, 1), (0, 3), (0, 8), (3, 0), (5, 5), (6, 6), (8, 0), (10, 0)] undominated
broken_missing_square: last token of row 4 (0-based) removed
exit=0
```

`python -I check_dom.py broken_one_label.txt 11 19` (excerpt; the other 18 classes still dominate):

```
class sizes: 0:5 1:7 2:6 3:6 4:6 5:6 6:6 7:6 8:6 9:6 10:6 11:6 12:6 13:6 14:7 15:7 16:7 17:8 18:8
size histogram: 5 (x1), 6 (x12), 7 (x4), 8 (x2)
sum of class sizes: 121
  class  0 size 5: DOES NOT dominate, undominated squares (row,col 0-based): [(0, 0), (0, 1), (0, 3), (0, 8), (3, 0), (5, 5), (6, 6), (8, 0), (10, 0)]
  ...
classes dominating (brute-force pairwise): 18/19
classes dominating (row/col/diag line sets): 18/19
RESULT: FAIL
exit=1
```

`python -I check_dom.py broken_missing_square.txt 11 19`:

```
PARSE ERRORS:
  line 4: expected 11 tokens, got 10
RESULT: FAIL (parse)
exit=1
```

The checker rejects both broken copies, so it can detect a failure.

## 5. Hand check of one class (no code)

Class 0 = (0,0), (1,10), (2,7), (4,2), (7,9), (9,4) (0-based row, col). Rows {0,1,2,4,7,9} and columns
{0,10,7,2,9,4} are covered. r-c in {0,-9,-5,2,-2,5}, r+c in {0,11,9,6,16,13}. I checked the 25 squares left over
(rows {3,5,6,8,10} x columns {1,3,5,6,8}) one by one. Each one is on one of these diagonals. Class 0 dominates, which
agrees with the program.

## Adversarial points checked

- Off-by-one in diagonals: the adjacency matches the known edge count and degrees of Q_n, and two methods agree.
- Labels: 19 distinct, contiguous 0..18. None are negative, non-integer or skipped.
- Missing or extra squares: 11 x 11 = 121 cells, the class sizes add up to 121, the parser is strict, and a missing
  square is rejected.
- Duplicate rows: none. Whitespace: single spaces only, no tabs, BOM or non-ASCII bytes. CRLF endings (see the
  sha256 caveat).
- Logic: a partition of all 121 squares into 19 dominating classes gives dom(Q_11) >= 19 directly from the
  definition in CLAIM.md. This does not contradict the upper bound of 20 quoted from Table 1, or the trivial bound
  min degree + 1 = 31.
- Out of scope for this skeptic: whether Table 1 / OEIS still list 18 as the best lower bound. I did not re-fetch
  any source; that is for another panel member.

## Verdict

Reproduced. The sha256 matches. The file is a valid partition of the 121 squares of the 11 x 11 board into 19
classes, and each class dominates Q_11 (19/19 under two independent methods and a hand check of class 0). Class sizes
are 6 (x14), 7 (x3), 8 (x2), as claimed. I could not find a computational flaw. The only reproducibility caveat is
that the stated hash depends on the CRLF line endings.

pass: true
