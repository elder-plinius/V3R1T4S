# Novelty verdict: [[28,7,13;9]]_3 at (n,k,c) = (28,7,9)

**Bottom line: novel.** Nothing I could find reaches d >= 13 at (28,7,9). That covers the live cell itself (d_lower 12, d_upper 18), every code the page's own propagation rules carry into this cell from the other listed cells, the literature I could read from the last 24 months (plus the older one-point Hermitian family the claim names), and the V3R1T4S repo (TROPHY_CASE.md, known-knowns/, and all open pull requests for this target). The best known value is 12, and the claimed d = 13 is strictly above it, so this is not a tie. It also stays within the cell's upper bound: 12 < 13 <= 18.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Fetch record (status source)

- URL: https://eaqecc.codetables.de/qutrit.php
- One plain GET with curl, User-Agent "V3R1T4S-research-agent (honest single fetch)", no retries.
- UTC time (`date -u` before and after): 2026-10-25T00:25:05Z to 2026-10-25T00:25:05Z. Response header `date: Sun, 25 Oct 2026 00:25:05 GMT`.
- HTTP status: 200. Size: 628039 bytes.
- sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c. This is byte-identical to the claim's copy, claim/table/qutrit.php (checked with `cmp`).
- Page footer: "Last change: 10.07.2025".
- Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt, fetched/qutrit.time_before.txt, fetched/qutrit.time_after.txt, fetched/qutrit.http_code.txt and fetched/qutrit.sha256.txt.
- The cell, verbatim:
  `<TD NOWRAP bgcolor="#ff6600" class="EAQECC" title="subcode of [[28,9,12;9]] from arXiv:2207.05647">[[28,7,12-18;9]]<sub>3</sub></TD>`
  So d_lower = 12 and d_upper = 18.

## Sources checked, and what each gives at (28,7,9)

| source | best d at (28,7,9) it gives |
|---|---|
| live cell | 12 |
| page's six propagation rules plus the trivial rule, closed over all 3888 listed cells (teleportation cells excluded, see below) | 12 |
| the same closure plus every code named in the repo's open and closed EAQECC pull requests, its known-knowns entry, and the author's unfiled codes | 12 |
| the same, plus the whole length-27 one-point Hermitian family of arXiv:2105.02166 (all pole orders m), plus the qutrit codes of arXiv:2607.02170 | 12 |
| claim | 13 |

### 1. The cell's neighbours on the live page

These are row n = 28, k = 7, written as c: d_lower-d_upper, read from fetched/qutrit.php:

0: 8-10; 1: 9-12; 5: 10-14; 7: 11-15; **9: 12-18**; 11: 13-19; 12: 14-19; 14: 15-20; 15: 16-20; 17: 17-21; 19: 18-21; 21: 19-22.

Every cell that can feed (28,7,9) in one step of the rules holds 12 or less:

| neighbour (n,k,c) | value | rule into (28,7,9) |
|---|---|---|
| (28,8,9) | 12 | subcode |
| (28,9,9) | 12 | subcode |
| (27,7,9) | 12 | lengthening |
| (28,6,8) | 12 | increasing dimension |
| (29,7,8) | 12 | length reduction |
| (29,7,9) | 12 (not listed separately; it is the c = 8 entry) | puncturing |
| (29,6,9) | 12 (not listed separately; it is the c = 7 entry) | quantum shortening |

The first d >= 13 in this row is at c = 11. No rule on the page lowers c.

### 2. The page's own propagation rules

I wrote my own parser and closure, in scripts/parse_table.py and scripts/closure.py. They read all 3888 cells and iterate the legend's rules to a fixed point:

- subcode: [[n,k-1,d;c]]
- lengthening: [[n+1,k,d;c]]
- puncturing: [[n-1,k,d-1;c]]
- quantum shortening: [[n-1,k+1,d-1;c]]
- increasing dimension: [[n,k+1,d;c+1]]
- length reduction: [[n-1,k,d;c+1]]
- trivial: [[n,0,n+1;n]]

The closure gives 12 at (28,7,9), the same as the listed value. My closure is in fact slightly more generous than the page: at a few other cells it exceeds the listed d_lower, at (22,11,11), (33,2,24), (33,3,24), (34,2,24) and some k = 0 cells. Even so, it still gives 12 here.

The "using teleportation" cells are 124 cells, all with c = k and k <= 8. If I seed them in as well, (28,7,9) rises to 24, but the same seeding pushes 2700 listed cells above their own d_upper. So they belong to a different resource model, and the page does not propagate them. This agrees with what the claim says.

### 3. The V3R1T4S repo

All requests were unauthenticated GETs to the GitHub REST API, one per query. All returned HTTP 200, and the log is in fetched/github_fetch_log.txt.

