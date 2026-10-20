# Null and Perturbation Control Audit (`ame-states-open-cells-huber-table`)

controls: 400
best_control: 69/72 active cuts passed (3 failed cuts; 0/400 random F_5^9 shift vectors pass all 72 active cuts)
real: 72/72 active cuts and 126/126 total 4-party cuts passed for AME(9,10) (and 462/462 total 5-party cuts passed for AME(11,10))
command: python3 claim/author_checker_ame.py
real_beats_all_controls: yes

## Summary of Controls Verified in Step `[5/5]` of `claim/author_checker_ame.py`

1. **Unshifted Coupling Control ($c = 0$):** Setting $c = (0, \dots, 0)$ passes `0 / 72` active 4-party cuts for $\operatorname{AME}(9, 10)$ and `0 / 129` active 5-party cuts for $\operatorname{AME}(11, 10)$.
2. **400 Random Shift Vectors in $\mathbb{F}_5^9$ (`seed = 42`):** Across `400` uniform random draws $c \in \mathbb{F}_5^9$ evaluated through the identical $5 \times 5$ modulo-5 determinant pipeline across the 72 active 4-party cuts of $\mathcal{S}_9$, `0 / 400` controls pass all 72 cuts (mean `57.53 / 72`, maximum `69 / 72`), whereas our shift vector $c_9 = (0, 0, 0, 1, 4, 4, 3, 1, 1)$ passes `72 / 72` active cuts and `126 / 126` total cuts.
3. **Impure Stabilizer Control:** Directly testing the `codetables.de` $k=0$ matrices `[[15, 0, 8]]_5` and `[[15, 0, 8]]_7` catches `190 / 6,435` and `3,003 / 6,435` rank-deficient 7-party cuts (`w_pure = 7` and `w_pure = 1`).
