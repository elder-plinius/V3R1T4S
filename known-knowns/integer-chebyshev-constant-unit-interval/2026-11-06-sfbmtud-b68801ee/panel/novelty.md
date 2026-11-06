# Fresh novelty assessment

context: Fresh novelty subagent; only claim-package inputs and explicit revisions, public primary sources, repository catalog/PR data, and this reviewer's own retained evidence; no attempts, construction notes, other panel verdicts, other conversations, or author ancillary verifier code.

Final evaluation: 2026-11-06 UTC.

Verdict: pass for the narrowly stated numerical upper-bound object, relative to the sources and searches below. This is an AI panel assessment, not external peer review or a proof of worldwide priority. Correctness of the proposed supremum certificate is a separate panel question.

## Context and object binding

I was a fresh subagent. I read only the supplied `../claim/` package and its explicit updates, public primary sources, and the repository catalog/pull-request data identified below. I did not read search-attempt histories, research notes, other panel verdicts, other conversations, or the source author's ancillary verifier programs. The later construction-chain and finite-library-obstruction data were received as claim-package updates.

The reviewed candidate is the immutable final object, `../claim/object/candidate.json`, SHA-256 `b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce`: 213 primitive integer factors, x-degree 2000000000052, claimed normalized norm strictly below the exact rational decimal **0.422640947**. I independently checked positive integer exponents, coefficient types, and the exact total degree. `../claim/TARGET.md` requires a rigorous upper bound strictly below 0.422684697505 and a comparison with current publications. The claimed numerical improvement is 0.000043750505, approximately 0.01035 percent. No lower-bound or exact-value claim is being assessed.

## Current primary comparator

The original primary-source receipts below are retained unchanged. They were approximately 67 minutes old when the final object was reviewed; I did not present them as a new fetch. The final literature/repository refresh completed at 2026-11-06T00:03:29.434Z.

