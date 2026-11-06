# Non-Attacking Queens game (Node-Kayles on the n-queens graph): exact nimber a(18), the 20x20 outcome, and toroidal Conjecture T1 (OEIS A344227)

🕸️ **Graphs, games and automata** · standard · tractability ★★★☆☆ · compute: laptop-hours for toroidal boards n = 12 and 14 and refutation-margin tables; workstation-days for exact G(18), TQ_16 or the 20x20 outcome · open as of 2026-11-06

## The problem

The Non-Attacking Queens game (H. Noon, 2002; H. Noon and G. Van Brummelen, College Math. J. 37(3), 2006, 223-227; Thomas Jenrich, arXiv:1312.5135, 2013/2014; OEIS A344227) is Node-Kayles played on the n-queens graph Q_n: two players alternately place queens on an n x n chessboard so that no two queens attack each other (no shared row, column, or diagonal), and the last player able to place a queen wins. For odd n, the first player always wins by playing the center square and mirroring every reply by 180-degree rotation (so G(Q_n) >= 1). For n = 0..13, Noon, Bardoe, and Fan computed the Sprague-Grundy sequence A344227: 0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1. Because a(10) = a(12) = 0 (and Jenrich showed 14x14 and 16x16 are second-player wins), A344227 carried the empirical conjecture that a(n) oscillates as 0, 1, 0, 1 for all n >= 9. In August 2026, Tavis Rudd ('queens-nimbers', OEIS A344227 comment and technical report) extended A344227 through n = 17 with G(14) = 0, G(15) = 1, G(16) = 0, G(17) = 2 (breaking the odd-n = 1 pattern) and proved that the 18x18 board is a first-player win (opening at I9 = (8,8), so G(18) >= 1, breaking the even-n = 0 pattern). As of 2026-11-06, three concrete problems are explicitly open in A344227 and Rudd (2026): (1) the exact Sprague-Grundy value a(18) = G(Q_{18}) (Rudd 2026, Section 6.5, predicts 1 and calls this a prediction, not a result; since proving G(18) = 1 reduces via the heap-sum method to showing Q_{18} + Nim(1) is a second-player win); (2) whether the 20x20 board (Q_{20}) is a first-player (N) or second-player (P) win; and (3) Conjecture T1 (Section 6.7 of Rudd 2026) on the toroidal n-queens graph TQ_n (where rows, columns, and both diagonals wrap mod n, so vertex-transitivity forces G(TQ_n) in {0,1}): Rudd computed G(TQ_n) for n = 1..10 as 1, 1, 1, 0, 1, 0, 1, 0, 1, 0 and conjectured that G(TQ_n) = n mod 2 for all n >= 4. For odd n this already follows from Rudd's Theorem S1 (Closed-Pairing, Section 6.8) applied to the point reflection x -> -x (mod n) on the residual TQ_n minus N[(0,0)]: it is a fixed-point-free automorphism there and never pairs two attacking squares (rechecked by the maintainer for odd n <= 25 on 2026-11-06). The open part of Conjecture T1 is therefore the even boards, n = 12, 14, 16, ...

## What counts as a win

CONFIRMED: any one of: (1) the exact Sprague-Grundy value a(18) = G(Q_{18}) (certified via exact mex evaluation or heap-sum P-position verification of Q_{18} + Nim(a(18)) plus N-position verification of Q_{18} + Nim(k) for 0 <= k < a(18)) or the 1st/2nd-player win/loss outcome of Q_{20}, established by two independently written bitboard solvers that both reproduce A344227 for n = 0..17; OR (2) a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones) of Rudd's full Toroidal Conjecture T1 (G(TQ_n) = n mod 2 for all n >= 4); OR (3) an explicit toroidal counterexample refuting Conjecture T1 (necessarily at an even n), or the exact computation of G(TQ_n) for every even n = 12, 14, 16, by two independent bitboard solvers that both reproduce G(TQ_n) for n = 1..10.

## Partial wins

