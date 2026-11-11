# Criterion skeptic report: queens-graph-domatic-numbers, dom(Q_12) >= 21

context: subagent (Claude Code Agent tool, fresh context)
role: CRITERION skeptic (default fail unless the object genuinely meets the success criterion or a named partial win)
inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/dom-Q12-21-partition.txt (nothing else in the repository)
my code: panel/criterion-code/check_dom.py (sha256 38da42b8f7d973984986281d0429ca96e6ffa73413990ebf139afeb23911c7c7), written from the definitions alone, run with `python -I` (Python 3.14.2)

confirmed_scope: The file claim/dom-Q12-21-partition.txt (sha256 e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e on its raw CRLF bytes) partitions all 144 squares of the 12 x 12 board into 21 nonempty classes (labels 0..20), each dominating the queens graph Q_12. This gives dom(Q_12) >= 21, one more than the lower bound 20 in Table 1 of Lauri's Corrigendum (Discrete Math. Lett. 18 (2026) 34-35), and it meets the named partial win p1 for the (dom, n = 12) cell.

## Verdict in one paragraph

The object does what the claim says. Two independent domination tests (pairwise queen adjacency, and coverage by row, column, diagonal and anti-diagonal) agree that all 21 classes dominate Q_12. Labels run exactly 0..20. Class sizes are 6 (x3) and 7 (x18), which sum to 144. Both hashes in the claim match. The wrong adjacency models (rook, bishop, king, queen with only one diagonal direction) each make 0 of 21 classes dominate. All 8 board symmetries of the object pass. Every corrupted copy I built is rejected. Random relabelings with the same class sizes give 0 dominating classes in 2000 trials, and no linear labeling (a*r + b*c) mod k with k from 18 to 25 works, so the object is not a trivial construction. The literal criterion clauses are met. The only clause I cannot fully close is "the interval must still be open in any later paper found by a search, re-fetched immediately before claiming". The author did no fresh literature search in this run. My spot check (Corrigendum and OEIS re-fetched, plus two web searches) found nothing that settles dom(Q_12), but the full search belongs to the novelty skeptic.

## Clause-by-clause reading of the success criterion and p1

| Clause (literal) | Finding |
|---|---|
| Invariant: dom (domatic number, plain domination) | Checked with closed-neighbourhood domination in Q_n (row, column, both diagonals, any distance). The object is not also an idomatic or total-domatic partition: 1/21 classes are independent and 1/21 classes totally dominate. So it says nothing about idom or tdom, and the claim does not say it does. |
| n = 12 | 12 lines of 12 tokens, 144 cells. |
| "explicit partition of all n^2 squares into k classes" | Each cell carries exactly one label. There are 21 distinct labels, exactly 0..20, all nonempty. Sizes sum to 144. |
| "each class dominating Q_n" | 21/21, both implementations agree class by class (the code asserts equality). |
| "k above the current lower bound" | 21 > 20. I re-fetched the Corrigendum myself. It has the same sha256 as in CLAIM.md, and its Table 1 lists dom(Q_12) as "20–21". The abstract text says dom(Q12) ∈ {20, 21}. |
| One of the six open cells | (dom, 12) is listed in the criterion's six intervals. |
| "interval must still be open ... re-fetched immediately before claiming" | Partly evidenced. The author re-fetched the Corrigendum and OEIS A292192 at claim time, but did no fresh literature search (it says the last one was 2026-11-05). My spot check at 2026-11-11T17:59Z: Corrigendum unchanged; OEIS A292192 has no term past n = 10; two web searches found no later source settling dom(Q_12). The full novelty search belongs to the novelty skeptic. |
| One object, one cell | One file, one cell (dom, 12). |
| Claimed vs cited | Claimed and verified: lower bound 21 from the object. Cited, not re-proved and not checked by me: Lauri's upper bound dom(Q_12) <= 21. In the Corrigendum it rests on an enumeration that finds only eight dominating 6-sets. The claim keeps these apart correctly and does not claim exactness. |
| Partial win p1, literal: "an explicit partition beating the Corrigendum's lower bound for one of the 6 open (invariant, n) pairs" | Met. |
| Non-subsumed | Not implied by Table 1 (the lower bound there is 20), and not reached by naive constructions (random and linear null models below). No source found by my spot check already has a domatic 21-partition of Q_12. |

