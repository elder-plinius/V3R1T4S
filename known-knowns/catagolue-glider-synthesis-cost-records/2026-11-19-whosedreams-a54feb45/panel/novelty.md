# NOVELTY skeptic: xs28_08ehlmggoz6a87066 (claimed 15 gliders vs listed 61)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, INDEX.csv, how-we-built-it/TARGET_CRITERION.md, how-we-built-it/COMMANDS.md, how-we-built-it/data/harvest_verify.json, the-record-we-beat/RECORD.md. The file I replaced, panel/novelty.md, was a packaging-run stub labelled "not a fresh three-skeptic vote"; I did not treat it as evidence.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (ET, America/New_York, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-18 19:40:32 ET | HTTP 200, 63,325 bytes, sha256 6274f22f0a81959089983989ed08910f0d13576956778d9c006206704c2c7cda. Index page; no per-object cost. |
| Object page | https://catagolue.hatsya.com/object/xs28_08ehlmggoz6a87066/b3s23 | 2026-11-18 19:40:32 ET | `#CSYNTH xs28_08ehlmggoz6a87066 costs 61 gliders (true).` The cost is **61 and true (not pseudo)**. 8,240 bytes, sha256 4d3902ac9bb4f139b472518fe5f72c2de0b25c4c9caa569e9a9b3742abcdea48. |
| xs28 tabulation (HTML) | https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs28 | 2026-11-18 19:40:33 ET | HTTP 200, 566,342 bytes, sha256 0396049e84156df740d7a19463a47ecdd379ecafa047183c7b031e40ff7a9557. "Displaying 1 to 200 of 86549 objects", glider costs 242 down to 100. This object is not on page 1 (a cost of 61 is below that range), so the full-table CSV linked from this page is the class table used for the cell. |
| xs28 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs28 | 2026-11-18 19:40:34 ET | `"xs28_08ehlmggoz6a87066","100000000000000061"`, i.e. **61 (true)** (values of 10^17 or more are true syntheses, cost = value - 10^17). 86,549 valid xs28_ rows, 3,968,618 bytes, sha256 d32be9c573c45c67dce05aaa1a530bd3dc5713692b5f6e0918aab6fb49e50712. This agrees with the object page. |
| Seed object page | https://catagolue.hatsya.com/object/xs26_08ehmkk8z6a87066/b3s23 | 2026-11-18 19:40:32 ET | `#CSYNTH xs26_08ehmkk8z6a87066 costs 58 gliders (true).` The seed's listed cost is **58 and true (not pseudo)**. 8,128 bytes, sha256 6d7c65f1d62f690652a3659988b619194330047e82a4dbcd6678a850fb2d2745. |
| xs26 tabulation (HTML) | https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs26 | 2026-11-18 19:40:33 ET | HTTP 200. "Displaying 1 to 200 of 106531 objects", glider costs 178 down to 92. The seed is not on page 1. |
| xs26 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs26 | 2026-11-18 19:40:35 ET | `"xs26_08ehmkk8z6a87066","100000000000000058"`, i.e. **58 (true)**. 106,531 valid xs26_ rows, sha256 7c74e09466399ebc4dbec487019e1ec3ca21b2c0907e0ee5b9048f568f20aacc. This agrees with the seed object page. |

The live cost of the target is 61 true. The claimed 15 is strictly less (saving 46), so the improvement has not been absorbed into the table. The object-page and CSV hashes match those already recorded in the-record-we-beat/RECORD.md from a fetch about eleven minutes earlier; the table had not moved.

## Seed identification (cheaper synthesis from a cheaper seed, not a new converter)

README.md, HOW_WE_FOUND_IT.md and the "Not claimed" section frame this honestly: the all-glider RLE is the cheaper synthesis of the seed `xs26_08ehmkk8z6a87066` stitched with published Shinjuku components that add 3 gliders. The converters themselves are not claimed as new. The packaged RLE is self-contained (all 15 gliders are in object/xs28_08ehlmggoz6a87066.rle).