- **TROPHY_CASE.md** (fetched 2026-10-25T00:27:49Z, file sha 571f2411...): no EAQECC or qutrit row at all.
- **known-knowns/eaqecc-qutrit-codetables-gaps/**: a single entry, 2026-10-17-anzal1-7b890c6f, which is [[14,3,8;5]]_3. It is far from (28,7,9) and adds nothing at this cell.
- **Open pull requests for target eaqecc-qutrit-codetables-gaps**: the search `is:pr is:open eaqecc-qutrit-codetables-gaps` at 2026-10-25T00:27:50Z returned total_count 9, incomplete_results false:
  - #363 [[33,1,31;24]]
  - #403 [[16,4,8;4]]
  - #404 [[34,2,24;24]]
  - #405 [[33,3,23;24]]
  - #643 [[28,5,15;11]]
  - #645 [[28,7,14;11]]
  - #646 [[28,6,12;6]]
  - #651 [[28,9,11;7]]
  - #710 [[33,8,16;15]]

  This is exactly the list given in CLAIM.md. Two wider searches (`is:open qutrit`, and `eaqecc` in any state) found the same nine plus the closed #331, which is [[14,3,8;5]]. I pulled out every [[n,k,d;c]] that appears in any of these PR bodies (47 codes, saved in pr_codes.json). That includes [[27,6,13;9]] and [[28,11,11;9]], which are mentioned in #646 and #651. I seeded all of them into the closure, together with the author's unfiled [[33,7,15;12]], [[33,9,14;12]] and [[33,3,20;18]]. The result at (28,7,9) is still 12. Every PR code with d >= 13 has c >= 10 at n <= 28, or sits at n = 33/34 with c >= 12, and the rules never lower c.

### 4. Literature

- **arXiv:2105.02166**, Christensen, Munuera, Pereira, Ruano (2021), read once as HTML. It gives one-point Hermitian EA codes at length 27 only. Its q = 3 examples include [[27,6,13;9]], [[27,4,16;13]] and [[27,9,10;6]].
  - I recomputed the whole family myself (scripts/cmpr_family.py) by computing the Hermitian hull of C(m) for every m. My values match all six of the paper's printed q = 3 examples.
  - The members that could matter here are [[27,4,14;9]], [[27,6,13;9]], [[27,6,12;7]] and [[27,7,11;6]]. With their designed distances they leave (28,7,9) at 12.
  - Those members would lift the cell only if their EA distance were above the designed distance. To rule that out, scripts/cmpr_lowweight.py constructs codewords from products of lines, and for each m = 13, 14, 15, 16 it finds one of exactly the designed weight (14, 13, 12, 11) outside the Hermitian hull. So those EA distances are exact.
  - The family has no member at k = 7 with c <= 9 and d >= 13.
- **arXiv:2207.05647**, Luo, Ezerman, Grassl, Ling (the table's source): the HTML URL returned 404 (no HTML version), so I did not read the paper. Its codes are on the table, for example [[28,9,12;9]] from a [28,14,12]_9 code with hull 5, and [[28,10,13;12]].
- **arXiv:2607.02170**, Li, Ezerman, Li, Ling, Sun (July 2026), read once as HTML. Its new qutrit codes stop at n <= 25 (Table V), and Table VII adds a few more reproduced ones. All are seeded into the closure, with no effect: none has both d >= 13 and c <= 9.
- **arXiv:2501.04921** (concatenated EA codes, 2025): qubit only.
- **arXiv:2512.17128** (Hermitian hulls of rational AG codes, Dec 2025): this covers MDS codes, which over GF(9) have length <= 10 and so d <= 11. Not relevant here.
- **Web searches**: six queries, including the exact string "[[28,7,13;9]]", turned up no qutrit EA code at length 27 to 30 with these parameters.
- **A general argument against the rest**: a code with maximal entanglement (c = n - k) and c <= 9 has d <= 10 by the EA Singleton bound. So the LCD and quasi-cyclic papers I found cannot reach this cell.

### 5. The classical GF(9) table at codetables.de

One GET per cell; log in fetched/bklc_fetch_log.txt.

| code | bounds | construction listed |
|---|---|---|
| [28,13]_9 | 13 to 14 | AG code on the Hermitian curve, 2003 |
| [27,13]_9 | 12 to 13 | shortening of [28,14,12] |
| [28,14]_9 | 12 to 13 | AG code on the Hermitian curve |

So the classical [28,13,13]_9 code is long known. What is new is the version with Hermitian hull 6. I recomputed that hull myself for the extended code E_15: hull 6, which gives [[28,7,>=13;9]]. The table's source paper evidently worked from a version with hull 3, since the table shows [[28,10,13;12]]. A GF(9)-linear code at d = 14 here would need a [28,13,14]_9 code, and none is known.

## What I could not read

- arXiv:2207.05647 as HTML (HTTP 404; I did not try another route). Its results are reflected on the table itself.
- The full text of Cao, Li, Zhu, "Classical codes and quantum codes involving the σ inner product" (IEEE TIT 2025). I could not locate it. Its qutrit codes quoted in arXiv:2607.02170 Table VII ([[7,0,7;5]], [[16,2,14;14]]) are seeded.
- I did not open the journal-only papers Li-Li-Guan-Song (IJTP 2024), Li-Zhu (DM 2024) or Liu-Li-Shi (AMC 2025). Their qutrit codes that arXiv:2607.02170 cites are seeded, and they are far from this cell.
- injection_suspected: none noticed in the pages or PR bodies I read.

## Scope note

This verdict covers novelty only. I did not re-verify d = 13 itself; that is the reproduce skeptic's job. I checked only that the claimed parameters fit the cell: s, c and k follow from the hull-6 construction, and 12 < 13 <= 18.

pass: true
