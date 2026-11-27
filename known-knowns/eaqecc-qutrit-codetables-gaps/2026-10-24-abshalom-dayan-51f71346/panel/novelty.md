# Novelty skeptic: [[28,6,12;6]]_3 at cell (n,k,c) = (28,6,6)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

File names below are relative to my work folder (`work-novelty/`), or start with `claim/` for the claim package.
Fetch logs with URL, UTC times, HTTP status and sha256 for every page I fetched are in `fetched/*/FETCHLOG.txt`
and `fetched/qutrit/{time_before,time_after,http_code,headers}.txt`.

## Bottom line

Novel as far as I can establish. The live cell is still `[[28,6,11-17;6]]_3`, so 11 < 12 <= 17. I found no published
code and no valid chain of the table's rules that gives d >= 12 at (28,6,6) with c <= 6. The closest known results:

| known code | source | why it does not reach (28,6,6) at d = 12 |
|---|---|---|
| [[28,6,12;8]]_3 | live table (increasing dimension of [[28,0,12;2]], from arXiv:2207.05647) | needs 8 pairs; c never decreases under the rules |
| [[28,5,12;5]]_3 | live table ("using teleportation") | one fewer logical qutrit; increasing dimension is not valid for teleportation codes (shown below) |
| [[28,9,12;9]]_3 | arXiv:2207.05647, Table 2 (also in the live table) | from a [28,14,12]_9 code with Hermitian hull 5, not 8 |
| [[27,6,13;9]]_3 | Christensen, Munuera, Pereira, Ruano, arXiv:2105.02166 (not in the live table) | c = 9; lengthening gives [[28,6,13;9]] |

There is one residual risk. Two papers on qutrit stabilizer codes (c = 0) could not be read in full: one fetch was
blocked, the other paper is paywalled. They would matter only if they contain a code such as [[28,0,12]]_3 or
[[29,1,12]]_3 (see Caveats).

## 1. Live status fetch (one plain GET, no retries)

- URL: https://eaqecc.codetables.de/qutrit.php
- Command: `curl -sS -A "V3R1T4S-research-agent (honest single fetch)" -D headers.txt -o qutrit.php -w '%{http_code}'`
- UTC from `date -u`: before 2026-10-24T15:34:47Z, after 2026-10-24T15:34:48Z. Server `date:` header: Sat, 24 Oct 2026 15:34:47 GMT
- HTTP status: 200 (`HTTP/2 200`, content-type text/html; charset=UTF-8). Size: 628039 bytes
- sha256: `37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`. That matches `claim/table/qutrit.php` byte
  for byte (`cmp` printed IDENTICAL), so the table has not changed since the claim's 15:03:31Z fetch.
- Page footer: `Last change: 10.07.2025`
- The cell, verbatim:
  `<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[28,0,11;0]] from codetables.de">[[28,6,11-17;6]]<sub>3</sub></TD>`
- So d_lower = 11 and d_upper = 17. The claim's d = 12 satisfies 12 > 11 and 12 <= 17.
- The full listed row n = 28, k = 6 (c: d_lower-d_upper): 0: 9-10, 4: 10-14, 6: 11-17, 8: 12-19, 11: 13-20,
  12: 14-21, 13: 15-21, 14: 16-21, 16: 17-22, 18: 18-22, 20: 19-22, 22: 20-23. Values of c that are not listed take the
  bound of the next lower listed c.
- No challenge page. A grep of the page for `<script`, `ignore`, `instruction` or `assistant` returned no hits.
  injection_suspected: none.

## 2. Closure under the table's own rules

