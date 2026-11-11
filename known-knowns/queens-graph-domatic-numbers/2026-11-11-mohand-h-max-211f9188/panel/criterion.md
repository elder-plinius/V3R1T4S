# Criterion skeptic report: tdom(Q_10) >= 16

context: subagent (Claude Code Agent tool, fresh context)
role: CRITERION skeptic (literal match of the result against the bank success criterion / named partial win)
inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/tdom-Q10-16-partition.txt (nothing else in the repository)

confirmed_scope: The file claim/tdom-Q10-16-partition.txt (raw-byte sha256 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec) labels each of the 100 squares of the 10 x 10 board with one of 16 labels so that every one of the 16 classes totally dominates the queens graph Q_10 (open neighbourhoods: every square, members included, shares a row, column or diagonal with a different member of the class), hence tdom(Q_10) >= 16, one above the lower bound 15 listed for tdom(Q_10) in Table 1 of Lauri's Corrigendum (Discrete Math. Lett. 18 (2026) 34-35) as re-fetched on 2026-11-11.

## 1. Clause-by-clause reading of the criterion and of partial win p1

| Clause | Requirement (literal) | Finding |
|---|---|---|
| Invariant | total domatic (tdom), not dom or idom | The object is checked against TOTAL domination (open neighbourhood). A control grid shows the checker separates total from plain domination (section 3). Claim names tdom throughout. OK |
| Cell | one of the six open cells; here tdom(Q_10) in {15,16} | n = 10, 100 squares, tdom. The cell is listed verbatim in the criterion. One object, one cell. OK |
| Explicit partition of all n^2 squares into k classes | every square in exactly one class | 10 lines x 10 integers, 16 distinct labels 0..15, sizes 6 (x14) + 8 (x2) = 100. Each square carries exactly one label by construction of the format. OK |
| Each class total dominating | for every class and every square, a different member of the class is queen-adjacent | Verified by my own checker: 0 failing classes; minimum number of in-class neighbours over all squares is 1 for every class; no member is isolated in its own class. OK |
| k above the current lower bound | k > 15 | k = 16 > 15. Lower bound 15 confirmed in the re-fetched Corrigendum (section 4). OK |
| Interval still open in any later erratum/paper found by a search | | Author made no literature search (stated in CLAIM.md). My spot check (2 web searches) found nothing newer than the Corrigendum's table; results still describe tdom(Q_10) as 15 or 16. Full novelty check belongs to the novelty skeptic. Not contradicted |
| Interval still open in live OEIS entries (A292192 and related), re-fetched | | Author did NOT re-fetch A292192 or any OEIS entry (stated in CLAIM.md). I re-fetched once (section 4): OEIS search "domatic queen" returns 5 entries, none of them a total domatic sequence; A292192 is the plain domatic number. OEIS does not close the tdom(Q_10) interval. Procedural gap on the author's side, cured by panel re-fetch |
| Claimed vs cited | | Only the lower bound is claimed; the upper bound 16 is explicitly cited to Lauri, not re-proved. Consistent with p1 |
| Partial win p1 | "Any single raised lower bound (an explicit partition beating the Corrigendum's lower bound for one of the 6 open (invariant, n) pairs)" | Met literally: explicit partition, beats the Corrigendum lower bound 15 by 1, cell is one of the six open pairs |

Hidden quantifiers / stretched definitions checked:
- "total" means open neighbourhood; a square is never adjacent to itself. My checker implements exactly that (a != b test inside adjacency).
- Queen adjacency is graph adjacency with no blocking, both diagonal directions (|r-r'| = |c-c'|). Rook-only, bishop-only and king adjacency all give a different verdict (all 16 classes fail), so the verdict depends on the queen-graph definition, as it should.
- "Partition of all n^2 squares": no square unlabelled, no duplicate labels per square; 16 classes all non-empty.
- Not subsumed by a weaker invariant: a total dominating partition is automatically a plain dominating one, but the claim is about tdom specifically, and the tdom cell is distinct from the dom/idom cells.
- Remark, not claimed by the author: the Corrigendum's Table 1 gives the total domination number gamma_t(Q_10) = 6, so tdom(Q_10) <= floor(100/6) = 16; together with this object, tdom(Q_10) = 16 exactly. The claim conservatively claims only the lower bound (p1), which is the correct scope for what the package itself proves.

## 2. Hash and object check (my own checker, written from the definition)

Code: panel/criterion-code/check_tdom.py (run with `python -I -B`).

```
> python -I -B check_tdom.py ..\..\claim\tdom-Q10-16-partition.txt
bytes: 250
sha256 raw: 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec
sha256 LF-normalised: cb3583332b8beb836a61d080eae4f645d27ba8cc513c0e682d45b7a61030f396
CRLF count: 10  bare LF count: 0
n = 10  squares = 100
labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
class sizes: {0: 6, 1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6, 11: 6, 12: 6, 13: 6, 14: 8, 15: 8}
size histogram: {6: 14, 8: 2}
MAIN  queen/total : k=16 failing classes=[]
min in-class queen-neighbours per class: {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
members isolated inside their own class: none
CTRL  queen/plain  : k=16 failing classes=[]
CTRL  rook/total   : k=16 failing classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
CTRL  bishop/total : k=16 failing classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
CTRL  king/total   : k=16 failing classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
CORRUPT random swaps of two differently-labelled squares: rejected 300 / 300
CORRUPT move one square out of a 6-class: rejected 84 / 84
CORRUPT merge class 15 into 0: k=15 failing=[]
CORRUPT first '13'->'12' in raw bytes: sha256=a3b56bdabc108c9e k=16 failing=[13]
```

