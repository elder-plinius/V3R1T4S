context: Claude Code subagent, fresh context [Sonnet 5.5]

## Status source (fetched once, no retries)
- 2026-11-16 (UTC, see a working file (not shipped)) https://wiki.bbchallenge.org/wiki/Post_Tag_System, HTTP 200. The page says "This page was last edited on 16 September 2026, at 14:37" (oldid=8554). Champions table row for size 8: "8 | >= 19 | 111_20_ | 7" (lower bound, 7 holdouts). Sizes 9, 10, 11 are also ">=". Exact values stop at size 7 (= 10, 0111_1). The page still lists size 8 as open. The history and raw-view URLs returned 404, so I could not read the edit history beyond that timestamp.

## Other places checked
- sligocki/etc post_tag (GitHub API): the last commits touching post_tag are 2026-09-16 and earlier (deciders such as Closed Tape Subset, ActiveNonDecreasing, Phase0Closed). The directory has only a working file (not shipped), README.md and src, with no results table and no releases. Nothing there states BB_PT(8).
- AzertyWasTaken/Busy-Beaver results.md: uses a different convention (size = sum of word lengths, halting step counted). Its BBPT(5) = 19 and BBPT(6)..(9) are bounds with holdouts; its BBPT(5) is an exact value of a different function and does not settle the wiki's size 8. No releases.
- bbchallenge forum (discuss.bbchallenge.org search for "tag system"): HTTP 200, zero posts. Discord archive: not reachable, not checked.
- arXiv API, query all:"tag system" AND all:"busy beaver": 0 results.
- GitHub searches (repos: "post tag", "BB_PT", "BBPT", "tag system busy beaver"; code and issues "post_tag BB_PT", "tag system busy beaver"): nothing relevant.
- elder-plinius/V3R1T4S: the target is still in known-unknowns (not shipped in this package, "open as of 2026-10-30"). TROPHY_CASE.md has no mention of BBPT or tag systems; known-knowns has no tag entry. PR searches ("BB_PT", "tag system", "post-tag") and a scan of the latest 400 PR titles found no other BBPT claim or package.

## Assessment
Nothing I could reach shows BB_PT(8) as proven, so this is not a tie with a published exact value. It also does not follow by restriction from a merged package. The wiki bar is "BB_PT(8) >= 19 with 7 holdouts", and the claim's value 19 equals the listed champion, so a new champion is not claimed. The record is the exact value (success criterion (b), p1). Limits: the Discord archive and the wiki edit history were not read, and sligocki's decider work could close the holdouts offline without publishing. Whether the 19,693-system enumeration and the certificates are correct is for the other skeptics.

novelty: NEW (exact value not published as of the checks above; still open on the status page)
pass: true
