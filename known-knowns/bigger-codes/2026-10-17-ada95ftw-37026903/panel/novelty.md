# NOVELTY verdict: A(33,10,7) <= 145

context: subagent (fresh executor, saw only claim/A33_10_7/)

Package files I read (relative to the claim folder): CLAIM.md, cert_A33_10_7.json, verify.py, REPRODUCE.md, table_record.md, table_snapshot/Andw.html.
I sent one request to each address listed below, with no retries. I took no outward action.

## 1. Live status source (one plain curl, no retry)
- URL: https://aeb.win.tue.nl/codes/Andw.html
- time (date -u): request started 2026-10-17T08:35:20Z, finished 2026-10-17T08:35:22Z (04:35 AM EDT)
- result: HTTP 200, 127383 bytes, sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8
  This is byte-identical to table_snapshot/Andw.html (same sha256 as in table_record.md).
- Target cell. Section "Bounds on A(n,10,w)" > "Values of A(n,10,7)", column n=33, raw HTML:
  `<td><a href="cwc/d10/i33.7">72</a><sup>g</sup>-150</td>`
  -> live lower bound 72, **live upper bound 150**. The upper bound has no superscript.
- Mirror A(33,10,26): the table lists only w <= n/2. The string "A(33,10,26)" appears 0 times on the page, so there is no separate mirror entry. By complementation A(33,10,26) = A(33,10,7), so its bound is the same 72-150.
- Page legend (line 68): "For n > 28 unmarked upper bounds are from the Johnson bound." So 150 is a Johnson bound.
- Input cell A(26,10,7), main d=10 table, raw HTML: `<span class="nw"><a href="cwc/d10/i26.7">30</a><sup>c</sup></span>-36`. This matches CLAIM.md: "30-36", and the upper bound 36 is unmarked, so it comes from AVZ for n <= 28. Agrell's table (https://codes.se/bounds/cw.html, fetched once) lists A(26,10,7) as "28- 36 14", i.e. AVZ Theorem 14. The input is consistent.

### Caveat found: the printed 150 is a stale Johnson value
- 150 = floor(33/7 * 32) = floor(1056/7). This uses A(32,10,6) <= 32.
- The same live page prints A(32,10,6) = 31 as an exact value (main row n=32 `<td>31</td>`; the "Values of A(n,10,6)" table also gives n=32: `<td>31</td>`).
- Putting 31 into the same Johnson bound gives A(33,10,7) <= floor(1023/7) = **146**. Anyone can derive this from the live table today; it just isn't printed.
- The other Johnson direction gives floor(33/26 * 139) = 176, which is weaker.
- So the real bar is 146, not 150. The claimed 145 still beats it strictly, but by **1**, not by 5. CLAIM.md's wording "strictly below the upper bound 150 printed" is true, but it should say that 146 follows directly from the table.

## 2. Independent recomputation (my own code, lp_check.py; it does not use verify.py)
I computed Q_k for J(33,7) from the dual-Hahn closed form and solved the LP exactly with Fractions by vertex enumeration:
```
plain Delsarte LP: 5456/35 155.88571428571427
Delsarte + a7<=36: 26928/185 145.55675675675676
Delsarte + R5,R6,R7 (A(26,10,5)=5, A(26,10,6)=13, A(26,10,7)<=36): 26928/185 145.55675675675676
```
This agrees with the certified value 26928/185 in cert_A33_10_7.json. Plain Delsarte alone gives 155 > 150, so the bound only works because of the R7 counting row. I also ran verify.py on cert_A33_10_7.json. It printed "VERIFIED bound 145" and exited with code 0. An earlier exit code of 1 came from a separate command chained in the same shell call, not from verify.py.

## 3. Repo: TROPHY_CASE.md and open PRs (one request each)
- 2026-10-17T08:36:05Z: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md -> HTTP 200, 30936 bytes.
  - It has no row for A(33,10,7) or A(n,10,7) upper bounds.
  - Its constant-weight rows are 30 codes (lower bounds) and 5 Delsarte LP upper bounds, all d=12: A(31,12,10), A(31,12,11), A(32,12,10), A(32,12,15), A(32,12,16).
  - The repo labels those LP bounds "classical method; new only as a table entry". The same label fits this claim.
- 2026-10-17T08:36:05Z: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 -> HTTP 200. That returned 92 open PRs, all on one page since 92 < 100.
  - No title or body matches "constant-weight", "A(33", "33,10", "Andw", "A(n,10", "Brouwer" or "Delsarte".
  - The newest PRs are about other targets, e.g. #331 qutrit EAQECC and #330 fmm.

## 4. Literature (upper bounds)
- Agrell-Vardy-Zeger 2000, and Agrell's table https://codes.se/bounds/cw.html (fetched once): only covers n <= 28. Nothing for n=33.
- Schrijver 2005: n <= 28 (also covered by Agrell's table updates 2004/2015). Nothing for n=33.
- Kim-Toan arXiv:1212.3467 (fetched once): "Twenty three new upper bounds on A(n,d,w) for n <= 28". Its Table II has no n=33 or (d=10, w=7) entry.
- Polak 2018, IEEE TIT doi 10.1109/tit.2018.2854800. I fetched the CWI copy https://ir.cwi.nl/pub/30362/30362.pdf once at 2026-10-17T08:36:38Z (HTTP 200).
  - Table III covers 29 <= n <= 32 and d >= 10 only. Its d=10 rows are (29,9), (32,10), (32,11), (29,12), (29,13), (30,14), (31,14), (32,15), (32,16).
  - No w=7 entry and no n=33.
- arXiv:2608.13906 (Echols, fetched once): lower bounds only. Its 124 cells include A(34..63,10,7) lower bounds, but nothing for A(33,10,7) and no upper bounds.
- arXiv:2607.19550 (Lysenstoen, fetched once): lower bounds only, d=6 cells. It explicitly says modern SDP/LP upper-bound work "never touched this cell" (about A(23,6,10)).
- Web searches (3 queries, 2026): nothing newer reports an upper bound for A(33,10,7) or new LP/SDP bounds for n > 28. The 2026 hits are lower-bound constructions (arXiv:2603.00174, 2608.13906, 2607.19550) or asymptotic work (arXiv:2609.01860).

## Verdict
- The live status source was read successfully: live upper bound for A(33,10,7) is 150, and the mirror A(33,10,26) is the same by complementation.
- No source I checked has a bound <= 145 for this cell.
- The best bound you can derive from the live table is 146 (Johnson bound with the table's exact A(32,10,6) = 31). 145 < 146, so this is a strict improvement and not a tie, but only by 1.
- The method is classical: Delsarte LP plus one AVZ-style counting row. It is new only as a table entry.
- Any write-up should say the margin is 1 over the derivable 146, not 5 over the printed 150.

novelty: CONFIRMED (strict, margin 1 vs. the table-derivable Johnson bound 146; 5 vs. the printed 150)
pass: true
