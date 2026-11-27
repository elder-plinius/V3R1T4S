# Novelty skeptic: <18,18,19> rank 3225 over Q (fmm-catalogue-small-format-rank, partial win p1)

reissued 2026-10-24 at the coordinator's request: login redacted and a quoted placeholder rephrased; findings and verdict unchanged
context: subagent (Claude Opus 5.5, fresh context, given only a copy of claim/)

## Bottom line

The lowest public value I could find for <18,18,19> in any axis order (18,18,19 / 18,19,18 / 19,18,18) is **3355**
(fmm_sota.json, the Lille catalogue index, matmulcatalog). The Lille per-format page shows 3524. No table, repository,
pull request by another contributor or paper lists 3225 or lower, and no listed larger format containing the cell is
at or below 3225 (the lowest is <18,18,20> at 3526). 3225 strictly beats everything known, by 130. The only earlier
public trace of 3225 is the same contributor's PR #708, which I rule is not a blocker (see the ruling below), but
the package must correct its disclosure of what #708 contains.

## Sources (my own fetches, one plain GET each, UTC, `date -u`)

All fetches: curl, User-Agent "V3R1T4S-novelty-skeptic (single GET)", no cookies, no retries; GitHub API reads as plain GET
requests to api.github.com (every call succeeded). No block, classifier denial, 401, 403 or 429 occurred.

### Bank p1 bar (fmm_sota.json and Lille; status_source https://fmm.univ-lille.fr/)

| fetched (UTC) | HTTP | URL | sha256 of body | value for the cell |
|---|---|---|---|---|
| 2026-10-24T19:28:13Z | 200 | https://fmm.univ-lille.fr/ (catalogue index, the bank's status_source) | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row 18x18x19: ⟨18×18×19:3355⟩, construction ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩; the index also shows ⟨18×19×18:3355⟩ (same value). Last-Modified Tue, 20 Oct 2026 08:14:45 GMT |
| 2026-10-24T19:28:13Z | 200 | https://fmm.univ-lille.fr/18x18x19.html | 0bae85379d91e8a22a54e37fc984a936bc6885947f00ccd481ee5e97e42beab3 | ⟨18×18×19:3524⟩ (Kronecker product of ⟨18×9×19:1762⟩ with ⟨1×2×1:2⟩). Last-Modified Fri, 19 Jun 2026 19:35:35 GMT |
| 2026-10-24T19:28:13Z | 404 | https://fmm.univ-lille.fr/18x19x18.html | 9448f8a1...e6e1e | Not Found (pages exist for sorted formats only) |
| 2026-10-24T19:28:14Z | 404 | https://fmm.univ-lille.fr/19x18x18.html | 9448f8a1...e6e1e | Not Found |
| 2026-10-24T19:28:14Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | `{"format": [18, 18, 19], "rank": 3355}`; createdAt 2026-10-19T20:46:33; 5456 entries (sorted formats only) |

My hashes match the ones the claim records (the-record-we-beat/RECORD.md) for all five, so nothing changed between
19:05:59Z and 19:28:14Z.

### Other comparators (POLICY FMM rule 1 and the bank's sources)

| fetched (UTC) | HTTP | URL | sha256 | finding for the cell (any order) |
|---|---|---|---|---|
| 2026-10-24T19:28:14Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 52db72a9cd408815d98ebcd851d55fb13b8d84eaa70b7ebd7c4de67cc29b9e61 | no mention |
| 2026-10-24T19:28:14Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a | no row; largest dimension in the table 16 |
| 2026-10-24T19:28:14Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md | 258cfa9846615ac5e75f665969b2aad3ca496a11fcb9d9561e368474a309ca88 | no row |
| 2026-10-24T19:28:15Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md | e451692724898898bbc051649324b015be4d7842d403f9c54909f4513f32d489 | no mention |
| 2026-10-24T19:28:41Z | 200 | https://api.github.com/repos/dronperminov/FastMatrixMultiplication/git/trees/master?recursive=1 (includes schemes/results/) | 408ac494c266f4a35503469729a264ff85643d988e1ef543701410622407a3f7 | 6863 paths, not truncated, largest dimension 16; no file for the cell |
| 2026-10-24T19:28:43Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/HEAD?recursive=1 | e6866337cf18c6f4bb9d2b950240341d901260e28b560a301853202c03b1a5fc | 39 paths, largest dimension 16; nothing |
| 2026-10-24T19:28:15Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 5c600b98b4bb8f9feed5b4d9ffabf11af34b98f49bf43ae250b81e71f43e000b | (18,18,19): 3355 (Q,R,C), 3356, 3524; external_best_rank 3355 |
| 2026-10-24T19:28:16Z | 200 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7 | no row (stops at max dimension 16) |
| 2026-10-24T19:28:16Z | 200 | https://raw.githubusercontent.com/khoruzhii/lita/main/README.md | 97df246f15643a7396307765d23432d03bcb5af97a9f8bf92cae85cb428d5b3f | square schemes only (even and odd N); no rectangular result, no restriction result; manuscript "in preparation" |
| 2026-10-24T19:28:43Z | 200 | https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1 | 75d497884cdff3414cc1b996c21083229d2984437f308186a686048ba4f7ee57 | 20 square schemes 13^3 to 32^3 (19^3 r3633, 20^3 r3994); no rectangular file |
| 2026-10-24T19:28:44Z | 200 | https://api.github.com/repos/khoruzhii/lita/commits?per_page=10 | a8ce4c2848796206b567208528d751391f626900767541a2aabfbf2ba5751580 | head 472a79fbc8, 2026-10-07; nothing newer |

