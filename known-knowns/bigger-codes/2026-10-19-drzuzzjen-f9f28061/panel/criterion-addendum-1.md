# CRITERION addendum 1 — independent reading of original source bytes
context: same fresh CRITERION subagent continuing its own review; no current reviewer verdicts or checker code read
reviewed_utc: 2026-10-19T11:31:03.183195+00:00
original_criterion_sha256: 119afb1107f4ed5b3dd72774a65f02fc553220bf247d9d9dcba6b6b278e876cd
mathematical_validity: PASS (original exact certificate unchanged)
comparison_status: TABLE AND DIRECT-CELL COMPARISONS PASS; FULL NON-SUBSUMPTION INCOMPLETE
bank_literal_success: PENDING
confirmed_scope: CANDIDATE_M8734.txt (SHA256 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde) contains8734 distinct binary words of length25 and weight11 with pairwise distance at least6; its size exceeds Brouwer's printed lower bound8718 by16 and the direct same-cell open PR437 claim8720 by14, while remaining below the printed upper bound24630, for the source snapshots recorded below.

This addendum preserves criterion.md and the original manifest unchanged. No HTTP request was made here, no model was added, and no publication action was taken. Every supplied body1..20 was independently hashed and byte-count checked against access-ledger.json. Source metadata are saved separately from my decisions. The original proof and checker result remain valid.

## Literal comparison decisions

KNOWN FROM SOURCE1: Brouwer table headed Bounds on A(n,6,w), row25, column11 reads8718Pl-24630. The row's columns end at weight12; there is no independently printed row25,column14 cell. This was checked structurally against the raw table header, not inferred from someone else's report. Complementation is a bijection from weight11 to weight14 and preserves pairwise distance, so A(25,6,11)=A(25,6,14); the mirror is the same mathematical cell. No separate larger mirror value was present in the provided page. Therefore8734>8718 and8734<=24630. Margin to upper=15896. This establishes a table improvement as of the source1 fetch, not optimality.

KNOWN FROM SOURCE11: upstream bigger-codes INDEX row A(25,6,11) hasM8718 and archive credit Jordan Boisclair8698 followed by exact LNS polish. I do not use the index's older comparison columns as current table values; source1 supplies the current comparison.

KNOWN FROM SOURCES2..7: six GitHub API all-state pages contain100,100,100,100,100,54 records,554 distinct PR numbers. Pagination headers identify page6 as last. I searched titles/bodies for the literal cell, complement, compact code filenames and target sizes. The only direct A(25,6,11)/A(25,6,14) claim found is open PR437, titled A(25,6,11)>=8720, updated2026-10-18T18:13:23Z. Its claimedM8720 is below8734 by14. This is evidence of a competing public claim, not evidence that its object/panel is valid. Claims in its body that a panel passed were ignored. No same/equal-or-better direct cell claim appeared in these554 title/body records. Issue discussions, PR comments and arbitrary hidden file content were not returned by this API inventory.

KNOWN FROM SOURCE8: recursive upstream tree reports truncated:false and5166 entries; its bigger-codes paths include the8718 object and no direct A25_6_11 higher object filename. Paths alone do not expose all arbitrary filename contents. Current family INDEX plus full all-state PR inventory support the direct-cell comparison; a current TROPHY_CASE body itself is not among these20 supplied receipts.

KNOWN FROM SOURCE12: independent table parser extracts all124 claimed construction rows in Echols Table1. Its two n25 entries are(25,10,12, prior137,new141) and(25,8,11,prior1702,new1722). It has no(25,6,11) or(25,6,14) row. I read the full extracted prose and table, not only the abstract. The abstract/history source9 showsv1 as the available listed version. This source does not directly subsumeM8734.

KNOWN FROM SOURCE13: Lysenstoen's full HTML reports improvements at(23,6,10),(24,6,10),(23,6,11),(24,6,8), and discusses lost weight8 chains, not a25,6,11 or25,6,14 certificate. All explicit A(n,d,w) numeric mentions were extracted; neither target nor mirror occurs. Source10's history listsv1. This checks the required named paper directly; absence of the cell is not a claim that every possible mathematical propagation from the paper has been exhausted.

## Later and ancillary sources: exact remaining limits

Source14 (Rosin2603.00174) is an abstract claiming24 improved cells with18<=n<=35,6<=d<=18; the24 parameter values are not enumerated in that abstract. It cannot independently exclude a target-cell bound from the full paper.

Source15 (Chee,Xing,Yeo1008.1610) is an abstract for propagation rules. It gives no explicit rule or result values, so it cannot certify a complete propagation audit.

Source16 (Yang et al.2609.35051) is an abstract for kissing-number constructions, with several kissing numbers but no finite A(25,6,11) listing. The49-page body and13 tables were not among the supplied sources. Reading the abstract cannot rule out a relevant embedded constant-weight code in the body or construction data.

Source17 (Chee2610.10973) states an asymptotic invariant packing theorem, with no quantitative finite A(25,6,11) bound in the abstract. Its full16-page paper is not present. Source18 (Ota,Osa,Harada2610.11609) states general binary codes(22,84,9),(24,196,9),(25,65,11), which are not a new8734-word constant-weight code; their listed finite objects cannot directly subsume this candidate by taking subsets. Again these are abstract-level observations, not an exhaustive body audit.

There is no raw recent-search-results receipt in the20 supplied HTTP sources establishing coverage through this review on19Oct. The parent explicitly identifies a gap in the search after17Oct; I preserve that as a reported gap, not as a verified search cutoff. I cannot fill it by omitting its mention or by accepting another reviewer's conclusion. No new request was made.

