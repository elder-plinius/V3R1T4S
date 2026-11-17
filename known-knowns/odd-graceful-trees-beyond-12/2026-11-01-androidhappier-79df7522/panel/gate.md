# Honesty gate (main session): odd-graceful-trees-beyond-12

Panel: three fresh subagent contexts (reproduce, novelty, criterion), each given only the original claim workspace. I read all three panel
files myself and applied downgrades only.

- panel/reproduce.md: pass: true. The skeptic wrote its own C checker and its own exhaustive tree regeneration
  before reading the author's code. Every line of every certificate was checked for n = 2..22 with no sampling.
  Distinct canonical forms = lines = A000055(n), and the certificate canonical-code sets equal the regenerated sets
  (SETS_EQUAL x21). Two runs gave identical output. No mismatch.
- panel/novelty.md: pass: true. One honest GET of the DS6 page at 2026-11-01T03:00:08Z (HTTP 200, "This Version DS6:
  Oct 30, 2025"), and of the PDF (same sha256 as the claim's copy). Section 3.6 still gives order 12 (Barrientos). No
  higher bound for all trees in 24 months of literature, code, TROPHY_CASE.md, known-knowns/ or repo PRs/issues.
- panel/criterion.md: pass: true. Full criterion (a) met literally; p1 and p2 subsumed. Caveats are disclosed, not
  hedges: networkx instead of nauty gentreeg (the criterion names the tree set, not a tool, and completeness is
  established by independent regeneration); the claimant's arXiv API query got HTTP 500 (the novelty skeptic's own
  searches cover it); stray files from another target were present in the original claim workspace at panel time and have no bearing on
  this claim. At gate time the original claim workspace holds no such files (checked by grep for tsasm and a005164: none).

Gate-time status re-fetch (one GET, plain curl, User-Agent "V3R1T4S-research-agent", no retries):
https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 at 2026-11-01T03:12:12Z, HTTP 200. The page still
reads "DS6: Oct 30, 2025" (the same edition). It differs from the scout's copy (the DS6 article snapshot (not shipped)) only in the
per-session csrfToken value. Saved as gate_fetch/DS6_page_gate.html, sha256
cf4cea9032753842d2ecd4ff74616919036dfcd0f2afe14f6a5aba8244a492af. The verified bound is still 12.

Downgrade checks: no hedging panelist; no reproduction mismatch; 22 is strictly above the live bound 12; no
stretched criterion or hidden quantifier found; the scope (n = 2..22) equals what was reproduced exhaustively; no
sample presented as complete; no capped search used as an exclusion; no probabilistic step; no table value obtained
by evasion; one claim (one cell: the all-trees order bound); no benchmark baseline involved.
Downgrade reasons applied: none. Never upgrade.

Package note: panel/novelty.md line 22 names the workspace's absolute path to its repo copy. The run's panel file is
left exactly as the skeptic wrote it; only the copy in the outbox package replaces that path (see the package's
panel/REDACTIONS.md, with the sha256 of the run's original). No finding or verdict is affected.

status: CONFIRMED_SOLUTION
confirmed_scope: Every tree on at most 22 vertices is odd-graceful: for each n = 2..22 the certificate lists A000055(n) pairwise non-isomorphic trees, each with a verified odd-graceful labeling (distinct labels in [0, 2n-3], edge differences exactly {1, 3, ..., 2n-3}).
