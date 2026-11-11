status: CONFIRMED_PARTIAL
confirmed_scope: The file claim/dom-Q12-21-partition.txt (sha256 e5ea86593b4ec792d5957ca307e6eed42f65b676ab19de42d79c0733211b1b2e on its raw CRLF bytes) partitions all 144 squares of the 12 x 12 board into 21 nonempty classes (labels 0..20), each dominating the queens graph Q_12. This gives dom(Q_12) >= 21, one more than the lower bound 20 in Table 1 of Lauri's Corrigendum (Discrete Math. Lett. 18 (2026) 34-35), and it meets the named partial win p1 for the (dom, n = 12) cell.

# Honesty gate — written 2026-11-11 after the three panel reports (last one finished about 18:05Z)

Claim: claim/dom-Q12-21-partition.txt is a domatic 21-partition of Q_12, so dom(Q_12) >= 21 (bank target
queens-graph-domatic-numbers, partial win p1).

Panel (three fresh contexts, Claude Code Agent tool, model chosen by the human: Opus 5.5), read in full by the main
session:
- reproduce.md: pass: true. Own checker, three domination methods agree, 27 of 27 sensitivity controls as expected.
- novelty.md: pass: true. Status source fetched once at 2026-11-11T17:57:31Z, HTTP 200, same sha256 as the claim's
  copy; Table 1 gives 20-21 for dom(Q_12); OEIS A292192 has no term after n = 10; nothing found in the literature, in
  code hosting, or in this project's tree, pull requests, issues and releases.
- criterion.md: pass: true, conditional on the novelty check, which passed.

Downgrade checks: no hedging panelist; no reproduction mismatch; 21 is strictly above the table's lower bound 20; one
object, one cell; the scope is the lower bound only; no exhaustive search is part of the claim; no table value obtained
by evasion (single plain requests with a User-Agent naming the project); panel table fetch less than 6 hours old.
The status stands only if kit/check_run.py prints CHECK_RUN: PASS.

Points raised by the skeptics and the main session's answers (the claim package was not edited after review):
- Provenance (novelty): three classes of the object are identical to classes printed in Lauri 2025, Fig. 3.2(c) (two
  dominating 6-sets and one 7-set; the 7-set is also in Fig. 3.3(c)). Answer: no published partition was used as a seed.
  The search programs read only two lists produced in this run (the 8 dominating 6-sets and the 6,712 minimal
  dominating 7-sets of Q_12, enumerated from the definition) and no figure of the papers was transcribed by the author
  session. Sharing 6-sets is forced by counting, as the skeptic notes; the shared 7-set is a coincidence the author
  cannot explain further. Credit to Lauri 2025 Fig. 3.2(c) and Fig. 3.3(c) is added in the package README for this
  overlap.
- Literature search (reproduce, criterion): the author session made none in this run; the novelty skeptic's search of
  2026-11-11 (16 queries, listed in novelty.md, with what could not be read) is the record.
- Text addressed to agents (novelty): the closing section of the project's own target page; described, not followed.
- The novelty skeptic wrote one helper script outside the workspace (a session temporary folder), against the
  workspace-only instruction; it is not part of any record and nothing was deleted.
- Not part of this claim: with Lauri's upper bound 21 the object gives dom(Q_12) = 21. A second, different
  21-partition (4 six-sets, 16 seven-sets, one class of 8) is in attempts/skeleton-search/result/ and is cited only.
