# Criterion skeptic verdict: robust-forecast-aggregation-bounds, first cell (unknown state values), lower-bound side

Run 2026-10-14-1717. Evidence used: only the claim package (claim/claim.md, claim/mixture.json, claim/lb_check.py,
claim/independent_recheck.py, claim/lb_check_output.log, claim/independent_recheck_output.log, claim/sha256.txt,
claim/REPRODUCE.md), plus one plain fetch each of https://arxiv.org/abs/2604.24517 and https://arxiv.org/pdf/2604.24517.

## The clause under test (verbatim from claim/claim.md, section "Success criterion")

> First cell: the unknown-state-values variant (bounds 31/1326 ≈ 0.023379 and 0.025512): an explicit aggregator with
> an interval-certified worst-case regret below 0.025512, or an explicit information structure certifying more than 31/1326.

The shape requirement is:

> bound (an explicit aggregator or information structure with the regret definition copied from the source; the worst
> case certified with interval or exact arithmetic over the full reduced parameter domain).

The claim targets only the second alternative of the first cell: "an explicit information structure certifying more than 31/1326".

## Sources and integrity

- Abstract page: HTTP 200 (2026-10-15 03:17 UTC), sha256 523d3c019876a3a9d14ed263520ff94b40902befaea19f9cd47bca77ae45b849.
  This is identical to the hash recorded in claim/claim.md. Submission history: v1 27 Apr 2026, v2 23 May 2026 (latest).
- PDF (v2): HTTP 200, 711486 bytes, sha256 1a5836aeae0fbac9603e3e9da59c802c296d9988c66e788d0eed810cc9ec5481.
  - Read in full: Section 2 (model, L(f | Θ, π), Reg_Π); Lemma 2.1 and its proof (Appendix A); Section 3
    (Π_CI, Definition 3.1, Theorem 3.2, Lemma 3.3, Theorem 3.4, Table 3, proof of Theorem 3.4).
  - The rest of the text was searched for any other lower-bound statement.
- `shasum -a 256 -c claim/sha256.txt`: mixture.json OK, lb_check.py OK, independent_recheck.py OK.

## Check 1. Is a two-environment mixture an "explicit information structure" for this clause? Result: yes, a legitimate certifying object

- **The paper's own bar is certified by exactly this kind of object.**
  - The proof of Theorem 3.4 reads: "We construct an adversary's mixed strategy over two conditionally independent
    information structures π^A, π^B. The adversary draws π^A and π^B uniformly. By Yao's principle, ...
    Reg_ΠCI[f] = sup_{Θ,π∈ΠCI} L(f | Θ, π) ≥ E_{(Θ^I,π^I)}[ L(f | Θ^I, π^I ∘ π^I) ]".
  - Table 3 is captioned "The two symmetric adversarial information structures". Its two state spaces differ:
    {0, 5/6} and {1/6, 1}.
  - So 31/1326 is not certified by a single structure.
- **A single information structure cannot certify any positive lower bound in this model.**
  - For a fixed (Θ, π) in Π_CI, f^Bayes is a function of the reports (equation (1) of the paper).
  - So the aggregator f := f^Bayes has L = 0 on that structure, by Lemma 2.1.
  - Read as "one structure", the clause could not be met by anyone, not even by the 31/1326 it names as the bar.
- **Conclusion.** The only reading that can be met is "an explicit adversarial construction" of the paper's kind. The
  second cell's wording ("an explicit finite mixture of structures") is looser drafting. It does not make the first
  cell's requirement stricter.
- **The claim's object matches that form.** claim/mixture.json has:
  - two environments of weight 1/2 each;
  - two identical CI experts with binary signals;
  - one revealing signal per environment;
  - mirror symmetry between the two environments;
  - every number given as an exact rational.

## Check 2. Definitions, line by line. Result: they match; no stretched definition found

