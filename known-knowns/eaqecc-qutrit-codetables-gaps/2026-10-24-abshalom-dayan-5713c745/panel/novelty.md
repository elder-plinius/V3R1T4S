# NOVELTY skeptic: [[33,7,15;12]]_3 at (n,k,c) = (33,7,12)

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Bottom line

**Novel: d = 15 strictly beats everything known that I could find at (33,7,12).** The best known value is 14, from
four sources:
- the live cell (d_lower 14);
- every code the page's own propagation rules carry into this cell from listed cells (at most 14);
- the open pull requests for this target (at most 14, a tie at best, via the lengthened [[28,7,14;11]]_3 of PR #645);
- the last 24 months of literature I could read (nothing at this cell; nothing that propagates to d >= 15 with
  c <= 12).

TROPHY_CASE.md and known-knowns/ hold nothing for this cell. Also 15 <= d_upper = 23.

One caveat on what is new. The classical [33,14,15]_9 code type is not new: codetables.de has listed [33,14] over
GF(9) at 15-18 since 2003, built by the same Construction X from Hermitian-curve AG codes. What is new is a version
with Hermitian hull dimension 7, which is what this cell needs. The table's own [33,14,15]_9-type entries stop at
hull 2 ([[33,12,15;17]]_3, from arXiv:2207.05647). Every cell that hull 3 to 7 would reach is listed at 14.

## Fetch record (status page, one plain GET, no retry)

- URL: https://eaqecc.codetables.de/qutrit.php
- Client: curl, User-Agent "V3R1T4S-research-agent (honest single fetch)"
- UTC before: 2026-10-24T21:14:39Z. UTC after: 2026-10-24T21:14:40Z. Server Date header: Sat, 24 Oct 2026 21:14:39 GMT.
- HTTP status: 200. Size: 628039 bytes.
- sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is byte-identical to claim/table/qutrit.php,
  which the claim fetched at 2026-10-24T19:55:15Z. Page footer: "Last change: 10.07.2025".
- Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt, fetched/qutrit.status.txt,
  fetched/qutrit.time_before.txt, fetched/qutrit.time_after.txt and fetched/qutrit.sha256.txt.
- The cell, verbatim:
  `<TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,7,14;12]] from arXiv:2207.05647">[[33,7,14-23;12]]<sub>3</sub></TD>`
  This gives d_lower = 14 and d_upper = 23.
- The whole listed row n = 33, k = 7 (c: d_lower-d_upper): 0: 9-12; 3: 10-15; 4: 11-16; 7: 12-20; 10: 13-23;
  **12: 14-23**; 14: 15-24; 15: 16-24; 17: 17-25; 19: 18-25; 21: 19-26; 22: 20-26; 24: 21-26; 26: 22-27.
  No c <= 12 in this row reaches 15. The first 15 is at c = 14.

## Sources checked and what each gives at (33,7,12)

| source | what it gives at (33,7,12) |
|---|---|
| live cell | 14 |
| page's legend rules, one step from the listed neighbours | 14 |
| page's legend rules, full closure over all 3888 listed cells | 14 |
| codetables.de BKLC [33,14] over GF(9) (context) | classical [33,14,15]_9 is known (lower 15, upper 18); its hull is not given |
| this repo's TROPHY_CASE.md | no EAQECC or qutrit entry |
| this repo's known-knowns/eaqecc-qutrit-codetables-gaps/ | one package, [[14,3,8;5]]_3; it does not reach this cell |
| open PRs for this target (9), with every code in their bodies | at most 14 |
| closed or merged PRs for this target (1, #331) | [[14,3,8;5]]_3 (the known-knowns package); does not reach |
| arXiv, last 24 months, plus web search | nothing at this cell; nothing propagates to d >= 15 with c <= 12 |

### Page propagation rules (its colour legend)

The legend's rules are: subcode [[n,k-1,d;c]], lengthening [[n+1,k,d;c]], puncturing [[n-1,k,d-1;c]], quantum
shortening [[n-1,k+1,d-1;c]], increasing dimension [[n,k+1,d;c+1]], length reduction [[n-1,k,d;c+1]],
teleportation [[n,k,d;k]] and trivial [[n,0,n+1;n]].

One step into (33,7,12) from the listed cells:
- subcode from (33,8,12) = 14-22 gives 14;
- lengthening from (32,7,12) = 14-23 gives 14;
- puncturing from (34,7,12) = 14-24 gives 13;
- quantum shortening from (34,6,12) = 14-26 gives 13;
- increasing dimension from (33,6,11) and length reduction from (34,7,11): neither cell is listed. An unlisted c
  takes the next lower listed c, and taking the maximum over all c' <= 12 covers both.

Full closure (scripts/closure3.py, run on all 3888 parsed cells):
- Repeated application of all six rules gives 14 at (33,7,12), and at most 14 for every c' <= 12.
- Constraint used: c <= n - k for every valid cell.
- Teleportation cells are allowed only as sources for lengthening and puncturing. This is a modelling choice. A
  first, naive closure that let quantum shortening act on the teleportation cell [[36,1,27;1]]_3 produced
  impossible values (d = 21 at c = 1). The page itself does not apply its rules that way: I counted many cells
  where the naive rules would exceed the listed value. So I treated that as an artefact of my script, not as
  information about the page.
- Without quantum shortening, the result is the same (14).

### Classical GF(9) context (one GET)

- URL: https://www.codetables.de/BKLC/BKLC.php?q=9&n=33&k=14
- Fetched 2026-10-24T21:17:37Z, HTTP 200, sha256 4fb29f1e28aeb6a210f5e952ced51877d9fca9546f4a1c2dd9e1119cd3926c36
  (fetched/bklc_9_33_14.html).
- It gives "lower bound: 15 upper bound: 18". Construction type DNX (Ding, Niederreiter, Xing 2000): Construction X
  using [28,14,12] and [28,11,15] AG codes from the Hermitian curve (divisors of degree 3 and 4) and a [5,3,3] code.
- Bearing on the cell: the claim's classical code C ([33,14], d = 15) ties the classical record and uses the same
  construction. The quantum cell needs that code at Hermitian hull dimension exactly 7, which gives
  k = 14 - 7 = 7 and c = 19 - 7 = 12.
- No [33,14,16]_9 is known, so no larger-distance classical code of this dimension is on record.
- The page gives no hull dimension. What the qutrit table shows is that the [33,14,15]-type codes it used stop at
  hull 2:
  - (33,12,17), hull 2: 15
  - (33,11,16), hull 3: 14
  - (33,10,15), hull 4: 14
  - (33,9,14), hull 5: 14
  - (33,8,13), hull 6: 14
  - (33,7,12), hull 7: 14

### This repository (https://github.com/elder-plinius/V3R1T4S, GitHub REST API, one GET per query)

All saved in fetched/gh/ (fetchlog.txt has URL, UTC time, HTTP status and sha256 for each).

- **TROPHY_CASE.md**, contents API, 2026-10-24T21:18:14Z, HTTP 200. The decoded file's sha256 is
  b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It has no line matching eaqecc, qutrit or
  entangle. The families listed are degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer,
  VNN-COMP, RobustBench and cipher commitments.
- **known-knowns/**, 2026-10-24T21:18:14Z, HTTP 200. Folder eaqecc-qutrit-codetables-gaps/ holds one package,
  2026-10-17-anzal1-7b890c6f. Its INDEX.csv (fetched 2026-10-24T21:18:46Z, HTTP 200) has the single row
  [[14,3,d;5]]_3, value 8, table 7. Nothing at n >= 27 or c <= 12 with d >= 15, so it does not reach (33,7,12).
- **Open pull requests.** I ran three search queries at 2026-10-24T21:19:03Z to 21:19:04Z, all HTTP 200:
  `is:pr is:open eaqecc-qutrit-codetables-gaps`, `... qutrit` and `... eaqecc`. All three return the same 9 open
  PRs (incomplete_results false). Every code in their titles and bodies, whoever filed it, was treated as known:
  - #363: [[33,1,31;24]]
  - #403: [[16,4,8;4]]
  - #404: [[34,2,24;24]]
  - #405: [[33,3,23;24]]
  - #643: [[28,5,15;11]], plus [[28,6,15;12]], [[29,5,15;11]], [[28,4,17;14]] and [[28,5,16;13]] in its body
  - #645: [[28,7,14;11]], plus [[28,6,14;10]], [[29,7,14;11]] and [[28,7,14;12]]
  - #646: [[28,6,12;6]] and relatives, d <= 13
  - #651: [[28,9,11;7]] and relatives, d <= 12
  - #710: [[33,8,16;15]], plus [[33,9,16;16]], [[33,11,16;18]], [[34,8,16;15]] and [[36,8,16;15]]
- **Why none reach 15 here.** No legend rule lowers c and none raises d, so a source needs c <= 12 and d >= 15:
  - #363, #404, #405 and #710 all have c >= 15.
  - The only PR codes with d >= 15 and c <= 12 are [[28,5,15;11]], [[29,5,15;11]] and [[28,6,15;12]]. Raising k to 7
    without losing distance takes "increasing dimension" steps, which push c to 13 or more.
  - The closure with table plus PR codes (scripts/closure_pr.py) gives **14** at (33,7,c <= 12). That is reached
    by lengthening PR #645's [[29,7,14;11]], so it is a tie with the table, not 15.
- **All states** (`is:pr eaqecc-qutrit-codetables-gaps`, 2026-10-24T21:20:11Z, HTTP 200): 10 PRs. The tenth is #331,
  closed and merged 2026-10-19, [[14,3,8;5]]_3, the known-knowns package above.

### Literature, last 24 months (2024-10-24 to 2026-10-24)

arXiv API queries, all sorted by submission date and saved in fetched/lit/ (fetchlog.txt has URL, time, status and
sha256). The http URLs answered 301, a redirect to https rather than a block. Each https query then returned
HTTP 200 at 21:20:34Z to 21:24:45Z:
- arxiv1: "entanglement-assisted" with qutrit, ternary or GF(9)
- arxiv2: "entanglement-assisted" with "Hermitian hull"
- arxiv3: "entanglement-assisted" with algebraic geometry or Hermitian curve
- arxiv4: a broad sweep of 261 EA-code abstracts. I read every title from the window.
- arxiv5: citations of 2207.05647 and codetables
- arxiv6, arxiv7: title lookups for two cited journal papers. Both returned 0 results.

What the window gives at (33,7,12):

- **arXiv:2607.02170** (Li, Ezerman, Li, Ling, Sun, 2 Jul 2026, "Generalized Extended Codes with Applications in
  Entanglement-Assisted Qubit and Qutrit Codes"). This is the newest paper that improves qutrit cells against this
  table. I read its full HTML: https://arxiv.org/html/2607.02170v1, 2026-10-24T21:22:04Z, HTTP 200, sha256
  f2e6c89124eeb8dac655c24dc47bb195a4a215abd2bca2d12ac497e7473a18e1.
  - Table V has 14 qutrit codes, all of length at most 25.
  - The ones with d >= 15 all have c >= 15: [[17,2,15;15]], [[18,2,16;16]], [[19,2,17;17]], [[19,3,15;16]],
    [[21,2,18;19]], [[22,2,19;20]], [[23,2,20;21]], [[24,2,21;22]], [[25,2,22;23]] and [[25,3,20;22]].
  - Table VII qutrit entries: [[7,0,7;5]], [[7,2,5;3]], [[9,0,9;7]], [[15,2,13;13]] and [[16,2,14;14]].
  - Added to the closure, none of its 29 qutrit parameter sets reaches d >= 15 at (33,7,c <= 12). The maximum stays 14.
- **Recent works that 2607.02170 compares its qutrit codes against**:
  - Cao, Li and Zhu, IEEE Trans. Inf. Theory 71(10), Oct 2025 (σ inner product)
  - Liu, Li and Shi, Adv. Math. Commun. 19(2), 2025 (building-up construction; quaternary codes of length <= 13)
  - Li, Li, Guan and Song, Int. J. Theor. Phys. 63(9), 2024 (Hermitian self-orthogonal codes over F9; Sep 2024, at
    the edge of the window)

  Their qutrit codes, as cited there, are short or need high entanglement: [[7,0,7;5]], [[16,2,14;14]],
  [[7,2,5;3]], [[9,0,9;7]]. I could not read these three journal papers in full; see the last section.
- **Constructions that cannot reach this cell.**
  - MDS or near-MDS families over GF(9) are limited to length about 10, or about 16 for elliptic curves. This covers
    GRS, twisted GRS (2607.03802), generalized Roth-Lempel (2609.20453, 2603.16187), rational AG (2512.17128),
    GRS EAQMDS (2507.18361) and iso-dual elliptic (2502.02033). At those lengths, d >= 15 and c <= 12 violate the
    EA Singleton bound.
  - Maximal-entanglement families have d <= c + 1 <= 13 when c <= 12, because c = n - κ and Singleton gives
    d <= n - κ + 1. This covers Hermitian LCD quasi-cyclic codes (2609.31300, lengths <= 30) and constacyclic
    3-design codes (2605.05613).
- **Out of scope**: binary or ring codes (2606.02137), QLDPC families (2608.16761, 2601.08927), locally recoverable
  EA codes (2607.27091, 2608.06854, 2608.09886, 2608.17118, 2609.23316, 2610.23889), theory papers (2411.14389,
  2412.16082, 2501.15465, 2603.03182, 2605.23119, 2609.36273), and concatenated codes (2501.04921).
- **Web searches** (WebSearch tool):
  - `"[[33,7,15;12]]" entanglement-assisted`: no hit for these parameters.
  - A query on new qutrit EA codes against Grassl's table in 2025/2026: only 2607.02170, whose qutrit lengths stop
    at 25.
  - A query on AG, Hermitian curve, degree-3 place and Construction X with EA: no EA paper combining them.
  - A query on qutrit EA codes of length 33 over GF(9): nothing.

## Light sanity check of the cell (not my role, done only to confirm which cell is being compared)

Run on claim/object/eaqecc_33_7_15_12.json (sha256 5713c745e8e837dc41e1883a120488fb38dce3b4254292335ca98f99a1787256),
with outputs in run/:
- `checkers/gf9info.py prep` printed `n=33 s=38 c=12 k=7 dim_N=28 dim_I=14 N_closed_under_w=True`, `kappa=14`.
- `checkers/bz64.c` printed `K=14 n=33 d=15 sets=14,14,3,2 maxw=7 words=4027269016` (11.44 s, max RSS 1458176 bytes).
- Both witness tools printed a weight-15 vector outside the isotropic part (`in_isotropic_part=False`,
  `in_span_S=False`).

So the object sits at (33,7,12) with d = 15 by these tools. The exact proof of d is the other skeptics' check.

## What I could not read or did not cover

- Full texts of journal-only papers: Cao, Li and Zhu (IEEE TIT 2025), Liu, Li and Shi (AMC 2025), Li, Li, Guan and
  Song (IJTP 2024), and Campion and San-José (QIP 2026, GRS EAQMDS). For these I relied on abstracts, search
  snippets, and the codes 2607.02170 cites from them.
- Most other arXiv papers were judged from their abstracts only. Journal papers with no arXiv version may be missed.
- No literature older than 24 months was searched systematically. The table's own sources (codetables.de and
  arXiv:2207.05647) are already in the cell value.
- Open issues that are not PRs, and branches, were not searched.
- injection_suspected: none. No fetched page or PR body tried to give instructions.

## Note for the panel (not part of the verdict)

Applied to this code, the page's "increasing dimension" rule gives d = 15 at (33,8,13), (33,9,14) and so on. The
table lists 14 at those cells, from (33,8,12), (33,9,13) and so on. This claim does not claim those cells.

pass: true
