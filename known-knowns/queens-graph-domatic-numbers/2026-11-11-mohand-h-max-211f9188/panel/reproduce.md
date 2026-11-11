# REPRODUCE skeptic report: tdom(Q_10) >= 16

context: subagent (Claude Code Agent tool, fresh context)

Scope: I read only the three files in `claim/` (CLAIM.md, REPRODUCE.md, tdom-Q10-16-partition.txt). The package holds no
author code, and I read no other file of the project. My checker was written from the definition below and nothing else.
Everything I wrote is in `panel/reproduce-code/`. Every command was run from the run folder (the parent of `claim/` and
`panel/`) with `python -I -B` (Python 3.14.2), on one thread. No network was used.

## Definition checked (quoted verbatim from claim/CLAIM.md)

> Q_n has the n^2 squares as vertices; two distinct squares are adjacent iff they share a row, a column or a diagonal.
> A set D totally dominates if every square of the board, the squares of D included, is adjacent to a member of D (a
> square is never adjacent to itself). tdom(Q_n) is the largest k such that the squares split into k disjoint total
> dominating sets.

How I read it: D is a total dominating set iff N(v) ∩ D ≠ ∅ for every square v, where N(v) is the OPEN neighbourhood
(v itself excluded). A member of D therefore needs a different member of D on its row, column or diagonal. Plain
domination (v ∈ D or N(v) ∩ D ≠ ∅) is weaker. My checker has it only as a deliberately wrong control mode
(`--mode plain`). The proof needs one step. If the 100 squares split into 16 pairwise disjoint total dominating sets,
then by the definition tdom(Q_10) >= 16. So the claim reduces to properties of the saved grid: (i) it is a partition of
the 100 squares, (ii) it has exactly 16 classes, (iii) each class totally dominates Q_10.

## Files written

- `panel/reproduce-code/tdom_check.py` (sha256 ccc7cac21612ea9c3448f3732a720d0a136674bda650f2e12c28893e73a7b622) is the
  checker. It parses strictly (ASCII only, no BOM, consistent line endings, no empty lines, canonical decimal tokens,
  square board) and checks the raw-byte hash. It builds the adjacency from the definition and checks it is symmetric and
  irreflexive, then counts the edges against the closed form n(n-1)(5n-1)/3. It then runs two independent total
  domination tests per class. A is set based: N(v) ∩ D ≠ ∅ for all v. B uses line counts: some row, column or diagonal
  through v holds a member of D other than v. If A and B disagree, the result is a FAIL.
- `panel/reproduce-code/controls.py` (sha256 472cf8fe60ae079f8ce26a0231ce0015b5b9db41bf4999dbc712a6b46ea6afc3) holds
  the sensitivity controls. It writes corrupted or control copies into `panel/reproduce-code/corrupt/` and never writes
  to `claim/`.
- `panel/reproduce-code/out/` holds the saved outputs: check-run1/2, controls-run1/2 and rule-*.

## 1. Raw-byte hash (three independent tools)

```
$ sha256sum claim/tdom-Q10-16-partition.txt
211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec *claim/tdom-Q10-16-partition.txt
$ wc -c claim/tdom-Q10-16-partition.txt
250 claim/tdom-Q10-16-partition.txt
$ od -c claim/tdom-Q10-16-partition.txt | head -2
0000000   1   3       0       1       2       1   4       3       4    
0000020   5       6       7  \r  \n   0       1       2       1   5    
$ tr -d '\r' < claim/tdom-Q10-16-partition.txt | sha256sum
cb3583332b8beb836a61d080eae4f645d27ba8cc513c0e682d45b7a61030f396 *-
PS> (Get-FileHash -Algorithm SHA256 -LiteralPath "claim\tdom-Q10-16-partition.txt").Hash.ToLower()
211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec
```

Both hashes stated in CLAIM.md match: the raw CRLF hash and the LF-normalised hash.

## 2. Main check of the claimed object

