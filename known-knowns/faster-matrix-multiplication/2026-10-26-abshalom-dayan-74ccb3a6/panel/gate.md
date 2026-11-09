# Honesty gate (run 2026-10-26-2200, main session)

claim: the scheme in claim/object/ is an exact rank-1836 bilinear scheme over Q for <14,15,15> (main success criterion).

status: CONFIRMED_SOLUTION
confirmed_scope: The files object/u.txt (sha256 74ccb3a6…), object/v.txt (sha256 0f86e47a…) and object/w.txt (sha256 cac452b5…) define an explicit bilinear scheme for the format <14,15,15> with exactly 1836 rank-one terms (no zero factors, no mergeable duplicates) that satisfies all 9,922,500 Brent equations exactly over Q (common denominator 54400), and 1836 is strictly below every bar the criterion names as re-fetched at 2026-10-26T22:25Z (fmm_sota.json 1848, fmm.univ-lille.fr/14x15x15.html 1890, Perminov ranks.md min of ZT 1894 / Z 1892 / Q 1848 = 1848, MerlijnW70/fmm-schemes no entry for this format or any permutation).

Gate written 2026-10-26T22:28:16Z.

How the panel was run: claim/ frozen at 22:08:55Z (panel/claim.sha256, 15 files) and re-checked unchanged after each
skeptic. Three fresh subagents, one after another, each given only its own copy of claim/: REPRODUCE (Claude Sonnet
5.5, about 22:09-22:12Z), NOVELTY (Claude Opus 5.5, about 22:12-22:23Z), CRITERION (Claude Opus 5.5, about
22:24-22:28Z). All three end with pass: true. The NOVELTY and CRITERION table fetches are minutes old (22:13Z, 22:25Z).

What the gate read and decided:
- REPRODUCE: two own checkers (exact bigint and a proved-exact modular one), all 9,922,500 equations, 0 wrong; planted
  negatives fail; author's checks PASS; rebuild run twice, byte-identical. Its remark that the least common
  denominator of the coefficients is 5440 (54400 is a common denominator, not the least) is correct (gate recomputed:
  lcm of coefficient denominators 5440); "common denominator 54400" in the scope is true as stated, so no change.
- NOVELTY: four sources and the repo re-fetched (bars 1848 tables, 1842 merged); all 755 PRs scanned; nothing at or
  below 1836 except the same contributor's own open PR #752 (2026-10-25T11:18:58Z), which names this scheme as an
  unclaimed intermediate and ships code that rebuilds it. The skeptic decided this sets the credit date and does not
  make the claim non-novel, and recorded the stricter reading as a caveat. The gate reads this as a decided verdict
  with a disclosed caveat, not a hedge: kit/POLICY.md FMM rule 2 dates a claim by the earlier filing of the same object
  here, and at 2026-10-25T11:18:58Z nothing at or below 1836 was public. The package must cite #752 as the first public
  mention, and the caveat goes to the human under "Needs you".
- CRITERION: clause by clause met; no null model applies (explicit object, deterministic exact check); trivial
  baselines 1977 and 1945. Scope above copied exactly.
- Downgrade checks: no reproduction mismatch; value strictly below the live tables (1848) and the merged 1842; no
  stretched clause; scope no wider than what was reproduced; no sample presented as complete; no evasion (one GET per
  URL, honest User-Agent); one object, one cell.