### This repository (elder-plinius/V3R1T4S)

| fetched (UTC) | HTTP | URL | sha256 | finding |
|---|---|---|---|---|
| 2026-10-24T19:28:16Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | no row for the cell, no 3225 |
| 2026-10-24T19:28:44Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/main?recursive=1 | e49a030f07630ba8def4ae850727750719a3401efe6da1940ad03fc80ee8874c | 5439 paths, not truncated, largest FMM dimension 16; nothing merged for the cell |
| 2026-10-24T19:28:45Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits?per_page=5 | ec1d4b44cda5bd28bc5be96c0ebd7dd475cc06c619c963062a960506dcaad82e | main head 1ebdef41c3, 2026-10-24T16:13:09Z |
| 2026-10-24T19:29:01Z to 19:29:08Z | 200 (8 pages) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..8 | page 1 a6febe40..., page 8 (empty) 4f53cda1... | 685 PRs, #1 to #708 (337 open, 348 closed, 150 merged), 118 FMM-related. Titles and bodies scanned for the cell in every order and notation (x, ×, commas, angle brackets, parentheses) and for 3225; also for any format that contains (18,18,19) componentwise. Only hit: #708 (open, the contributor, created 2026-10-24T18:58:23Z). No PR by anyone else names the cell, 3225, or a containing format with a rank |
| 2026-10-24T19:29:16Z to 19:29:18Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/708, /pulls/708/files, /pulls/708/commits, /issues/708/comments | 1457d5ac..., 812cf2fc..., c34f21a1..., 4f53cda1... | one commit e4bb688f43 (2026-10-24T18:31:54Z), 30 files, no comments. Object: <18,19,19> rank 3424 only. See the ruling |

### Literature (last 24 months)

| fetched (UTC) | HTTP | URL | sha256 | finding |
|---|---|---|---|---|
| 2026-10-24T19:30:11Z | 301 (empty body, redirect to https) | http://export.arxiv.org/api/query?... (three queries) | e3b0c442... (empty) | scheme redirect only, not a block; the same queries were then issued once at the https URL in the Location header |
| 2026-10-24T19:30:19Z | 200 | https://export.arxiv.org/api/query?search_query=abs:"matrix multiplication" (300 newest, 2026-04-03 to 2026-10-21) | c6524b0ee7961098d4a59f04986de388d2f0dad5f0986b04c4510f8ea00d9431 | no abstract names the cell in any order, 3225 or 3355 |
| 2026-10-24T19:30:38Z | 200 | https://export.arxiv.org/api/query?search_query=abs:"fast matrix multiplication" OR "matrix multiplication tensor" OR "bilinear algorithm" OR "flip graph" (337 entries; 38 relevant since 2024-10-24, incl. 2606.02480, 2606.13408, 2603.02398, 2511.20317, 2510.19787, 2502.04514, 2610.26563) | 36a74f94cf31b999ef86a7f5392bc25a6ef230dd6972d8763b89c95e5aacda82 | no hit for the cell, 3225 or 3355 |
| 2026-10-24T19:30:23Z | 200 | https://export.arxiv.org/api/query?search_query=all:"trilinear aggregation" | 5c4ec0cca2f5c073d43d012cce55cf963ed3e7147c34cee927b6a7aa4d9ed917 | one entry, 2508.01748 (Schwartz and Zwecher, square N=44); no rectangular 18/19 result in the abstract |
| 2026-10-24T19:30:27Z | 200 | https://export.arxiv.org/api/query?search_query=au:Khoruzhii | 13d66d3655253e01b97dca1e86bc61880fad3319860915b97491a4c09fa93122 | 13 entries; no LITA manuscript |
| about 19:31Z | - | WebSearch: `"18x18x19" matrix multiplication rank scheme`; `LITA "Local Improvements to Trilinear Aggregation" rectangular schemes Khoruzhii Pokutta` | - | nothing for the cell (closest hit fmm.univ-lille.fr/2x18x19.html, a different format); LITA only as square schemes |

Limit: I read abstracts and catalogues, not every full text. The Lille catalogue and matmulcatalog aggregate the
literature and both stop at 3355 for this cell.

### Larger formats containing the cell

