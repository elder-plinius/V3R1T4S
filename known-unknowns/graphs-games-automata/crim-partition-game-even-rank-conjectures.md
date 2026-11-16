# CRIM on integer partitions: prove or refute the Bašić-Gottlieb-Krnc normal-play P-position conjectures (arXiv:2606.16828)

🕸️ **Graphs, games and automata** · standard · tractability ★★★★☆ · compute: laptop-hours to pure thought (p(50) = 204,226, p(65) = 2,012,558 and p(75) = 8,118,264 partitions; bottom-up dynamic programming over partitions by size, and closed-form invariants that can be formalised) · open as of 2026-11-15

## The problem

Column-Row Impartial Merge (CRIM), studied by Ina Bašić, Eric Gottlieb, and Matjaž Krnc ('CRIM: A Natural Game on Integer Partitions', arXiv:2606.16828v1, June 15, 2026), is a normal-play impartial combinatorial game played on an integer partition lambda = [lambda_1, ..., lambda_r] (viewed as a Young diagram with r rows and largest part lambda_1). A legal move consists of removing either an arbitrary row i in {1, ..., r} (deleting lambda_i) or an arbitrary column j in {1, ..., lambda_1} (decrementing by 1 every part lambda_i >= j and dropping zero parts), with the remaining cells reattaching to form a single partition; the empty partition [] is the unique terminal P-position (second-player win). Bašić, Gottlieb, and Krnc prove that all Odds-Are-Even (OAE) partitions are P-positions (Theorem 1), that an Evens-Are-Odd (EAO) partition with lambda_1 > 1 and r > 1 is a P-position iff its Dyson rank |r - lambda_1| is even (Theorem 2), that the meld of balanced rectairs is in P (Theorem 3), and they completely characterize P-positions for 2-part and 3-part partitions (Proposition 10 and Theorem 11). For normal-play P/N outcomes, they pose four explicit structural conjectures: Conjecture 1 (Even-Rank Conjecture, verified computationally by the authors for all partitions of size n <= 50): every P-position in CRIM has even Dyson rank |r - lambda_1|; Conjecture 7: the meld of losing thick hooks is in P; Conjecture 8: if lambda and the hook Gamma_{r,c} are both losing and the stack Gamma_{r,c} <| lambda is defined, the stack is losing (a hook with at least two rows and two columns is losing exactly when its rank is even); and Conjecture 9: a parity self-conjugate partition (lambda_k = lambda'_k mod 2 for all k) is in N iff it is a stack of odd self-conjugate hooks and [1]. (Note: Section 5 Question 1 asking for a characterization of 4-part P-positions [lambda_1, lambda_2, lambda_3, lambda_4] was already resolved and formalized in Lean 4 in the-omega-institute/trureturing, D5/S3/Combinatorics/Games/CrimFourPartClassification.lean, commit f88c5c77fa6a3e13fd808905f2493c7cf48a7ba0 on 2026-11-04, and is therefore excluded. In addition, the paper's Sprague-Grundy Conjectures 2-5 and misere Conjecture 6 are excluded: Conjecture 3 disagrees with Conjecture 5 on padded staircases PS_{r-1}, where exact computation gives G(PS_6) = 1 and G(PS_7) = 3 as Conjecture 5 predicts.)

## What counts as a win

CONFIRMED: either (A) a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones) of one of Bašić, Gottlieb, and Krnc's normal-play P-position conjectures (Conjecture 1, Conjecture 7, Conjecture 8, or Conjecture 9); OR (B) an explicit counterexample partition lambda refuting Conjecture 1 (with size n > 50), Conjecture 7, Conjecture 8, or Conjecture 9, verified by two independently written normal-play CRIM solvers that both reproduce the authors' computational baseline for all partitions of size n <= 50 (no odd-rank P-position, and Conjecture 9 holding) and the paper's printed values (Proposition 10, Theorem 11, and the Sprague-Grundy values printed with Conjectures 2-5, for example G(R^1_{3,2}) = 3 and G(R^4_{6,5}) = 5) and agree on the P/N status of lambda and all its reachable subpartitions (with all package files strictly <= 1 MB per kit/SUBMIT.md).

## Partial wins

- **p1:** Exhaustive verification of Conjecture 1 (every P-position has even Dyson rank) and Conjecture 9 (characterization of parity self-conjugate N-positions) extended from n <= 50 to all partitions of size n <= 65, by two independent bottom-up dynamic programming solvers that reproduce all n <= 50 results and agree on the exact count of P-positions and Dyson-rank distributions for every n <= 65.

## How a win is checked

For a formal proof (A), build the development in a clean project and audit the axioms of the main theorem (Lean: `lake build` and `#print axioms`). For a counterexample (B) or finite-range verification (p1, p2), run two independent normal-play CRIM engines (one indexing partitions by integer-partition rank/lexicographic hash in C/Rust, one using conjugate-canonicalized Young diagram bitmasks in Python/C++) implementing the normal-play P/N recurrence (lambda is in P iff every legal row removal and every legal column removal lands in N). Both engines must first reproduce the paper's theorems on small cases, the n <= 50 baseline (Conjectures 1 and 9 hold for all n <= 50) and the printed Sprague-Grundy values, and then verify every transition of the claimed counterexample or finite range.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2606.16828>

## Sources

- <https://arxiv.org/abs/2606.16828>
- <https://arxiv.org/html/2606.16828v1>
- <https://github.com/the-omega-institute/trureturing>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Because CRIM is symmetric under conjugation (transposing the Young diagram swaps row moves and column moves and preserves Dyson rank |r - lambda_1|), canonicalizing each partition with its conjugate lambda' halves the state space immediately.
- For p1, bottom-up evaluation by partition size n = |lambda| needs only the P/N bit (1 bit per partition) of smaller sizes, and since p(65) = 2,012,558, the entire P-position bitset up to n = 65 fits in a few megabytes of RAM.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Question 1 (characterization of losing 4-part partitions) was solved and formalized in Lean 4 in the-omega-institute/trureturing (D5/S3/Combinatorics/Games/CrimFourPartClassification.lean, commit f88c5c77fa6a, 2026-11-04) and is excluded as already settled.
- Removing column j decrements every part lambda_i >= j by 1 (reattaching the right side of the Young diagram to the left); do not confuse this with Chomp (which deletes all cells below and to the right).
- Dyson's rank in arXiv:2606.16828 is defined as |r - lambda_1|, where r is the number of positive parts and lambda_1 is the largest part.
- Conjectures 3 and 5 disagree on padded staircases (the case k = r - 2 of Conjecture 3 is PS_{r-1}); exact values follow Conjecture 5 (G(PS_6) = 1, G(PS_7) = 3). Conjectures 2-6 are out of scope; only the normal-play P-position Conjectures 1, 7, 8, and 9 are in scope.
- Always calibrate on all partitions up to n = 50 (the range the authors checked, Section 5 of arXiv:2606.16828v1), not only on small cases.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/crim-partition-game-even-rank-conjectures.md
```

Already set up? Say `run V3R1T4S on crim-partition-game-even-rank-conjectures`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `crim-partition-game-even-rank-conjectures`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
