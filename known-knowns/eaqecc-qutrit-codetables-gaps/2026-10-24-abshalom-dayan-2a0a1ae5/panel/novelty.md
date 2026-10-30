# Novelty verdict: [[28,9,11;7]]_3 at (n,k,c) = (28,9,7)

**Bottom line: novelty: PASS.** I fetched the live qutrit table once. It still lists `[[28,9,10-14;7]]_3`, so
d_lower = 10 and d_upper = 14. Nothing else I could find gives d >= 11 at (28,9) with c <= 7. I checked the cell
itself, the rest of its row, every chain of the page's own propagation rules (its colour legend) applied to the whole
table, the seven open V3R1T4S pull requests for this target, the repo's TROPHY_CASE.md and known-knowns/ folder, the
last 24 months of arXiv, and the codetables.de stabilizer and GF(9) pages that feed this cell. The claimed d = 11
is strictly above the best known value (10), and 11 <= 14. This is not a tie.

This verdict covers novelty only. It assumes the claimed d = 11 is right. I did not re-derive d; the other two
skeptics check that. I did recompute the cell's identity from S with my own code (scripts/params_from_S.py):
n = 28, s = rank(S) = 26, rank(S J S^T) = 14, so c = 7 and k = 9.

context: subagent (Claude Agent tool, model claude-opus-5-5), given only claim/

## Fetch record (status source, one plain GET, no retries)

- URL: https://eaqecc.codetables.de/qutrit.php
- Client: curl, User-Agent "V3R1T4S-research-agent (honest single fetch)"
- UTC before: 2026-10-24T17:16:20Z. UTC after: 2026-10-24T17:16:21Z. Server Date header: Sat, 24 Oct 2026 17:16:20 GMT.
- HTTP status: 200. Size: 628039 bytes.
- sha256: 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c
- Page footer: "Last change: 10.07.2025"
- Byte-identical to the claim's copy claim/table/qutrit.php (`cmp` reports no difference; same sha256 as claim/table/RECORD.md).
- Saved as fetched/qutrit.php, with fetched/qutrit.headers.txt, fetched/qutrit.time_before.txt, fetched/qutrit.time_after.txt, fetched/qutrit.http_code.txt and fetched/qutrit.sha256.txt.
- The cell, verbatim (it occurs exactly once on the page):

  `<TD NOWRAP bgcolor="#0099ff" class="EAQECC" title="increasing dimension of [[28,2,10;0]] from codetables.de">[[28,9,10-14;7]]<sub>3</sub></TD>`

- The full listed row (n,k) = (28,9), shown as c: d_lower-d_upper. I parsed all 3888 entries on the page into fetched/qutrit_cells.json:
  0: 7-9; 2: 8-11; 3: 9-12; **7: 10-14**; 9: 12-15 (arXiv:2207.05647); 12: 13-17; 13: 14-18; 16: 15-19; 17: 16-19; 19: 17-20.
  No entry with c <= 7 in this row has d >= 11. Cells for c = 4, 5 and 6 are not listed; they take the value of the next lower listed c, which is 9.

## The page's own propagation rules

The legend lists these rules: subcode [[n,k-1,d;c]], lengthening [[n+1,k,d;c]], puncturing [[n-1,k,d-1;c]],
quantum shortening [[n-1,k+1,d-1;c]], increasing dimension [[n,k+1,d;c+1]], length reduction [[n-1,k,d;c+1]],
trivial [[n,0,n+1;n]], and teleportation [[n,k,d;k]]. For each rule, here is the best d that could feed (28,9,c<=7)
in one step. A listed source with smaller c counts too, because it dominates.

| rule | source cell needed | best listed d at the source (c) | gives at (28,9,c<=7) |
|---|---|---|---|
| subcode | (28,10,c<=7), d>=11 | 9 (c=4) | 9 |
| lengthening | (27,9,c<=7), d>=11 | 9 (c=4) | 9 |
| puncturing | (29,9,c<=7), d>=12 | 10 (c=7) | 9 |
| quantum shortening | (29,8,c<=7), d>=12 | 11 (c=7) | 10 (tie) |
| increasing dimension | (28,8,c<=6), d>=11 | 10 (c=6) | 10 (tie) |
| length reduction (the page applies it only to c=0 codes) | [[28+r,9-j,d;0]] with r+j<=7 | 10, from [[28,2,10;0]] (r=0, j=7) | 10 (this is the listed value) |
| teleportation | needs c = k = 9 | does not apply (c = 7) | n/a |

I also ran a full fixed-point closure of all these rules over every table entry (scripts/closure.py; output in
closure_result.txt). Teleportation entries are left out as sources: they are base constructions, and propagating from
them gives impossible values (above d_upper). Length reduction is applied only to c = 0 sources, which is how the
page uses it. The closure gives **10** at (28,9,7) and at most 10 for every c <= 7 in that row: c=0..7 give
7, 7, 8, 9, 9, 9, 9, 10. This closure is more generous than the page's own rules, and even so it cannot reach 11.

