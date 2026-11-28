# Criterion skeptic vote: A361864(12) = 2092816 (oeis-keyword-more-new-terms)

context: subagent (criterion)
working copy: private copy of claim/ (panel-medmed-criterion2 scratch); fresh context, no other panel files read.

## Bank criterion, clause by clause
1. Keyword 'more' in live entry: live re-fetch 2026-11-03T17:41:23Z (12:41 PM EST) of https://oeis.org/search?q=id:A361864&fmt=text shows `%K A361864 nonn,more`, `%I #5 Apr 04 2023`, `%O 1,3`. PASS.
2. First index not in DATA or b-file: live DATA `%S 1,0,3,6,30,96,461,2000,10727,57092,342348` (n=1..11, offset 1); live b-file https://oeis.org/A361864/b361864.txt ends `11 342348`. Claimed index 12 is the first missing one. Matches table/A361864_internal.txt and table/b361864.txt. PASS.
3. Two independently written programs that agree and reproduce all existing terms: rebuilt and ran from the copy:
   - programs/pA_c/medmed.c (C, restricted-growth strings, doubled-integer medians, parity tests): 1..12 -> 1,0,3,6,30,96,461,2000,10727,57092,342348,2092816 (0.9 s).
   - programs/pB_go/main.go (Go, "block containing lowest unused element" over bitmasks, exact rationals p/q): identical 12 lines (4.4 s).
   Different language, different partition generator, different median arithmetic; no shared code; produced in separate attempts (attempts/exact-eval-first, attempts/search-engineer). Both reproduce a(1..11) exactly. PASS.
   - Extra: programs/pC_py/brute.py reproduces a(1..10). My own skeptic script (skeptic.py in the scratch copy; insertion-order partition generator, Python statistics.median over Fractions) gives a(1..12) identical, a(12)=2092816 (41 s).
4. Not in comments/links/extensions: entry has no %H/%E lines; `2092816` occurs 0 times in table/A361864_internal.txt and the live history page. PASS.
5. Not in edit history incl. pending drafts: live https://oeis.org/history?seq=A361864 (17:41:24Z) lists revisions #1..#5 only, latest #5 by Michael De Vlieger 2023-04-04 (approved); "proposed"/"editing" strings appear only as status diffs inside old revisions. No pending draft. PASS.
6. Not in OEIS search for the value: live https://oeis.org/search?q=2092816&fmt=text -> "No results." (17:41:23Z); also table/search_2092816.txt and table/search_342348_2092816.txt "No results." PASS.
7. Exclusions: bank/targets.json and repo bank/ contain no mention of A361864 (grep "361864" in bank/ = 0 hits; known-knowns hits are unrelated digit substrings in certificate files). Not a near-repdigit/repunit prime-index sequence. Run 2026-11-03-1621-totcross mentions A361864 only as a sibling family reference, not a claim on this cell. PASS.
8. No submission to the OEIS: nothing in the run indicates one. PASS.

## Definition match
Entry: "%N Number of set partitions of {1..n} whose block-medians have integer median. %C The median of a multiset is either the middle part (odd length), or the average of the two middle parts (even length)." Mathematica `%t ... IntegerQ[Median[Median/@#]]` over all set partitions (sps). All programs compute the median of each block, then the median of the multiset of block medians (with repetition), integer test exact. Example check: a(4)=6 and {{1,2},{3},{4}} counted (medians 3/2,3,4 -> 3), reproduced. Offset 1, no n=0 term involved. Matches PREREG statistic. PASS.

## PREREG timing vs attempts
PREREG.md frozen 2026-11-03T16:18:26Z (file mtime 11:18:26 EST matches). Earliest attack code: attempts/exact-eval-first/code/medmed.c 11:18:35 EST, attempts/search-engineer/code/main.go and brute.py 11:18:47 EST; first outputs 11:18:56 EST onward. All attack files postdate PREREG (margin ~9 s, consistent but tight; only mtime evidence). Data fetches (16:17:38Z-16:17:44Z) predate PREREG, which is fine (table, not attack). Value search fetched 16:19:42Z after the computation, before claim (claim/ 11:24 EST). PREREG threshold "A and B reproduce a(1..11) and agree on a(12)" is met. PASS.

## Caveats (not blocking)
- Timing evidence is filesystem mtimes only; 9 s margin between PREREG and first code.
- By-product terms a(13), a(14), a(15) in attempts/ are not part of the claim and were not checked here.

confirmed_scope: A361864(12) equals 2092816, the first term beyond the live DATA and b-file of OEIS A361864 (keyword more), computed by two independent programs that reproduce a(1..11) and not found in the entry, its history, or an OEIS value search as of 2026-11-03T17:41Z.

pass: true
