# Verdict

The 7-glider pattern is a valid all-glider synthesis of the strict still life `xs28_69a4owgzxol5d1d96`, and that apgcode is absent from the live Catagolue xs28 synthesis-cost table. The object page is a real 200 response for that apgcode and contains no `#CSYNTH` line. This meets the table first-synthesis criterion for an unlisted strict still life.

The route is the published 6-glider synthesis of `xs25_0ml1u8z643032ak8` plus one glider. It is a new table row reached by that disclosed extension. It is a different object from the predecessor (28 cells versus 25).

pass: true

## Context

context: This session began as a fresh headless agent CLI.

Fresh headless agent CLI. Work stayed in this directory and in `claim/`. No sibling directories, transcripts, or other skeptics were read. No GitHub login, writes, installs, or browser impersonation. Jobs were `nice -n 19` and single-threaded. Primary Catagolue URLs were fetched once each, with curl's default user agent and `--retry 0`. Both returned HTTP 200 on the first attempt.

The author's `ok: false` in `claim/result/xs28_69a4owgzxol5d1d96.json` was not used. That verifier only accepts a numeric `#CSYNTH` cost and records the HTML page as a failed cost fetch. The page is the object page; it has no cost line.

## Method

1. Fetch and hash the xs28 synthesis-cost census and the hero object page. Accept the census only if it is a complete plain-text table of plausible `xs28_` rows. Accept the object page only if it is a real Catagolue object page for this apgcode. Absence of the apgcode and of `#CSYNTH` counts only after that positive identification.
2. Decode the apgcode and test the still-life predicate directly: every live cell has 2 or 3 live neighbours, and no dead cell has exactly 3.
3. Exhaust every nonempty proper subset of the 28 cells with an uncapped bitmask loop. A subset is stable only under that same predicate, including births on cells that are live in the full pattern but dead in the subset, and births on exterior dead cells. If a subset is stable, test the complement the same way. The pattern is pseudo when both sides are stable. Five found subsets were rechecked with a grid Life step and with an independent Python step.
4. A separate pruner assigns cells in order and drops a branch only when every completion is already illegal. It was required to match the flat loop on every control.
5. Simulate the claimed RLE with a separate standard-library checker: glider components, rewind, and exact ash. Cross-check with `claim/code/life_check.py`.
6. Read the pinned trophy and known-knowns files. Fetch the predecessor object and its synthesis sample. Search public GitHub issues and pull requests, and search the public Shinjuku component files named below.

Strictness is the partition test above. An 8-connected component count is reported only as a contrast with that test. The target has two Moore components, and neither component is stable, so a component count would misclassify it.

### Why the pruning is sound

Cells are assigned in a fixed order, in or out. A partial assignment is discarded only in two cases. An already-in cell whose assigned in-neighbours already exceed 3, or whose assigned in-neighbours plus still-unassigned pattern neighbours are fewer than 2, dies in every completion. An already-out cell, or an exterior dead cell, whose pattern neighbours are all assigned and of which exactly 3 are in, is a birth in every completion. Any stable subset survives every prefix of its assignment, so the discarded branches contain none. There is no population cap and no connectivity filter. On every control of at most 8 cells the pruned counts matched the flat `2^n - 2` loop, including one pseudo partition for each two-block pattern and zero partitions for the aircraft carrier.

The 28-cell measurement itself is the flat loop, which tests every nonempty proper mask. The grid stepper agreed with the bit test on every mask of every control through 8 cells, and on every mask the bit test called stable in the 28-cell pattern, together with that mask's complement.

## Primary fetches

Census `https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs28`

Command:

```
nice -n 19 curl -sS --retry 0 --max-time 180 -D out/textcensus_xs28.headers -o out/textcensus_xs28.raw -w "curl_http=%{http_code} curl_size=%{size_download} curl_time=%{time_total}\n" "https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs28"
```

