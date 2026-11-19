# NOVELTY skeptic: xs25_69ar1mkiczx643 (claimed 21 gliders vs listed 49)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, INDEX.csv, how-we-built-it/TARGET_CRITERION.md, the-record-we-beat/RECORD.md. I did not treat panel/gate.md (a packaging-run PROMISING draft) as evidence.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (ET, America/New_York, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-19 10:32:52 ET | HTTP 200, 63,325 bytes, sha256 6274f22f0a81959089983989ed08910f0d13576956778d9c006206704c2c7cda. Index page; no per-object cost. |
| Object page | https://catagolue.hatsya.com/object/xs25_69ar1mkiczx643/b3s23 | 2026-11-19 10:32:50 ET | `#CSYNTH xs25_69ar1mkiczx643 costs 49 gliders (true).` The cost is **49 and true (not pseudo)**. 8,618 bytes, sha256 3d492c75d15077174c94f95bfac015352cbbc65d8383259ee537c825bfc32fa1. |
| xs25 tabulation (full CSV) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs25 | 2026-11-19 10:32:51 ET | `"xs25_69ar1mkiczx643","100000000000000049"`, i.e. **49 (true)** (values of 10^17 or more are true syntheses, cost = value - 10^17). 106,730 valid xs25_ rows, 4,658,021 bytes, sha256 7a22074cb023f5c8fa976c1b7886e49adf76e3112d3a96ec5127bdf94ab8e7d3. This agrees with the object page. |
| Input object page (derivation only) | https://catagolue.hatsya.com/object/xs27_cikm1da4ozxd8711/b3s23 | 2026-11-19 10:32:53 ET | `#CSYNTH xs27_cikm1da4ozxd8711 costs 20 gliders (true).` 7,295 bytes, sha256 b8a48fd189d6cc8423e55912395dd8231d9a1ac97242c5d17d6180f41ff35c63. The live xs27 CSV (fetched once at 2026-11-19 10:32:52 ET) has `"xs27_cikm1da4ozxd8711","100000000000000020"` (20 true). 20 + 1 = 21. |

The live cost of the target is 49 true. The claimed 21 is strictly less (saving 28), so the improvement has not been absorbed into the table. The object-page and CSV hashes match those already recorded in the-record-we-beat/RECORD.md from a fetch about twelve minutes earlier (10:20:47–10:20:58 ET); the table had not moved. The listed cost of 49 is below 60, so partial win p1 is not available; the README correctly claims only the main success criterion. That scope decision is for the CRITERION skeptic.

## Construction (published input still life + 1 glider)

README.md and HOW_WE_FOUND_IT.md frame this honestly: the all-glider RLE is the published 20-glider Shinjuku route to `xs27_cikm1da4ozxd8711` stitched with one new glider that turns that 27-cell still life into this 25-cell target. The new part is that 1-glider step. The packaged RLE is self-contained (all 21 gliders are in object/xs25_69ar1mkiczx643.rle). No earlier V3R1T4S claim is used as a seed.

- The input still life is already in the live Catagolue table at 20 (true), as in the fetch above, so its route is public independently of this repo.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to that published 20-glider synthesis yields the input still life, not this 25-cell target. Reaching the target needs the disclosed 1-glider step. That step applied to the still-listed 20-glider input gives 21, which strictly beats the live 49. The claim names its input and does not present the conversion as a previously published component.
- This object is not the merged #970 near-twin (`xs27_0ca1ugmicz651346`) or any other prior V3R1T4S catagolue claim (see repo search below).

## Repo search (upstream elder-plinius/V3R1T4S, public API and raw files, no login)

- **TROPHY_CASE.md** on upstream `main` (https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-11-19 10:33:02 ET, HTTP 200, 31,306 bytes): 0 matches for this apgcode, the input apgcode, or catagolue. The pinned kit copy is byte-identical and likewise has no match. The merged catagolue packages are in known-knowns/ but are not listed in TROPHY_CASE.md.
- **known-knowns/** on upstream `main` (contents API, 2026-11-19 10:33:02 ET): the family `catagolue-glider-synthesis-cost-records` exists and contains only `2026-11-06-whosedreams-a855292d` (merged #969, `xs26_08ehmkk8z6a87066`) and `2026-11-06-whosedreams-7c80a914` (merged #970, `xs27_0ca1ugmicz651346`). Neither README names this apgcode. The pinned kit tree has no catagolue family (those merges were after that pin).
- **Pull requests and issues** (public GitHub issue search, read-only, no login, 2026-11-19 10:33:02–10:33:45 ET): search for `69ar1mkiczx643` and for `2dc7924d` returned 0. Search for `catagolue-glider-synthesis` returned five PRs, none of which is this object: #969 (merged; an xs26), #970 (merged; an xs27 near-twin of a different package, not this one), #1089 (open draft; `xs28_69a4owgzxol5d1d96`), #1171 (open draft; `xs28_08ehlmggoz6a87066`), and #1172 (open draft; `xs31_g8e1ugmmzd553w643`). I read those PR titles and bodies; they do not mention this apgcode.
- **Code search** via the GitHub Search API returned HTTP 401 unauthenticated at 2026-11-19 10:33:45 ET. I did not log in. The contents-API listing of the catagolue family and the issue/PR search above are the substitute.
- **Releases**: the repo has 0 releases (empty list, 2026-11-19 10:33:02 ET), so there are no release assets to check.

## Literature / web search (last 24 months)

- **Catagolue**: the live object page and the class CSV both show 49 (true) at the times above. Catagolue is assembled from Shinjuku and is the target's status table. Any synthesis already merged into Shinjuku and processed would show up here.
- **Web**: a general search for the exact apgcode (2026-11-19 about 10:33 ET) returned only unrelated commercial pages. A quoted search with catagolue, shinjuku or conwaylife returned only general synthesis-index and LifeWiki pages, not a page that names this apgcode or a cheaper cost. I found no LifeWiki article that names it.
- **ConwayLife forums**: I did not fetch or search the forums in this review. HOW_WE_FOUND_IT.md already discloses that the forums were not searched or read at packaging, and that a post giving only an RLE, without the apgcode, would not be found by such a search.
- **Shinjuku**: I did not crawl the GitLab tree file-by-file. Catagolue's still-listed 49 (true) is treated as the current official rendering of that database.

I found no published synthesis of `xs25_69ar1mkiczx643` at 21 gliders or fewer, so none that ties or beats 21.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- I did not search the ConwayLife forums myself.
- GitHub code search required authentication, so I listed the merged known-knowns family and searched pull requests and issues instead.
- I did not crawl Mark Niemiec's synthesis collection separately; for this target the official cheapest-cost table is Catagolue.

## Verdict

novelty: PASS. The live true cost is 49 (object page and xs25 CSV, fetched 2026-11-19 10:32:50–10:32:51 ET). The claimed 21 strictly beats it. The claim is honestly framed as a published input still life (`xs27_cikm1da4ozxd8711`, still listed at 20 true) plus one new glider, not as a derivative of an earlier V3R1T4S claim, and not as partial win p1 (listed cost 49 is below 60). The unread-forums limit is disclosed. I found nothing published that ties or beats 21.

pass: true
