# Criterion skeptic: A316471(21) = 482706
context: subagent (criterion)
run: runs/2026-11-03-2000-locdisj ; claim copied to /workspace/panel-locdisj-criterion/claim ; live fetches in /workspace/panel-locdisj-criterion/live (fetchlog.txt)
checked: 2026-11-03T21:17Z (16:17 EST)

## Bank criterion match
- Criterion text in claim/CLAIM.md is byte-identical in content to repo/bank/targets.json id oeis-keyword-more-new-terms success_criterion (read directly). OK.

## Not excluded
- grep A316471 over repo/bank/ (targets.json + proposed/robust-forecast-aggregation-bounds.json): no hit. Not in the named exclusion list.
- Not a near-repdigit/repunit prime-index sequence (rooted-tree count), so the Kamada clause does not apply. OK.

## keyword more (live)
- https://oeis.org/search?q=id:A316471&fmt=text 21:17:29Z HTTP 200 sha256 b425e36d75f6f8f0... (identical to scout and preclaim): %K nonn,more; %I #6 Jul 05 2018.
- https://oeis.org/search?q=id:A316471+keyword:more 21:17:35Z HTTP 200: 1 hit, A316471. OK.

## n = 21 is the first missing index
- DATA (%S/%T) = a(1..20), offset 1, last 214490.
- b-file https://oeis.org/A316471/b316471.txt 21:17:31Z HTTP 200 sha256 da35dd33b0431ceb... (identical to preclaim): synthesized, 20 rows, last "20 214490". First absent index = 21. OK.

## Definition match
- Entry %N + %t Mathematica: strut[1]={{}}; strut[n] = sorted tuples over IntegerPartitions[n-1], kept iff UnsameQ (pairwise distinct branches) and every ordered pair of distinct branches has empty Intersection of their branch lists.
- Program B (Go) is a literal transcription: partitions x tuples, sorted canonical strings, UnsameQ + pairwise child-set intersection test. Matches.
- Program A (C): branches chosen as strictly increasing ids (= pairwise distinct, multiset-free), with a mark array forbidding any child id shared by two chosen branches (= pairwise empty intersection). Recursive by construction (only stored valid trees used as branches). Matches.
- Negative fixture (nodisj) in both gives 1,1,1,2,3,6,12,25,52,113,247,548,1226,2770,6299,14426 = A004111 (rooted identity trees), so the disjointness test is the active difference. OK.
- Two independent programs (C vs Go, id/bitmark backtracking vs literal tuple-filter, no shared code). I rebuilt both from the claim copy: outputs identical for n=1..21; rows 1..20 diff-equal to the live b-file; a(21)=482706 in both (live/pA_21.out, live/pB_21.out). OK.

## PREREG before attempts
- PREREG.md frozen 2026-11-03T20:01:18Z (mtime 15:01:18.17 EST). Earliest attempt artifact: attempts/exact-eval-first/code/progA.c mtime 15:01:52 EST; main.go 15:02:08; progC.py 15:02:44; all outputs later. PREREG thresholds (A and B reproduce DATA and agree; negative fixture -> A004111; value search no hit; preclaim re-fetch) are all met. OK. (mtime-based; no git history for the run folder.)

## Value novelty (criterion-level only)
- https://oeis.org/search?q=482706&fmt=text 21:17:33Z HTTP 200: "No results."
- https://oeis.org/search?q=214490,482706&fmt=text 21:17:34Z HTTP 200: "No results."
- Live entry page and history (21:17:28Z / 21:17:32Z HTTP 200): 0 occurrences of 482706; history top revision still #6 (Susanna Cuyler, Jul 05 2018) above #5..#1 by Gus Wiseman 2018; "proposed"/"editing" words only in those approved 2018 revisions, no pending draft. Text diff vs preclaim copies differs only in the footer timestamp/Cloudflare token. Entry comments/links/extensions contain no a(21). OK.
- Not done (outside this role): web/literature search for off-OEIS extensions (novelty skeptic's job).

confirmed_scope: A316471 (bank-eligible, keyword more, live 2026-11-03T21:17Z) has DATA/b-file ending at a(20)=214490, and two independent programs matching the entry's definition (C and Go, rebuilt by me) both reproduce a(1..20) and give a(21)=482706, a value absent from OEIS search, the entry and its history; by-products a(22..26) are not covered.
pass: true