The colour legend lists these rules: subcode [[n,k-1,d;c]], lengthening [[n+1,k,d;c]], puncturing [[n-1,k,d-1;c]],
trivial [[n,0,n+1;n]], quantum shortening [[n-1,k+1,d-1;c]], increasing dimension [[n,k+1,d;c+1]], length reduction
[[n-1,k,d;c+1]], teleportation [[n,k,d;k]], plus entries from codetables.de and arXiv:2207.05647. I parsed all 3888
cells (`scripts/parse.py` produced `fetched/qutrit/cells.json`). Every single-rule source that could land on (28,6,6)
with d >= 12 and c <= 6 has a lower bound that is too small:

| rule into (28,6,6) | source cell needed | table d_lower there |
|---|---|---|
| subcode | (28, k>=7, c<=6), d >= 12 | (28,7,6) 10, (28,8,6) 10, (28,9,6) 9; at most 10 for all k >= 7 |
| lengthening | (27, k>=6, c<=6), d >= 12 | (27,6,6) 10; at most 10 for all k >= 6 |
| puncturing | (29, k>=6, c<=6), d >= 13 | (29,6,6) 11; at most 11 |
| quantum shortening | (29,5,c<=6), d >= 13 | (29,5,6) 12 ("using teleportation") |
| length reduction | (29, k>=6, c<=5), d >= 12 | (29,6,5) 11; at most 11 |
| increasing dimension | (28,k,k) with k <= 5, d >= 12 | (28,0,0) 11; (28,1,1) 21, (28,2,2) 18, (28,3,3) 15, (28,4,4) 15, (28,5,5) 12, all "using teleportation" |
| teleportation | a classical [28,12,12]_3 code | codetables [28,12]_3: lower bound 10, upper bound 11 |

