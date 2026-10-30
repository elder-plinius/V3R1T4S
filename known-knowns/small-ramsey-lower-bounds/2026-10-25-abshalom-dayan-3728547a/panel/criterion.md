context: headless claude -p session (claude-opus-5-5, effort high), fresh, started inside a copy of claim/ .

# CRITERION skeptic verdict: partial win p1, R(3,5,7) >= 252

Verdict: the object meets partial win p1, read clause by clause. The main (two-colour) success criterion is not claimed and is not met; this is a multicolour cell.

## Clause-by-clause check of p1

| p1 clause | Evidence | Met? |
|---|---|---|
| "an explicit edge colouring of K_N" | object/R_3_5_7.txt: "circulant 251 3", colour lists of sizes 26 + 42 + 57 = 125 = (251-1)/2 distances; my loader asserts every distance 1..250 gets exactly one colour (no conflict, no gap) | yes, N = 251 |
| "no monochromatic forbidden clique in each colour" (K3 / K5 / K7) | two independent exact methods of my own, below | yes |
| "verified exhaustively" | Bron-Kerbosch max-clique with pivoting (work/mycheck.py) and CaDiCaL SAT with a cardinality constraint (work/satcheck.py), both on the neighbourhood of vertex 0 (valid by the circulant's vertex transitivity) | yes |
| "N+1 strictly above the best lower bound in DS1" | DS1 revision #18 (April 24, 2026), Table XIb: R(3,5,7) >= 241 (ref 6.2.g). 252 > 241 | yes |
| "and any newer arXiv paper for that multicolour cell" | my own arXiv API searches (below): no paper gives a lower bound for R(3,5,7) | yes, as far as these searches reach |

## Object checks (real output)

```
$ shasum -a 256 object/R_3_5_7.txt
3728547aec5e9b0b5779c21b5bf06cee6dfb90a01230c42389b821fcfa351976  object/R_3_5_7.txt
$ python3 work/mycheck.py object/R_3_5_7.txt        # own Bron-Kerbosch, max clique through vertex 0
colour 1 degree 52 clique number 2
colour 2 degree 84 clique number 4
colour 3 degree 114 clique number 6
$ venv python work/satcheck.py object/R_3_5_7.txt   # own SAT (CaDiCaL 1.5.3), "clique of size k through 0"
colour 1 K3-clique through 0 SAT? False
colour 2 K5-clique through 0 SAT? False
colour 3 K7-clique through 0 SAT? False
$ python3 verify_circ.py object/R_3_5_7.txt 3 5 7   # author's checker, agrees
proves R(3,5,7) >= 252
PASS
```
The clique numbers are 2, 4 and 6, each one below the forbidden size 3, 5 and 7. So K_251 has a (3,5,7)-colouring and R(3,5,7) >= 252 (off by one handled correctly).

## DS1 (fetched by me)

- https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1: HTTP 200, 17621 bytes, fetched Sun Oct 25 09:11:44 UTC 2026, page text "Apr 24, 2026".
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf: HTTP 200, 585821 bytes, fetched Sun Oct 25 09:11:57 UTC 2026, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (same as table_record.md). Header: "version #0: August 1, 1994; revision #18: April 24, 2026".
- Table XIb, row k = 5: "89 139 181 241" with references "Ex17 Ex17 Ex17 6.2.g". So R(3,5,7) >= 241. Notes 6.1.2(c)-(h) give no other R(3,5,7) value.

Hidden-quantifier check ("best lower bound in DS1" could include bounds that DS1's general results imply but do not print). I applied DS1 section 6.2 to the current Table Ia/XIb values (R(4,7) >= 49, R(5,6) >= 59, R(5,7) >= 80, R(3,4,4) >= 55, R(3,3,6) >= 61, R(3,7) = 23, R(3,5) = 14):
- 6.2.g: 4R(5,6)-3 = 233; 4R(4,7)-3 = 193; R(5,7,3) >= 4R(4,4,3)-3 = 217; R(7,5,3) >= 4R(6,3,3)-3 = 241 (this is the table's 241).
- 6.2.q: 2(R(5,7)-1)+1 = 159; 6.2.r: 4(R(3,7)-1) = 88; 6.2.o: best split I found gives 2(R(3,4,5)-1) = 176.
- 6.2.j (Rowley): ((2L(5,7)-1)(2L(3)-1)+1)/2 <= ((2*79-1)*3+1)/2 = 236.
None reaches 252. A bound of 252 or more through 6.2.g would need R(5,6) >= 64 or R(3,3,6) >= 64. No source I read gives either.

Null-model check: no trivial or product construction (above) reaches 252. The source circulant gives R(7,9) >= 252 (DS1 Table Ia lists 252, ref "Kuz"), but no DS1 inequality turns R(7,9) into a bound for R(3,5,7). The win needs the actual split of the K9-free colour into a triangle-free and a K5-free colour, and I checked that split directly above.

## arXiv (my own searches, export.arxiv.org API, one request each, User-Agent naming V3R1T4S)

| query | HTTP | entries | published range | sha256 |
|---|---|---|---|---|
| abs:Ramsey AND (abs:"lower bound" OR abs:"lower bounds"), 300, newest first | 200 | 300 | 2010-04-25 .. 2026-10-20 | f7087a364a701b4e... |
| ti:Ramsey, 300, newest first | 200 | 300 | 2025-05-07 .. 2026-10-21 | 4d684353cc86e454... |
| au:Rowley OR au:Exoo OR au:Kuznetsov_E OR au:Radziszowski OR au:Tatarevic OR au:Boza, 100 | 200 | 100 | 2021-02-18 .. 2026-08-24 | (q3) |
| abs:Ramsey AND (multicolor OR multicolour OR "three-color" OR "3-color" OR "three colors" OR "edge colorings"), 200 | 200 | 200 | 2020-06-08 .. 2026-10-17 | (q4) |
| id_list = 2603.09172, 2608.18169, 2608.18769, 2610.12122, 2609.28455, 2607.06817 | 200 | 6 | | |

(The search queries ran 09:13:15 to 09:14:13 UTC on 2026-10-25.) "R(3,5,7)" occurs 0 times in all five result files (grep -c). The 2026 multicolour items are asymptotic or about other graphs (2609.28455: R(3,3,k) = Theta(k^3/log^2 k); 2608.01962 and 2609.04596: upper bounds; 2608.02537: odd cycles; plus ordered, bipartite and star cases). The named 2026 two-colour papers improve only R(3,13), R(3,18), R(4,13..20) (2603.09172v5), R(4,20) (2608.18169v2), R(3,n) for 24 <= n <= 49 (2608.18769), R(6,8) and R(8,10) (2610.12122), and R(k+1,s+1) for k >= 5 (2608.06531, Tatarevic). None of these changes R(5,6), R(3,3,6), R(3,4,4) or R(4,7), so the 6.2-implied bounds above stay below 252.

## Limits of this check

My search covered arXiv titles and abstracts only, not full texts, and no non-arXiv repositories. p1 asks only for DS1 and newer arXiv papers. A bound for R(3,5,7) that sits only in a paper's body, with no mention in its abstract, would not have shown up.

confirmed_scope: The circulant 3-colouring of K_251 in object/R_3_5_7.txt (sha256 3728547a...351976) has, by two independent exact checks, no monochromatic K3 in colour 1, K5 in colour 2 or K7 in colour 3, so R(3,5,7) >= 252, strictly above the bound 241 in DS1 revision #18 (April 24, 2026, Table XIb) and above every lower bound for R(3,5,7) found in arXiv titles and abstracts up to 2026-10-21.

pass: true
