# Honesty gate, claim <18,18,19> rank 3225, fmm-catalogue-small-format-rank

Read by the run's main session (the coordinating Claude Code session, Opus 5.5) at 2026-10-24T19:36Z.
Panel: three fresh subagents, each given only its own copy of claim/; claim/ unchanged since the panel started (every
file's sha256 equals panel/claim.sha256).
- reproduce.md: own standard-library exact checker written before reading the author's code; all 37,896,336 Brent
  equations hold, 3225 terms, ring Q, hashes match, run_checks.sh PASS twice and byte-identical. It did not repeat the
  network rebuild from LITA 19^3 (the object itself is fully verified). pass: true.
- novelty.md: one honest fetch of every comparator 19:28-19:31Z (no blocks); lowest public value 3355 for every
  order of the format; nothing at or below 3225 in Perminov, Lille, fmm_sota.json, matmulcatalog, LITA, V3R1T4S main,
  TROPHY_CASE.md, 685 open and closed PRs, or the literature. Ruling on PR #708 (same contributor, 18:58:23Z): not a
  blocker under POLICY FMM rules 2-3, but the disclosure must say #708 published the value and the identical
  generating code, and that the scheme files are first filed here. pass: true.
- criterion.md: every p1 clause quoted from the bank and met; own exact check (0 wrong of 37,896,336); live index and
  digest re-fetched 19:34Z unchanged; null models (restriction, block sums, Kronecker) give nothing below 3355; not
  subsumed by the sibling <18,19,19> claim. pass: true.

No hedging panelist, no mismatch, value strictly below the live table (3225 < 3355), scope no wider than reproduced,
one object. Table fetches are under 6 hours old.

Disclosure to carry into the pull request description (the gated claim/ is not edited): PR #708 already published
the value 3225 for this cell and the deterministic code that rebuilds this scheme (how-we-built-it of #708); the
scheme files are first filed in this claim.

Reissue: panel/novelty.md was reissued by the same NOVELTY subagent at 2026-10-24T19:51Z at the gate's request, with two text changes only (the contributor's GitHub login replaced, and a quoted POLICY placeholder rephrased) so the package passes the kit's leak and placeholder checks; the main session re-read the reissued file: findings and verdict unchanged, last line pass: true.

status: CONFIRMED_PARTIAL
confirmed_scope: object/u.txt, object/v.txt (object/v.part1.txt followed by object/v.part2.txt) and object/w.txt form an exactly verified bilinear scheme over Q for <18,18,19> with 3225 rank-one terms (no zero or mergeable terms), which is strictly below the rank 3355 for [18,18,19] in fmm_sota.json and in the Lille catalogue index (both re-fetched 2026-10-24T19:34Z) and below the 3524 on the Lille per-format page as recorded in the-record-we-beat/RECORD.md; this meets partial win p1 of fmm-catalogue-small-format-rank, not the main criterion.
