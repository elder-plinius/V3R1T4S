# NOVELTY skeptic (retry): claim B, f(3,6) = 13

context: subagent (fresh context; read kit/RULES.md rule 3, kit/RUN.md steps 6-7, and claim/CLAIM.md, TARGET.md, TABLE_RECORD.md only)

Question: has f(3,6) = 13 (no S_6 set of 3 tournaments on 12 vertices), or a bound settling it, already been shown or
claimed publicly? All requests were plain, read-only, User-Agent "V3R1T4S-novelty-skeptic (read-only)". Nothing was posted.

## Source log

1. https://arxiv.org/abs/2604.08790, 2026-10-30T14:52:12Z, HTTP 200. Submission history lists **[v1] only**
   (Thu, 9 Apr 2026 21:58:15 UTC, 143 KB). No later version.
2. https://arxiv.org/pdf/2604.08790v1, 2026-10-30T14:52:12Z, HTTP 200 (393,509 bytes). Figure 7 ("Known upper bounds of
   f(m,k) for small values of m and k. Starred values show confirmed equality"), rows k, columns m: row k=6 reads
   `1163  26  13  10  9*`, so the (m,k)=(3,6) cell is **13, unstarred** (an upper bound only). Starred cells were "confirmed
   to be exact values ... using a SAT formulation ... discussed further in [8]". Section 4: "This work also provides no
   non-trivial lower bound for f(m,k)." The (3,6) cell is not marked known.
3. Jeffries' dissertation (ref [8]), Iowa State 2024, DOI 10.31274/td-20250502-307. Landing page
   https://dr.lib.iastate.edu/handle/20.500.12876/Ewpa01Ov, 2026-10-30T14:52:43Z, HTTP 200 (redirected to
   /entities/publication/33a1fdb3-...). Full PDF via the citation_pdf_url bitstream
   (/server/api/core/bitstreams/6f2ce53a-ab52-4d94-bbc7-bab801e54fd3/content), 2026-10-30T14:53:15Z, HTTP 200,
   application/pdf, 790,604 bytes; read as text. Figure 4.5 is the same table as Figure 7: f(3,6) = 13 and f(2,5) = 14,
   both **unstarred**. Section 4.3 gives a generic SAT formulation with no result for (3,6) or (2,5). Chapter 7 says the
   construction "is tight for small values, but it is likely that this bound can be improved". It contains no UNSAT result,
   lower bound or certificate for either cell. It settles neither f(3,6) nor f(2,5).
4. OpenAlex, 2026-10-30T14:52:35Z to 14:53:45Z, HTTP 200 (all queries). Paper W7154014129, cited_by_count 0;
   `filter=cites:W7154014129` returns 0 works. Dissertation W4410025275, cited_by_count 0; `filter=cites:` returns 0. The
   dissertation is flagged closed access by OpenAlex, but the repository PDF downloaded fine (item 3).
5. CrossRef bibliographic query, 2026-10-30T14:52:35Z, HTTP 200. It returns only the dissertation record (type
   dissertation) and unrelated items.
6. Google Scholar, query "Schuttes property for sets of tournaments", 2026-10-30T14:53:45Z, HTTP 200 (with the banner
   "The system can't perform the operation now", but it showed results). One result, the arXiv preprint, with
   "All 3 versions" and **no "Cited by" link**, so no citing works.
