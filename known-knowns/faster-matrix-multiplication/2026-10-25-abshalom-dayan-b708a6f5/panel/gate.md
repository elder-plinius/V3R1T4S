# Honesty gate, claim <28,28,29> rank 10290, fmm-catalogue-small-format-rank

Read by the coordinating main session (Claude Code, Opus 5.5) at 2026-10-25T09:21Z.
Panel: three fresh subagents, each given only its own copy of claim/ (one batched subagent per role judged the 12 band
cells, each cell separately, with a separate verdict file per cell); claim/ unchanged since the panel started (every
file's sha256 equals panel/claim.sha256, re-checked at the gate).
- reproduce.md (Claude Sonnet 5.5): own exact checker written before reading the author's code, validated on Strassen
  <2,2,2>, naive <2,2,3> and corrupted schemes; every Brent equation holds (0 wrong), r = 10290, hashes match, no zero
  factors; the author's run_checks.sh output matches REPRODUCE.md. It did not repeat the network rebuild from LITA.
  pass: true.
- novelty.md (Claude Opus 5.5): one honest GET of every comparator on 2026-10-25 (no blocks); the live tables are
  byte-identical to the claim's copies; nothing at or below r in fmm_sota.json, the Lille index and per-format page,
  matmulcatalog, LITA (square schemes only), Perminov, MerlijnW70, the repository's pull requests or the literature
  read. pass: true.
- criterion.md (Claude Opus 5.5): every p1 clause read literally and met, main criterion not met (max(n,m,p) > 16), p2
  not applicable; own full exact Brent check (0 wrong); live fmm_sota.json, Lille index and page re-fetched
  2026-10-25T09:09Z unchanged; null models (block sums, tensor products, restriction of listed larger formats) give
  exactly the table value, never below; not subsumed by the sibling cell. pass: true.

No hedging panelist, no mismatch, value strictly below the live table (10290 < 10630, the fmm_sota.json entry; Lille page
11340), scope no wider than reproduced, one object, no sample presented as complete. Table fetches under 6 hours old.

Disclosures to carry into the pull request description (the gated claim/ is not edited):
- Earlier p1 claims using this slice method (#41 to #51) were closed unmerged on 2026-10-14 with no comment on
  record; no p1 claim of this method has been merged yet.
- The README's sibling-deletion figures count only deleting a column of A and a row of B; counting every single
  coordinate deletion (criterion.md) gives slightly lower numbers, still above this cell's rank where relevant.
- The scheme is a non-coordinate slice of LITA's published square scheme followed by exact 2-reductions; LITA must be
  credited.

status: CONFIRMED_PARTIAL
confirmed_scope: The joined object files (sha256 u b708a6f57581..., v b84fdd470305..., w 27aa43deb60a...) define a bilinear scheme over Q with exactly 10290 rank-one terms for <28,28,29> whose 516925696 Brent equations I verified exactly, and 10290 is strictly below both the live fmm_sota.json entry (10630) and the live Lille per-format page (11340) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).
