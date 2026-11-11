# REPRODUCE skeptic report: dom(Q_12) >= 21

context: subagent (Claude Code Agent tool, fresh context)

Date: 2026-11-11. Inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/dom-Q12-21-partition.txt (a listing of claim/
shows these three files and nothing else). No author code, notes or other run folders were read. The checker below was
written from the definition only. Runtime: Python 3.14.2, every script run with `python -I`, one thread, standard
library only. All commands run from the run folder.

## Definition (quoted verbatim from claim/CLAIM.md)

> Q_n has the n^2 squares as vertices; two distinct squares are adjacent iff they share a row, a column or a diagonal.
> A set D dominates if every square is in D or adjacent to a member of D. dom(Q_n) is the largest k such that the
> squares split into k disjoint dominating sets.

Claimed value: the file is a partition of the 144 squares of the 12 x 12 board into 21 classes (labels 0..20), each
dominating Q_12, hence dom(Q_12) >= 21. Claimed raw sha256 e5ea8659...b1b2e, LF-normalised sha256 bc2433e6...266cb7.

## My checker (panel/reproduce-code/check_partition.py)

- Hash: sha256 of the raw bytes, and of the bytes with CRLF replaced by LF, compared to both claimed values.
- Strict parse: ASCII, no BOM, no bare CR, exactly 12 lines of exactly 12 single-space-separated tokens, each token a
  non-negative integer without sign or leading zeros.
- Partition: labels must be exactly {0..20} (21 classes); every square in exactly one class; sizes sum to 144.
- Domination of each class by three independent methods that must agree:
  A. the literal definition: each square not in D is tested against every member of D with the rule "distinct, and
     same row, same column or |r-r'| = |c-c'|";
  B. line occupancy: a square is attacked iff its row, column, r-c line or r+c line holds a member of D;
  C. closed neighbourhoods built by walking the 8 queen rays to the board edge.
- Self-test of the adjacency before use: method C equals the pairwise rule on all 144 x 144 ordered pairs, and the
  edge count of Q_12 equals the closed form n(n-1)(5n-1)/3.
- Informational: for each class, how many members are redundant (removal keeps domination).

### Output on the claimed object

```
$ python -I panel/reproduce-code/check_partition.py claim/dom-Q12-21-partition.txt
file: claim/dom-Q12-21-partition.txt
adjacency self-test: ray-walk == pairwise rule on all 20736 ordered pairs: True
edges of Q_12: 2596 (closed form n(n-1)(5n-1)/3 = 2596)
sha256(raw bytes)      = e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e
  matches claimed raw  : True
sha256(CRLF->LF bytes) = bc2433e6874495f692cf019621059178394cdafde073b9956262ea8f0b266cb7
  matches claimed LF   : True
parse note: bytes=377 CRLF=12 bare_LF=0 bare_CR=0 tabs=0
parse note: final newline: yes
PARSE: ok, 12 rows x 12 cols = 144 cells
distinct labels: 21, min 0, max 20
labels == {0..20}: True
sum of class sizes = 144 (n^2 = 144)
classes pairwise disjoint and cover all squares: True
class  0 size 6 undominated A/B/C = 0/0/0  redundant members 0  squares 0,0 2,4 4,10 6,6 8,2 10,8
class  1 size 6 undominated A/B/C = 0/0/0  redundant members 0  squares 0,11 2,3 4,9 6,5 8,1 10,7
class  2 size 6 undominated A/B/C = 0/0/0  redundant members 0  squares 1,3 3,9 5,5 7,1 9,7 11,11
class  3 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 3,8 4,6 5,3 5,4 6,7 7,5 8,8
class  4 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,1 1,9 3,7 5,1 7,11 9,5 11,3
class  5 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,1 1,0 3,5 5,11 7,7 9,3 11,9
class  6 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,7 2,1 4,3 6,9 8,11 9,2 10,5
class  7 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,5 2,11 4,7 6,3 8,9 10,0 11,1
class  8 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,8 2,6 4,0 6,10 8,4 9,9 10,2
class  9 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,5 3,3 3,11 5,0 7,9 9,1 11,7
class 10 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,11 2,5 5,9 6,2 9,6 10,1 10,10
class 11 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,9 1,7 3,1 5,7 7,3 9,11 11,5
class 12 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,2 2,8 4,4 6,0 8,6 10,11 11,10
class 13 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,4 2,2 2,10 4,2 6,8 8,0 10,6
class 14 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,10 2,9 4,1 4,5 6,11 8,7 10,3
class 15 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,6 2,0 4,8 6,4 8,10 10,4 11,2
class 16 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,4 3,6 3,10 5,2 7,8 9,8 11,0
class 17 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 0,3 1,10 2,7 4,11 6,1 8,5 10,9
class 18 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,2 3,4 5,10 7,6 8,3 9,0 11,8
class 19 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,6 3,0 5,8 7,2 7,4 9,10 11,4
class 20 size 7 undominated A/B/C = 0/0/0  redundant members 0  squares 1,8 3,2 5,6 7,0 7,10 9,4 11,6
size histogram: 6 x3, 7 x18
classes dominating: 21 / 21
VERDICT: PASS
EXIT: PASS
exit=0
```

