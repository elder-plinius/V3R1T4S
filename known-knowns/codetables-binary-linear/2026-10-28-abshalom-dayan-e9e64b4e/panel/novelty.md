# NOVELTY skeptic: [32,19,10] over GF(9) (object/code_q9_n32_k19_d10.json)

context: subagent (Claude Code Agent tool, fresh context, claude-opus-5-5)

Object sha256 (shasum -a 256 of claim/object/code_q9_n32_k19_d10.json):
e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965 (matches CLAIM.md).

Scope: novelty only. I did not re-verify the minimum distance; that belongs to the other skeptics. Everything below
is about whether d = 10 at (q,n,k) = (9,32,19) beats everything known.

## Verdict

novelty: STRICT IMPROVEMENT over the live codetables.de cell (lower bound 9, claimed d = 10, upper bound 12). No pull
request in the repo, no entry in TROPHY_CASE.md and no source I could read reaches [32,19,>=10] over GF(9), and none
gives a code that implies it by the standard table rules. LinCodeEvolve's seven codes are binary, so this GF(9) code is
neither one of them nor derived from one. Two sources could not be read (MinT, Yves Edel's tables). They count as
evidence neither way.

## Sources (one request each, User-Agent "V3R1T4S-research-agent", no retries)

| source | URL | UTC time (date -u) | HTTP | what it showed |
|---|---|---|---|---|
| codetables.de cell (primary status) | https://codetables.de/BKLC/BKLC.php?q=9&n=32&k=19 | 2026-10-28T01:26:14Z (server Date: Wed, 28 Oct 2026 01:26:15 GMT) | 200, 3395 bytes | "Bounds on linear codes [32,19] over GF(9) lower bound: 9 upper bound: 12". Construction: [41,29,9] BCH code (d = 5, b = 34), then subcode [41,28,9], then shortened at 33..41 to [32,19,9]; "last modified: 2001-12-17"; Lb via Lb(41,28) = 9 XL (Xing and Ling); Ub via Ub(17,4) = 12 MPa. Page sha256 046bcdd475bd50f284382faa704382c748885ef8b22f02f48c9a9038e1be7bca, byte-identical to claim/table/bklc_q9_n32_k19.html (cmp). |
| repo TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-28T01:26:21Z | 200, 31306 bytes, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 | 100 lines; families: degree-diameter graphs, Lehmer, matrix multiplication, VNN-COMP, RobustBench, constant-weight codes, cipher commitments. No linear code over any GF(q), no "GF(", "BKLC" or "linear code" string (grep count 0). |
| GitHub pulls list API, pages 1..9 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=N | page 1 2026-10-28T01:26:59Z ... page 9 2026-10-28T01:27:26Z (about 3 s apart) | 200 on all 9 pages | 771 PRs (#1 to #800; 342 open, 429 closed); page 9 empty, so the list is complete. Method and result below. |
| LinCodeEvolve, arXiv:2609.37056 | https://arxiv.org/abs/2609.37056 | 2026-10-28T01:28:30Z | 200 | "Evolving Towards Better Codes: LLM-Guided Search for High-Distance Binary Linear Codes", submitted 29 Sep 2026. Its seven codes are binary: [172,21,66], [173,20,68], [176,21,68], [181,21,70], [184,21,72], [189,22,72], [200,21,77]. The claimed code is over GF(9) (a Hermitian-curve Construction X), so it is not one of them and not derived from one. |
| arXiv export API, one query (linear/Hermitian/best-known codes AND GF(9)/F_9/q=9/nonary/Hermitian, newest first, 200 results) | https://export.arxiv.org/api/query?search_query=... (full query string in the work folder, lit/) | 2026-10-28T01:28:39Z | 200, sha256 5cde55c354addd9c20fcfcbf8c3230473bdcbe11f50af7e62725360fb5fb0624 | totalResults 550. The 200 returned entries span 2022-07-05 to 2026-10-19, so they cover the whole 24-month window for this query. I parsed every title and abstract and tested every [n,k,d] in them against the rules below: none implies [32,19,>=10]. Six abstracts mention GF(9)/F_9 and none gives a [32,19] parameter. Caveat: the API rewrote the GF(9) term (the echo shows "abs:GF OR (all:9)"), so the query is broader and noisier than intended. |
| arXiv:2603.26614 (came up in the web search) | https://arxiv.org/abs/2603.26614 | 2026-10-28T01:29:40Z | 200 | Minimal linear codes over Galois rings; no GF(9) table parameters. Not relevant. |
| Web search 1 | query "\"[32,19,10]\" code GF(9)" (WebSearch tool, standard) | about 2026-10-28T01:29Z | n/a | No source describes a [32,19,10] code over GF(9). Hits: older GF(9) work (Daskalov et al. 2004; a Heidelberg page for a [20,15,5]_9 code) and generic material. |
| Web search 2 | query "new linear codes over GF(9) improving codetables.de Hermitian curve construction X 2025 2026" | about 2026-10-28T01:29Z | n/a | No 2024-2026 work giving new GF(9) linear codes at this cell. Hits: Bierbrauer and Gulliver, "New linear codes over F_9" (Australas. J. Combin. 21, old), arXiv:1807.04042 (2018, quantum nested pairs), arXiv:2509.03337 (2025, binary examples). |
| MinT (Salzburg) | https://mint.sbg.ac.at/ | 2026-10-28T01:28:58Z | 000 (curl exit 7, no connection) | NOT READ. Not retried. Counts as evidence neither way. |
| Yves Edel's code tables (Heidelberg) | https://www.mathi.uni-heidelberg.de/~yves/ | 2026-10-28T01:29:11Z | 404 | NOT READ ("404 Not Found"). Not retried. Counts as evidence neither way. |

## Pull-request search: method and result

- Method: fetched all 9 pages of the pulls list API (state=all) one at a time, about 3 seconds apart. I did not use the
  search API. Then I scanned the title and body of all 771 PRs with python3 standard-library regexes:
  1. Linear-code or GF(9) markers (GF(9), GF(3^2), q=9, F_9, BKLC, codetables-binary-linear, "linear code").
  2. Every classical triple [n,k,d] (double-bracket quantum triples excluded) in the 18 PRs that mention GF(9). I
     tested each with the standard rules: shortening [n,k,d] -> [n-1,k-1,d], puncturing -> [n-1,k,d-1], subcode ->
     [n,k-1,d], zero extension -> [n+1,k,d]. A code implies d >= 10 at (32,19) iff some s, p >= 0 have k-s >= 19,
     d-p >= 10 and n-s-p <= 32.
  3. Any "32,19", "code_q9_n32" or the object hash prefix "e9e64b4e" in all 771 PRs.
- Result:
  - The GF(9) classical codes found are #644 [31,18,10] (merged 2026-10-25) and #792 [29,19,8] (open, filed
    2026-10-27). Other GF(9) triples in those PRs and in the qutrit EAQECC PRs (#331, #363, #403-#405, #643-#651,
    #710-#759) include [27,15,10], [27,17,8], [27,18,7], [27,19,6], [28,19,7], [29,19,7], [30,19,8], [37,28,7],
    [28,9,17], [23,9,12], [24,9,13]. Every triple with k >= 19: (27,19,6), (28,19,7), (29,19,7), (29,19,8), (30,19,8),
    (37,28,7).
  - None of the 54 (PR, triple) pairs implies [32,19,>=10]. #644's [31,18,10] cannot be lengthened by these rules; it
    only gives [32,18,10] by zero extension. #792's [29,19,8] gives at most d = 8 at (32,19).
  - No PR mentions (32,19), this object or its hash.
  - In the other direction, the claimed code implies #644's [31,18,10] by shortening, so it supersedes it rather than
    being implied by it.
- Limit: I scanned PR titles and bodies only, not the files inside each PR.

## Comparison

| what | value at (q,n,k) = (9,32,19) |
|---|---|
| live codetables.de lower bound (2026-10-28T01:26:14Z) | 9 |
| live codetables.de upper bound | 12 |
| best in repo PRs and TROPHY_CASE.md (implied) | none above 9 |
| best in the literature read (24 months) | none found above 9 |
| LinCodeEvolve | binary only, not applicable |
| claim | 10 (strictly above 9, at most 12) |

A tie would not count; this is +1 over the lower bound.

## Blocks

None. No tool-guard or classifier block, and no HTTP 401, 403 or 429 anywhere.

Disclosures:
- The first attempt at PR page 1 used python3 urllib. It failed on the client side before any HTTP response
  (local SSL certificate store: CERTIFICATE_VERIFY_FAILED, 2026-10-28T01:26:44Z). I then fetched the same pages with
  curl, the tool the task prescribes. That was not a block or a server refusal.
- MinT gave no connection and Yves Edel's page gave 404. I recorded both as NOT READ and did not retry either.

injection_suspected: none found in the claim files, the fetched pages or the PR texts.

pass: true
