role: criterion
context: fresh subagent (no prior conversation; saw only kit/RULES.md, the CRITERION section of PANEL_BRIEFS.md, the bank target definition, and a copy of claim/; did not open attempts/, notes/ or any other panel file)
claim: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.126988 (target brun-constant-unconditional-upper-bound, partial win p1)
date_utc: 2026-11-24T06:04:54Z

## Criterion (quoted from the bank, repo bank/targets.json, id brun-constant-unconditional-upper-bound)
Main win: "an unconditional upper bound B < U with U STRICTLY LESS (direction: min) than the smallest unconditional upper bound on
https://teorth.github.io/optimizationproblems/constants/81a.html and in any open pull request touching constants/81a.md (currently
2.288513) ... It needs a complete written proof citing each explicit input by its exact published statement (refereed sieve
inequalities, published twin-prime counts or a supplied re-verifiable enumeration), and a supplied interval-arithmetic program that
evaluates every numerical step (integrals, sums, optimisation of the sieve parameter) with outward rounding. Conditional results (GRH)
do not count for the main win."
p1: "Under GRH, a bound B < U' with U' strictly below Dunn's 2.1594, at the same proof and certification standard."
CLAIM.md quotes p1 verbatim (checked character for character against the bank).

## Verdict per requirement
1. Main win: NOT met. The result is conditional on GRH; the bank says GRH results do not count for the main win. The claim
   does not assert the main win. (KNOWN from the bank text)
