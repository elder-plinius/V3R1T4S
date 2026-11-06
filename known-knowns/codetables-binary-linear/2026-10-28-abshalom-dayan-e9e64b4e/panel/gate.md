# Honesty gate (main session), run folder 2026-10-28-0100

status: CONFIRMED_SOLUTION
confirmed_scope: The 19 x 32 matrix G in object/code_q9_n32_k19_d10.json (sha256 e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965), read in the stated GF(9) = GF(3)[w]/(w^2 - w - 1) encoding, has rank 19 and generates a linear [32,19,10] code over GF(9), whose minimum distance 10 is strictly above the lower bound 9 and at most the upper bound 12 of the codetables.de cell (q,n,k) = (9,32,19) as fetched at 2026-10-28T01:39:29Z.

## Reading of the panel (main session, 2026-10-28T01:42:21Z)

Skeptics ran one at a time, each a fresh Claude Code subagent on claude-opus-5-5 that saw only its copy of claim/
(panel/work-*/claim/): REPRODUCE from about 01:21Z, NOVELTY from 01:25:36Z, CRITERION from about 01:36Z.

- REPRODUCE (reproduce.md): own GF(9) arithmetic and own dual-side exhaustive checker written before opening
  claim/checkers/ (visit counts equal C(32,s) for s = 1..9, no dependent set of 9 or fewer parity-check columns;
  self-test on 300 random matrices, 0 mismatches); weight-10 witness with its message vector; author's REPRODUCE.md
  matched; rebuild byte-identical (sha256 e9e64b4e...7965). pass: true.
- NOVELTY (novelty.md): one GET of the cell at 2026-10-28T01:26:14Z, HTTP 200, page byte-identical to the scout's,
  "lower bound 9 upper bound 12"; all 771 PRs (pulls list API, 9 pages, one at a time, all 200): nothing reaching or
  implying [32,19,>=10]_9; TROPHY_CASE.md: nothing; arXiv export API query (200), web searches: nothing in 24 months;
  LinCodeEvolve codes are binary. Not read, not retried: MinT (no connection), Yves Edel's tables (404). A first
  python urllib attempt at PR page 1 failed client-side (local CERTIFICATE_VERIFY_FAILED, no HTTP response); the
  pages were then fetched with curl: not a block or server refusal. pass: true.
- CRITERION (criterion.md): conditions (1)-(4) checked literally; own rank 19; own third exact check (rank of every
  9- and 10-subset of H's columns: 0 of 28048800 9-subsets deficient, 4432 deficient 10-subsets), seeded weight-9
  negative caught; own fetch 2026-10-28T01:39:29Z, HTTP 200, 9-12; no null model needed (deterministic exact
  checkers). Wording note: the bank id says "binary" while the criterion says GF(q); the maintainer merged a GF(9)
  claim under this same bank entry (#644, 2026-10-25), so the literal reading stands. pass: true.

Downgrade checks: no hedging verdict; no reproduction mismatch; 10 > 9 strictly (not a tie) and 10 <= 12; one cell, one
object; exact exhaustive methods only (m3_mindist, hdep, and both skeptics' own); table fetches are plain single GETs
(curl, User-Agent naming V3R1T4S), all HTTP 200; newest panel fetch 01:39:29Z, under 6 hours old. Not checked by
anyone: MinT and Yves Edel's tables (a human can check them by hand); older non-arXiv literature beyond the 2001 table
entry was not exhaustively searched.