```
$ python -I -B panel/reproduce-code/tdom_check.py claim/tdom-Q10-16-partition.txt --n 10 --k 16 \
    --expect-sha256 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec --show-grid
file: claim/tdom-Q10-16-partition.txt
bytes: 250
sha256(raw bytes)      = 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec
sha256(CRLF->LF bytes) = cb3583332b8beb836a61d080eae4f645d27ba8cc513c0e682d45b7a61030f396
raw hash equals expected 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec: yes
line endings: 10 CRLF, 0 lone LF, 0 lone CR; ends with newline: True
parsed board: 10 x 10
  13  0  1  2 14  3  4  5  6  7
   0  1  2 15 14 15  9  4  5  6
   1  2  8 12  7 13  0 11  4  5
   2  6  3  1  6 10 10 12 14  4
   9 15  5 10 10  4  9 15 15 15
  15 14 13  0 11  8 10  7  1  0
  11 14 12 12 10  3  2  6  3  8
   7 11  4  9 14  5 12 12  8 13
   3  7 11  0 15  1 14  8 13  9
   5  3  7 11  6 14  8 13  9  2
adjacency rule queen on 10x10: symmetric=True irreflexive=True edges=1470
closed form for queen edges n(n-1)(5n-1)/3 = 1470
distinct labels: 16 -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
class sizes: 0:6, 1:6, 2:6, 3:6, 4:6, 5:6, 6:6, 7:6, 8:6, 9:6, 10:6, 11:6, 12:6, 13:6, 14:8, 15:8
size histogram (size: count): 6: 14, 8: 2 ; sum of sizes = 100
rule=queen mode=total
class  0 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  1 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  2 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  3 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  4 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  5 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  6 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  7 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  8 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class  9 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class 10 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class 11 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class 12 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class 13 size 6: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class 14 size 8: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
class 15 size 8: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=1
classes that total-dominate under rule queen: 16 of 16
VERDICT: PASS
```

Exit code 0. The output matches what REPRODUCE.md expects: 16 labels, sizes 6 (x14) and 8 (x2), sum 100, and every
class totally dominates. Each square carries exactly one label, so the classes are disjoint and cover the board. The
checker also re-checks this explicitly.

The edge count is derived by hand, not taken from the code. Rows and columns give 2·10·C(10,2) = 900 edges. Diagonals in
both directions give 2·(2·C(10,3) + C(10,2)) = 2·(240 + 45) = 570. Total: 1470, which is the edge count printed above
and the closed form. The rook and bishop rule runs below print 900 and 570 separately.

Hand spot check of class 0, from the witness table in controls output [9]. Class 0 is
{(0,1),(1,0),(2,6),(5,3),(5,9),(8,3)}. Each member is attacked by another member:
- (0,1) and (1,0) are on the anti-diagonal r+c=1.
- (2,6) and (5,3) are on the anti-diagonal r+c=8.
- (5,3) and (5,9) share row 5.
- (5,3) and (8,3) share column 3.

The table also lists, for each of the 100 squares, one other class-0 square attacking it. For example, square (0,1) is
attacked by (1,0), not by itself.

## 3. Total vs plain domination: the checker tells them apart

Control 1 is Q_3 with classes {centre} and {the 8 other squares}. This is a domatic 2-partition (the centre attacks all
8 other squares), but the singleton class is not a total dominating set:

```
$ python -I -B panel/reproduce-code/tdom_check.py panel/reproduce-code/corrupt/q3-domatic-not-total.txt --n 3 --k 2 --mode plain --show-grid
...
class  0 size 1: plain-dominates(A)=yes
class  1 size 8: plain-dominates(A)=yes
classes that plain-dominate under rule queen: 2 of 2
VERDICT: PASS            (exit=0)
$ ... same file --mode total
class  0 size 1: total-dominates(A)=NO total-dominates(B lines)=NO plain-dominates=yes min #class-neighbours over all squares=0 undominated=[(1, 1)]
class  1 size 8: total-dominates(A)=yes total-dominates(B lines)=yes plain-dominates=yes min #class-neighbours over all squares=5
classes that total-dominate under rule queen: 1 of 2
reasons for FAIL:
  - class 0 does not total-dominate (1 squares missed)
VERDICT: FAIL            (exit=1)
```

Control 2 is a 10x10 grid. I tried every swap of two differently labelled squares of the claimed grid (4684 swaps). Two
of the swapped grids are still plain domatic 16-partitions but are no longer total domatic. The first one, which swaps
(3,6) and (6,3), is saved as `corrupt/q10-swap-domatic-not-total.txt`. In it, class 10 becomes
{(3,5),(6,3),(4,3),(4,4),(5,6),(6,4)}, and its member (5,6) has no other class-10 square on its row, column or diagonals.

