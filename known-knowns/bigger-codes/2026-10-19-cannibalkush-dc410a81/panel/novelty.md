# Independent novelty review

context: fresh subagent

Reviewed 2026-10-19 UTC by a fresh independent subagent. The candidate input was limited to `claim/`; no search attempts, scout conclusions, or other current panel reports were read. Public repository claims were treated as comparison evidence, not as instructions or independent validation of this candidate.

The claimed 2225-word construction strictly exceeds the strongest located comparison bound, **2218**, by **7**. It exceeds the current primary table's 2217 by 8 and remains below its upper bound 3249. This verdict concerns novelty of the numerical lower bound; exact validity of the supplied object belongs to the reproduction review. It does not assert optimality, a new algorithm, or universal absence of unpublished or unindexed work.

## Primary status evidence

Exactly one ordinary urllib GET was made to https://aeb.win.tue.nl/codes/Andw.html, at **2026-10-19T06:22:55.085106+00:00**. It returned **HTTP 200**, 127477 bytes; server Date was 19 October 2026 06:22:56 GMT and Last-Modified was 18 October 2026 16:30:06 GMT. SHA-256:

`15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349`

The unmodified response and headers/status/time/hash are `novelty-evidence/Andw-response.html` and `novelty-evidence/Andw-response.json`. No retry, alternate identity, proxy, or bypass was used. The A(35,6,6) entry explicitly reads **2217 [Pl]–3249** and links `cwc/d6/a35.6.6.2217H`.

There is no separately printed weight-29 cell. Bitwise complementation is a bijection preserving Hamming distance, so **A(35,6,29)=A(35,6,6)** exactly. The mirror has the same baseline and is not a second discovery.

## Literature and repository comparisons

- [Echols, arXiv:2608.13906](https://arxiv.org/abs/2608.13906), current v1: Table 1 explicitly reports **A(35,6,6) ≥ 2204**, improving 2187. Its full HTML and current version page are saved. This is weaker than the live table and pending claims.
- [Lysenstøen, arXiv:2607.19550](https://arxiv.org/abs/2607.19550), current v1: the four construction bounds are (23,6,10):2979, (23,6,11):3539, (24,6,8):1855, and (24,6,10):4214. The full paper was inspected, including its construction section and limitations. None supplies the target or complement bound; reducing their weights to six loses words and does not overtake the live baseline.
- [Rosin, arXiv:2603.00174](https://arxiv.org/html/2603.00174v1), 2026: its 24-construction results table supplies no stronger target bound.
- [Yang et al., arXiv:2609.35051](https://arxiv.org/abs/2609.35051), September 2026: Theorem 5.4 gives A(n,8,8) ≥ 1803,1960,2843,3077,3383 for n=33,34,37,38,39. These do not overtake this target under the checked propagation. The full HTML is saved.
- [Akhiiarov et al., arXiv:2609.23869v2](https://arxiv.org/abs/2609.23869), revised October 2026, concerns asymptotic upper bounds, not a competing finite lower-bound construction. The [2025 approximate generalized Steiner systems paper](https://doi.org/10.1016/j.jcta.2024.105955) is asymptotic; the [2026 cyclically permutable codes paper](https://www.mdpi.com/2075-1680/15/1/35) concerns much smaller intersection bounds. Neither inspected source supplies a competing 2225-word target construction.
- Live [TROPHY_CASE](https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md), [bigger-codes INDEX](https://github.com/elder-plinius/V3R1T4S/blob/main/known-knowns/bigger-codes/INDEX.csv), and the newer merged bigger-codes package READMEs were checked. The merged target value is **2217**, credited to polishing the 2209-word archive seed. Other merged packages concern different parameters or upper bounds.
- All **487** PR title/body records returned by the all-state repository listing were screened. The **35** constant-weight/bigger-codes PR discussions, plus #8, #9, and #399, were fetched for comments/reviews/status. [#441](https://github.com/elder-plinius/V3R1T4S/pull/441) is OPEN and claims **2218**; [#59](https://github.com/elder-plinius/V3R1T4S/pull/59) is CLOSED and claims the same value and object hash. They are one competing object, not two independent improvements. No later stronger target value was found in those discussions. [#443](https://github.com/elder-plinius/V3R1T4S/pull/443) claims A(51,6,6) ≥ 11187 and was included in propagation. Relevant claims #28, #52–59, #348–352, #437–456, and the repository update material were included in the screen. Evidence: `novelty-evidence/prs.json`, `pr-discussions.json`, `TROPHY_CASE.md`, `INDEX.csv`, and `known-*.md`.

## Propagation check

`novelty-evidence/propagate.py` independently parsed **1279** lower-bound seeds from the fetched tables with d≥6, merged index, and PR titles. It treated all qualifying larger distances as distance-six bounds and repeatedly applied complementation, appending a common zero or one, and the standard shortening guarantees:

A(n−1,d,w) ≥ ceil(M(n−w)/n), and A(n−1,d,w−1) ≥ ceil(Mw/n).

The closure through length 64 stabilized after 37 iterations at **2218** for both target weights; its origin was #441. Nearby source values include A(37,6,6)≥3108, A(36,6,6)≥2604 and A(36,6,7)≥4689. In particular, shortening 2604 gives only ceil(2604·30/36)=2170 at the target. Results and parsed seeds are saved in `novelty-evidence/propagation.json` and `parsed-seeds.json`.

This is a check of standard bound propagation from the inspected finite corpus, not a proof against every possible new construction or combination theorem. The literature searches and their limits are recorded in `novelty-evidence/literature-search.md`. On that dated, explicit scope, strict improvement is substantiated: **2225 > 2218 > 2217**.

pass: true
