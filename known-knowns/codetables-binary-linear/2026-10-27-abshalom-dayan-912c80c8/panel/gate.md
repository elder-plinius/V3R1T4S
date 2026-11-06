# Honesty gate (main session), run folder 2026-10-27-0100

status: CONFIRMED_SOLUTION
confirmed_scope: The 19 x 29 matrix in object/code_q9_n29_k19_d8.json (sha256 912c80c8...f9e7), read over GF(9) = GF(3)[w]/(w^2 - w - 1), has rank 19 and exact minimum distance 8 (A_8 = 12456), which is strictly above the lower bound 7 and within the upper bound 9 of the codetables.de [29,19] GF(9) cell as fetched at 2026-10-27T02:09:43Z, and it is not a LinCodeEvolve (binary) code nor derived from one.

## Reading of the panel (main session, 2026-10-27T02:14:13Z)

- REPRODUCE (reproduce.md, fresh Opus subagent, started 2026-10-27T01:56:34Z per started_reproduce.txt): own two exhaustive
  subset checkers written before opening claim/checkers/ (parity side: no dependent 7-set of H's columns among
  1560780; 1557 dependent 8-sets, A_8 = 12456; generator side agrees); seeded negative caught; author's REPRODUCE.md
  matched line for line; rebuild byte-identical. pass: true.
- NOVELTY (novelty.md, fresh Opus subagent, started 2026-10-27T02:00:19Z): one GET of the cell at 02:00:51Z, HTTP 200,
  same sha256 fe750485... as the scout's, "lower bound 7 upper bound 9"; all 288 cells of the n = 28..36 range page
  checked under shortening, puncturing, subcode and zero-column rules: best implied d at (29,19) is 7; repo, trophy case,
  PRs (bodies, including the qutrit PRs' classical GF(9) codes, all dimension <= 15) and literature: nothing at
  d >= 8. Could not read (no retries): arXiv export API (429/503), MinT (no connection), Yves Edel's GF(9) index (TLS
  name mismatch). pass: true.
- CRITERION (criterion.md, fresh Opus subagent, started 2026-10-27T02:09:13Z): conditions (1)-(4) checked literally
  with its own rank and two-sided subset checker; its own fetch 02:09:43Z (7-9); no null model needed. Two wording
  notes (bank id says "binary" while the criterion says GF(q); the "2^k" feasibility clause is binary-shaped and the
  MacWilliams route was used): neither changes the literal outcome, and the maintainer merged a GF(9) claim under this
  same bank entry on 2026-10-25 (#644). pass: true.

Downgrade checks: no hedging verdict; no reproduction mismatch; 8 > 7 strictly (not a tie) and 8 <= 9; scope one cell,
one object; exact exhaustive methods only (four agree: m3_mindist, hdep, bz9t, dualenum + MacWilliams, plus the
skeptics' own); table fetches are plain single GETs (fetch_cells.sh, curl, User-Agent naming V3R1T4S), all HTTP 200;
newest panel fetch 02:09:43Z, under 6 hours old. Not checked by anyone: the three sources NOVELTY could not read
(listed above; a human can check MinT and Edel's tables by hand).
