# Panel: REPRODUCE — run 2026-11-03-1625-capconn
context: subagent (reproduce)

## Claim
A326336(11) = 70472 (set partitions of {1..11} whose capturing-block graph is connected).

## Method
- I copied claim/ to /workspace/panel-capconn-repro/claim and worked only from that copy and a fresh OEIS fetch (https://oeis.org/A326336/internal, fetched 2026-11-03).
  The fresh fetch shows %S 1,1,1,1,2,7,24,100,458,2279,12270, %O 0,5, %K nonn,more.
- I wrote my own checker BEFORE opening claim/programs: /workspace/panel-capconn-repro/mine/checker.py. A copy is at panel/reproduce_checker.py.
  - It enumerates set partitions as restricted growth strings.
  - Its graph has the blocks as vertices, with an edge where two blocks capture. It counts partitions whose graph is connected, and treats 0 or 1 blocks as connected.
  - Mode `literal` uses the definition word for word: some pair x<y in one block and z<t in the other with x<z<t<y or z<x<y<t.
  - Mode `fast` uses an equivalent test: A captures B iff |B ∩ (min A, max A)| >= 2, or the same with A and B swapped.
  - Both modes ran for n = 0..11 and agree.
- I then ran the claim programs as REPRODUCE.md says: A (C, gcc -O2), B (Go build) and C (Python literal, 47 s).
- I grepped the programs for 12270 and 70472. Neither value is hard-coded.

## Results, a(0..11)
| n | mine literal | mine fast | pA C | pB Go | pC Py | OEIS DATA |
|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 | 1 |
| 3 | 1 | 1 | 1 | 1 | 1 | 1 |
| 4 | 2 | 2 | 2 | 2 | 2 | 2 |
| 5 | 7 | 7 | 7 | 7 | 7 | 7 |
| 6 | 24 | 24 | 24 | 24 | 24 | 24 |
| 7 | 100 | 100 | 100 | 100 | 100 | 100 |
| 8 | 458 | 458 | 458 | 458 | 458 | 458 |
| 9 | 2279 | 2279 | 2279 | 2279 | 2279 | 2279 |
| 10 | 12270 | 12270 | 12270 | 12270 | 12270 | 12270 |
| 11 | 70472 | 70472 | 70472 | 70472 | 70472 | (not in DATA) |

The three claim programs also print the side columns A326245, A326246, A326249 and A326335, and those columns are identical across the programs. I did not check them against OEIS, because they are outside my role.

## Verdict
My independent checker (both modes) and all three claim programs reproduce the OEIS DATA for n = 0..10 and give a(11) = 70472.
I did not look at novelty or the criterion.

pass: true
