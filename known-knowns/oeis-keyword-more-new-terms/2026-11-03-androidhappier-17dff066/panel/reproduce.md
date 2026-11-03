# Panel: REPRODUCE skeptic, run 2026-11-03-2004-ldsemi
context: subagent (reproduce)
date: 2026-11-03 ~16:25 EST (UTC-5)
claim under test: A331783(21) = 10950456 (locally disjoint rooted semi-identity trees, n unlabeled vertices). DATA/b-file end a(20) = 4242226.
scratch: /workspace/panel-ldsemi-repro/ (claim copy in claim/, own checker in own/ld.c, output own/own_out.txt)

## 1. Own checker (written from the OEIS definition only, before opening CLAIM.md/programs)
Definition read from data/A331783_text.txt (%N, %C, %e). Model: a tree = k leaf children + a SET of
distinct non-leaf children; non-leaf children must pairwise have disjoint child-type sets (leaf type
counts as an element, so two non-leaf branches that both contain a leaf overlap; e.g. ((o)(oo)) is
excluded, matching the a(6)=17 example list). Recursion applies at every vertex because only stored
valid trees are used as children. C (gcc -O2), trees stored up to size N-1, size N counted only;
DFS over increasing tree ids with a mark array for disjointness.
Output n=1..21: 1,1,2,4,8,17,37,83,191,450,1076,2610,6404,15875,39676,99880,253016,644524,1649918,4242226,10950456
All 20 DATA terms reproduced; a(21) = 10950456. Runtime 0.3 s.
Caveat: after opening the claim, my checker's algorithm turns out to be the same family as Program A
(id-set backtracking with mark array). Independent code, not an independent algorithm; Program B
(Go, partition x tuple transcription of Mathematica disjunsQ) is the algorithmically different confirmation.

## 2. Claim programs per claim/REPRODUCE.md (fresh build in copy)
- object/VALUE.txt = 10950456
- Program A (C): gcc -O2; ./pA 21 -> n=1..20 = DATA exactly, a(21) = 10950456 (0.25 s)
- Program B (Go 1.27.3): go build; ./pB 21 -> n=1..20 = DATA exactly, a(21) = 10950456 (2.3 s)
- Program C (Python, n<=11): A000081 column 1,1,2,4,9,20,48,115,286,719,1842 (correct); A331783 column 1,1,2,4,8,17,37,83,191,450,1076 (= DATA)
- Negative fixture: ./pA 16 nodisj and ./pB 16 nodisj both give 1,1,2,4,8,18,41,98,237,591,1488,3805,9820,25593,67184,177604 (semi-identity counts, A306200-type), differing from A331783 from n=6 on, as REPRODUCE.md states. Disjointness test is live in both.

## 3. Verdict
Three codes (own C checker, claim pA C, claim pB Go) agree on a(1..21); all reproduce a(1..20) = DATA; a(21) = 10950456.
Did not assess novelty/criterion/packaging (out of scope).
pass: true