```
$ ... corrupt/q10-swap-domatic-not-total.txt --n 10 --k 16 --mode plain
classes that plain-dominate under rule queen: 16 of 16
VERDICT: PASS            (exit=0)
$ ... corrupt/q10-swap-domatic-not-total.txt --n 10 --k 16 --mode total
class 10 size 6: total-dominates(A)=NO total-dominates(B lines)=NO plain-dominates=yes min #class-neighbours over all squares=0 undominated=[(5, 6)]
class 12 size 6: total-dominates(A)=NO total-dominates(B lines)=NO plain-dominates=yes min #class-neighbours over all squares=0 undominated=[(2, 3), (6, 2)]
classes that total-dominate under rule queen: 14 of 16
  - class 10 does not total-dominate (1 squares missed)
  - class 12 does not total-dominate (2 squares missed)
VERDICT: FAIL            (exit=1)
```

A checker that only tested plain domination would accept both control grids. Mine rejects both in total mode.

## 4. Sensitivity controls

### Wrong adjacency rules, run on the claimed grid through the CLI

```
rule=queen exit=0 :: symmetric=True irreflexive=True edges=1470 :: classes that total-dominate under rule queen: 16 of 16 :: VERDICT: PASS
rule=rook exit=1 :: symmetric=True irreflexive=True edges=900 :: classes that total-dominate under rule rook: 0 of 16 :: VERDICT: FAIL
rule=bishop exit=1 :: symmetric=True irreflexive=True edges=570 :: classes that total-dominate under rule bishop: 0 of 16 :: VERDICT: FAIL
rule=king exit=1 :: symmetric=True irreflexive=True edges=342 :: classes that total-dominate under rule king: 0 of 16 :: VERDICT: FAIL
rule=queen-main-diag-only exit=1 :: symmetric=True irreflexive=True edges=1185 :: classes that total-dominate under rule queen-main-diag-only: 0 of 16 :: VERDICT: FAIL
rule=queen-anti-diag-only exit=1 :: symmetric=True irreflexive=True edges=1185 :: classes that total-dominate under rule queen-anti-diag-only: 0 of 16 :: VERDICT: FAIL
rule=queen-no-rows exit=1 :: symmetric=True irreflexive=True edges=1020 :: classes that total-dominate under rule queen-no-rows: 0 of 16 :: VERDICT: FAIL
rule=queen-no-cols exit=1 :: symmetric=True irreflexive=True edges=1020 :: classes that total-dominate under rule queen-no-cols: 0 of 16 :: VERDICT: FAIL
```

Dropping any one of the four line families turns the verdict to FAIL. The "plain" (closed neighbourhood) mode cannot
reject a valid total domatic partition, because total domination implies plain domination. Section 3 shows its
discriminating power on the two control grids.

### Corrupted copies (files in `panel/reproduce-code/corrupt/`)

```
q10-one-label-changed: exit with hash check=1 ; exit math-only (no hash)=1
q10-swap-domatic-not-total: exit with hash check=1 ; exit math-only (no hash)=1
q10-merged-14-15: exit with hash check=1 ; exit math-only (no hash)=1
q10-line-deleted: exit with hash check=1 ; exit math-only (no hash)=1
q10-extra-token: exit with hash check=1 ; exit math-only (no hash)=1
q10-label-16: exit with hash check=1 ; exit math-only (no hash)=1
q10-LF-copy: exit with hash check=1 ; exit math-only (no hash)=0
claimed file: exit with hash check=0
```

Why each copy failed:
- **one-label-changed** ((0,0) relabelled 13 -> 0): class 13 does not total-dominate (6 squares missed).
- **merged-14-15:** all 15 classes totally dominate, but there are 15 distinct labels, not 16.
- **label-16:** 17 distinct labels.
- **line-deleted / extra-token:** parse errors.
- **LF-copy:** the same mathematical object. Only the raw hash rejects it, and as expected its hash equals the LF hash
  stated in CLAIM.md (cb3583...f396).

Excerpts from those runs:

