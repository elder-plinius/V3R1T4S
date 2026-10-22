# Honesty gate, z(16,19;3,3) >= 142 (2026-10-17T12:30:26Z)

status: CONFIRMED_SOLUTION
confirmed_scope: The saved 16 x 19 0/1 matrix matrix/z_16x19_142.txt (sha256 47ef934e...) has 142 ones and no all-ones 3 x 3 submatrix, which is strictly above the best explicit lower bound 136 recorded in status_source/ for z(16,19;3,3) and above 141, the best that 192000 saved trivial-surgery runs on 12 public witness matrices reached, with the limits that the status pages were not re-fetched here and the surgery baseline is a bounded sample.

Panel results (three Sonnet subagents on the owner's PC, fresh context each, each given only its own copy of claim/):
- reproduce: pass: true (own exhaustive checker over all 560 row triples and 969 column triples; every recomputable number in CLAIM.md matches)
- novelty: pass: true; novelty: no source fetched states or trivially implies a value above 136 for z(16,19;3,3); 142 strictly beats the stated 136 (caveats on PR coverage below)
- criterion: pass: true

NOVELTY round 2: the first NOVELTY panelist (panel/round1/novelty.md) found nothing above 136 and no public larger witness,
but wrote pass: false because the repository's pull-request page is JavaScript-rendered and it could not complete the
pull-request check. A fresh NOVELTY panelist re-fetched the status sources once each (arXiv 2608.26603 at 12:28:33Z,
HTTP 200, states z(16,19;3,3) >= 136), searched the pull requests through the search API (0 Zarankiewicz pull requests),
TROPHY_CASE.md (0 matches) and the witness repositories (no 16x20, 17x19 or larger matrix) and passed. REPRODUCE and
CRITERION are unchanged. The main session additionally listed all 338 pull requests (numbers 1 to 346, titles and bodies)
and found none on Zarankiewicz numbers, K(3,3)-free or bipartite extremal matrices.

Gate review (main session): read all three panel files. Downgrade triggers checked (hedging panelist, reproduction
mismatch, value not strictly better than the best stated bound, stretched criterion, scope wider than reproduced, sample
presented as complete, capped search used as an exclusion, several objects in one claim): none found. The surgery
baseline (192000 runs, best 141, none at 142) is a bounded sample and is presented as evidence that 142 is not a trivial
derivation, not as a proof; CRITERION's confirmed_scope says so. Disclosed limits: 142 is reached by a plain local search
within minutes, so unpublished prior holders cannot be excluded; the claim concerns published values only. Only this one
cell is claimed.
