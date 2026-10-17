# Novelty verdict: A(34,10,8) <= 618

context: subagent (fresh executor, saw only claim/A34_10_8/)

Role: NOVELTY skeptic. I read only claim/A34_10_8/ and made my own fetches. Each URL was fetched once with plain curl, and no retries were needed. All times below are UTC (`date -u`).

## 1. Live status source (fetched once)
- URL: https://aeb.win.tue.nl/codes/Andw.html
- fetched: 2026-10-17T08:35:50Z, one curl request, HTTP 200, 127383 bytes
- sha256 of the live page: 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8.
  It is byte-identical (`cmp`) to table_snapshot/Andw.html, which matches the sha256 in table_record.md.
- Target cell, from section "Bounds on A(n,10,w)", subsection "Values of A(n,10,8)", column n=34:
  `<td><a href="cwc/d10/i34.8">181</a><sup>g</sup>-637</td>`  ->  **live lower bound 181, live upper bound 637** (unmarked).
- Page legend: "For n > 28 unmarked upper bounds are from the Johnson bound." Check: floor(34/8 * A(33,10,7) upper bound 150) = floor(637.5) = 637.
- Mirror A(34,10,26): the page lists only w <= n/2, and A(34,10,26) = A(34,10,8) by complementation. No separate entry exists, so the mirror's bound is also 637.
- Input cell A(26,10,7), main d=10 table, row 26: `<span class="nw"><a href="cwc/d10/i26.7">30</a><sup>c</sup></span>-36`. This gives upper bound 36, unmarked for n <= 28, so it comes from AVZ 2000. The input the claim uses (36) matches the live page.
- Neighbouring cells with Polak marks: A(31,10,8) 124-322^Po and A(32,10,8) 145-402^Po. The n=34 cell has no Po, S, KT or KKT mark.

## 2. The claimed value against the live bound
618 < 637, so the claim strictly improves the upper bound by 19. It is not a tie.

## 3. Literature (each fetched once; times UTC)
- AVZ 2000 (Agrell, Vardy, Zeger), via the online tables https://codes.se/bounds/cw.html, fetched 2026-10-17T08:36:46Z, HTTP 200. The page says "The tables give the best known bounds on A(n,d,w) for all n up to 28". It does not cover n=34.
- Schrijver 2005: the Brouwer legend credits S for n <= 28 cells only, and AVZ's online table lists Schrijver's updates within n <= 28. Nothing covers n=34.
- Kang-Kim-Toan 2011, arXiv:1108.5104 (fetched 2026-10-17T08:36:48Z, HTTP 200), and Kim-Toan 2012, arXiv:1212.3467 (fetched 08:36:47Z, HTTP 200). Their tables stop at n=28 (e.g. the last row of 1212.3467 is "28 10 11 ..."). Nothing covers n=34.
- Polak, arXiv:1703.05171 = IEEE TIT 64 (2018), doi 10.1109/tit.2018.2854800 (fetched 08:36:47Z, HTTP 200). Table 2 covers n <= 28. Table 3 is "An overview of the new upper bounds for constant weight codes for 29 <= n <= 32 and d >= 10". Its d=10, w=8 rows are only "31 10 8 124 322B 329" and "32 10 8 145 402B 436". No row has n > 32, so n=34 is not covered.
- Smith-Hughes-Perkins 2006, EJC 13 #A2 (https://www.combinatorics.org/ojs/index.php/eljc/article/download/v13i1a2/pdf, fetched 08:37:19Z, HTTP 200). Table 9 ("d = 10, w = 8"), row 34, has UB 637. The paper says the UB column is "the Johnson upper bound". So this agrees with 637.
- Echols, arXiv:2608.13906 (fetched 08:36:47Z, HTTP 200): a lower-bound paper using tabu search. Its tables list d=10, w=8 lower bounds (e.g. 43 10 8 456 -> 470) and have no upper bounds.
- Lysenstoen, arXiv:2607.19550 (fetched 08:36:47Z, HTTP 200): a lower-bound paper (A(23,6,10) and others). It has no upper bounds and no n=34, d=10 cell.
- Newer sources, via web searches on 2026-10-17:
  - arXiv:2603.27639 covers q-ary and constant-weight B_2 codes, which is a different problem.
  - arXiv:2609.23869 covers nonbinary and constant-composition envelopes, not binary cells.
  - arXiv:2609.35051 (Yang et al., fetched 08:37:45Z) is a kissing-number paper with no A(34,10,8) bound.
  - zerothesis.com constant-weight-codes (fetched 08:38:00Z) is a lower-bound challenge with n <= 28 only.
  - I found no upper bound for A(34,10,8) below 637 anywhere.

## 4. Repo checks (read-only, once each)
- TROPHY_CASE.md, https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-10-17T08:36:16Z, HTTP 200, 30936 bytes.
  - Its constant-weight rows are 30 codes plus 5 Delsarte LP upper bounds: A(31,12,10), A(31,12,11), A(32,12,10), A(32,12,15) and A(32,12,16).
  - None of them is A(34,10,8) or A(34,10,26).
- Open PRs, https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100, fetched 2026-10-17T08:36:16Z, HTTP 200, 92 open PRs.
  - No title or body matches "constant weight", "A(34", "34,10,8", "34,10,26", "Andw", "cwc" or "Brouwer" (regex scan).
  - So no open PR claims this cell or anything below 618 for it.

## 5. Independent sanity checks (do not affect the novelty finding)
- `python3 verify.py cert_A34_10_8.json` printed the selftest OK line and column sums x=5..8 all equal to 1, then "certified: A(34,10,8) <= 114444/185 = 618.616216, hence A(34,10,8) <= 618" and "VERIFIED bound 618".
- My own exact vertex enumeration of the LP (lp_check.py in this folder; it does not use the claim's code) gave:
  - pure Delsarte: 23188/35 = 662.51. This is worse than the printed 637, so plain Delsarte alone does not give a record.
  - Delsarte + a_7 <= 8*A(26,10,7) = 288: 114444/185 = 618.616. This equals the certified value, so the certificate is optimal for that LP.

## Caveats (to pass on, not grounds for failing)
- The method is classical: Delsarte LP plus AVZ/KKT-style constraints a_x <= C(w,x) A(n-w,d,x). The improvement is new only as a table entry, in a cell whose printed bound is just the Johnson bound.
- The result depends on the published input A(26,10,7) <= 36 (AVZ, live on the page).
- The lower bound (181) is unchanged, so the cell stays open (181..618).

novelty: CONFIRMED. The live printed upper bound for A(34,10,8) (mirror A(34,10,26)) is 637 (Johnson) at 2026-10-17T08:35:50Z, and 618 is strictly below it. No literature (AVZ 2000, Schrijver 2005, KKT 2011, Kim-Toan 2012, Polak 2018 with n <= 32, SHP 2006, Echols, Lysenstoen, newer searches), TROPHY_CASE.md entry or open PR has a bound <= 618 for this cell.

pass: true