Remark, which does not widen my scope: raising the lower bound from 20 to 21 also fits the full criterion's wording "narrowing one of the six intervals". Together with Lauri's cited upper bound, it would give dom(Q_12) = 21. The object is consistent with Lauri's counting argument: a 21-partition needs at least 21*7 - 144 = 3 parts of size 6, and the object has exactly 3 pairwise disjoint dominating 6-sets. I did not check the upper bound, which would need an enumeration of the dominating 6-sets. So my confirmed_scope stays at the lower bound, as claimed.

## Commands and real output

Run from the run folder. Command: `python -I panel/criterion-code/check_dom.py claim/dom-Q12-21-partition.txt`

```
== 1. file bytes: dom-Q12-21-partition.txt
sha256(raw bytes)      = e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e
sha256(CRLF->LF bytes) = bc2433e6874495f692cf019621059178394cdafde073b9956262ea8f0b266cb7
  bytes: 377
  has_utf8_bom: False
  non_ascii_bytes: 0
  CR: 12
  LF: 12
  CRLF: 12
  tabs: 0
  lines: 12
  lines_matching_strict_format: 12
row lengths: [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]

== 2. main verdict, queen model (pairwise implementation)
distinct labels k = 21 | labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
class sizes: {0: 6, 1: 6, 2: 6, 3: 7, 4: 7, 5: 7, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7, 11: 7, 12: 7, 13: 7, 14: 7, 15: 7, 16: 7, 17: 7, 18: 7, 19: 7, 20: 7}
size histogram: {6: 3, 7: 18} | sum = 144
cells covered exactly once: True
  class  0 size 6 squares [(0, 0), (2, 4), (4, 10), (6, 6), (8, 2), (10, 8)] -> undominated(pairwise)=0 undominated(lines)=0
  class  1 size 6 squares [(0, 11), (2, 3), (4, 9), (6, 5), (8, 1), (10, 7)] -> undominated(pairwise)=0 undominated(lines)=0
  class  2 size 6 squares [(1, 3), (3, 9), (5, 5), (7, 1), (9, 7), (11, 11)] -> undominated(pairwise)=0 undominated(lines)=0
  class  3 size 7 squares [(3, 8), (4, 6), (5, 3), (5, 4), (6, 7), (7, 5), (8, 8)] -> undominated(pairwise)=0 undominated(lines)=0
  class  4 size 7 squares [(1, 1), (1, 9), (3, 7), (5, 1), (7, 11), (9, 5), (11, 3)] -> undominated(pairwise)=0 undominated(lines)=0
  class  5 size 7 squares [(0, 1), (1, 0), (3, 5), (5, 11), (7, 7), (9, 3), (11, 9)] -> undominated(pairwise)=0 undominated(lines)=0
  class  6 size 7 squares [(0, 7), (2, 1), (4, 3), (6, 9), (8, 11), (9, 2), (10, 5)] -> undominated(pairwise)=0 undominated(lines)=0
  class  7 size 7 squares [(0, 5), (2, 11), (4, 7), (6, 3), (8, 9), (10, 0), (11, 1)] -> undominated(pairwise)=0 undominated(lines)=0
  class  8 size 7 squares [(0, 8), (2, 6), (4, 0), (6, 10), (8, 4), (9, 9), (10, 2)] -> undominated(pairwise)=0 undominated(lines)=0
  class  9 size 7 squares [(1, 5), (3, 3), (3, 11), (5, 0), (7, 9), (9, 1), (11, 7)] -> undominated(pairwise)=0 undominated(lines)=0
  class 10 size 7 squares [(1, 11), (2, 5), (5, 9), (6, 2), (9, 6), (10, 1), (10, 10)] -> undominated(pairwise)=0 undominated(lines)=0
  class 11 size 7 squares [(0, 9), (1, 7), (3, 1), (5, 7), (7, 3), (9, 11), (11, 5)] -> undominated(pairwise)=0 undominated(lines)=0
  class 12 size 7 squares [(0, 2), (2, 8), (4, 4), (6, 0), (8, 6), (10, 11), (11, 10)] -> undominated(pairwise)=0 undominated(lines)=0
  class 13 size 7 squares [(0, 4), (2, 2), (2, 10), (4, 2), (6, 8), (8, 0), (10, 6)] -> undominated(pairwise)=0 undominated(lines)=0
  class 14 size 7 squares [(0, 10), (2, 9), (4, 1), (4, 5), (6, 11), (8, 7), (10, 3)] -> undominated(pairwise)=0 undominated(lines)=0
  class 15 size 7 squares [(0, 6), (2, 0), (4, 8), (6, 4), (8, 10), (10, 4), (11, 2)] -> undominated(pairwise)=0 undominated(lines)=0
  class 16 size 7 squares [(1, 4), (3, 6), (3, 10), (5, 2), (7, 8), (9, 8), (11, 0)] -> undominated(pairwise)=0 undominated(lines)=0
  class 17 size 7 squares [(0, 3), (1, 10), (2, 7), (4, 11), (6, 1), (8, 5), (10, 9)] -> undominated(pairwise)=0 undominated(lines)=0
  class 18 size 7 squares [(1, 2), (3, 4), (5, 10), (7, 6), (8, 3), (9, 0), (11, 8)] -> undominated(pairwise)=0 undominated(lines)=0
  class 19 size 7 squares [(1, 6), (3, 0), (5, 8), (7, 2), (7, 4), (9, 10), (11, 4)] -> undominated(pairwise)=0 undominated(lines)=0
  class 20 size 7 squares [(1, 8), (3, 2), (5, 6), (7, 0), (7, 10), (9, 4), (11, 6)] -> undominated(pairwise)=0 undominated(lines)=0
VERDICT queen: ok=True k=21 dominating_classes=21 (OK)
smallest class size: 6

== 3. sensitivity: wrong adjacency models must change the verdict
  model queen                    ok=True  dominating classes 21/21
  model rook                     ok=False dominating classes  0/21
  model bishop                   ok=False dominating classes  0/21
  model king                     ok=False dominating classes  0/21
  model queen_one_diagonal_only  ok=False dominating classes  0/21

== 4. positive control: all 8 board symmetries of the object must still pass
  dihedral images passing: 8 / 8

== 5. corrupted copies (each must be rejected unless noted)
  merge labels 19 and 20 (k=20): False | k=20 not above lower bound 20
  cell (0,0) relabelled 21 (new singleton class): False | 2 non-dominating classes
  last row deleted: False | shape is not 12x12
  one token dropped in row 5: False | shape is not 12x12
  rows cyclically shifted by 1 (not a symmetry): False | 15 non-dominating classes
  columns cyclically shifted by 1 (not a symmetry): False | 16 non-dominating classes
  single-cell relabellings that still pass: 0 / 2880
  one-byte-corrupted file hash differs: True

== 6. null models
  random relabellings with the same size multiset (2000 trials): mean dominating classes 0.000, max 0 of 21
  linear labelling (a*r+b*c) mod 18 with all classes dominating: None
  linear labelling (a*r+b*c) mod 19 with all classes dominating: None
  linear labelling (a*r+b*c) mod 20 with all classes dominating: None
  linear labelling (a*r+b*c) mod 21 with all classes dominating: None
  linear labelling (a*r+b*c) mod 22 with all classes dominating: None
  linear labelling (a*r+b*c) mod 23 with all classes dominating: None
  linear labelling (a*r+b*c) mod 24 with all classes dominating: None
  linear labelling (a*r+b*c) mod 25 with all classes dominating: None
  largest k reached by a linear labelling: None
```

