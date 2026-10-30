# How We Found It — `coin-basket-random-expected-values`

_contributor text, unverified_

## The Brief and Problem Framing
Jehn's random-basket coin game (OEIS A391791 for $k=2$, A391792 for $k=3$) models a finite-horizon Markov decision process where coins $1, 2, \dots, n$ are sequentially placed into one of $k$ uniformly randomly chosen baskets to maximize the expected value of the maximum basket sum.
Because each coin is placed under complete information of the current basket contents and remaining coins, the value function satisfies Bellman's equation with backward induction:
$$V(R, s) = \frac{1}{k} \sum_{b=1}^k \max_{c \in R} V(R \setminus \{c\}, s + c \cdot e_b)$$
with boundary conditions $V(\emptyset, s) = \max_{1 \le b \le k} s_b$.

The published literature records halted at $n=22$ for $k=2$ and $n=18$ for $k=3$. Furthermore, Ruediger Jehn conjectured that for $n > 9$, the optimal first move in the 2-basket game is always coin $\lfloor (n+3)/2 \rfloor$, but this had only been verified up to $n=22$.

## What Failed
1. **Direct Float Bellman Induction**: Floating-point precision degrades rapidly over 25 backward-induction steps. The OEIS sequence requires integer terms $a(n) = k^{n-1} \max_c V(\{1..n\} \setminus \{c\}, c \cdot e_1)$. Any floating-point representation causes catastrophic rounding errors on high terms ($> 10^{11}$).
2. **Naive State Representation**: Storing arbitrary basket tuples $(s_1, s_2)$ or $(s_1, s_2, s_3)$ causes exponential state explosion. At $n=25$, the subset layer has $\binom{25}{12} = 5,200,300$ subsets; storing unrestricted tuples requires tens of gigabytes per layer.

## What Worked
1. **Scaled Integer Invariant**: Multiplying by $k^m$ where $m = |R|$ yields integer-valued scaled Bellman values:
   $$W(R, s) = k^{|R|} V(R, s) \in \mathbb{N}$$
   $$W(R, s) = \sum_{b=1}^k \max_{c \in R} W(R \setminus \{c\}, s + c \cdot e_b)$$
   This transforms every Bellman update into pure unsigned 64-bit integer additions and comparisons with zero floating-point division.
2. **Parity Difference Profiling ($k=2$)**:
   The difference $d = |s_1 - s_2|$ satisfies $d \equiv P(R) \pmod 2$, where $P(R) = \frac{n(n+1)}{2} - \sum_{c \in R} c$ is the placed coin sum. By indexing states purely by non-negative difference $d \in [0, P(R)]$ with step size 2, the number of distinct profile states is bounded by $\lfloor P(R)/2 \rfloor + 1$. Peak memory for layer 12 at $n=25$ is reduced to $3.3$ GB.
3. **Sorted Partition Normalization ($k=3$)**:
   Sorting basket sums $s_1 \ge s_2 \ge s_3 \ge 0$ with $\sum s_i = P(R)$ compresses the state space by a factor of 6.
4. **Dual Independent Compiled Implementations**:
   - Solver 1 (Rust): Multi-threaded layered DP using colexicographical subset ranking.
   - Solver 2 (C++): Multi-threaded C++20 engine using parallel layer transitions.
   Both solvers produced 100% identical outputs on all published terms and all new terms.
5. **Settling Jehn's Conjecture**:
   Evaluating turn 1 decisions for $n=10..25$ proves that coin $\lfloor (n+3)/2 \rfloor$ is the strictly unique optimal first move for every $n \in [10..25]$.
