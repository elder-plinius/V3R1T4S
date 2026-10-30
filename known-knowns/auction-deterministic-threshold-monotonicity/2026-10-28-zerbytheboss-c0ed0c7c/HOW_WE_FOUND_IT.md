# How We Found It

*contributor text, unverified*

## The Brief
Thirumulanathan (arXiv:2608.22371, Section 3.1) constructed a sufficient condition for deterministic optimal mechanisms in a two-item setting, defining the threshold $c_2^*(c_1) = \max(h_1, h_2, h_3)$ and noting in a footnote: *"Whether $c_2^*$ is an increasing function of $c_1$ or not is still an open problem."*

## What Failed
- **Uniform and Low-Degree Densities**: For uniform distributions, $c_2^*(c) = 2 b_2 b_1^2 / (b_1 - c)^2$, which is strictly convex and increasing. Linear densities $g_1(x) = \frac{1}{4}(1+x)$ also exhibit strictly increasing thresholds because the derivative is small and flat.
- **Asymptotic Regime**: For $c$ close to the upper limit $1/g_1(0)$, $h_1(c) \to \infty$ and $h_3(c) \to \infty$ for all nondecreasing densities because $R(c) - c \to 0$, forcing $t \to 0$ and $h_3 \to \infty$. Thus monotonicity cannot be refuted near the right boundary.

## What Worked
- **Elasticity Truncation Mechanism**:
  The second threshold is $h_2(c) = 2 + \max_{0 \le x \le y(c)} (c + x) \frac{g_1'(x)}{g_1(x)}$.
  As shift $c$ increases, the unshifted monopoly price $y(c)$ strictly contracts because $M(y) = \frac{1 - G_1(y)}{g_1(y)} - y$ is strictly decreasing.
  By choosing a high-degree power density $g_1(x) = (\epsilon + x^d)/Z$ with $\epsilon = 1/50, d = 6, Z = 57/350$, the ratio $g_1'(x)/g_1(x) = 300 x^5 / (1 + 50 x^6)$ grows steeply towards $x = 1$.
  When $y(c)$ contracts, the upper end of the maximization interval $[0, y(c)]$ is truncated, forcing $h_2(c)$ to drop precipitously.
- **Dominance Window**:
  In the intermediate shift regime around $c \approx 4.25..4.40$, $h_2(c)$ strictly dominates both $h_1(c)$ and $h_3(c)$.
  Because $h_2$ is strictly decreasing in this window, the true maximum $c_2^*(c) = \max(h_1, h_2, h_3) = h_2(c)$ strictly decreases!
  At $c_A = 11702081697/2754078775 \approx 4.249000$, $c_2^*(c_A) = 24.43151065$.
  At $c_B = 939499441/214943135 \approx 4.370921$, $c_2^*(c_B) = 24.32958944$.
  We verified this drop across two independent exact methods: Lens 1 (Sturm root isolation over $\mathbb{Q}[x]$) and Lens 2 (80-digit `mpmath.iv` interval arithmetic), providing an ironclad refutation of monotonicity.
