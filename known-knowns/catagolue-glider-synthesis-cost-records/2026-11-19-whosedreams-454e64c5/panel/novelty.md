# NOVELTY skeptic: xs31_g8e1ugmmzd553w643 (claimed 14 gliders vs listed 60)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, INDEX.csv, how-we-built-it/TARGET_CRITERION.md, how-we-built-it/COMMANDS.md, how-we-built-it/data/harvest_verify.json, the-record-we-beat/RECORD.md. The file I replaced, panel/novelty.md, was a packaging-run stub labelled "not a fresh three-skeptic vote"; I did not treat it as evidence.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (ET, America/New_York, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-18 19:40:32 ET | HTTP 200, 63,325 bytes, sha256 6274f22f0a81959089983989ed08910f0d13576956778d9c006206704c2c7cda. Index page; no per-object cost. |
| Object page | https://catagolue.hatsya.com/object/xs31_g8e1ugmmzd553w643/b3s23 | 2026-11-18 19:40:32 ET | `#CSYNTH xs31_g8e1ugmmzd553w643 costs 60 gliders (true).` The cost is **60 and true (not pseudo)**. 8,447 bytes, sha256 4f18b74b7b06f34c161507798f2a2ba8f568f97fd1041242b7d333193cdfe9a2. |
| xs31 tabulation (HTML) | https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs31 | 2026-11-18 19:40:33 ET | HTTP 200, 620,415 bytes, sha256 53250a15d8a022299c1f8fb1fa441faf51fcba88f9eddfc531a206c474b423e7. "Displaying 1 to 200 of 45939 objects", glider costs 254 down to 105. This object is not on page 1 (a cost of 60 is below that range), so the full-table CSV linked from this page is the class table used for the cell. |
| xs31 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs31 | 2026-11-18 19:40:34 ET | `"xs31_g8e1ugmmzd553w643","100000000000000060"`, i.e. **60 (true)** (values of 10^17 or more are true syntheses, cost = value - 10^17). 45,939 valid xs31_ rows, 2,203,035 bytes, sha256 83b06ac0d229fa243d8ebdf621900fb3325bd9a6949e65677f81d1ed62e7c422. This agrees with the object page. |
| Seed object page | https://catagolue.hatsya.com/object/xs26_08ehmkk8z6a87066/b3s23 | 2026-11-18 19:40:32 ET | `#CSYNTH xs26_08ehmkk8z6a87066 costs 58 gliders (true).` The seed's listed cost is **58 and true (not pseudo)**. 8,128 bytes, sha256 6d7c65f1d62f690652a3659988b619194330047e82a4dbcd6678a850fb2d2745. |
| xs26 tabulation (HTML) | https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs26 | 2026-11-18 19:40:33 ET | HTTP 200. "Displaying 1 to 200 of 106531 objects", glider costs 178 down to 92. The seed is not on page 1. |
| xs26 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 | 2026-11-18 19:40:35 ET | `"xs26_08ehmkk8z6a87066","100000000000000058"`, i.e. **58 (true)**. 106,531 valid xs26_ rows, sha256 7c74e09466399ebc4dbec487019e1ec3ca21b2c0907e0ee5b9048f568f20aacc. This agrees with the seed object page. |

The live cost of the target is 60 true. The claimed 14 is strictly less (saving 46), so the improvement has not been absorbed into the table. The object-page and CSV hashes match those already recorded in the-record-we-beat/RECORD.md from a fetch about eleven minutes earlier; the table had not moved. The listed cost of 60 is at least 60, which is the p1 threshold; that threshold itself is for the CRITERION skeptic.

## Seed identification (cheaper synthesis from a cheaper seed, not a new converter)

README.md, HOW_WE_FOUND_IT.md and the "Not claimed" section frame this honestly: the all-glider RLE is the cheaper synthesis of the seed `xs26_08ehmkk8z6a87066` stitched with published Shinjuku components that add 2 gliders. The converters themselves are not claimed as new. The packaged RLE is self-contained (all 14 gliders are in object/xs31_g8e1ugmmzd553w643.rle).

