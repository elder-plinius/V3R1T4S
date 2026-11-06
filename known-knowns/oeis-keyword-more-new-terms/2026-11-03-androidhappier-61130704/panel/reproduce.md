# REPRODUCE skeptic — run 2026-11-03-1617-medmed

context: subagent (reproduce)

Claim under test: A361864(12) = 2092816 (claim/object/VALUE.txt).
Definition used (from claim/table/A361864.html / claim/table/A361864_internal.txt %N):
"Number of set partitions of {1..n} whose block-medians have integer median."

## Independent checker (written before reading claim/programs)
- Scratch copy of claim/ made under the skeptic's own scratch area; checker source `mine/chk.c` (scratch, not packaged).
- Method: enumerate all set partitions via restricted-growth strings (Bell(12)=4,213,597 for n=12).
  Each block median stored doubled (odd size k: 2*x[k/2]; even size: x[k/2-1]+x[k/2]).
  Sort the doubled medians; with b blocks: b odd -> integer iff middle value is even;
  b even -> median = (m[b/2-1]+m[b/2])/4, integer iff that sum is divisible by 4.
- Output (gcc -O2, 0.39 s):
  1 1 / 2 0 / 3 3 / 4 6 / 5 30 / 6 96 / 7 461 / 8 2000 / 9 10727 / 10 57092 / 11 342348 / **12 2092816**
- n=1..11 match OEIS %S exactly: 1,0,3,6,30,96,461,2000,10727,57092,342348 (claim/table/A361864_internal.txt, %O 1,3, %K nonn,more).

## Rerun of claim programs (from the scratch copy of claim/, per claim/REPRODUCE.md)
- programs/pA_c/medmed.c (`./pA 1 12`): 12 lines identical to above, a(12)=2092816.
- programs/pB_go/main.go (`./pB 1 12`, 3.4 s): 12 lines identical, a(12)=2092816.
- programs/pC_py/brute.py 10 (Fraction brute force): a(1..10) identical to OEIS.

## Table context (as recorded in claim/, not re-fetched)
- claim/table/search_2092816.txt and claim/table/search_342348_2092816.txt: "No results."
- Data ends at a(11)=342348; claimed value is the next term.

## Verdict
Independent checker and all three claim programs agree: A361864(12) = 2092816. Reproduced.

pass: true
