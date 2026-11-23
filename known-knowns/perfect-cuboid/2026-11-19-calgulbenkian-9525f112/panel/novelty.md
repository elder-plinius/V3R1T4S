context: Claude Code subagent, fresh context [Sonnet 5.5]

# NOVELTY report, perfect-cuboid p1

## Fetch log (honest, no retries; all worked in WORK, one folder each)
- 2026-11-19T05:49:12Z https://en.wikipedia.org/wiki/Euler_brick HTTP 200 sha256 c9e13da3fa92464a1c28163858afcae7af6aef2e7acda2f492e0102429b6db98 (matches the package's hash). Status text: "no example of a perfect cuboid had been found and no one has proven that none exist." Cell value: OPEN.
- 2026-11-19T05:49:13Z https://arxiv.org/pdf/2401.06784 HTTP 200 sha256 8498dd78...23d4 (matches package)
- 2026-11-19T05:49:13Z https://arxiv.org/pdf/2604.28072 HTTP 200 sha256 1b91c4ad...a05e (matches)
- 2026-11-19T05:49:14Z https://arxiv.org/pdf/2609.14526 HTTP 200 sha256 7a961832...6599 (package hashed the e-print, not the PDF; not comparable)
- 2026-11-19T05:49:16Z https://pub.math.leidenuniv.nl/~luijkrmvan/ps/cuboids.pdf HTTP 200 sha256 2ab77033...174c (matches)
- 2026-11-19T05:50:05Z https://arxiv.org/pdf/2609.38650 HTTP 200 sha256 f834ef31...e1e3 (checked as a possible competitor; unrelated)
- Two web searches (standard and extended) for 2024-2026 follow-ups.

## Findings
1. de Grey-Gibbs-Helm: Theorem 5 (7.4) gives the two internal-ratio edge-cuboid families, with the generators and the tangent-doubling construction. Section 7.2 excludes the face-ratio family (cites a known descent). Section 10.2 states, verbatim in substance: "It would be of interest to prove that members of the two internal-ratio families can also never be PCs". So those two families are exactly the ones left open there. Section 9.1.2 only excludes individual ratios for p <= 103 via rank tests, not these families.
2. van Luijk 2000 (pp. 4-5, and the surrounding text): constructs cycles of four from Q and 2Q; says every Pythagorean triangle occurs as an edge cuboid; contains no statement that c^2 is never a square for these families. Grep of the thesis finds nothing on that. Not handled there.
3. Peschmann (2604.28072) and Cipollini (2609.14526): work in master-tuple language (fix (m,n), vary (a,b)), bounded max(m,n) <= 100, 1072 + 968 fibers. Neither mentions edge cuboids, van Luijk, the internal-ratio families or Euler's quartic in this role. Cipollini says explicitly it is a bounded-fiber theorem. The package's families are a different parametrization, so they are not covered by these papers, and not excluded by them.
4. 2024-2026 other work found (2609.38650 square-class finiteness, 2610.10643 rank condition, 2510.11768, 2604.09328, 2602.00239 and older claimed proofs): none treats the dGGH internal-ratio families. No claimed exclusion found.
5. Classical results: Spohn 1972 (Saunderson family), Leech 1977 (Euler and derived cuboids, face-ratio family), Colman, Korec: none covers these internal-ratio families according to dGGH, who knew the literature and called it open in 2024. The package's own reduction ends in Euler's classical quartic x^4+x^2y^2+y^4=z^2 (no nontrivial solutions). That is a classical ingredient, but I found no publication that applies it to these families, so the exclusion is not an already stated fact. Risk: it may be viewed as an easy corollary of Euler's quartic; this does not make it a published result.
6. Own quick sanity test (not shipped in this package): the package's unified c^2(a,e) = e^2(e^4-a^2e^2-a^4)(e^4+3a^2e^2+3a^4) is never a positive square over 64,670 (a,e) pairs from primitive triples with m < 400, both orderings. Consistent with the claim. This is a spot check only; correctness of the formula versus dGGH Theorem 5, and the proof, are for the reproduce/criterion roles.
7. This repository: bank entry and TROPHY_CASE.md / known-knowns have no cuboid result; gh search of all PRs returned nothing for cuboid or brick. No prior package.

## Comparison to bar
The p1 text allows "a whole elliptic fibration of the de Grey-Gibbs-Helm reformulation" and an explicit infinite family not covered by the 1072 fibers. The two internal-ratio families are infinite, explicitly open in the dGGH paper, not in van Luijk's thesis as a result, and not in Peschmann/Cipollini. Not obtainable by trivial edits of a published object. The status page is still OPEN, so no later upstream value beats it.

Caveat: dGGH say "members of the families", and the claim concerns the doubled-tangent edge cuboids at integer (p,q) under rescaling; whether this equals "the families" fully is a criterion-role question. Novelty only: not published, not implied by anything I found.

pass: true
