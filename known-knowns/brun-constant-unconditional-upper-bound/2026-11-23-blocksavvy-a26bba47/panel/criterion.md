# CRITERION skeptic: brun-constant-unconditional-upper-bound, partial win p1
context: subagent (fresh knowledgeWork context, started by the parent session; saw only claim/, PREREG.md, PREREG.v2.md, the bank entry, and primary sources fetched independently from arXiv)
date (date -u at check): Mon Nov 23 17:17 UTC 2026
claim/ hashes checked: CLAIM.md 25f3f9a5..., PROOF.md cff35346..., code/replay.py b5ece49f..., code/vsieve_fx.c f4b33018..., code/vlemma.py f8af4a39...

## Criterion, literally
Bank p1: "Under GRH, a bound B < U' with U' strictly below Dunn's 2.1594, at the same proof and certification standard."
The main win is out of scope because it needs an unconditional bound, and this claim is conditional. The claim asserts p1 only.
- Hypothesis: the claim assumes GRH for Dirichlet L-functions, including RH. That is no stronger than "GRH" in p1 and in Dunn. PASS.
- Value: U'' = 2.1569669355299578202 is the sup of the arb ball. I reran it at 128 and 256 bits after rebuilding every table from
  claim/code, and both runs gave the same sup. The headline 2.156967 is that sup rounded up. Both are strictly below 2.1594. PASS.
- PREREG.v2 bar: R = 2.1593210323778804655 (I reproduced it), so R - 1e-4 = 2.15922103. U'' is at or below that and at or
  below 2.15939. The improvement comes from a stated input change: change (B) is the modulus-dependent GRH error constant, and
  PREREG.md listed it in advance as L3(b). It does not come from re-optimising parameters. U' = 2.1569562895 is change (B) alone,
  using Dunn's own z-bracket rule and all of Dunn's other inputs. The c_pi with lambda is pointwise <= Dunn's c_pi, with equality
  at lambda = 1/2, so the gain does not depend on the optimiser. PASS.
- Same certification standard: every term is evaluated in arb ball arithmetic and the sup of the final ball is reported. The
  V(z) tables are exact fixed-point lower bounds (floor(2^64/prod(p-2)) summed in u128, so the dense doubles round down). M(z)
  are exact integer counts. The z_i come from a float optimiser and are only parameters; the code asserts z_i <= m_i^(1/4).
  As an independent check, I recomputed V(1e6) in arb from a smallest-prime-factor sieve: [11.425902775340183195 +/- 2.5e-19].
  The table value 11.425902775340171 is below it, a valid lower bound. M(1e6) = 405286 also matches. PASS.
- The headline also removes two inputs that were never published in refereed form: Klyve's thesis constant c3 = 12.6244
  (replaced by a proved lemma) and the Dusart/Schoenfeld li bracketing (li is now computed directly). Both swaps only raise the
  bound, from 2.156957 to 2.156967.

## Proof audit (PROOF.md)
1. Grenie-Molteni Cor. 1.2 (I fetched arXiv:1709.07609v3, HTTP 200). The statement is quoted correctly: for x >= 2,
   |(|G|/|C|) pi_C(x) - int_2^x du/log u| <= sqrt(x)[(1/(2pi) + 3/log x) log Delta_L + (log x/(8pi) + 1/(4pi) + 6/log x) n_L].
   It is applied to K = Q, L = Q(zeta_q), C = {-2 mod q}, with q = [d1,d2] odd squarefree, so (-2,q) = 1. The ramified primes
   p | q cannot satisfy q | p+2, so pi_C = pi(x;q,-2). The other inputs are |G|/|C| = phi(q) = n_L and
   log Delta_L <= phi(q) log q. I re-derived the division by phi(q) and the li(2) shift and got PROOF.md's bracket exactly.
   At lambda = 1/2 it reduces to Johnston-Starichkova Lemma 5.1's c_pi (I fetched arXiv:2208.01229 and checked it).
   The range is x >= 2 with no restriction on q, so q <= z^2 is fine. lambda <= 2 log z_i / log m_i holds and each term
   decreases in x. The code clamps lambda at 1/2 conservatively whenever the ball straddles it.
   q = 1: GM prove Theorem 1.1 for L = Q explicitly (Sec. 5: "For L = Q, the theorem is weaker than Schoenfeld's result"), so
   Cor. 1.2 covers q = 1. Schoenfeld's RH bound |pi(x) - li(x)| < sqrt(x) log x/(8 pi) would be smaller still. Either way q = 1
   is covered. This also fixes a small slip in Dunn: JS Lemma 5.1 assumes q >= 3, but Dunn applied it to every [d1,d2].
   Hypothesis: GM's proof uses Hecke L-functions L(s,chi,L/E) with E inside L. For abelian L/Q these divide zeta_L, which is a
   product of Dirichlet L-functions, so GRH for Dirichlet L-functions (including zeta) suffices. The "Dirichlet-only" claim is
   correct.
