context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# NOVELTY verdict (skeptic 1 of 3), claim R(3,5,7) >= 252 vs DS1 R(3,5,7) >= 241

## Status table (one plain request each, curl, User-Agent "V3R1T4S-novelty-skeptic", no retries)
- https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : fetched 2026-10-25T09:08:04Z..09:08:05Z, HTTP 200, 17621 bytes; page text "DS1: Apr 24, 2026" (latest revision). Page sha256 differs from the one in table_record.md (821635...a819fd vs 9095c6...), the byte count and revision date are identical, so I treat this as dynamic page markup, not a new revision.
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf : fetched 2026-10-25T09:08:09Z..09:08:12Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (same as table_record.md). pdftotext, Table XIb, row k=5: "89 139 181 241" for m=4..7 with references "Ex17 Ex17 Ex17 6.2.g". Value for R(3,5,7) = 241 (reference 6.2.g), column m=7. Claim's baseline is correct.

## Object
- shasum of object/R_3_5_7.txt: 3728547aec5e9b0b5779c21b5bf06cee6dfb90a01230c42389b821fcfa351976 (matches CLAIM.md).
- My own checker (work/mycheck.py, written from the definition, exact max-clique search from vertex 0 by transitivity): "partition of 1..125: True 125"; "colour 1 omega 2", "colour 2 omega 4", "colour 3 omega 6". So no K3 / K5 / K7 in colours 1/2/3 on Z_251, R(3,5,7) >= 252 (validity is the other skeptics' job, but it checks out).

## Search for anything >= 252 (all negative)
- TROPHY_CASE.md (raw GitHub, HTTP 200, 31235 bytes, 09:08:48Z): grep for ramsey / R(3 / 3,5,7 / 252 / 241 found nothing; it lists six other families.
- Open pull requests, GitHub API pages 1 and 2 (100 each, HTTP 200): title+body regex for ramsey|circulant|3,5,7 matched only PR 614 (an unrelated Z_19 quantum-state circulant claim). Pages beyond 2 not fetched.
- arXiv API (HTTP 200, 300 newest entries for Ramsey AND multicolor/three-colour/lower bounds; 110 entries within the last 24 months): only R(3,4,5)/R(3,3,6) upper-bound paper (arXiv:2603.10851) matches an R(3,k,m) pattern; none gives R(3,5,7). arXiv:2509.03784 (new bounds for small multicolour Ramsey numbers, Sept 2025) has no (3,5,7) string. Two web searches (standard mode) found no published R(3,5,7) bound.
- Full texts grepped for "3,5,7": Rowley arXiv:2203.13476, Exoo-Tatarevic arXiv:1504.02403, Kuznetsov arXiv:1505.07186: no hit. Exoo's page (HTTP 200, 5609 bytes): no hit.

## Do general constructions or related cells already imply >= 252? (hand arithmetic from DS1 Section 6.2 and Table XIb values)
- 6.2.g second form: R(7,5,3) >= 4R(6,3,3)-3 = 4*61-3 = 241 (R(3,3,6)=61 in Table XIb): this is the DS1 entry. Other orderings: 4R(4,4,3)-3 = 217, 4R(7,4)-3 = 193.
- 6.2.q/r and Rowley's L-product (6.2.j) with two-colour DS1 values give far less (roughly 78..236; best is about 236 via R(5,7) >= 80).
- Monotonicity only links (3,5,7) to dominated cells (3,5,6)=181, (3,4,7)=152 etc., all below 252.
- The source (7,9) circulant gives R(7,9) >= 252 but does not by itself imply a 3-colour bound: that needs the split of the K9-free colour into K3-free and K5-free parts, which is the claim's new content (Exoo-Tatarevic splitting method applied to this cell; their paper does not treat (3,5,7)).
No published construction or bound found that reaches 252.

## Verdict
252 > 241 strictly; no newer source, trophy-case entry or open PR in the checked scope; no general construction implies it. Caveats: GitHub PRs only pages 1-2; Exoo's ExTa folder was not reachable; literature search is search-engine/arXiv-API based, not exhaustive.

novelty: confirmed
pass: true
