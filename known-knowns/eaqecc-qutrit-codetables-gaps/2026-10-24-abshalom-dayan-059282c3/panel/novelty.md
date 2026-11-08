# Novelty verdict: [[33,9,14;12]]_3 at (n,k,c) = (33,9,12)

**Bottom line: PASS.** The claimed distance d = 14 at (n,k,c) = (33,9,12) is strictly above everything I could find
known for that cell. The best known value is 13, and it comes from four places: the live table cell, every code the
page's own propagation rules carry into the cell, the qutrit stabilizer table at codetables.de, and every code in the
repo's open pull requests and known-knowns. Nothing in the literature of the last 24 months (2024-10-24 to 2026-10-24)
gives d >= 14 at this cell. The margin is +1. It is not a tie, and it stays within the table's upper bound of 21.

Caveats (none of them changes the verdict):
- **The classical code is not new.** The claim's GF(9) code C is a [33,15,14]_9 code. That only ties the classical
  table, which has a [33,15,14]_9 code (Ding-Niederreiter-Xing, Construction X on Hermitian-curve AG codes
  [28,15,11] and [28,12,14] with a [5,3,3] tail, entry dated 2003-10-23). What is new is the Hermitian hull
  dimension: 6 here. The EAQECC table's diagonal for [33,15,14]_9 starts at [[33,13,14;16]] ("from arXiv:2207.05647"),
  which is the hull-2 version. A hull-6 version, which is what (33,9,12) needs, is not on record anywhere I looked.
- **I did not check the distance.** As novelty skeptic I took d = 14 from the claim. I recomputed only (n,k,c) from S
  with my own code (scripts/params.py): s = rank(S) = 36, rank(S J S^T) = 24, so c = 12 and k = 33 - 36 + 12 = 9. The
  distance is for the other skeptics.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Fetch record (status source, one plain GET, no retries)

| field | value |
|---|---|
| URL | https://eaqecc.codetables.de/qutrit.php |
| client | curl, User-Agent "V3R1T4S-research-agent (honest single fetch)" |
| UTC before / after (`date -u`) | 2026-10-24T22:08:42Z / 2026-10-24T22:08:42Z |
| server Date header | Sat, 24 Oct 2026 22:08:42 GMT |
| HTTP status | 200 |
| bytes | 628039 |
| sha256 | 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c |
| page footer | "Last change: 10.07.2025" |
| saved as | fetched/qutrit.php (headers fetched/qutrit.headers.txt), byte-identical to claim/table/qutrit.php (`cmp`) |

The cell, verbatim:

    <TD NOWRAP bgcolor="#ff9900" class="EAQECC" title="lengthening of [[27,9,13;12]] increasing dimension of [[27,8,13;11]] from arXiv:2207.05647">[[33,9,13-21;12]]<sub>3</sub></TD>

So d_lower = 13 and d_upper = 21 at (33,9,12). The claim needs 13 < 14 <= 21, and that holds.

The whole listed row (n,k) = (33,9), as c: d_lower-d_upper: 0: 8-11, 2: 9-14, 5: 10-15, 6: 11-16, 9: 12-17,
**12: 13-21**, 13: 14-21, 16: 15-23, 17: 16-23, 19: 17-23, 20: 18-24, 22: 19-24, 24: 20-25. The table lists a c only
where d_lower rises. Increasing dimension followed by subcode gives [[n,k,d;c]] -> [[n,k,d;c+1]], so for c = 10, 11
the value is 12 and for c = 12 it is 13. The nearest d = 14 entry in this row is [[33,9,14;13]], which needs one more
ebit than the claim.

