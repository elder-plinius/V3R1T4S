# Independent NOVELTY review: A334497(37) = 49276415 (Rule 30, cyclic width 37)

context: subagent (fresh executor subagent; saw only files and my own live read-only fetches; no other panel file read)
role: NOVELTY
fresh_context: true
target: eca-rule30-rule110-cyclic-max-period (bank, repo commit 5db3547); status_source https://oeis.org/A334497

## Claim judged
The exact value A334497(37) = 49276415, from an exhaustive search of all 2^37 cyclic Rule 30 states, with witness 0x7fbfe703e (README.md, object/a334497_37.txt). The number itself is not new (see below). The new content claimed is that the value is exact: no start has a longer eventual period.

## Live status source, one curl per URL, UA "V3R1T4S-kit (whosedreams)", no retries
All fetched 2026-11-23 between 23:52:27Z and 23:52:58Z (18:52 ET, America/Toronto, UTC-5).
- https://oeis.org/search?q=id:A334497&fmt=json: HTTP 200, 1708 bytes, sha256 149cd9be2665bd90... (same as the packager's 23:39:09Z snapshot in the-record-we-beat/RECORD.md). Revision 40, last edited 2026-06-12T18:55:01-04:00. DATA has 36 terms ending 5656002, 18480630, 2237472. No a(37). Keyword "more".
- https://oeis.org/A334497/b334497.txt: HTTP 200, 338 bytes, sha256 7339a6ff9bd1784e... (same as the packager's). Last line "36 2237472". No index 37.
- https://oeis.org/A334497 (HTML): HTTP 200. EXTENSIONS: a(8)-a(12) Jinyuan Wang 2020, a(13)-a(22) Pontus von Brömssen 2022, a(23)-a(36) Paolo Xausa 2023 from Gage, Laub and McGarry (2005) Table 2. No a(37).
- https://oeis.org/draft/A334497: HTTP 200, "No pending changes for A334497."
- https://oeis.org/A334497/history: HTTP 404. The page's own history link, https://oeis.org/history?seq=A334497: HTTP 200. Newest entry #40 (Andrei Zabolotskii, 2026-06-12, a link and status edit only). The last DATA change was #34 (Paolo Xausa, 2023-06-29, a(23)-a(36)). No a(37) was ever added or proposed.
- Value search https://oeis.org/search?q=49276415&fmt=json: HTTP 200, one result, A334496 only (same sha256 as the A334496 id fetch, 730cb5f2d04d5ada...). A334496's name is "Eventual period of a single cell in rule 30 cellular automaton in a cyclic universe of width n". Its b-file (HTTP 200) has the line "37 49276415". So 49276415 appears in OEIS only as the single-cell period, which is a floor for A334497(37). It does not appear as a maximum over all starts.

## Literature
- Wolfram, "Random sequence generation by cellular automata", Adv. Appl. Math. 7 (1986), Table 9.2. I read the packager's PDF text (fetch/2026-11-23/wolfram/w86.txt, outside the package). Column CA30, row N=37: 49276415. The caption says: "In the former case [CA30], a selection of seeds, including single nonzero sites, were used." So it is a sampled maximum, a lower bound. The table is demonstrably not exhaustive. Its N=17 (10845), N=22 (3256), N=27 (67554) and N=30 (306120) values are below the exhaustive or larger values now in A334497 (10846, 3553, 240300, 374265). Nothing in the paper claims exactness at N=37.
- Gage, Laub and McGarry (2005), "Cellular Automata: Is Rule 30 Random?" I fetched it myself: https://homes.luddy.indiana.edu/dgerman/2005midwestNKSconference/dgelbm.pdf, HTTP 200, sha256 1df505f6bfaf0e77... Table 2 covers N=4..36 only, and they say their complete data covers window sizes below 25. For 37..54 they only cite Wolfram's data for a trend fit. They give no width-37 result.
- Web searches (2026-11-23) for an exhaustive width-37 Rule 30 maximum cycle, for "49276415", and for recent A334497 extensions turned up the following, none of which gives an exhaustive or larger width-37 value:
  - only the above sources;
  - OEIS A334496 and A357950 (A357950 lists terms to n=35 only);
  - sequencedb's mirror of A334496 (single cell);
  - jeremysalwen/rule30cyclefinder (single cell only);
  - Wolfram's 2019 Rule 30 Prize post (single-cell periods);
  - Wolfram Rule30PrizeKit and arXiv 2609.09431 (infinite-array problems, not cyclic maxima).
  One search engine's auto-summary wrongly said 49276415 is "the width-37 entry in the OEIS sequence for maximum eventual period". Its own cited sources show that value only in A334496 (single cell), so I disregarded the summary.