Every expectation in claim/REPRODUCE.md is met: raw hash matches; 21 distinct labels; all 21 classes dominate;
class sizes 6 (x3) and 7 (x18), summing to 144.

### Hash cross-check with an independent tool (raw bytes, not Python)

```
$ sha256sum claim/dom-Q12-21-partition.txt
e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e *claim/dom-Q12-21-partition.txt
$ tr -d '\r' < claim/dom-Q12-21-partition.txt | sha256sum
bc2433e6874495f692cf019621059178394cdafde073b9956262ea8f0b266cb7 *-
$ wc -c -l claim/dom-Q12-21-partition.txt
 12 377 claim/dom-Q12-21-partition.txt
```

Both claimed hashes reproduce (raw CRLF and LF-normalised).

## Re-derivation of the proof step

The claim has one step: by the quoted definition, dom(Q_12) is the largest k for which the 144 squares split into k
disjoint dominating sets. The file gives such a split with k = 21 (disjoint, covering all 144 squares, each class
dominating, all verified above), so the largest such k is at least 21. Nothing else is claimed; the upper bound
dom(Q_12) <= 21 is attributed to Lauri and is not re-proved, and I did not check it.

## Sensitivity controls (panel/reproduce-code/controls.py)

```
$ python -I panel/reproduce-code/controls.py claim/dom-Q12-21-partition.txt panel/reproduce-code
[EXPECTED] K0 re-serialisation (CRLF) is byte-identical to the file: expected verdict PASS, got PASS 
[EXPECTED] K0 baseline full verify: expected verdict PASS, got PASS 
[EXPECTED] K1 one-byte change, full verify: expected verdict FAIL, got FAIL (raw hash match: False)
[EXPECTED] K2 cell (0,0) moved from class 0 to 1 (hash ignored): expected verdict FAIL, got FAIL (class 0 now leaves undominated [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 11), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (11, 0)])
[EXPECTED] K3 all 2880 single-cell relabels rejected: expected verdict PASS, got PASS (0 still pass)
[EXPECTED] K4 merge class 20 into 19 (20 labels; all 20 classes dominate: True): expected verdict FAIL, got FAIL 
[EXPECTED] K5 wrong rule 'rook (row/col only)': expected verdict FAIL, got FAIL (21/21 classes fail)
[EXPECTED] K5 wrong rule 'queen without anti-diagonals': expected verdict FAIL, got FAIL (21/21 classes fail)
[EXPECTED] K5 wrong rule 'queen without main diagonals': expected verdict FAIL, got FAIL (21/21 classes fail)
[EXPECTED] K5 wrong rule 'queen with diagonals only up to distance 5': expected verdict FAIL, got FAIL (21/21 classes fail)
[EXPECTED] K5 wrong rule 'bishop (diagonals only)': expected verdict FAIL, got FAIL (21/21 classes fail)
[EXPECTED] K5 wrong rule 'king': expected verdict FAIL, got FAIL (21/21 classes fail)
[EXPECTED] K5 control rule 'queen' via custom-rule path: expected verdict PASS, got PASS 
[EXPECTED] K5 too-generous rule 'all distinct squares adjacent': expected verdict PASS, got PASS 
[EXPECTED] K6 200 seeded shuffles (same size multiset) all rejected: expected verdict PASS, got PASS (0 pass; best shuffle had 0/21 dominating classes)
[EXPECTED] K7 truncated to 11 lines: expected verdict FAIL, got FAIL (PARSE: FAIL (expected 12 lines, got 11))
[EXPECTED] K7 extra token on line 1: expected verdict FAIL, got FAIL (PARSE: FAIL (line 1: expected 12 single-space-separated tokens, got 13))
[EXPECTED] K7 non-integer token: expected verdict FAIL, got FAIL (PARSE: FAIL (line 1: bad token 'x'))
[EXPECTED] K7 negative token: expected verdict FAIL, got FAIL (PARSE: FAIL (line 1: bad token '-0'))
[EXPECTED] K7 UTF-8 BOM prefix: expected verdict FAIL, got FAIL (PARSE: FAIL (UTF-8 BOM present))
[EXPECTED] K7 one label 20 -> 21 (22 labels): expected verdict FAIL, got FAIL (labels == {0..20}: False; classes dominating: 20 / 22)
[EXPECTED] K8 LF copy, structure only: expected verdict PASS, got PASS (matches claimed LF   : True)
[EXPECTED] K8 LF copy, full verify against claimed raw hash: expected verdict FAIL, got FAIL 
[EXPECTED] K9 symmetry 'transpose' (hash ignored): expected verdict PASS, got PASS 
[EXPECTED] K9 symmetry 'rotate 90' (hash ignored): expected verdict PASS, got PASS 
[EXPECTED] K9 symmetry 'mirror' (hash ignored): expected verdict PASS, got PASS 
[EXPECTED] K9 non-symmetry 'cyclic column shift by 1': expected verdict FAIL, got FAIL (5/21 classes dominate)
controls behaving as expected: 27 / 27
CONTROLS: ALL EXPECTED
exit=0
```

