# Reproduce report: cover-57-14-3-b108

context: Claude Code subagent, fresh context
role: reproduce

Step 1: shasum -a 256 -c on the contributor's hash list run inside the package folder: every listed file reported OK (0 failures). All work was then done on a private copy of the package folder; no network was used.

## Definition (quoted from the claim record, not shipped)
"A (v,k,t) covering design is a collection of k-subsets (blocks) of a v-set such that every t-subset lies in at least one block." Criterion: "b blocks, each a k-subset of a v-set (no repeated points), covering every t-subset (checked exhaustively) ... Parameters must be within v <= 99, k <= 25, t <= 8, and b must be at least the Schonheim bound L(v,k,t); going below it means a bug. Same-day claim only if C(v,t) <= 5e9." Here v=57, k=14, t=3, b=108, C(57,3) = 29260 <= 5e9.

## My checker (written before reading verify-it-yourself/)
My own checker (written from scratch, not shipped in this package): parses the JSON, asserts each block has exactly 14 distinct integers in 1..57, checks that the blocks are pairwise distinct, then checks coverage of all 29260 3-subsets by two methods (a Python set of all triples of all blocks compared with every triple of {1..57}; and a combinadic-rank count array of size C(57,3) giving the multiplicity of every triple), computes the Schonheim bound recursively L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)), L(.,.,0) = 1, and runs a negative control (drop one block).

## Command and real output
Own checker, run on object/C_57_14_3_b108.json; its output is shown below:

```
sha256 f133e94dd68370e1e8001f34d0f021032948f2380962a71e8a4d80b15bee0803
keys ['v', 'k', 't', 'm', 'b', 'method', 'blocks'] v,k,t,m,b 57 14 3 3 108
number of blocks 108
all blocks length 14: True | all distinct points: True | all in 1..57: True | distinct blocks: 108
declared b equals len: True
C(57,3) = 29260 covered distinct triples 29260
method1 uncovered: 0
method2 (combinadic) uncovered: 0 min mult 1 max mult 11 rank space size 29260
Schonheim L(57,14,3) = 90 ; chain: 1 5 22
parameter ranges v<=99,k<=25,t<=8: True True True ; b>=L: True ; b<109: True
negative control (drop block 1) uncovered triples: 68
```

The "chain:" line in that output is a leftover debug print of unrelated small values and is not the bound. The bound is the single value L(57,14,3) = 90, confirmed by hand: L(55,12,1) = ceil(55/12) = 5, L(56,13,2) = ceil(56*5/13) = 22, L(57,14,3) = ceil(57*22/14) = ceil(89.57) = 90.

## Clause-by-clause
- 108 blocks, each 14 distinct points in 1..57, format as claimed (keys v,k,t,m,b,method,blocks; b equals the list length): yes.
- Every one of the 29260 3-subsets is covered, exhaustively, by two methods: yes (0 uncovered; each triple covered 1 to 11 times). Dropping one block leaves 68 triples uncovered, so the check can fail.
- b = 108 >= Schonheim 90: yes. Parameters within the allowed ranges: yes. 108 < 109 and 108 < 110 as stated: arithmetic yes (the table values themselves were not fetched in this role).
- File sha256 equals the INDEX.csv value: yes (first output line).

## Author's own run (after my checker)
```
sha256 matches INDEX.csv (f133e94dd68370e1e8001f34d0f021032948f2380962a71e8a4d80b15bee0803)
== check_covering.py: every 3-subset of the 57-set lies in some block
C(57,14,3) b=108 blocks_ok=True covered=29260/29260 PASS sha=f133e94dd68370e1
== schonheim.py
Schonheim L(57,14,3) = 90; blocks b = 108; b >= L: True; parameters within v<=99,k<=25,t<=8: True
SCHONHEIM PASS
== negative control: a copy with one block removed (and b adjusted) must FAIL the coverage check
negative control rejected as expected: C(57,14,3) b=107 blocks_ok=True covered=29192/29260 FAIL sha=515a97be11f66b5a
ALL CHECKS PASS
```

## Result
No mismatch with the author's checker; no missing object; the check is a pure exhaustive computation and is deterministic.

pass: true
