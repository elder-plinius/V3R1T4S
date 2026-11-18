context: Claude Code subagent, fresh context [Sonnet 5.5]

# Novelty report, elliptic-quadric-q7-3-spread, partial win p1 (no automorphism of order 3)

## Fetch log (UTC, URL, HTTP, sha256)
- 2026-11-18T17:31:12Z https://arxiv.org/abs/2403.11188 200 b54a2f4cdb2bf94340a65ae21570103810d15152ae5f8ad43a1874f54525a742 (status source; matches the sha256 recorded in the-record-we-beat/README.md; latest version v3, 1 Oct 2025)
- 2026-11-18T17:31:12Z https://arxiv.org/pdf/2403.11188v3 200 57e169c70ed45a09df4d3429e5673232907ff1207e4a778b7f2be2e5769cdd0c
- 2026-11-18T17:31:30Z https://arxiv.org/pdf/2402.07882 200 cdd907cf3e37d844fa232504b2f8a380ddea37c6a38ec1dac50c9ebcfd8e8225
- 2026-11-18T17:31:30Z https://export.arxiv.org/api/query?search_query=all:"elliptic quadric" AND all:spread (sorted by date) 200 47aad2fb64fd7caa28a54b20a0119a0a92b23379804e810acdb34da5acd0455a
- 2026-11-18T17:31:33Z https://export.arxiv.org/api/query?search_query=all:"Q^-(7,3)" OR all:"\Omega^-(8,3)" 200 b591fc7fa0df022172c7c304e6c58e7147070cfb0fd99174a4b599e2022e07c6
- 2026-11-18T17:31:50Z https://api.openalex.org/works?filter=cites:W4402584757 (citing works of the paper) 200 094c5877ecc733f0819c4334e8a03ef049f61059d4b6ae3c859d2a809b0ff80b
- 2026-11-18T17:31:51Z https://export.arxiv.org/api/query?search_query=all:spread AND all:"polar space" AND all:automorphism 200 54124f49266fde9fd1709a20bd9f5cabf955689f9f35a1fb9051d295cf1646d6
- Two web searches (no URLs fetched beyond the above).

## What the status source proves
The v3 text (Sec. 6, the paragraph on spreads) reads: for q odd it is open whether a spread in Omega^-(2r+2,q), r>=3, exists; "By computer search, we could show that if in Omega^-(8,3) such a spread exists, the only prime powers that may divide the order of an automorphism are 2 or 3."
- Primes allowed: 2 and 3 only (so 5, 7, 13, 41 are excluded by them).
- Order 2 and order 3 are NOT excluded. No statement of any kind about orders 2 or 3 being impossible, and no class-by-class result. Orders 2, 3, 4, 6, 9, ... all remain allowed by that paper.
- Not implied: "no automorphism of order 3" does not follow from the published statement; it is strictly stronger than it on the prime 3.

## Later work, 2024-2026
- The 5 papers citing the status source (OpenAlex): "Nontrivial t-designs in polar spaces exist for all t" (2024-08), "Regular sets of lines in rank 3 polar spaces" (2025-01), "Intersection numbers for designs in regular semilattices" (2026-08), "From almost tight p-group enumeration..." (2026-10), "A class of LDPC codes based on attenuated polar spaces" (2026-09). None addresses spreads of Q^-(7,3).
- arXiv searches for the quadric or the spread-plus-automorphism topic: nothing relevant newer than the status source. 2402.07882 (affine vector space partitions and spreads of quadrics) only restates the equivalence of elliptic avsp with spreads of Q^-(n+1,q); no result for Q^-(7,3).
- Q^-(7,3) is not the same as Q^+(7,3), which has spreads and ovoids (unique ovoid for q in {2,3,4}); those results do not apply.
- The authors' Zenodo dataset (13353388), as recorded in the package, holds only strength-2 designs (lambda 2, 5), no spreads.
- I did not find code that settles this. Search coverage limits: arXiv API and OpenAlex plus two general web searches; I did not search the authors' personal pages or GitHub beyond that. Absence of evidence is reported as such.

## This repository
- The local checkout is stale (last commit 2026-10-17); its TROPHY_CASE.md, the repository's known-knowns folder and bank contain no entry for elliptic-quadric-q7-3-spread (grep). The package's own record states zero open or closed pull requests for the target at fetch time 2026-11-18T03:58Z. My `gh pr list --state all --limit 500` title/branch search for quadric, q7, spread and elliptic found only an unrelated elliptic-curve PR (#664). No duplicate.

## Trivial-edit check
Not a deletion, restriction, relabelling or propagation of a published object; no published object is seeded. The claim is a nonexistence statement for a symmetry class, and the published bar (only primes 2 and 3) is strictly weaker than it. Orders 5, 7, 13, 41 and the involution results are not needed for p1 and are extra; the prime exclusions merely repeat the published result.

## Limits
Novelty only. I did not verify the proof or run the checker; correctness of the nonexistence claim belongs to the other panel roles. One nuance for them: the partial win text says "order 2 (or of order 3)", and the claim covers order 3 only (order 2 is left open in the package's own "Not claimed" section for the similarity involution class Inv_0_sim), which fits the "or".

Conclusion: the order-3 exclusion is not stated or implied by the status source or any later work I could find; it strictly extends the published restriction.

pass: true