| Item | arXiv:2604.24517v2 | claim/mixture.json | Match |
|---|---|---|---|
| State space | binary Θ = {θ1, θ2}, θi in [0,1], θ1 ≤ θ2; outcome ω ~ Bern(θ) | A: {0, 33307/40000}; B: {6693/40000, 1} | yes |
| State values unknown to the aggregator | Reg_Π[f] = sup over Θ ⊂ [0,1]^2 and π in Π | Θ differs between the environments, as in Table 3 | yes |
| Prior | λi in [0,1]; part of π in Δ(Θ × S) | A: (415554, 417121)/832675, B mirrored; prior means 417121/10^6 and 582879/10^6 (recomputed; equal to the json "mu") | yes (non-uniform priors are allowed) |
| Two experts, CI | π(s1,s2 \| θ) = π1(s1 \| θ) π2(s2 \| θ) | joint built as a product of per-expert likelihoods | yes |
| Signals | arbitrary S_i (Lemma 3.3: binary signals already attain the worst case) | binary | yes |
| Identical experts | not excluded; Theorem 3.4 itself uses π = π^I ∘ π^I | identical | yes |
| Reports | x_i(s_i) = Pr_π[ω = 1 \| s_i] (posterior means) | recomputed exactly: 6693/40000 and 33307/40000 in both environments (equal to the json "reports") | yes |
| Aggregator | deterministic f : [0,1]^2 → [0,1] of the reports only | infimum over all real-valued functions on the 4 report pairs (a superset) | yes |
| Loss | squared | squared | yes |
| Regret | L(f \| Θ, π) = E[ℓ(f(x(s)), ω) − ℓ(f^Bayes(x(s)), ω)], ω ~ Bern(θ). f^Bayes = Pr_π[ω = 1 \| s] is the forecast of an omniscient aggregator that knows Θ, λ, π and sees the signals | claim/lb_check.py (literal route) and my own computation evaluate exactly this, per environment | yes |
| Worst case | sup over Θ and π in Π_CI | both environments are in Π_CI; sup ≥ D-average (Yao) | yes |

Hidden quantifiers:

- **"For any aggregation function f".** The paper's aggregators are deterministic. The certificate covers every
  function: no measurability, symmetry or range condition is needed, because only 4 report pairs carry probability.
- **Randomised aggregators are covered too.** By Lemma 2.1 and convexity, E_r[(f_r − f^Bayes)^2] ≥ (E_r f_r − f^Bayes)^2.
  So a randomised rule does no better than its pointwise mean, which is a deterministic rule. Equivalently, in Yao's
  inequality the expectation over the rule's internal randomness can be swapped with E_D.
- **Knowing the mixture.** Letting the aggregator know D only strengthens the bound, because the infimum over f is taken
  after D is fixed.
- **No degenerate case is exploited.** In both environments θ1 < θ2 and the prior has full support. All four report
  pairs have positive probability in both environments.
- **Cell identity.** Neither environment has state space {0,1}, so this is the unknown-state cell. As claim/claim.md says,
  nothing is claimed for the known-{0,1} cell or for an upper bound.

## Check 3. Direction and size of the margin. Result: strictly greater, in exact arithmetic; the 1e-5 remark does not apply

- **The numbers (my exact computation, output below).**
  - LB = 1652448303171916717080006468042849/70681471350112364987160770000000000 ≈ 0.023378804538274.
  - The bar is 31/1326 ≈ 0.023378582202112, so LB > 31/1326.
  - Margin = 612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.223361628e-07, which is positive
    (relative margin 9.51e-06).
- **Why the tolerance remark does not apply.**
  - The charter's remark ("every published upper bound is a floating-point maximisation, so a claimed improvement
    smaller than about 1e-5 is inside their tolerance") concerns published upper bounds such as 0.025512 and 0.022599.
  - The bar here is a lower bound, the exact rational 31/1326. It is proved in closed form, and my control below
    reproduces it exactly.
  - The new LB is also an exact rational. It comes from an exact minimisation in closed form: a convex quadratic in f
    at each of the 4 report pairs. No search, rounding or tolerance is involved.
  - When an exact rational is compared with an exact rational, any positive margin is a true strict inequality. The
    clause sets no minimum margin.
- **Shape line.** For a lower bound, the "worst case" to certify is the infimum over aggregators. That infimum is solved
  exactly over the whole aggregator domain, so the requirement for exact arithmetic over the full domain is met.
- **Size, stated plainly.** At the six-decimal precision of the paper's Table 1, both values print as 0.023379. The gain
  closes about 0.01% of the gap to the upper bound 0.025512.

