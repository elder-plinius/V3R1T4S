# How We Found It

*Contributor text, unverified.*

## Asymptotic Mechanism & Traps Avoided

On Cai et al.'s asymmetric matrix `A = [[3,0,-3],[0,3,-4],[0,0,1]]`, the two players' cumulative regrets desynchronize: the column regret scale `S_y` grows unboundedly (`~ 0.001815 * t`) while row regrets `R_x(0), R_x(2)` contract at `O(1 / S_y)` and `x^t` locks onto pure row `(0, 0, 1)` during two phases of a drift-coupled period-6 cycle. Standard interval arithmetic wraps within 45 steps, and fixed-frame Lohner enclosures lose contraction as `S_y -> infinity`.

## What Worked

We combined (1) a 12-symbol Unit-L Lohner affine reachability engine (`t = 0..13203`, `48` Lean chunk modules) that bridges the chaotic transient from exact `(R = 0, uniform)` initialization into the asymptotic regime `S_y >= 24`, and (2) a 6D desingularized Poincare return map in `eps = 1 / S_y in (0, 1/24]` using 15-symbol Chebyshev `T_2, T_3` correlation-preserving affine arithmetic around a degree-15 Chebyshev slow-manifold center curve with a degree-9 Unit-LDU moving Floquet frame across `256` slabs (`64` Lean chunk modules), proving strict tube forward-invariance and `DualGap >= 1/20` at all six phases for all `t >= 13203`.
