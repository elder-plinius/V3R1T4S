context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ .

# NOVELTY verdict: R(3,3,11) >= 183 (claim p1)

novelty: CONFIRMED (183 strictly above every bound found, 174)

## Primary table (one plain request each, User-Agent "V3R1T4S-novelty-skeptic", no retries)
- Status page https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1: fetched 2026-10-25T08:43:55Z, HTTP 200, 17621 bytes, sha256 bdb5e3734f410b12377675bb08f120fd69f75fe9080705e2b391a1b35f9a0be4 (differs from the author's page hash; page body is dynamic; the PDF below is the authoritative table).
- PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf: fetched 2026-10-25T08:44:00Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc (identical to the author's record). Header: "revision #18: April 24, 2026".
- Table XIb (pdftotext), row k=3, column m=11: value 174, reference ExT (columns 4..16 read 30 45 61 85 103 129 150 174 194 217 242 269 291). Value read: 174. Claimed 183 > 174.
- Table Ia, row k=5, l=5..15 lower bounds: 43 59 80 101 133 149 183 203 233 267 275 -> R(5,11) >= 183 (reference Kuz), the source graph of the object.

## Independent check of the object (own checker work/chk.py, written before reading verify_circ.py)
- shasum -a 256 of object/R_3_3_11.txt: 622b79c6646d2617cd7f0b74c224ad3d5bd6cb856c6824ace5a5e30664461270 (matches CLAIM.md).
- Output: colour sizes {1: 19, 2: 15, 3: 57} distances, overlap 0, cover of 1..91 True; max clique (vertex-transitive, clique through vertex 0): colour 1 K3? False (max 2); colour 2 K3? False (max 2); colour 3 K11? False (max 10). So the colouring of K_182 is valid, R(3,3,11) >= 183 holds (correctness itself is the other skeptics' job).

## Literature, last 24 months (2024-10-25 .. 2026-10-25)
- arXiv API (one request per query, 2026-10-25T08:45Z, HTTP 200): query for R(3,3,11)/R(3,3,k)/R(3,3,10)/R(3,3,12) returned 1 paper in range (arXiv:2609.28455, asymptotic Theta for R(3,3,k)); query "Ramsey + lower bound(s) + three/multi colo(u)r" returned 44 entries, 15 in range, none states a bound for R(3,3,11) (checked 2509.03784 and 2601.15183 full text: grep for (3,3,k) / 3,3,1x empty). arXiv:2608.18769 (named in target bank) full text: two-colour R(m,n) only, no three-colour cell.
- WebSearch (2 queries): only Exoo-Tatarevic arXiv:1504.02403 (R(3,3,11): 162 -> 174 by splitting a (5,11) colouring); nothing gives 183.
- Exoo's Ramsey page https://cs.indstate.edu/ge/RAMSEY/index.html (HTTP 200): multicolour list shows R(3,3,3,4), R(3,3,4,4), R(3,3,7); no R(3,3,11) entry.
- Author's literature_record.md agrees (no R(3,k,m) hits beyond R(3,3,3), R(3,4,5), R(3,3,6)).

## Repo
- TROPHY_CASE.md (GitHub contents API, HTTP 200, 43863 bytes JSON, decoded 31012 chars): 0 occurrences of "ramsey".
- Open PRs (GitHub API, pages 1-4 HTTP 200, page 5 empty list; 357 open PRs scanned by title+body): no Ramsey/R(3,3,x) PR; two regex hits (#614, #509) are unrelated (AME states, qubit codes).

## Implied-bound check (published general constructions / related cells)
- DS1 6.2.g: R(3,k,l) >= 4R(k,l-1)-3 gives for (3,3,11): 4*R(3,10)-3 = 4*40-3 = 157 < 174 (R(3,10) >= 40 from Table Ia). Other items (6.2.h needs 4 colours; 6.2.l needs Paley graph K-free; 6.2.q/r/o product-type bounds) give far less than 183 for (3,3,11).
- Monotone neighbours: R(3,3,10) >= 150, R(3,3,12) >= 194 (Table XIb); neither forces 183.
- Related cell R(5,11) >= 183 is the origin of the object, but no published theorem turns R(5,k) >= N into R(3,3,k) >= N (the K5-free graph must be splittable into two triangle-free graphs; ExT only did it for the (5,k) graphs they had, and the 174 predates Kuznetsov's 182-vertex (5,11) circulant). The claim's value therefore does not follow from any published bound I found; it follows from the claimed explicit splitting, which I verified.

## Caveats
- Tie-break is not an issue: 183 > 174 by 9.
- Search is limited to arXiv API, two web searches, Exoo's page, DS1; unpublished data cannot be excluded. Exoo's ExTa/ folder was not fetched (author saw HTTP 403; not retried).
- "Novel" here means vs. published record; that the splitting method and the (5,11) circulant are others' work is credited in CLAIM.md.

pass: true
