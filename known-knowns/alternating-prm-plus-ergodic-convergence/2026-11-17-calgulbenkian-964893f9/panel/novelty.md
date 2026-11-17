context: Claude Code subagent, fresh context [Sonnet 5.5]

NOVELTY check, partial win p2 (kernel-checked proof that PRM+ does not converge in the last iterate on A = [[3,0,-3],[0,3,-4],[0,0,1]] from R = 0 and uniform strategies).

Status source (fetched once, no retries): https://arxiv.org/abs/2311.00676, 2026-11-17T05:09:21Z, HTTP 200. The page lists only v1 and v2 (v2 last revised 4 Mar 2025). Its abstract says the authors show "numerically" that RM+, predictive RM+ and alternating RM+ lack last-iterate convergence guarantees on a simple 3x3 matrix game. It proves last-iterate convergence only for the smoothed variants, ExRM+ and SPRM+. So the source proves nothing formal about non-convergence of RM+, PRM+ or alternating variants on this game. The non-convergence is left as a numerical observation, and last-iterate behaviour of the unmodified algorithms is left open. No v3 exists.

Searches, all via the arXiv API (one request each, 2026-11-17T05:09-05:10Z, hashes in the fetches file in my scratch folder):
- regret matching AND last-iterate
- "predictive regret matching"
- regret matching AND (Lean OR Coq OR Isabelle OR formalization OR formalisation)
- regret matching AND (divergence OR non-convergence OR counterexample OR CFR+)
- "RM+" AND "last iterate"
- alternating AND regret matching
A GitHub code search by curl returned 401 and counts as a failed fetch; I then used read-only gh instead.

Later and related work found (none proves the claimed statement):
- arXiv 2610.19016 (IR-PRM+ with previous-utility prediction): a different, modified algorithm. It proves positive convergence results, not non-convergence of PRM+.
- arXiv 2609.38162 (Why last-iterate scale-invariant regret matching converges linearly): proves convergence for IREG-PRM+, again a different algorithm.
- arXiv 2510.17067 (Convergence of regret matching in potential games): about KKT points of RM+, not this question.
- Other hits (2023 last-iterate algorithms, optimistic OMD CFR, bounds for approximate regret matching) are unrelated to a PRM+ counterexample.
- No Lean, Coq or Isabelle formalisation of regret matching turned up in any query. Coverage limit: arXiv plus repository only, no Google Scholar, and the GitHub code search by curl failed.

Repository check, read-only gh on elder-plinius/V3R1T4S, 2026-11-17:
- TROPHY_CASE.md: no match for regret, PRM or RM+ (grep).
- known-knowns: 34 target folders listed; none is for this target. The only hits for "regret" are inside an unrelated forecast-aggregation folder.
- the target's own page in the repository's known-unknowns folder: the target is still listed open as of 2026-10-25, with p2 worded as in the claim.
- Pull requests (open and closed, searched for "regret matching", "PRM+", "alternating-prm", "RM+"): only #649 (closed 2026-10-25), the bank proposal. It carries no proof. Nothing else concerns this target. The RM+ search returned unrelated PRs (#1043, #846, #599, #761).
- Releases: none listed.

Conclusion: within the searches above I found no published kernel-checked proof, and no repository claim, of last-iterate non-convergence of PRM+ (or RM+) on this game. The only prior statement is the paper's numerical one, which the criterion itself says is not a result. No earlier formal proof exists, so the claim strictly beats the published state; a tie is not in play. Limits: search was arXiv plus repository only, and I did not check the Lean content itself (other skeptics' job).

pass: true
