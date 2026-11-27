context: Claude Code subagent, fresh context [Sonnet 5.5]

[Edited 2026-11-19 when the package was assembled: two file paths were changed to the shipped copies (the status-check record is panel/status_check_by_hand.md). The checks and verdict are unchanged.]

Role: NOVELTY (narrow brief: are Schroeder's preprint or the GitHub Lean repository enough to give this package's bound by running their method further?). Claim: partial win p2, L >= 168,131,152,814,625.

## Status-page evidence
Not fetched by me (the single honest fetch was refused with HTTP 403). Evidence is the operator's own browser read in panel/status_check_by_hand.md: the page lists the problem open and states no numeric lower bound on L; the forum thread's newest post is 15 Sep 2026 and its largest stated bound is 11,486,475 (Egeozturk); 9,704,539,845, 1,527,701,174 and 168,131,152,814,625 do not appear. That is a machine read by the operator, not verified by me.

## Fetch log (UTC; curl -A 'V3R1T4S-research (honest client; curl)'; each URL once)
- 2026-11-19T12:44:15Z https://zenodo.org/api/records/22759614 HTTP 200 sha256 99da4ccea3947f333c0ea0214fe46c3d5e819276d373a260abffcac27c14475a (record metadata)
- 2026-11-19T12:44:20Z https://zenodo.org/api/records/22759614/files/nine_prime_support_zenodo_v1.0.1.pdf/content HTTP 200 sha256 df0f8e827ca3d2a8a30b54ca8df18439e1c68bc95f8773e01b30854ecd095469 (Schroeder PDF; read in full as extracted text)
- 2026-11-19T12:44:21Z https://api.github.com/repos/rw762-sketch/Open-Math-problem/git/trees/HEAD?recursive=1 HTTP 200 sha256 a0b3412be67a34730eaeb97d1a967fcfdd58112a39ecce549accedd6b3e953f9 (file tree)
- Raw files under https://raw.githubusercontent.com/rw762-sketch/Open-Math-problem/HEAD/ , all HTTP 200:
  - 12:44:28Z README.md 975e30a19cf2a83c43dc6b3caf4c739e60b93808f183d5dbb8c9884cef06fc63
  - 12:44:28Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/MILESTONES.md 721916bf16f11c9d64889567c607ccb889ed27faa66a4840da5298e6aee889b7
  - 12:44:28Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/docs/PROGRESS.md 52a63009bfb27a27e0a0ae51579181c7715e718d606de3fb286a35d2a0c3004b
  - 12:44:29Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/RESEARCH_LOG.md 97224f02cfd7821dd9fe8c5ba488daed20cbeb730f87ab4897841de3325648d1
  - 12:44:29Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/docs/references/S26.md 302af55e9bc227bc90dd0c570848b68bd9e5b628d0056571c064e6908fe42b46
  - 12:44:29Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/docs/references/H26.md 29f719c0e134e7117ca803c607018fb34a64a8c29d8078c0fab38ee18d79d7ce
  - 12:44:30Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/docs/references/O26.md 4b7a5d7fbb6880a14b3e9fc5a2cf7b0aa63056e0f1de324e9a06dd0dfea94752
  - 12:44:30Z paper/main.tex 3ef63ce112b240a27c9a9c3611549cb3319a7f5afee1636a83de0af92066769d
  - 12:44:31Z lean/Covering/Hybrid/Main.lean 1a5eb3e3649e1903bf982b2aa65138994df606d23a1fae24021f6df0ce91e11f
  - 12:44:31Z lean/Covering/Tower.lean ffd5619a90e4f4e8c6b7647166a1a0e2f024dbde9946eb6381e42dc0814d93eb
  - 12:44:31Z lean/Covering/Phi.lean d645f6bbdcd3a5ab934aa5b35e08950c72b5f5f4f12833ef4b20a72bc1fd3de1
  - 12:44:31Z lean/Covering/Replace.lean 374a9079edaa62227a3e82910bbd7349eadf0480d3afd464b059ef34fb057948
  - 12:44:32Z lean/Covering/Hybrid/Fibre.lean 9cd4461601c97652a0bc02456ca4aa1869ce23ff0c0c1569e322422441734207
  - 12:44:32Z lean/Covering/Hybrid/Nu.lean c592dd8acf1082007dff66c176bbe91c2eba17d2915e8eda85375eaac3409bd4
  - 12:44:33Z lean/Covering/Axioms.lean 3e04da9cb42e6a114a40e4aba610188137a18c839fd0e2be73414540f41b2c3f
  - 12:44:33Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/hybrid_scan.py 1fefbcfeae6eefe8ca67a6543960a163428e50329728f18bec42d4d73446936a
  - 12:44:33Z https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/research/records/2026-11-04-uniform-exponent-certificate.md f06e713ac38fc7e5ee1ac04aa0310b9942f0128841fd672c55a088a60e8cfbc9

