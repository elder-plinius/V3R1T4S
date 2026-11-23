# How We Built It

Constructed an 820-line private section `SubsingletonAux` in `FLT/Patching/Utils/CompactHausdorffRings.lean` proving `Group.subsingleton_of_pow_prime_eq_one` (and `@[to_additive]` `AddGroup.subsingleton_of_nsmul_prime_eq_zero`) against `ImperialCollegeLondon/FLT` commit `a3210204ad8876e851e32f73dd97d882bf1ccd0a` (`leanprover/lean4:v4.35.0`) using only stock Mathlib imports (Haar probability measure, Urysohn separation, Hilbert-Schmidt autocorrelation convolution, Arzela-Ascoli compactness, and Riesz finite-dimensional eigenspaces).