Reading of the controls: any single-byte change breaks the hash (K1); because every class is a minimal dominating set,
every one of the 2880 possible single-cell relabels is rejected (K3), and the corrupted copy written to disk is
rejected by the command-line checker with a non-zero exit (below); merging two classes is caught by the label count
even though every class still dominates (K4); every weakened adjacency rule makes all 21 classes fail (K5), so the
verdict really depends on both diagonal directions at full range; random relabellings with the same class sizes never
pass (K6); malformed files are rejected at parse (K7); the board symmetries preserve the verdict while a non-symmetry
breaks it (K9).

```
$ python -I panel/reproduce-code/check_partition.py panel/reproduce-code/control-corrupt-cell-0-0.txt | grep -E "matches claimed raw|class  0 |classes dominating|VERDICT|EXIT"
  matches claimed raw  : False
class  0 size 5 undominated A/B/C = 12/12/12  redundant members 0  squares 2,4 4,10 6,6 8,2 10,8
classes dominating: 20 / 21
VERDICT: FAIL
EXIT: FAIL
exit=1
```

## Determinism

Three runs of each script, stdout hashed; identical each time.

```
98be4733aaaae0fb32c2372347d54cd60a09faba2d4a84471bf8b2d25ec3aa80 *-   (check_partition.py, run 1)
98be4733aaaae0fb32c2372347d54cd60a09faba2d4a84471bf8b2d25ec3aa80 *-   (run 2)
98be4733aaaae0fb32c2372347d54cd60a09faba2d4a84471bf8b2d25ec3aa80 *-   (run 3)
e8a893147a2286f3545e86099bf7e3e79f3e58a23d0b96f5e23727a02bbb996b *-   (controls.py, run 1)
e8a893147a2286f3545e86099bf7e3e79f3e58a23d0b96f5e23727a02bbb996b *-   (run 2)
e8a893147a2286f3545e86099bf7e3e79f3e58a23d0b96f5e23727a02bbb996b *-   (run 3)
```

The object is a fixed file; the check involves no search and no randomness (the K6 shuffles use a fixed seed).
Checker source hashes at the time of these runs:

```
e34297120fe44fc68f285dc258ce2a13ddfbcd36cf8f452a565d4411e6179eb5 *panel/reproduce-code/check_partition.py
d1a3bad2c98a6391e39bc6c71eb632c3a20498107ced2d3926484ea272d28588 *panel/reproduce-code/controls.py
3918534619edd850849b21860355b7efea861fbe251c94df6a71aa739716ef4e *panel/reproduce-code/control-corrupt-cell-0-0.txt
```

## Not checked by this skeptic

- The literature status (Table 1 of Lauri's Corrigendum listing dom(Q_12) as 20-21, OEIS A292192 stopping at n = 10,
  no later result). This review had no web access by design, so the novelty of the bound is not confirmed here.
  CLAIM.md also says no fresh literature search was made in this run (the last one is dated 2026-11-05), while the bank
  criterion asks for searches "re-fetched immediately before claiming". That is for the status skeptic to judge.
- The upper bound dom(Q_12) <= 21 (not claimed; attributed to Lauri). If it holds, this object would make
  dom(Q_12) = 21 exact, but the claim does not say so and I did not check it.

## Observations

- Classes 0, 1 and 2 (the size-6 classes) are each one regular step pattern ((+2,+4) mod 12 style), consistent with
  minimum dominating sets of Q_12. The other 18 classes have 7 squares.
- Some classes contain mutually attacking squares (e.g. class 3 has 5,3 and 5,4; class 20 has 7,0 and 7,10). This is
  allowed: the claim is about domination only, not independent domination.
- Every class is a minimal dominating set (0 redundant members in each), which is why the object is so fragile under
  single-cell changes.
- The file is plain ASCII, 377 bytes, CRLF line endings on all 12 lines, final newline present, no tabs, no BOM.

Verdict: the object exists, its raw hash matches, it parses as a 12 x 12 grid with labels exactly 0..20, it is a
partition of all 144 squares, and each of the 21 classes dominates Q_12 under the quoted definition (three methods
agree). This gives dom(Q_12) >= 21. Every sensitivity control behaved as expected and the outputs are deterministic.

pass: true