Read in full: the Schroeder PDF text; the Lean repo's README, MILESTONES, PROGRESS (full prose proofs), RESEARCH_LOG and reference notes. The Lean sources were fetched and their theorem names and claims were taken from README and PROGRESS; I did not rebuild Lean (not needed for a novelty judgement). I did not download the 13.6 MB Zenodo zip (the PDF is the full paper; the zip holds code).

## 1. Schroeder (Zenodo 10.5281/zenodo.22759614, v1.0.1)
What is certified: Theorem 1.1, omega(N) >= 9 for any odd distinct cover, with no exponent restriction. Method: prime replacement (Lemma 2.1) to the support {3,...,23}; countable completion (Lemma 2.2) adding all pure prime powers and the mixed moduli 15,21,35,45,63,75,105,165; a capped current-loss kernel (Lemma 3.1, density <= C_q); an ordered-increments convex comparison (Lemma 4.1); a 135-cell spatial anchor on primes 3 and 5 with two continuous deletion budgets; a charged fibre at 7 (Lemma 6.1); a fixed 165 projection at 11; a 28,001-inequality integer certificate (Prop. 10.1). A Lean formalisation of the rank theorem and corollaries is claimed.

Where the L bound comes from: Corollary 1.3 is only rank >= 9 plus one square-free argument. If omega >= 10 then N >= 31P > 3P (P = 3*5*...*29). If omega = 9 and N is square-free, a product-measure union bound (value 295112669/340623360 < 1) excludes it. So N is not square-free, rad(N) >= P and N >= 3P = 9,704,539,845. Nothing is proved about non-square-free rank-9 profiles beyond "N/rad(N) is odd and > 1".

Where it says it stops: Section 10, "Prospects for rank ten". At the hardest terminal state the six charges leave 0.0125 units; stage q = 29 adds at least 0.234; with all seven caps varied over their comparison laws the charge is at least 34.099 > 33.75; "cap retuning alone cannot complete this extension; rank ten needs a sharper comparison or additional geometric information." It never states an L bound above 9,704,539,845, and its bound is not a per-profile exclusion of lcm values.

