context: codex exec (fresh context via codex-fresh)
novelty: PASS

The unchanged n19 object passes this NOVELTY review. Its 935,662 stable matchings strictly exceed the operative comparison of 896,068 by 39,594 (4.4186378712%). The accessible sources and repository search establish no equal or stronger applicable instance. This is an explicit-instance lower-bound record, not a determination of the maximum, a new general construction theorem, or approval of the other gates. A tie would fail.

All local filenames below are relative to claim/.

The primary status source was read successfully on one GET, with no retry or redirect. Canonical entry: https://oeis.org/A357271. Requested table: https://oeis.org/A357271/b357271.txt. The response quotes the exact row:

> 19 637336

Request began at 2026-10-15T17:42:05.016972+00:00; response completed at **2026-10-15T17:42:06.375762+00:00**, HTTP **200 OK**. The server Date header is Thu, 15 Oct 2026 17:42:06 GMT. SHA-256: `0d0e95042f30b2f8be60174047a5a03ea45bf70203d39e40b1665d0085b32b4a`. The source itself labels this “b-file synthesized from sequence entry”; that upstream wording is preserved. The body, headers, and complete receipt are `audit/data/primary_bfile.body`, `audit/data/primary_bfile.headers`, and `audit/data/primary_bfile.json`. Historical receipts in LITERATURE_ACCESS.md and data/fetches.json were not substituted for this request. The canonical entry was not separately re-requested.

The comparison remains the stronger supplied bar, not merely the public table:

| Comparison | Count | Assessment |
|---|---:|---|
| Submitted object.prefs, n19 | 935,662 | Exact recount agrees with the unchanged claim. |
| data/prior_n19.prefs | 896,068 | Operative bar; exact recount agrees. |
| Earlier X2 n19 reported in COMPARISON_SCOPE.md | 889,780 | Below the operative bar; this historical profile was not independently recovered. |
| OEIS A371810, nineteenth term | 650,736 | Conservatively considered; the entry expressly says it is likely incorrect. |
| Fresh A357271 b-file, n19 | 637,336 | Readable primary comparison. |
| Independent block products from the identified smaller instances | 586,416 | Largest product at total size 19: 195,472 × 3, from sizes 16 + 3. |

https://oeis.org/A371810 returned HTTP 200 at 2026-10-15T17:42:37.758786+00:00. Its qualification is explicit: “Subsequent verification by Dan Eilers in A069194 indicates that it is likely this sequence which is incorrect.” It is not silently promoted to a verified strict-profile record. Even considering its larger displayed term does not affect the verdict. Receipt: `audit/data/qualified_oeis.json`.

The literature window searched was **2024-10-15 through 2026-10-15**, with evidence limited to what was available at the recorded request times. Search records are preserved, not represented as exhaustive knowledge of every publication:

- arXiv API query `(all:"stable marriage" OR all:"stable matchings") AND submittedDate:[202410150000 TO 202610152359]`: both pages retrieved, 100 + 45 entries, matching totalResults = 145. Records were screened by title and abstract for counts, constructions, and applicability. Receipts: `audit/data/arxiv_search.json` and `audit/data/arxiv_search_p2.json`; extracted metadata: `audit/arxiv_screening.json`.
- Zenodo query `("stable marriage" OR "stable matchings") AND publication_date:[2024-10-15 TO 2026-10-15]`, **size=25**, page 1: HTTP 200, all 15 reported hits returned, no next-page link. All returned records were screened. There was no size=100 request. Receipt: `audit/data/zenodo_search_p1.json`.
- Crossref queries `maximum number stable matchings stable marriage` and title query `maximum number stable matchings`, each with publication dates restricted to the window: 100 ranked results each, 158 distinct DOI records in their union. These were ranked searches, not all-results enumeration. Relevant titles and available abstracts were screened; a missing abstract was not treated as read. Receipts: `audit/data/crossref_search.json` and `audit/data/crossref_titles.json`; metadata: `audit/crossref_screening.json`.

The material literature comparisons were resolved as follows:

