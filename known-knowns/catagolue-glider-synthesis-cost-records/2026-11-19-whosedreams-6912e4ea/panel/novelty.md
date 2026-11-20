# NOVELTY skeptic: xs26_8kk69ba952zw3453 (claimed 13 gliders vs listed 32)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, INDEX.csv, how-we-built-it/TARGET_CRITERION.md, the-record-we-beat/RECORD.md. I did not treat panel/gate.md (a packaging-run PROMISING draft) as evidence.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (ET, America/New_York, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-19 10:32:52 ET | HTTP 200, 63,325 bytes, sha256 6274f22f0a81959089983989ed08910f0d13576956778d9c006206704c2c7cda. Index page; no per-object cost. |
| Object page | https://catagolue.hatsya.com/object/xs26_8kk69ba952zw3453/b3s23 | 2026-11-19 10:32:50 ET | `#CSYNTH xs26_8kk69ba952zw3453 costs 32 gliders (true).` The cost is **32 and true (not pseudo)**. 27,635 bytes, sha256 a95b1034d24decdf023875c9af2c2cba1cfc0a4a1ae26e43ad1f9c3957630021. |
| xs26 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 | 2026-11-19 10:32:51 ET | `"xs26_8kk69ba952zw3453","100000000000000032"`, i.e. **32 (true)** (values of 10^17 or more are true syntheses, cost = value - 10^17). 106,531 valid xs26_ rows, 4,716,955 bytes, sha256 7c74e09466399ebc4dbec487019e1ec3ca21b2c0907e0ee5b9048f568f20aacc. This agrees with the object page. This CSV was fetched once and is the same class table used for the other xs26 package reviewed in this panel. |
| Input object page (derivation only) | https://catagolue.hatsya.com/object/xs27_g88ehmkia4z0178a6/b3s23 | 2026-11-19 10:32:53 ET | `#CSYNTH xs27_g88ehmkia4z0178a6 costs 12 gliders (true).` 7,208 bytes, sha256 5d31ba691bf0aaa8df06e88fb232100c8b25201fab0fb6e0e7437755b71c5d1a. The live xs27 CSV (fetched once at 2026-11-19 10:32:52 ET) has `"xs27_g88ehmkia4z0178a6","100000000000000012"` (12 true). 12 + 1 = 13. |

The live cost of the target is 32 true. The claimed 13 is strictly less (saving 19), so the improvement has not been absorbed into the table. The object-page and CSV hashes match those already recorded in the-record-we-beat/RECORD.md from a fetch about twelve minutes earlier (10:20:50–10:21:03 ET); the table had not moved. The listed cost of 32 is below 60, so partial win p1 is not available; the README correctly claims only the main success criterion. That scope decision is for the CRITERION skeptic.

## Construction (published input still life + 1 glider)

README.md and HOW_WE_FOUND_IT.md frame this honestly: the all-glider RLE is the published 12-glider Shinjuku route to `xs27_g88ehmkia4z0178a6` stitched with one new glider that turns that 27-cell still life into this 26-cell target. The new part is that 1-glider step. The packaged RLE is self-contained (all 13 gliders are in object/xs26_8kk69ba952zw3453.rle). No earlier V3R1T4S claim is used as a seed.

- The input still life is already in the live Catagolue table at 12 (true), as in the fetch above, so its route is public independently of this repo.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to that published 12-glider synthesis yields the input still life, not this target. Reaching the target needs the disclosed 1-glider step. That step applied to the still-listed 12-glider input gives 13, which strictly beats the live 32. The claim names its input and does not present the conversion as a previously published component.
- This object is not merged #969 (`xs26_08ehmkk8z6a87066`), not the other xs26 seed in this same four-package panel (`xs26_oo0o4qabqiczx321`), and not the #970 near-twin (`xs27_0ca1ugmicz651346`).

## Repo search (upstream elder-plinius/V3R1T4S, public API and raw files, no login)

- **TROPHY_CASE.md** on upstream `main` (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-11-19 10:33:02 ET, HTTP 200, 31,306 bytes): 0 matches for this apgcode, the input apgcode, or catagolue. The pinned kit copy is byte-identical and likewise has no match. The merged catagolue packages are in known-knowns/ but are not listed in TROPHY_CASE.md.
- **known-knowns/** on upstream `main` (contents API, 2026-11-19 10:33:02 ET): the family `catagolue-glider-synthesis-cost-records` exists and contains only `2026-11-06-whosedreams-a855292d` (merged #969, `xs26_08ehmkk8z6a87066`) and `2026-11-06-whosedreams-7c80a914` (merged #970, `xs27_0ca1ugmicz651346`). Neither README names this apgcode. The pinned kit tree has no catagolue family (those merges were after that pin).
- **Pull requests and issues** (public GitHub issue search, read-only, no login, 2026-11-19 10:33:02–10:33:45 ET): search for `8kk69ba952zw3453` and for `6912e4ea` returned 0. Search for `catagolue-glider-synthesis` returned five PRs, none of which is this object: #969 (merged; a different xs26), #970 (merged; an xs27), #1089 (open draft; `xs28_69a4owgzxol5d1d96`), #1171 (open draft; `xs28_08ehlmggoz6a87066`), and #1172 (open draft; `xs31_g8e1ugmmzd553w643`). I read those PR titles and bodies; they do not mention this apgcode.
- **Code search** via the GitHub Search API returned HTTP 401 unauthenticated at 2026-11-19 10:33:45 ET. I did not log in. The contents-API listing of the catagolue family and the issue/PR search above are the substitute.
- **Releases**: the repo has 0 releases (empty list, 2026-11-19 10:33:02 ET), so there are no release assets to check.

## Literature / web search (last 24 months)

- **Catagolue**: the live object page and the class CSV both show 32 (true) at the times above. Catagolue is assembled from Shinjuku and is the target's status table. Any synthesis already merged into Shinjuku and processed would show up here.
- **Web**: a general search for the exact apgcode (2026-11-19 about 10:33 ET) returned only unrelated commercial pages. A quoted search with catagolue, shinjuku or conwaylife returned general synthesis-index pages and, in one snippet, the official Catagolue object-page URL already fetched above; it did not name a cheaper cost or a prior claim. I found no LifeWiki article that names this apgcode.
- **ConwayLife forums**: I did not fetch or search the forums in this review. HOW_WE_FOUND_IT.md already discloses that the forums were not searched or read at packaging, and that a post giving only an RLE, without the apgcode, would not be found by such a search.
- **Shinjuku**: I did not crawl the GitLab tree file-by-file. Catagolue's still-listed 32 (true) is treated as the current official rendering of that database.

I found no published synthesis of `xs26_8kk69ba952zw3453` at 13 gliders or fewer, so none that ties or beats 13.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- I did not search the ConwayLife forums myself.
- GitHub code search required authentication, so I listed the merged known-knowns family and searched pull requests and issues instead.
- I did not crawl Mark Niemiec's synthesis collection separately; for this target the official cheapest-cost table is Catagolue.

## Verdict

novelty: PASS. The live true cost is 32 (object page and xs26 CSV, fetched 2026-11-19 10:32:50–10:32:51 ET). The claimed 13 strictly beats it. The claim is honestly framed as a published input still life (`xs27_g88ehmkia4z0178a6`, still listed at 12 true) plus one new glider, not as a derivative of an earlier V3R1T4S claim, and not as partial win p1 (listed cost 32 is below 60). The unread-forums limit is disclosed. I found nothing published that ties or beats 13.

pass: true
