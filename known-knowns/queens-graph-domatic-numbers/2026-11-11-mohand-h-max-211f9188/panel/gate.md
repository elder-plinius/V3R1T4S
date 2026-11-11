status: CONFIRMED_PARTIAL
confirmed_scope: The file claim/tdom-Q10-16-partition.txt (raw-byte sha256 211f9188400687ad9e5fbe69cb47cf465acd1de52e9476992e0c7497efd034ec) labels each of the 100 squares of the 10 x 10 board with one of 16 labels so that every one of the 16 classes totally dominates the queens graph Q_10 (open neighbourhoods: every square, members included, shares a row, column or diagonal with a different member of the class), hence tdom(Q_10) >= 16, one above the lower bound 15 listed for tdom(Q_10) in Table 1 of Lauri's Corrigendum (Discrete Math. Lett. 18 (2026) 34-35) as re-fetched on 2026-11-11.

# Honesty gate — written 2026-11-11 after the three panel reports (last one finished about 18:45Z)

Claim: claim/tdom-Q10-16-partition.txt is a total domatic 16-partition of Q_10, so tdom(Q_10) >= 16 (bank target
queens-graph-domatic-numbers, partial win p1).

Panel (three fresh contexts, Claude Code Agent tool, model chosen by the human: Opus 5.5), read by the main session:
- reproduce.md: pass: true. Own checker with two implementations of total domination; controls show it separates plain
  from total domination; exhaustive single-square relabels all rejected.
- novelty.md: pass: true. Status source fetched once at 2026-11-11T18:39:44Z, HTTP 200, same sha256 as the claim's
  copy; Table 1 gives 15-16 for tdom(Q_10); no OEIS entry for this invariant; nothing found in the literature, in code
  hosting, or in this project's tree, pull requests and issues.
- criterion.md: pass: true. Own checker, control grid on which plain domination passes and total domination fails.

Downgrade checks: no hedging panelist; no reproduction mismatch; 16 is strictly above the table's lower bound 15; one
object, one cell; the scope is the lower bound only; no exhaustive search is part of the claim; no table value obtained
by evasion (single plain requests with a User-Agent naming the project); panel table fetch less than 6 hours old.
The status stands only if kit/check_run.py prints CHECK_RUN: PASS.

Points raised by the skeptics and the main session's answers (the claim package was not edited after review):
- Overlap with a published object (novelty): four classes of the object are reflected copies of one total dominating
  6-set printed in Lauri 2025, Fig. 3.3(a). No published partition was used as a seed; the search read only the list of
  216 total dominating 6-sets enumerated in this run, which necessarily contains every published 6-set. The overlap is
  credited in the package README.
- Literature and OEIS (reproduce, criterion): the author session made no literature search and re-fetched no OEIS entry
  for this claim; the novelty skeptic's searches and the criterion skeptic's OEIS query of 2026-11-11 are the record.
- Pre-registration: PREREG.v2.md records that one of the two checkers named in PREREG.md does not test total
  domination (found by this run's negative control, after the result existed) and was dropped. The object was judged
  by check.py with kind tdom, by a third check written in this run, and by the three skeptics' own checkers.
- Not part of this claim: with Lauri's upper bound 16 the object gives tdom(Q_10) = 16.