## Check 4. Null models. Result: none needed; calibration and negative controls pass

This is a deterministic exact certificate: there is no sampling, no search statistic and no p-value, so no null model is
needed. The relevant checks are calibration and negative controls:

- (a) My implementation reproduces, on the paper's Table 3 mixture, every intermediate value printed in the proof of
  Theorem 3.4:
  - f^Bayes = 5/102, 5/6, 1/6, 97/102;
  - report-pair probabilities 17/32, 9/32, 3/32;
  - f* = 7/78, 71/78, 1/2;
  - and exactly 31/1326.
- (b) claim/lb_check.py on the same Table 3 mixture returns NO_IMPROVEMENT (exit 1, exactly 31/1326).

So the evaluation has no upward bias, and the margin is not an artefact of a definition mismatch.

## Check 5. Subsumption by the paper itself. Result: not subsumed, with one stray number to flag

- **What the paper states for this cell.**
  - Theorem 3.4, Table 1, Section 1.1 ("31/1326 ≈ 0.0234") and the Figure 1 caption ("theoretical lower bound of
    0.023379") all give 31/1326 as the lower bound.
  - The paper has no conclusion or open-problems section. It nowhere says its construction can be optimised further,
    and it states no optimised value.
  - Its other lower bounds are 0.022542: the bound inherited from the known-{0,1} setting, and Theorem 5.1 for the
    known-marginals setting. Both are smaller.
- **A stray number.**
  - The opening sentence of Section 3.2 reads: "we then establish a regret lower bound of 0.02344 for our prior-agnostic
    robust forecasting problem". It appears in all three text extractions.
  - 0.02344 is larger than LB (my check prints "LB > 0.02344 ? False").
  - Nothing in the paper certifies it:
    - the theorem this sentence introduces proves 31/1326 ≈ 0.023379;
    - Figure 1's caption, in the same section, says 0.023379;
    - the paper's own construction family cannot reach it (its float optimum is 0.0233788045).
  - I read it as a typo (probably for 0.0234), not a stated result, so it does not subsume the claim.
  - claim/claim.md does not mention it and should, so that no reader takes the published bound to be 0.02344.
- **What kind of win this is (context only; floating point, not part of the certificate).**
  - The object belongs to the paper's own two-parameter mirrored family (low report r, prior mean μ). It uses
    (r, μ) = (0.167325, 0.417121) instead of the paper's (1/6, 5/12).
  - A float search over that family finds its optimum 0.023378804538678 at r ≈ 0.1673243, μ ≈ 0.4171191. The claim's
    object is within 4.0e-13 of that optimum.
  - So this is a re-tuning of the published construction's parameters: genuine and strict, but tiny.
- **Not checked (outside my permitted evidence).** I did not check papers citing arXiv:2604.24517, or its v1.
  claim/claim.md records only the abstract-page status check, not the charter's "papers citing it" check. My
  non-subsumption finding is therefore limited to arXiv:2604.24517v2.

## My own exact computation (real output)

Method:

- Written from the definitions in Section 2. Python 3 standard library (`fractions`), run isolated with `python3 -I`,
  independent of the package scripts.
- For each environment it builds:
  - the joint distribution P(θ_j, s1, s2) = λ_j π1(s1 | θ_j) π2(s2 | θ_j);
  - the reports Pr[ω = 1 | s_i];
  - f^Bayes = Pr[ω = 1 | s1, s2].
- For each report pair x it adds up the literal objective
  Σ_I w_I Σ P_I(θ_j, s) Σ_ω Bern(θ_j)(ω) [(c − ω)^2 − (f^Bayes − ω)^2] = A c^2 − 2 B c + C,
  then minimises exactly over all real c: the minimum is C − B^2/A, at c* = B/A.
- As a cross-check it also evaluates the variance form of Lemma 2.1.
- The paper's Table 3 mixture is run first, as a control.

```
[paper:env0] theta=0,5/6  prior=1/2,1/2  signals/expert=[2, 2]  identical experts=True  well-formed member of Pi_CI (binary state, theta in [0,1]): True
[paper:env1] theta=1/6,1  prior=1/2,1/2  signals/expert=[2, 2]  identical experts=True  well-formed member of Pi_CI (binary state, theta in [0,1]): True
[paperA] reports expert1=[Fraction(1, 6), Fraction(5, 6)] expert2=[Fraction(1, 6), Fraction(5, 6)]  prior mean mu=5/12
   paperA: fBayes by report pair = {(Fraction(1, 6), Fraction(1, 6)): Fraction(5, 102), (Fraction(1, 6), Fraction(5, 6)): Fraction(5, 6), (Fraction(5, 6), Fraction(1, 6)): Fraction(5, 6), (Fraction(5, 6), Fraction(5, 6)): Fraction(5, 6)}
   paperA: Pr[report pair]       = {(Fraction(1, 6), Fraction(1, 6)): Fraction(17, 32), (Fraction(1, 6), Fraction(5, 6)): Fraction(3, 32), (Fraction(5, 6), Fraction(1, 6)): Fraction(3, 32), (Fraction(5, 6), Fraction(5, 6)): Fraction(9, 32)}
[paperB] reports expert1=[Fraction(1, 6), Fraction(5, 6)] expert2=[Fraction(1, 6), Fraction(5, 6)]  prior mean mu=7/12
   paperB: fBayes by report pair = {(Fraction(1, 6), Fraction(1, 6)): Fraction(1, 6), (Fraction(1, 6), Fraction(5, 6)): Fraction(1, 6), (Fraction(5, 6), Fraction(1, 6)): Fraction(1, 6), (Fraction(5, 6), Fraction(5, 6)): Fraction(97, 102)}
   paperB: Pr[report pair]       = {(Fraction(1, 6), Fraction(1, 6)): Fraction(9, 32), (Fraction(1, 6), Fraction(5, 6)): Fraction(3, 32), (Fraction(5, 6), Fraction(1, 6)): Fraction(3, 32), (Fraction(5, 6), Fraction(5, 6)): Fraction(17, 32)}
[paper:env0] reports expert1=[Fraction(1, 6), Fraction(5, 6)] expert2=[Fraction(1, 6), Fraction(5, 6)]  prior mean mu=5/12
[paper:env1] reports expert1=[Fraction(1, 6), Fraction(5, 6)] expert2=[Fraction(1, 6), Fraction(5, 6)]  prior mean mu=7/12
CONTROL paper Table 3: f* = {(Fraction(1, 6), Fraction(1, 6)): Fraction(7, 78), (Fraction(1, 6), Fraction(5, 6)): Fraction(1, 2), (Fraction(5, 6), Fraction(1, 6)): Fraction(1, 2), (Fraction(5, 6), Fraction(5, 6)): Fraction(71, 78)}
CONTROL paper Table 3: LB literal = 31/1326  LB Lemma2.1 = 31/1326  equals 31/1326: True

weights: ['1/2', '1/2'] sum to 1: True
[claim:env0] theta=0,33307/40000  prior=415554/832675,417121/832675  signals/expert=[2, 2]  identical experts=True  well-formed member of Pi_CI (binary state, theta in [0,1]): True
[claim:env1] theta=6693/40000,1  prior=417121/832675,415554/832675  signals/expert=[2, 2]  identical experts=True  well-formed member of Pi_CI (binary state, theta in [0,1]): True
[claim:env0] reports expert1=[Fraction(6693, 40000), Fraction(33307, 40000)] expert2=[Fraction(6693, 40000), Fraction(33307, 40000)]  prior mean mu=417121/1000000  (json mu matches: True)  (json reports match: True)
[claim:env1] reports expert1=[Fraction(6693, 40000), Fraction(33307, 40000)] expert2=[Fraction(6693, 40000), Fraction(33307, 40000)]  prior mean mu=582879/1000000  (json mu matches: True)  (json reports match: True)
claim: distinct report pairs: 4
claim: f* = {(Fraction(6693, 40000), Fraction(6693, 40000)): 0.09023976321849553, (Fraction(6693, 40000), Fraction(33307, 40000)): 0.5, (Fraction(33307, 40000), Fraction(6693, 40000)): 0.5, (Fraction(33307, 40000), Fraction(33307, 40000)): 0.9097602367815044}
claim: LB literal  = 1652448303171916717080006468042849/70681471350112364987160770000000000
claim: LB Lemma2.1 = 1652448303171916717080006468042849/70681471350112364987160770000000000
claim: routes agree: True
claim: LB equals stated value: True
claim: LB float = 0.023378804538274
bar 31/1326 float = 0.023378582202112
claim: LB > 31/1326 strictly: True
margin exact = 612886837595654297197253671111/2756577382654382234499270030000000000
margin float = 2.223361628e-07 ; relative margin = 9.510250e-06
LB vs stray text number 0.02344 (Sec 3.2 sentence): LB > 0.02344 ? False
```

Package checkers re-run with `python3 -I` (Python 3.9.6). Their outputs are identical to claim/lb_check_output.log and
claim/independent_recheck_output.log. The last run is the negative control on a JSON transcription of Table 3:
- π^A: θ = {0, 5/6}, λ = (1/2, 1/2), Pr[s_L | θ] = (1, 1/4).
- π^B: θ = {1/6, 1}, λ = (1/2, 1/2), Pr[s_L | θ] = (3/4, 0).
- Weights 1/2 each.

```
== lb_check.py on mixture.json
environments: 2
distinct report pairs: 4
LB_variance_form: 1652448303171916717080006468042849/70681471350112364987160770000000000
LB_literal_definition: 1652448303171916717080006468042849/70681471350112364987160770000000000
LB_float: 0.023378804538
bar: 31/1326 (0.023378582202)
two_computations_agree: yes
LB_strictly_greater_than_bar: yes
margin: 612886837595654297197253671111/2756577382654382234499270030000000000 (2.223e-07)
verdict: LOWER_BOUND_BEATS_BAR
exit=0
== independent_recheck.py on mixture.json
independent LB: 1652448303171916717080006468042849/70681471350112364987160770000000000
float: 0.023378804538274
bar 31/1326 = 0.023378582202112
strictly greater than bar: yes
margin: 2.223362e-07
exit=0
== lb_check.py on paper Table 3 mixture (negative control)
environments: 2
distinct report pairs: 4
LB_variance_form: 31/1326
LB_literal_definition: 31/1326
LB_float: 0.023378582202
bar: 31/1326 (0.023378582202)
two_computations_agree: yes
LB_strictly_greater_than_bar: no
verdict: NO_IMPROVEMENT
exit=1
```

Floating-point context only, not part of the certificate: the paper's mirrored family, Table 3 shape, parametrised by
(r, μ):

```
paper (1/6, 5/12): 0.0233785822021116  31/1326 = 0.023378582202111614
claim (0.167325, 0.417121): 0.023378804538274366
family optimum (float): LB=0.023378804538678 at r=0.167324326 mu=0.417119125
claim LB minus family optimum: -4.036e-13
```

## Verdict

The result literally meets one enumerated success route of the criterion: the first cell's lower-bound alternative,
"an explicit information structure certifying more than 31/1326".

- The certifying object is an explicit two-environment adversary mixture. It is of the same kind, and from the same
  family, as the mixture that certifies the bar itself.
- The definitions match the source line by line.
- The strict inequality holds in exact arithmetic.
- It does not meet, and does not claim, the first cell's upper-bound alternative or either alternative of the second cell.

Caveats:

- The improvement is 2.2e-7, obtained by re-tuning the parameters of Theorem 3.4's construction.
- The unsupported "0.02344" in Section 3.2 should be acknowledged in the claim.
- This skeptic did not check papers citing arXiv:2604.24517.

confirmed_scope: In the model of Section 2 of arXiv:2604.24517v2 restricted to the class Pi_CI (two experts whose signals are conditionally independent given a binary state whose values in [0,1] are unknown to the aggregator, squared loss, additive regret against the omniscient aggregator), the uniform mixture of the two explicit rational environments in claim/mixture.json certifies through Yao's principle, as in the proof of that paper's Theorem 3.4, that every aggregation function f has worst-case regret at least 1652448303171916717080006468042849/70681471350112364987160770000000000 ≈ 0.0233788045, which exceeds that paper's lower bound 31/1326 by exactly 612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.22e-7.
context: subagent
pass: true