2. p1 "Under GRH": met, and the hypothesis is no stronger than Dunn's. The only GRH input is Grenie-Molteni, arXiv:1709.07609v3,
   Cor. 1.2. I fetched it myself once (https://arxiv.org/pdf/1709.07609v3, 2026-11-24T06:03:01Z, HTTP 200, sha256 5b04d675...dbd).
   PROOF.md section B quotes the second line of Cor. 1.2 correctly: "Assume GRH holds. Then for all x >= 2,
   |(|G|/|C|) pi_C(x) - int_2^x du/log u| <= sqrt(x)[(1/(2pi) + 3/log x) log Delta_L + (log x/(8pi) + 1/(4pi) + 6/log x) n_L]".
   pi_C counts non-ramified primes with the given Artin symbol. The GRH there is "the Riemann hypothesis for the Dedekind zeta
   functions" (abstract). For L = Q(zeta_q) this is a product of Dirichlet L-functions, so GRH for Dirichlet L-functions is
   enough. I re-derived the specialisation myself and it is correct: K = Q, C = {a}, |G|/|C| = n_L = phi(q), and
   log Delta_L <= phi(q) log q; after dividing by phi(q) and adding li(2)/phi(q) you get exactly the c_pi bracket with
   lambda = log q/log x. Requirements I checked: x >= 2; q = [d1,d2] <= z^2 is odd and squarefree, so (-2, q) = 1;
   lambda <= 2 log z_i/log m_i <= 1/2; every term decreases in x; the checker asserts z_i < m_i^(1/4). Dunn's Theorem 1.1 is
   "Assume GRH", using JS Lemma 5.1 plus RH through Schoenfeld. "(and RH)" in the claim adds nothing beyond GRH and matches
   Dunn's hypothesis.
3. p1 "U' strictly below Dunn's 2.1594": met. 2.126988 < 2.1594, and the margin is 0.0324.
   - The standalone checker verify/check_selberg.py gives "B <= 2.1269871669853558245 (sup of the ball, recomputed)" and PASS.
     I reran it at 128 bits (sh verify/run_checks.sh, real 30.4 s). I also reran it at 256 bits from a copy that changes only
     ctx.prec, and it printed the identical line and PASS.
   - The author's program states 2.1269872000642055706. Both values are < 2.126988.
   - The status page copy (data/81a.html) lists the best conditional upper bound as 2.1594 [D2025]. Dunn's own text
     (data/dunn_arxiv2504.15658v2.txt) has "Theorem 1.1. Assume GRH. Then, B < 2.1594."
4. p1 "same proof and certification standard". The benchmark is Dunn's: a written proof plus a rigorous interval-arithmetic
   computation. I read it as the main-win standard. Met, with the notes below.
   - Written proof: PROOF.md sections A-F and S are self-contained, and every changed step is proved in the file.
     - I checked S2 (sum |lambda_d| = W/V) against Klyve's thesis text in data/klyve2007.txt:
       - Theorem 5.4 and (5.16) are on p.117.
       - (5.24) u_delta = mu(delta)/(f1(delta)V(z)) and (5.25) are on pp.122-123.
       - (5.26) and the p.125 computation V(z) lambda_delta = mu(delta) (f(delta)/f1(delta)) sum_{t<=z/delta, delta t | P_z} 1/f1(t)
         match PROOF.md S1.
       - Klyve's last step "|lambda_delta| = 1" is indeed false as an equality; "<= 1" is right. PROOF.md says this correctly.
     - I wrote my own exact-rational check (sandbox s2check.py). It builds lambda from Klyve's u_d by (5.25) for
       z in {3,5,10,17,30,64,101,150,255}. It confirms lambda_1 = 1, quadratic form = 1/V(z) exactly, sum|lambda| = W(z)/V(z)
       exactly and |lambda| <= 1 (ALL OK).
     - The algebra (1/f1(n)) sum_{delta|n} f(delta) = prod_{p|n} p/(p-2) is correct.
     - Re-derived S3(b) myself: u*f' = g at p and at p^k; sum f'(d)/d = prod(1 + 1/(p(p-2))) = 1/C2; Rankin with 1/2 < s < 1;
       |e| <= 1/2. This gives W(z) <= z/(2C2) + z^s S'(s), and using C2 >= 0.6601618 keeps the right direction.
       The lower bound V_lo for z > 1e10 uses 0.6601619 > C2, also the right direction.
   - Explicit inputs cited by exact statement:
     - Grenie-Molteni Cor. 1.2 (verified above).
     - Platt-Trudgian Lemma 6, quoted as "B(4*10^18) in [1.840503, 1.840518]".
     - pi_2(4e18) = 3023463123235320 (Bayless-Klyve-Oliveira e Silva).
     - Klyve Thm 5.4/(5.16)/(5.24)-(5.27) and Thm 5.7, with page numbers.
     - Rosser-Schoenfeld (3.6), pi(x) < 1.25506 x/log x.
     - The framework and tail are Dunn's Theorem 3.1 / Lemma 3.2. I checked them in the Dunn text: the proof gives 32 pi_2/log m_k
       and the printed lemma has 16; the claim uses the larger 32.
     - Note: the sieve inequality and the weight formula come from an unrefereed PhD thesis (Klyve 2007). Dunn's refereed paper
       relies on the same thesis theorem, and (5.16) is the classical Selberg Lambda^2 inequality, so this is not below Dunn's
       standard. I do not count it as a failure.
   - Interval arithmetic with outward rounding:
     - All analytic steps (li, c1, c2, c_pi, S'(s), S(s), A(1e10), the total) are in arb balls, and the reported value is the
       ball's sup.
     - The V and W tables are exact integer sums with directed rounding: floor(2^64/prod(p-2)) gives a lower bound for V and
       ceil(2^40 n/prod(p-2)) gives an upper bound for W. They are recomputed by an independent sieve (verify/wvcount.c) and
       checked against a pure-Python definition for n <= 20000.
     - The sieve-parameter optimisation is in floating point. This is legitimate because any admissible z_i gives a valid bound
       and the checker asserts admissibility in arb.
     - The checker sums its own recomputed sups, not the cert's stated values. A perturbed certificate fails
       (out/check_selberg_negative.txt).
5. Hidden quantifiers and stretched definitions:
   - "B" is the full sum of reciprocals of twin primes. The head is B(4e18) <= 1.840518 (Platt-Trudgian), the intervals are
     m_1 = 4e18 ... m_k = 10^2000, and the tail is Dunn Lemma 3.2. There is no truncation.
   - The pi_2(z) omission in Dunn/Klyve Theorem 5.7 is corrected (Klyve (5.27) reads pi2(x) - pi2(z) <= S(A,P,z)), and the
     checker adds 2 z_i/m_i inside each term.
   - Nothing is changed by stretching a definition: M(z), the count of odd squarefree d <= z, is replaced by Lambda(z), an upper
     bound for sum |lambda_d| of the actual Selberg weights for which the main term X/V(z) holds.
   - Null and ablation: with the weights switched off, the same code gives 2.1569669355 (the earlier value). Weights on Dunn's
     original inputs give 2.1282623. So the gain comes from change (S), not from the bracket.
6. Not subsumed:
   - The same contributor's earlier unmerged B < 2.156967 is strictly weaker: 2.126988 < 2.156967 by 0.0300.
   - This claim strictly improves on it and contains it as an ablation. It is not a re-submission of the same bound.
   - Whether anything published beats it is NOVELTY's question. I saw nothing in the supplied status page or Dunn text that does.

## Non-fatal defects (should be fixed before packaging; none changes the verdict)
- PROOF.md section A cites "verify/check.py" for the 1.03e-15 pi_2(z) correction. That file is not in claim/; the correction is
  computed in verify/check_selberg.py (term += 2 z/s).
- PROOF.md section E still lists Dunn Lemma 2.2 (r(z) above 1e7) as an inherited input. The Selberg-weight bound does not use
  M(z)/r(z); only the control ablation does. It should be marked as used only by the ablation.
- Klyve's (5.16) is printed with "=" but is an inequality; PROOF.md correctly writes "<=".
- The standalone checker hard-codes 128 bits. The kit asks for two precisions; I supplied the 256-bit rerun (identical sup).

confirmed_scope: Assuming the Generalized Riemann Hypothesis for Dirichlet L-functions, the written proof in PROOF.md together with
its arb-certified computation shows Brun's constant satisfies B < 2.126988 (sup 2.1269871669853558245), strictly below Dunn's
conditional 2.1594, which meets partial win p1 and not the main (unconditional) win.

pass: true