Local clock before the request: 2026-11-06T22:00:33.851310Z, 2026-11-06T17:00:33.851310-05:00. Response `Date: Fri, 06 Nov 2026 22:00:34 GMT`. Clock after: 2026-11-06T22:00:34.597128Z, 2026-11-06T17:00:34.597128-05:00. HTTP 200, `content-type: text/plain;charset=iso-8859-1`, `content-length: 3925886`, curl size 3925886, curl exit 0. Body SHA256 `8609d21c267e51083574a20019c741745ee37ef31305cee3c9051b6d1c4dc95a`. Header SHA256 `5f6ea28d124e3d38368f88208662c9d5cc7ee84bf9e81b6c6124e930c94e622f`.

The body is 85616 LF-terminated lines. Line 1 is `"apgcode","occurrences"`. The other 85615 lines each match `"xs28_"`, lowercase apgcode suffix, `","`, and a decimal cost. All 85615 apgcodes are unique. Costs are nonincreasing (0 inversions). Values `>= 10^17` are true-synthesis marks: 77685 rows, adjusted cost 5 through 181. Values below that are pseudo costs: 7930 rows, cost 3 through 136. The exact string `xs28_69a4owgzxol5d1d96` occurs 0 times. 152 other rows share the prefix `xs28_69a4`.

Object `https://catagolue.hatsya.com/object/xs28_69a4owgzxol5d1d96/b3s23`

Command:

```
nice -n 19 curl -sS --retry 0 --max-time 180 -D out/object_hero.headers -o out/object_hero.raw -w "curl_http=%{http_code} curl_size=%{size_download} curl_time=%{time_total}\n" "https://catagolue.hatsya.com/object/xs28_69a4owgzxol5d1d96/b3s23"
```

Clock before: 2026-11-06T22:00:49.639399Z, 2026-11-06T17:00:49.639399-05:00. Response `Date: Fri, 06 Nov 2026 22:00:49 GMT`. Clock after: 2026-11-06T22:00:49.931558Z, 2026-11-06T17:00:49.931558-05:00. HTTP 200, `content-type: text/html;charset=utf-8`, `content-length: 8455`, curl exit 0. Body SHA256 `a9eb249b1e832076f8b6b5c4ffea252da42181a27feec10e5547082a1d962005`. Header SHA256 `f03271571650f720366b8a183d9c60c1110438fda105098e0a2aa45d16166496`.

Title is `xs28_69a4owgzxol5d1d96 - Catagolue`. The page says the pattern is a still-life, period 1, population constantly 28, in standard life b3s23. `#CSYNTH` and `csynth` occur 0 times. There is no synthesis section. The census block lists 10 sample soups: 1 in symmetry C2_1 and 9 in `mvr_component_stdin`. Comments are 0. A later one-shot fetch of `https://catagolue.hatsya.com/textsamples/xs28_69a4owgzxol5d1d96/b3s23/synthesis` returned HTTP 200 and the five bytes `null\n`.

## Strict still life

Checker: `out/strict_enum.c`, compiled and run as:

```
nice -n 19 gcc -O2 -o out/strict_enum out/strict_enum.c
nice -n 19 ./out/strict_enum
```

Controls, flat loop and pruner agreeing:

| pattern | still | 8-components | stable proper subsets | unordered stable partitions | class |
|---|---|---|---|---|---|
| block | yes | 1 | 0 | 0 | STRICT |
| barge `xs6_696` | yes | 1 | 0 | 0 | STRICT |
| aircraft carrier | yes | 2 | 0 | 0 | STRICT |
| bi-block | yes | 2 | 2 | 1 | PSEUDO |
| two separated blocks | yes | 2 | 2 | 1 | PSEUDO |
| blinker | no | 1 |  |  | UNSTABLE |
| L triomino | no | 1 |  |  | UNSTABLE |

The separated-block and bi-block cases are pseudo, so the checker fails those patterns. The aircraft carrier is strict even though it has two Moore components; neither half is stable. The blinker and the L triomino are rejected before any subset search.

