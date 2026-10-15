# REPRODUCE skeptic verdict: robust-forecast-aggregation-bounds, unknown-state CI cell, lower-bound side (run 2026-10-14-1717)

Claim under test (claim.md): every aggregation function f has worst-case regret
Reg_{Pi_CI}[f] >= LB = 1652448303171916717080006468042849/70681471350112364987160770000000000 = 0.023378804538...,
which strictly exceeds 31/1326 (Theorem 3.4 of Chen, Peng, Tang, arXiv:2604.24517v2). The certificate is the two-environment
adversary mixture in mixture.json, used through Yao's principle.

## 0. Scope and procedure

- Inputs seen: only the claim package (claim.md, REPRODUCE.md, mixture.json, lb_check.py, independent_recheck.py,
  lb_check_output.log, independent_recheck_output.log, sha256.txt) plus the public paper, fetched once each:
  https://arxiv.org/pdf/2604.24517 (read in full, 27 pages; the PDF stamp reads "arXiv:2604.24517v2 [cs.LG] 23 May 2026")
  and https://arxiv.org/abs/2604.24517 (submission history v1 27 Apr 2026, v2 23 May 2026; latest is v2; no withdrawal notice).
- Order: (1) read claim.md; (2) quoted the definitions from the paper; (3) wrote my own checker from those definitions
  (Python 3, fractions.Fraction, standard library only) and ran it; (4) only then opened lb_check.py and independent_recheck.py
  and ran them exactly as REPRODUCE.md says, from inside the claim copy. REPRODUCE.md (with its expected outputs) was read before
  step 3. The two .log files and the two scripts were not opened until step 4.
- Interpreter: Python 3.9.6, every script run with python3 -I.

## 1. Definitions (quoted)

### 1a. From the paper (transcribed from the rendered PDF; math written in plain text)

Section 2, model: "We consider a stochastic environment where the world randomly generates a state θ from a finite state space Θ.
In this work, we focus on a binary state space, so that |Θ| = 2. Once a state is realized, it further induces a random binary
outcome, which is unobservable to all players. Specifically, for each state i ∈ [2], the binary outcome ω ∈ Ω ≜ {0, 1} is drawn
from a Bernoulli distribution with mean θ_i ∈ [0, 1]. Without loss of generality, we assume that the states are sorted in
non-decreasing order of their Bernoulli means: θ_1 ≤ θ_2. [...] We denote by λ_i ∈ [0, 1] the prior probability of the state θ_i
for i ∈ [2] and let μ be the prior mean of the state, i.e., μ ≜ E_{θ∼λ}[θ]."

Section 2, information structure: "Formally, an information structure for two experts is a tuple (S, π), where S = S_1 × S_2 is a
2-dimensional signal space and π ∈ Δ(Θ × S) is a joint distribution over states and signal profiles. [...] each expert's
forecast is simply their conditional probability that ω = 1, i.e., x_i(s_i | π) ≜ Pr_π[ω = 1 | s_i]."

Section 2, aggregator and loss: "An aggregator, who does not observe the signals or the true state, must form her own forecast
about the underlying outcome based solely on the experts' reported forecasts x(s) = (x_1(s_1), x_2(s_2)). [...] she knows only
that the state space is binary but does not know the specific values of θ_1 and θ_2, nor the prior probabilities λ_1, λ_2, nor
the information structure. More formally, the aggregator uses a deterministic aggregation function f : [0, 1]^2 → [0, 1] that is
a mapping from the two experts' forecasts (x_1, x_2) ∈ [0, 1]^2 to her own forecast." "Throughout this work, we adopt the
squared loss ℓ(x, ω) = (x − ω)^2 as our loss function."

Section 2, omniscient benchmark: "We denote by f^BAYES : [0, 1]^2 → [0, 1] such Bayesian optimal aggregation:
f^BAYES(x(s)) ≜ Pr_π[ω = 1 | s] where s = (s_1, s_2) is the full signal profile."

Section 2, regret: "Given a state space Θ ⊂ [0, 1]^2 and an information structure π ∈ Δ(Θ × S), the expected loss of the
aggregation function f is L(f | Θ, π) ≜ E_{(θ,s)∼π, ω∼Bern(θ)}[ ℓ(f(x(s)), ω) − ℓ(f^BAYES(x(s)), ω) ]."
"min_f Reg_Π[f], where Reg_Π[f] ≜ sup_{Θ⊂[0,1]^2, π∈Π} L(f | Θ, π)."

