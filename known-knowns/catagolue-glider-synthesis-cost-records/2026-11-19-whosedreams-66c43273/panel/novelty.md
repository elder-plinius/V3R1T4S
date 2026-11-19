# NOVELTY skeptic: xs26_oo0o4qabqiczx321 (claimed 11 gliders vs listed 35)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, INDEX.csv, how-we-built-it/TARGET_CRITERION.md, the-record-we-beat/RECORD.md. I did not treat panel/gate.md (a packaging-run PROMISING draft) as evidence.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (ET, America/New_York, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-19 10:32:52 ET | HTTP 200, 63,325 bytes, sha256 6274f22f0a81959089983989ed08910f0d13576956778d9c006206704c2c7cda. Index page; no per-object cost. |
| Object page | https://catagolue.hatsya.com/object/xs26_oo0o4qabqiczx321/b3s23 | 2026-11-19 10:32:50 ET | `#CSYNTH xs26_oo0o4qabqiczx321 costs 35 gliders (true).` The cost is **35 and true (not pseudo)**. 7,702 bytes, sha256 1e64fedef8a336ed851116ea8c026b98514d2fde54417eadfb504a497df7f07b. |
| xs26 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 | 2026-11-19 10:32:51 ET | `"xs26_oo0o4qabqiczx321","100000000000000035"`, i.e. **35 (true)** (values of 10^17 or more are true syntheses, cost = value - 10^17). 106,531 valid xs26_ rows, 4,716,955 bytes, sha256 7c74e09466399ebc4dbec487019e1ec3ca21b2c0907e0ee5b9048f568f20aacc. This agrees with the object page. This CSV was fetched once and is the same class table used for the other xs26 package reviewed in this panel. |
| Input object page (derivation only) | https://catagolue.hatsya.com/object/xs27_3lkmz01iu1u8zw1221/b3s23 | 2026-11-19 10:32:53 ET | `#CSYNTH xs27_3lkmz01iu1u8zw1221 costs 10 gliders (true).` 7,231 bytes, sha256 7d84e0a937d509d2a16c2937ff2d7e8c468be3bac51c3b75eee01a2e3aa5ef34. The live xs27 CSV (fetched once at 2026-11-19 10:32:52 ET) has `"xs27_3lkmz01iu1u8zw1221","100000000000000010"` (10 true). 10 + 1 = 11. |

The live cost of the target is 35 true. The claimed 11 is strictly less (saving 24), so the improvement has not been absorbed into the table. The object-page and CSV hashes match those already recorded in the-record-we-beat/RECORD.md from a fetch about twelve minutes earlier (10:20:50–10:21:00 ET); the table had not moved. The listed cost of 35 is below 60, so partial win p1 is not available; the README correctly claims only the main success criterion. That scope decision is for the CRITERION skeptic.

## Construction (published input still life + 1 glider)

README.md and HOW_WE_FOUND_IT.md frame this honestly: the all-glider RLE is the published 10-glider Shinjuku route to `xs27_3lkmz01iu1u8zw1221` stitched with one new glider that turns that 27-cell still life into this 26-cell target. The new part is that 1-glider step. The packaged RLE is self-contained (all 11 gliders are in object/xs26_oo0o4qabqiczx321.rle). No earlier V3R1T4S claim is used as a seed.

- The input still life is already in the live Catagolue table at 10 (true), as in the fetch above, so its route is public independently of this repo.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to that published 10-glider synthesis yields the input still life, not this target. Reaching the target needs the disclosed 1-glider step. That step applied to the still-listed 10-glider input gives 11, which strictly beats the live 35. The claim names its input and does not present the conversion as a previously published component.
- This object is not merged #969 (`xs26_08ehmkk8z6a87066`), not the other xs26 seed in this same four-package panel (`xs26_8kk69ba952zw3453`), and not the #970 near-twin (`xs27_0ca1ugmicz651346`).

## Repo search (upstream elder-plinius/V3R1T4S, public API and raw files, no login)

- **TROPHY_CASE.md** on upstream `main` (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-11-19 10:33:02 ET, HTTP 200, 31,306 bytes): 0 matches for this apgcode, the input apgcode, or catagolue. The pinned kit copy is byte-identical and likewise has no match. The merged catagolue packages are in known-knowns/ but are not listed in TROPHY_CASE.md.
- **known-knowns/** on upstream `main` (contents API, 2026-11-19 10:33:02 ET): the family `catagolue-glider-synthesis-cost-records` exists and contains only `2026-11-06-whosedreams-a855292d` (merged #969, `xs26_08ehmkk8z6a87066`) and `2026-11-06-whosedreams-7c80a914` (merged #970, `xs27_0ca1ugmicz651346`). Neither README names this apgcode. The pinned kit tree has no catagolue family (those merges were after that pin).
- **Pull requests and issues** (public GitHub issue search, read-only, no login, 2026-11-19 10:33:02–10:33:45 ET): search for `oo0o4qabqiczx321` and for `66c43273` returned 0. Search for `catagolue-glider-synthesis` returned five PRs, none of which is this object: #969 (merged; a different xs26), #970 (merged; an xs27), #1089 (open draft; `xs28_69a4owgzxol5d1d96`), #1171 (open draft; `xs28_08ehlmggoz6a87066`), and #1172 (open draft; `xs31_g8e1ugmmzd553w643`). I read those PR titles and bodies; they do not mention this apgcode.
- **Code search** via the GitHub Search API returned HTTP 401 unauthenticated at 2026-11-19 10:33:45 ET. I did not log in. The contents-API listing of the catagolue family and the issue/PR search above are the substitute.
- **Releases**: the repo has 0 releases (empty list, 2026-11-19 10:33:02 ET), so there are no release assets to check.

## Literature / web search (last 24 months)

- **Catagolue**: the live object page and the class CSV both show 35 (true) at the times above. Catagolue is assembled from Shinjuku and is the target's status table. Any synthesis already merged into Shinjuku and processed would show up here.
- **Web**: a general search for the exact apgcode (2026-11-19 about 10:33 ET) returned only unrelated pages. A quoted search with catagolue, shinjuku or conwaylife returned general synthesis-index pages and, in one snippet, the official Catagolue object-page URL already fetched above; it did not name a cheaper cost or a prior claim. I found no LifeWiki article that names this apgcode.
- **ConwayLife forums**: I did not fetch or search the forums in this review. HOW_WE_FOUND_IT.md already discloses that the forums were not searched or read at packaging, and that a post giving only an RLE, without the apgcode, would not be found by such a search.
- **Shinjuku**: I did not crawl the GitLab tree file-by-file. Catagolue's still-listed 35 (true) is treated as the current official rendering of that database.

I found no published synthesis of `xs26_oo0o4qabqiczx321` at 11 gliders or fewer, so none that ties or beats 11.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- I did not search the ConwayLife forums myself.
- GitHub code search required authentication, so I listed the merged known-knowns family and searched pull requests and issues instead.
- I did not crawl Mark Niemiec's synthesis collection separately; for this target the official cheapest-cost table is Catagolue.

## Verdict

novelty: PASS. The live true cost is 35 (object page and xs26 CSV, fetched 2026-11-19 10:32:50–10:32:51 ET). The claimed 11 strictly beats it. The claim is honestly framed as a published input still life (`xs27_3lkmz01iu1u8zw1221`, still listed at 10 true) plus one new glider, not as a derivative of an earlier V3R1T4S claim, and not as partial win p1 (listed cost 35 is below 60). The unread-forums limit is disclosed. I found nothing published that ties or beats 11.

pass: true