fmm_sota.json, lowest ranks for sorted formats (a,b,c) with a >= 18, b >= 18, c >= 19: (18,18,19) 3355,
(18,18,20) 3526, (18,19,19) 3633, (19,19,19) 3633, (18,18,21) 3751. matmulcatalog: (18,18,20) 3526,
(18,19,19) 3595, (19,19,19) 3633. None is at or below 3225, so no listed containing format restricts to <= 3225.
The only lower value for a containing format is the same contributor's open PR #708 (<18,19,19> 3424); the claim's
own accounting (how-we-built-it/COMMANDS.md) shows its best plain coordinate restriction to the cell gives 3395 and
the non-coordinate slice gives 3226 before the extra 2-reduction, so #708 does not tie or beat 3225 either.

Residual risk, not a blocker: LITA also publishes 20x20x20 r3994 (and larger). Non-coordinate slicing of that scheme
(five slices) has not been tried by anyone as far as the record shows, and could conceivably land near or below 3225.
That would be an unpublished derivation, so under POLICY rule 3 it is not a public value. I did not download the
LITA npz files (a file download needs the user's yes, naming the file: schemes/20x20x20_r3994.npz, 513040 bytes, from
github.com/khoruzhii/lita). Worth noting for the user, not a reason to fail.

## Ruling on PR #708 (POLICY FMM rules 2 and 3, read literally)

What #708 actually contains (read at 19:29:17Z), which is more than a sentence:
- The body's "Not claimed" list: "The run also built <18,18,19> at 3225 (fmm_sota.json 3355); it is not part of
  this package (one cell per package)."
- Its files include how-we-built-it/code/rebuild_lita_slices.py, engine.py, convert.py and export_txt.py, each
  text-identical to the files of the same names in this claim's how-we-built-it/code/, and its COMMANDS.md says
  "code/rebuild_lita_slices.py: the same for any odd N, plus a second slice (gives <18,18,19> 3225 from N = 19)".
- It does not contain the <18,18,19> scheme files (no u/v/w for this cell; no file name with 18x18x19).

So as of 2026-10-24T18:58:23Z the value 3225 was public, and the exact recipe that deterministically regenerates this
claim's object from public LITA data was public too, both by the same contributor (Abshalom Dayan).

Rule 3 says a value that was public before the filing date with an equal or better value blocks. Read literally and
alone, "3225 was public at 18:58:23Z" looks like it triggers it. I do not think that is the right reading, for these
reasons:
1. Rule 2 sets the filing date by the first public filing of the claimed object (PR creation time, or the commit that
   added the object, or an earlier PR here holding byte-identical bytes). The policy's priority unit is the filed
   object, and rule 2 explicitly anticipates the contributor's own earlier publication (a dated 'by the contributor on'
   note) as something that dates the claim, not something that voids it.
2. Rule 3 exists to stop claiming what someone else already achieved. A contributor's own earlier mention of their
   own unfiled result is not prior art against themselves; treating it as a blocker would mean any honest
   "not claimed, also built X" disclosure destroys X, which punishes exactly the transparency the kit asks for.
3. There is no competing party: no other filing, table or paper has 3225 or lower for this cell before 18:58:23Z or
   since.

So #708 is not a blocker. Its effect is on dating and disclosure:
- Priority date. By the spirit of rule 2 the earliest public filing that makes this object reproducible is #708
  (created 2026-10-24T18:58:23Z; its single commit e4bb688f43 is 2026-10-24T18:31:54Z), because it published the
  identical deterministic generator and named its output. The conservative date is this claim's own PR creation
  time. Both dates are by the same contributor and nothing public by anyone else sits before either, so the outcome
  is the same: 3225 is a record either way. The merged record should date the cell to #708's creation time
  (generator and value) with the object first filed in this PR.
- Disclosure correction required. The package currently understates #708. README.md ("Not a new method" bullet)
  says #708's body "mentions the value 3225 for this cell, without the scheme", and the-record-we-beat/RECORD.md says
  "The scheme itself has not been filed anywhere." Both should say, in substance: "PR #708 (same contributor, opened
  2026-10-24T18:58:23Z, commit e4bb688f43 of 18:31:54Z) states the value 3225 for <18,18,19> and contains
  how-we-built-it/code/rebuild_lita_slices.py, engine.py, convert.py and export_txt.py, identical to the files here,
  whose second step rebuilds this exact scheme from LITA 19x19x19 r3633; the scheme files themselves are first filed
  in this PR." The merged record should carry the dated note "value and generator first made public by the
  contributor in #708 on 2026-10-24".
- Rule 5 does not apply: #708 is a different cell (<18,19,19>), and its object does not match or beat 3225 for this
  cell by restriction (3226 at best before the extra reduction, per the claim's accounting).

## Other notes

- The claim's provenance is honest and complete: derived from the published LITA <19,19,19> r3633 scheme by two
  non-coordinate slices and two 2-reductions; the method was already used in this repository by another
  contributor (calgulbenkian, PRs #41, #51 closed; #130, #164, #172, #197 merged, all from LITA 15^3 to 18^3, none
  for this cell). That is method precedent, not a value precedent, and the README already says "Not a new method".
- Not a plain composition listed in the Lille construction column: the listed constructions are the block sum
  (3355) and the Kronecker product (3524), both above 3225.
- Ring Q, rank 3225 versus bar 3355: strict improvement of 130; not a tie.

pass: true