Lemma 2.1: "Given any state space Θ ⊂ [0, 1]^2 and any information structure π, we have that
L(f | Θ, π) = E_{(θ,s)∼π, ω∼Bern(θ)}[ (f(x(s)) − f^BAYES(x(s)))^2 ]." (Proof in Appendix A: f^BAYES(x(s)) = E[ω | s] = E[θ | s],
and the cross term vanishes after conditioning on s.)

Section 3, the class: "We refer to such structures as conditionally independent (CI), and denote by Π_CI the set of all CI
information structures. Formally, for a conditionally independent information structure π ∈ Δ(Θ × S) with S = S_1 × S_2, we say
π is CI if for every state θ ∈ Θ and every signal profile (s_1, s_2) ∈ S, we have π(s_1, s_2 | θ) = π_1(s_1 | θ) × π_2(s_2 | θ)".

Theorem 3.4: "For any aggregation function f, it follows that inf_f Reg_{Π_CI}[f] ≥ 31/1326 ≈ 0.023379."
Proof of Theorem 3.4 (the argument the claim reuses): "By Yao's principle, we have that Reg_{Π_CI}[f] = sup_{Θ,π∈Π_CI} L(f | Θ, π)
≥ E_{(Θ^I,π^I)}[ L(f | Θ^I, π^I ∘ π^I) ]. Therefore, we have inf_f Reg_{Π_CI}[f] ≥ inf_f E_{(Θ^I,π^I)}[ L(f | Θ^I, π^I ∘ π^I) ]."
"For a report profile x, the optimal forecast f*(x) minimizes the expected squared loss: f*(x) = (Pr_{π^A∘π^A}[x]
f^BAYES_{π^A∘π^A}(x) + Pr_{π^B∘π^B}[x] f^BAYES_{π^B∘π^B}(x)) / (Pr_{π^A∘π^A}[x] + Pr_{π^B∘π^B}[x])." and
"E_{(Θ^I,π^I)}[ L(f | Θ^I, π^I ∘ π^I) ] = Σ_{I∈{A,B}} Pr[π^I] Σ_{x∈{x_L,x_H}^2} (f*(x) − f^BAYES_{π^I∘π^I}(x))^2 · Pr_{π^I∘π^I}[x]
= 31/1326." Table 1 lists, for "Unknown state space", CI: LB 31/1326 (Theorem 3.4), UB 0.025512 (Theorem 3.2).

### 1b. From claim.md (verbatim)

"LB(D) = min over aggregators f of E_D[ L(f | environment) ], where L(f | Theta, pi) is the regret of Section 2 (equal, by
Lemma 2.1 of the paper, to E[(f(x_1, x_2) - f^Bayes(x_1, x_2))^2]); the minimiser is the D-weighted conditional mean of f^Bayes
given the report pair, and LB(D) is the D-weighted expected conditional variance of f^Bayes. For every f: sup over all CI
environments of L(f | env) >= E_D[L(f | env)] >= LB(D)."

## 2. Re-derivation of every proof step

Notation: D puts weight w_I on environment I = (Θ^I, π^I). For a signal profile s in environment I let P_I(s) = Pr_{π^I}[s],
x^I(s) = (x_1^I(s_1), x_2^I(s_2)) its report pair, and b_I(s) = Pr_{π^I}[ω = 1 | s] = f^Bayes.

(a) Lemma 2.1 (squared loss, additive regret). With b = E[ω | s]: (f − ω)^2 − (b − ω)^2 = (f − b)^2 + 2(f − b)(b − ω). Since f(x(s))
and b(s) are functions of s, E[(f − b)(b − ω)] = E[(f − b)(b − E[ω | s])] = 0. So L(f | Θ, π) = E[(f(x(s)) − b(s))^2] for every Θ, π, f.
The claim's use of it is correct. Here b = E[θ | s] because ω ~ Bern(θ) depends on s only through θ, which is the paper's model.
My checker evaluates the literal loss-difference definition (it enumerates ω) and the Lemma 2.1 form separately, and they agree exactly.

(b) Minimisation over f. Since f sees only the ordered report pair, E_D[L(f)] = Σ_r Σ_{(I,s): x^I(s)=r} m_{I,s} (f(r) − b_I(s))^2 with
m_{I,s} = w_I P_I(s). Fix r, let M(r) = Σ m_{I,s} and f*(r) = Σ m_{I,s} b_I(s) / M(r). The cross term 2(f(r) − f*(r))(M(r) f*(r) − Σ m b)
is 0, so the inner sum equals M(r)(f(r) − f*(r))^2 + Σ m (b − f*(r))^2. Hence
E_D[L(f)] = LB(D) + Σ_r M(r)(f(r) − f*(r))^2 >= LB(D), where LB(D) = Σ_r Σ m (b − f*(r))^2 = E_D[ Var(f^Bayes | report pair) ].
f*(r) is a convex combination of posteriors in [0, 1], so f* is itself an admissible deterministic aggregator, and the minimum is
attained: LB(D) = min_f E_D[L(f)]. A randomised f cannot do better (Jensen: E_ξ(F_ξ − b)^2 >= (E_ξ F_ξ − b)^2). Restricting f
(to continuous or symmetric functions, say) can only raise the minimum.

