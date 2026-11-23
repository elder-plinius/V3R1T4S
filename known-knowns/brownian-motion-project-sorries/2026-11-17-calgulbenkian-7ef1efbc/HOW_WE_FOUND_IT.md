# How We Found It

*Contributor text, unverified.*

## Brief & Dead Angles

Auditing the five eligible declarations in `RemyDegenne/brownian-motion` revealed mathematical counterexamples to two of them as stated (`Submartingale.uniformIntegrable_stoppedValue` fails on `WithTop Nat`, and `Martingale.ae_tendsto_limitProcess` fails on general Banach spaces lacking the Radon-Nikodym property). We therefore targeted `ProbabilityTheory.IsBrownianReal.reflection` in `BrownianMotion/Gaussian/IteratedLogarithm.lean`, where upstream noted `-- needs strong Markov property`.

## What Worked

Instead of building full continuous-time stopping-time strong Markov machinery, we passed to the everywhere-continuous modification `Y := hX.toIsPreBrownianReal.mk X`, partitioned discrete exceedance events on dyadic grids `{k t / 2^n}` by first-passage index, applied independent Gaussian increments (`hY.indepFun_shift`) and symmetry (`gaussianReal_map_neg`) for the upper bound, and controlled discrete inter-sample overshoot via pathwise Heine-Cantor uniform continuity on `[0, t]` and dominated convergence for the lower bound.
