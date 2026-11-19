context: Claude Code subagent, fresh context [Sonnet 5.5]

[Edited 2026-11-19 when answering the maintainer's review: a reference to a working file not shipped in this package was removed. The checks, numbers and verdict are unchanged.]

Novelty check for partial win p1 (rigorous POVM-valid upper bound <= 0.6990 on the 3-trits-into-1-qutrit QRAC; claimed 4368312591/6250000000 = 0.69893001456).

Status source (read once, no retries): 2026-11-17T03:54:05Z, https://arxiv.org/abs/2312.14142 (HTTP 200) and the paper PDF https://arxiv.org/pdf/2312.14142 (HTTP 200, same time). Abstract page: submitted 21 Dec 2023; the paper was accepted in Quantum 2025-02-11. What the paper gives for n = d = D = 3:
- Seesaw lower value 0.69715 (table row (3,3)), MUB value about 0.6971.
- Analytic upper bound 0.71823 (Corollary 1).
- QDimSum (QDimSum SDP hierarchy) upper bounds, explicitly projective-only: level 1 0.7182; 1+rhoM 0.6989; 2 0.6989; 2+MMM 0.6989; 2+rhoMM 0.69855; 2+MMM+rhoMM 0.69853. The paper says these may be lower than the true maximum because projective measurements are assumed. They are floating-point, not certificates.
- The POVM-valid almost-qudit SDP (Pauwels et al., arXiv:2208.07887) is only plotted in Fig. 2, not tabulated; the claim folder reads it as about 0.699. It is floating-point with no exact certificate. The paper text gives no rigorous POVM-valid bound at or below 0.6990.
So the table's best number is 0.69853 (projective-only, floating-point) and 0.71823 is the best rigorous bound. The claim's 0.69893 does not beat 0.69853, and it does not claim to. It is a p1 partial win (rigorous and POVM-valid), not a main-criterion win.

Literature search (arXiv API, plain GET, 2026-11-17T03:54-03:55Z, all HTTP 200):
- all:"random access code" AND all:qutrit (sorted by newest): hits were Prepare-and-Magic, Bell vs prepare-measure incompatibility, Quantum Advantage in Information Retrieval; none gives a 3-trit qutrit QRAC bound.
- all:"random access" AND all:"upper bound" AND all:POVM: (n,n-1) QRAC analytic construction; quantum one-time memories; neither is this case.
- all:"random access codes" AND all:NPA: one hit, chain-shaped prepare-and-measure networks; not this case.
- all:"random access code" AND all:Naimark: no results.
- all:"random access codes" AND all:dimension AND all:semidefinite: absolutely entangled sets certification (2026-09), semi-DI QKD (2026-07), Almost qudits (2022), Characterizing finite-dimensional quantum behavior (2015); none gives an exact bound for this case.
- A citations query (cit:) returned nothing useful (not supported by that API).
Limits: I used only the arXiv API and the GitHub CLI (no Google Scholar or journal-site search), so a bound buried in a non-arXiv venue or in a paper that does not use these keywords could be missed. I did not re-fetch 2208.07887; its value comes from the claim folder's description and the 2312.14142 Fig. 2 discussion.

Repository check (read-only gh, same time window): searches of elder-plinius/V3R1T4S pull requests for "qrac", "qutrit", "random access code", "Naimark" and the target id qrac-qutrit-three-trits-smallest-open found no claim on this target. The only QRAC pull request is #1101 (open), a 4-to-1 QRAC with shared randomness, a different target. Issues search for the target id: empty. TROPHY_CASE.md has no mention of this target. known-knowns has no QRAC entry (the folder lists entries such as eaqecc-qutrit-codetables-gaps, none on QRACs). known-unknowns holds the target definition file for this id and a separate one for the shared-randomness QRAC. No merged or open package claims a rigorous POVM-valid bound for this case.

Conclusion: no published or merged rigorous, exactly verified, POVM-valid upper bound at or below 0.6990 for n = d = D = 3 was found. The nearest items (0.69853 projective-only; Pauwels et al. about 0.699 floating-point) do not meet the "rigorous and POVM-valid" description of p1, so the claim is not tied or beaten on that description. Caveat: if the Pauwels value is read as a bound strictly below 0.69893 in floating point, it is not rigorous, so under the p1 wording it is not a rival record.

pass: true
