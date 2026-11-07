# NOVELTY review

context: fresh independent subagent given the claim packet and operational rules; independent source access and a frozen source-check plan
reviewed_utc: 2026-11-04T02:35:01.572189+00:00
claim_level: KNOWN source comparisons; novelty assessment is limited to the dated public search below
object: object/assignment.txt
object_sha256: d12cb8aee658a8e3657c8607ba722531604366ba65a97f8fd357aea7d482131e
criterion_sha256: d057d8759f6ae9daa90bdbabb2fbbc6d8f89c67a9f1b3ce9da0254b6ff936690

The claimed n=25 count 186310276 strictly exceeds every same-n value found in this dated source review. This review judges novelty only; the count and Condorcet property require the separate mathematical reviews.

## Latest paper and Table 4

One plain request to [the primary abstract page](https://arxiv.org/abs/2601.07336) completed at 2026-11-04T02:28:56.911613+00:00 with HTTP200. It listed only v1, but Age385746 exceeded its max-age3600. Neither the fresh Date nor the requested no-cache headers establishes that this response was revalidated; I do not use that response alone to determine latest version.

The separately preplanned [official metadata-only query](https://export.arxiv.org/api/query?id_list=2601.07336) completed at 2026-11-04T02:29:33.436710+00:00 with HTTP200, Age0 and X-Cache MISS,MISS,MISS. Its entry identifies arXiv:2601.07336v1, submitted/updated 2026-01-12T09:03:12Z. The [official API manual, section5.1.1](https://info.arxiv.org/help/api/user-manual.html#511-a-note-on-article-versions) specifies that an unversioned id_list retrieves the latest version. These observations support v1 as the latest version at this dated check. The API's feed timestamp is recorded as metadata, not used as proof of origin freshness; the transport Age/cache evidence and documented query semantics supply the corroboration. This does not claim an instantaneous origin guarantee.

One request to [the fixed v1 HTML](https://arxiv.org/html/2601.07336v1) completed at 2026-11-04T02:30:05.952223+00:00 with HTTP200. Table4's n25 f(n)&h(n) lower-bound cell is **160316046**, marked ks. Its separate formula column is195312500 and is not a constructed-domain lower-bound cell. The versioned response was cached (Age1050848); it supplies fixed v1 content, while the independent metadata query supplies the latest-version determination. Authors: Alexander Karpov, Klas Markström, Søren Riis and Bei Zhou.

The gain over that lower bound is25994230. The raw abstract, metadata and version-specific table bodies have SHA256 c1106cdaf31d9faf04e46b9a4ae3f0dca421eab95b4e57cabaff58794cf2f32d, 72bfe80d3374c180f74482a80b48c9746b3ea786c9af567930e56b0a11992178 and a018d41785d2594aca2ffb57a28eb3e596acda1469395452e565aa4c268fb93a respectively. All three requests used the normal curl identity, no cookies, redirects, retry or cache-buster; none returned a denial or challenge. Exact argv, raw headers, hashes and process wait receipts remain in novelty-data/.

## Public and local comparisons

Connected GitHub reads checked [PR762](https://github.com/elder-plinius/V3R1T4S/pull/762), [PR389](https://github.com/elder-plinius/V3R1T4S/pull/389) and [PR388](https://github.com/elder-plinius/V3R1T4S/pull/388). All are open and unmerged in the returned metadata. PR762 claims180870896 for n25; the new claim exceeds it by5439380. PR389 claims178950728 for n25; the difference is7359548. These are public unmerged claims, not published record-table values. PR388's n24 claim81912986 is a source dependency and is credited to psmoros; its returned head isabc5220fd79f75651d5faadb71df365566201121. Its smaller alternative count is not a same-n comparison.

An all-state upstream PR search for Condorcet returned13 results with incomplete_results:false; the same-n claims were389 and762. Exact searches for186310276 and186216544 returned zero results, also without truncation. The live [TROPHY_CASE.md](https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md), blob18b731d7d4bf99efd323d48740284daccb8501b0, had no Condorcet text entry. The requested upstream known-knowns/condorcet-domains directory returned404, and its parent listing had no such directory. The pinned local trophy likewise had no Condorcet entry and its corresponding known-knowns directory was absent. The claim packet's prior local threshold186216544 is surpassed by93732; its older object was not supplied to this review, so I treat that number as a comparison threshold, not an independently recounted result.

## Literature coverage and limits

The bounded search covered2024-11-04 through2026-11-04 with15 web queries, including arXiv, Zenodo, GitHub, MathOverflow and Russian-language terms. Search-index results are discovery evidence; relevant primary records were opened. No larger n25 construction was found within that coverage.

Opened recent primary sources included [Zhou and Markström's orderly generation paper](https://arxiv.org/html/2509.20865v1), whose computational section treats8-10 alternatives; [Gao and Peng's Coxeter framework](https://arxiv.org/html/2606.01690v1), including its maximum-size discussion; and [Faliszewski and coauthors' outer-diversity paper](https://arxiv.org/html/2610.00720v1), including its largest-domain discussion. These inspected sections supplied no competing n25 numerical construction. [The institutional2025 coherent-domain publication record](https://www.ipu.ru/node/80126) and [the authors' seven-alternative archive](https://webspace.eecs.qmul.ac.uk/s.riis/condorcet-data.html) were also checked.

The newer [Karpov dissertation record](https://www.hse.ru/sci/diss/1124596639) lists defense on2026-09-23 and PDF posting on2026-05-04. In the linked PDF, the relevant tables inspected were2.1 (through n8),2.3 (through n20, largest listed value2917604), and2.4 (through n20). No larger n25 entry was found in these tables or the scoped text search. This is not a claim to have independently reviewed every theorem in the248-page thesis. The [Puppe-Slinko author-hosted draft](https://micro.econ.kit.edu/downloads/CondorcetDomains_Buch_Puppe_Slinko.pdf), dated2025-11-14, has a through-n20 construction table and discusses growth-rate bounds; it supplied no larger n25 cell in the inspected sections. Search-only unrelated or duplicate hits were not used as numerical comparators. Forum/Zenodo searches produced no relevant competing record in the returned results.

A dated bounded search cannot exclude unpublished, unindexed or subsequently posted work. The conclusion is a strict improvement over the latest identified paper's n25 construction cell and all additional same-n values found in the required current-source checks. It asserts no optimality, upper bound, other n, new construction method or universal literature completeness.

Factual source packet: novelty-source.json. Raw source bodies, HTTP/connector receipts, extraction/parser code and search logs are retained locally in novelty-data/ and are **unshipped** if omitted from the public package; the reader must not expect those files inside that package.

pass: true
