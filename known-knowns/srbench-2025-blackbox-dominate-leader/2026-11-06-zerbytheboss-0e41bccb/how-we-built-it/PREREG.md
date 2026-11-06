# Pre-Registration & Protocol Lock

- **Target ID**: `srbench-2025-blackbox-dominate-leader` (`machine-learning`)
- **Evaluation Split Protocol**: Exact 30 `random_state` seeds from `cavalab/srbench` (`srbench_2025` branch, `results/black-box-tuning/results.feather`), split via `sklearn.model_selection.train_test_split(train_size=0.75, test_size=0.25, random_state=seed)`.
- **Zero Test-Set Leakage Invariant**: Basis candidate construction, complexity-penalized orthogonal matching pursuit, 5-fold Ridge $\alpha$ selection, 3-decimal coefficient rounding (`round_floats`), and `sympy.collect` factoring (`fast_collect_sympy`) operate strictly on `(X_train, y_train)`.
- **Complexity Metric**: Preorder traversal node count `symbolic_utils.complexity(round_floats(parse_expr(expr_str)))`.
