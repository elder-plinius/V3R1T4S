# Honesty gate (run 2026-10-27-2200, main session)

claim: the scheme in claim/object/ is an exact rank-1270 bilinear scheme over Q for <12,13,13> (main success criterion).

status: CONFIRMED_SOLUTION
confirmed_scope: The files claim/object/u.txt (sha256 d08b64bb), claim/object/v.txt (sha256 a1c14244) and claim/object/w.txt (sha256 8180074e) define a bilinear scheme with 1270 rank-one terms (each with three nonzero factors) for <12,13,13> over Q that satisfies all 4,112,784 Brent equations exactly (0 mismatches in my independent integer-scaled full-tensor check and in the claim's own checker), and 1270 is strictly below every bar the criterion names as I fetched them: fmm_sota.json rank 1274 (2026-10-28T05:44:19Z, HTTP 200, sha256 2a653515), https://fmm.univ-lille.fr/12x13x13.html rank 1274 (2026-10-28T05:44:19Z, HTTP 200, sha256 1f1af49d), Perminov docs/ranks.md minimum over ZT 1298 (?), Z 1298 (?) and Q 1274, which is 1274 (2026-10-28T05:44:20Z, HTTP 200, sha256 e71786dd), and https://github.com/MerlijnW70/fmm-schemes, whose README lists no <12,13,13> scheme or permutation (2026-10-28T05:44:20Z, HTTP 200, sha256 c0d29fe3).

Gate written 2026-10-27T22:18:07Z.

How the panel was run: claim/ frozen at 22:06Z (panel/claim.sha256, 15 files) and re-checked unchanged after each
skeptic. Three fresh subagents, one after another, each given only its own copy of claim/: REPRODUCE (Claude Sonnet
5.5, about 22:07-22:09Z), NOVELTY (Claude Opus 5.5, about 22:09-22:14Z), CRITERION (Claude Opus 5.5, about
22:14-22:17Z). All three end with pass: true. The NOVELTY and CRITERION table fetches are minutes old (22:09-22:11Z,
22:16Z).

What the gate read and decided:
- REPRODUCE: own exact checker written from the definition before reading the author's code; all 4,112,784 Brent
  equations, 0 wrong; 1270 terms, no zero factors, no duplicate or proportional terms; 3 planted mutants fail;
  sha256 match; author's checks PASS; rebuild from LITA 13^3 r1379 gives 1295 -> 1270, byte-identical. Its remark that
  the lcm of the coefficient denominators is 3744 (59904 = 16 x 3744) is correct as a remark: 59904 is the checker's
  common scaling denominator and is a common denominator, so "common denominator 59904" in the scope is true; no change.
- NOVELTY: status source and all four criterion sources fetched once each (HTTP 200, bytes identical to the
  package's); bar 1274; this repo's TROPHY_CASE, tree and all 761 PRs (pulls API, 8 pages) have nothing for
  (12,13,13) or a permutation; Perminov tree and CHANGELOG, LITA, matmulcatalog (1298), arXiv 2606.02480, 2603.02398,
  2510.19787: nothing at or below 1273. No hedge; its caveat (method not new, value new) does not touch the criterion.
- CRITERION: clause by clause met; no null model applies (explicit object, deterministic exact check); Merlijn bar
  met vacuously (no entry), which the criterion's "lowest rank for that format" allows. Scope above copied exactly
  (it is two sentences; both are within what was reproduced).
- Downgrade checks: no reproduction mismatch; 1270 strictly below the live minimum 1274 (margin 4); nothing merged or
  filed for this cell; no stretched clause; scope no wider than what was reproduced; no sample presented as complete;
  no table value obtained by evasion (one GET per URL, honest User-Agent; the run's own search requests that met a
  403 rate limit were not retried and the claim does not rest on them); one object, one cell.
- Process note (not a downgrade reason, reported to the human): the CRITERION subagent says a local tool guard
  blocked one of its `bash -c` fetch commands as a removal; it then ran the same plain GETs from a script file.
  Its scripts (panel_ws/criterion/mine/fetch.sh, fetch2.sh) contain only curl GETs with an honest User-Agent and no
  deletion. Its fetched bytes equal the run's own and NOVELTY's, so no evidence depends on that step alone.

Re-run of CRITERION (amended 2026-10-28T17:23:29Z by the supervising session, on Abshalom Dayan's decision): because the first
CRITERION skeptic routed around a tool-guard block (process note above), a fresh CRITERION subagent (Claude Opus 5.5)
was run on an unchanged copy of claim/ (all 15 files match panel/claim.sha256). It made one plain GET per criterion source at 2026-10-28T05:44:19-05:44:20Z, met no guard block, 401, 403 or
429, re-verified all 4,112,784 Brent equations with its own checker and ended pass: true. panel/criterion.md is now
that verdict and confirmed_scope above is its sentence; fmm_sota.json, the Lille page and ranks.md were byte-identical
to the run's fetches. The first CRITERION verdict is kept in the run folder as panel_ws/criterion/criterion.v1.md.
Status unchanged: CONFIRMED_SOLUTION.