Both hashes match CLAIM.md and REPRODUCE.md (raw CRLF bytes and LF-normalised text). The parser is strict (ASCII only, single spaces, square grid).

## 3. Sensitivity controls and null models

Plain vs total, on a control grid where they must differ (panel/criterion-code/control_plain_vs_total.py): an independent dominating 5-set I of Q_10 is found by search; grid = {class 0 = I, class 1 = the rest}. I dominates but no member of I has a neighbour in I.

```
> python -I -B control_plain_vs_total.py
independent dominating set found: [(0, 2), (6, 0), (4, 4), (8, 6), (2, 8)]
control grid plain verdict : (2, [])
control grid total verdict : (2, [0])
```

So the same verdict() routine accepts this grid under plain domination and rejects class 0 under total domination: the checker really tests the open-neighbourhood condition. On the claimed grid plain and total both pass (expected: total domination implies domination).

Random null model (panel/criterion-code/null_random.py): random labellings with the same class sizes.

```
> python -I -B null_random.py
random same-size labellings: 2000 trials, all-16-classes-total-dominating: 0, mean good classes per labelling: 0.003
```

The passing verdict is not something a generic labelling achieves; the object is specific and fragile (every tested corruption is rejected, except the deliberate merge which correctly reports k = 15).

## 4. Status sources re-fetched (spot check; full novelty check is another skeptic's job)

Corrigendum PDF, one curl fetch with the project user agent, saved under panel/criterion-code/fetched/:

```
HTTP 200 bytes 274739
2026-11-11T18:41:15Z
b4eb41f90a01eb7af70ff6b8428bf9fa67d0f7b7aff37b48b7865acc2956d154
```

Identical size and sha256 to the record in CLAIM.md (fetched 18:20:59Z there). Text of Table 1 extracted with a stdlib-only inflater (panel/criterion-code/pdf_strings.py; the en dash prints as `{` in this font encoding):

```
n 456789101112 ... \015 t \050 Q n \051 234455677 dom\050 Q n \051 88101112 1517 18{2020{21
idom\050 Q n \051 5 7 8 10 12 15 16 18 18{20 tdom\050 Q n \051 88911121415{1616{1718{20
```

Row tdom(Q_n), n = 4..12: 8 8 9 11 12 14 15-16 16-17 18-20, so tdom(Q_10) is 15-16 in the Corrigendum, as CLAIM.md says. Row gamma_t(Q_n): 2 3 4 4 5 5 6 7 7, so gamma_t(Q_10) = 6.

OEIS, one curl fetch of the text-format search "domatic queen" (saved under panel/criterion-code/fetched/), 2026-11-11T18:41:57Z, HTTP 200, 27504 bytes:

```
Showing 1-5 of 5
%I A292192 #13 Jan 25 2026 11:09:23
%S A292192 1,4,5,8,8,10,11,12,13,16
%N A292192 Domatic number of the n X n queen graph.
%N A000170 Number of ways of placing n nonattacking queens on an n X n board.
%N A075458 Domination number for queens' graph Q(n).
%N A075324 Independent domination number for queens' graph Q(n).
%N A088202 Chromatic number of the n X n queen graph.
```

No OEIS entry for the total domatic number of the queens graph exists in this search, so OEIS does not settle tdom(Q_10).

Web search spot check (2 queries): results still cite Lauri's bounds tdom(Q_10) in {15, 16}; nothing newer surfaced. Sources seen in results: https://www.dmlett.com/archive/v16/DML25_v16_pp94-99.pdf , https://oeis.org/A303003 , https://en.wikipedia.org/wiki/Queen%27s_graph .

## 5. Odd points (none blocking for p1)

1. The author did not re-fetch any OEIS entry and made no literature search, which the criterion asks for "immediately before claiming". CLAIM.md says so openly. I re-fetched the OEIS search and the Corrigendum myself (above); the novelty skeptic should do the full search.
2. Live OEIS A292192 is stale relative to the Corrigendum: its a(9)=13 and a(10)=16 come from Lauri's original Table 1.1, while the Corrigendum's corrected dom row gives dom(Q_9)=15 and dom(Q_10)=17. This concerns the plain domatic cell, not tdom, and does not affect this claim, but it is worth knowing for the dom(Q_11)/dom(Q_12) claims of this project.
3. The CLAIM.md statement about the repository's pull requests (only drafts on other cells) was not checked by me (outside my read scope).
4. No text in the claim package addressed agents or reviewers.
5. The re-fetched PDF contains a personal contact line of the paper's author; it is not reproduced here.

## Verdict

The object meets partial win p1 literally: an explicit partition of all 100 squares of Q_10 into 16 total dominating classes, beating the Corrigendum's lower bound 15 for the open cell tdom(Q_10). The only shortfall is procedural (author-side OEIS/literature re-fetch missing), and the panel re-fetch done here finds the cell still open in both the Corrigendum and live OEIS. The full success criterion is not claimed; with the cited upper bound the cell would be settled at 16, but that relies on Lauri's bound, not on this package.

pass: true