Section 7 was added afterwards. I re-ran the script; it is deterministic with a fixed seed. The tail of the second run, then a second hash tool (PowerShell Get-FileHash) on the object and on my script:

```
  largest k reached by a linear labelling: None

== 7. consistency with the other cited upper bounds (idom(Q_12) <= 20, tdom(Q_12) <= 20)
  (if all 21 classes were independent, or all totally dominating, a cited upper bound would be contradicted)
  classes that are independent sets: 1 / 21
  classes that are total dominating sets: 1 / 21
e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e
38da42b8f7d973984986281d0429ca96e6ffa73413990ebf139afeb23911c7c7
```

How to read the controls:
- Section 3: domination holds only under the true queen model. Dropping one diagonal direction already kills all 21 classes, so both diagonals are actually used.
- Section 5: 0 of 2880 single-cell relabelings pass. Moving any one square out of any class breaks that class, so all 21 classes are minimal dominating sets. My checker therefore rejects every one-cell corruption.
- Section 6: a random class of the same size never dominates. The object is highly structured, not luck.
- Section 7: the object does not contradict the Corrigendum's upper bounds idom(Q_12) <= 20 and tdom(Q_12) <= 20.

## Spot check that the interval is still open

I fetched each source once with curl and User-Agent `V3R1T4S-research-agent/1.0 (honest single fetch)`, saved into a private scratch folder, no retries.