| Work/source | Accessible evidence and relevance |
|---|---|
| Ong, Ang, Ho, Eilers, Marks and Buzi, Improved Hill Climbing for the Stable Marriage Problem, IFoRE 2024; published ranking dataset | https://oeis.org/A357271/a357271_1.txt returned HTTP 200 at 2026-10-15T17:42:30.582519+00:00. The authors' header dates the work 2024-11-01 and explicitly identifies the poster and all five new bounds: n7=81, n9=365, n11=1,690, n13=7,123, n15=27,059. The complete ranking matrices are supplied and were converted and recounted. No n19 result is asserted in this dataset. |
| Myunglae Jo, A computer-assisted proof that the maximum number of stable matchings of order seven is 85, 2026-10-13 | Author-deposited description in the accessible Zenodo response, record https://zenodo.org/records/23329599, identifies an actual-profile lower bound of 85. Its universal upper-bound/formalization qualifications were retained; no proof of f(7)=85 is assumed here. Including the 85 block in the comparison does not defeat n19. The manuscript and ZIP were not read. |
| Jo, Small Rotation Blocks and the Order-Six Stable Marriage Problem, 2026-09-23 | Author-deposited description, https://zenodo.org/records/22909380, concerns f(6)=48 and states that its Lean formalization is partial. It supplies no improved n19 bound; no universal optimality claim from it is required here. |
| Yoshiteru Ishida, Regular Anti-Phase Templates…, arXiv:2607.10306v1 | Primary HTML read: https://arxiv.org/html/2607.10306v1, HTTP 200 at 2026-10-15T17:42:35.344906+00:00. Corollary 5.10 gives exactly p stable matchings for this family at prime size p, hence 19 at n19. The family counting bound and small-group census do not assert a competing unrestricted n19 record. Section 6 gives independent composition. |
| Ishida, Prime factorisation of stable-matching instances…, arXiv:2610.05617v1 | Primary HTML read: https://arxiv.org/html/2610.05617v1, HTTP 200 at 2026-10-15T17:42:36.444781+00:00. Theorem 9/Table 3 count preference profiles: e.g. 109,986,835,968 input-prime profiles at n4. These are not stable matchings of one profile. The paper's direct-product statement supplies no larger n19 block. Zenodo's smprime code/data description concerns the same census and a complete n3 dataset. |
| Baturay Yilmaz and Esra Erdem, Generating Satisfiable Benchmark Instances for Stable Roommates Problems with Optimization, arXiv:2507.20013v1 | Primary HTML read: https://arxiv.org/html/2507.20013v1, HTTP 200 at 2026-10-15T17:45:24.474341+00:00. Table 1 reports roommate benchmarks with 20–100 total agents, including averages and a large approximate count at 100 agents. Section 6 explains an SMTI generator option, but gives no strict complete n19 profile with a competing count. Neither averages, ties, nor larger roommate instances are substituted for this claim's object. |

Other screened hits concerned matching cardinality, random/relaxed preferences, robustness under swaps, general choice functions, algorithms, or exposition; no additional explicit strict-complete n19 bound or construction yielding a competing count was identified. For example, Crossref's “Stable matchings under relaxed random preferences” studies expected epsilon-stable counts, and Zenodo's “The complexity of stability probability under compact indifference” counts preference refinements for a fixed matching, a different quantity.

The known-blocked https://www.jstor.org/stable/community.39515645 was **never requested**. Its poster was not read, and no unseen poster text is evidence. This does not leave a material gap for the cited numerical work: the authors' independently accessible original dataset expressly identifies the work, its claimed improved orders and all five counts, and gives the actual ranking matrices. All five reported counts were reproduced. Thus the accessible primary dataset adequately covers the relevant lower-bound claims without asserting knowledge of the poster's unobserved contents or methods.