2. Dunn's framework (I fetched arXiv:2504.15658v2). The structure is reused faithfully: Thm 2.1 sieve, Lemma 3.1 partial
   summation with c1 = int li/t^2 and c2 = int t^(-3/2) log t, and the Lemma 3.2 tail. The code matches it term by term.
   The tail coefficient 32*C2/log m_k is right: Platt-Trudgian Lemma 3 (arXiv:1803.01925, fetched) has 16C with
   C = 2*C2 = 1.3203..., and Dunn's printed "16" counts C2 differently. B(4e18) <= 1.840518 matches PT Lemma 6, and
   pi_2(4e18) = 3023463123235320 matches PT Lemma 5.
   Numbering: CLAIM/PROOF cite "Dunn Theorem 3.3". arXiv v2 numbers it Theorem 3.1. The published BAustMS numbering may
   differ, and I did not check it.
3. Change (V), the lower bound on V(z) for z > 1e10. I re-derived every step and found it correct:
   - the Dirichlet-convolution identity h = u*f, at p, p^2 and p^k;
   - O(t) = H(t) - H(t/2)/2 with |eps(t)| <= 4/t for t >= 1, including the case 1 <= t < 2;
   - the three-sum decomposition, the uniform bound in z, the Rankin bounds and the max of g(u)u^-s at u = 1 (needs
     kappa + 4 >= 1/(2s); at s = 0.44 it is 4.635 >= 1.136);
   - S(s) as an Euler product, with the prime tail via Rosser-Schoenfeld pi(x) < 1.25506 x/log x and partial summation;
   - sum_d f(d) = 1/C2;
   - 0.6601619 > C2.
   I reran vlemma.py: A(1e10) <= 0.010700091 < 0.0107001. V_lo(1e10) = 18.401710861595 matches my rebuild.
4. Change (L), the direct li(x). d/dt[log log t - li(t)/t] = li(t)/t^2, as claimed. python-flint arb.li() defaults to
   li = int_0, which is >= int_2, so the result is valid and conservative under either convention. It is also consistent with
   the li(2) term added to c_pi.

## Gaps found (none affects the verdict)
- G1 (inherited from Dunn Thm 2.1): pi_2(x) <= S(A,P,z) leaves out twin pairs whose larger member p+2 is <= z, because those
  are sieved out. The correct bound is pi_2(x) <= S + pi(z). The extra contribution is <= 2 sum_i pi(z_i)/m_i
  <= 2 sum_i m_i^(-3/4) < 6.1e-14. The headline's rounding margin is 2.156967 - 2.1569669355 = 6.4e-8, so B < 2.156967 still
  holds. PROOF.md should state this term.
- G2 (claim hygiene, RULES rule 1): CLAIM.md was last modified at 17:07:16Z (file mtime), yet it says the status page was
  "re-fetched 2026-11-23 ~17:20Z". That time is later than the file itself, so it cannot be a real fetch time. The gate must
  correct or remove that line. p1 compares against Dunn's fixed 2.1594, so this does not change the criterion verdict. The
  live-table and novelty check is NOVELTY's job.
- G3 (process): PREREG.md says "L3 improver (NOT started today; needs Matthew's go for the compute)", but L3(b) is the source
  of this result. The gate should confirm that the go-ahead was given. This is outside the criterion itself.
- G4 (minor): Dunn's r(z) formula above 1e7 (his Prop. 2.1 / Lemma 2.2) and the Selberg sieve inequality (via Klyve Thm 5.7,
  the standard Selberg upper bound) are inherited without re-proof. Both appear in Dunn's refereed paper.
- Non-subsumption: I found no subsuming result within the claim package and the cited sources. Whether a stronger GRH bound
  exists elsewhere is NOVELTY's question.

confirmed_scope: Assuming GRH for Dirichlet L-functions (including RH), Brun's constant satisfies B < 2.156967, by Dunn's
(arXiv:2504.15658) sieve framework with Grenie-Molteni Cor. 1.2 applied per modulus q <= z^2 and a proved V(z) lower bound,
evaluated in arb ball arithmetic (claim/code/replay.py, sup 2.1569669355 at 128 and 256 bits), which meets bank partial win p1
(strictly below Dunn's 2.1594) and the PREREG.v2 bar (U <= R - 1e-4, R = 2.1593210324) but is conditional and not the main win.
pass: true