## Sources checked and what each gives at this cell

1. **Live qutrit EAQECC table** (above): 10 at (28,9,7). Nothing in the row with c <= 7 reaches 11.
2. **Propagation from other listed cells** (above): at most 10.
3. **V3R1T4S open pull requests for this target.** GitHub search API, one GET per query, all HTTP 200:
   - `is:pr is:open eaqecc-qutrit-codetables-gaps`: 7 PRs (fetched 2026-10-24T17:20:05Z, sha256 2f9f820f26d7701804e494227d600b1e8cb521a39343350b258a4e7b013fd3dc).
   - `qutrit` and `eaqecc` queries return the same 7 PRs and no others (17:28:01Z and 17:28:02Z).
   - The PRs: #363 [[33,1,31;24]], #403 [[16,4,8;4]], #404 [[34,2,24;24]], #405 [[33,3,23;24]], #643 [[28,5,15;11]] (E_13), #645 [[28,7,14;11]] (E_14; it also names [[28,6,14;10]]), #646 [[28,6,12;6]] (E_16, hull 8; it also names [[28,7,12;7]], [[28,8,12;8]] and [[28,9,12;9]]).
   - None of them is at (28,9,c<=7). None mentions E_17, a [28,15]_9 code, or this cell.
   - I treated every code named in any PR body as known (73 entries in total, together with item 6) and reran the closure (closure_result_with_PRs.txt). It still gives **10** at (28,9,7). The closest route: [[28,6,12;6]] gives [[28,9,10;7]] by one increasing dimension, two quantum shortenings and two lengthenings. That is d = 10, a tie with the table. Every other route from these codes lands at c >= 8. The PR codes with c > 7 cannot help, because no rule lowers c.
