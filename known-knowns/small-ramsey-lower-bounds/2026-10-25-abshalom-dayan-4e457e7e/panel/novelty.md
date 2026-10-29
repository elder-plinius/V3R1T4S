context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ .

# NOVELTY verdict: R(3,3,15) >= 272 (claim p1, small-ramsey-lower-bounds)

## 1. Primary table, fetched once (curl, User-Agent "V3R1T4S-novelty-skeptic/1.0", no retries)
- https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : fetched 2026-10-25T11:33:20Z, HTTP 200, 17621 bytes, page text "This Version ... Apr 24, 2026".
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf : fetched 2026-10-25T11:33:22Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (same hash as in table_record.md).
- Table XIb (pdftotext -layout), row k=3, columns m = 4..16: "30 45 61 85 103 129 150 174 194 217 242 269 291"; so R(3,3,14) >= 242, R(3,3,15) >= 269 (ref ExT), R(3,3,16) >= 291.
- DS1 text line: "the bounds 261 <= R (3, 3, 15) and 247 <= R (3, 3, 3, 7) were not published explicitly but are implied by 6.2.g and 6.2.h".
- DS1 Table Ia, row k=5 lower bounds, l=4..15: "43 59 80 101 133 149 183 203 233 267 275", so R(5,14) >= 267 [Kuz] and R(5,15) >= 275 are on the table.
- Claimed 272 > 269 by 3 (strict).

## 2. Object checked by my own code (work/mychk2.py, written from the definition)
- shasum -a 256 object/R_3_3_15.txt = 4e457e7ee1232a6b4c5ea299b7616c6e4329f04ba11531cadacd4a0d715e9ca7 (matches CLAIM.md).
- Output: "N 271 r 3 symmetric ok", "colour 1 triangles 0", "colour 2 triangles 0", "structure ok: circulant on 0..265, block 266..270 has no colour 3, cross edges colour 3", "deg0 in colour3 172", "max clique containing 0 in circulant colour 3 = 13" (exhaustive bitset branch and bound; vertex-transitivity of the circulant). Block vertices add at most 1 to a colour-3 clique, so max colour-3 clique <= 14 < 15. The object is valid, so R(3,3,15) >= 272 as a mathematical statement holds (and, by the same object minus the block, R(3,3,14) >= 267).
- (A first, structure-blind full-graph clique search hit my 7-minute cap with no output; the structural check above replaced it.)

## 3. Repository, read-only
- TROPHY_CASE.md (raw, main): fetched 2026-10-25T11:33:25Z, HTTP 200, 31235 bytes, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1; no occurrence of "ramsey" in it.
- Open pull requests via the GitHub API (pages 1-4, HTTP 200 each, 379 PRs; page 5 returned an empty list): none mentions R(3,3,15) or 272. Five open claim PRs are for the same target by the same pipeline: #731 R(3,3,11) >= 183, #732 R(3,3,12) >= 203, #733 R(3,3,14) >= 267, #734 R(3,5,7) >= 252, #735 R(3,3,9) >= 133. #733 is the sibling claim this object is built on; it does not beat 272 for the R(3,3,15) cell. Neither is third-party prior art.

## 4. Literature (last 24 months)
- Web searches (two) plus a read of arXiv:2509.03784 (HTTP 200, 279953 bytes, sha256 4b8e6947850feedd0a690eadedb7ffe9105bfb979648372af6ea023e2abc3ad3; grep for R(3,3,k) finds nothing): no paper since 2024 gives a lower bound for R(3,3,14) or R(3,3,15). Related 2026 items are asymptotic (Campos-Pohoata, arXiv:2601.*), or upper bounds (Boza, arXiv:2603.10851). The author's literature_record.md (arXiv API listings) agrees. Exoo's page http://cs.indstate.edu/ge/RAMSEY/ : fetched 2026-10-25T11:42:33Z, HTTP 200, 5609 bytes; no R(3,3,k) text found by grep (its ExTa folder was not opened; the author's record says it returned 403).
- Search was limited: a very recent unlisted preprint or unpublished Exoo data cannot be excluded.

## 5. Does a published construction or bound already imply >= 272?
- DS1 6.2.g: R(3,k,l) >= 4R(k,l-1)-3 gives only 261 for R(3,3,15) (DS1 says so). The colour-3 join (R(3,3,15) >= R(3,3,14) + 5) gives 247 from DS1's 242. No general theorem gives R(3,3,k) >= R(5,k), so R(5,14) >= 267 does not imply R(3,3,14) >= 267.
- The Exoo-Tatarevic paper (arXiv:1504.02403) publishes the METHOD (split the K5-free colour of a (5,k) colouring into two triangle-free colours) and used it for its R(3,3,k) entries. It predates Kuznetsov's R(5,14) >= 267 circulant (arXiv:1505.07186v5). Applying the method to that input and getting a valid split is a computational result, not a published statement. No located source states or implies R(3,3,14) >= 267 or R(3,3,15) >= 272.
- Honest weakness: the 272 is an application of a published method to a published input plus a folklore join, and the margin over the table is +3 (but +25 on the R(3,3,14) base). Strictness is met.

## Verdict
Primary table fetched honestly (HTTP 200, value 269 quoted). The object is valid by my own check. 272 strictly exceeds DS1's 269 and the implied 261/247. No open PR, trophy entry, or paper in the last 24 months that I could find reaches 272 for this cell, and no published construction implies it. Residual risk is only an unseen preprint or unpublished data.

pass: true
