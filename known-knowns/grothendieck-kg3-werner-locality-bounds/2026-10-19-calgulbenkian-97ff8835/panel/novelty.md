# Novelty report: kg8-e8-p2 (Grothendieck constant, E8 instance, partial win p2)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: novelty (skeptic 1 of 3). Read: the claim statement, INDEX.csv and the record files (README, paper excerpt, abstract excerpt). I did not read or run the author's verifier scripts or receipts and I did not re-derive the proof (that is for reproduce and criterion).

## Sources fetched (one plain GET each; the log is not shipped in this package; 2026-10-19 UTC)
| Source | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| arXiv abstract page of 2409.03739 (versions v1 to v4 listed; first submitted 5 Sep 2024; v4 dated 2026-10-05 per the package folder) | https://arxiv.org/abs/2409.03739 | 05:39:14 | 200 | 070b07ba4ae05a0d8df875e86927d33909e4731ee50ae065792df7d2dfac26d1 |
| arXiv API, query 2 (Grothendieck, constant, lower bound; newest first, 25 results of 68) | export.arxiv.org api query, https | 05:37:38 | 200 | 92a7b17a769dfa51ede0fcd8912fec54555c111d0c0aec79dd27208e52f4179b |
| arXiv 2609.35399v1 (28 Sep 2026), PDF | https://arxiv.org/pdf/2609.35399v1 | 05:39:14 | 200 | edd279e17475265cf7b7a4a21e59a70140da59b944a67f34533ba74c09a46478 |
| Zenodo 13693164 (supplementary files of 2409.03739) | https://zenodo.org/api/records/13693164 | 05:39:59 | 200 | 1661a1273766e534a11c302bf1535d07387baf4004f2ead96c4e1d5124f3fac5 |
| TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 05:37:22 | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| known-knowns listing | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | 05:37:22 | 200 | 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011 |

Pull requests: used the saved list of all V3R1T4S PRs (473 entries, highest 481, fetched 2026-10-19T04:30:31Z, sha256 0a1d00562d9b2af7d165703ebb9732af8e1bc3328848eba98c8cc3096dd5bb14) instead of the pulls pages. No PR title or body mentions Grothendieck, K_G or the target id grothendieck-kg3-werner-locality-bounds. known-knowns has 20 folders, none for this target. the trophy-case file has no Grothendieck entry. The arXiv API request used https (no redirect).

## What is known
- The instance (d=8, 120 x 120, E8 roots) is printed in arXiv 2409.03739v4 (tab:sym) with lower bound 165/109 = 1.5138 and an asterisk: the caption says the paper's solution of the binary problem is heuristic and the value is putative. Table `heuristic` lists d=8, 120 x 120, 1.51376 against state of the art 1.48217, and the abstract says d in (4, 7, 8) can only be solved heuristically. The largest exact (proven) bound for d >= 5 in that paper is 1.49339 (d=5), which by monotonicity applies to d=8. So the published proven lower bound on K_G(8) is 1.49339; 165/109 is published only as a heuristic.
- The matrix file is the authors' own: the Zenodo record 13693164 (version 0.0.2, 2024-09-06) lists d8_n1_120x120.mat with md5 59e20586d208c78d49c73fa9bb99c796, the same md5 as the claim's object file. Whether the file's stored values 9240 and 6104 are labelled proven there I could not tell without downloading the mat file; the paper says they are heuristic.
- Newer literature (arXiv query 2, last 24 months): 2609.35399 (28 Sep 2026) cites 165/109 = 1.513761 as the "candidate ratio" from Table I of the Designolle et al. paper and states that its own d=4..24 bounds are conditional on conjectured binary optima. 2610.10477 (7 Oct 2026) concerns the unbounded-order real constant (1.773 <= K_G <= 1.7799). 2608.11158 and 2603.22616 and 2609.20074 etc. are also about unbounded order. None proves the binary optimum 6104 for the E8 matrix or K_G(8) >= 165/109. No paper I saw (titles and abstracts of all 25 results; full text of 2609.35399 searched for the E8 instance) states a proof.

## What p2 credits
p2 credits "a certified local bound for one of the heuristic symmetric instances (d in 4, 7, 8) that turns their heuristic value into a proven bound". It does not require a larger number than the paper's heuristic value; it requires a proof where the paper has none. The ratio 165/109 equals the paper's printed heuristic value (a tie in the number), but it does not tie any proven bound: against the proven 1.49339 (d=5, propagated to d=8) it is larger by 0.0204. For the thing p2 asks (proof status) nothing published precedes it that I could find. The maintainer ruling on PR 350 does not apply: the proof is not a propagation of a table value; the value was an unproved candidate.

## Open questions answered (novelty side)
- Does the contributor's proof duplicate anything in the paper's supplementary material? The Zenodo record is metadata plus data files; I did not download the 239024-byte mat file, so I cannot say whether it stores the dual certificate. unresolved: whether the authors' data files already contain a certificate that the contributor's argument reproduces. The paper itself says it could not prove it.
- Newer paper that already proves this instance: none found in the arXiv API query (68 hits, the 25 newest read) or in 2609.35399. unresolved: arXiv listing beyond the 25 most recent hits, and papers not matching the words Grothendieck, constant, lower bound (e.g., a paper on Bell polytopes or E8 lattice binary quadratic programs).
- Whether the argument is complete and correct, whether a second exact method is required, and whether floating-point LP duals verified exactly suffice are not novelty questions; I leave them to reproduce and criterion.

## Verdict
No published or queued proof of the binary optimum 6104, hence of K_G(8) >= 165/109, was found; the number 165/109 itself is published only as a heuristic candidate (2409.03739v4 and 2609.35399). The claim is new as a proof (p2), not as a number, and strictly above the published proven bound 1.49339 for d=8. Caveats: the number is a tie with the printed heuristic; the matrix is the authors' own; two unresolved literature gaps above.

novelty: NEW as a proof of an already-printed heuristic value (p2 reading); not new as a number

pass: true
