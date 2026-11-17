# Panel: reproduce — run 2026-11-03-1625-nestconn
context: subagent (reproduce)

Claim under test: A326335(11) = 61987 (object/VALUE.txt: "A326335(11) = 61987").
Fresh context: I did not read any other panel/*.md or GATE.md. Work copy: /workspace/panel-nestconn-repro/claim (copied from run claim/; diff -rq vs original shows only my build artifacts pA, pB, pC.out added).

## 1. Independent checker (written BEFORE reading claim/programs)
File: /workspace/panel-nestconn-repro/mine/check.py (sha256 d8362b02a7056502f219fe173637cb94c80228f242d359afa5bac8de1a7d17fb).
Source of definition: table/A326335_internal.txt (%C and %t lines): blocks sorted ascending; two blocks nest if some consecutive pair (x,y) of one and consecutive pair (z,t) of the other satisfy x<z<t<y or z<x<y<t; count set partitions whose block graph under nesting edges has <=1 component (n=0 empty partition and one-block partitions count).
Method: enumerate all set partitions via restricted-growth strings (Bell(11)=678570 at n=11), test each block pair by brute force over consecutive pairs, union-find for connectivity.
Output (python3 check.py 11, 7.0 s):
n: 0..11 -> 1,1,1,1,2,6,21,86,394,1974,10696,61987
n=0..10 matches %S DATA 1,1,1,1,2,6,21,86,394,1974,10696 and b326335.txt exactly; n=11 = 61987.

## 2. Claim programs (per claim/REPRODUCE.md, run from the copy)
- pA (C, gcc -O2): A326335 column n=0..11 = 1,1,1,1,2,6,21,86,394,1974,10696,61987 (0.44 s)
- pB (Go): identical full table, A326335(11)=61987 (1.0 s)
- pC (Python literal transcription): identical full table, A326335(11)=61987 (49.8 s)
All three print identical full tables (also the cross-check columns: n=11 -> A326245 23096, A326246 596688, A326249 24744, A326336 70472; not assessed).

## 3. Table files integrity
sha256 of copied table files equal TABLE_RECORD.md entries: A326335.html 66a171d6..., b326335.txt 22e6ca0a..., A326335_internal.txt 38087a77..., A326335_history.html 7d22a1d7..., search_61987.txt 2062eba1..., search_10696_61987.txt 2e27052c... (all match).
internal.txt shows %K nonn,more, %O 0,5, %S ending at a(10)=10696, so n=11 is the first missing index.

## Verdict
My independent checker and all three claim programs agree: A326335(11) = 61987, and all reproduce the existing terms n=0..10.
(Scope: reproduction only; novelty/criterion not assessed.)
pass: true
