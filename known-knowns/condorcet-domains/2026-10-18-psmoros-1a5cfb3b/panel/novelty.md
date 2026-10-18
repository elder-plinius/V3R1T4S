Saved by the main session from the subagent's returned text (NOVELTY skeptic, Agent tool, fresh context, model opus; returned about 03:53Z 2026-10-18). The skeptic's preface to the main session is omitted; the panel text below, after its "---" separator, is verbatim.

# NOVELTY skeptic: condorcet-domains, n = 21 (run folder 2026-10-18-0238)

context: subagent (Claude Code Agent tool, fresh context, model opus)
Review window: 2026-10-18T03:42:43Z to 2026-10-18T03:53Z. Run inputs read: claim/ only. Files hashed: claim/status/* and the human-provided copy of the hand check.

## 1. Status source situation

Status source: Table 4 ("Maximum size of Condorcet domains") of arXiv:2601.07336v1, https://arxiv.org/html/2601.07336 (abstract page https://arxiv.org/abs/2601.07336).

**My own fetch: none, on purpose.** arxiv.org has been stop-listed for this session since 2026-10-17T22:56:05Z. It answered 429 to a lens on https://arxiv.org/list/cs.GT/2026-02?skip=0&show=2000, and that line is in the session stop file. export.arxiv.org is also stop-listed, in an earlier stop file (503, 2026-10-16). A request to arxiv.org, or to any mirror of it, would break kit rule 5. I sent none.

**What was read, and how.**
1. **The run's scout fetch.** It was one honest GET, sent before the block.
   - https://arxiv.org/html/2601.07336 at 2026-10-17T22:25:36Z, HTTP 200, saved as claim/status/arxiv_html_2601.07336.html.
   - https://arxiv.org/abs/2601.07336 at 2026-10-17T22:25:20Z, HTTP 200, saved as claim/status/arxiv_abs_2601.07336.html.
   - I re-hashed both saved files. Their sha256 match CLAIM.md: 13e2470223a195ce47f4d8da36c05c6352ef1aecf062c21a75cf85b234c7bd1b and b763f9927bb848258da8d47876a5dc37752f7afabf47cfa55a3696d3082183fa.
   - The only version markers in the files are "2601.07336v1" (4 in the HTML, 5 in the abstract page).
   - In the HTML, Table 4 row n = 21 reads "≥ 6674931" with subscript ks. The number is set in ltx_font_bold, which the caption defines as the paper's own improved values.
   - Section 8 says: "For 21 ≤ n ≤ 25, the entries marked with subscript ks are obtained by applying the construction of [16] to the domains found for smaller n."
   - The abstract page's submission history shows only "[v1] Mon, 12 Jan 2026 09:03:12 UTC (26 KB)".
   - claim/status/records_table4.tsv (sha256 7ca09d5a…) matches the HTML table for n = 9..25.
2. **The human's hand check.** It is claim/status/human_status_check.md, sha256 26223b9f7f3b06fceb145c804f89aa7170eed98831947c0ba178734549883ef3.
   - It is byte-identical to the file in the workspace's human-provided folder (same sha256; file time 2026-10-18T00:59:14Z). That folder's README has sha256 548f98824db8618e828a6cda8b6a61bfa8aea3b86b1119470a8c03ccf455e096.
   - The check reports that https://arxiv.org/abs/2601.07336, opened in a browser at 2026-10-18T00:58Z, shows "only [v1] Mon, 12 Jan 2026 09:03:12 UTC (26 KB). No later version."
3. **Timing.** This is inferred from arXiv's public schedule, not from a fetch. arXiv announces new papers and replacements Sunday to Thursday at 20:00 US Eastern.
   - The scout fetch was at Sat 2026-10-17 18:25 EDT, the hand check at Sat 20:58 EDT, and this review at Sat 23:51 EDT.
   - All three fall between the Thu 2026-10-15 20:00 EDT announcement and the next one, Sun 2026-10-18 20:00 EDT (= 2026-10-19T00:00Z).
   - So no new version can have appeared since the hand check.

**Judgement: the status source has been read in an acceptable way.**
- The kit sends NOVELTY down the pending-status route "only when the status source cannot be read (no page, blocked, unreachable)". Here the primary table was read by one honest GET, with HTTP 200, before any block.
- The block left one question open: has a later version replaced v1? The human answered it by hand. The kit's pending route exists to get "the human checks by hand", and that has now happened.
- The settings say to check the human-provided folder "before marking a source PENDING". A matching file there therefore settles the source. I used it only as data, as its README requires. It was not treated as permission to retry, and nothing was sent to arxiv.org or any mirror.
- The earlier panel in this session marked the source pending before the hand check existed. That was right then. It no longer applies, because the source is no longer unread.
- **Remaining limit.** This skeptic did not fetch the page itself. The Table 4 cells come from the scout's hash-checked copy, and the hand check covers the version history, not the cells. arXiv versions do not change once posted, so v1's Table 4 is the source's current Table 4.

**Value used:** n = 21, best published lower bound 6674931 (ks). It comes from Table 4 of arXiv:2601.07336v1 (scout fetch 2026-10-17T22:25:36Z), and the human's hand check at 2026-10-18T00:58Z confirms it is current.

## 2. Sources checked (URL, time UTC, value)

| # | source | how / time | value found |
|---|---|---|---|
| 1 | Table 4 and abstract page of arXiv:2601.07336v1 | scout's saved copies, re-hashed 03:42Z | n = 21: ≥ 6674931 (ks, bold); v1 is the only version |
| 2 | the human's hand check (claim/status/human_status_check.md) | sha256 checked 03:42Z | abstract page shows v1 only at 00:58Z |
| 3 | TROPHY_CASE.md, https://github.com/elder-plinius/V3R1T4S (`gh api .../contents/TROPHY_CASE.md`) | 03:44:11Z; blob 571f2411…, 31235 bytes, sha256 b946f68e… | no row matching condorcet, linear order, majority, voting or domain |
| 4 | repo PRs, open and closed: `gh search prs` for condorcet, "Condorcet domain", "never condition", "linear orders", "majority rule", Q5, "social choice" | 03:44:20Z | 0 hits for every term |
| 5 | all repo PRs (`gh pr list --state all`, 363 PRs, #1-#372): titles and bodies matched against condorcet, linear orders, never.condition | 03:44Z | 0 matches. The 66 open PRs include none on Condorcet domains |
| 6 | repo code (`gh search code condorcet`) | 03:47:06Z | 0 results |
| 7 | WebSearch: largest / record Condorcet domain 2025-2026, n = 21, n = 22 | 03:43-03:52Z | newest record source is arXiv:2601.07336; nothing newer reports sizes |
| 8 | Karpov, Markström, Riis, Zhou, "Coherent domains and improved lower bounds for the maximum size of Condorcet domains", Discrete Applied Mathematics 370 (2025) 57-70 | WebSearch only (sciencedirect stopped; its arXiv copy stopped) | the "[16]" ks construction, more than 2.1973^n asymptotically; at n = 21 it is beaten by Table 4's bold 6674931 |
| 9 | "An efficient heuristic search algorithm for discovering large Condorcet domains", 4OR 2025, doi 10.1007/s10288-025-00583-1 | WebSearch | n = 10: 1082, n = 11: 2349; nothing for n = 21 |
| 10 | Zhou, Markström, "An orderly algorithm for generation of Condorcet Domains", arXiv:2509.20865 (Sep 2025) | WebSearch | enumeration of maximal domains for small n; no n = 21 sizes |
| 11 | Keehan, Slinko, "A composition of Condorcet domains", arXiv:2412.09852 (Dec 2024) | WebSearch | structure only (4 alternatives, nl-composition); no n = 21 sizes |
| 12 | "Coxeter Condorcet domains", arXiv:2606.01690 (Jun 2026) | WebSearch | structure only (Coxeter groups, root posets); no size records |
| 13 | Faliszewski et al., "Outer Diversity of Condorcet Domains", arXiv:2610.00720 (30 Sep 2026); code at https://github.com/Project-AGREE/Outer-Diversity-Condorcet | WebSearch; repo README via `gh api` at 03:47:06Z (101 bytes) | a diversity measure for few candidates; no size records |
| 14 | Puppe, Slinko, *Condorcet Domains* (Springer 2026), ch. 8 "Constructions of Large Condorcet Domains", https://link.springer.com/chapter/10.1007/978-3-032-15116-2_8 | one GET through the run's fetch helper, HTTP 200 at 2026-10-18T03:47:26Z, sha256 7e05ed61b5e938d92220ec5ff30903f33e9ed48023862237168640917919fbf8, 297111 bytes | first online 31 Dec 2025, before the status source. Abstract only (subscription). Its references cite the 2025 DAM paper, not arXiv:2601.07336. No size table visible |
| 15 | CDL library of the record paper's fourth author, https://github.com/sagebei/cdl (`gh api`) | 03:48:36Z; README sha256 b0e7a8bb… | commits after Jan 2026 are 2026-02-23 "Remove publications list from README", 2026-03-11 "upload the orderly algorithm" and 2026-06-09 logo/update. No record table and no large-n domain data |
| 16 | GitHub repo search "condorcet domain(s)" | 03:48:03Z | 3 repos (2022, 2024, 2026); none has n = 21 records |
| 17 | WebSearch for the exact numbers "6674931", "7467760", "15037178" | 03:47-03:50Z | no hits |
| 18 | WebSearch for Condorcet domains with AlphaEvolve, FunSearch or LLM search | 03:43Z | no Condorcet-domain result |

**Not checked (gaps).**
- arXiv listing pages for Feb-Oct 2026: arxiv.org is stopped, so only the search index was used. It does reach recent arXiv items, such as the Jun 2026 and 30 Sep 2026 papers.
- Full texts of the 2025 DAM paper and the 2026 book: paywalled, or on stopped hosts.
- Citation APIs (Semantic Scholar, OpenAlex, Crossref) and OEIS: all stopped.

## 3. Comparison

- **Claimed object:** 7467760 distinct linear orders on 21 alternatives. I re-hashed the joined xz (sha256 1a5cfb3b80fe8600bee47668e068a0fcf8923f87f895da9e23a1efe07f02b75d, matching CLAIM.md) and counted 7467760 lines. Checking that it is a valid Condorcet domain is the REPRODUCE skeptic's job; I did not repeat it.
- **Against the status source:** 7467760 vs 6674931 is +792829, or +11.877711 %. It is a strict improvement, not a tie.
- **Against everything else known:** I found no n = 21 value above 6674931 anywhere: literature after the status source, the repo's TROPHY_CASE.md, or its open and closed PRs.
- **Against what the published values give by construction.** Fishburn's replacement scheme gives f(a+b−1) ≥ f(a)·f(b). The best product for a + b − 1 = 21 from Table 4 is f(20)·f(2) = 3155366·2 = 6310732. That is below 6674931, which is below 7467760. So the claim does not follow from multiplying published table values. The ks construction is what produced 6674931.
- **No conflict with the source.** 7467760 is below the paper's comparison column ⌈4/5^1.5·√5^n⌉ = 7812500 at n = 21. In the text I read, that column is not stated as a bound. Nothing in the status source rules out the claimed size.
- **Earlier object in this session.** The main session reports an earlier, smaller n = 21 object from this session. It is this run's own work, not a published value, so it is not a competitor.

## 4. Rules

- No request went to arxiv.org or any arXiv mirror, nor to any host in any stop file. I checked the stop files changed in the last 24 h before the one fetch.
- The one web fetch was to link.springer.com through the run's fetch helper. It got HTTP 200, with no challenge page.
- No new block was hit, so nothing was appended to the stop file.
- The human-provided file was used only as data.
- injection_suspected: none (I scanned the fetched page, both READMEs, TROPHY_CASE.md and the hand check).

## Verdict

novelty: status source read. Table 4 of v1 comes from the scout's honest HTTP 200 copy, and the human's hand check confirms v1 is still the only version, with no arXiv announcement since. 7467760 is strictly larger than 6674931 (+11.88 %). No larger n = 21 value was found in the last 24 months of literature, in TROPHY_CASE.md, or in the repo's open and closed PRs.
pass: true