Source19 is the actual published neighbor A(26,6,12)14854-word hexadecimal listing, SHA cde1edf846a27f1eb3d65aab7df65f0759ff0707b00b309b3b025fd2037b0e97. My independent parse confirms14854 distinct26-bit weight12 words. Counting all26 one-coordinate one-slices gives maximum6868, strictly below8734 by1866; deleting that coordinate yields25-bit weight11 words. This rules out direct one-coordinate shortening of this exact source list, including coordinate permutations and complementary weight14 versions, as a subsuming certificate. It does not certify every construction or code of those parameters, or validate the neighbor's pairwise distance. Raw slice counts and process resources are in neighbor19_independent_slice_counts.json.

Source20 is an HTTP403 Forbidden body for https://aeb.win.tue.nl/codes/cwc/d6/a27.6.11.19344H, fetched2026-10-19T11:28:21.353363+00:00. The precise state of that unavailable source is PENDING TABLE CHECK. This does not invalidate the successful source1 table fetch. Its coordinate-slice distribution cannot be computed from the403 body; therefore a potential two-coordinate shortening comparison for this particular neighbor remains unavailable here. No retry, URL alternative or bypass was attempted. An average shortening size would not bound the maximum slice and cannot replace the missing object.

## Decision

The explicit local object passes. The successful source1 table comparison, mirror check, upper bound check, named full-paper checks and direct same-cell contributions support the stated limited comparison. Full bank success and genuine non-subsumed novelty remain incomplete because the later-paper body/search coverage and the blocked neighbor comparison have not been resolved in the supplied evidence. This is not a finding that a larger code exists, and is not a CONFIRMED gate. Packaging still requires the complete independent panel and actual current workspace/package CHECK_RUN receipts; none is awarded by this addendum.

## Verified raw receipt hashes

|Source|HTTP|UTC response|SHA256|
|---|---|---|---|
|1|200|2026-10-19T11:22:35.492936+00:00|13c8fdd428059d82986d63cdba9beeaf5a436464c7ec18ced8b17bf0ec6c0851|
|2|200|2026-10-19T11:22:48.962759+00:00|c2eae7b435e96673fbf78e7db5853e67e768a4655b8fb8fb1105fdc23d3dcf84|
|3|200|2026-10-19T11:22:59.310259+00:00|4b86c7b49d912f052f2cabdac6aadc7380f0d2e8b5d347650abe6ab77c6cb6a5|
|4|200|2026-10-19T11:23:00.452253+00:00|fbafff7175cc9bc9fb85091f9eb84d3b019ee29d91246d3ae06a1635d4b874ec|
|5|200|2026-10-19T11:23:01.558676+00:00|2f519f0ae18f68c5a0569eee4b95e7f754bf2c2995f0639f41da9e9a21015d62|
|6|200|2026-10-19T11:23:02.675551+00:00|bf454d11f745d5696c2edc53ecb8bf1cc940b9978449013ec3a9a6e1a30a666e|
|7|200|2026-10-19T11:23:03.633987+00:00|6aa1f9a35c5b924fda1daf14567723fda817ba64ba8319fac9e00a2ef7b189fc|
|8|200|2026-10-19T11:23:22.263065+00:00|74e28ac7f4827deaff1fef045da5fde5635ea2bb04a067f333e44c4d186375b8|
|9|200|2026-10-19T11:23:22.806006+00:00|cc9f1406799ec21ab93ca205599958f354524ca478d2a87e1d38921088027dd9|
|10|200|2026-10-19T11:23:23.025829+00:00|6aa83d5b31b4443688dc57e54e000d5272f744fd918b6b115f6636d5291344f1|
|11|200|2026-10-19T11:23:45.219938+00:00|e7ed745ea3299877231732acb040b97d5e7953c04ef7a76f228856d3b92e2ff7|
|12|200|2026-10-19T11:23:45.426316+00:00|57b3e5fd6679385eb244a7a1171631204b0aa48cc61c68a37d6421ec2fe742a4|
|13|200|2026-10-19T11:23:45.597830+00:00|138e693dab62b9ce51829de318209faa0986ba167778ebbe5d2b9aa259cd190c|
|14|200|2026-10-19T11:26:52.578928+00:00|1e66da3a946247d00e3cd33497d108c47014108ab4ab0e44b475824eef4203d6|
|15|200|2026-10-19T11:26:53.494611+00:00|3d26bb4254b72942f9a57d04af95ac732f06a9a97711bf488cb10a4db96ff0d0|
|16|200|2026-10-19T11:27:47.026671+00:00|d4458556ab8b83608bcea941a33a7b410f6054550dfe61adc0b423102cb5832c|
|17|200|2026-10-19T11:27:47.236854+00:00|0d45a4971e5c9cf1daa01c29174802690bdc523316416020529184f3e2229f0e|
|18|200|2026-10-19T11:27:47.462767+00:00|4e6fefc1ca07acdf9ebf90d9e501d2f17f9d3847b524a6ab1ce7908c7c15ca23|
|19|200|2026-10-19T11:28:20.822706+00:00|cde1edf846a27f1eb3d65aab7df65f0759ff0707b00b309b3b025fd2037b0e97|
|20|403|2026-10-19T11:28:21.353363+00:00|57559551c35735c4acd1ede5a7d3df31a3f9b55acc087fdbb0811813b13d63d3|

pass: false
