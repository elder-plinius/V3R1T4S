context: headless claude -p session (claude-opus-5-5, effort high), fresh, started inside a copy of claim/

# CRITERION verdict: claim R(3,3,12) >= 203, partial win p1

Verdict: the object meets partial win p1 read literally. It is an explicit 3-colouring of K_202 with no monochromatic K_3/K_3/K_12, checked exhaustively by two independent methods. N+1 = 203 is strictly above the DS1 Table XIb entry of 194, and I found no newer arXiv paper giving a better bound for this cell. It is not subsumed by the main criterion, which is about two-colour R(s,t).

## Clause by clause (p1)

1. "explicit edge colouring of K_N": object/R_3_3_12.txt is a circulant on Z_202 (sha256 checked: `eeb47c398be7c450cadf8d9b5939d4996761911a1ddba276e6d820b87fd0db1b  object/R_3_3_12.txt`, which matches CLAIM.md). My parser asserts that each distance 1..201 gets exactly one colour, with d and 202-d treated as the same distance. Colour degrees: `colour 1 degree 35`, `colour 2 degree 40`, `colour 3 degree 126` (sum 201).
2. "no monochromatic forbidden clique in each colour ... verified exhaustively":
   - I wrote my own checker (work/check.py) from the definition before reading verify_circ.py. Colours 1 and 2: brute force over every triple of the 202 vertices, without relying on symmetry: `all-triples mono triangles colours 1,2: {1: 0, 2: 0}`.
   - Colour 3: a SAT encoding (CaDiCaL 1.5.3, sequential-counter cardinality). Vertex 0 is in the clique, which is fine because translations are automorphisms. Pairwise non-adjacent neighbours give exclusion clauses, plus "at least 11 of the 126 neighbours": `colour 3: 11-clique in N(0) SAT? False` (UNSAT, so no K_12).
   - Non-vacuity control: the same encoding with bound 10 is SAT and finds a K_11, `[0, 3, 6, 11, 14, 17, 43, 61, 64, 67, 75]`. So colour 3's clique number is exactly 11.
   - Second, independent method (the author's B&B, verify_circ.py, stdlib): `colour 3: degree 126, no K_12 (no K_11 among the neighbours of 0, exhaustive)` / `proves R(3,3,12) >= 203` / `PASS`.
3. "N+1 strictly above the best lower bound in DS1": I re-fetched the DS1 status page (HTTP 200, 17621 bytes, 2026-10-25 08:57:57 UTC; it shows "DS1: Apr 24, 2026"). I also re-fetched the PDF (HTTP 200, 585821 bytes, 08:58:08 UTC, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc, identical to table_record.md). The Table XIb row k=3 reads `30 45 61 85 103 129 150 174 194 217 242 269 291` for m=4..16, so R(3,3,12) >= 194 [ExT].
   - Hidden-quantifier check: DS1 says "Lower bounds for higher numbers can be obtained by using general constructive results from Section 6.2". I applied every 6.2 lower-bound item that fits (3,3,12), using DS1 Table Ia values (R(3,11) >= 47, R(3,12) >= 53, R(3,10) >= 40, row k=3 of Table Ia reads `40 47 53 61 67 74` for l=10..15):
     - 6.2.g: 4R(3,11)-3 = 185.
     - 6.2.q: 5*11 = 55 or 2*(53-1) = 104.
     - 6.2.r: at most 4*(R(3,10)-1) = 156.
     - 6.2.j (Rowley): ((2*5-1)(2*11-1)+1)/2 = 95.
     - 6.2.o: at most (53-1)*2 = 104.
     None reaches 194, so 194 is DS1's best for the cell. 203 > 194.
4. "and any newer arXiv paper for that multicolour cell": my own arXiv API searches, sorted newest first:
   - `all:Ramsey AND (multicolor OR multicolour OR three-color OR 3-color OR multi-color)`: HTTP 200, 150 entries, 2012-09-10..2026-10-19.
   - `all:Ramsey AND ("lower bounds" OR circulant OR cyclic)`: HTTP 200, 200 entries, 2021-06-01..2026-10-21.
   - A regex over titles and abstracts found only one post-DS1 paper on this family, arXiv:2609.28455 "On the multicolour Ramsey numbers R(3,3,k)". It is asymptotic (Theta(k^3/log^2 k)). Its full PDF (HTTP 200, 389231 bytes) contains no "194", "203" or "R(3,3,12)".
   - The other newer papers are two-colour (2610.12122, 2608.18169, 2608.18769) or asymptotic or about other graphs.
   - Two web searches for "R(3,3,12)" surfaced only Exoo-Tatarevic 2015 (185 -> 194 by splitting).
   - I found no source with R(3,3,12) >= 195 or more.

## Null model / stretched definitions

- The construction is the published Exoo-Tatarevic splitting method applied to Kuznetsov's published (5,12) circulant. DS1 Table Ia lists R(5,12) >= 203 [Kuz]. So 203 is exactly the ceiling of that null pipeline (split a K5-free colour into two K3-free colours): the method is not new, only its application to this colouring. p1 requires an explicit colouring that beats the DS1 cell, not a new method, so this does not fail the criterion. It does mean the win is modest and mechanical.
- Nothing is stretched: there is no "up to isomorphism" or restricted class, and the "verified exhaustively" clause is met by full SAT UNSAT and B&B over all cliques through vertex 0, plus all-triples brute force for colours 1 and 2.
- The claim is not the main success criterion, which is two-colour R(s,t), and is not claimed as such.
- Limits: my searches cover arXiv and open web results only. Exoo's ExTa/ folder (403 per the author's record) was not re-requested.

confirmed_scope: The circulant 3-colouring of K_202 in object/R_3_3_12.txt has no monochromatic K_3 in colours 1 and 2 and no K_12 in colour 3 (checked by all-triples brute force, a CaDiCaL UNSAT proof and the author's exhaustive B&B), so R(3,3,12) >= 203, strictly above DS1 (April 24, 2026) Table XIb's 194 and above every bound for this cell I found in arXiv papers newer than that revision.

pass: true
