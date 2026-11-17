# How We Found It

*Contributor text, unverified.*

## Structural Bottleneck & Normalizer Breakthrough

Under the canonical order-`5` automorphism `pi = G_{5,1}` in `GL(7, 2)`, `1,491` length-`5` orbits of planes disjoint from the fixed 3-space `F` are internally line-disjoint. Direct MILP branching on all `1,491` binary orbit variables stalls due to the `2,016`-element quotient normalizer `(GammaL(1, 16) x GL(3, 2)) / gen(pi)`, while prescribing uncoupled symmetries `(id_W, g_F)` or `(tau_W, id_F)` yields immediate `UNSAT`.

## What Worked

Prescribing a coupled diagonal involution `tau = (tau_W, tau_F)` combining the Frobenius involution `z -> z^4` on `W = F_{16}` (extending `gen(pi_W)` to dihedral `D_{10}`) with an order-`2` involution in `GL(3, 2)` on `F` collapsed the `1,491` `pi`-orbits to `339` non-clashing `D_{10}`-orbits, on which HiGHS found an exact `48`-orbit (`240`-plane) solution in under `2` seconds.
