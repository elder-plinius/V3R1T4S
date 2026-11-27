# Honesty Gate — `non-attacking-queens-game-nimbers-a344227`

status: CONFIRMED_SOLUTION
confirmed_scope: Full confirmation of target success_criterion clause (3) and partial_wins p1: two independent C++ bitboard solvers plus a pure-Python strategy-certificate verifier establish the exact toroidal Sprague-Grundy values G(TQ_1..TQ_{16}) = (1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0) — providing both the explicit even-n counterexample G(TQ_{14}) = 1 (0/144 winning replies in H_{14}) that refutes Rudd's Toroidal Conjecture T1 and the exact values G(TQ_n) for all even n = 12, 14, 16 calibrated against G(TQ_1..TQ_{10}) — as well as the exact planar central-strike refutation margins 140/144 on R_{14} and 146/196 on R_{16} calibrated against 0/36 on R_8, 8/64 on R_{10}, 100/100 on R_{12}, and planar A344227(0..16).

## Three-Skeptic Panel Summary

| Panelist | Context | Verdict | Report |
|---|---|---|---|
| `REPRODUCE` | `subagent` | `pass: true` | `panel/reproduce.md` |
| `NOVELTY` | `subagent` | `pass: true` | `panel/novelty.md` |
| `CRITERION` | `subagent` | `pass: true` | `panel/criterion.md` |

## Gate Checklist (`kit/RUN.md` Step 7)

1. **All three panelists ran in fresh `subagent` contexts and returned `pass: true`**:
   - `REPRODUCE` ran `claim/code/check_claim.py`, `claim/code/verify_tq14_python.py`, `claim/code/solver_a_full.cpp`, and `claim/code/solver_b_tq.cpp`, and wrote an independent from-scratch verification script in Python verifying all entries of `claim/result/toroidal_queens_and_margins.json`.
   - `NOVELTY` verified against all primary-source snapshots in `claim/data/` (`A344227.json`, `A344227.html`, `queens-n18-paper.md`, `conjecture-theory.md`, `submission-package.md`, `verification-RESULTS.md`, `othello-winning-geometry-n20.md`, `othello-cgt-laws-and-tricks.md`) that $G(TQ_{11} \dots TQ_{16})$ (specifically $G(TQ_{12})=0$, the Conjecture T1 counterexample $G(TQ_{14})=1$, and $G(TQ_{16})=0$) and the planar central-strike refutation margins $140/144$ on $R_{14}$ and $146/196$ on $R_{16}$ are unrecorded in prior literature and non-trivial.
   - `CRITERION` verified word-for-word satisfaction of both branches of `success_criterion` clause (3) and `partial_wins` `p1`.
2. **Pre-registration (`PREREG.md`) & Null Test**:
   - `PREREG.md` was frozen prior to the attack (`null_test: not needed because this target is in graphs-games-automata (deterministic finite impartial combinatorial game theory on the n-queens and toroidal n-queens graphs)`).
3. **Table Access & No Leaks**:
   - All status snapshots were fetched politely once per URL with HTTP 200; the URLs, exact UTC fetch times and page SHA-256 hashes are recorded in `the-record-we-beat/table_snapshot.md`.
   - No personal paths, usernames, emails, or tokens appear in `panel/*.md`.
