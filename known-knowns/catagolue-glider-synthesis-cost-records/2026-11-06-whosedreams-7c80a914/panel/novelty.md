# NOVELTY skeptic: xs27_0ca1ugmicz651346 (claimed 32 gliders vs listed 66)

context: subagent

Role: NOVELTY skeptic only (kit/RUN.md step 6). I did not re-simulate the synthesis; reproduction is the REPRODUCE skeptic's job.
Package files read: claim/CLAIM.md, claim/TARGET_CRITERION.md, claim/METHOD.md, claim/STATUS.md, claim/REPRODUCE.md, claim/result/xs27_0ca1ugmicz651346.json (and the .rle text embedded in it), plus a diff against claim/data/status_source_syntheses_2026-11-05-18.html.

## Live status fetches (one fetch each, no retries, all HTTP 200)

| Source | URL | Fetched (America/Coral_Harbour, UTC-5) | Value read |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | 2026-11-06 10:20:33 EST | HTTP 200, 63,202 bytes. This is the index page. It holds no per-object cost. After stripping tags, it matches the packaged snapshot except for the "Last cache update" line. |
| Object page | https://catagolue.hatsya.com/object/xs27_0ca1ugmicz651346/b3s23 | 2026-11-06 10:20:34 EST | `#CSYNTH xs27_0ca1ugmicz651346 costs 66 gliders (true).` The cost is **66 and true (not pseudo)**. |
| xs27 tabulation (HTML) | https://catagolue.hatsya.com/census/b3s23/synthesis-costs/xs27 | 2026-11-06 10:20:34 EST | HTTP 200. The page shows "Displaying 1 to 200 of 87485 objects", sorted by cost from highest down. An object costing 66 is not on page 1, so I used the full-table CSV linked from this page. |
| xs27 tabulation (full CSV, linked from that page) | https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/xs27 | 2026-11-06 10:20:49 EST | `"xs27_0ca1ugmicz651346","100000000000000066"`, i.e. **66**. This agrees with the object page. |

The live cost is 66 true. The claimed 32 is strictly less (saving 34), so the improvement has not been absorbed into the table.

## Seed identification (published seed plus new step)

claim/REPRODUCE.md and claim/METHOD.md say the 32-glider synthesis was composed (`compose_ms.py --pre 32`) from the input still life `xs27_8ehf8bbgz6430321`, followed by one extra glider (1G sweep: rot 0, lane 4, phase 0).

- Published seed: `xs27_8ehf8bbgz6430321`. The same CSV fetch gives `"xs27_8ehf8bbgz6430321","100000000000000031"`, so its Catagolue cost is **31**.
- New step: a single glider that turns `xs27_8ehf8bbgz6430321` into `xs27_0ca1ugmicz651346`. That gives 31 + 1 = 32.
- Trivial-edit test: deleting, restricting, relabelling or applying symmetry to the published 31-glider synthesis of the seed yields the seed, not the target (a different 27-cell still life). Reaching the target needs the new collision. The published route to the target alone costs 66. The claim names its seed, and seed plus new step (32) strictly beats what the published objects give without it (66).

## Repo search (kit pin f3b19b4, commit 2026-10-30)

- **TROPHY_CASE.md**: 0 matches for glider, catagolue or life. No accepted claim exists for this target.
- **known-knowns/**: 26 folders, none for Life or glider synthesis. I grepped for the apgcode, the seed apgcode, "glider-synthesis" and "catagolue" and got no hits.
- **bank/**: the only match is the target definition itself (`catagolue-glider-synthesis-cost-records` in bank/targets.json). The only other mention in the tree is known-unknowns/graphs-games-automata/catagolue-glider-synthesis-cost-records.md, the target writeup. No prior result is recorded.
- **Pull requests** (public GitHub API, read-only, no login; gh was not logged in and I did not log in): 925 PRs listed (state=all). None mentions glider, catagolue, synthesis or an xs2x_ apgcode in its title or body. Search-API queries for the exact apgcode and for "catagolue" returned 0.
- **Releases**: the repo has 0 releases, so there are no release assets to check.

## Literature / code search (last 24 months)

- **Catagolue**: the live object page and the tabulation both show 66 (true). Catagolue builds its costs from Jeremy Tan's Shinjuku database and refreshes several times a day. Any synthesis merged into Shinjuku and processed would show up here.
- **Shinjuku** (https://gitlab.com/parclytaxel/Shinjuku): GitLab reports last activity at 2026-10-27T12:21:52Z (2026-10-27 07:21 EST). That is before the claim's discovery fetch and today's live 66. Blob search of that repo needs a login (HTTP 401), so I could not grep its files directly. I relied on Catagolue's live rendering of it.
- **Web**: searching for the exact apgcode, and for "0ca1ugmicz651346" together with conwaylife, shinjuku or catagolue, returned no relevant hits (unrelated retail pages only). Recent ConwayLife activity, such as the 2026 thread "Synthesising every natural still life" (t=7474) and the 23-bit still life threads, does not mention this object in the indexed snippets I saw. I did not read every page of those threads.
- **LifeWiki**: no page or mention of this apgcode found.
- I found no published synthesis of `xs27_0ca1ugmicz651346` at 32 gliders or fewer, so none that ties or beats 32.

## Limits of this check

- I cannot see Catagolue's readsynth submission queue. A synthesis posted to the forums or submitted within the last few hours and not yet processed would not appear here. The kit's pre-submission re-fetch should cover this.
- This is not an exhaustive read of every ConwayLife forum page.
- Neighbouring cells: the only published neighbour that bears on this result is the seed `xs27_8ehf8bbgz6430321` (31). No other published object gives the target through trivial edits for 32 gliders or fewer, as far as the live table shows.

## Verdict

novelty: PASS. The live true cost is 66 (fetched 2026-11-06 10:20:34 EST). The claimed 32 strictly beats it. The seed is named (`xs27_8ehf8bbgz6430321`, published at 31) and the new step is one glider. I found nothing published that ties or beats 32.

pass: true
