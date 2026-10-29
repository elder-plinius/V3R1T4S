context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# NOVELTY verdict: R(3,3,9) >= 133 (claim p1, target small-ramsey-lower-bounds)

novelty: CONFIRMED (strictly above every bound I could find; no tie)

## Primary table (one plain request each, User-Agent "V3R1T4S-novelty-skeptic/1.0 (read-only check)", no retries)
- Status page https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1: fetched 2026-10-25T09:22:05Z, HTTP 200, 17621 bytes, page text "Apr 24, 2026" (revision of April 24, 2026).
- PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf: fetched 2026-10-25T09:22:07Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (same as the author's table_record.md).
- Table XIb ("Three colors", pdftotext -layout), row k=3, m=4..16: `30 45 61 85 103 129 150 174 194 217 242 269 291`; references `Ka2 Ex2 ExT Ex18 Ex18 Ex18 ExT ...`. So R(3,3,9) >= 129 [Ex18] (column m=9). Claim 133 > 129 by 4.
- DS1 comment (c)/(f): Rowley's bounds concern R(3,6,6), R(3,7,7), ..., R(3,9,9), not R(3,3,9).

## Independent check of the object (own code work/chk.py, vertex-transitive clique search at vertex 0)
- sha256 of object/R_3_3_9.txt = a88af7a9fb8fc8eb0ddf226628db6f59df6c1fb8504ed3ec80d2eeaf972a64cd (matches).
- Output: `dists 66 True` (the three colours partition distances 1..66 exactly), `colour 1 max clique 2 ok`, `colour 2 max clique 2 ok`, `colour 3 max clique 8 ok`. So no K3 in colours 1 and 2, no K9 in colour 3 on 132 vertices, R(3,3,9) >= 133.
- Union of colours 1 and 2 equals, as a set, the 27 distances of the K5-free colour of Kuznetsov's (5,9) circulant on Z_132 (Table 2 of arXiv:1505.07186v5, fetched; check printed `True 27`). Provenance as stated.

## Searches
- This repo, TROPHY_CASE.md (raw GitHub, HTTP 200, 31235 bytes, sha256 b946f68e...): grep for "ramsey", "3,3,9", "R(3" gives no line.
- Open pull requests (GitHub API, pages 1 and 2, HTTP 200 each, 200 PRs, numbers 510..729): no title or body matches ramsey, R(3,3, small-ramsey or circulant. GitHub issue search "ramsey" in the repo: total_count 0.
- arXiv API (HTTP 200), "multicolor Ramsey" AND "lower bound", newest first, entries published since 2024-10 (newest 2026-10-17), relevant hits are 2601.15183 (asymptotic multicolor lower bounds), 2509.03784 (K4/C4 mixed numbers, SAT), 2609.28455 (R(3,3,k) = Theta(k^3/log^2 k), asymptotic, no constants, no value at k=9), plus papers on trees, matchings, stars, K_{2,t}. None states a bound for R(3,3,9).
- Exoo's page http://cs.indstate.edu/ge/RAMSEY/ (HTTP 200, fetched 2026-10-25T09:22:59Z, "attempt to update" note dated Apr 09, 2024): multicolour list is R(4,4,4,4), R(5,5,5), R(3,3,3,4), R(3,3,4,4), R(3,3,7) > 78, R(3,4,5); no R(3,3,9) above 129.
- Exoo-Tatarevic 2015 (arXiv:1504.02403v3, fetched, HTTP 200): its Table lists R(3,3,k) for k = 6, 10..16 only (R(3,3,10) 147->150, etc.); no entry for k = 9. Section 3.5 describes the splitting method as a heuristic that "there is no guarantee ... will work", and says the splitting failed for their best (5,13) and (5,16) colourings. Kuznetsov's order-132 (5,9) colouring (arXiv:1505.07186v5, May 2015) came after, and its paper has no three-colour bound.
- The author's literature_record.md is consistent with this; I did not rely on it.

## Does a published construction or bound for a related cell imply >= 133?
- R(5,9) >= 133 in DS1 (Kuz) is the related cell, but a (5,9)-colouring gives a (3,3,9)-colouring only if the K5-free colour splits into two K3-free graphs. That is not a theorem; ExT says it can fail. DS1's own row shows both outcomes: R(3,3,11) >= 174 vs R(5,11) >= 183, R(3,3,13) >= 217 vs R(5,13) >= 233. So the (5,9) bound does not imply 133 and the split had to be exhibited; the object exhibits it.
- Larger cells (R(3,3,10) >= 150, R(3,4,9) >= 242) do not give R(3,3,9) >= 133 by a simple argument (colour-3 degree in a 149-vertex colouring is only forced to about 68 by R(3,10) bounds).
- Asymptotic result 2609.28455 gives no explicit constant, so no value at k = 9.

## Caveats (not blocking)
- Exoo's ExTa/ folder was answered HTTP 403 for the author and not retried by me (not fetched). Unpublished constructions there cannot be excluded; DS1 is the status source and it says 129.
- The claim is a partial win p1 (multicolour record); DS1 is the survey of record and it lists 129, so 133 is strictly above, not a tie.

pass: true