Decoded target: 28 cells, one Life step fixes the pattern, bounding box 11 by 10. Moore components have 21 and 7 cells. Each component alone births at the dead cell (5, 6); the 21-cell piece also births at (6, 6). Together the pattern is stable, so those two components are not a pseudo split.

Flat enumeration of all `2^28 - 2` nonempty proper subsets found exactly five stable subsets. All five complements are unstable under both the bit test and the grid step. Python `step` on the same cell lists agreed. No subcollection of the five is pairwise disjoint and covers all 28 cells, so there is no partition into two or more stable pieces.

The five subsets:

- 7 cells, mask `0x7f`: `(0,1) (0,2) (1,0) (1,3) (2,1) (2,3) (3,2)`. Complement 21, unstable.
- 11 cells, mask `0x91ff`: that 7-cell still life plus `(4,3) (4,4) (4,5) (5,5)`. Complement 17, unstable.
- 6 cells, mask `0xd4c00`: a ship, `(3,8) (3,9) (4,9) (5,7) (6,7) (6,8)`. Complement 22, unstable.
- 13 cells, mask `0xd4c7f`: the disjoint union of the 7-cell still life and the ship. Complement 15, unstable.
- 20 cells, mask `0xfffff00`. Complement 8, unstable.

Class recorded by the program: STRICT. Stable proper subsets exist. Their complements are not stable, so the pattern is not pseudo.

## Synthesis

`nice -n 19 python3 out/check_synth.py` on `claim/result/xs28_69a4owgzxol5d1d96.rle`:

- rule B3/S23, generation-0 population 35, 7 components, each a glider
- bounding box 204 by 213
- rewind at T=852 and T=1176: no interaction, returns to generation 0
- forward: exact repeat at generation 759, period 1, population 28, matches the decoded target under rotation and reflection
- deleting the glider whose minimum cell is `(0, 2)`, direction `(1, 1)`, yields period 1, population 25, matching `xs25_0ml1u8z643032ak8`
- the other six single deletions do not build the target

`nice -n 19 python3 claim/code/life_check.py --rle claim/result/xs28_69a4owgzxol5d1d96.rle --target xs28_69a4owgzxol5d1d96 --controls --control-positive xs25_0ml1u8z643032ak8` printed the same ash (generation 759, period 1, population 28), rewind ok at T=852 and T=1180, one positive control building the predecessor, and `PASS`.

## Provenance

`claim/data/provenance/candidate.txt` says the candidate is untabulated, cost 7, from `xs25_0ml1u8z643032ak8` at cost 6, rot 1 lane 11 phase 0. `claim/METHOD.md` says the same and says the predecessor was seeded from a published synthesis.

Live predecessor page `https://catagolue.hatsya.com/object/xs25_0ml1u8z643032ak8/b3s23`, fetched once: HTTP 200, 21708 bytes, title `xs25_0ml1u8z643032ak8 - Catagolue`, still-life, population constantly 25, one line `#CSYNTH xs25_0ml1u8z643032ak8 costs 6 gliders (true).`

`https://catagolue.hatsya.com/textsamples/xs25_0ml1u8z643032ak8/b3s23/synthesis`, fetched once: HTTP 200, 200 bytes, same `#CSYNTH` line plus a 6-glider RLE. That RLE has 6 glider components, rewind at T=68 succeeds, and generation 32 is period 1, population 25, matching the predecessor.

Pinned `claim/data/provenance/TROPHY_CASE.md` has no glider-synthesis family and no occurrence of either apgcode. `claim/data/provenance/known-knowns-matches.txt` is the single header line `Pinned repository content search for xs28_69a4owgzxol5d1d96:` and no hit lines.

Public Shinjuku (`parclytaxel/Shinjuku`, master), raw files fetched once each, zero occurrences of either apgcode:

