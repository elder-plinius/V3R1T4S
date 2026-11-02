context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ 

# NOVELTY verdict: R(3,4,7) >= 154 (claim/object/R_3_4_7.txt)

novelty: CONFIRMED (strictly beats everything I could find; margin +2 over DS1)

## 1. Primary table, fetched once each, honest client (curl, User-Agent "V3R1T4S-novelty-skeptic (read-only check)", no retries)
- https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : fetched 2026-10-25T11:04:17Z, HTTP 200, 17621 bytes, sha256 f7d0c5a4e36ad24008173d2f9bc9adb11d4b5ea742d6af3a4da1d120bd4a27d7 (differs from the author's page hash with the same byte count; the page header says "DS1: Apr 24", i.e. the April 24, 2026 revision, unchanged).
- https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf : fetched 2026-10-25T11:04:18Z to 11:04:22Z, HTTP 200, 585821 bytes, sha256 9519a676ee381f02f032... (full hash 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc; identical to the author's table_record.md). pdftotext header: "revision #18: April 24, 2026".
- Table XIb (6.1.2) as extracted, row k=4: "55 89 117 152 193 242" with references "KrLR Ex17 Ex17 ExT 6.2.g ExT" for m = 4..9. So the cell R(3,4,7) (k=4, m=7) = 152, reference ExT. Value quoted: 152. Claimed 154 > 152.
- Consistency check of my column reading: R(3,4,8) >= 193 equals 4*R(4,7)-3 with R(4,7) >= 49 (Table Ia), as 6.2.g says.

## 2. Independent check of the object (own code, work/chk.py, standard library)
- shasum -a 256 of object/R_3_4_7.txt: e9fa8b95605e0f8e8d7b020855f7905ff9c02269c9d49a48abd725e7858d6a40 (matches CLAIM.md).
- Output: "distances covered 76 of 76 []"; "colour 1 omega 2 forbidden K3 OK"; "colour 2 omega 3 forbidden K4 OK"; "colour 3 omega 6 forbidden K7 OK" (exact max-clique search from vertex 0, valid by vertex-transitivity). So a 3-colouring of K_153 exists, R(3,4,7) >= 154. (Correctness is the other skeptics' job; this only supports that the thing compared is real.)

## 3. Literature, last 24 months
- arXiv API (one request, sorted by date, Ramsey AND three-colour/multicolor terms; 93 entries, 2024-11 .. 2026-10-12): no title or abstract mentions R(3,4,7). Closest: arXiv 2601.05221 (survey), 2509.03784 (SAT, R(K4,K4-e,K4-e)>=35, R(K3,K4,C4,C4)>=49), 2603.10851 (Boza, upper bounds R(3,4,5), R(3,3,6)), "An update on multicolor Ramsey lower bounds" (submitted 2026-01-21, asymptotic). None give a lower bound for R(3,4,7).
- arXiv all-fields query "R(3,4,7)": 0 entries.
- The four 2026 papers named in the target (2603.09172v5, 2608.18169v2, 2608.18769v1, 2610.12122v1): abstracts concern two-colour cells (R(4,20), R(6,8), R(8,10), circulant IP, etc.); none mentions three colours or (3,4,7).
- One WebSearch: only Exoo-Tatarevic (arXiv 1504.02403) found, "R(3,4,7) & 145 & 152 & splitting"; nothing newer.
- Exoo's page (http://cs.indstate.edu/ge/RAMSEY/, HTTP 200, one request): multicolour section lists only R(4,4,4,4) > 577 in the part read; no R(3,4,7).
- Limits: arXiv-metadata and one web search, not a full-text search of every paper; an unpublished record could exist.

## 4. This repo
- TROPHY_CASE.md (raw GitHub, HTTP 200, 31235 bytes, sha256 b946f68e...): no occurrence of "Ramsey" (grep exit empty).
- Open pull requests via GitHub API (pages 1 to 5, HTTP 200 each, 369 open PRs read in total, page 5 empty): Ramsey claims are #731 (R(3,3,11)>=183), #732 (R(3,3,12)>=203), #733 (R(3,3,14)>=267), #734 (R(3,5,7)>=252), #735 (R(3,3,9)>=133). None concerns R(3,4,7); no PR text contains "3,4,7".

## 5. Do published constructions or bounds for related cells already imply >= 154?
DS1 6.2 constructions applied to (3,4,7), best of each:
- 6.2.g: R(3,k,l) >= 4R(k,l-1)-3 gives 4*R(4,6)-3 with R(4,6) >= 36 = 141.
- 6.2.q/o product constructions: at most 2*(49-1)+1 = 97, other splits 66 to 108.
- 6.2.j Rowley cyclic recurrence with L(4,7) at most about 48 and L(3) = 2 gives about 143.
- Monotonicity: smaller cells R(3,4,6) >= 117, R(3,3,7) >= 85 are below; larger cells (R(3,4,8) >= 193) do not imply lower bounds for R(3,4,7).
- Nothing reaches 154, and the only published value for the cell is 152. The object itself is the Exoo-Tatarevic splitting of a Kuznetsov (7,7) circulant; Kuznetsov's v1 appeared after ExT (arXiv 1505 vs 1504), which is a plausible reason ExT did not get 154. The splitting method is published, but the existence of a valid split of this circulant is not implied by any bound; it is a computed fact (verified in section 2).

## Caveats
- The margin is +2, a genuine strict improvement, but a modest and derived one (published method on a published graph). The "partial win p1" wording needs "any newer arXiv paper for that multicolour cell": none found.
- The DS1 view page hash differs from the author's, but the PDF hash is identical and its revision date is April 24, 2026.

pass: true