## 2. GitHub Lean repository (rw762-sketch/Open-Math-problem, headline 2 Nov 2026)
What is certified (README, https://github.com/rw762-sketch/Open-Math-problem/blob/HEAD/docs/PROGRESS.md section 1b): odd_covering_lcm_gt_1527701174, i.e. L >= 1,527,701,175, kernel only, standard axioms. Method: prime replacement for arbitrary exponents (Replace.lean); the "distorted tower certificate": sieve the pure prime-power classes (Hackmon-style weight region), then BBMST distortion on the mixed classes using only first and second moments, eta = sum_i min(M1_i, M2_i/(4 delta_i (1-delta_i))); order and caps chosen per L; 1638 certificates for initial-run profiles. Convex comparison and capped fibre kernels are NOT used.

Where it says it stops: every odd abundant L <= 1e10 is excluded except 20 values, the first being 1,527,701,175 = 3^3 5^2 7^2 11 13 17 19 (eta = 1.014). README "Beyond": it "cannot give omega(lcm) >= 6" for large exponents; "Going further needs an exact (non-union-bound) treatment of the first mixed stage {3,5}, or a prime-by-prime distorted sieve in the style of Hough / BBMST." MILESTONES: an exact {3,5} first stage was tried with no gain; higher moments (k <= 4) give no gain; the only routes named are a prime-by-prime distorted sieve or "Schroeder-style conditional reweighting". It states it never rebuilt Schroeder's package. Nothing in the repository states a bound above 1.5277e9 (a certificate file for L <= 1e10 sits in the tree).

## 3. Comparison with the package (README.md, Lemmas 1-5)
Candour first: the package's lemma set is, in substance, already in the sources.
- Lemma 1 (prime replacement, abundancy): Schroeder Lemma 2.1; Lean Replace.lean.
- Lemma 3 (pure prime-power completion with pairwise disjoint pure classes): Schroeder Lemma 2.2, specialised to pure powers.
- Lemma 4(1) (pure-deletion product bound): BFF, the Lean tower certificate, and Schroeder's Corollary 1.3 union bound.
- Lemma 4(2) (capped fibre kernel, k_i <= C_i, loss (1 - C u(G))_+): Schroeder Lemma 3.1, near word for word (same two-case density).
- Lemma 5 (nested convex comparison with U ~ Unif[0,1]): Schroeder Lemma 4.1 (same statement and proof), applied backward by coordinate as in his Section 4.
- Lemma 2 (3^k band scaling): elementary monotonicity (a covering mod L* is a covering mod 3^k L*, and sigma(N)/N is non-decreasing). It is not stated in either source but is trivial, a bookkeeping device only.
The package's README credits Schroeder for the capped kernels and the comonotone comparison. So the package does NOT rely on a lemma that neither source has. Its new content is a combination and an application: (i) the Lean repo's architecture (prime replacement, then exclude every initial-run profile with L below a bound by an explicit certificate); (ii) a pure-deleted uniform measure on the first k0 primes, as in the Lean tower measure; (iii) Schroeder's capped kernels and convex comparison from prime k0 onward; (iv) fixed dyadic caps C_i = m_i/32 chosen per profile; (v) a scan over 30,147 / 7,036 / 4,517 profiles with exact rational checks.

Is it obtainable by running a source's method unchanged with more computation? No.
- Lean method unchanged: its own scan stops at 1,527,701,175 (eta = 1.014 there); more computation only confirms failures. It uses no convex comparison, which is what lets the package go further, and its authors list "Schroeder-style reweighting" as the untried route.
- Schroeder method unchanged: proves omega >= 9; its machinery is a bespoke rank-eight geometry (135-cell anchor, 28,001 inequalities) that its author says fails at rank ten for unbounded exponents. It gives no per-profile exclusion of rank-9 non-square-free lcm values above 3P. The package excludes all abundant profiles up to 1.68e14, including rank-9 and rank-10 profiles with bounded exponents, with a simpler certificate that has no anchor geometry. Schroeder's rank-ten failure concerns unbounded exponents with his fixed anchor geometry; it neither predicts nor contradicts the finite-exponent per-profile result.
Neither source states or computes "run this certificate on every profile to get X". The step to X is genuine new work, though lemma-level unoriginal, and the jump over the best posted figure is 17,325x, not a polish. This is the main judgement call: a reader who counts only "new lemma" finds none; a reader who asks whether it follows from a published method unchanged must answer no. I take the brief's test (same certificate type, no new lemma, run further) as not met, because the certificate type is not either source's, and neither source's own text allows extending it.

## 4. Does any source already state a bound at or above 168,131,152,814,625?
No. Schroeder: 9,704,539,845 (Cor. 1.3) and 3,234,846,615 (Cor. 1.2), nothing larger; I searched the extracted text for the claimed number and for rank-ten bounds and found only the "Prospects for rank ten" paragraph (no theorem). Lean repo: 1,527,701,175; its README, MILESTONES, PROGRESS, RESEARCH_LOG, paper/main.tex and reference notes state nothing larger and name 11,486,475 and 1.5277e9 as walls. Cited works: Mian-Siddique 10,000; Egeozturk 11,486,475; Hackmon (at most 4 primes, i.e. omega >= 5); McNew-Setty no odd bound; Dai-Li-Li-Yi 45 | L (no further lower bound). The claimed value is about 17,325 times Schroeder's and about 1.1e5 times the Lean repo's.

## Limits
- I did not verify the correctness of the claim (that is another role), only novelty relative to the two sources and what they cite.
- I did not rebuild either source's Lean proofs and did not open the Zenodo zip. Postings after 2026-11-19T12:44Z are not covered. The status page was seen only through the operator's browser read.
- Every lemma in the package has a counterpart in Schroeder, the Lean repo or BFF. A maintainer who requires a new lemma, not merely a new combined certificate that no source runs, would treat this as a combination of published tools. I judge it not a trivial run of either method, for the reasons above.

Verdict: the bound strictly beats every bound in both sources and everything they cite. Neither source states it or anything near it. Neither source's method, run unchanged, gives it: the Lean method's own scan stops at 1,527,701,175, with its authors naming Schroeder-style reweighting as the untried route; Schroeder's method gives only 3P and says it stops at rank nine. It is not a trivial edit of a published object; it is a new combination of published lemmas applied per profile.

pass: true