- `shinjuku/comp/comp-pool.sjk` (5335554 bytes, 70847 lines, 689 other `xs28_` mentions)
- `shinjuku/comp/large-still-lifes.sjk` (15406 bytes)
- `shinjuku/comp/base/one-glider-cleanups.sjk` (1699 bytes)
- `shinjuku/comp/autogen/mvr-farm-2-deduped.sjk` and `mvr-farm-3-deduped.sjk`
- autogen batches `contrib_20241007`, `contrib_20250606`, `contrib_20250711`, `contrib_20250914`, `contrib_20260923`, `contrib_20260924`, `transfer_20241011`, `transfer_20261013`

The mvr farm files were included because the object page's sample soups use symmetry `mvr_component_stdin`. Those soups show the still life has been seen in the census. They are not a `#CSYNTH` line, and the apgcode is not in the mvr farm files that were downloaded.

## Other public searches

GitHub repository `elder-plinius/V3R1T4S` is public (HTTP 200). Issue search, which includes pull requests, returned `total_count` 0 and `incomplete_results` false for `69a4owgzxol5d1d96` inside the repo, for open pull requests, for closed pull requests, for the predecessor apgcode inside the repo, and for both apgcodes across public GitHub issues. GitHub code search returned HTTP 401 `Requires authentication`. That is not evidence the string is absent from file contents.

GitLab blob search for the Shinjuku project returned HTTP 401. The raw-file greps above are the substitute. Older autogen shards outside the dated list were not downloaded.

`conwaylife.com` wiki and forum searches returned HTTP 403 challenge pages titled `Just a moment...`. The apgcode appears there only inside the requested URL. Those responses were not counted as absence. DuckDuckGo HTML search returned HTTP 202 and an anomaly challenge form, with no result list. A general web-index query split the apgcode and returned unrelated pages, so it was not used as a source of absence.

LifeWiki's glider-synthesis article, as returned by the web index from 2026 revisions, records that syntheses of all still lifes through 23 cells were completed in December 2025. That is background for why an xs28 table is partial. It is not evidence about this apgcode. The direct LifeWiki fetch was the 403 above.

No cost-optimality or global-priority claim was tested. Seven is the cost of this synthesis. The table does not list a cost to beat.

## Limitations

ConwayLife forum and wiki were blocked, so a forum post of this exact synthesis could exist and not have been read. GitHub file search and GitLab server-side search were unauthorized. The Shinjuku greps cover the component pool, the one-glider cleanup list, the mvr farms, and the October 2024 through October 2026 batches that were downloaded, and they do not cover every older shard. The census already contains this still life as an object with 10 soups; the missing piece on Catagolue is the synthesis-cost row. Primary fetches were not retried because the first attempt succeeded.

## Commands and sources

Relative paths only. Raw responses are under `out/` and `out/sources/`.

- `out/textcensus_xs28.raw`, `out/textcensus_xs28.headers`
- `out/object_hero.raw`, `out/object_hero.headers`
- `out/strict_enum.c`, `out/check_synth.py`
- `claim/code/life_check.py`, `claim/result/xs28_69a4owgzxol5d1d96.rle`
- `claim/CLAIM.md`, `claim/METHOD.md`, `claim/TARGET_CRITERION.md`, `claim/data/provenance/candidate.txt`, `claim/data/provenance/composition.json`, `claim/data/provenance/known-knowns-matches.txt`, `claim/data/provenance/TROPHY_CASE.md`
- Catagolue object and textsample URLs for `xs25_0ml1u8z643032ak8` and the hero textsample URL
- `https://api.github.com/repos/elder-plinius/V3R1T4S` and the issue-search queries named above
- `https://gitlab.com/api/v4/projects/parclytaxel%2FShinjuku` and the raw `shinjuku/comp/...` files named above
- Blocked or unused as evidence: ConwayLife 403 pages, DuckDuckGo 202 challenge, GitHub code search 401, GitLab blob search 401

pass: true
