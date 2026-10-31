context: subagent
role: NOVELTY skeptic (fresh; read only claim/ plus public web / gh read-only)

## 1. Primary status page (one fetch, no retries)
- URL: https://en.wikipedia.org/wiki/Tetrahedron_packing
- Fetched 2026-10-31T07:41:48Z, HTTP 200.
- Quoted: "Tetrahedra do not tile space, and an upper bound below 100% (namely, 1 - (2.6...)*10^-25) has been reported.[3]" (ref 3 = Gravel-Elser-Kallus, arXiv:1008.2830, DCG 46 (2011) 799-818).
- Value to beat: deficit 2.6e-25. Claim: deficit 4.501141e-15 (about 1.7e10 times larger) -> numerically strictly better than the table.

## 2. Literature, last 24 months (and the neighbourhood)
Two web searches ("upper bound density packing regular tetrahedra improvement GEK", "... strictly less than 1 new bound 2025 arXiv"), restricted to after 2024-10. Nothing newer than GEK 2010/2011 came up as an upper bound for regular tetrahedra. The only related hits are: Dostert-Guzman-de Oliveira Filho-Vallentin 2015 (arXiv:1510.02331, translative packings only, a different problem, a weaker bound, irrelevant to general packings), Fejes Toth-Fodor-Vigh 2015 (cross-polytope), and cylinder bounds. No release assets exist in the repo (`gh api releases` returns 0 releases). I found no published or filed rigorous bound better than 1 - 4.501141e-15. Search was limited to the web search tool and gh; I cannot exclude an obscure unindexed preprint [INFERENCE].

## 3. V3R1T4S repo (gh, read-only)
- `pr list --state all --search tetrahedra / tetrahedron / regular-tetrahedra / "Gravel Elser Kallus"`: exactly ONE hit, PR #863, OPEN, DRAFT, last updated 2026-10-31T05:53:43Z: "[claim] regular-tetrahedra-densest-packing: conditional upper bound density <= 1 - 1.0215562e-15 (p2)". No closed or merged PR on this target.
- known-knowns/ on the default branch has no regular-tetrahedra directory (404); the directory exists only inside PR #863 (`known-knowns/regular-tetrahedra-densest-packing/2026-10-31-swittensswittonio-af4e1320/`). So nothing merged. TROPHY_CASE.md (89 lines) has no line matching "tetrahed".
- known-unknowns/packings-physics/regular-tetrahedra-densest-packing.md is just the problem statement.

## 4. PR #863 versus this claim
PR #863 body: "conditional on GEK's published Lemma 3.3, Lemma 3.5 and the Lemma 4.2 nested-ball construction, and on Arb ... at most 1 - 1.0215562e-15 ... improves the deficit from 2.6e-25 to 1.0215562e-15". Object: object/REDUCTION.md, rig_dp.py, scheme.py. This is the same project, same target, same GEK inputs K1-K5 and same Arb dependency, so the claim's REDUCTION_prev.md = #863's reduction (claim says sections 1, 2.2, 2.3, 3 stay verbatim).

Is the new claim a genuine strict improvement or a re-parametrisation? Per claim/REDUCTION2.md and code/ablation.out (Q=40 best certified deficits): previous 1.0216e-15 -> multiplicity count (Claim 2', replaces conflict-graph independent set; 1/9 -> 1/q, q=6) only 1.8388e-15 -> + surface-area vertex count (Claim 3', q_v 9 -> 7) 3.0642e-15 -> + Lemma V2 (wedge excess E2 ~ 0.3537 e instead of 0.375 e) 4.5011e-15. Each step is a new proved lemma or counting argument (not a change of Q/k/u parameters; the headline Q=40 parameter set is re-optimised but the gain is mostly from the new lemmas; the ablation shows the multiplicity count alone, with the same Q, already beats #863's 1.0216e-15 by 1.8x). It names #863's object as its predecessor and beats what simple edits of it give (a parameter scan of the old scheme is exactly the 1.0216e-15 optimum). So: genuine strict improvement of #863, not a re-parametrisation. Improvement factor 4.41 over #863, ~1.7e10 over GEK.

Caveats I could not close from the claim folder (not my lens, flagged for Criterion/Reproduce): (a) conditional on GEK lemmas as KNOWN (the same status as #863; the criterion wording says "rigorous bound" and does not say unconditional; GEK's own 2.6e-25 is also built from those lemmas, so conditional-on-published-lemmas is the same standard); (b) the new Claim 2' / 3' / Lemma V2 proofs were not independently checked by me; (c) not machine-checked in a proof assistant (the criterion allows an interval-arithmetic computation the skeptic re-runs).

Duplicate question: it is not a duplicate in content (the bound is 4.4x stronger, with different lemmas), but it competes for the SAME cell/target and builds on, and strictly dominates, open draft PR #863. Filing it as a separate fresh claim would leave two overlapping open claims on one cell; the right handling is to file it naming #863 as predecessor and explicitly supersede it (or update #863 / close #863 in its favour), not to present it as independent. As a certificate it is strictly better than everything known (GEK 1 - 2.6e-25; #863 1 - 1.0215562e-15); ties: none.

## 5. Verdict
Strictly beats the published table (GEK, deficit 2.6e-25) and the only filed rival (#863, deficit 1.0215562e-15); nothing better found in literature (24 months), repo trees, PRs (open+closed) or releases. Novelty satisfied, with the supersede-#863 and conditional-on-GEK caveats stated above.

pass: true
