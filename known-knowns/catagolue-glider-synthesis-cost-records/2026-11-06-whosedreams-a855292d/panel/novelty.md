# NOVELTY skeptic: xs26_08ehmkk8z6a87066 (claimed 12 gliders)
context: subagent

Fresh context. I read only claim/ (CLAIM.md, METHOD.md, STATUS.md, REPRODUCE.md, TARGET_CRITERION.md, result/xs26_08ehmkk8z6a87066.rle, result/xs26_08ehmkk8z6a87066.json, data/status_source_syntheses_2026-11-05-18.html) plus the kit's TROPHY_CASE.md, known-knowns/, bank/ and PRs. I did not reproduce the synthesis. I only ran the RLE far enough to name the intermediate stages, so the seed could be identified (see "Seed").

## Live fetches (each fetched once, no retries)

| What | URL | Result | Fetched (America/Coral_Harbour, ET, UTC-5) |
|---|---|---|---|
| status_source | https://catagolue.hatsya.com/syntheses | HTTP 200, 63,195 bytes. It is the index of syntheses, assembled from Jeremy Tan's Shinjuku database, and has no per-object cost. It is byte-identical to the packaged snapshot data/status_source_syntheses_2026-11-05-18.html. | 2026-11-06 10:15:11 ET |
| object page | https://catagolue.hatsya.com/object/xs26_08ehmkk8z6a87066/b3s23 | HTTP 200. `#CSYNTH xs26_08ehmkk8z6a87066 costs 58 gliders (true).` The cost is a true cost, not pseudo. | 2026-11-06 10:15:11 ET |

The live cost is 58 (true), and 12 < 58 strictly. The improvement still stands on the primary table.

Supporting lookups (literature, not the gate fetch), at 10:16:55 ET and 10:18:54 ET:
- xs25_3ihf8bbgzw34311 has a live cost of 56 (true). Shinjuku's only listed route into the target is xs25_3ihf8bbgzw34311 plus 2 gliders, from shinjuku/comp/autogen/transfer_20220628.sjk:193075. That gives 56 + 2 = 58, which matches the table.
- xs28_651ugmmz69706221 has a live cost of 11 (true).
- xs27_0adhmkk8z6a87066 has a live cost of 8 (true).

## Seed (the claim package does not name it, so I name it here)

I ran result/xs26_08ehmkk8z6a87066.rle and split off the gliders at each stage:
- At gen 500 there are 7 gliders plus xs20_6s1v0rrzw1, built by 5 gliders.
- At gen 1000 there are 4 gliders plus xs27_0adhmkk8z6a87066. That is 3 more gliders, matching the Shinjuku component in contrib_20260923.sjk:12301, which is dated Sep 2026 and inside the 24-month window.
- At gen 1700 there is 1 glider plus xs28_651ugmmz69706221. That is 3 more gliders, matching transfer_20210826.sjk:220316.
- At gen 3000 there are 0 gliders plus xs26_08ehmkk8z6a87066.

So the claim is the published 11-glider synthesis of xs28_651ugmmz69706221 plus one new 1-glider transfer, xs28_651ugmmz69706221 → xs26_08ehmkk8z6a87066. The seed is published. The new part is that single-glider component.

Is that component already published? Shinjuku master was pulled once as the GitLab archive. Its last commit is "27 oct '26 update" (2026-10-27 08:21 ET), there are no releases, and the only branch is master. I grepped the whole tree:
- xs28_651ugmmz69706221 appears only as an output (from xs27_0adhmkk8z6a87066 and from xs31_g8e1ugmmzd553w643), never as an input to the target.
- The target appears as an output only in the xs25 + 2 line.

The two open Shinjuku MRs, !61 and !62 (natural still-life work), have 0 hits for the target. The compiled table (58) agrees: no route of 12 or fewer is known.

Trivial-edit check: deletion, restriction, relabelling or symmetry applied to the published xs28 synthesis (11 gliders) or to the published 58 synthesis does not yield the target with 12 or fewer gliders. Removing cells from a still life is not free in glider-cost terms; the added glider is exactly the contribution. Apgcodes are canonical, so a symmetric relabelling would show up under the same code. The claim beats the published seed path plus trivial edits, 12 against 58.

## Kit repo search
- TROPHY_CASE.md (89 lines) has no match for the apgcode, "catagolue" or "glider-synthesis".
- known-knowns/ has 25 folders and none is for this target. A grep for the apgcode across known-knowns/ and bank/ finds nothing. bank/targets.json is the only file naming the target id.
- The local clone, all refs, has no commit mentioning glider, catagolue or synthesis.
- The GitHub API search of elder-plinius/V3R1T4S PRs (925 open and closed) returns 0 hits for the apgcode, "glider synthesis", "glider" and "catagolue". The only Life-related PRs (#911, #613, #709, #641 and others) are unrelated targets.

## Literature and code search (last 24 months)
- ConwayLife forums search for "08ehmkk8z6a87066" shows "Search found 0 matches". curl was blocked by Cloudflare, so I read the page through the fetch tool.
- LifeWiki full-text search returns "no results matching the query".
- Web search finds nothing relevant.
- GitHub global code search needs a login and was not run (inconclusive). I did not log in as the user.
- Shinjuku and Catagolue are covered above.

Caveats:
- The forum search matches the apgcode only. A post giving an RLE without the code would be missed, but anything accepted into Shinjuku would have lowered the table cost.
- The claim package should name the seed, xs28_651ugmmz69706221 at 11 gliders, and the new 1-glider transfer. I have named both here.
- p1 needs a listed cost of at least 60, and 58 is below that. Whether p1 applies is for CRITERION, not NOVELTY. The main success rule (strictly below the live cost) is met.

## Verdict
novelty: PASS. 12 strictly beats the live true cost of 58. No published synthesis of this object at 12 or fewer was found in Catagolue, Shinjuku master or its open MRs, LifeWiki, the ConwayLife forums, TROPHY_CASE, known-knowns or the kit PRs. The construction is the published xs28_651ugmmz69706221 path (11 gliders) plus one new transfer glider, and that transfer is not in Shinjuku as of 2026-10-27.

pass: true
