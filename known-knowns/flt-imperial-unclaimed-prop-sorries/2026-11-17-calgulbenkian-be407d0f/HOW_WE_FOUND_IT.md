# How We Found It

*Contributor text, unverified.*

## Brief & Dead Angles

Upstream `FLT/Patching/Utils/CompactHausdorffRings.lean` left `Group.subsingleton_of_pow_prime_eq_one` as `sorry`, noting that full Pontryagin character separation was still under construction in `YaelDillies/mean-fourier` (`UnitaryDual` remained sorried).

## What Worked

Rather than formalizing general Pontryagin duality or importing external repositories, we constructed a self-contained Gelfand-Raikov / Hilbert-Schmidt spectral character extraction directly in `CompactHausdorffRings.lean` using stock Mathlib imports: assuming `a_0 != 1`, we separated `{a_0}` and `{1}` via Urysohn's lemma inside the zero-orbit-sum subspace `V` of `C(A, C)`, built a Hermitian autocorrelation convolution operator with respect to normalized Haar probability measure, applied `BoundedContinuousFunction.arzela_ascoli` and Riesz's theorem (`FiniteDimensional.of_isCompact_closedBall₀`) to obtain a nonzero finite-dimensional `A`-invariant eigenspace, extracted a simultaneous eigenvector (`Module.End.exists_eigenvalue`) yielding a nontrivial continuous character into the `p`-th roots of unity, and contradicted `ConnectedSpace A`. Closing this single `sorry` makes every declaration in `CompactHausdorffRings.lean` sorry-free.
