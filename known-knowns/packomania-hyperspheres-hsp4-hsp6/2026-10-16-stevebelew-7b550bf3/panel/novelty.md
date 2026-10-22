# Novelty verdict, hsp4 N = 104

context: subagent (Claude Code Agent tool, fresh context for this one claim)
role: novelty skeptic (one of three)
claim folder read: CLAIM.md, REPRODUCE.md, hsp4-104-candidate.txt (head), hsp4-104-posted.txt (head), hsp4_radius_as_fetched.txt (row 104)
candidate value (from CLAIM.md, recomputed below): r* = 0.240538697623896582... ; posted table value: 0.240535464233

All fetches below were made exactly once, plain curl, User-Agent "V3R1T4S skeptic", no retries. Times are from `date -u` immediately before each request.

## 1. Live table

- URL: https://packomania.com/hsp4/txt/radius.txt
- time: Fri Oct 16 21:25:19 UTC 2026
- HTTP: 200
- row 104: `104 0.240535464233`
- file: 299 rows, MD5 deb4cbcd0a0131989fbf6d1adf1e85f9, byte-identical to hsp4_radius_as_fetched.txt (cmp: identical). The snapshot value is still the live value.

## 2. Status page

- URL: https://packomania.com/hsp4/hsp4.html
- time: Fri Oct 16 21:25:25 UTC 2026
- HTTP: 200
- quoted: `Last update: 06-Jul-2025`
- History of updates, complete: 04-Jul-2025 (first presentation N = 2 to 100), 05-Jul-2025 (extension to N = 200), 06-Jul-2025 (extension to N = 300). No entry newer than 06-Jul-2025, none mentioning N = 104. The table row on the page reads `104 0.240535464233 ... [31]` (E. Specht's own program), consistent with radius.txt.

## 3. Pending-requests queue

- URL: https://packomania.com/pending-requests.html
- time: Fri Oct 16 21:25:37 UTC 2026
- HTTP: 200
- page dated 08-Oct-2026. Categories listed: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, and one `*many*`. No line contains "hsp"; no hsp4 range is listed, so N = 104 lies inside no hsp4 range on the page.
- QUEUE CAVEAT (cannot be resolved from the page): `26-Sep-2026 01:11  Moki & Julio  *many*  4666 candidates total` is category-unspecified. See section 7: the same authors' public repository lists an hsp4 N = 104 candidate, so it is likely that this bundle contains one. Per the bank entry, N = 104 must be re-checked against the live table once that bundle leaves the pending list.

## 4. TROPHY_CASE.md

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
- time: Fri Oct 16 21:25:45 UTC 2026
- HTTP: 200
- 100 lines; grep for "hsp4", "hypersphere", "packomania", "packing", "sphere" and the whole word "104": zero hits each. The file lists six families plus two cipher commitments; no hypersphere family is recorded there.

## 5. Open pull requests and the merged family

- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
- time: Fri Oct 16 21:25:58 UTC 2026
- HTTP: 200
- 78 open PRs (fits in one page). Open PRs for target packomania-hyperspheres-hsp4-hsp6: #242 (N=79), #243 (N=67), #244 (N=91), #245 (N=81), #246 (N=88), #247 (N=94), #248 (N=89), #249 (N=74), #250 (N=80), #251 (N=111). None is N = 104. The only PRs whose title or body contain the whole word "104" are #218, #221, #222 (fmm-additive-complexity, rank 104, unrelated).
- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6
- time: Fri Oct 16 21:26:07 UTC 2026
- HTTP: 200
- 12 directories, all dated 2026-10-14. Directory names do not carry N, so one further fetch resolved them:
- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1
- time: Fri Oct 16 21:26:26 UTC 2026
- HTTP: 200 (truncated: False)
- object file names in the family: hsp4-30, 35, 42, 48, 54, 62, 63, 64, 66, 69, 74, 75. No hsp4-104, no path in the family containing "104". Matches the list given in the brief.

## 6. Literature search (2024-2026)

Web searches run (extended mode where noted):
- "104 equal hyperspheres packed in 4-dimensional ball best known radius 0.2405" (extended): only general sphere-packing pages (Wikipedia, MathWorld, Cohn's Notices article, hyperbolic 4-space bounds). Nothing on finite packings of 104 balls in a 4-ball.
- "packing equal balls in a 4-ball hypersphere packings container sphere 2025 2026 arXiv Packomania hsp4" (extended): arXiv 2305.10023 (equal spheres in a 3-ball, 2023), Stoyan and Yaskov 2012 and Stoyan et al. 2020 (hyperspheres in a hypersphere, both older than 24 months and predate Specht's July 2025 table), the Packomania front page, and a GitHub topic page mentioning a repository claiming "6,071 new best-known packings ... balls in 4-6 D". That lead is followed in section 7.
- "arXiv 2025 OR 2026 hyperspheres packing in a hypersphere / in a 4-ball improved best-known Specht": no 2025-2026 preprint on finite packings in a 4-ball; hits were hyperbolic-space packings and density bounds.
- "github 6,071 new best-known packings equal circles spheres hyperspheres Packomania": no direct hit (resolved instead via the topic page below).
No paper or dataset from 2024-2026 was found that lists a packing of 104 equal balls in a 4-ball above 0.240535464233, other than the repository in section 7.

## 7. Competing public claim: Moki & Julio repository (the queue bundle's authors)

- URL: https://github.com/topics/sphere-packing?o=desc&s=updated
- time: Fri Oct 16 21:26:51 UTC 2026, HTTP 200. Identifies repository "moki-julio-circle-packing" (Zenodo DOI 10.5281/zenodo.22981305), described as "6,071 new best-known packings of equal circles, spheres and hyperspheres (Packomania, 21 tables: ... balls in 4-6 D) ... By Moki&Julio".
- URL: https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/README.md
- time: Fri Oct 16 21:27:17 UTC 2026, HTTP 200. Quotes: "Table - equal balls in the unit ball of dimension 4 (hsp4, Packomania page last updated July 2025): 220 records, N = 57-300. Largest gains ... N = 67 +0.017 %"; "What's new in version 2.6 (2026-09-26)"; the hsp4 shelf first appeared in v2.4 (2026-09-26). The README states these are submissions against Packomania's tables; the queue bundle of the same date and authors is therefore very likely to include them.
- URL: https://api.github.com/repos/Hashirama1337s/moki-julio-circle-packing/git/trees/main?recursive=1
- time: Fri Oct 16 21:27:20 UTC 2026, HTTP 200, 261 entries. hsp4 data lives in certificates/hsp4.zip and packomania/hsp4.zip (archives, not downloaded).
- URL: https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/MANIFEST.csv
- time: Fri Oct 16 21:27:37 UTC 2026, HTTP 200, 6071 data rows, 220 hsp4 rows. Row for our cell:
  `hsp4,104,0.240535464233,0.2405354810907891588282257,7.008442e-08,REFINEMENT,dp`
- URL: https://raw.githubusercontent.com/Hashirama1337s/moki-julio-circle-packing/main/RESULTS_TABLE.md
- time: Fri Oct 16 21:27:39 UTC 2026, HTTP 200. hsp4 section row: `| 104 | 0.2405354810907891588282257 | 0.240535464233 | +7.008e-08 | dp |`.

Comparison (Python decimal, 60 digits, r* recomputed from hsp4-104-candidate.txt as min of half the minimum pairwise distance and 1 minus the largest centre norm; mpmath was not installed in this shell, so the decimal module was used):
- N = 104 points read
- r* candidate = 0.240538697623896582089346515939...
- live table = 0.240535464233; candidate minus table = 3.2334e-06
- Moki & Julio = 0.2405354810907891588282257; candidate minus Moki & Julio = 3.2165e-06 (strictly greater, margin far above 1e-10)
Their value is a published claim I did not verify from coordinates (archive not downloaded); the point is that even taken at face value it is below our candidate by 3.2e-06, so it does not match or beat it. Should Packomania accept their N = 104 entry, the live value would rise to about 0.240535481091, and this candidate would still exceed it by more than 3e-06.

## Verdict

- live N = 104 value unchanged from snapshot: yes (byte-identical file)
- no history entry newer than 06-Jul-2025 covering (4, 104): confirmed
- no hsp4 range on the pending page includes 104: confirmed (no hsp4 line at all); the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved from the page; section 7 makes it likely to contain an hsp4 N = 104 candidate at 0.240535481091, which this candidate beats. The cell must be re-checked against the live table once that bundle disappears from the pending list.
- TROPHY_CASE, merged family (12 cells, none 104), open PRs (10 hsp4 cells, none 104): no match
- literature 2024-2026: nothing at or above the candidate; the one public competing value (Moki & Julio, 0.240535481091) is strictly below it by 3.2e-06
- the candidate strictly beats everything found, by at least 3.2e-06 against the best competing value; not a tie.

pass: true