I fetched [arXiv's abstract/status page](https://arxiv.org/abs/2610.00386) once using unmodified Python urllib, without retries or a disguised user agent. HTTP 200 completed at 2026-11-05T22:56:49.458826Z. The 41374-byte response has SHA-256 `9bda8aa69e2819681666d46975d8b01afeebd7ca87b8b1302d44bde9a5918c07`; raw bytes and the URL/time/status/value receipt are retained in `novelty_evidence/`, outside the distributable claim package.

The page lists v1 on September 30, v2 on October 3, and current v3 on October 12, 2026. Its abstract rounds the upper value upward to 0.4226846976. I separately fetched and read the [v3 primary paper](https://arxiv.org/html/2610.00386v3), whose Theorem 1 states **0.422684697505** and Theorem 2 states **0.422228600019**. The former is the appropriate exact comparator. The v3 paper hash is `b84eae34f93bc17ab14b027448871ddf78718c8cfe8a464fabdc1605612e9309`.

David Niedbala Giraudin's published upper certificate is the seed and must remain credited. Its independently fetched JSON has SHA-256 `2633846f0d83a22a15b3d37f7927fd9fc585d43fcc7f8f6b083f390ca89cc0a2`, exactly matching the packaged comparator. The lower-library JSON independently fetched for comparison has SHA-256 `9aa29685d9195ea2ce89a42927fdb3525cdf9d247820cd51131755f955d74270`. No author verifier was opened. The paper credits earlier factor libraries of Flammang, Hare and Hodges, and Gorshkov–Wirsing constructions; those inherited contributions should also remain explicit.

## Comparison of mathematical objects and routine transformations

I compared primitive coefficient tuples and used exact SymPy factorization, independently of the supplied checkers. Both the published 92 w-polynomials and all 154 final-candidate polynomials absent from that list are irreducible over Q. The intersection contains 59 factors; the candidate drops 33 published factors and adds 154. Thus this particular product is not merely a sign change, permutation, integer power, or reweighting of the 92-factor certificate. The x-to-w substitution, reflection symmetry, factor-product optimization and auxiliary-function transport are established methods; no novelty of these methods is justified here.

I independently transported all 206 published lower-library polynomials: a reflection-invariant Q(x) is descended directly to w=x(1-x), and otherwise Q(x)Q(1-x) is descended. There are 198 distinct representatives. One of the final candidate's 154 added factors occurs in that set, leaving 153 absent from the two compared published lists. The one matching added factor has descending w-coefficients [6219131, -10171006, 7336756, -3062919, 815351, -143489, 16690, -1237, 53, -1]. This is a statement about these lists, **not** a claim that 153 individual factors were previously unknown everywhere. The supplied construction chain traces the final exponent-compressed object through its parent hash `782f42518e5f248f778fbeca406ad9fa5d28d44dc31fd1b6b9e588ab87abde63` to the published seed. I did not inspect the intermediate attempts. Compression of exponents is not itself a novelty claim; the final degree and factors were checked directly.

The stronger numerical comparison is supplied by the fixed-library obstruction. I re-derived its averaging lemma and wrote `novelty_evidence/check_dual_independent.py` from the statement and JSON data without reading `verify.py` or `transport_coverage.py`. Exact Fraction arithmetic checks each rational polynomial value; 512-bit Arb encloses logarithms. I verified positive masses, exact total mass one, support in [0,1/4], nonzero polynomial values at every atom, all columns, and the library hashes. I regenerated the 258-element union from my independent primary downloads and checked exact set equality. I reran this independent audit on the final package; its published-library data and measures retain the same hashes. The final results are `novelty_evidence/final_object_comparison.json` and `novelty_evidence/final_dual_comparison.json`.

| Library | Atoms | Independently confirmed strict lower floor for every reweighting |
|---|---:|---:|
| Published 92 upper factors | 92 | 0.422684674774607313 |
| Upper factors plus all symmetric lower-library representatives, 258 total | 94 | 0.422684490944649449 |

These floors exceed the final threshold 0.422640947, so the same fixed-library obstruction applies without change to the improved final claim. For coefficients b_j>=0 with sum b_j=1, averaging the objective over the certificate's probability measure gives a value at least min_j C_j, hence its supremum is at least min_j C_j. Exponentiation and the degree-doubling map give the displayed x-norm obstruction. Averaging an unsymmetrized objective with its reflection cannot increase its supremum, so the union comparison also covers arbitrary nonnegative weights on the original unsymmetrized published factors. This rules out obtaining the claimed value by reweighting the two compared published libraries alone. It is not an unrestricted lower bound on the integer Chebyshev constant and says nothing about other libraries or other transformations.

The union library hash is `8390d929c286b23d72dfffb5828bb837c99a5301bf3f379ec4da0653755b34a4`; its measure hash is `d98b8b6a435bf74dcb1ccdf3f4e68241a79fc7d168d0be2a5cfbea0bfe9eab61`. The original measure hash is `c583e46b56a9915b13003b4231db1d29b36b0a074628ca602e48ce74bfa8a29d`. Results and the fresh comparison programs are retained in `novelty_evidence/`.

## Literature, code, releases, and repository coverage

Searches on November 5–6, 2026 targeted November 5, 2024 onward, with older primary references checked where relevant. Queries covered the exact target name and decimals; integer Chebyshev constant, integer transfinite diameter, certificates, bounds, code and releases; and French, Chinese and Russian terminology. Both web engines, full-text literature search, GitHub code/repository search, and the repository release endpoint were used. Search-date labels on old papers were not treated as publication dates.

- [Qu–Yang, arXiv:2609.39505v1](https://arxiv.org/html/2609.39505v1): I read primary section 1.5 and its Theorem H. It identifies t_Z([0,1]) with the reciprocal of a limiting leading-coefficient quantity; that section does not evaluate a new numerical bound. It does not supersede this numerical target merely by supplying an identity.
- [Hare–Hodges, arXiv:1804.05985v2](https://arxiv.org/html/1804.05985v2): I read the primary introduction, which explicitly says its finite-degree advances do not improve the asymptotic 0.422685 upper bound.
- [Wang–Wu, 整Chebyshev问题及其应用, 2024](https://doi.org/10.1360/SSM-2023-0293): the primary Chinese abstract and bibliographic text were retrieved in search. It is a survey with additional interval-factor results, published before the 24-month window. A direct full-PDF fetch timed out, so this is not claimed as a complete reading.
- [Trigub–Volchkov, 2026](https://doi.org/10.1016/j.jat.2025.106225): the publisher search result describes approximation of noninteger rational constants on intervals strictly inside (0,1). No competing unit-interval zero-approximation bound appeared in the accessible abstract; the direct publisher fetch returned 403 and was not retried.
- [Pinho's October/November 2026 trace certificate](https://hexagonmath.org/2610.00695v3): the primary abstract concerns the Schur–Siegel–Smyth trace constant, not a numerical replacement for the present t_Z([0,1]) bound. No assertion of an automatic numerical implication is made.

The refreshed live [V3R1T4S trophy file](https://github.com/elder-plinius/V3R1T4S/blob/main/TROPHY_CASE.md), blob `18b731d7d4bf99efd323d48740284daccb8501b0`, contained no integer-Chebyshev result. The live `known-knowns/` listing contained 27 directories and no matching family. Proper `search_prs` calls were made separately for open and closed PRs with `Chebyshev`, and again with the exact target/bound/author terms. The broad open and closed PR searches were repeated for the final object with the same outcome: the open search returned four unrelated PRs, concerning Feigenbaum constants, domino tilings and asteroid ephemerides; the closed search and both exact searches returned none. The repository releases endpoint returned an empty list. These were PR searches, not issue-search substitutes.

The exact published decimal in GitHub code search led to the known target and a mirror of the published article. Final targeted web queries included 0.422640947 and nearby decimal prefixes, alongside a seven-day integer-Chebyshev bound query; no competing numerical certificate appeared. A GitHub code search of the final exact decimal returned only unrelated numerical datasets. Broad code and release searches likewise found no competing certificate. Search transcripts are retained in `novelty_evidence/repository_checks.json`, `web_checks.json`, `additional_checks.json`, `final_search_refresh.json`, and `final_code_search.json`.

## Scope of the pass

The primary numerical comparator was successfully re-read in this review session and its actual receipt is retained; no better competing unit-interval numerical bound was found in the recorded searches; the object differs mathematically from the shipped product; and an independently verified obstruction rules out reaching this value by arbitrary nonnegative reweighting of the two compared published factor libraries. That is enough for a scoped novelty pass for this explicit upper-bound object under criterion A, assuming the independent correctness panel confirms the claimed norm certificate.

Coverage is not exhaustive: unpublished work, unindexed code, inaccessible full texts and additional old factor tables could contain relevant material. There is no claim of a new optimization method, new symmetry reduction, discovery of every added factor, optimality, a world record, or a first-ever result. A changed candidate SHA or changed numerical threshold requires a fresh object-specific evaluation.

pass: true