- Published seed in this repo: `xs26_08ehmkk8z6a87066`, 12 gliders, V3R1T4S PR #969 (package 2026-11-06-whosedreams-a855292d), merged upstream as 1209b9bf7906415e04bebbad2ef0a1d69cc5b626 at 2026-11-16 21:11:42 ET (2026-11-17T02:11:42Z). Confirmed from the public pull-request and commit APIs, no login. PR #969's body does not mention this xs31 target.
- Catagolue still lists that seed at 58 (true), as in the live fetches above.
- Using only that still-listed 58 plus the same 2 published-component gliders would cost 60, which ties the live cost of this object. The strict saving of 46 is entirely downstream of the cheaper seed. If the cheaper seed is later ingested by Shinjuku, Catagolue will recompute and this listed cost will drop.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to the published 12-glider synthesis of the seed yields the seed, not this 31-cell still life. Reaching the target needs the (disclosed, not-new) component steps. Those steps applied to Catagolue's still-listed 58-glider seed only tie 60; applied to the named 12-glider seed they give 14, which strictly beats the live table. The claim names its seed and does not present the transfer as a new converter.

## Repo search (upstream elder-plinius/V3R1T4S, public API and raw files, no login)

- **TROPHY_CASE.md** on upstream `main` (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-11-18 19:41:52 ET, HTTP 200, 31,083 bytes): 0 matches for this apgcode, the seed apgcode, catagolue, or glider. The merged #969 package is in known-knowns/ but is not yet listed in TROPHY_CASE.md. The pinned kit copy of TROPHY_CASE.md is byte-identical and likewise has no match.
- **known-knowns/** on upstream `main` (contents API, 2026-11-18 19:41:52–19:41:53 ET): the family `catagolue-glider-synthesis-cost-records` exists and contains only `2026-11-06-whosedreams-a855292d` (the seed package from PR #969). It does not contain this xs31 object. The pinned kit tree has no catagolue family (the merge was after that pin).
- **bank/** in the pinned kit: the only match is the target definition itself (`catagolue-glider-synthesis-cost-records`). The target writeup is known-unknowns/graphs-games-automata/catagolue-glider-synthesis-cost-records.md. No prior result for this object is recorded there.
- **Pull requests** (public GitHub issue search and pull APIs, read-only, no login, 2026-11-18 19:41:04–19:41:53 ET): search for `g8e1ugmmzd553w643` and for `454e64c5` returned 0. Search for `catagolue-glider-synthesis` returned three PRs, none of which is this object: #969 (merged; the seed), #970 (open draft; `xs27_0ca1ugmicz651346`), and #1089 (open draft; `xs28_69a4owgzxol5d1d96`). Bodies of #970 and #1089 do not mention this apgcode.
- **Code search** via the GitHub Search API returned HTTP 401 unauthenticated. I did not log in. The contents-API listing of the catagolue family above is the substitute.
- **Releases**: the repo has 0 releases (empty list, 2026-11-18 19:41:53 ET), so there are no release assets to check.

## Literature / web search (last 24 months)

- **Catagolue**: the live object page and the class CSV both show 60 (true) at the times above. Catagolue is assembled from Shinjuku and is the target's status table. Any synthesis already merged into Shinjuku and processed would show up here.
- **Web**: searches for the exact apgcode, and for `g8e1ugmmzd553w643` together with catagolue, shinjuku or conwaylife, returned no relevant hits (unrelated identifier pages only). A `site:conwaylife.com` search and a `site:gitlab.com/parclytaxel/Shinjuku` search did not surface this code. I found no LifeWiki page that names it.
- **ConwayLife forums**: a shell fetch of the forum search at 2026-11-18 19:42:03 ET was blocked by Cloudflare (HTTP 403, page title "Just a moment..."). I did not retry. I rely on the recorded browser text-only search at about 19:27 ET on 2026-11-18, which found 0 hits for this object's suffix, for the seed suffix, and for the full apgcodes. That search was text-only: a post that gave only an RLE, without the apgcode, would not have been found.
- **Shinjuku**: I did not crawl the GitLab tree file-by-file. Catagolue's still-listed 60 (true) is treated as the current official rendering of that database.

I found no published synthesis of `xs31_g8e1ugmmzd553w643` at 14 gliders or fewer, so none that ties or beats 14.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- The forum check I can stand behind is the recorded text-only browser search; my own shell fetch was blocked.
- GitHub code search required authentication, so I listed the merged known-knowns family and searched pull requests instead.
- I did not crawl Mark Niemiec's synthesis collection separately; for this target the official cheapest-cost table is Catagolue.

## Verdict

novelty: PASS. The live true cost is 60 (object page and xs31 CSV, fetched 2026-11-18 19:40:32–19:40:34 ET). The claimed 14 strictly beats it. The claim is honestly framed as a cheaper synthesis derived from the named cheaper seed `xs26_08ehmkk8z6a87066` (12 gliders, merged PR #969; Catagolue still lists 58 true) plus published components, not as a new converter. I found nothing published that ties or beats 14.

pass: true