Corrigendum PDF (https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf). The text `time_utc_now` is a literal word left in my curl format string, not a value. The next lines are `date -u` and the sha256 of the downloaded bytes:

```
HTTP 200 bytes 274739 time_utc_now
2026-11-11T17:59:27Z
b4eb41f90a01eb7af70ff6b8428bf9fa67d0f7b7aff37b48b7865acc2956d154
```

This hash is identical to the one in CLAIM.md. The Corrigendum was published online 26 August 2026. Reading the PDF: Table 1 has the row "dom(Qn) 8 8 10 11 12 15 17 18–20 20–21" for n = 4..12, and the abstract replacement reads "dom(Q11) ∈ {18, 19, 20}, and dom(Q12) ∈ {20, 21}". The corrected proof of Theorem 3.6 derives dom(Q12) <= 21: it says a 22-partition needs at least ten 6-parts, and that only eight dominating 6-sets exist. The Corrigendum uses the same definition of domatic partition as the claim.

OEIS A292192 (https://oeis.org/search?q=id:A292192&fmt=text):

```
HTTP 200 bytes 969
2026-11-11T17:59:28Z
```

The content has revision #13 (Jan 25 2026), the sequence data "1,4,5,8,8,10,11,12,13,16" (n = 1..10), and the keywords "nonn,hard,more". There is no term for n = 11 or 12, so nothing there closes the dom(Q_12) cell.

Web searches (standard mode, 2 queries: "domatic number queens graph Q12 21" and "Lauri queens graphs domatic corrigendum 2026 dom(Q12) erratum new bound"). The results were the 2025 paper (https://www.dmlett.com/archive/v16/DML25_v16_pp94-99.pdf), the Corrigendum (https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf), Wikipedia "Queen's graph" (https://en.wikipedia.org/wiki/Queen%27s_graph), the domatic number game (https://arxiv.org/pdf/2508.10754), fractional domatic number (https://arxiv.org/pdf/2508.19617), and older queen-domination papers. None reports a domatic 21-partition of Q_12 or settles dom(Q_12). One result, https://arxiv.org/pdf/2603.13522, gave no visible title; its identifier dates it to March 2026, before the Corrigendum. I did not open it; that is left to the novelty skeptic.

## Oddities and caveats

1. OEIS A292192 is stale relative to the Corrigendum: it lists a(9) = 13 and a(10) = 16, while the Corrigendum gives dom(Q9) = 15 and dom(Q10) = 17. This is not this cell, and CLAIM.md's statement "terms stop at n = 10" is accurate. It means OEIS cannot be used as a stand-in for the current Table 1.
2. The author made no fresh literature search at claim time (last one 2026-11-05). This falls short of the criterion's "re-fetched immediately before claiming" for the "found by a search" part. My pass on the criterion relies on the novelty skeptic's full search confirming that no later source closes the cell.
3. The upper bound dom(Q_12) <= 21 is only cited, and I did not verify it. The claim correctly does not claim dom(Q_12) = 21 or an A292192 extension (which would need n = 11 as well).
4. The package contains no text addressed to agents or reviewers; I saw none.

pass: true
