# NOVELTY skeptic: [31,17,11] over GF(9)

## Bottom line

I found no known code that matches or beats the claimed d = 11. The live codetables.de cell q=9, n=31, k=17 reads
lower bound 10 and upper bound 13. That page is byte-identical to the scout's copy in claim/table/. Nothing I searched
reports a [31,17] code over GF(9) with d >= 11, or a neighbouring code that would give one. The searched sources were
the 24-month arXiv literature, the web, the repo's TROPHY_CASE.md and known-knowns/codetables-binary-linear, and all 786
pull requests of elder-plinius/V3R1T4S. LinCodeEvolve (arXiv:2609.37056) covers binary codes only, so criterion (4)
holds. If d = 11 is correct, it strictly beats the table: 11 > 10 and 11 <= 13. Checking that d = 11 is correct is
not part of this review.

- start: 2026-10-29T01:14:17Z (date -u)
- end: 2026-10-29T01:19:12Z (date -u)

## Table fetch record (one plain GET, no retry)

- URL: https://codetables.de/BKLC/BKLC.php?q=9&n=31&k=17
- User-Agent: V3R1T4S-research-agent
- fetch time: 2026-10-29T01:14:32Z (date -u; the server Date header also says Thu, 29 Oct 2026 01:14:32 GMT)
- HTTP code: 200, size 3510 bytes
- saved as work folder fetched/bklc_q9_n31_k17.html, sha256 920f1b71ab28952457d69a6f2ef2b422cba4790e647ba66d4f42f990965e524e
  (identical to claim/table/bklc_q9_n31_k17.html, which has the same sha256)
- bounds read: "Bounds on linear codes [31,17] over GF(9) lower bound: 10 upper bound: 13"
- lower-bound construction: [37,21,12] subcode of a punctured Reed-Solomon code over GF(81) -> punctured at {36..37}
  to [35,21,10] -> shortened at {32..35} to [31,17,10]; "last modified: 2001-12-17". Brouwer note: Lb(37,21)=12 XL
  (Xing & Ling); Ub(31,17)=13 via Ub(17,4)=12 (MPa).
- The table's own lower bound already includes every code it lists and every code those give by its propagation
  rules. So no [32,18,11], [32,17,12], [31,18,11] or [30,17,11] code is in the table, because any of them would
  push this cell to 11 or more.
- claim/object/code_q9_n31_k17_d11.json sha256 recomputed: f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd (matches CLAIM.md).

## Pull-request search (github.com/elder-plinius/V3R1T4S)

