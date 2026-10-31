# Novelty skeptic report: claim/ (bound 1 - 1.0215562e-15)

context: subagent

## Status page (one plain fetch, no retry)
- URL: https://en.wikipedia.org/wiki/Tetrahedron_packing (read tool, "Fetched via Wikipedia API"; fetched at about 2026-10-31T05:17Z by my clock)
- Value stated: "an upper bound below 100% (namely, 1 − (2.6...)·10^-25) has been reported" [3] = Gravel-Elser-Kallus. Best lower bound 85.63% (Chen-Engel-Glotzer). No other upper bound is listed.
- The page text I received has no "last edited" stamp, so I cannot independently confirm the claim's sha256; the value is the same as the claim's quote.

## Literature and code search (about 8 queries on arXiv, Springer, Zenodo, GitHub; one-shot each)
- GEK, arXiv:1008.2830 (DCG 46, 2011): abstract and full text read. Empty-space fraction 2.6...e-25 for tetrahedra, 1.4e-12 for octahedra. Their Table 1 gives rho_hat(0,5) = 8.5e-19. They explicitly "chose simplicity of the proof at the expense of tightness" and pose a challenge for a much larger deficit.
- Follow-up and related searches found nothing that improves it: Kallus/Elser/Gravel seminar slides (Harvard 2010, NYU 2010) repeat only GEK. De Laat-Oliveira-Vallentin (arXiv:1510.02331) gives translative-packing bounds for bodies with tetrahedral symmetry, not for the regular tetrahedron. Zong's AMS Notices 2012 survey and the Lagarias ICERM 2015 slides quote "delta < 1 - 2.6e-25" as the best known. Later citations (Mysteries in Packing Regular Tetrahedra, Zong) still quote 2.6e-25. arXiv:2505.14110 is about binary sphere packings, not relevant.
- No hit for Torquato-Jiao, Glotzer, Hales-style, or Fernique upper bounds for regular tetrahedra. I found none.
- Zenodo and GitHub: web search found no repo or record with a regular-tetrahedron bound near 1e-15.
- V3R1T4S repo (https://github.com/elder-plinius/V3R1T4S): TROPHY_CASE.md contains no "tetra" string. I scanned all 600 PRs (open pages 1-5, closed pages 1-6, GitHub API, all pages exhausted) for "tetra": the only title match is open #375 (polytetrahedral Dzugutov cluster energies, unrelated). bank/targets.json has the target id regular-tetrahedra-densest-packing and no claim attached. No existing or earlier submission of this bound was found.

## Plausibility
- Arithmetic check: b = (120/9)(4pi/3)/v_t * u^3 * rho(0,40) = 473.9 * 5.927e-7 * 3.637e-12 = 1.0216e-15. Consistent with the claim.
- A 1e-15 deficit is consistent with what the nested-ball method can give: the dominant loss in GEK is the tiny sphere radius and one ball per tetrahedron edge. Claim gains from (i) pearls (120 good balls per tetrahedron, independent-set fraction 1/9) and (ii) a better rho(0,5) (8.6e-12 vs GEK 8.5e-19, 7 orders). Both are mechanisms GEK themselves left on the table. Nothing in the literature gives an upper bound on rho(0,5) that this contradicts; the known true deficit is >= 14% so nothing contradicts a 1e-15 deficit.
- The jump in rho(0,5) by 7 orders is the one number that deserves scrutiny by the criterion/reproduce skeptics (new Lemma V and profile recursion replace GEK's single-radius DP; the claim's own float prototype agrees at 1.1e-11). I did not audit the proof, which is the others' remit.
- I re-ran in a fresh venv (python-flint, numpy) a temp copy: rig_dp.py 150, scheme.py 40, verify_final.py all reproduce rho_hat(0,5) >= 8.619948e-12, rho(0,Q) = 3.636896e-12, b >= 1.021556e-15, "CERTIFIED density <= 1 - 1.021556e-15", ratio to GEK 3.929e9. The numbers match REPRODUCE.md.
- Conditional on K1-K5 (GEK lemmas, K4's constant only checked numerically) and unproved-in-a-proof-assistant Arb; correctness of those is outside novelty.

## Verdict (novelty only)
No published or posted upper bound for regular tetrahedra at or below 1 - 1.0215562e-15 was found; the claimed value strictly improves the only published bound (GEK 2.6e-25) and is not already in the V3R1T4S repo or PRs. Novelty confirmed; validity of the proof is for the other skeptics.

pass: true