(c) Averaging (the easy direction of Yao's principle; no minimax theorem needed). If each (Θ^I, π^I) is admissible, then for every f,
Reg_{Π_CI}[f] = sup_{Θ, π∈Π_CI} L(f | Θ, π) >= max_I L(f | Θ^I, π^I) >= Σ_I w_I L(f | Θ^I, π^I) = E_D[L(f)] >= LB(D), since (w_I) is a
probability vector. Taking inf over f gives inf_f Reg_{Π_CI}[f] >= LB(D).

(d) Admissibility of the two environments in Π_CI. Each has |Θ| = 2 with values in [0, 1] (A: {0, 33307/40000}; B: {6693/40000, 1}),
sorted. Each has a prior that is a probability vector, a joint law built as prior × π_1(·|θ) × π_2(·|θ) (CI, rechecked from the joint),
and ω ~ Bern(θ) given the state. Reports are recomputed as Pr[ω = 1 | s_i], every signal has positive probability, and f^Bayes is a
well-defined function of the report pair inside each environment, as Section 2's "f^BAYES(x(s))" requires. The state values differ
between A and B; this is exactly the unknown-state-values freedom that Reg's sup over Θ grants the adversary.

(e) What the aggregator may depend on. Section 2: only the ordered pair (x_1, x_2). It does not know θ_1, θ_2, λ or π. It knows the
class Π, which is already reflected in the sup over Π_CI. The claim groups by exact ordered report pairs, which matches this. Both
environments induce exactly the same reports 6693/40000 and 33307/40000, so there are 4 distinct report pairs, not 8.
Scope remark: in the known-marginals variant (Section 5; Table 1, third row) this mixture would not be a valid certificate, because the
marginal report laws differ (Pr[x_L] = 207777/332675 in A versus 124898/332675 in B). The claim is explicitly about the first cell
(Section 3, Table 1 row "Unknown state space"), where it is valid.

## 3. My own checker (written before reading the author's code)

What it does (a separate script, standard library only, exact Fractions; run as `python3 -I <my checker> mixture.json`):
it parses every number as an exact "p/q" string; checks binary states in [0,1], sorted and distinct; checks that priors and
likelihood rows are distributions and that the two experts are identical; compares every value with the prose of claim.md.
It builds the full joint law of (state, s1, s2, ω) and rechecks CI and ω ~ Bern(θ) from that joint. It recomputes reports
x_i = Pr[ω=1 | s_i] and f^Bayes = Pr[ω=1 | s1,s2] from the joint, and checks Bayes plausibility. It groups atoms by exact ordered
report pair and computes f* and the D-weighted conditional-variance mass. It recomputes the value via the literal loss-difference
definition and the Lemma 2.1 form, and via a two-atom closed form m1·m2·(v1−v2)^2/(m1+m2). As a sanity check of the identity in 2(b)
(not the proof), it tests E_D[L(f)] = LB + Σ_r M(r)(f(r)−f*(r))^2 >= LB at 200 random rational aggregators. As a control, it first
reproduces the paper's own Table 3 mixture, every intermediate value of the proof of Theorem 3.4, and exactly 31/1326.

### 3a. Exact output of my checker (verbatim; two runs byte-identical, exit code 0)

```
=== Control: the paper's own Table 3 mixture (proof of Theorem 3.4) ===
  [ok]   paper A: joint law of (state, s1, s2, omega) sums to 1 (got 1)
  [ok]   paper A: joint law is nonnegative
  [ok]   paper A: signals independent given the state (recomputed from the joint), conditional marginals equal the stated likelihoods, omega ~ Bern(theta) given the state
  [ok]   paper A: expert 1 signal 0 has positive probability (5/8)
  [ok]   paper A: expert 1 signal 1 has positive probability (3/8)
  [ok]   paper A: expert 2 signal 0 has positive probability (5/8)
  [ok]   paper A: expert 2 signal 1 has positive probability (3/8)
  [ok]   paper A: f^Bayes is a well-defined function of the report pair
  [ok]   paper B: joint law of (state, s1, s2, omega) sums to 1 (got 1)
  [ok]   paper B: joint law is nonnegative
  [ok]   paper B: signals independent given the state (recomputed from the joint), conditional marginals equal the stated likelihoods, omega ~ Bern(theta) given the state
  [ok]   paper B: expert 1 signal 0 has positive probability (3/8)
  [ok]   paper B: expert 1 signal 1 has positive probability (5/8)
  [ok]   paper B: expert 2 signal 0 has positive probability (3/8)
  [ok]   paper B: expert 2 signal 1 has positive probability (5/8)
  [ok]   paper B: f^Bayes is a well-defined function of the report pair
  [ok]   paper: reports x_L = 1/6, x_H = 5/6 in both structures
  [ok]   paper: f^Bayes under A = 5/102 at (x_L,x_L), 5/6 otherwise
  [ok]   paper: f^Bayes under B = 97/102 at (x_H,x_H), 1/6 otherwise
  [ok]   paper: report-pair probabilities 17/32, 9/32, 3/32, 3/32 (A) and 9/32, 17/32, 3/32, 3/32 (B)
  [ok]   paper: D-weighted law of report pairs sums to 1
  [ok]   paper: literal loss-difference definition at f* equals the conditional-variance form
  [ok]   paper: Lemma 2.1 form at f* equals the conditional-variance form
  [ok]   paper: E_D[L(f)] == LB + sum_r M(r)(f(r)-f*(r))^2 >= LB at 200 random rational aggregators (sanity check of the algebraic identity, not the proof)
  [ok]   paper: minimiser f* takes values in [0,1]
  [ok]   paper: f* = 7/78, 71/78, 1/2, 1/2
  [ok]   paper: LB of Table 3 mixture == 31/1326 exactly (got 31/1326)
  [ok]   paper: two-atom closed form == 31/1326

=== The claimed mixture (mixture.json) ===
  [ok]   number of environments == 2 (got 2)
  [ok]   top-level keys: ['environments']
-- env A --
  keys: ['experts', 'mu', 'prior', 'reports', 'theta', 'weight']
  [ok]   env A: binary state space |Theta| = 2
  [ok]   env A: the two states are distinct
  [ok]   env A: state values in [0,1] (Bernoulli means)
  [ok]   env A: states sorted theta_1 <= theta_2
  [ok]   env A: prior entries in [0,1]
  [ok]   env A: prior sums to 1 (sum = 1)
  [ok]   env A: two experts
  [ok]   env A: expert 1 has one likelihood row per state
  [ok]   env A: expert 1 Pr[s | theta_1] entries in [0,1]
  [ok]   env A: expert 1 sum_s Pr[s | theta_1] = 1 (sum = 1)
  [ok]   env A: expert 1 Pr[s | theta_2] entries in [0,1]
  [ok]   env A: expert 1 sum_s Pr[s | theta_2] = 1 (sum = 1)
  [ok]   env A: expert 2 has one likelihood row per state
  [ok]   env A: expert 2 Pr[s | theta_1] entries in [0,1]
  [ok]   env A: expert 2 sum_s Pr[s | theta_1] = 1 (sum = 1)
  [ok]   env A: expert 2 Pr[s | theta_2] entries in [0,1]
  [ok]   env A: expert 2 sum_s Pr[s | theta_2] = 1 (sum = 1)
  [ok]   env A: the two experts are identical
  [ok]   env A: weight 1/2 as stated in claim.md
  [ok]   env A: states ['0', '33307/40000'] as stated in claim.md
  [ok]   env A: prior ['415554/832675', '417121/832675'] as stated in claim.md
  [ok]   env A: likelihoods as stated in claim.md
  [ok]   env A: joint law of (state, s1, s2, omega) sums to 1 (got 1)
  [ok]   env A: joint law is nonnegative
  [ok]   env A: signals independent given the state (recomputed from the joint), conditional marginals equal the stated likelihoods, omega ~ Bern(theta) given the state
  [ok]   env A: expert 1 signal 0 has positive probability (207777/332675)
  [ok]   env A: expert 1 signal 1 has positive probability (124898/332675)
  [ok]   env A: expert 2 signal 0 has positive probability (207777/332675)
  [ok]   env A: expert 2 signal 1 has positive probability (124898/332675)
  [ok]   env A: f^Bayes is a well-defined function of the report pair
  [ok]   env A: prior mean mu = 417121/1000000 (json 417121/1000000, claim.md 417121/1000000)
  [ok]   env A: recomputed reports equal the JSON reports
  [ok]   env A: recomputed reports x_L = 6693/40000, x_H = 33307/40000 (stated 6693/40000, 33307/40000)
  [ok]   env A: Bayes plausibility E[x_1] = mu
  [ok]   env A: Bayes plausibility E[x_2] = mu
  signal-profile table (s1, s2): Pr_env[s], f^Bayes = Pr[omega=1 | s1,s2], report pair
    (L,L): Pr = 979603486100241/1846555551478225 (0.530503122592785) ; f^Bayes = 9307630228473/188587473320000 (0.049354445789088) ; x = (6693/40000, 6693/40000)
    (L,H): Pr = 173689586175978/1846555551478225 (0.094061392324176) ; f^Bayes = 33307/40000 (0.832675000000000) ; x = (6693/40000, 33307/40000)
    (H,L): Pr = 173689586175978/1846555551478225 (0.094061392324176) ; f^Bayes = 33307/40000 (0.832675000000000) ; x = (33307/40000, 6693/40000)
    (H,H): Pr = 519572893026028/1846555551478225 (0.281374092758863) ; f^Bayes = 33307/40000 (0.832675000000000) ; x = (33307/40000, 33307/40000)
-- env B --
  keys: ['experts', 'mu', 'prior', 'reports', 'theta', 'weight']
  [ok]   env B: binary state space |Theta| = 2
  [ok]   env B: the two states are distinct
  [ok]   env B: state values in [0,1] (Bernoulli means)
  [ok]   env B: states sorted theta_1 <= theta_2
  [ok]   env B: prior entries in [0,1]
  [ok]   env B: prior sums to 1 (sum = 1)
  [ok]   env B: two experts
  [ok]   env B: expert 1 has one likelihood row per state
  [ok]   env B: expert 1 Pr[s | theta_1] entries in [0,1]
  [ok]   env B: expert 1 sum_s Pr[s | theta_1] = 1 (sum = 1)
  [ok]   env B: expert 1 Pr[s | theta_2] entries in [0,1]
  [ok]   env B: expert 1 sum_s Pr[s | theta_2] = 1 (sum = 1)
  [ok]   env B: expert 2 has one likelihood row per state
  [ok]   env B: expert 2 Pr[s | theta_1] entries in [0,1]
  [ok]   env B: expert 2 sum_s Pr[s | theta_1] = 1 (sum = 1)
  [ok]   env B: expert 2 Pr[s | theta_2] entries in [0,1]
  [ok]   env B: expert 2 sum_s Pr[s | theta_2] = 1 (sum = 1)
  [ok]   env B: the two experts are identical
  [ok]   env B: weight 1/2 as stated in claim.md
  [ok]   env B: states ['6693/40000', '1'] as stated in claim.md
  [ok]   env B: prior ['417121/832675', '415554/832675'] as stated in claim.md
  [ok]   env B: likelihoods as stated in claim.md
  [ok]   env B: joint law of (state, s1, s2, omega) sums to 1 (got 1)
  [ok]   env B: joint law is nonnegative
  [ok]   env B: signals independent given the state (recomputed from the joint), conditional marginals equal the stated likelihoods, omega ~ Bern(theta) given the state
  [ok]   env B: expert 1 signal 0 has positive probability (124898/332675)
  [ok]   env B: expert 1 signal 1 has positive probability (207777/332675)
  [ok]   env B: expert 2 signal 0 has positive probability (124898/332675)
  [ok]   env B: expert 2 signal 1 has positive probability (207777/332675)
  [ok]   env B: f^Bayes is a well-defined function of the report pair
  [ok]   env B: prior mean mu = 582879/1000000 (json 582879/1000000, claim.md 582879/1000000)
  [ok]   env B: recomputed reports equal the JSON reports
  [ok]   env B: recomputed reports x_L = 6693/40000, x_H = 33307/40000 (stated 6693/40000, 33307/40000)
  [ok]   env B: Bayes plausibility E[x_1] = mu
  [ok]   env B: Bayes plausibility E[x_2] = mu
  signal-profile table (s1, s2): Pr_env[s], f^Bayes = Pr[omega=1 | s1,s2], report pair
    (L,L): Pr = 519572893026028/1846555551478225 (0.281374092758863) ; f^Bayes = 6693/40000 (0.167325000000000) ; x = (6693/40000, 6693/40000)
    (L,H): Pr = 173689586175978/1846555551478225 (0.094061392324176) ; f^Bayes = 6693/40000 (0.167325000000000) ; x = (6693/40000, 33307/40000)
    (H,L): Pr = 173689586175978/1846555551478225 (0.094061392324176) ; f^Bayes = 6693/40000 (0.167325000000000) ; x = (33307/40000, 6693/40000)
    (H,H): Pr = 979603486100241/1846555551478225 (0.530503122592785) ; f^Bayes = 179279843091527/188587473320000 (0.950645554210912) ; x = (33307/40000, 33307/40000)
  [ok]   mixture weights in [0,1] and sum to 1
  [ok]   claim: D-weighted law of report pairs sums to 1
  [ok]   claim: literal loss-difference definition at f* equals the conditional-variance form
  [ok]   claim: Lemma 2.1 form at f* equals the conditional-variance form
  [ok]   claim: E_D[L(f)] == LB + sum_r M(r)(f(r)-f*(r))^2 >= LB at 200 random rational aggregators (sanity check of the algebraic identity, not the proof)
  [ok]   claim: minimiser f* takes values in [0,1]
  report pairs (distinct): 4
    x = (6693/40000, 6693/40000): D-mass = 1499176379126269/3693111102956450 (0.405938607675824) ; f*(x) = 216456514360185597/2398682206602030400 (0.090239763218496) ; D-weighted conditional-variance mass = 4714944575741249267348951052119457411/3685340751378777474476185942896250000000 (0.001279378188836)
    x = (6693/40000, 33307/40000): D-mass = 173689586175978/1846555551478225 (0.094061392324176) ; f*(x) = 1/2 (0.500000000000000) ; D-weighted conditional-variance mass = 86844793087989/8342420000000000 (0.010410024080302)
    x = (33307/40000, 6693/40000): D-mass = 173689586175978/1846555551478225 (0.094061392324176) ; f*(x) = 1/2 (0.500000000000000) ; D-weighted conditional-variance mass = 86844793087989/8342420000000000 (0.010410024080302)
    x = (33307/40000, 33307/40000): D-mass = 1499176379126269/3693111102956450 (0.405938607675824) ; f*(x) = 2182225692241844803/2398682206602030400 (0.909760236781504) ; D-weighted conditional-variance mass = 4714944575741249267348951052119457411/3685340751378777474476185942896250000000 (0.001279378188836)
  per-environment regret of f*: L(f*|A) = 1652448303171916717080006468042849/70681471350112364987160770000000000 (0.023378804538274) ; L(f*|B) = 1652448303171916717080006468042849/70681471350112364987160770000000000 (0.023378804538274)
  [ok]   claim: two-atom closed form agrees with the conditional-variance form

my LB (exact):  1652448303171916717080006468042849/70681471350112364987160770000000000
my LB (float):  0.023378804538274
claimed LB:     1652448303171916717080006468042849/70681471350112364987160770000000000
  [ok]   my LB equals the claimed LB exactly
bar 31/1326:    0.023378582202112
  [ok]   my LB strictly exceeds 31/1326
margin (exact): 612886837595654297197253671111/2756577382654382234499270030000000000
margin (float): 2.223362e-07
  [ok]   my LB is below the published upper bound 0.025512 (consistency)

FAILED CHECKS: 0
RESULT: ALL CHECKS PASSED
```

### 3b. Third, hand-derived route: closed form in the three free parameters (Fraction and 80-digit Decimal)

For the mirror-symmetric family (A: states {0, t}, prior (a, 1−a), Pr[s_L|0] = 1, Pr[s_L|t] = q; B is the image under θ → 1−θ,
s_L ↔ s_H; weights 1/2), LB = 2·m1·m2/(m1+m2)·(b_A(LL) − (1−t))^2 + 2·c·(t − 1/2)^2 with P_A(LL) = a + (1−a)q^2,
b_A(LL) = (1−a)q^2·t/P_A(LL), m1 = P_A(LL)/2, m2 = (1−a)(1−q)^2/2, c = (1−a)q(1−q). Equal reports across A and B force
q = a(1−t)/((1−a)(2t−1)). Output (verbatim):

```
constraint q == a(1-t)/((1-a)(2t-1)): True
closed form (Fraction): 1652448303171916717080006468042849/70681471350112364987160770000000000 == claimed: True
closed form (Decimal, 80 digits): 0.023378804538274368534466411008214277962195239175164297651404771504793308298677764
claimed as Decimal               : 0.023378804538274368534466411008214277962195239175164297651404771504793308298677764
|difference|: 0E-81
31/1326 as Decimal               : 0.023378582202111613876319758672699849170437405731523378582202111613876319758672700
paper point (a,t)=(1/2,5/6): 31/1326 == 31/1326: True
dLB/da at paper point ~ 1.069229e-04 ; dLB/dt ~ -8.292214e-04  (nonzero => paper point not stationary in this family)
```

The nonzero gradient shows that the paper's own point (a, t) = (1/2, 5/6) is not stationary within its own family. A small
improvement of this kind is therefore expected, and mixture.json lies in that family (the constraint holds exactly).

Contrast for the "conditional versus total variance" check (verbatim):

```
E_D[f^Bayes] = 1/2 ; total variance of f^Bayes under D = 0.159695791310 (not the claimed quantity)
```

The claimed 0.0233788 is the conditional variance given the report pair, as it must be. It is not the total variance (0.1597).

## 4. Comparison with the claimed value and the bar

- My LB (exact): 1652448303171916717080006468042849/70681471350112364987160770000000000 = 0.023378804538274...
- Claimed LB (claim.md, REPRODUCE.md, both logs): 1652448303171916717080006468042849/70681471350112364987160770000000000. EXACT MATCH.
- Bar 31/1326 = 0.023378582202112... My LB > 31/1326, margin 612886837595654297197253671111/2756577382654382234499270030000000000
  = 2.223362e-07, equal to the margin printed by lb_check.py. The claimed float 0.023378804538... and margin 2.223362e-07 also match.
- Consistency: LB < 0.025512 (published upper bound, Theorem 3.2), so there is no contradiction with the other side of the cell.
- Control: the paper's Table 3 mixture gives exactly 31/1326 with my checker, with f^Bayes = 5/102 and 97/102, report-pair
  probabilities 17/32, 9/32, 3/32, and f* = 7/78, 71/78, 1/2, all as printed in the proof of Theorem 3.4.

## 5. Property checks (all from the saved files, exact arithmetic)

| property | result |
|---|---|
| number of environments = 2, weights 1/2 and 1/2, in [0,1], sum to 1 | PASS |
| env A states {0, 33307/40000}; env B states {6693/40000, 1}; binary, distinct, in [0,1], sorted; as stated in claim.md | PASS |
| env A prior (415554/832675, 417121/832675); env B prior (417121/832675, 415554/832675); entries in [0,1]; each sums to 1; as stated | PASS |
| likelihood rows Pr[s \| θ] are distributions (entries in [0,1], each row sums to 1), every expert, every state; values as stated | PASS |
| the two experts are identical (A and B) | PASS |
| joint law of (state, s1, s2, ω) sums to 1 and is nonnegative | PASS |
| CI: Pr[s1,s2 \| θ] = Pr[s1 \| θ]·Pr[s2 \| θ], recomputed from the joint; conditional marginals equal stated likelihoods; ω ~ Bern(θ) given θ | PASS |
| every signal has positive probability (A: 207777/332675, 124898/332675; B mirrored) | PASS |
| induced reports x_L = 6693/40000, x_H = 33307/40000 for both experts in both environments; equal to the JSON "reports" fields | PASS |
| prior means μ_A = 417121/1000000 and μ_B = 582879/1000000 (recomputed = JSON "mu" = claim.md); Bayes plausibility E[x_i] = μ | PASS |
| f^Bayes is a well-defined function of the report pair inside each environment | PASS |
| distinct report pairs = 4 (report values coincide exactly across A and B) | PASS |
| minimiser f* in [0,1]; literal definition = Lemma 2.1 form = variance form = two-atom closed form = parametric closed form | PASS |
| LB equals the claimed fraction exactly; LB > 31/1326 | PASS |
| mixture.json: ASCII only, no duplicate JSON keys, every number an exact rational string | PASS |
| sha256 of mixture.json, lb_check.py, independent_recheck.py equal sha256.txt and claim.md/REPRODUCE.md | PASS |
| determinism: my checker, lb_check.py and independent_recheck.py each run twice, byte-identical | PASS |
| every file listed in claim.md "Files" is present | PASS |

## 6. The author's scripts, run exactly as REPRODUCE.md says (from inside the claim copy)

`python3 -I lb_check.py mixture.json` (exit code 0), output verbatim:

```
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
```

`python3 -I independent_recheck.py mixture.json` (exit code 0), output verbatim:

```
independent LB: 1652448303171916717080006468042849/70681471350112364987160770000000000
float: 0.023378804538274
bar 31/1326 = 0.023378582202112
strictly greater than bar: yes
margin: 2.223362e-07
```

- diff against the expected blocks in REPRODUCE.md: IDENTICAL (both scripts). Against lb_check_output.log and
  independent_recheck_output.log: IDENTICAL. Two runs of each: byte-identical.
- Negative control claimed in REPRODUCE.md: on the paper's Table 3 mixture, lb_check.py prints LB_variance_form 31/1326 and
  LB_literal_definition 31/1326, "LB_strictly_greater_than_bar: no", "verdict: NO_IMPROVEMENT", exit code 1, as stated.
  independent_recheck.py prints "independent LB: 31/1326". A mixture with weights 1/2 and 1/3 is rejected by both (exit 1).
- Code review (after my checker): lb_check.py computes reports E[θ | s_i], f^Bayes = E[θ | s1,s2] from the CI product, the variance
  form Σ(M2 − M1^2/M0) per report pair, and the literal form using E[(a−ω)^2] = a^2 − 2aθ + θ. All correct.
  independent_recheck.py uses p_i = Pr[θ_2 | s_i], x_i = θ_1 + Δ·p_i, Pr[s1,s2] = P1·P2·((1−p1)(1−p2)/λ1 + p1p2/λ2) and
  p12 = (p1p2/λ2)/z. I checked this algebra; it is correct. Neither script reads the file system beyond the JSON argument, uses
  randomness, or uses floating point in the certified value.

## 7. sha256 (shasum -a 256, from inside the claim copy)

```
c8c3d23d5e791ec2c2d51a0ce5555fa7af7e9712d0c0ad0acd31f7bdbdc0b971  mixture.json
90804c5ffff5d8b266b2fc0ac81ca46dec011fc3b03f060f4cd13598d3c57bf9  lb_check.py
68c57158c8dce06e8f3fe756d49fb46f41a6f6343ce28293673ba6e4ee643762  independent_recheck.py
```
`shasum -a 256 -c sha256.txt`: mixture.json: OK, lb_check.py: OK, independent_recheck.py: OK (exit 0). These also equal the hashes
quoted in claim.md (mixture.json) and REPRODUCE.md (all three).

## 8. Error hunt

- Sign: regret = E[ℓ(f, ω) − ℓ(f^Bayes, ω)] >= 0. The literal enumeration over ω reproduces the positive variance value; no sign error.
- Normalisation: the D-weighted masses of report pairs sum to exactly 1; the weights 1/2 enter once; the value is
  Σ_r P_D(r)·Var(f^Bayes | r), not unweighted and not double-counted. Both environments have L(f* | env) = LB (mirror symmetry).
- Conditional versus total variance: conditional given the ordered report pair (total variance would be 0.1597).
- Class admissibility: binary state space, CI signals, state values in [0,1] that differ across environments (allowed, because the
  sup in Reg_{Π_CI} runs over Θ), ω ~ Bern(θ), reports equal to posteriors. All verified in exact arithmetic.
- Aggregator information: only (x_1, x_2), as in Section 2. The ordered-pair grouping is correct, and randomised or restricted f
  cannot beat LB.
- Exhaustive-search rule: there is no search to audit. The inner minimisation over all f is solved in closed form (2(b)), and the
  outer sup is bounded below by averaging over two explicit environments. My random-f test is labelled as a sanity check only.

## 9. Discrepancies and notes (none affects the certified value)

1. The paper's Section 3.2 opening sentence says "we then establish a regret lower bound of 0.02344", but Theorem 3.4, its proof,
   Table 1 and Figure 1 all give 31/1326 ≈ 0.023379, and the proof computes exactly 31/1326, which I reproduced. The claim beats the
   proven 31/1326, which is the charter's bar. It does not exceed the figure 0.02344 in that sentence, which appears to be a typo in the
   paper. The panel should be aware of this.
2. The margin, 2.2e-07, is below the 6-decimal precision at which the paper reports 31/1326 (both values round to 0.023379). It is
   nevertheless a strict inequality between exact rationals. The charter's 1e-5 tolerance remark concerns float-maximised upper
   bounds, not this exactly computed lower bound.
3. The docstring of independent_recheck.py refers to lb_check.py by a relative path that points outside the claim package. This is cosmetic:
   lb_check.py is shipped in the package and its hash is verified.
4. independent_recheck.py exits 0 whatever the comparison result (REPRODUCE.md claims no exit code for it, so this is not a mismatch).
   Its Δ = 0 branch and its divisions by λ_1, λ_2 would mishandle degenerate environments; that is irrelevant here (Δ > 0, λ > 0).
5. lb_check.py does not compare the informational "reports" and "mu" fields of mixture.json with recomputed values. It correctly groups
   by recomputed reports. My checker confirms that those fields agree exactly.
6. claim.md cites the regret definition by reference rather than verbatim. Section 1a above quotes it, and it matches what both
   scripts and my checker implement.

## Verdict

Every item was confirmed independently in exact rational arithmetic, with no mismatch, no missing object and no non-determinism.
Those items are: the definitions, all the stated properties of mixture.json, the validity of the reduction (Lemma 2.1, pointwise
minimisation, averaging), admissibility in Π_CI, and the value. The value LB(D) = 1652448303171916717080006468042849/70681471350112364987160770000000000
is a valid lower bound on inf_f Reg_{Π_CI}[f] in the unknown-state-values CI cell, and it strictly exceeds 31/1326, by
612886837595654297197253671111/2756577382654382234499270030000000000 ≈ 2.223362e-07. The author's two scripts reproduce REPRODUCE.md
byte-for-byte and the hashes match.

context: subagent
pass: true
