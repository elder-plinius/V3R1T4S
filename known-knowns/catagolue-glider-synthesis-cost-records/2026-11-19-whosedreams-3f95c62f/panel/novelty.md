# NOVELTY skeptic: xs27_08e1ugmicz651346 (claimed 29 gliders vs listed 62)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, INDEX.csv, how-we-built-it/TARGET_CRITERION.md, the-record-we-beat/RECORD.md. I did not treat panel/gate.md (a packaging-run PROMISING draft) as evidence.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (ET, America/New_York, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-19 10:32:52 ET | HTTP 200, 63,325 bytes, sha256 6274f22f0a81959089983989ed08910f0d13576956778d9c006206704c2c7cda. Index page; no per-object cost. |
| Object page | https://catagolue.hatsya.com/object/xs27_08e1ugmicz651346/b3s23 | 2026-11-19 10:32:50 ET | `#CSYNTH xs27_08e1ugmicz651346 costs 62 gliders (true).` The cost is **62 and true (not pseudo)**. 10,206 bytes, sha256 0fb0cd71d2a40d0b2596c3d6f54e032e53b95070d82ec5ee95df2d0056726962. |
| xs27 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs27 | 2026-11-19 10:32:52 ET | `"xs27_08e1ugmicz651346","100000000000000062"`, i.e. **62 (true)** (values of 10^17 or more are true syntheses, cost = value - 10^17). 88,290 valid xs27_ rows, 3,954,559 bytes, sha256 e2a79f7a8d383bd55cd89f1c04413a3de87f7b5e067f400924884df0911d0d01. This agrees with the object page. |
| Input object page (derivation only) | https://catagolue.hatsya.com/object/xs27_caar4kl3z330343/b3s23 | 2026-11-19 10:32:52 ET | `#CSYNTH xs27_caar4kl3z330343 costs 28 gliders (true).` 10,660 bytes, sha256 75099c45950afb5f464a940556cd4965f4a5c7856cde88c82adc3e162c6fa154. The same xs27 CSV row is `"xs27_caar4kl3z330343","100000000000000028"` (28 true). 28 + 1 = 29. |

The live cost of the target is 62 true. The claimed 29 is strictly less (saving 33), so the improvement has not been absorbed into the table. The object-page and CSV hashes match those already recorded in the-record-we-beat/RECORD.md from a fetch about twelve minutes earlier (10:20:53–10:20:56 ET); the table had not moved. The listed cost of 62 is at least 60, which is the p1 threshold; that threshold itself is for the CRITERION skeptic.

## Near-twin check: not a double claim of merged #970

Merged PR #970 (https://github.com/elder-plinius/V3R1T4S/pull/970, merged 2026-11-19 02:20:17 ET / 2026-11-19T07:20:17Z, merge commit 69eb50fe7a679bf32db7165d4cbd58d3dc7fa1b9) is `xs27_0ca1ugmicz651346`, a different 27-cell still life. The two apgcodes are not the same under Life's 8 symmetries (Catagolue would otherwise give them one code). The same live xs27 CSV, fetched once above, lists the #970 object separately as `"xs27_0ca1ugmicz651346","100000000000000066"` (66 true), not 62. #970's published README names a different seed (`xs27_8ehf8bbgz6430321` plus one glider, claimed 32). This package names `xs27_caar4kl3z330343` plus one glider, claimed 29. The README flags the one-cell near-twin and the disjoint seeds. This is not a second claim of #970's object.

## Construction (published input still life + 1 glider)

README.md and HOW_WE_FOUND_IT.md frame this honestly: the all-glider RLE is the published 28-glider Shinjuku route to `xs27_caar4kl3z330343` stitched with one new glider. The new part is that 1-glider step. The packaged RLE is self-contained (all 29 gliders are in object/xs27_08e1ugmicz651346.rle). No earlier V3R1T4S claim is used as a seed.