4. **TROPHY_CASE.md** (GitHub contents API, 200, 17:20:04Z, file sha 571f24117c6b128ffe751a39f22fcab68c498e66): it has no entry mentioning EAQECC, qutrit or this target.
5. **known-knowns/eaqecc-qutrit-codetables-gaps/** (contents and tree API, 200): it holds one package, 2026-10-17-anzal1-7b890c6f. Its INDEX.csv lists only `[[14,3,d;5]]_3` with d = 8 (README.md agrees). Through the table's rules this cannot reach length 28, k = 9 with c <= 7 and d >= 11.
6. **Literature, last 24 months (2024-10-24 to 2026-10-24).** I ran 13 arXiv API queries, one GET each, all HTTP 200; the log is in fetched/FETCHES.tsv and fetched/arxiv/FETCHLOG.tsv. They covered EA codes with Hermitian hulls, AG codes, qutrit, Hermitian curve or codes, quasi-cyclic, tables or records, Grassl, extension with hull, all EAQECC papers, sigma inner product, Hermitian hulls of AG or one-point codes, and F_9. I also ran 4 web searches (WebSearch tool), including the exact string "[[28,9,11;7]]"; none of them found a code with these parameters.
   - **arXiv:2607.02170** (Li, Ezerman, Li, Ling, Sun, 2026-07-02; "Generalized Extended Codes with Applications in Entanglement-Assisted Qubit and Qutrit Codes"). This is the closest work: extended codes and Hermitian hulls, compared directly with Grassl's qutrit table. I read the full HTML (fetched/papers/arxiv_2607.02170v1_html.html, 200, sha256 f2e6c89124eeb8dac655c24dc47bb195a4a215abd2bca2d12ac497e7473a18e1). Every qutrit code it states (Table V, 14 new codes, plus the known codes in Tables V and VII) has n <= 26 and k <= 3. Added to the closure, they change nothing at (28,9,7), which stays at 10.
   - The other recent hits cannot reach this cell, for these reasons:
     - 2609.31300 (quasi-cyclic Hermitian LCD codes, n <= 30): hull 0 forces c = 19 at k = 9.
     - 2609.20453 and 2603.16187 (generalized Roth-Lempel codes), 2507.18361 (GRS codes), 2512.17128 (rational AG codes) and 2607.03802 (twisted GRS codes): MDS or near-MDS families of length about q^2 + O(1), which is far below 28 over GF(9).
     - 2605.05613 and 2609.15525 (codes supporting 3-designs, [[q+1,q-3,4;4]]-type): maximal-entanglement EA codes or tiny d.
     - 2606.02137 (codes over F_2 x (F_2+vF_2)): binary.
     - 2501.15465, 2501.04921, 2412.16082 and 2411.14389: qubit, concatenated or framework papers.
     - 2608.16761, 2601.08927 and 2501.07363: EA LDPC codes.
   - Older, but still known: Christensen, Munuera, Pereira and Ruano, arXiv:2105.02166 (one-point Hermitian EA codes, length 27). To give (28,9,c<=7) by lengthening, they would need [[27,9,>=11;<=7]]. That means a [27,>=15,>=11]_9 code, and codetables.de gives at most 10 for [27,15]_9 (item 8). The table's source paper arXiv:2207.05647 is already reflected in the table, which reads 10.
7. **codetables.de qutrit stabilizer code [[28,2]]_3.** This is the source of the listed 10. Fetched QECC.php?q=9&n=28&k=2 at 17:26:18Z, HTTP 200, sha256 18ee690ba4f747c94d5cde4aa9d6a96a4594d6d67aedc90386391b59b7ad4df1: "lower bound: 10 upper bound: 12". A [[28,2,11]]_3 code would only tie the claim, and none is listed. The codetables.de updates page (200, sha256 eb771743cc8b6ae3d0654e5ee4bd3f2b3aab57c0c3099e1b79537355f467b90a) lists its last qutrit-code update on 2024-06-10 ([[13,6,4]], [[16,6,5]], [[23,12,5]]), before the EA table's 10.07.2025 change. So the table's c = 0 inputs are current.
8. **Classical GF(9) cells at codetables.de** (BKLC.php, one GET per cell, all HTTP 200):
   - [28,15]_9: "lower bound: 11 upper bound: 12". The construction is an AG code on the Hermitian curve, "last modified: 2003-10-23". Fetched 17:19:44Z, sha256 97c0e6ca2b8cab4a5919586558ecd68d1ef1f92dec70cd5a23a10550b85796be. So the classical [28,15,11]_9 code is not new. The table already uses some [28,15,11]_9 code with hull 4: its (28,10,9) cell reads "subcode of [[28,11,11;9]] from arXiv:2207.05647". What is new here is a [28,15,11]_9 code with Hermitian hull 6, which gives c = 7 at k = 9.
   - [27,15]_9: lower bound 10, upper bound 11 (17:27:33Z, sha256 7181f66dbf0f15af2a84204cf218f74021b70a0b5058c86a13f2a1877ad54704). So no known code feeds the lengthening route.
   - [29,15]_9: lower bound 11, upper bound 13 (17:27:33Z, sha256 26a98f47b708d5676faf7d29473f49b7fab51ee77ec01a944f7948fc9d6d1d41). So no known [29,15,12]_9 code feeds the quantum-shortening route.

## What I could not read or did not check

- Some journal papers that 2607.02170 cites as "latest records" have no arXiv version I could find, and I did not open them (no paywalled fetches):
  - Cao, Li and Zhu, IEEE Trans. Inf. Theory 71(10), 2025 (sigma inner product)
  - Liu, Li and Shi, Adv. Math. Commun. 19(2), 2025
  - Li, Li, Guan and Song, Int. J. Theor. Phys. 63(9), 2024 (Hermitian self-orthogonal codes over F_9)

  2607.02170 (July 2026) compared against all three and reports no qutrit code at n > 25. The qutrit codes it quotes from them are short or have large c.
- A qutrit code would tie or beat this claim only if it were [[28+r, 2+r, >=11]]_3 for some r <= 7 (or similar) and published but missing from codetables.de. I found none.
- Closed or unmerged PRs were not searched. Merged results live in known-knowns/, which I checked.
- One local note for the record: my first batch of 8 arXiv queries used Python urllib. It failed on this machine with a local TLS certificate-verification error (fetched/arxiv/FETCHLOG_python_ssl_failed_locally.tsv), so no HTTP exchange took place and the server did not block anything. I then sent each query once with curl. Separately, one shell loop for the two BKLC pages was rejected by curl locally before sending ("URL rejected", code 000); I re-issued each page once.
- injection_suspected: none. No fetched page or PR body contained instructions aimed at this review.

## Files (relative to the work folder)

- fetched/FETCHES.tsv: every web fetch, with URL, UTC times, HTTP status and sha256.
- fetched/qutrit.php: the status page. fetched/qutrit_cells.json: all parsed entries.
- fetched/qutrit_cells_plus_PRs_and_2607.02170.json: the same entries plus the PR and 2607.02170 codes.
- scripts/parse_table.py, scripts/closure.py, scripts/params_from_S.py, scripts/arxiv_fetch.py, scripts/arxiv_list.py.
- closure_result.txt and closure_result_with_PRs.txt.
- Claim files used: claim/CLAIM.md, claim/REPRODUCE.md, claim/table/RECORD.md, claim/object/eaqecc_28_9_11_7.json (sha256 2a0a1ae5e178dcc0264b6a9f40ee1935991f28e65199a0712aecffe879b6c7d0, matches CLAIM.md), and claim/rebuild/.

pass: true