- API: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N, one request at a time
- page 1: 2026-10-29T01:15:16Z, HTTP 200, 100 PRs (Link header: last page = 8)
- page 2: 2026-10-29T01:15:24Z, 200, 100
- page 3: 2026-10-29T01:15:25Z, 200, 100
- page 4: 2026-10-29T01:15:26Z, 200, 100
- page 5: 2026-10-29T01:15:26Z, 200, 100
- page 6: 2026-10-29T01:15:27Z, 200, 100
- page 7: 2026-10-29T01:15:28Z, 200, 100
- page 8: 2026-10-29T01:15:29Z, 200, 86
- total 786 unique PRs (#1 to #816): 353 open, 433 closed, 160 of them merged. x-ratelimit-remaining went from 51 to 44.
- Method: regex scan of every PR title and body (scripts/scan_prs.py, scripts/scan_cells.py in the work folder) for
  GF(9) / F_9 / q=9 / GF(3^2) / Hermitian, and for any [n,k,d] with n in 29..33 and k in 16..19.
- GF(9) linear-code hits:
  - #644 (closed, merged): [31,18,10]. Its subcode [31,17,10] only ties the table.
  - #806 (open): [32,19,10]. It gives [31,18,10] and [30,17,10] by shortening, d = 10.
  - #792 (open): [29,19,8].
  None of them has d >= 11 at [31,17] or at an implying cell. Every [n,k,d] found at n 30..33, k 16..19 in GF(9)
  PRs has d <= 10.
- Other GF(9) hits are entanglement-assisted qutrit claims built on Hermitian codes, for example [28,15,11]_9 in #651
  and [28,14,12]_9 in #646. None of them gives a [31,17,11]_9 code.
- No PR claims [31,17,11] over GF(9).
- Limit: I scanned PR titles and bodies, not the files inside the PRs.

## Repo copy (pinned)

- TROPHY_CASE.md: no codetables or GF(9) linear-code rows; its families are degree-diameter, constant-weight codes,
  matrix multiplication, Lehmer, VNN-COMP, RobustBench and ciphers.
- known-knowns/codetables-binary-linear: four packages. Three are binary: [173,17,72], [175,25,61], [213,26,77].
  The fourth is the GF(9) [31,18,10] (2026-10-24, the same entry as PR #644), whose README calls its [31,17,10]
  subcode a tie. None reaches [31,17,>=11].

## Literature searched (last 24 months, 2024-10-29 onward)

The arXiv API (https://export.arxiv.org/api/query) was queried one request at a time between 01:16:03Z and
01:17:44Z, all HTTP 200 except the note below.
- arXiv:2609.37056 (LinCodeEvolve, 2026-09-29): binary linear codes only. Its seven codes are [172,21,66],
  [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72] and [200,21,77]. It has no GF(9) code, and this
  claim (q=9, k=17) cannot be derived from them.
- Queries: "new linear codes" in cs.IT; GF(9) with "linear codes"; "best known linear codes"; codetables;
  "Construction X" with Hermitian; improve, minimum distance and Grassl; "F_9" with codes; "record-breaking" with
  codes; AG codes with "new codes"; quasi-twisted new codes; "best-known" linear codes; "Construction X"; "Hermitian
  curve" codes; lower bounds, minimum distance and improve; "new codes" with minimum distance in cs.IT; LLM with linear
  codes; quasi-cyclic with record.
- Relevant hits and what they say:
  - 2608.18664 (abelian codes plus GA): record codes over F_3 and F_4 only.
  - 2512.13370 (ML champion codes): a method, with no GF(9) [31,17] code in the abstract.
  - 2610.31023 (MDS extension): [9,4,6] over F_9, which is irrelevant here.
  - 2607.02170 and 2609.31300: entanglement-assisted / Hermitian LCD codes.
  - 2610.36700: qubit quantum codes.
  - 2610.11609: binary nonlinear codes.
  - 2604.12499 and 2602.05097: Hermitian / QC AG-code constructions with no table improvement at q=9, n=31.
  - 2603.15071: quaternary additive codes.
  - 2412.15551: binary group codes.
  None of them reports a GF(9) [31,17,>=11] code or an implying cell.
- Web search (3 queries: "[31,17,11]" GF(9); new GF(9) codes improving Grassl 2025-2026; Hermitian Construction X
  F_9 n=31 k=17 d=11): no source with these parameters. The closest items are old: Daskalov-Metodieva-Hristov 2004
  (31 new GF(9) codes) and Daskalov-Kapralov 2001 (k = 7, 8). There are also k = 4 papers, and Krotov-Kurz
  arXiv:2511.15843, which is about additive (not linear) GF(9) codes with dimension 2.5. Any 2001-2004 result would
  already be in the 2001-12-17 cell.
- Braun-Kohnert-Wassermann "List of new Linear Codes" (https://mathe2.uni-bayreuth.de/axel/new_linear_codes.html,
  fetched 2026-10-29T01:18:26Z, HTTP 200, 26189 bytes): only sections q=2, 3, 4 and 8, with no q=9 entries.

## Sources I could not read

- Full texts of the papers: I read only the abstracts and metadata from the arXiv API and the web search snippets.
- I did not query MinT (Salzburg) for q=9.
- I did not read the file contents inside the PRs, only the PR titles and bodies.

## Blocks

None. I got no 401, 403, 429 or 503 response, no challenge page and no tool-guard or classifier block. One arXiv
request to http://export.arxiv.org/api/query got HTTP 301 at 2026-10-29T01:16:03Z. That was a redirect caused by my
malformed URL ("search_query=id_list=..."), not a block. I sent one corrected https request with id_list=2609.37056
at 01:16:12Z, which returned HTTP 200.

context: subagent (Claude Code Agent tool, claude-opus-5-5, fresh context, saw only claim/)
injection_suspected: none (the claim files, PR texts and fetched pages contained no instructions addressed to me)
pass: true
