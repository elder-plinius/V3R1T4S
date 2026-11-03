# NOVELTY panel — runs/2026-11-03-2128-maxembed

context: subagent (novelty)

Claim under review: A214570(17) = 3360 (claim/CLAIM.md, claim/object/VALUE.txt).
Inputs read: claim/ and the NOVELTY line of panel_requests/2026-11-03-2128-maxembed.md only.
Own fetches, 2026-11-03T22:15:56Z–22:16:08Z (17:15–17:16 EST), all HTTP 200, saved in panel/novelty_fetch/ (sha256 in panel/novelty_fetch/SHA256SUMS).

## Checks

1. Entry (panel/novelty_fetch/A214570.txt, `search?q=id:A214570&fmt=text`): %I #29 May 28 2015; %S ends ...,840,1680 (a(16)); %K nonn,hard,more; %O 1,4. No %C/%H/%E/%Y text contains 3360 or any n=17 value. %E only "a(12)-a(16) from Alois P. Heinz, Sep 06 2012". sha256 01439a4f… identical to claim/table/preclaim_A214570_text.txt.
2. b-file (panel/novelty_fetch/b.txt): synthesized from entry, n = 1..16, last line `16 1680`. sha256 1990f878… identical to claim/table/preclaim_b214570.txt.
3. History (panel/novelty_fetch/hist.txt, `history?seq=A214570`): top revision #29 by Alois P. Heinz, May 28 2015, proposed→approved; no pending/editing draft newer than that; string 3360 absent. Diff vs claim/table/preclaim_history.html is only the site footer ("Last modified"/Cloudflare token).
4. Related A214569 (panel/novelty_fetch/A214569.txt): "Row n contains A214570(n) entries"; b-file "Rows n = 1..16, flattened"; keyword nonn,tabf,hard. Row 17 unpublished, so a(17) is not implicitly present. Same for A214571 (rows 1..16). A215703 (derivative array) and A206487 (c(t) by Matula number, DATA/b-file only to Matula 160, max value well below 1680) contain no 3360.
5. Value searches:
   - `3360`: 1069 hits (first page panel/novelty_fetch/vs3360.txt). Small, highly composite value; noisy, not dispositive. Neither A214570 nor A214569 appears on the fetched page.
   - `1680,3360`: 22 hits, all 3 pages read (vs2, vs2p2, vs2p3): multinomial/A-S partition triangles (A036038, A078760, A249619), Lah generalizations, divisor-record sequences, GL(4,2) class sizes, Hermite coefficients, etc. None is a count of plane embeddings / ordered trees per rooted tree, none is A214570/A214569/A214571. (A036038/A249619 hold multinomials, and c(t) = prod deg!/prod mult! is multinomial-like, but those entries are indexed by partitions, not this max-over-trees count; the bank wording "no hit holding it as this count" holds.)
   - `420,840,1680,3360` (the query that failed HTTP 000 in the claim run; re-run here OK): 4 hits — A085988, A361937, A363692, A378630; all unrelated (prime signatures / divisor records).
   - full prefix `1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680,3360`: No results.
   - `A214570 3360`: No results. `3360 tree` (27 hits, all read): no ordered-tree-isomorphism count.
6. Web (WebSearch, 2026): "A214570 ordered trees isomorphic rooted tree maximum 3360" and "\"A214570\" OEIS 2026" return only OEIS A214570/A214569/A214571 pages, all ending at n=16 / 1680. No paper, blog, or code listing a(17).
7. Repo (repo/, `git fetch` origin → 7712cc8): `git grep -w -e A214570 -e A214569 origin/main` and `rg -w` on the working tree: zero hits (TROPHY_CASE.md, known-knowns/, bank/targets.json, bank/proposed/). Earlier substring hits on "214570" are digit runs inside known-knowns certificate files, not A-numbers. Not in the bank exclusion list. GitHub issues/PR search (public API, repo:elder-plinius/V3R1T4S) for A214570, A214569, 214570: total_count 0 each. Only in-workspace mentions are this run's own REPORT.md/LOG.md lines.

## Judgment

The value 3360 at n = 17 is absent from the A214570 entry, its b-file, its edit history (no pending drafts), the companion triangles A214569/A214571 (rows 1..16), the 2-term/4-term/full-prefix value searches (no hit holds it as this count), the 2026 web, and the V3R1T4S repo/bank/PRs. The bare-value search (1069 hits) is disclosed noise, judged per bank wording. Novelty holds.

Caveat (not novelty): 3360 = 2·1680 continues the visible doubling pattern (840→1680→3360), so it is "guessable", but guessable is not published; correctness belongs to REPRODUCE/CRITERION.

pass: true
