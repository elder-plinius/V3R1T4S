# How We Found It

*Contributor text, unverified.*

## Brief & Traps Avoided

Upstream `APAP/Integer.lean` had two major traps: (1) `C` was omitted from `C * N`, making the literal statement false at `N = 2, A = {0, 1}`, and (2) `APAP/Prereqs/DummyPositivity.lean` registers sorried `@[positivity]` extensions imported by `Convolution.Order`, `Physics.DRC`, and `FiniteField`, silently tainting `#print axioms` with `sorryAx`.

## What Worked

We built an independent, `DummyPositivity`-free 6-module Bohr-set hierarchy (`Regular.lean`, `BohrBasic.lean`, `BohrFourier.lean`, `BohrStep.lean`, `BohrIter.lean`, `Integer.lean`): proving `BohrSet.regularity` via `9^d` angular buckets and multiplicity-`<= 2` open subcovers, constructing `twoBohr` (`2 * B` in `ZMod q`), proving positive-definite Bohr measure lifting and Bohr `L^infty` almost-periodicity, proving clean-room Bohr DRC/sifting and `curlog_mul_add` width control (`O(curlog alpha ^ 12)` total log-size loss across `O(curlog alpha)` density-increment steps), and transferring `ZMod p` (`2N < p <= 4N`) to `Nat` via Bertrand's postulate.
