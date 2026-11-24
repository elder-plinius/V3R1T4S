# Claim
One sentence: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.126988.
target_id: brun-constant-unconditional-upper-bound (partial win p1)
Criterion p1 (verbatim from the bank): "Under GRH, a bound B < U' with U' strictly below Dunn's 2.1594, at the same proof and
certification standard."
Status source: https://teorth.github.io/optimizationproblems/constants/81a.html, fetched 2026-11-24T05:32:04Z (HTTP 200, sha256
f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9, data/81a.html): best conditional upper bound 2.1594 [Dunn],
best unconditional 2.288513 [Platt-Trudgian]. GitHub search API 2026-11-24T05:37:17Z (HTTP 200): 0 open pull requests in
teorth/optimizationproblems matching "81a" (data/prs_81a_search.json; title/body search only).
Relation to earlier work by the same contributor: a bound B < 2.156967 under the same hypothesis was submitted on 2026-11-23 as
a pull request to the V3R1T4S repository (not yet merged or refereed). This claim keeps that proof and replaces one step.
Value: B <= 2.1269871669853558245 (standalone checker verify/check_selberg.py, sup of the arb ball, recomputed from definitions);
the author's program gives 2.1269872000642055706 at 128 and 256 bits. Rounded up: 2.126988.
Method: Dunn's framework (arXiv:2504.15658v2 Theorem 3.1) with the submitted changes (B) q-dependent GRH constant (Grenie-Molteni
Cor. 1.2), (L) li computed directly, (V) own V(z) lemma, the pi_2(z) correction, and the new change (S): in the sieve error term
the bound |lambda_d| <= 1 is replaced by the exact Selberg weights from Klyve's proof, using
sum_{d<=z} |lambda_d| = W(z)/V(z), W(z) = sum_{n<=z, n odd squarefree} prod_{p|n} p/(p-2) (PROOF.md section S).
Ablations (out/): weights off -> 2.1569669355299588530 (the submitted value); weights on Dunn's original inputs -> 2.1282623410.
Hypothesis: GRH for the Dedekind zeta functions of Q(zeta_q), which factor into Dirichlet L-functions.
Files: PROOF.md, REPRODUCE.md, code/, out/, verify/, data/ (status page, PR search, Klyve thesis text, Dunn arXiv text).
