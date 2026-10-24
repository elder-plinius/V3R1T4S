context: codex exec (fresh context via codex-fresh)

NOVELTY: pass for the inherited n=23 explicit-instance claim, as checked on 2026-10-15. The claimed 19,305,568 stable matchings strictly exceed the strongest identified same-size predecessor, 19,290,640, by 14,928 (about 0.077385%). No equal or larger n=23 result was found in the searches below. This assessment concerns an instance lower bound; it establishes no maximum.

I read the historical criterion literally in CLAIM.md and search/PREREG.md. Order 23 is eligible under its n >= 17 clause. The historical requirement is random-start calibration to 85 at n=7; I did not substitute a later criterion or require a proof of n=7 optimality. COMPARISON_SCOPE.md includes the unpanelled 19,290,640 predecessor in data/prior_n23.prefs, so the weaker public table is not the sole comparison. All 51 files listed in MANIFEST.json match their supplied hashes. The supplied historical receipts and object were left unchanged. The numerical claim and predecessor count here are those supplied by the package; I did not rerun the exact enumerators in this novelty review.

The primary table was fetched once by an ordinary HTTP GET, without browser impersonation, redirects, retries, or challenge handling:

| URL | Exact returned value | HTTP | Receipt time, UTC |
|---|---|---|---|
| https://oeis.org/A357271/b357271.txt | `23 15481956` | 200 | 2026-10-15T18:53:25.006174+00:00 |

The body labels itself `# A357271 (b-file synthesized from sequence entry)`. Its SHA-256 is `0d0e95042f30b2f8be60174047a5a03ea45bf70203d39e40b1665d0085b32b4a`, identical to the supplied table snapshot. Exact response bytes and headers are in novelty_audit/primary.body and novelty_audit/primary.receipt.json. Two local launcher failures from unsupported macOS resource-limit setters occurred before any network code; neither issued a request. The subsequent invocation made the sole primary request. No fetched endpoint was blocked or retried.

Repository checks:

- Searched the supplied data/TROPHY_CASE.md and the current https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, HTTP 200 at 2026-10-15T18:53:39.972769+00:00. Neither contains a stable-marriage result. The current file differs from the supplied snapshot; the current bytes are retained in novelty_audit/trophy.body.
- Fetched https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100, HTTP 200 at 2026-10-15T18:53:41.725321+00:00. It returned all nine open PRs, with no next-page link. I screened all titles and bodies. Relevant claims are #190 (n=13, 9,836), #191 (n=19, 935,662), and #194 (n=21, 5,400,616), plus bank proposal #153. None claims n=23. See novelty_audit/prs.body and its receipt.
- Also screened the supplied 59-PR snapshot in data/prs.json and both pages of current closed PRs (183 records, completed 18:55:47 UTC). This preserves comparisons with closed or merged claims, including n=14 at 24,992, n=18 at 530,528, n=22 at 12,277,568, and n=28 at 2,497,797,760. No n=23 tie or superior claim appeared. See novelty_audit/closed_prs.body and novelty_audit/closed_prs_p2.body.

Literature search window: 2024-10-15 through 2026-10-15. All searches used ordinary GET requests, with exact query URLs, times, headers, and response hashes retained in the corresponding novelty_audit/*.receipt.json files.

- arXiv: searched `(all:"stable marriage" OR all:"stable matchings") AND submittedDate:[202410150000 TO 202610152359]` through https://export.arxiv.org/api/query. Both result pages were fetched successfully, covering all 145 returned entries. I screened titles and relevant abstracts. Receipts: novelty_audit/arxiv_search.receipt.json and novelty_audit/arxiv_search_p2.receipt.json, completed at 18:53:43 and 18:54:03 UTC.
- Zenodo: searched `("stable marriage" OR "stable matchings") AND publication_date:[2024-10-15 TO 2026-10-15]` through https://zenodo.org/api/records, using size=25. All 15 returned records fit on one page. Receipt: novelty_audit/zenodo_search.receipt.json, HTTP 200 at 18:54:05 UTC.
- Crossref: searched `maximum number of stable matchings`, restricted to publication dates in that window, through https://api.crossref.org/works. Screened the first 100 relevance-ranked records; this is a bounded supplementary search, not all 86,357 broad keyword hits. Receipt: novelty_audit/crossref_search.receipt.json, HTTP 200 at 18:54:07 UTC.

The relevant recent evidence does not subsume this cell:

- Ong, Ang, Ho, Eilers, Marks, and Buzi, *Improved Hill Climbing for the Stable Marriage Problem* (IFoRE, 2024-11-01): the authors' ranking matrices at https://oeis.org/A357271/a357271_1.txt were fetched with HTTP 200 at 2026-10-15T18:54:45.043351+00:00. They state n=7,9,11,13,15 counts of 81,365,1690,7123,27059. The response matches data/instances.txt byte for byte. The previously challenged JSTOR poster endpoint disclosed in ACCESS_RECORD.md was not requested, and no unseen poster content was inferred.
- Myunglae Jo, https://doi.org/10.5281/zenodo.23329599 (2026-10-13): the public record states an order-seven 85-instance and describes a claimed upper bound with explicit formalization limitations. It provides no n=23 record. The order-six work at https://doi.org/10.5281/zenodo.22909380 concerns 48 stable matchings at n=6.
- Yoshiteru Ishida, https://arxiv.org/html/2607.10306v1, *Regular anti-phase templates...* (2026): full text fetched with HTTP 200 at 18:54:42 UTC. Corollary 5.10 says every prime-order template in that family has exactly p stable matchings. At p=23 this is 23, not an improved n=23 record. Its general subgroup-index lower bound is not a universal upper bound or an n=23 construction exceeding this claim.
- Ishida, https://arxiv.org/html/2610.05617v1, *Prime factorisation of stable-matching instances...* (2026): full text fetched with HTTP 200 at 18:54:43 UTC. The large census numbers count preference profiles, not stable matchings of one profile. The products theorem multiplies stable-set sizes across independent blocks; it supplies no stronger n=23 instance.
- Other screened count-related results concerned roommates, relaxed stability or switching costs, general choice functions, or algorithmic enumeration. None supplied a competing count for one complete, strict, balanced n=23 instance.

I also checked the direct-sum consequence of known blocks rather than comparing isolated table rows only. An integer dynamic program over every partition of 23, using the public terms, the improved published odd-order blocks, the saved local bars in search/PREREG.md, and the newer PR values above, gives the best proper direct sum as 195,472 x 85 = 16,615,120, using sizes 16+7. This incorporates the reported doubled blocks at sizes 14, 18, and 22 through comparison values at least as large as those constructions. It remains below 19,290,640. Inputs and result are in novelty_audit/comparison.json. This is a complete partition check for those comparison blocks, not an exhaustive search over possible constructions or profiles.

The strongest identified n=23 baseline remains data/prior_n23.prefs at 19,290,640. The claimed count is strictly higher, not tied. The primary fetch succeeded, current repository comparisons were checked, and the last 24 months of accessible literature disclosed no equal or stronger applicable result. The novelty gate passes on that evidence. No other local session or run folder was consulted, no messages or repository changes were sent outward, and no search or enumeration workload was launched.

pass: true