Three supplementary discovery attempts supplied no usable comparison evidence: Google returned a 302 consent redirect, which was not followed; Bing returned HTTP 200 but unrelated Croatian health-directory results; OpenAlex returned HTTP 429 with no results and was not retried. Their complete responses remain in `audit/data/web_record_search.*`, `audit/data/bing_record_search.*`, and `audit/data/openalex_search.*`. None is called a successful literature search or used as negative evidence. The assessment instead rests on the completed arXiv/Zenodo searches, Crossref screening, and the accessible primary material resolving the concrete record/construction leads. No material cited-work coverage gap remains on that evidence; this is not a claim to have read all 145 arXiv papers or every Crossref hit in full.

Repository comparison used the supplied data/TROPHY_CASE.md and a fresh copy from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, HTTP 200 at 2026-10-15T17:42:31.514650+00:00. They are byte-identical (SHA-256 `b4f3ad52f6587e5aefdc3b555db200d99543e6b500c805012226f2042cdcc412`). Searching the trophy text found no stable-marriage record.

The live open-PR query https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 returned HTTP 200 at 2026-10-15T17:42:33.918577+00:00: **62 open PRs**, fewer than the page limit and no Link pagination header. All titles and bodies were searched. The relevant submissions are:

| PR | Claimed size/count |
|---|---|
| https://github.com/elder-plinius/V3R1T4S/pull/150 | n13: 7,698 |
| https://github.com/elder-plinius/V3R1T4S/pull/156 | n14: 24,992 |
| https://github.com/elder-plinius/V3R1T4S/pull/151 | n15: 30,362; supersedes the earlier 27,510 submission |
| https://github.com/elder-plinius/V3R1T4S/pull/147 | n18: 530,528 |
| https://github.com/elder-plinius/V3R1T4S/pull/157 | n22: 12,277,568 |
| https://github.com/elder-plinius/V3R1T4S/pull/174 | n28: 2,497,797,760 |
| https://github.com/elder-plinius/V3R1T4S/pull/153 | Target/bank proposal, not a further record |

Their discussion-comment endpoints were each read once and each returned HTTP 200 with an empty array, between 17:46:11 and 17:46:17 UTC. No n19 competitor appears in these submissions. The n22/n28 raw counts are larger but concern larger instances; their stated doubling constructions do not yield size 19. The available doubled n7/n9 results at n14/n18 are already included. Padding n18 preserves 530,528. Exhausting all independent block products from the identified n1–n18 values gives 586,416 at n19, below even the primary table; details and inputs are in `audit/comparisons.json`. This is an exact comparison within that construction, not a universal upper bound over unknown constructions.

For a numerical cross-check, the supplied arc_count.cpp was compiled once and run sequentially on the converted five published profiles, data/prior_n19.prefs and object.prefs. The counts were 81, 365, 1,690, 7,123, 27,059, 896,068 and 935,662, with complete enumeration and the same number of stable leaves. This uses the supplied counter, not a newly independent implementation. An initial parser for paired comments missed the n15 matrix-only section; reading the explicit rankWomen/rankMen matrices resolved that local parser issue without a network request. Results are in `audit/counts.json`. The object's SHA-256 remains `1e284a0dc1fe44f2d4693de19c1543ad99020937d7f8266bcc6cc7979ecc763e`.

The complete status-source rule was applied: **PENDING STATUS CHECK is not appropriate because the target primary table was read successfully.** A material literature gap would still fail; the blocked optional poster's numerical scope was instead covered by its authors' accessible, checkable dataset. The comparison bar and criterion were not weakened, and no tie was accepted.

Audit: `audit/data/receipts.json` consolidates URL, request/response UTC, HTTP status, headers, response size and SHA-256 for all 23 requests, including unsuccessful/unusable discovery responses. Individual `.body`, `.headers` and `.json` files preserve the responses. `audit/fetch.py` prohibits duplicate URLs and JSTOR requests. Integrity checks found exactly one primary request, zero duplicate URLs, zero JSTOR requests, matching saved-body hashes, and all 44 supplied manifest entries unchanged. Work was sequential without extra agents, used about 5.2 MB of audit disk, and finished within the 20-minute limit. The only write outside the permitted working folder is this verdict, ../../../../panel/novelty-retry.md.

pass: true
