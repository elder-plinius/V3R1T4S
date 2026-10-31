context: subagent
# NOVELTY verdict: regular-tetrahedra-densest-packing, p2

## Status source (fetched once, no retry)
- URL: https://en.wikipedia.org/wiki/Tetrahedron_packing
- Fetched 2026-10-31T09:48:55Z, HTTP 200. Text: "an upper bound below 100% (namely, 1 - (2.6...)x10^-25) has been reported" (GEK, arXiv:1008.2830, DCG 46 (2011) 799-818). Best known published value is therefore 1 - 2.6e-25.

## Literature and code, last 24 months
- One web search (GEK upper bound, Wikipedia, HandWiki, Kallus slides, arXiv:1003.3301). It found no paper or preprint after 2011 that improves the 2.6e-25 upper bound. This is a single search, not exhaustive; the Wikipedia and HandWiki pages still quote 2.6e-25.
- V3R1T4S repo, read-only via gh:
  - TROPHY_CASE.md has no mention of "tetrahed".
  - Code search for "tetrahedra" finds only known-unknowns/packings-physics/regular-tetrahedra-densest-packing.md (the target entry) and unrelated files.
  - I did not read the release assets or the known-knowns/ folder in detail; I only searched for matches.
- `gh pr list --state all --search tetrahedra` returns exactly two PRs, both OPEN drafts:
  - #863 (created 2026-10-31T05:53:43Z): conditional bound 1 - 1.0215562e-15.
  - #864 (created 2026-10-31T08:50:03Z): conditional bound 1 - 4.501141e-15, "supersedes draft #863". Its body says: "Conditional on GEK's published Lemma 3.3 ..., Lemma 3.5 ... and the Lemma 4.2 nested-ball construction, plus the newly written elementary lemmas ... (not machine-checked)".
- No merged or closed PR on this target.

## Comparison with the claim
- The claim's own output code/verify_final.out says "b >= 4.501166e-15 ... CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15".
- Against #864 (4.501141e-15): the claim is numerically larger by 2.5e-20 (relative 5.6e-6). It is a strict improvement in value, but only in the 6th significant digit. The same b to 5 digits. Treat that gap as cosmetic.
- Against #863 (1.0215562e-15): 4.41 times better.
- Against the published 2.6e-25: about 1.7e10 times better.
- What is new in kind: the claim states that every lemma is proved in REDUCTION_FULL.md, so it no longer depends on the three GEK inputs that #863 and #864 assume (Lemma 3.3, Lemma 3.5, Lemma 4.2). It is the only item (published or filed) offering an unconditional bound that beats GEK. #864 is explicitly conditional, so by itself it does not give a proved bound below 1 - 2.6e-25.
- Is it subsumed by #864? In value, yes in essence: the same method and the same b to 5 digits. In status, no: #864 does not claim to prove the bound, and this claim does. I judge removal of the conditions to be new content and the only thing that makes this a result rather than a conditional one. This novelty judgement says nothing about correctness. Correctness, completeness of the lemma proofs, and the bank criterion are for the reproduce and criterion skeptics. The claim itself admits it is not machine-checked or refereed.

## Caveats
- The tie-breaker 2.5e-20 should not be presented as a record margin. The honest framing is "same value as #864, with the three GEK lemmas re-proved".
- The same contributor filed #863 and #864 and the claim is a follow-on of them, so novelty rests on the removal of conditions, not on a new idea.
- The sharpness of the 2.6e-25 baseline is a Wikipedia quote; I did not re-derive GEK's value.

pass: true
