# Honesty gate: cap_1104_n9.txt (target cap-set-dim7-dim8, partial win p1)

status: CONFIRMED_PARTIAL
partial_win: p1
confirmed_scope: The file cap_1104_n9.txt (sha256 26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e) is an affine cap of 1104 distinct points in F_3^9, with no three distinct points summing to 0 mod 3, verified exhaustively over all 608,856 pairs; 1104 is strictly larger than every F_3^9 cap size found on 2026-10-24 in the sources p1 names as the panel read them (1082 from the FunSearch notebook and from doubling Edel's 541-cap in PG(8,3), no n = 9 value in X-evolve Table 2 or OEIS A090245, none in arXiv titles and abstracts) and than the unrefereed 1084 of Noirsys/capset, so it meets partial win p1 for dimension 9 and does not meet the main n = 7 or 8 criterion.

## How the panel was run
- REPRODUCE: a headless `claude -p` session (claude-sonnet-5-5, effort high), fresh, started inside its own copy of
  claim/ (panel/.work/reproduce/claim). pass: true.
- NOVELTY: a fresh Agent-tool subagent (claude-opus-5-5) given only its own copy of claim/ (panel/.work/novelty/claim).
  pass: true.
- CRITERION: a fresh Agent-tool subagent (claude-opus-5-5) given only its own copy of claim/ (panel/.work/criterion/claim).
  pass: true.
- Run one after another, never in parallel. Each skeptic wrote its own file in its copy; the run's main session copied
  the three files into panel/ unchanged.

## What the gate checked (read by the run's main session, 2026-10-24T20:35Z)
- Reproduction: three independent checkers (REPRODUCE's pair scan, CRITERION's pair scan plus an exact integer Fourier
  count, the package's two routes) agree: 1104 distinct points of F_3^9, 0 lines. Deterministic. No mismatch.
- Bar: 1082 published (FunSearch notebook "largest known cap set for n = 9 has size 1082"; Edel's 541-cap in PG(8,3)
  doubled by the doubling theorem), 1084 unrefereed (Noirsys/capset, 2026-10-23). 1104 is strictly larger than both:
  not a tie.
- Table access: every fetch was one plain GET with an honest User-Agent and no retries. Edel's Heidelberg pages
  answered 404 (moved); NOVELTY and CRITERION read his tables at yvesedel.de, which OEIS A090245 links and which calls
  itself "The website formerly known as www.mathi.uni-heidelberg.de/~yves/". The gate judges this the author's own
  current page, not a mirror used to dodge a block, so the PREREG clause "PENDING TABLE CHECK for Edel's tables unless a
  skeptic reads them honestly" is met. The arXiv http-to-https 301 was followed once (a redirect, not a block). MinT
  (not one of p1's named sources) timed out once and was not retried.
- Fetch age: the panel's table fetches are from 20:04Z to 20:29Z, less than 6 hours old.
- Scope: one object, one dimension (n = 9). The 2368-point cap in F_3^10 from the same lens is not part of this claim.
  The main criterion (n = 7 or 8) is not met and not claimed.
- Remaining risk, stated by NOVELTY and CRITERION: beyond the cited values, "nothing at 1104 or above" is absence of
  evidence (journals outside arXiv and MinT not searched exhaustively).

## Changes during the panel (recorded so nothing is hidden)
- After NOVELTY's report, claim/CLAIM.md was amended to cite the 1084 of Noirsys/capset and Edel's 541 (claim sentence,
  table record and credits). The object and every checked file were unchanged. REPRODUCE and NOVELTY saw the earlier
  CLAIM.md; CRITERION saw the amended one.
- REPRODUCE's verdict file reproduce.md overwrote REPRODUCE.md in its own work copy (this file system ignores case);
  the run's claim/REPRODUCE.md is unaffected.
