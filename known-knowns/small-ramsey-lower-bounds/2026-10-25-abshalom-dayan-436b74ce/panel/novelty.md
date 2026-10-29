context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# NOVELTY verdict: R(3,5,6) >= 183 (claim: object/R_3_5_6.txt, 3-colouring of K_182)

novelty: CONFIRMED (strictly above every source I could read)

## 1. Primary table (one plain request each, User-Agent "V3R1T4S-novelty-skeptic (read-only research)", no retries, no cookies)
- Status page https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : fetched 2026-10-25T11:17:24Z, HTTP 200, 17621 bytes, page text "This Version ... DS1: Apr 24, 2026". (sha256 4f8d21a4..., differs from the author's recorded 9095c60e...; same size and same version text, so a dynamic page fragment, not a new revision.)
- Full text https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf : fetched 2026-10-25T11:17:29Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (identical to the author's record), 149 pages.
- Table XIb (section 6.1.2), pdftotext of my own copy, row k=5: "89 139 181 241" for m=4..7 with references "Ex17 Ex17 Ex17 6.2.g". So the DS1 value for R(3,5,6) is 181 (Ex17 = Exoo, personal communication 2010-2011). The claim needs 183 > 181: strictly above.
- DS1 two-colour table: R(6,9) >= 183 is listed (row 6, column 9), consistent with the Kuznetsov circulant used as the starting point.

## 2. The object (own checker work/mine.py, written from the definition)
- shasum -a 256 object/R_3_5_6.txt -> 436b74cecb10c8263ed5c3413d66993ce1f9d34993718f7b5bb4b31890896826 (matches CLAIM.md).
- Output: "N 182 partition ok; sizes {1: 39, 2: 68, 3: 74}" / "colour 1 has K3: False | has K2: True" / "colour 2 has K5: False | has K4: True" / "colour 3 has K6: False | has K5: True".
  So the three distance sets partition 1..181 and the colourings avoid K3, K5, K6, so R(3,5,6) >= 183 holds. (Correctness is the other skeptics' job; this check was only to be sure the claimed value is real.)

## 3. Literature, last 24 months (2024-10-25 .. 2026-10-25)
- arXiv API, one request (all:Ramsey AND multicolor/multicolour/three colors/3-colour...), fetched 2026-10-25T11:18:53Z, HTTP 200, 174 entries, sha256 prefix 0ad40ee4fcd683a0. Listed every 2024-10..2026-10 entry that mentions lower bounds or Ramsey numbers; none concerns R(3,5,6). Closest: 2509.03784 (SAT, R(K4,K4-e,K4-e) >= 35, 4-colour R(K3,K4,C4,C4) >= 49), 2601.15183 and 2602.02155 (asymptotic multicolour lower bounds), 2603.10851 (upper bounds R(3,4,5), R(3,3,6)), 2609.28455 (R(3,3,k) asymptotics). I downloaded the full text of 2601.15183 and 2509.03784 (HTTP 200 each) and grepped for "3,5,6" / "(3,5,": no match.
- The author's own search record (literature_record.md) covers four more arXiv queries with the same outcome. I did not repeat them.
- Two WebSearch queries ("R(3,5,6)" lower bound; R(3,k,m) circulant 2025-2026 Exoo Tatarevic Rowley): no source giving any bound for R(3,5,6) other than DS1 table; no 2025-2026 R(3,k,m) lower-bound paper surfaced.
- Exoo's page http://cs.indstate.edu/ge/RAMSEY/ : fetched 2026-10-25T11:19:31Z, HTTP 200, 5609 bytes; text only says "Multicolor Ramsey Numbers ... colorings obtained using the growth method"; no table of values. The author recorded the ExTa/ subfolder as HTTP 403; I did not request it (no retry after a block).
- Limit: Ex17 is a personal communication, so an unpublished Exoo colouring above 181 cannot be excluded by anything I can read. No evidence of one.

## 4. TROPHY_CASE.md and open pull requests (GitHub raw/API, read-only, UA as above, fetched ~11:18Z)
- TROPHY_CASE.md (raw main): HTTP 200, 31235 bytes, sha256 b946f68eb0a6473d...; grep for "ramsey", "R(3", "183", "181": the only hit is an unrelated constant-weight-code row (A(29,6,10)). No Ramsey entry.
- Open PRs: pulls?state=open, pages 1-4 returned 100+100+100+78 = 378 PRs (pages 5 and 6 returned empty "[]"). Searched titles and bodies for "3,5,6", "3, 5, 6", "R_3_5_6", "R(3,5,". Only hit: #734 "R(3,5,7) >= 252 (3-colouring of K_251)", a different cell. Other small-ramsey claims: #731 R(3,3,11), #732 R(3,3,12), #733 R(3,3,14), #735 R(3,3,9). No PR claims R(3,5,6). #734 does not imply the claim: R(3,5,6) <= R(3,5,7) goes the wrong way.

## 5. Do published general constructions or neighbouring-cell bounds already imply >= 183?
DS1 section 6.2 constructions, evaluated at (3,5,6) with DS1's own two-colour values (R(5,5) >= 43, R(4,6) >= 36, R(3,5) = 14, R(3,6) = 18, R(5,6) >= 58):
- 6.2.g R(3,k,l) >= 4R(k,l-1)-3: 4*43-3 = 169 (k=5,l=6); 4*36-3 = 141 (k=6,l=5). Both < 183 (169 is the best, and DS1 itself lists the 181 as Ex17, not 6.2.g, at this cell).
- 6.2.q/o product bounds: (R(3,5)-1)(R(6)-1) = 65; (R(3)-1)(R(5,6)-1) = 2*57 = 114. 6.2.r (k1+1)(R(k2-k1+1,..)-1): 4*17 = 68. All far below 183.
- 6.2.j cyclic/Giraud/Rowley recurrences: no numeric (3,5,6) value stated in DS1; Rowley's items (6.1.f) concern (3,6,6), (3,7,7) etc., and R(3,5,6) <= R(3,6,6) gives nothing from below.
- Monotone neighbours: R(3,5,6) >= R(3,5,5) >= 139, R(3,4,6) >= 117, both < 183. Larger neighbours give only upper bounds on R(3,5,6).
- The claimed construction (split the K9-free colour of the Kuznetsov (6,9) circulant on Z_182) is the Exoo-Tatarevic splitting idea; the Kuznetsov two-colour bound R(6,9) >= 183 alone does not imply a 3-colouring, since a K9-free graph need not split into K3-free + K5-free parts. No published statement gives 183 here.
- Strict-beat check: 183 > 181 (DS1) > 169 (best implied). No tie.

## Verdict
The DS1 value (181, table fetched live, HTTP 200) is strictly below the claimed 183; no 2024-2026 paper, no trophy-case row, no open PR and no general construction I evaluated reaches 183 for the cell (3,5,6). Residual risk: unpublished Exoo data behind the personal-communication entry.

pass: true
