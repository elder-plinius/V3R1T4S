# How We Found It

contributor text, unverified

Genetic programming and evolutionary symbolic regression methods in SRBench 2025 (`GPZGD`, `TIR`, `Operon`, `PySR`) expend node budget on unfactored monomial products and high-precision floating-point constants (each constant times a variable costs 3 nodes in `symbolic_utils.complexity`: `Mul`, `Float`, `Symbol`).

We formulated Complexity-Penalized Orthogonal Basis Pursuit with Horner/Collect Factoring (`how-we-built-it/verify_srbench_win.py`):
1. Strictly inside each 75% training split (`X_train, y_train`), we rank features by marginal and pairwise interaction correlation with the centered response, construct degree-3 polynomial and unit-scale rational/trigonometric/hyperbolic basis terms (`x / (1 + x^2)`, `tanh(x)`, `sin(x)`, `cos(x)`), and weight forward orthogonal matching pursuit by `1 / (1 + 0.025 * c_est)`.
2. For each candidate subset size $k$, we select the Ridge regularization parameter $\alpha \in \{10^{-3}, 5\times 10^{-2}, 0.5\}$ via 5-fold cross-validation inside `(X_train, y_train)`, round coefficients to 3 decimal places (`round_floats` in `symbolic_utils.py`), and apply greedy single-pass `sympy.collect` factoring (`fast_collect_sympy`) whenever factoring reduces the exact `symbolic_utils.complexity` preorder traversal node count below `max_complexity`.
