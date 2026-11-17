# Honesty gate: anomaly-free-atlas-qmax, claim "SMnuR Q_max 19 and SM Q_max 32..35" (run 2026-10-28-0820)

status: CONFIRMED_SOLUTION
confirmed_scope: In the Allanach-Davighi-Melville census convention (1 + number of nonzero gcd-1 integer solutions of the six anomaly equations with |F| <= Q_max, modulo per-species family permutations and overall sign), the counts are 4247050205 for the SM plus three right-handed neutrinos at Q_max = 19 and 15866882, 19550225, 22847889, 26469950 for the SM fermions at Q_max = 32, 33, 34, 35, each equal to one plus the line count of a checker-passing canonical list with the sha256 recorded in object/counts.txt and to an independent non-listing count, beyond the published Q_max <= 10 and beyond the workspace's previously confirmed rows (SMnuR 11..18, SM 11..31).

Read by the run's main session at 2026-10-28T12:29:43Z. All three panel files were written by fresh subagent contexts that saw only
claim/ plus what each fetched or computed itself:
- reproduce.md: pass: true
- novelty.md: pass: true
- criterion.md: pass: true

The scope line is CRITERION's sentence, copied exactly. This claim replaces the PROMISING claim of run 2026-10-22-0818
(same rows). That claim stopped because novelty was then unreadable and because its claim/ was assembled 42 s before
its PREREG. Tonight every row was recomputed after this run's PREREG (2026-10-28 08:21:31 UTC).

## Downgrade checks (kit/RUN.md step 7)
- **Hedging.**
  - CRITERION lists risks without hedging the verdict: completeness rests on two different methods agreeing, which
    is no weaker than the atlas's own lists; the list is regenerated and hashed rather than deposited (the SMnuR 19
    list would be about 200 GB); it relied on CLAIM.md for which rows were confirmed earlier.
  - NOVELTY notes its search could not include GitHub-wide code search or full-text literature.
  - REPRODUCE lists gaps it closed itself: its own checker and its own counters replaced the author's tools. It notes
    the author's checklist.c accepts whitespace variants and an empty stream, which pipefail plus the line-count
    comparison cover.
  - None of these is a doubt about the result.
- **Reproduction.** REPRODUCE regenerated all five rows in full: SMnuR 19 in 5708 s, ending 12:27:56Z. For each row:
  - the sha256 equals object/counts.txt;
  - checklist.c and its own checker (mycheck.c) both PASS on the same bytes;
  - the line count equals count − 1;
  - its own counters (mycount.c, mycount_nu.c) give all five counts and reproduce all 20 published "solutions" values
    and all 20 "symmetric solutions" values.

  CRITERION regenerated SM 32 independently (hash and lines match). The counters lens (mitm.c, count.c) agrees too.
- **Novelty.**
  - The largest published Q_max is 10 for both contents: the paper and Zenodo 3345889 v1.1.0, the last version.
  - None of the 121 citing records on INSPIRE gives a larger census.
  - The V3R1T4S trophy case and all 774 PR refs carry no such rows.
  - NOVELTY's fetches (10:49Z) are less than 6 hours old.
- **Literalness.** CRITERION pinned the convention to the atlas: only it reproduces the published values, including at
  prime Q_max. Both contents are present. Nothing in the package subsumes the claim.
- **Scope.** The scope is no wider than what was reproduced.
- **Completeness.** These are full lists, not samples, and no search is capped.
- **Evasion.** None. The proxy blocks were recorded and not retried.
- **Bundling.** Both contents form one claim, as the charter's "with and without three right-handed neutrinos"
  requires. CRITERION judged this acceptable.
- **Timing.** PREREG (08:21:31Z) precedes every output of the attack and of the claim.

## Notes (not part of the verdict)
- Fix for the package: REPRODUCE.md says the SMnuR 19 run needs "< 3 GB", but the lister log shows 4.35 GB of
  bucket memory.
