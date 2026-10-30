context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# NOVELTY verdict: R(3,3,12) >= 203 (claimed) vs DS1 >= 194

## Primary table (one plain request each, User-Agent "V3R1T4S-novelty-skeptic/1.0", no retries)
- Status page https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 fetched 2026-10-25T08:54:40Z, HTTP 200, 17621 bytes; page text "DS1: Apr 24, 2026" (latest revision).
- PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf fetched 2026-10-25T08:53:21Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (equals table_record.md).
- Table XIb (pdftotext), row k=3, columns m=4..16: 30 45 61 85 103 129 150 174 194 217 242 269 291; the m=12 entry is 194, reference ExT. Item 6.1.2(h) also lists no better value; the text names 261 <= R(3,3,15) as implied, not R(3,3,12).

## Object re-check (own checker, work/chk.py, written from the definition)
sha256 of object/R_3_3_12.txt = eeb47c398be7c450cadf8d9b5939d4996761911a1ddba276e6d820b87fd0db1b (matches CLAIM.md). Distances 1..101 are each in exactly one colour. Output:
```
colour 1 has K3: False
colour 2 has K3: False
colour 3 has K12: False
```
So the colouring on 202 vertices is valid and R(3,3,12) >= 203 (correctness is the other skeptics' job; this only supports the novelty comparison).

## Implied-bound check (do published general results already give >= 203?)
- DS1 6.2.g: R(3,k,l) >= 4R(k,l-1)-3. With R(3,11) >= 47 (Table Ia row 3, l=11) gives 185 < 194.
- 6.2.h, 6.2.q/r (products), 6.2.j (Giraud/Rowley cyclic recurrences): by hand, about 95 to 155 for this cell, all below 194. No other 6.2 item applies to (3,3,12).
- ExT (arXiv:1504.02403) Table 2 states R(3,3,12) 185 -> 194 "splitting"; it split its own (5,12) colouring, which was R(5,12) >= 194 (same paper, "R(5,12) 191 194 circulant"). Kuznetsov (arXiv:1505.07186v5, posted after ExT) prints a (5,12) circulant on Z_202 (DS1 Table Ia R(5,12) >= 203); neither Kuznetsov's text (no "split" or three-colour mention, grep) nor DS1 splits it. This is the origin of the claim, and the step is not in print.
- Monotonicity or neighbour cells (R(3,3,11) >= 174, R(3,3,13) >= 217) give nothing for m=12 at 203.

## Literature, last 24 months (fresh searches by this session)
- arXiv API all:"R(3,3,12)" returned 0 entries (HTTP 200). Query on abs:Ramsey with three colors/multicolor, newest first: latest entries 2026-07 .. 2026-10-12, all asymptotic or other graphs (ordered matchings, odd cycles, Erdos-Sos, upper bounds).
- arXiv:2609.28455 (R(3,3,k) = Theta(...), asymptotic) and arXiv:2509.03784 (small multicolour numbers, Wesley, SAT; other cells), arXiv:2601.05221 (survey): text searched for "3,3,12" and "R(3,3,1x)": no hit giving a number for R(3,3,12).
- Two WebSearch queries (R(3,3,12) lower bound; R(3,3,k) circulant splitting): nothing newer than ExT 194.
- Exoo's page http://cs.indstate.edu/ge/RAMSEY/ (HTTP 200, 5609 bytes, 2026-10-25T08:55:41Z): multicolour section lists R(4,4,4,4) only, no R(3,3,12). The ExTa/ subfolder was not fetched (403 in the author's record; not retried).

## This repo (github.com/elder-plinius/V3R1T4S, read-only, one plain request per page)
- TROPHY_CASE.md (raw, HTTP 200, 31235 bytes, 2026-10-25T08:54:26Z): 0 occurrences of "ramsey"; its families are degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, ciphers.
- Open pull requests via API pages 1-4 (HTTP 200; pages 5, 6 empty, 2-byte): 357 open PRs scanned for ramsey/circulant/"r(3,3" in title and body: no match (the two matches, #614 and #509, only contain the word "circulant" in quantum-code / graph-state text, checked: Z_19-circulant graph state; double-circulant seeds; neither concerns Ramsey numbers). Issue search repo:elder-plinius/V3R1T4S ramsey: total_count 0.

## Verdict
Nothing found in DS1 (Apr 24, 2026), the last 24 months of arXiv, Exoo's page, TROPHY_CASE.md or open PRs reaches 203 for R(3,3,12); the best known value is 194 and no general construction implies more than 194. The claim is strictly above the status table by 9 (203 vs 194).
Residual risk, honestly stated: Exoo's ExTa/ folder was not readable (403 in the author's record), and the arXiv/web search is keyword-based, so an unpublished or unindexed value cannot be excluded. A caveat on the cell's nature: the object is a direct split of a published 2015 circulant, so it is novel as a number but not as a method; the criterion asks only for the number.

pass: true