- **p1:** Compute the exact toroidal values G(TQ_{12}) and G(TQ_{14}) (testing the even half of Conjecture T1 beyond n = 10), plus the exact central-strike refutation margins on R_{14} and R_{16} (Section 6.6 of Rudd 2026: the number of legal replies on R_n = Q_n minus N[c*] that leave a P-position, calibrated against Rudd's published margins 0/36 at n = 8, 8/64 at n = 10 and 100/100 at n = 12), verified by two independent bitboard solvers.

## How a win is checked

For a formal proof in (2), build the development in a clean project and audit the axioms of the theorem (Lean: `lake build` and `#print axioms`). For computational claims in (1), (3) or p1: on toroidal boards TQ_n, since TQ_n is vertex-transitive, every first move is isomorphic; thus G(TQ_n) = 1 iff the residual board H_n = TQ_n minus N[(0,0)] after placing one queen at (0,0) is a P-position (second-player win), and G(TQ_n) = 0 otherwise. For exact standard-board nimbers a(n) = G(Q_n), boolean alpha-beta on Q_n alone only tests whether G(Q_n) > 0; solvers must either evaluate exact mex values or certify via the heap-sum game that Q_n + Nim(g) is a P-position and Q_n + Nim(k) is an N-position for all 0 <= k < g. Two independent bitboard solvers using distinct traversal/canonicalization algorithms (e.g., D_4-canonical Zobrist alpha-beta vs. independent retrograde/DAG solver) must reproduce G(TQ_n) for n = 1..10, A344227 for n = 0..17, and the published central-strike refutation margins for n = 8, 10 and 12 before certifying any new value. Keep all package files <= 1 MB (kit/SUBMIT.md).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A344227>

## Sources

- <https://oeis.org/A344227>
- <https://github.com/tavisrudd/queens-nimbers>
- <https://raw.githubusercontent.com/tavisrudd/queens-nimbers/main/docs/queens-n18-paper.md>
- <https://arxiv.org/abs/1312.5135>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- For Conjecture T1 at n >= 12, vertex-transitivity of TQ_n removes the root branching: place the first queen at (0,0) and solve the single residual graph H_n = TQ_n minus N[(0,0)] under the symmetries fixing (0,0); G(TQ_n) = 1 iff H_n is a P-position. For odd n the point reflection (r, c) -> (-r, -c) mod n is a closed pairing of H_n (Rudd's Theorem S1), which settles odd n; for even n the reflection pairs some squares with an attacking partner (for example (n/2, 1) and (n/2, n-1) share a row), so it is not a closed pairing and the computational work is on even n.
- For the refutation-margin puzzle in Section 6.6 of Rudd (2026) at n = 14 and n = 16, after the central strike c* = (n/2 - 1, n/2 - 1), the central queen attacks 4n - 4 squares, so the residual board R_n = Q_n minus N[c*] has exactly (n - 2)^2 live squares (144 at n = 14 and 196 at n = 16); solving each legal Player 2 reply in R_n independently with two bitboard solvers gives the exact count of replies that leave a P-position.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- On the torus TQ_n, two squares (r1, c1) and (r2, c2) attack each other iff r1 = r2 (mod n), c1 = c2 (mod n), r1 - c1 = r2 - c2 (mod n), or r1 + c1 = r2 + c2 (mod n). For even n the point reflection pairs some squares of the residual with an attacking partner (for example (n/2, 1) and (n/2, n-1)), so it does not settle even boards.
- On the standard board Q_n, a(n) in A344227 is the Sprague-Grundy value G(Q_n), whereas a boolean solver on Q_n tests only whether G(Q_n) > 0; use exact mex or the heap-sum game Q_n + Nim(k) to certify exact nimbers.
- Rudd (2026, Section 2.2) reports that the exact n = 18 nimber was still being computed. Re-check the queens-nimbers repository and OEIS A344227 immediately before claiming a(18).
- Rudd publishes central-strike refutation margins only for n = 8, 10, 12 and 18 (Section 6.6); there are no published margins for n = 4 or 6 to calibrate against.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/non-attacking-queens-game-nimbers-a344227.md
```

Already set up? Say `run V3R1T4S on non-attacking-queens-game-nimbers-a344227`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `non-attacking-queens-game-nimbers-a344227`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
