# REPRODUCE skeptic — odd-graceful-trees-beyond-12
context: subagent (parent Task)

Scratch copy: [scratch] (copied from [original claim workspace]). Own code: [scratch].
Read only the original claim materials, recorded results and status sources, and (after writing and running my checkers) the original code. The original run materials are not shipped in that form. Did not read REPORT, NOTES, attempts, LOG, or other panel files. No web requests (none needed).

## Definition used (quoted from the DS6 snapshot (not shipped) §3.6, Gallian DS6)
"Gnanajothi [1202, p. 182] defined a graph G with q edges to be odd-graceful if there is an injection f from V (G) to {0, 1, 2, . . . , 2q − 1} such that, when each edge xy is assigned the label |f (x) − f (y)|, the resulting edge labels are {1, 3, 5, . . . , 2q − 1}."
For a tree on n vertices q = n−1: labels distinct in [0, 2n−3], edge differences exactly {1,3,…,2n−3}.

## Independent checks (written before reading author code)
1. sha256sum -c the original certificate hash list (not shipped; see object/CERTIFICATES.txt): all 21 files OK.
2. Tree counts: own Otter-formula script (otter.py) gives t(n) for n=2..22 = 1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320,48629,123867,317955,823065,2144505,5623756; equals saved the OEIS A000055 snapshot (not shipped) (%S/%T, offset 0).
3. myck.c (own checker, every line of every file, no sampling): parses 'p_1..p_{n-1} | f(0)..f(n-1)' strictly (exact token count); checks 0<=p_i<i (so it is a tree on n vertices); labels distinct in [0,2n-3]; each edge diff odd, distinct, and the full set {1,…,2n-3} hit; canonical form = AHU parenthesis code rooted at center(s), min over centers; rejects duplicates. Result for every n=2..22: bad=0, dup=0, distinct = lines = A000055(n). Output identical on two runs (deterministic).
   - Canonical-form validation: on all n^(n-2) labeled trees (Prüfer) for n=4..7, distinct codes = 2,3,6,11.
4. regen.c (own exhaustive regeneration, independent of the author's networkx generator): all free trees of order n built by leaf addition from order n−1, deduped by canonical code; counts n=2..22 equal Otter/A000055 (5,623,756 at n=22). The sorted canonical-code set of every certificate file equals the regenerated set exactly for every n=2..22 (cmp.out: SETS_EQUAL ×21). Hence each certificate covers every isomorphism class exactly once, each with a valid odd-graceful labeling.

## Author's tooling (run after own checks)
- REPRODUCE.md: gcc ogcheck.c; "PASS order n" for n=2..22.
- code/check_py.py: "PASS" for n=2..22 (Otter counts match).

## Notes / caveats (not failures)
- Trees generated with networkx, not nauty gentreeg (disclosed in claim); my regeneration replaces that and agrees completely.
- n=1 (K1, q=0) is not covered by the files; the claim sentence and criterion range are n=2..22 / 13..22, and K1 is degenerate under the definition. Literature-bound re-check (DS6 says ≤12, Barrientos) is a novelty question for another panelist; DS6.txt quote verified present at lines 3870-3872.

## Verdict
Every property and claimed value (all trees of order 2..22, counts A000055(n), valid odd-graceful labeling for each) reproduced exhaustively and deterministically from the saved files with independent code.

pass: true