The teleportation cells (28,k,k) for k <= 5 are not valid sources for increasing dimension. If that rule applied to
them, [[28,1,21;1]] would give [[28,14,21;14]] after 13 steps. The table's own upper bound at (28,14,14) is 15, so
that is impossible. Luo, Ezerman, Grassl and Ling (arXiv:2207.05647, Theorem 12, "More Entanglement") state the rule
only for pure codes from the Hermitian construction. Quantum shortening likewise needs purity. A naive closure that
applies these two rules to every cell inflates (28,6,6) to 21 or 23 through teleportation cells, which is impossible
(`scripts/closure.py`, `scripts/trace.py`). With those misapplications excluded, nothing reaches 12. The source paper's
Theorem 18 ("Less Entanglement", [[n,k,d;c]] to [[n+1,k,d';c-1]]) only guarantees d' <= d, so it gives no lower bound.

## 3. Codes over GF(9) and their Hermitian hulls

In the Hermitian construction, an [n,K,d]_9 code with Hermitian hull dimension l gives [[n, K-l, >=d; n-K-l]]_3. At
(28,6,6) that means K = 14 and l = 8, which is exactly the claim's G9: the extended one-point Hermitian code E_16. Its
sha256 is 51f713462c7db831723702a4d0b0cc9a73faacd2552999a7007f75d393188573, which matches CLAIM.md. Getting k >= 6 with
c <= 6 at n = 28 needs K >= 14 and d >= 12. I checked codetables.de, one GET per cell, all HTTP 200:

| code | codetables.de bounds | consequence |
|---|---|---|
| [28,14]_9 | 12-13 (AG code on the Hermitian curve, "based on 2 divisors of degree [3,4]") | d = 12 is known; the hull is what matters |
| [28,15]_9 | 11-12 | no K >= 15 code with d = 12 is known |
| [27,14]_9 | 11-12 | no length-27 route |
| [29,15]_9 | 11-13 | rules out puncturing from d = 13 and length reduction |
| [29,14]_9 | 12-14 | rules out quantum shortening (needs d >= 13) |

So only a [28,14,12]_9 code with hull >= 8 would do. The table's source paper lists [[28,9,12;9]]_3 for n = 28 (its
Table 2), which corresponds to hull 5. They searched for the minimum c over coordinate scalings (their Theorem 14) and
did not report hull 8.

Qutrit stabilizer routes (c = 0, then length reduction j times, then increasing dimension) would need a code
[[28+j, >=j, >=12]]_3. codetables.de shows [[28,0]]_3 at 11-13, [[29,1]]_3 at 11-13 and [[30,2]]_3 at 10-13 (pages say
"Last change: 10.06.2024"). In the live table's c = 0 column, (31,3) is 10-13, (32,4) 10-13, (33,5) 9-13 and (34,6)
9-13. None is known at 12.

## 4. Literature searched

WebSearch queries:

1. entanglement-assisted quantum codes Hermitian curve Hermitian hull one-point codes
2. qutrit entanglement-assisted quantum error-correcting codes new codes 2025 2026 arXiv table Grassl
3. Hermitian hull extended algebraic geometry codes entanglement-assisted quantum codes 2025
4. "[[28,6,12;6]]" entanglement-assisted (no hits for these parameters)
5. Hermitian hull of one-point Hermitian codes ... q^3+1 points extended
6. new entanglement-assisted qutrit codes improving Grassl's table F_9 ... 2025 2026
7. Li Li Guan Song "Hermitian self-orthogonal codes over F9" ...
8. entanglement-assisted ... "Hermitian codes" extended OR "two-point" ... length 28 F_9
9. linear codes over F9 prescribed Hermitian hull dimension ... building-up construction 2025
10. new ternary quantum stabilizer codes ... length 28 29 30
11. "Hermitian self-dual" codes over GF(9) length 28 minimum distance 12
12. to 18. targeted searches for the parameter lists of recent ternary quasi-twisted and quasi-cyclic stabilizer-code
    papers, and for "[[28,0,12]]", "[[29,1,12]]", "[[30,2,12]]", "[[32,4,12]]"
19. Pereira, Pellikaan, La Guardia, Assis, EAQECCs from AG codes
20. entanglement-assisted codes from Castle curves or the Hermitian curve on all q^3+1 points

Sources I opened (one GET each, saved under `fetched/`) and what they contain:

- https://arxiv.org/html/2607.02170 (Li, Ezerman, Li, Ling, Sun, July 2026). Generalized extended codes with Hermitian
  hull control. It reports 14 new qutrit EA codes with 7 <= n <= 25, all with k <= 3 and none with d >= 12 at c <= 6;
  lengthening cannot raise k. It compares against Grassl's tables as accessed 15 June 2026. It has no n >= 26 qutrit
  entries and no Hermitian-curve codes.
- https://arxiv.org/html/2105.02166 (Christensen, Munuera, Pereira, Ruano). EAQECCs from one-point Hermitian codes. For
  q = 3 (n = 27) it lists [[27,1,19;16]], [[27,4,16;13]], [[27,6,13;9]], [[27,9,10;6]], [[27,13,7;4]], [[27,16,4;1]].
  Wherever d >= 12, c >= 9.
- https://arxiv.org/pdf/2207.05647 (Luo, Ezerman, Grassl, Ling, the table's source). Its qutrit Table 2 has [[28,9,12;9]]
  and [[30,0,12;0]]. Proposition 10 says a one-column extension raises the hull by 1 with d <= d' <= d+1. That is a
  technique, not this code.
- https://arxiv.org/html/2607.12242 (Lu, Yang, Liu, Fu, Guo, v3 14 Oct 2026). Extensions of cyclic codes for stabilizer
  codes; the qutrit entries include [[27,1,8]]_3 and [[42,16,8]]_3. Nothing on the route.
- https://arxiv.org/html/2605.23119 (Guo, Li, May 2026). EA codes with imperfect ebits: [[28,2,11;4]]_3 and
  [[28,2,13;6]]_3 (k = 2) in a different noise model. Nothing on the route.
- https://arxiv.org/html/2608.09886. EA quantum locally recoverable codes, including Hermitian specializations. My
  parse found no explicit qutrit parameter sets.
- https://arxiv.org/pdf/2405.15057 (Ezerman et al., IEEE TIT 2025). Its qutrit stabilizer codes include [[28,6,9]],
  [[31,3,10]], [[33,3,11]] and [[40,4,12]]. None is of the form [[28+j, >=j, >=12]].
- https://arxiv.org/html/2507.17319 and https://arxiv.org/html/2511.02813: no qutrit codes with n >= 24.
  https://arxiv.org/pdf/2412.13613: no codes of any q with n >= 26 and d >= 11. https://arxiv.org/pdf/2312.12288: qutrit [[n,0,d]] records only at n >= 51.
- https://www.researchsquare.com/article/rs-10009179/v1: maximal-entanglement EA codes (c = n - k), irrelevant at c = 6.
- https://link.springer.com/article/10.1007/s10773-026-06280-x (Zhang, Li, Xing, IJTP 2026): abstract only (paywalled).
  It reports six record-breaking ternary stabilizer codes; their parameters are not visible.
- https://globals.ieice.org/en_transactions/fundamentals/10.1587/transfun.2024EAP1055/_pdf (Li, Li, Guan, Lu, Song, Fu,
  IEICE E108.A(2), 2025): HTTP 405, an AWS WAF "Human Verification" page
  (sha256 348afbe433966840919c61d1010ed403d0514446b0e26ee6f533cd82c3e2bab2). Not retried and not fetched from a mirror.
- Search results only, not opened: Sok, Ezerman, Ling, arXiv:2512.17128 (rational AG codes; over GF(9) these have
  length <= 10); GRS and Reed-Solomon hull papers (also length <= 10 over GF(9)).

## 5. This repository and its pull requests

- `TROPHY_CASE.md`: 0 matches for eaqecc or qutrit.
- `known-knowns/eaqecc-qutrit-codetables-gaps/`: one entry, [[14,3,8;5]]_3, which is irrelevant here.
- `bank/proposed/`: no entry for this target.
- GitHub search API, one GET per term, all HTTP 200 (`fetched/github/FETCHLOG.txt`): terms eaqecc, qutrit, hermitian,
  entanglement-assisted and "28,6,12" (0 results). The matching PRs are #363 [[33,1,31;24]], #403 [[16,4,8;4]],
  #404 [[34,2,24;24]] and #405 [[33,3,23;24]] (all open), plus #331 [[14,3,8;5]] (closed). PR #614 is about AME and qudit
  codes with n <= 20 and d <= 11. Under the rules none reaches d >= 12 at (28,6,6): the c = 24 codes cannot lower
  c, and the others have d <= 8 or n too small.

## Caveats

- Two qutrit stabilizer-code papers were not readable (IJTP 2026 paywalled; IEICE 2025 blocked). Their abstracts are
  about c = 0 codes. They would undercut this claim only if they contain a code [[28+j, >=j, >=12]]_3 that allows
  increasing dimension, most plausibly a +1 record at [[28,0,12]]_3 or [[29,1,12]]_3. That would make this result a
  tie. I could not rule this out from what I could read.
- Not opened: Li, Li, Guan, Song (IJTP 2024, Hermitian self-orthogonal codes over F9), Li and Zhu (Discrete Math 2024)
  and Cao, Li, Zhu (IEEE TIT 2025). I saw them only through 2607.02170's comparisons, which show small n or large c.
  Hermitian self-orthogonal codes matter here only as a self-dual [28,14,12]_9, which would also raise codetables'
  [[28,0]]_3 entry, and it has not.
- The construction applies published ideas: one-point Hermitian codes (Christensen et al.) and the hull-raising
  one-column extension (Luo et al., Proposition 10). The specific code and parameters do not appear in any source I
  found. Any write-up should credit both.
- The maintainer may hold unpublished codes; the table last changed 10.07.2025.
- I did not re-verify d, k or c. That is the other skeptics' job, and this verdict assumes the claim's parameters are
  right.
- Search-engine coverage is incomplete, and Chinese-language journals were not searched.

pass: true
