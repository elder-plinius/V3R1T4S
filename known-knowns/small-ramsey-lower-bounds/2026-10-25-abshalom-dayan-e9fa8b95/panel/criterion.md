context: headless claude -p session (claude-opus-5-5, effort high), fresh, started inside a copy of claim/ .

# CRITERION skeptic verdict: claim R(3,4,7) >= 154, partial win p1

Verdict: PASS. The object meets every literal clause of p1. It is a genuine improvement by 2 over the DS1 cell, and no newer arXiv paper covers that cell. The main criterion (two-colour R(s,t)) is not claimed and does not apply to a 3-colour cell.

## Clause-by-clause check of p1

p1 (verbatim): "A multicolour classical Ramsey record: an explicit edge colouring of K_N with no monochromatic forbidden clique in each colour (...), verified exhaustively, with N+1 strictly above the best lower bound in DS1 and any newer arXiv paper for that multicolour cell."

| clause | finding |
|---|---|
| multicolour classical Ramsey cell | R(3,4,7): 3 colours, complete-graph (classical) forbidden cliques K3, K4, K7 |
| explicit edge colouring of K_N | object/R_3_4_7.txt, a circulant on Z_153 (N = 153). Every distance 1..152 gets exactly one colour (asserted in work/check.py) |
| no monochromatic forbidden clique in each colour | confirmed by 3 methods, below |
| verified exhaustively | yes: a full enumeration over all 153 vertices for K3/K4, plus Bron-Kerbosch and a CaDiCaL UNSAT check for K7 |
| N+1 strictly above DS1 best | 154 > 152 (DS1 rev. #18, April 24, 2026, Table XIb, R(3,4,7) >= 152 [ExT]) |
| and any newer arXiv paper | none found that gives a bound for R(3,4,7), below |

## Object checks (my own code in work/, written before reading verify_circ.py)

shasum -a 256 object/R_3_4_7.txt:
```
e9fa8b95605e0f8e8d7b020855f7905ff9c02269c9d49a48abd725e7858d6a40  object/R_3_4_7.txt
```
This matches the hash in CLAIM.md.

work/check.py builds the full adjacency on all 153 vertices. It counts triangles in colour 1 and K4s in colour 2 over all vertices, with no symmetry assumption. For colour 3 it finds the maximum clique in N(0) by Bron-Kerbosch with pivoting, which is valid because each colour graph is a Cayley graph of Z_153, so it is vertex-transitive:
```
N 153 colours 3 degrees [36, 42, 74]
colour1 triangles (all vertices): 0
colour2 K4 (all vertices): 0
colour3 max clique in N(0): 5 => max clique through 0: 6
```
work/sat3.py runs CaDiCaL 1.5.3 (pysat). For each colour it asks for a (k-1)-clique in N(0): non-edges are pairwise exclusive, with a sequential-counter at-least-(k-1) constraint:
```
colour 1 K2-clique in N(0) (size 36): UNSAT
colour 2 K3-clique in N(0) (size 42): UNSAT
colour 3 K6-clique in N(0) (size 74): UNSAT
```
The author's checker (python3 verify_circ.py object/R_3_4_7.txt 3 4 7) agrees:
```
colour 3: degree 74, no K_7 (no K_6 among the neighbours of 0, exhaustive)
proves R(3,4,7) >= 154
PASS
```
Off-by-one: a colouring of K_153 proves R(3,4,7) >= 154. This is correct.

## DS1 (my own fetch, one plain request each, User-Agent naming V3R1T4S)

- https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1: HTTP 200, 17621 bytes, fetched at about 2026-10-25T11:13:06Z.
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf: HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc. This is identical to the hash in table_record.md. The PDF text reads "revision #18: April 24, 2026".
- The Table XIb row k = 4 (pdftotext -layout) reads "55 89 117 152 193 242" / "KrLR Ex17 Ex17 ExT 6.2.g ExT" for m = 4..9. So R(3,4,7) >= 152 [ExT].
- Null model (bounds implied by the general constructions in DS1 section 6.2): none reaches 154.
  - 6.2.g: R(3,4,7) >= 4R(4,6)-3 = 4*36-3 = 141.
  - 6.2.q: (R(3)-1)(R(4,7)-1) = 2*48 = 96.
  - 6.2.r: tiny.
  - Notes 6.1.2(c)-(h) list no other R(3,4,7) bound.

## Newer arXiv papers (my own searches)

- arXiv API query all:Ramsey AND submittedDate:[202604010000 TO 202610252359]: HTTP 200, totalResults 362, all 362 entries retrieved (dl/ax1.xml, sha256 9889f05b...). I screened the 215 math/cs entries by abstract. The only multicolour classical items are asymptotic: 2609.28455 R(3,3,k) = Theta(k^3/log^2 k), 2609.04596 an upper bound on R_r(k), and 2608.02537 odd cycles. The other multicolour items concern stars, cycles, matchings or ordered graphs. None gives a bound for R(3,4,7).
- The target-bank papers 2603.09172v5, 2608.18169v2, 2608.18769 and 2610.12122 (API id_list, HTTP 200) are all two-colour R(s,t).
- 2509.03784 (Wesley, SAT multicolour) gives R(K4,K4-e,K4-e) >= 35 and R(K3,K4,C4,C4) >= 49 only. 2601.15183 is asymptotic.
- Two web searches ("R(3,4,7)" Ramsey lower bound 2026; three-color R(3,k,m) circulant 2026) found no source giving R(3,4,7) >= 153 or higher.

## Caveats (they do not change the verdict)

- arXiv metadata search covers titles and abstracts, not full text. A paper that lists R(3,4,7) only inside its body, with no Ramsey keyword in its metadata, could be missed. I found no hint that such a paper exists.
- The "record" status is relative to the sources named in the criterion (DS1 plus newer arXiv). Unpublished web tables, for example Exoo's ExTa/ folder (the author recorded HTTP 403 for it), were not checked by me.
- I did not compare the colour-3 connection set against Kuznetsov's Table 2. Provenance does not affect validity, which was checked directly.

confirmed_scope: The circulant 3-colouring of K_153 in object/R_3_4_7.txt (sha256 e9fa8b95...6a40) has no colour-1 K3, no colour-2 K4 and no colour-3 K7, which I verified exhaustively by 3 independent methods, so R(3,4,7) >= 154, which is strictly above the R(3,4,7) >= 152 in DS1 revision #18 (April 24, 2026) Table XIb and above every bound for that cell in arXiv papers whose metadata (searched 2026-10-25) mentions Ramsey and that were submitted since April 2026.

pass: true
