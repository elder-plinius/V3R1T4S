# CRITERION skeptic — odd-graceful-trees-beyond-12
context: subagent (parent Task)
Fresh context; worked only from a scratch copy of the original claim workspace ([scratch]). Did not read REPORT, NOTES, attempts, LOG or other panel files.

## Criterion read literally
Full (a): for EACH n in 13..22, a file giving EVERY unlabeled tree on n vertices with an odd-graceful labeling; an independent checker
regenerates the trees, counts = A000055(n), matches every tree by canonical form, labels distinct in [0,2n-3], differences exactly {1,3,...,2n-3}.
Also: re-check latest DS6 and literature for a higher bound. Partial wins p1 (<=16) and p2 (<=20) are subsumed if (a) holds.

## What I checked
1. `sha256sum -c the original certificate hash list (not shipped; see object/CERTIFICATES.txt)`: all 21 cert files OK.
2. My own checker ([scratch].py, written from scratch and not derived from the claimant's code): for each line it checks that the parent array is a tree,
   that there are n labels, that the labels are distinct in [0,2n-3], and that the edge differences form exactly the set {1,3,...,2n-3}. It computes the free-tree canonical form
   (AHU at centre(s), min) and counts distinct forms. The counts come from my own Otter-formula implementation, which matches the OEIS A000055 %S/%T line.
   Result for every n=2..22: bad=0, lines = distinct canonical forms = A000055(n). Examples: n=13: 1301, n=16: 19320, n=20: 823065, n=21: 2144505,
   n=22: 5623756. The set of non-isomorphic trees for an order has exactly A000055(n) members. So getting A000055(n) pairwise-distinct canonical forms means every tree is covered.
3. Null-model and sanity checks on my checker: canonical form unchanged under 200 random relabelings (n=12). A swapped label and an out-of-range label
   are both rejected. A duplicated tree drops the distinct count from 551 to 550, so duplicates or omissions would be caught.
4. Claimant's regeneration checker code/ogcheck.c (leaf-addition regeneration, which does not use networkx or the searcher), compiled and run by me for
   every n=2..22: "PASS order n" each time, with 0 invalid, duplicate, missing or extra trees. The regenerated counts for orders 13..22 equal A000055.
5. Status/literature: I sent one GET (UA V3R1T4S-research-agent) to the DS6 article page at 2026-11-01 03:02 UTC (2026-10-31 23:02 EDT). It returned HTTP 200 and the same edition markers as the claim's copy
   (dates 2026-01-27 etc.), so I found no newer edition. DS6 3.6 in the claim's text says verification reaches "order up to 12" (Barrientos). One web search
   found nothing beyond 12, only order-12 enumeration and diameter<=5 results. Graceful-tree verifications to larger orders do not imply odd-gracefulness,
   so they do not subsume this result.

## Caveats (not disqualifying)
- Trees were generated with networkx, not nauty gentreeg. In the criterion, "as from nauty gentreeg" names the object (all unlabeled trees), not a required tool.
  Completeness is established independently of the generator by items 2 and 4.
- The claimant's arXiv literature query got HTTP 500, so its literature re-check is thin. My one search and the DS6 GET found no higher bound, but I
  cannot rule out an obscure unindexed result.
- Hygiene: the original claim workspace contains unrelated files from another target (A005164/TSASM: unrelated TSASM material, not shipped here). They have no bearing on this claim, but the bundle should be cleaned.
- Nothing is proved beyond n=22. Trees of order 1 are trivial.

confirmed_scope: Every tree on at most 22 vertices is odd-graceful: for each n = 2..22 the certificate lists A000055(n) pairwise non-isomorphic trees, each with a verified odd-graceful labeling (distinct labels in [0, 2n-3], edge differences exactly {1, 3, ..., 2n-3}).

Verdict: full success criterion (a) met. p1 and p2 are subsumed. Within the checks I could make, no higher prior bound than 12 was found.
pass: true
