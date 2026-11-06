# Criterion skeptic -- runs/2026-11-03-2004-ldsemi
context: subagent (criterion)
Inputs: copy of claim/ at /workspace/panel-ldsemi-criterion/claim; fresh fetches 2026-11-03T21:19:25Z..21:19:32Z (16:19 EST), log + files in panel/criterion_fetch/ (FETCHLOG.txt with HTTP code + sha256).

Claim: A331783(21) = 10950456. Target oeis-keyword-more-new-terms; criterion text in target.md / claim/CLAIM.md checked verbatim against repo/bank/targets.json (identical).

## Checks against the success criterion
1. Bank criterion match: CLAIM.md/target.md criterion string == bank/targets.json "success_criterion" for id oeis-keyword-more-new-terms. PASS.
2. Not excluded: "331783" appears nowhere in repo/bank/targets.json or repo/bank/proposed/* (grep); not in the named exclusion list; not a near-repdigit/repunit prime-index sequence (tree count). Only other run touching it is the sibling 2000-locdisj (A316471, different cell). PASS.
3. keyword more, live: entry text (search id:A331783, fmt=text, HTTP 200, sha256 b9aa4fc4..., identical to pre-claim) shows %K nonn,more, %I #6 Feb 02 2020; keyword:more+id:A331783 search returns 1 of 1. PASS.
4. n = 21 first missing: %O 1,3; %S/%T has 20 terms ending 4242226 (= a(20)); live b-file (sha256 bd1ee969..., unchanged, "synthesized from sequence entry") has 20 lines, last "20 4242226". So 21 is the first absent index (no offset slip). PASS.
5. Not in comments/links/extensions/history: no %H, %E, or %F lines; 10950456 not in entry page or history page; live history top is still #6 (Susanna Cuyler, approved 2020-02-02), no pending/editing draft. PASS.
6. OEIS value search: q=10950456 -> "No results."; q=4242226,10950456 -> "No results." (sha256 identical to the claim's pre-claim table). PASS.
7. Definition match: claim's definition = entry %N + %C + %t (disjunsQ/ldrsi). I wrote my own literal Python transcription of the %t code (panel/criterion_fetch/lit.py: partitions of n-1 x sorted tuples, Union, disjunsQ = single branch OR (non-leaf branches pairwise distinct AND every pair equal or with empty set intersection)); it gives a(1..21) = DATA then 10950456 (lit_21.out, 43 s). PASS.
8. Two independent programs agree and reproduce all DATA: rebuilt claim/programs pA_c (C) and pB_go (Go) from the copy; both print a(1..20) == DATA exactly and a(21) = 10950456 (pA_21.out 0.2 s, pB_21.out 2.3 s). Different languages and algorithms (id-set + mark array vs. literal partition x tuple transcription). Negative fixture pA 16 nodisj gives 1,1,2,4,8,18,41,... (A306200), != DATA. PASS.
9. PREREG before attempts: PREREG.md frozen 2026-11-03T20:05:19Z (mtime 15:05:19 EST); earliest program file attempts/exact-eval-first/code/progA.c 15:05:36 EST, Go 15:06:03, Python 15:06:27; only pre-PREREG files are data/ fetches (15:04:59-15:05:00). PASS.
10. Value novelty: claimed value 10950456 at the first missing index, absent from entry, b-file, history and value searches (items 4-6). PASS.
11. No submission to OEIS: none made or implied (CLAIM status PROMISING; packaging gated on owner). By-products a(22..23) are explicitly excluded from the claim and not assessed.

Caveats (not failing): a(21) relies on the entry's own definition/Mathematica; the b-file is synthesized from DATA, so "first index not present" is the same for both. Literature/web novelty is the novelty skeptic's job; not re-done here.

confirmed_scope: A331783(21) = 10950456 meets the oeis-keyword-more-new-terms criterion as of 2026-11-03T21:19Z (live entry keyword more, DATA and b-file end at a(20), n = 21 first missing, no value-search/history/draft hit, not bank-excluded, PREREG precedes all programs, and two claim programs plus my own literal %t transcription all reproduce DATA and give 10950456); by-products a(22..23) are out of scope.
pass: true
