# PREREG — latin-max-intercalates

Frozen at 2026-11-20T12:25Z (from `date -u`), before any attack program was run.

## Criterion (verbatim, bank/targets.json)
"Success means an explicit Latin square of order n, 10 <= n <= 28 with n not 15 or 16, whose number of
intercalates is STRICTLY GREATER than the largest bound listed for that n in A092237 (comments and the
a092237_2.txt proving-list headers) and A307164 (comments and its proving-list headers). Re-fetch all of them
immediately before claiming. The 2026-10-30 values are above; the n = 23 bar is 985 and the n = 27 bar is 1372.
The count must agree between two independent programs. Order 16 is excluded because 960 meets the proven bound
n^2(n-1)/4. Order 15 is excluded because 630 meets the proven odd-order bound n(n-1)(n-3)/4."

## Statistic that judges it
`intercalates(L)` from `attempts/checker-first/code/countA.py`, and independently `countB.py`. Both validated by
`selftest.py` (PASS) and both agree on all 54 posted squares. A candidate counts as a win only if:
1. it is a Latin square of order n (all rows and all columns contain each symbol exactly once);
2. countA == countB on it;
3. its count is STRICTLY greater than the bar for that n (the larger of the two proving-list headers, and, if a
   human later reads the OEIS comments, the larger of those too);
4. its count does not exceed the proven bound (even: n^2(n-1)/4, odd: n(n-1)(n-3)/4);
5. n in 10..28, n not 15 or 16.

## Thresholds
- A win needs count >= bar + 1.
- Anything at exactly the bar is a tie, not a record.
- Above the proven bound is a checker bug, not a win; such a case is treated as a failed check.

## Bars frozen (proving-list headers, both files, max), 2026-11-20T12:20:40Z
10:125 11:172 12:324 13:216 14:391 15:630 16:960 17:736 18:729 19:472 20:1500 21:1026 22:1497 23:985
24:2736 25:1888 26:2197 27:1372 28:2940
(OEIS comments PENDING TABLE CHECK: HTTP 403 Cloudflare on both sequence pages and on the fmt=text search.)

## Null design
null_test: not needed because the win is an explicit object (a Latin square) checked by two deterministic
counters against a published table value; there is no search-statistic claim, no key, and no "beats chance"
language. Every claimed number is a deterministic recount of a saved square.

## Primary target for this run
n=17 (bar 736, proven bound 952, only posted witness recounts to 272). Chosen because it is an odd order where the
bar sits far from both the bound and the only witness; per-row-pair cap is (17-3)/2 = 7, and there are 136 row
pairs, so the ceiling is 952.