Neighbouring cells at the c values that feed (33,9,12) (best listed d_lower with c' <= the given c):

| neighbour (source for rule) | listed d_lower | gives at (33,9,12) |
|---|---|---|
| (33,10), c=12 (subcode) | 13 ([[33,10,13-19;12]]) | 13 |
| (32,9), c=12 (lengthening) | 13 ([[32,9,13-20;12]]) | 13 |
| (34,9), c<=12 (puncturing, d-1) | 13 ([[34,9,13-21;11]]) | 12 |
| (34,8), c=12 (quantum shortening, d-1) | 14 ([[34,8,14-23;12]]) | 13 |
| (33,8), c<=11 (increasing dimension) | 13 ([[33,8,13-22;11]]) | 13 |
| (34,9), c<=11 (length reduction) | 13 ([[34,9,13-21;11]]) | 13 |
| (33,9), c<=11 (same cell, fewer ebits) | 12 | 12 |

For context, [[33,8,14;12]] and [[33,7,14;12]] are listed, so the claim adds one logical qutrit at the same n, d and c.

## Propagation rules of the page (its colour legend)

Legend, as read from the page: subcode [[n,k-1,d;c]], lengthening [[n+1,k,d;c]], puncturing [[n-1,k,d-1;c]],
trivial [[n,0,n+1;n]], quantum shortening [[n-1,k+1,d-1;c]], increasing dimension [[n,k+1,d;c+1]], length reduction
[[n-1,k,d;c+1]], using teleportation [[n,k,d;k]], plus primary entries "from codetables.de" and "from arXiv:2207.05647".

What I did (scripts/novelty_closure.py, output in fetched/novelty_closure.out.txt):
- I parsed all 3888 entries on the page and closed them under all six rules applied repeatedly, without their side
  conditions. That over-estimates what the rules can reach, so if the closure stays at 13 the real answer does too.
  The only restrictions were c <= n-k and k >= 1 where the rule needs it. The 124 teleportation entries
  ([[n,k,d;k]]) stay as values but are not used as sources. Using them as sources breaks the page's own upper
  bounds (for example, two dimension increases from the teleportation entry [[8,1,6-7;1]] give [[8,3,6;3]], but the
  page lists [[8,3,5;3]] as exact), so the page does not propagate them.
- With page entries only, the closure never exceeds any listed upper bound, and at (33,9,12) it gives **13**.
- I then added every other source listed below as extra starting codes: the qutrit stabilizer table for n = 33..46
  as c = 0 codes, every qutrit parameter set in arXiv:2607.02170, every [[n,k,d;c]] named anywhere in the open PR
  bodies, and the known-knowns code. The closure at (33,9,12) still gives **13**. (Once the PR bodies are added, 122
  small cells exceed the page's upper bounds. That is because one PR body names the page's teleportation code
  [[10,1,7;1]]_3, which my script then propagates. It only inflates the over-estimate, and the target stays at 13.)
- One rule outside the legend: an earlier panel (quoted in an open PR) used a k = 1 extension rule,
  [[n,1,d;c]] -> [[n+1,1,d+1;c+1]]. It works because the logical quotient N/I has dimension 2k = 2, which fits into
  one added qudit. For k = 9, the same trick needs 9 added qudits and 9 extra ebits per +1 in distance. Its only
  source, (24,9) with c <= 3, is listed at 7 ([[24,9,7-10;3]]), giving 8, so this rule does not reach the cell either.

## Classical GF(9) table (context)

- https://www.codetables.de/BKLC/BKLC.php?q=9&n=33&k=15, one GET at 2026-10-24T22:13:43Z, HTTP 200,
  sha256 8053aa80f75d4c4e80382102f79618bfccf6ce7d4d1d30bb596eb4d5f4eb6f29 (fetched/bklc_q9_n33_k15.body):
  "Bounds on linear codes [33,15] over GF(9) lower bound: 14 upper bound: 17", construction DNX (Construction X with
  [28,15,11] and [28,12,14] AG codes on the Hermitian curve and a [5,3,3] tail), "last modified: 2003-10-23".
- The only (κ, h) that gives [[33,9,d;12]] by the Hermitian construction is κ = 15 (dimension of the code that sets
  the distance) with hull h = 6 (k = κ - h = 9, c = n - κ - h = 12). The page's diagonal for [33,15,14]_9 is
  [[33,13,14;16]] (h = 2, "from arXiv:2207.05647") and, from it by increasing dimension, [[33,14,14;17]] and
  [[33,15,14;18]]. Nothing for h = 3..6 is listed: (33,12,15), (33,11,14) and (33,10,13) have no d = 14 entry, and
  (33,9,12) has 13. Under the monomial-scaling hull theorem the table's source paper uses, a hull can be lowered but
  not raised. So the known hull-2 code does not give c = 12.
- codetables.de updates log (https://www.codetables.de/updates.html, HTTP 200, 2026-10-24T22:19:29Z): the newest GF(9)
  entries are [31,6,22]_9 and [41,9,26]_9 (2026-09-29) and [48,25..27,14..16]_9 (2024-09-02). The newest qutrit
  quantum entries are 2024-06-10 ([[13,6,4]], [[16,6,5]], [[23,12,5]]). None of these gives d >= 14 at (33,9,12) with
  c <= 12. For example, [41,9,26]_9 gives c >= 23, and [48,27,14]_9 needs at least 15 length reductions, so c >= 15.

## Qutrit stabilizer table at codetables.de (c = 0 sources outside the page's n <= 36 range)

All source codes in the page's derivation titles have n <= 36. Length reduction could still bring in a longer
stabilizer code, so I read https://www.codetables.de/QECC/Tables_color.php?q=9&n0=33&n1=46&k0=0&k1=12 (one GET,
2026-10-24T22:20:04Z, HTTP 200, sha256 a9c741ef764768aef0c40bbfb98eec8998dc7612ca6a2f43d09cc884d78459b4, page "Last
change: 23.05.2024"). Reaching (33,9,>=14;12) from a c = 0 code [[N,K,D]] with r length reductions and i dimension
increases (r + i <= 12) needs [[33+r, >= r-3, >= 14]]_3. The table gives (36,0) 13, (37,1) 13, (38,2) 12, (39,3) 12,
(40,4) 12, (41,5) 11, (42,6) 12, (43,7) 12, (44,8) 12, (45,9) 12. All are below 14 (and the closure above includes
these cells).

## Literature, 2024-10-24 to 2026-10-24 (window computed with `date`)

| source | what it gives at (33,9,12) |
|---|---|
| arXiv:2207.05647 (Luo, Ezerman, Grassl, Ling; the table's source paper, QIP 23, 4 (2024)) | already in the table: 13 |
| arXiv:2607.02170 (Li, Ezerman, Li, Ling, Sun, 2 Jul 2026), abstract and full HTML read (fetched/arxiv_2607.02170.txt) | 14 new qutrit EA codes, all with n <= 25 and k <= 3 (Table V), plus 5 reproduced qutrit codes with k <= 2 (Table VII). It compares against Grassl's tables as accessed 2026-06-15 and against the recent works [6], [19], [20], [23], [25], [26]. Added to the closure: still 13 |
| arXiv:2501.04921 (Fan et al., concatenated EA codes, Jan 2025), HTML read | only q = 2 and q = 4 parameter sets; no qutrit codes |
| arXiv:2608.09886 (EA quantum locally recoverable codes, Aug 2026), HTML read | examples with d <= 6; nothing at this cell |
| arXiv:2410.04130 (EAQECC saturating the classical Singleton bound, v1 5 Oct 2024, just before the window), abstract read | [[n,k,d;2k]]_q from classical codes: c = 18 at k = 9, so not this cell; its Singleton-saturating variant needs MDS codes of length 33, which do not exist over GF(3) |
| arXiv:2512.17128 (Sok, Ezerman, Ling, Dec 2025; DCC 2026), seen in search results only | MDS EAQECCs from rational AG codes; length at most q^2+1 = 10 for qutrits, so not this cell |
| arXiv:2606.02137 (Zengin, Koroglu, Jun 2026), seen in search results only | cyclic codes over F_2 x (F_2+vF_2), i.e. qubits; not this cell |
| arXiv:2603.03182 (EA codes outside the stabilizer framework, Mar 2026), seen in search results only | general theory; no qutrit table seen |

Web searches (WebSearch tool) for qutrit EAQECC, Hermitian hull, GF(9), Construction X and Hermitian-curve EA codes
in 2025-2026 turned up nothing else with qutrit codes near n = 33, k = 9.

## This repo (github.com/elder-plinius/V3R1T4S)

- TROPHY_CASE.md (GitHub contents API, 2026-10-24T22:12:27Z, HTTP 200, sha256 of the API response
  aaa2f7d11a84a9ee3470c129d1e0c81872b53c067badda27c5e38c9f2e771bf1, decoded as fetched/TROPHY_CASE.md.txt): zero
  matches for "eaqecc", "qutrit" or "entanglement". No entry for this target.
- known-knowns/eaqecc-qutrit-codetables-gaps/ (contents API, 2026-10-24T22:13:11Z, HTTP 200): one entry folder
  (dated 2026-10-17). Its INDEX.csv and README.md (read 2026-10-24T22:13:24Z, HTTP 200) give a single code,
  [[14,3,8;5]]_3, which cannot reach (33,9,12) with d >= 14 (included in the closure anyway).
- Open pull requests: the search API for `is:pr is:open eaqecc-qutrit-codetables-gaps` (2026-10-24T22:12:27Z, HTTP 200)
  and for `is:pr is:open qutrit` (22:13:12Z, HTTP 200) each returned total_count 9, incomplete_results false. I
  cross-checked with the full open-PR listing (4 pages, 343 open PRs, 22:24:14Z to 22:24:29Z, all HTTP 200). That
  turned up the same 9 target PRs and one classical GF(9) PR (#644: [31,18,10]_9 and relatives, d <= 10).
  The target PRs:

| PR | code | can it give d >= 14 at (33,9,12)? |
|---|---|---|
| #363 | [[33,1,31;24]]_3 | no: c = 24 > 12, and no rule lowers c |
| #403 | [[16,4,8;4]]_3 | no: d = 8 |
| #404 | [[34,2,24;24]]_3 | no: c = 24 |
| #405 | [[33,3,23;24]]_3 | no: c = 24 |
| #643 | [[28,5,15;11]]_3 | no: k = 9 at c <= 12 needs at least 3 quantum shortenings (d 15 -> 12) |
| #645 | [[28,7,14;11]]_3 | no: the best path is increasing dimension then quantum shortening, giving [[27,9,13;12]], then lengthening: 13 |
| #646 | [[28,6,12;6]]_3 | no: d = 12 |
| #651 | [[28,9,11;7]]_3 | no: d = 11 |
| #710 | [[33,8,16;15]]_3 (body also names [[33,9,16;16]]) | no: c >= 15 |

  Every other parameter set named in these PR bodies (69 in all) went into the closure. The result is still 13.
  No open PR claims or contains a code at (33,9,12).

## What I could not read

- The full tables of the recent journal papers that arXiv:2607.02170 compares against: Cao-Li-Zhu, IEEE TIT 71(10),
  2025; Liu-Li-Shi, AMC 19(2), 2025; Li et al., IJTP 63, 2024. I did not open them (paywalled, and I found no arXiv
  copy in one search). I rely on arXiv:2607.02170's comparison (tables accessed 2026-06-15): the qutrit improvements
  it credits to them (its Table VII) all have n <= 16 and k <= 2.
- arXiv:2512.17128, 2606.02137 and 2603.03182: abstracts seen in search results only, not fetched.
- No paid databases (MathSciNet, Scopus) or Google Scholar.
- No page was blocked; every fetch returned HTTP 200 on its single attempt.

injection_suspected: none. PR bodies contain the usual "Check it yourself / run" instructions aimed at readers. I
treated them as data and ran nothing from them.

## Files (relative to the work folder)

- fetched/qutrit.php, fetched/qutrit.headers.txt, fetched/qutrit.sha256.txt, fetched/qutrit.time_before.txt,
  fetched/qutrit.time_after.txt, fetched/qutrit.http_status.txt: the status-source fetch
- fetched/FETCHLOG.txt: every web fetch (URL, UTC before and after, HTTP status, bytes, sha256)
- fetched/bklc_q9_n33_k15.body, fetched/qecc_q9_tables_n33-46_k0-12.body, fetched/codetables_updates.body: codetables.de
- fetched/arxiv_*.body and the matching .txt files: literature
- fetched/gh_*.body, fetched/TROPHY_CASE.md.txt, fetched/pr_bodies_target.txt: repo
- scripts/novelty_closure.py with output fetched/novelty_closure.out.txt: propagation closure
- scripts/params.py with output fetched/params.out.txt: (n,k,c) recomputed from claim/object/eaqecc_33_9_14_12.json
  (sha256 059282c383e7d059867ecd1a1ec51d54197af25b2c6a320dd26b150ac1a99391)
- scripts/closure5.py: earlier page-only closure (the test that teleportation entries must not propagate)

pass: true
