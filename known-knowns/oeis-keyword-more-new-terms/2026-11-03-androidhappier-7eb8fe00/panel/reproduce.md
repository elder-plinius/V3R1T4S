# REPRODUCE skeptic — run 2026-11-03-2000-locdisj

context: subagent (reproduce)
date: 2026-11-03 (America/New_York, ~16:20 EST)
working copy: /workspace/panel-locdisj-repro/claim (copied from runs/2026-11-03-2000-locdisj/claim/)

## Claim under test
A316471(21) = 482706 (locally disjoint rooted identity trees, 21 nodes). object/VALUE.txt = 482706.
Pre-claim b-file / DATA ends at n = 20, a(20) = 214490.

## 1. Independent checker (written from the definition before opening claim/programs)
File: /workspace/panel-locdisj-repro/mine/check.py (copy at panel/reproduce_check.py).
Algorithm: explicit bottom-up enumeration with canonical tree ids. Each valid tree of size n gets an id;
a tree of size n is a set of child ids chosen strictly increasing (=> pairwise distinct branches, identity)
with sizes summing to n-1, and each new child's own child-set must be disjoint from the union of child-sets
of the already-chosen children (=> every two distinct branches share no branch: locally disjoint).
Only valid trees receive ids, so the condition holds recursively. Top level counted only.
Negative fixture (`nodisj` drops the disjointness test) gives A004111: 1,1,1,2,3,6,12,25,52,113,247,548,1226,2770,6299,14426 (correct).

Output n = 1..21:
1, 1, 1, 2, 3, 6, 11, 21, 43, 89, 185, 391, 840, 1822, 3975, 8727, 19280, 42841, 95661, 214490, 482706
Python 3, <1 s wall, peak RSS ~115 MB.

## 2. Claim programs per REPRODUCE.md (gcc 14.2.0, go1.27.3)
sha256: progA.c a8a00c57...9024b; main.go fa5811fa...19ca; go.mod 355f251f...3b00; progC.py 017357a0...f521
- Program A (C): `./pA 21` -> 1..20 identical to DATA, a(21) = 482706. ~0.02 s.
- Program B (Go): `./pB 21` -> 1..20 identical to DATA, a(21) = 482706. ~1.7 s, peak RSS ~227 MB (<300 MB).
- Program C (Python+sympy, Matula-Goebel oracle): needed `pip install sympy` (used a venv; sympy absent on box by default).
  `progC.py 11` -> A000081 column 1,1,2,4,9,20,48,115,286,719,1842 (correct); A316471 column 1,1,1,2,3,6,11,21,43,89,185 (matches DATA).
- Negative fixture: `./pA 16 nodisj` and `./pB 16 nodisj` both give A004111 through n = 16 (correct), not A316471.

## 3. Agreement
All three full-range computations (my checker, A, B) agree on a(1..20) = DATA and a(21) = 482706; C agrees for n <= 11.
Only friction: REPRODUCE.md assumes sympy installed (environment issue, not a correctness issue).
Not assessed here (out of scope): novelty, criterion, GATE, packaging.

pass: true
