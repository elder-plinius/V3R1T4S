# Honesty gate (kit/RUN.md step 7)

status: CONFIRMED_SOLUTION
confirmed_scope: For every n from 18 to 25, the hash-verified certificate file in claim/object gives exactly A000055(n) pairwise non-isomorphic trees on n vertices (hence every unlabeled tree of that order), each with a bijection onto {1..n} whose n-1 edge sums are consecutive integers (a super edge-magic labeling), as confirmed by an exact canonical-key count, by leaf-extension regeneration from order n-1, and by the claim's own regenerating checker for n up to 24; combined with the Lee and Shan verification up to 17 cited in DS6 (29th ed., Nov 6, 2026), every tree on at most 25 vertices is super edge-magic, meeting criterion (a) in full.

Read in full by the run's main session (2026-11-10T18:41Z) from panel/reproduce.md, panel/novelty.md and panel/criterion.md, each
written by a fresh-context subagent that saw claim/ only, each ending pass: true.
- REPRODUCE: own checker written before reading the author's code; every line of all eight files read (n = 25 in 8
  hash-bucket passes with exact keys, under 8 GB); invalid 0, distinct = A000055(n) from its own Otter computation at
  every order 18..25; 10 injected defects rejected; all 8 hashes OK; the author's checkers agree where run (indep
  18..23, coverage 18..24). SURVIVES.
- NOVELTY: DS6 status page fetched once at 2026-11-10T17:26:37Z, HTTP 200, 29th edition (Nov 6, 2026), bound 17
  (under 6 hours old at this gate). Every pull request on the target listed: #917 (closed, at most 20) and #945
  (open, at most 22), both by this contributor; nothing published or pending reaches 25; no counterexample anywhere.
  NOVEL.
- CRITERION: meets criterion (a) in full, not only a partial win; own C checker over all 165,778,009 lines with exact
  canonical keys; regeneration two ways (leaf extension from each certified order n-1 for 18..25, and the claim's
  indep_check.py --regen for 18..24); definition is exactly super edge-magic. Five non-blocking gaps; gap 3 (no logs of
  the claimant's own n = 25 run) is answered by the run's output (indep_check.py --regen PASS at n = 25,
  2026-11-10 12:16 EST) and the package receipts.
- No downgrade trigger: no hedging on the science, no reproduction mismatch, scope no wider than reproduced (orders up
  to 17 rest on the citation the criterion builds in), no sample presented as complete, no capped search used as an
  exclusion (every residue tree was labelled), no evasion in any fetch, one claim (criterion (a)).
