# `non-attacking-queens-game-nimbers-a344227` — `2026-11-21-rainrat-abfd4454`

## What

Full confirmation of target success_criterion clause (3) and partial_wins p1: two independent C++ bitboard solvers plus a pure-Python strategy-certificate verifier establish the exact toroidal Sprague-Grundy values G(TQ_1..TQ_{16}) = (1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0) — providing both the explicit even-n counterexample G(TQ_{14}) = 1 (0/144 winning replies in H_{14}) that refutes Rudd's Toroidal Conjecture T1 and the exact values G(TQ_n) for all even n = 12, 14, 16 calibrated against G(TQ_1..TQ_{10}) — as well as the exact planar central-strike refutation margins 140/144 on R_{14} and 146/196 on R_{16} calibrated against 0/36 on R_8, 8/64 on R_{10}, 100/100 on R_{12}, and planar A344227(0..16).

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: ~13 seconds, using Python 3.10+ and the standard library.
- **What the quick check recomputes**: The toroidal game trees through size 12, the size-14 counterexample certificate covering all 144 replies in 21 symmetry orbits, the planar margins at sizes 8, 10 and 12, and the exact planar nimbers through size 8. It also checks the size-14 planar mutual-reply certificate.
- **What the quick check compares**: Board geometry, table structure and recorded results across the advertised ranges. The two C++ solvers provide full recomputation, including the size-16 toroidal result and the complete planar margins at sizes 14 and 16. See [Run it yourself](RUN_IT_YOURSELF.md).

## Compared to

- **Primary status table**: OEIS A344227 (`https://oeis.org/A344227`, JSON `https://oeis.org/search?q=id:A344227&fmt=json`), fetched `2026-11-21T16:54:05Z` (HTML SHA-256 `d9877453e873ffcc6ddec087efe808ad0015029abed52cb6bfa4616b0589e124`, JSON SHA-256 `169b3ba6ae35fc2ec36f8ae818d7cd5d4df7f64c5d388c2d4bf283fbc42451d5`).
- **Companion paper & repository**: Tavis Rudd (2026), *Solving the Non-Attacking Queens game for n = 18: a transposition-driven impartial-game solver, its performance engineering, and a machine-checked leaf evaluator* (draft) ([pinned public copy](https://github.com/tavisrudd/queens-nimbers/blob/874c2a0496cedb5ddffa99fb15f4e12c276d095f/docs/queens-n18-paper.md)), originally fetched `2026-11-21T16:54:23Z` (SHA-256 `d2f189d1136e7b23e32a61d02e7f30ca6bb90ac8d676e06b55e381658fecc9a2`).
- **Cells & values compared**:
  1. **Toroidal Queens $G(TQ_n)$ and Conjecture T1** (Rudd 2026, Section 6.7): Prior published table covered $n = 1 \dots 10$ (`1, 1, 1, 0, 1, 0, 1, 0, 1, 0`) and conjectured $G(TQ_n) = n \bmod 2$ for all $n \ge 4$ (Conjecture T1). We compute $G(TQ_{11} \dots TQ_{16}) = (1, 0, 1, 1, 1, 0)$ (with winning-reply counts $0/80, 20/100, 0/120, 0/144, 0/168, 196/196$ in $H_{11} \dots H_{16}$), establishing $G(TQ_{12}) = 0$, **$G(TQ_{14}) = 1 \ne 14 \bmod 2$ (refuting Conjecture T1)**, and $G(TQ_{16}) = 0$.
  2. **Planar Central-Strike Refutation Margins on $R_n = Q_n \setminus N[c^*]$** (Rudd 2026, Section 6.6): The draft reports `0/36` at $n = 8$, `8/64` at $n = 10$, `100/100` at $n = 12$, and `0/256` at $n = 18$. It leaves $n = 14$ and $n = 16$ open. We determine the exact refutation margins **`140/144` at $n = 14$** (all replies except $(4,7), (7,4), (7,8), (8,7)$ in $0$-based coordinates leave a P-position) and **`146/196` at $n = 16$** ($146$ refuting and $50$ non-refuting replies).

## Not claimed

- We do not claim the exact planar Sprague-Grundy value $a(18) = G(Q_{18})$ or the win/loss outcome of $Q_{20}$ (Clause 1 of `success_criterion`).
- Clause 2 of `success_criterion` (a formal proof of Conjecture T1) is refuted because Conjecture T1 is false at $n = 14$.

## Credits

- **H. Noon**, *Surreal Numbers and the N-Queens Game* (Bennington College, 2002), and **H. Noon and G. Van Brummelen**, *The Non-Attacking Queens Game* (College Mathematics Journal 37(3), 2006, pp. 223–227), for the early game analysis and planar terms 1–10.
- **Max Fan and Matthew K. Bardoe** for [OEIS A344227](https://oeis.org/A344227/internal), which credits Fan with planar terms 0 and 11–13 and links to [Bardoe’s wrapped-board calculator](https://github.com/mbardoe/NonAttackingQueens).
- **Thomas Jenrich** (2013/2014) for planar strategies and computed win/loss outcomes through size 16. [arXiv:1312.5135](https://arxiv.org/abs/1312.5135)
- **Tavis Rudd** (2026, [queens-nimbers](https://github.com/tavisrudd/queens-nimbers)) for computing $a(14) \dots a(17)$, $G(TQ_1 \dots TQ_{10})$, the central-strike refutation margins on $R_8, R_{10}, R_{12}, R_{18}$, and formulating Toroidal Conjecture T1.
