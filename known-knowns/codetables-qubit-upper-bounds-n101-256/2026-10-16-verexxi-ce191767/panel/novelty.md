context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty review: no [[140,2,46]] qubit code (upper bound 47 -> at most 45)

## Table fetch (once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=140&k=2
- Fetched after `sleep 30` with the user agent V3R1T4S-verexxi, at 2026-10-16T21:04:31Z (date -u), HTTP status 200, no challenge page.
- Value: "Bounds on [[140,2]]: lower bound: 30, upper bound: 47" (the page footer says "Last change: 10.06.2024").
- This matches the claim's own record (data/QECC_q4_n140_k2_claimtime.html, 2026-10-16T21:00:17Z: 30 / 47).
- The claim lowers the upper bound to 45, a strict improvement of 2, and the certificate for d=47 (the literal criterion) is also provided.

## Propagation check
- check/propagation_check.txt: live (140,2) = [30,47]; neighbours (140,1) = [30,47], (141,2) = [30,47], (139,3) = [27,47].
- No neighbouring cell's upper bound is below 47, so the standard propagation rules do not already imply 45 or 46 for this cell.
- I did not rerun the propagation script; I only read its output.
- I did not re-verify the Farkas certificate itself. That is outside the novelty role.

## Repo checks (read-only)
- data/TROPHY_CASE_pinned_9b1d444.md: no entry for [[140,2]] or any codetables-qubit cell. The only grep hit was an unrelated constant-weight-codes row.
- Open pull requests on github.com/elder-plinius/V3R1T4S (77 open):
  - The first page shows verexxi claims for [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]] and [[164,1]]. None is [[140,2]].
  - A title search for "140" found no [[140,2]] claim.
  - I viewed only the first page plus that search, not all 77 titles. The first page was summarised by a fetch tool, so its list may be incomplete.

## Literature (last 24 months, arXiv search)
- I found no paper reporting an LP or shadow-enumerator upper bound below 47 for [[140,2]].
- Hits were unrelated or generic: Hamming-like bound for degenerate stabilizer codes (2306.00048), check-weight-constrained code bounds (2601.15446), distance-finding algorithms (2603.22532), and new constructions.
- The search was a limited web search, not exhaustive.

## Verdict
- Live table upper bound 47 confirmed. The claim strictly improves it, is not implied by propagation, and no competing claim or prior record was found.
- Residual uncertainty is that the PR list and literature search were not exhaustive.

pass: true
