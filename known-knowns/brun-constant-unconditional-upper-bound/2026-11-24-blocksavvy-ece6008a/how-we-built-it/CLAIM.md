# Claim
One sentence: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.1257395.
target_id: brun-constant-unconditional-upper-bound (partial win p1)
Criterion p1 (verbatim from the bank): "Under GRH, a bound B < U' with U' strictly below Dunn's 2.1594, at the same proof and
certification standard."
Status source: https://teorth.github.io/optimizationproblems/constants/81a.html, fetched 2026-11-24T07:29:34Z (HTTP 200, sha256
f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9, data/81a.html): best conditional upper bound 2.1594 [Dunn],
best unconditional 2.288513 [Platt-Trudgian]. GitHub search API 2026-11-24T07:29:34Z (HTTP 200): 0 open pull requests in
teorth/optimizationproblems matching "81a" (data/prs_81a_search.json; title/body search only).
Relation to earlier work by the same contributor (none merged or refereed): B < 2.156967 (2026-11-23-blocksavvy-a26bba47, draft PR
#1231) and B < 2.126988 (2026-11-24-blocksavvy-e6b84d42, branch pushed for a draft PR). This claim keeps the e6b84d42 proof and
changes one step (PROOF_DELTA.md, section R of PROOF.md).
Value: B <= 2.1257393973040676877 (standalone checker verify/check_rho.py, 128 and 256 bits, sup of the arb ball, recomputed from
definitions); the author's program gives 2.1257394310040893870 at 128 and 256 bits. Claimed, rounded up: 2.1257395.
Method: as e6b84d42 (Dunn arXiv:2504.15658v2 Theorem 3.1; q-dependent GRH constant, direct li, own V lemma, pi_2(z) correction,
exact Selberg weights). New: in the sieve remainder, the weight products are first combined per modulus q = [d1,d2]:
sum lambda_d1 lambda_d2 R_[d1,d2] = sum_q rho_q R_q, and Lambda(z)^2 is replaced by Sigma(z) = sum_q |rho_q| (about 0.645 Lambda^2)
for the 22 intervals with z_i <= 20000. Sigma is bounded with exact rational weights and exact integer sums.
Control: change switched off -> 2.1269872000642055706 (the e6b84d42 value).
Hypothesis: GRH for the Dedekind zeta functions of Q(zeta_q), which factor into Dirichlet L-functions.
Supersedes (post-panel erratum (e)): this claim is intended to SUPERSEDE submission 2026-11-24-blocksavvy-e6b84d42 / PR #1232
(B < 2.126988) for the same table cell; both rest on the same base proof. Five of the 22 rho intervals sit at the 20000 cap
(n = 19993, 19997, 19999), so the cap, not the method, limits the gain. Margin: the certified value is about 1.0e-7 below 2.1257395.
Not claimed: anything unconditional; the main win. Sigma is used only for z_i <= 20000 (larger z needs a different algorithm; see
the run report).
Files: PROOF.md (full proof: section R + the e6b84d42 proof verbatim), PROOF_DELTA.md, REPRODUCE.md, code/, out/, verify/, data/
(status page, PR search, Klyve thesis text, Dunn arXiv text).
