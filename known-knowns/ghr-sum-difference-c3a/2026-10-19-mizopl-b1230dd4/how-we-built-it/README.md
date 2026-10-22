# How We Built It (`how-we-built-it/`)

- `PREREG.md`: Frozen pre-registration rule for `ghr-sum-difference-c3a` (`p1`).
- `author_checker_c3a_check.py`: Reconstructs the digit masks $M = \operatorname{span}_{\mathbb{N}_0}(G) \cap [0, B]$, sum supports $S = M + M$, minimal digit-sum costs $\kappa(d)$, and mod-$q$ pruned difference alphabets $\widetilde{D}_+$ from $G = \{1518, 1524, 1587, 2024, 2032, 2116\}$, verifies `cfFloorOK == True` in $2^{-128}$ fixed-point arithmetic, and certifies the GHR lower bounds in both 60-digit `mpmath.iv` Robbins-Stirling interval arithmetic and 100% pure integer-interval (`atanh` + Lean `StirlingBounds.lean`) arithmetic.
