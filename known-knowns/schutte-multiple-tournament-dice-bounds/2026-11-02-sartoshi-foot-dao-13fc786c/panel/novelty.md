# NOVELTY skeptic (final): claim B, f(3,6) = 13

context: subagent (fresh context; read kit/RULES.md rules 3, 5, 7, kit/RUN.md steps 6-7, claim/CLAIM.md, TARGET.md,
TABLE_RECORD.md, and the earlier novelty.md and novelty.retry.md as leads only)

Question: has f(3,6) = 13 (no S_6 set of 3 tournaments on 12 vertices, Jeffries arXiv:2604.08790 Def 2.1/2.2), or a bound
that settles the cell, already been shown or claimed in public? Every request was one plain read-only request, with
User-Agent "V3R1T4S-novelty-skeptic (read-only)" for curl and the default client for gh. Nothing was posted, commented,
filed or sent.

## Source log

1. arXiv abstract page https://arxiv.org/abs/2604.08790. Fetched 2026-11-02T06:23:37Z, HTTP 200, 38,790 bytes, sha256
   e613623af0d4312ac1282bb4031c201d62dc6c3ee16db06b5e1e37f3d0cf7863. The submission history lists **[v1] only**
   (Thu, 9 Apr 2026 21:58:15 UTC, 143 KB); the only "v2" strings on the page are inside an SVG logo path. There is no
   version after v1. The page hash differs from the one recorded on 2026-10-27 and 2026-10-30 (0b2c17af...) and so does
   the size. The version list is unchanged, so this is a change to the page template, not to the paper.
2. Figure 7 of the paper (v1), from the earlier retry's PDF read on 2026-10-30 (novelty.retry.md, source 2). There is no
   new version, so it still applies: the (m,k) = (3,6) cell is 13 and **unstarred** (an upper bound only), and Section 4
   says the paper gives "no non-trivial lower bound for f(m,k)". I did not fetch the PDF again today, because v1 is
   unchanged.
3. arXiv API, https://export.arxiv.org/api/query, 4 searches sorted newest first, 2026-11-02T06:23:46Z to 06:23:59Z, all
   HTTP 200. (An http:// request at 06:23:37Z returned a 301 redirect to https, and the https searches were run instead.)
   The queries were all:Schutte AND all:tournaments; abs:"sets of tournaments"; all:Jeffries AND all:tournament; and
   abs:tournaments AND abs:dice. The only paper on Schutte's property for several tournaments is 2604.08790v1. The newest
   hits (2609.16723, 2609.15220 feedback vertex sets; 2608.05455) are unrelated. Nothing submitted since 2026-10-30
   matches.
4. OpenAlex, 2026-11-02T06:24:11Z, HTTP 200. Work W7154014129 (DOI 10.48550/arxiv.2604.08790) has cited_by_count 0, and
   `works?filter=cites:W7154014129` returns meta.count 0.
5. Semantic Scholar: **human hand check**, done 2026-10-31 by the human owner, with the confirmation relayed
   2026-11-01. The page for arXiv 2604.08790 ("Schutte's property for sets of tournaments and an application to dice
   games", Jeffries) lists 15 references and **no citing papers**. This settles the HTTP 429 left open in
   novelty.retry.md, as rule 5 allows. I did not fetch Semantic Scholar myself.
6. GitHub elder-plinius/V3R1T4S, read-only gh queries:
   - PR #816, fetched 2026-11-02T06:24:23Z: OPEN, **draft**, by DmitrL-dev, created and last updated
     2026-10-29T00:58:29Z, one commit b37d9aed (2026-10-29T00:57:45Z), 0 comments, 0 reviews, 0 inline review comments.
     **Nothing has changed since 2026-10-30.** It claims f(2,5) = 14 only. Under "Not claimed" it says "Nothing about
     f(3,6)". It reports that the same encoding for 3 tournaments on 12 vertices came back UNSAT from CaDiCaL (7089 s),
     but that the LRAT proof exhausted cake_lpr's heap, so there is no verified certificate and no panel review.
   - All PRs, fetched 2026-11-02T06:24:24Z: 865 PRs, up to #896. I grepped title, body and branch for f(3,6), Schutte
     (all spellings), tournament, 2604.08790 and Jeffries. The hits were #816 and #694 (the closed bank-entry PR) only.
     54 PRs were created since 2026-10-30 (#842 to #896), and none of them matches. An extra grep for
     dominat / S_6 / k-subset matched only unrelated PRs ("not dominated" in the sorting-network PRs and similar).
   - All issues, fetched 2026-11-02T06:24:30Z: 31 issues, with no match.
   - TROPHY_CASE.md at HEAD, fetched 2026-11-02T06:24:31Z: 31,306 bytes, with no match for schutte/schütte, tournament,
     f(3, 2604.08790, jeffries or dice.
7. Web search (WebSearch tool, standard mode, about 2026-11-02T06:24Z). The query was "Schütte property sets of
   tournaments f(3,6) exact value 12 vertices S_6 three tournaments". The results:
   - the arXiv paper ([arxiv.org/pdf/2604.08790](https://arxiv.org/pdf/2604.08790));
   - the Jeffries dissertation ([dr.lib.iastate.edu](https://dr.lib.iastate.edu/entities/publication/33a1fdb3-3801-4087-ae1e-5b3dd4ac6c6c)),
     which the retry read in full on 2026-10-30: f(3,6) <= 13 unstarred, with no lower bound or certificate;
   - the FAU talk abstract ([math.fau.edu](https://www.math.fau.edu/combinatorics/abstracts/jeffries54.pdf));
   - older work on Schutte's problem for a single tournament, for example
     [Star-factors of tournaments](https://arxiv.org/pdf/math/9807021). Its "f(3)=6, f(4)=12" is a different function,
     not Jeffries' f(m,k).
   None gives a value or bound for f(3,6) beyond <= 13.

## Reasons

Every source that matters has now been read, either by me today or, for Semantic Scholar, by the human owner's hand
check under rule 5:
- The status source still lists v1 only, and its Figure 7 marks f(3,6) <= 13 as unstarred. The paper says it gives no
  non-trivial lower bound.
- The dissertation (ref [8]) has the same unstarred cell and no certificate.
- OpenAlex shows 0 citing works, and the hand check found none on Semantic Scholar.
- No arXiv paper on these sets of tournaments has appeared since April 2026.
- TROPHY_CASE.md and the repo's issues are silent.
- The only repo PR that touches the cell, draft PR #816 (unchanged since 2026-10-29), explicitly disclaims f(3,6).

So nothing public shows or claims that no S_6 triple exists on 12 vertices, and nothing settles the cell. A certified
exact value f(3,6) = 13 would strictly improve on what is known, which is an upper bound only. This judges novelty only;
whether the certificate itself is correct is the REPRODUCE and CRITERION skeptics' question.

A submission must acknowledge one thing. PR #816 (DmitrL-dev, opened 2026-10-29) publicly reports an **unverified**
CaDiCaL UNSAT result for the same instance (3 tournaments, 12 vertices, S_6). That PR disclaims the result and has no
checked certificate. It is a prior public mention of the same outcome by someone else, though not a prior claim or
proof. A submission should cite it, and should also note that priority could be contested if #816 later adds a verified
certificate.

pass: true