7. Semantic Scholar API, `paper/arXiv:2604.08790?fields=...citations`: 2026-10-30T14:53:44Z **HTTP 429**. A single retry
   after a pause of about 2 minutes (the server's message says "Please wait and try again"): 2026-10-30T14:56:07Z
   **HTTP 429**. Different routes: `paper/DOI:10.48550/arXiv.2604.08790/citations`, 14:56:24Z, HTTP 404 ("not found");
   `paper/search?query=...`, 14:56:32Z, **HTTP 429**. Web page www.semanticscholar.org/arxiv/2604.08790 via WebFetch:
   HTTP 404. **Not read.** I stopped there under kit/RULES.md rule 5 (no further retries, no browser to get past a block).
8. arXiv API (export.arxiv.org/api/query), 9 searches sorted by submission date, 2026-10-30T14:54:07Z to 14:54:59Z, all
   HTTP 200: "sets of tournaments"; Schutte AND tournament; Schütte AND tournaments; abs "multiple tournaments" AND
   dominat*; nontransitive AND dice; Jeffries AND tournament; paradoxical AND tournaments; abs "property S_k"; abs
   tournament AND "every k" AND dominat*. The only Schütte-type multiple-tournament paper is 2604.08790v1 itself. Later
   hits (2606.20744 Dice Bingo, 2609.* feedback vertex set, 2603.04174 k-majority Ramsey, which predates it) are
   unrelated. Nothing after April 2026 addresses f(m,k).
9. GitHub elder-plinius/V3R1T4S via gh, read-only. PR #816 at 2026-10-30T14:55:10Z: OPEN, draft, by DmitrL-dev, created
   and last updated 2026-10-29T00:58:29Z, one commit b37d9aed (2026-10-29T00:57:45Z), no comments. **No changes after
   2026-10-30T04:00Z.** It claims f(2,5) = 14 only. On f(3,6) it says explicitly: "Nothing about f(3,6). The same encoding
   for three tournaments on 12 vertices is UNSAT according to CaDiCaL (7089 s), but its LRAT proof exhausted cake_lpr's
   heap ... so there is no verified certificate yet", and "it is not claimed here". That is a public mention of an
   unverified solver answer for the (3,6, n=12) instance, disclaimed as a claim. PR #816's diff reaches f(3,6) only in
   that disclaimer, the bank text and the composition script "f(3,6) <= 13".
   All PRs (820, created 2026-10-14T01:52:59Z to 2026-10-30T14:33:53Z, fetched 14:55:35Z) and all issues (30, fetched
   14:55:40Z) were grepped in title, body and branch for f(3,6), Schütte/Schutte, tournament, 2604.08790, Jeffries, S_6.
   Hits: #816 (above), #694 (closed bank-entry PR; its body does not mention (3,6)), and #810, #628, #394, #362, #148,
   where "S_6" means permutation groups or BB(6), so they are unrelated. 5 PRs were created and 12 updated since
   2026-10-30T04:00Z, and none mentions the target. TROPHY_CASE.md at HEAD (gh api, 2026-10-30T14:55:51Z, 31,306 bytes)
   has no match for schutte, schütte, tournament, f(3, 2604.08790 or jeffries.
10. Web search (WebSearch tool), 2026-10-30 about 14:56Z: queries `"f(3,6)" Schütte tournaments "sets of tournaments" S_6`
    and `Schütte property multiple tournaments dominating k-set minimum order exact value SAT 2026`. The results are only
    the arXiv paper, the dissertation, an FAU talk abstract (www.math.fau.edu/combinatorics/abstracts/jeffries54.pdf,
    fetched 14:56:13Z, HTTP 200: an abstract only, no values), and unrelated single-tournament Schütte papers. No value or
    bound for f(3,6) beyond <= 13.

## Verdict

pass: false

Every source I could read says f(3,6) is open in the claimed sense. The arXiv paper (v1 only, no later version) and the
dissertation both list f(3,6) <= 13 unstarred with no lower bound. OpenAlex and Google Scholar show no citing works. arXiv
has no later Schütte multiple-tournament paper. TROPHY_CASE.md is silent, and the only repository mention (draft PR #816,
unchanged since 2026-10-29T00:58Z) explicitly disclaims f(3,6) and reports only an unverified CaDiCaL UNSAT for 12
vertices. That is not a prior proof or claim, but it is a public prior mention a submission should acknowledge. On the
substance, the claim would be new. The brief, however, requires every listed source to be read, and the Semantic Scholar
citation index (source 2) answered 429 on every API route, even after a pause; its web page gave 404. Under rule 5 I did
not push further, so the citation check is incomplete. A human can check Semantic Scholar's "cited by" for 2604.08790 by
hand. If it shows no citing work that settles the cell, this file's evidence supports flipping to pass: true.

One-line verdict: no public source settles f(3,6), and PR #816 disclaims it, but Semantic Scholar citations are unread (HTTP 429), so pass: false pending that check.