- I found no sampled value larger than 49276415 at width 37 anywhere. That is consistent with the claim.

## This repository
- Upstream TROPHY_CASE.md (raw main; latest commit 989ddf5, 2026-11-23T18:25:27Z): no row for eca, Rule 30 or A334497.
- known-knowns/ (API listing): only graph-automata-max-period, a different target with three 2026-11-02 runs. Nothing for this target.
- GitHub issue/PR search on elder-plinius/V3R1T4S (unauthenticated API, 23:52Z):
  - "A334497": 1 hit, PR #1173.
  - "eca-rule30": 1 hit, PR #1173.
  - "49276415": 0 hits.
  - "rule 30": 108 hits. The first 50, by relevance, include no other claim on this target.
- PR #1173 is the Rule 110 sibling, A204371(37)=4403. It is not this term. It is relevant as a precedent. On 2026-11-19 the maintainer independently re-ran Rule 110 at n=37 and asked only for packaging fixes before merging. That claim's value also equals a known single-cell floor (A180001(37)=4403). So upstream treats an exhaustive exact term equal to a published lower bound as a valid harvest result.

## Judgement against the novelty rules
- Bank criterion: "The term must not already be in the live OEIS entry at claim time." It is not: entry, b-file, draft and history all end at a(36).
- Bank pitfall: "a new term must be at least as large as Wolfram's value for that width". It is equal, so this is met, and the README discloses the equality explicitly.
- RUN.md NOVELTY rule, "A tie is not a record": I considered this carefully. The target is a harvest of an exact term, not an extremal record. The published object, Wolfram's 1986 value, is a lower bound from sampled seeds, and no one has published or listed the upper bound or exactness. The claim adds information no published source has: an exhaustive census showing 49276415 is the maximum over all 2^37 starts. That strictly improves the state of knowledge, from "A334497(37) >= 49276415" to "A334497(37) = 49276415". No trivial edit of a published object yields exactness. So this is not a tie in the sense of LESSONS #9, and the #1173 maintainer response supports that reading.
- Honest framing: README.md says plainly, in ## What, the plain-words paragraph, ## Compared to and ## Not claimed, that:
  - the number is not new;
  - it equals A334496(37) and Wolfram's 1986 sampled value;
  - the witness lies on the single-cell cycle;
  - the new content is the exhaustive upper bound.
  It does not claim the number as a discovery. The Wolfram source and its lower-bound caveat are credited. I see no overclaim on novelty.

## Caveats (not blocking)
- Novelty is judged only against the sources above as of 2026-11-23T23:52Z. The parent must refetch OEIS immediately before any submission.
- Whether the census is correct (exhaustive coverage, agreement between the two programs) is for REPRODUCE and CRITERION, not this review. The 2^37 census was run on the contributor's PC and not on the box.
- If the submission were described anywhere as a "new value" rather than a "new exact term", that would be an overclaim. The current README avoids this.

verdict: novelty SURVIVES. A334497(37) is absent from the live OEIS entry, b-file, drafts and history. No published exhaustive width-37 result exists. The only published equal value (Wolfram 1986) is an explicitly sampled lower bound, which the claim meets with equality and discloses.

pass: true
