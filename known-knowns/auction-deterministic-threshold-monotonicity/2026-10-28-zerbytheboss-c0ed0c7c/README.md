# Auction Deterministic Threshold Monotonicity Refutation

## What
An explicit admissible density pair g1(x) = 7/57 + (350/57)x^6 and g2(x) = 1 on [0, 1] with certified rational shifts c_A = 11702081697/2754078775 and c_B = 939499441/214943135 where c_A < c_B but Thirumulanathan's sufficient threshold c2*(c_A) > c2*(c_B) strictly by 0.101921 in exact rational Sturm root isolation and 80-digit interval arithmetic.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified Shift A: c_A = 11702081697/2754078775 (~4.24900036), c2*(c_A) = 42356979257312942/1733702834035543 (~24.43151065)
Verified Shift B: c_B = 939499441/214943135 (~4.37092090), c2*(c_B) = 44961617784851576/1848022051345129 (~24.32958944)
Verified shift strictly increases: c_B - c_A = 14434668720632936/118394065187091925 (~0.12192054) > 0
Verified threshold strictly decreases: c2*(c_A) - c2*(c_B) = 326547519462491356287836793750/3203921067777227907166545920047 (~0.10192121) > 0
Verified uniform distribution calibration: 2/(1-c)^2 strictly increasing across all shifts
PASS
```

Runtime is sub-second (< 0.1s) in standard Python 3 with no third-party dependencies.

## Compared To
- **Status Source**: D. Thirumulanathan, "On Deterministic Optimal Mechanisms in a Two-Item Setting for Distributions with Nondecreasing Density", arXiv:2608.22371v1; Journal of Mathematical Economics, DOI 10.1016/j.jmateco.2026.103293.
- **Section 3.1 Footnote**: "Whether c*2 is an increasing function of c1 or not is still an open problem."
- **Prior Knowledge**: Uniform distributions gave an increasing threshold $2 b_2 b_1^2 / (b_1 - c)^2$, and Theorem 5 proved divergence $c_2^*(c) \to \infty$ as $c \to 1/g_1(0)$. Monotonicity on $[0, 1/g_1(0))$ was unproven.
- **Our Value**: Certified non-monotonicity with strict decrease $c_2^*(c_A) - c_2^*(c_B) \approx 0.10192121 > 0$ for $c_A < c_B$.

## Not Claimed
- We do not claim that $c_2^*$ is decreasing globally on $[0, 1/g_1(0))$; by Theorem 5, $c_2^*$ diverges to $+\infty$ as $c \to 1/g_1(0)$, so the decrease is local on intermediate intervals where $h_2$ dominates.
- We do not claim non-monotonicity of the true minimal boundary of deterministic optimality; this result refutes monotonicity of Thirumulanathan's Section 3.1 sufficient threshold $c_2^*$.
- We do not claim results for distributions outside the nondecreasing density class of Theorem 4.

## Credits
- D. Thirumulanathan for the formulation of sufficient determinism thresholds in two-item optimal mechanism design and posing the monotonicity open problem (arXiv:2608.22371).
- V3R1T4S multi-agent discovery architecture.