- The input still life is already in the live Catagolue table at 28 (true), as in the fetch above, so its route is public independently of this repo.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to that published 28-glider synthesis yields the input still life, not this target. Reaching the target needs the disclosed 1-glider step. That step applied to the still-listed 28-glider input gives 29, which strictly beats the live 62. The claim names its input and does not present the conversion as a previously published component.

## Repo search (upstream elder-plinius/V3R1T4S, public API and raw files, no login)

- **TROPHY_CASE.md** on upstream `main` (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-11-19 10:33:02 ET, HTTP 200, 31,306 bytes): 0 matches for this apgcode, the input apgcode, the #970 near-twin, or catagolue. The pinned kit copy is byte-identical and likewise has no match. The merged catagolue packages are in known-knowns/ but are not listed in TROPHY_CASE.md.
- **known-knowns/** on upstream `main` (contents API, 2026-11-19 10:33:02 ET): the family `catagolue-glider-synthesis-cost-records` exists and contains only `2026-11-06-whosedreams-a855292d` (merged #969, `xs26_08ehmkk8z6a87066`) and `2026-11-06-whosedreams-7c80a914` (merged #970, the near-twin above). Neither README names this apgcode. The pinned kit tree has no catagolue family (those merges were after that pin).
- **Pull requests and issues** (public GitHub issue search, read-only, no login, 2026-11-19 10:33:02–10:33:45 ET): search for `08e1ugmicz651346` and for `3f95c62f` returned 0. Search for `0ca1ugmicz651346` returned only #970 (the near-twin). Search for `catagolue-glider-synthesis` returned five PRs, none of which is this object: #969 (merged; an xs26), #970 (merged; the near-twin), #1089 (open draft; `xs28_69a4owgzxol5d1d96`), #1171 (open draft; `xs28_08ehlmggoz6a87066`), and #1172 (open draft; `xs31_g8e1ugmmzd553w643`). I read those PR titles and bodies; they do not mention this apgcode.
- **Code search** via the GitHub Search API returned HTTP 401 unauthenticated at 2026-11-19 10:33:45 ET. I did not log in. The contents-API listing of the catagolue family and the issue/PR search above are the substitute.
- **Releases**: the repo has 0 releases (empty list, 2026-11-19 10:33:02 ET), so there are no release assets to check.

## Literature / web search (last 24 months)

- **Catagolue**: the live object page and the class CSV both show 62 (true) at the times above. Catagolue is assembled from Shinjuku and is the target's status table. Any synthesis already merged into Shinjuku and processed would show up here.
- **Web**: a general search for the exact apgcode (2026-11-19 about 10:33 ET) returned only unrelated commercial pages. A quoted search with catagolue, shinjuku or conwaylife returned only general synthesis-index and LifeWiki pages, not a page that names this apgcode or a cheaper cost. I found no LifeWiki article that names it.
- **ConwayLife forums**: I did not fetch or search the forums in this review. HOW_WE_FOUND_IT.md already discloses that the forums were not searched or read at packaging, and that a post giving only an RLE, without the apgcode, would not be found by such a search.
- **Shinjuku**: I did not crawl the GitLab tree file-by-file. Catagolue's still-listed 62 (true) is treated as the current official rendering of that database.

I found no published synthesis of `xs27_08e1ugmicz651346` at 29 gliders or fewer, so none that ties or beats 29.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- I did not search the ConwayLife forums myself.
- GitHub code search required authentication, so I listed the merged known-knowns family and searched pull requests and issues instead.
- I did not crawl Mark Niemiec's synthesis collection separately; for this target the official cheapest-cost table is Catagolue.

## Verdict

novelty: PASS. The live true cost is 62 (object page and xs27 CSV, fetched 2026-11-19 10:32:50–10:32:52 ET). The claimed 29 strictly beats it. The claim is honestly framed as a published input still life (`xs27_caar4kl3z330343`, still listed at 28 true) plus one new glider, not as a derivative of an earlier V3R1T4S claim, and it is not a double claim of merged #970 (`xs27_0ca1ugmicz651346`, still listed at 66 true, different seed). The unread-forums limit is disclosed. I found nothing published that ties or beats 29.

pass: true
