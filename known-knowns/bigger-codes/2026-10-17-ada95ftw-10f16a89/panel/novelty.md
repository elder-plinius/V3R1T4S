# NOVELTY verdict: claim A(32,10,7) <= 131

context: subagent (fresh executor, saw only claim/A32_10_7/)

novelty: CONFIRMED. 131 is strictly below the live printed upper bound 139, and I found nothing published or pending that is at or below 131.

## 1. Live status source (one plain curl, no retries)
- URL: https://aeb.win.tue.nl/codes/Andw.html
- Fetch window (UTC, `date -u`): 2026-10-17T08:31:22Z to 2026-10-17T08:31:23Z. HTTP 200, 127383 bytes.
- sha256 of the live page: 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. This is byte-identical to table_snapshot/Andw.html and matches table_record.md.
- Target cell, main table "Bounds on A(n,10,w)", row n=32, column w=7. Raw HTML:
  `<th>32</th><td>31</td>` / `<td><a href="cwc/d10/i32.7">64</a><sup>c</sup>-139</td>`
  So the live value is **64-139**: lower bound 64, upper bound **139**. The upper bound has no source mark.
- The same cell in the secondary table "Values of A(n,10,7)": `<td><a href="cwc/d10/i32.7">64</a><sup>c</sup>-139</td>`. It agrees.
- What an unmarked bound means, from the page header: "For n > 28 unmarked upper bounds are from the Johnson bound." Check: floor(32/25 * A(31,10,7) <= 109) = floor(139.52) = 139.
- Input cell A(25,10,7), raw HTML: `<th>25</th><td>10</td>` / `<td><a href="cwc/d10/i25.7">28</a><sup>c</sup>-32</td>`, so it reads **28-32**. Per the page header, "Unmarked upper bounds (for n <= 28) are taken from" [AVZ] (Agrell, Vardy and Zeger). So the input <= 32 is a published, peer-reviewed bound.
- Mirror A(32,10,25): the d=10 table prints only w <= n/2 (for n=32 the columns run w=6..16). A(32,10,25) = A(32,10,7) by complementation, so there is no separate mirror cell, and the live bound for it is also 139.

## 2. Comparison with the literature
- Agrell-Vardy-Zeger 2000: its tables cover n <= 28, and the page uses it only as the source of unmarked bounds for n <= 28. It gives no value for n=32.
- Schrijver 2005 and Kim-Toan 2012 (arXiv:1212.3467, fetched 2026-10-17T08:32:35Z, HTTP 200). The abstract says: "Twenty three new upper bounds on A(n,d,w) for n <= 28". Nothing for n=32. arXiv:1108.5104 (improved LP bounds) also covers n <= 28. I saw this only in a search snippet and did not fetch it.
- Polak 2018/2019 (IEEE TIT 65, 28-38, doi 10.1109/tit.2018.2854800). I fetched arXiv:1703.05171 once (abstract at 2026-10-17T08:32:35Z, PDF at 2026-10-17T08:32:40Z, HTTP 200). Its Table 3 ("new upper bounds ... 29 <= n <= 32 and d >= 10") has these d=10 rows for n=32: w=8 (402), 10, 11, 12, 13, 14, 15, 16. **It has no w=7 row**, so Polak gives no bound for A(32,10,7). This matches the live page, which has no "Po" mark on that cell.
- arXiv:2608.13906 (Echols, submitted 14 Aug 2026; fetched 08:32:35Z): "124 new constructions that improve existing **lower** bounds". It is a lower-bound paper with no upper bounds.
- arXiv:2607.19550 (Lysenstoen, submitted 21 Jul 2026; fetched 08:32:35Z): explicit codes, i.e. **lower** bounds, for A(23,6,10), A(24,6,10), A(23,6,11) and A(24,6,8). It does not touch this cell.
- Web searches on 2026-10-17: (a) for new SDP or LP upper bounds on constant-weight codes in 2025-2026, and (b) for the exact string "A(32,10,7)". (a) turned up only Polak, the 2026 lower-bound papers, and a quantum-code SDP paper (arXiv:2603.19901), which does not apply. (b) returned only unrelated pages. I found no newer upper bound for this cell.

## 3. The repo (elder-plinius/V3R1T4S), read-only
- TROPHY_CASE.md: one curl of raw.githubusercontent.com/.../main/TROPHY_CASE.md at 2026-10-17T08:32:09Z, HTTP 200, 30936 bytes. Its constant-weight section lists 30 codes and 5 Delsarte LP upper bounds: A(31,12,10) <= 197, A(31,12,11) <= 380, A(32,12,10) <= 245, A(32,12,15) <= 2511 and A(32,12,16) <= 2652. **There is no A(32,10,7) and no A(32,10,25) entry.** The trophy case also labels its own LP bounds "classical method; new only as a table entry".
- Open PRs: GET api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 at 2026-10-17T08:32:10Z, HTTP 200. It returned 92 open PRs, fewer than 100, so this is the full list. A regex over all titles and bodies for constant-weight / A(32 / 32,10,7 / 32,10,25 / Andw / cwc found **no matches**. The PRs cover qubit codetables, packomania, FMM, covering designs and similar.
- Disclosure: after the GET, I also sent one header-only (HEAD) request to the same PR endpoint to look for a pagination link. That is a second request to that URL. It did not change the result.

## 4. Sanity check of the bound (not my role's main job, but it shows the claim is not a misread)
- `python3 verify.py cert_A32_10_7.json` output:
```
selftest: Delsarte inequalities hold on 150 random subsets; P-for-Q control fails; scheme sums zero: OK
  column x=5: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=6: sum_r y_r row_r(x) = 1  (needs >= 1)
  column x=7: sum_r y_r row_r(x) = 1  (needs >= 1)
certified: A(32,10,7) <= 46624/355 = 131.335211, hence A(32,10,7) <= 131
VERIFIED bound 131
```
- I wrote my own exact solver for the 3-variable LP. It finds every vertex, computes Q_k(x) = m_k P_x(k)/v_x from the Eberlein eigenvalues instead of the package's dual-Hahn formula, and imposes all 7 Delsarte inequalities:
```
pure Delsarte LP: 992/7 141.71428571428572 ['105', '0', '250/7']
Delsarte + a7<=32: 46624/355 131.33521126760564 ['33999/355', '182/71', '32']
```
  Pure Delsarte only gives 141, which is weaker than the Johnson value 139. The improvement comes entirely from the valid constraint a_7 <= A(25,10,7) <= 32 (the codewords disjoint from a fixed codeword form a (25,10,7) code; this is an AVZ-type constraint). My maximum agrees exactly with the certificate: 46624/355, so the bound is 131.

## 5. Assessment
- Strictly beats the live table: 131 < 139, a margin of 8. It is not a tie.
- Strictly beats the literature: no source I checked (AVZ 2000, Schrijver 2005, Kim-Toan 2012, Polak 2018/19, Echols 2026, Lysenstoen 2026, web search) gives any upper bound for A(32,10,7) below 139.
- Not already claimed in the repo: no TROPHY_CASE entry and no open PR for this cell.
- Caveats:
  - The method is classical: Delsarte LP plus an AVZ-style a_w <= A(n-w,d,w) constraint. The novelty is only as a table entry.
  - The result depends on the AVZ-published input A(25,10,7) <= 32.
  - A literature search cannot rule out an unindexed private computation.

pass: true
