# Preregistered Evaluation Bar (`myerson-vs-anonymous-reserve-gap`)

frozen_utc: 2026-10-28T18:18:00Z
target_id: myerson-vs-anonymous-reserve-gap
category: graphs-games-automata
null_test: not needed because deterministic interval and exact rational arithmetic evaluates closed-form expressions

## 1. Verbatim Target Bank Criteria
> An explicit instance of n >= 2 independent buyers with regular distributions, plus a certificate that a skeptic re-runs with interval or exact arithmetic, showing certified OPT/AR >= 2.1600 (higher is better). The distributions must be triangular Tri(v_i, q_i) with rational parameters (Tri(inf) allowed), or other closed-form distributions accompanied by a written regularity proof. The certificate has three parts. (a) A certified lower bound on OPT. For triangular instances sorted v_1 >= ... >= v_n this is JLTX Lemma 1: OPT = sum_i v_i q_i prod_{j<i}(1 - q_j). Otherwise use Myerson's formula with interval-certified integrals. (b) A certified upper bound on AR = sup over all reserves r >= 0 of the expected second-price revenue with anonymous reserve r. For triangular instances, JLTX Lemma 9 puts the supremum at some r = v_i, so it suffices to bound every AR(v_i) (closed-form antiderivatives or interval quadrature). For non-triangular instances, give an explicit argument covering all r. (c) The ratio of the two certified bounds is at least 2.1600. That threshold sits above JLTX's rounded 2.1596, so rounding cannot decide a claim. The certified ratio must also be strictly larger than any certified ratio published after JLTX; re-check arXiv before claiming.

## 2. Partial Wins (Verbatim)
- **p1:** The same certificate (certified OPT/AR >= 2.1600) for an instance whose distributions are quasi-regular in the sense of Feng-Jin (arXiv 2411.03583) but not all regular. This improves the upper end 0.4630 of the open quasi-regular interval AR/OPT in [0.2770, 0.4630] (Feng-Jin Result 3); that end is currently inherited from JLTX's regular instance.

## 3. Evaluation Metric & Thresholds
- Instance format: $n \ge 5$ buyers, with buyer 0 being $\text{Tri}(\infty)$ and buyers $1..n-1$ having exact rational parameters $(v_i, q_i) \in \mathbb{Q}$.
- Lower bound $\text{OPT}_{\min}$ computed via exact rational arithmetic or interval arithmetic from JLTX Lemma 1:
  $$\opt = 1 + \sum_{i=1}^{n-1} v_i q_i \prod_{j=1}^{i-1} (1 - q_j)$$
- Upper bound $\text{AR}_{\max}$ computed over all $k \in \{1, \dots, n-1\}$:
  $$\ar(v_k) = v_k \left[ 1 - F_0(v_k) (1 - q_k) \prod_{j=1}^{k-1} F_j(v_k) \right] + \int_{v_k}^{v_1} (1 - \second(x)) dx$$
  using exact rational partial fraction decomposition and interval logarithms.
- Rigorous threshold:
  $$\frac{\text{OPT}_{\min}}{\max_{k=1}^{n-1} \text{AR}_{\max}(v_k)} \ge 2.16000000$$
- Calibration controls:
  - 3-buyer instance must reproduce $v_1 \approx 1.5699, v_2 \approx 0.8399, \opt \approx 2.1361$ within $\pm 0.0001$.
  - 4-buyer printed instance must reproduce $\opt \approx 2.1596$ and $\ar(v_k) \approx 1.0000$ within $\pm 0.0001$.