- Published seed in this repo: `xs26_08ehmkk8z6a87066`, 12 gliders, V3R1T4S PR #969 (package 2026-11-06-whosedreams-a855292d), merged upstream as 1209b9bf7906415e04bebbad2ef0a1d69cc5b626 at 2026-11-16 21:11:42 ET (2026-11-17T02:11:42Z). Confirmed from the public pull-request and commit APIs, no login. PR #969's body does not mention this xs28 target.
- Catagolue still lists that seed at 58 (true), as in the live fetches above.
- Using only that still-listed 58 plus the same 3 published-component gliders would cost 61, which ties the live cost of this object. The strict saving of 46 is entirely downstream of the cheaper seed. If the cheaper seed is later ingested by Shinjuku, Catagolue will recompute and this listed cost will drop.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to the published 12-glider synthesis of the seed yields the seed, not this 28-cell still life. Reaching the target needs the (disclosed, not-new) component steps. Those steps applied to Catagolue's still-listed 58-glider seed only tie 61; applied to the named 12-glider seed they give 15, which strictly beats the live table. The claim names its seed and does not present the transfer as a new converter.

## Repo search (upstream elder-plinius/V3R1T4S, public API and raw files, no login)

- **TROPHY_CASE.md** on upstream `main` (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-11-18 19:41:52 ET, HTTP 200, 31,083 bytes): 0 matches for this apgcode, the seed apgcode, catagolue, or glider. The merged #969 package is in known-knowns/ but is not yet listed in TROPHY_CASE.md. The pinned kit copy of TROPHY_CASE.md is byte-identical and likewise has no match.
- **known-knowns/** on upstream `main` (contents API, 2026-11-18 19:41:52–19:41:53 ET): the family `catagolue-glider-synthesis-cost-records` exists and contains only `2026-11-06-whosedreams-a855292d` (the seed package from PR #969). It does not contain this xs28 object. The pinned kit tree has no catagolue family (the merge was after that pin).
- **bank/** in the pinned kit: the only match is the target definition itself (`catagolue-glider-synthesis-cost-records`). The target writeup is known-unknowns/graphs-games-automata/catagolue-glider-synthesis-cost-records.md. No prior result for this object is recorded there.
- **Pull requests** (public GitHub issue search and pull APIs, read-only, no login, 2026-11-18 19:41:04–19:41:53 ET): search for `08ehlmggoz6a87066` and for `a54feb45` returned 0. Search for `catagolue-glider-synthesis` returned three PRs, none of which is this object: #969 (merged; the seed), #970 (open draft; `xs27_0ca1ugmicz651346`), and #1089 (open draft; `xs28_69a4owgzxol5d1d96`, a different xs28). Bodies of #970 and #1089 do not mention this apgcode.
- **Code search** via the GitHub Search API returned HTTP 401 unauthenticated. I did not log in. The contents-API listing of the catagolue family above is the substitute.
- **Releases**: the repo has 0 releases (empty list, 2026-11-18 19:41:53 ET), so there are no release assets to check.

## Literature / web search (last 24 months)

- **Catagolue**: the live object page and the class CSV both show 61 (true) at the times above. Catagolue is assembled from Shinjuku and is the target's status table. Any synthesis already merged into Shinjuku and processed would show up here.
- **Web**: searches for the exact apgcode, and for `08ehlmggoz6a87066` together with catagolue, shinjuku or conwaylife, returned no relevant hits (unrelated product and identifier pages only). A `site:conwaylife.com` search and a `site:gitlab.com/parclytaxel/Shinjuku` search did not surface this code. I found no LifeWiki page that names it.
- **ConwayLife forums**: a shell fetch of the forum search at 2026-11-18 19:42:03 ET was blocked by Cloudflare (HTTP 403, page title "Just a moment..."). I did not retry. I rely on the recorded browser text-only search at about 19:27 ET on 2026-11-18, which found 0 hits for this object's suffix, for the seed suffix, and for the full apgcodes. That search was text-only: a post that gave only an RLE, without the apgcode, would not have been found.
- **Shinjuku**: I did not crawl the GitLab tree file-by-file. Catagolue's still-listed 61 (true) is treated as the current official rendering of that database.

I found no published synthesis of `xs28_08ehlmggoz6a87066` at 15 gliders or fewer, so none that ties or beats 15.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- The forum check I can stand behind is the recorded text-only browser search; my own shell fetch was blocked.
- GitHub code search required authentication, so I listed the merged known-knowns family and searched pull requests instead.
- I did not crawl Mark Niemiec's synthesis collection separately; for this target the official cheapest-cost table is Catagolue.

## Verdict

novelty: PASS. The live true cost is 61 (object page and xs28 CSV, fetched 2026-11-18 19:40:32–19:40:34 ET). The claimed 15 strictly beats it. The claim is honestly framed as a cheaper synthesis derived from the named cheaper seed `xs26_08ehmkk8z6a87066` (12 gliders, merged PR #969; Catagolue still lists 58 true) plus published components, not as a new converter. I found nothing published that ties or beats 15.

pass: true