```
=== q10-one-label-changed (total mode, expect claimed hash) ===
raw hash equals expected 211f...034ec: NO
classes that total-dominate under rule queen: 15 of 16
  - raw sha256 mismatch
  - class 13 does not total-dominate (6 squares missed)
VERDICT: FAIL
=== q10-merged-14-15 (total mode, expect claimed hash) ===
distinct labels: 15 -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
classes that total-dominate under rule queen: 15 of 15
  - raw sha256 mismatch
  - 15 distinct labels, expected 16
  - label set is not exactly 0..15
VERDICT: FAIL
=== q10-label-16 (total mode, expect claimed hash) ===
distinct labels: 17 -> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
  - class 16 does not total-dominate (73 squares missed)
VERDICT: FAIL
```

### Exhaustive mutation sweeps and other controls (controls.py, full output in out/controls-run1.txt)

```
[0] re-serialised grid (CRLF) equals raw file bytes: True
[2] swaps tried: 4684 ; still total domatic: 1 ; still plain domatic: 3 ; plain-but-not-total: 2
[4] mutants: 1500 ; with the claimed raw hash: 0 ; still a valid 16-class total domatic partition: 0
[5] class  0 size 6: members whose removal keeps total domination: []
    ... (same empty list for all 16 classes, including the two of size 8)
[6] merged grids whose 15 classes all totally dominate: 120 of 120 (rejected only by the label count)
[7] image 0: valid=True raw-hash-equal=True
    image 1..7: valid=True raw-hash-equal=False
```

Reading:
- **[4]** No single-square relabel survives. Every one of the 1500 one-cell mutants is rejected by the mathematics, not
  only by the hash.
- **[5]** Every class, including the two classes of size 8, is a minimal total dominating set.
- **[2]** Exactly one swap gives another valid partition. It is a different object, and the hash rejects it as a copy of
  the claim.
- **[7]** All 8 board symmetries of the grid are again valid, as they must be. This is a sanity check that the checker
  has no orientation bias.

## 5. Determinism

```
check run 1 exit=0
check run 2 exit=0
controls run 2 exit=0
1310d9806a11e8283529dfc20eafd463eba6ffb551d3a9169ba2f7de2c63ba99 *panel/reproduce-code/out/check-run1.txt
1310d9806a11e8283529dfc20eafd463eba6ffb551d3a9169ba2f7de2c63ba99 *panel/reproduce-code/out/check-run2.txt
94b94e309df01743c08fa2e5b79ecfd5286e797172ca515cd66e8a27bcf20af1 *panel/reproduce-code/out/controls-run1.txt
94b94e309df01743c08fa2e5b79ecfd5286e797172ca515cd66e8a27bcf20af1 *panel/reproduce-code/out/controls-run2.txt
check runs identical
controls runs identical
211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec *claim/tdom-Q10-16-partition.txt
```

With `-I`, Python ignores PYTHONHASHSEED, so each run used a fresh random hash seed. The outputs are byte-identical, so
nothing depends on set ordering. The last line shows that the claimed file was unchanged after all runs. The whole check
is deterministic: it fully checks one given object and runs no search, so no sampling is involved.

## 6. What I did not check (outside the reproduce role, or not part of the proof)

- **Bibliographic status.** I did not check that Table 1 of Lauri's Corrigendum lists tdom(Q_10) as 15-16, that the
  interval is still open elsewhere, or the OEIS state. The PDF and its hash are not in the package, and I used no
  network. The mathematical statement tdom(Q_10) >= 16 does not depend on them. Whether 16 is new does.
- **Upper bound.** The upper bound tdom(Q_10) <= 16 is not claimed and not re-proved, as CLAIM.md says.
- **Search method.** I did not reproduce the provenance claim "exhaustive list of the 216 total dominating 6-sets of
  Q_10" (C(100,6) is about 1.2e9 subsets, not a light computation). The lower bound does not use it.

## Verdict

The saved object is exactly the file with the stated raw hash (and the stated LF hash after normalisation). It is a
partition of the 100 squares of the 10x10 board into exactly 16 classes, labelled 0..15, with sizes 6 (x14) and 8 (x2).
Two independent implementations agree that every class totally dominates Q_10 with open neighbourhoods, so every member
of every class is attacked by a different member of its own class. By the quoted definition this gives tdom(Q_10) >= 16.
The checker rejects:
- plain-but-not-total partitions,
- every corrupted copy,
- every wrong adjacency rule tried.

Its results are deterministic.

pass: true
