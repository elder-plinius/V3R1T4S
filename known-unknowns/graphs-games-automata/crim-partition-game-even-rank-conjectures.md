# CRIM on integer partitions: prove or refute the Bašić-Gottlieb-Krnc normal-play P-position conjectures (arXiv:2606.16828)

🕸️ **Graphs, games and automata** · standard · tractability ★★★★☆ · compute: laptop-hours to pure thought (p(50) = 204,226, p(65) = 2,012,558 and p(75) = 8,118,264 partitions; bottom-up dynamic programming over partitions by size, and closed-form invariants that can be formalised) · open as of 2026-11-16

## The problem

Column-Row Impartial Merge (CRIM), studied by Ina Bašić, Eric Gottlieb, and Matjaž Krnc ('CRIM: A Natural Game on Integer Partitions', arXiv:2606.16828v1, June 15, 2026), is a normal-play impartial combinatorial game played on an integer partition lambda = [lambda_1, ..., lambda_r] (viewed as a Young diagram with r rows and largest part lambda_1). A legal move consists of removing either an arbitrary row i in {1, ..., r} (deleting lambda_i) or an arbitrary column j in {1, ..., lambda_1} (decrementing by 1 every part lambda_i >= j and dropping zero parts), with the remaining cells reattaching to form a single partition; the empty partition [] is the unique terminal P-position (second-player win). Bašić, Gottlieb, and Krnc prove that all Odds-Are-Even (OAE) partitions are P-positions (Theorem 1), that an Evens-Are-Odd (EAO) partition with lambda_1 > 1 and r > 1 is a P-position iff its Dyson rank |r - lambda_1| is even (Theorem 2), that the meld of balanced rectairs is in P (Theorem 3), and characterize P-positions for 2-part and 3-part partitions (Proposition 10 and Theorem 11; Theorem 11's printed wording requires lambda_1 >= 3 because [1, 1, 1] = Gamma_{3,1} has G([1, 1, 1]) = 1 in N by Proposition 7). For normal-play P/N outcomes, they pose four structural conjectures: Conjecture 1 (Even-Rank Conjecture): every P-position in CRIM has even Dyson rank |r - lambda_1|; Conjecture 7: the meld of losing thick hooks is in P; Conjecture 8: if lambda and the hook Gamma_{r,c} are both losing and the stack Gamma_{r,c} <| lambda is defined, the stack is losing; and Conjecture 9: a parity self-conjugate partition (lambda_k = lambda'_k mod 2 for all k) is in N iff it is a stack of odd self-conjugate hooks and [1]. Prior work and negative-run status as of 2026-11-16: (1) the-omega-institute/trureturing (D5/S3/Combinatorics/Games/CrimFourPartClassification.lean, commit f88c5c77fa6a3e13fd808905f2493c7cf48a7ba0 on 2026-11-04, plus CrimGrundyRefutation.lean and CrimRectairSquareBoundaryRefutation.lean) formalized Question 1 (4-part P-positions) in Lean 4 and refuted Sprague-Grundy Conjectures 2 and 3; (2) Sanjit Singh Mehat (doi:10.5281/zenodo.22070744, 2026-08-23) formalized in Lean 4 the P/N classification and Conjecture 1 for width <= 6 (l(lambda) <= 6 or lambda_1 <= 6); (3) Zijian Zeng (ArtificialZeng/AI-Has-Taste, commit f3ae144b, 2026-09-16, manuscript BW2-B02-P10 dated 2026-08-29) gave an unformalized LaTeX paper proof of a complete boundary-word classification of all CRIM P-positions (Theorem 1.1: W(lambda) = 0^{a_1} 1^{b_1} ... 0^{a_k} 1^{b_k} in P iff |w| = 0 mod 2 and M(w) = 0 mod 2) and deduced Conjecture 1 on paper for all n >= 0 (Corollary 1.2), with numerical checks up to n <= 50; (4) a 2026-11-16 negative run verified via two independent C++20 bottom-up DP solvers across all 14,320,697 partitions of size 0 <= n <= 65 (4,035,765 P-positions) that there are 0 counterexamples to Conjecture 1, Conjecture 7 (7,709 melds of losing thick hooks), Conjecture 8 (2,074,930 valid losing hook stacks), or Conjecture 9 (15,586 parity self-conjugate partitions, 136 in N). (Note: the paper's Sprague-Grundy Conjectures 2-5 and misere Conjecture 6 are excluded: Conjecture 3 disagrees with Conjecture 5 on padded staircases PS_{r-1}, where exact computation gives G(PS_6) = 1 and G(PS_7) = 3 as Conjecture 5 predicts.)

## What counts as a win

CONFIRMED: either (A) a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones) of one of Bašić, Gottlieb, and Krnc's normal-play P-position conjectures in full generality: unrestricted Conjecture 1 (for all n and arbitrary number and size of parts, beyond the width <= 6 formalization of 10.5281/zenodo.22070744), Conjecture 7, Conjecture 8, or Conjecture 9; OR (B) an explicit counterexample partition lambda (with size n > 65) refuting Conjecture 7, Conjecture 8, or Conjecture 9 (or Conjecture 1), verified by two independently written normal-play CRIM solvers that reproduce the n <= 65 baseline (4,035,765 P-positions across 14,320,697 partitions, 0 counterexamples) and the paper's printed values (Proposition 10, Theorem 11 for lambda_1 >= 3, and the Sprague-Grundy values printed with Conjectures 2-5, e.g. G(R^1_{3,2}) = 3, G(R^4_{6,5}) = 5, G(PS_6) = 1, G(PS_7) = 3) and agree on the P/N status of lambda and all its reachable subpartitions (with all package files strictly <= 1 MB per kit/SUBMIT.md).

## Partial wins

- **p1:** Extend exhaustive verification of Conjecture 9 (characterization of parity self-conjugate N-positions), Conjecture 7 (melds of losing thick hooks), and Conjecture 8 (losing hook stacks Gamma_{r,c} <| lambda) beyond n <= 65 to all 61,537,395 partitions of size 0 <= n <= 75 (p(75) = 8,118,264), by two independent bottom-up dynamic programming solvers that reproduce all n <= 65 results (4,035,765 P-positions, 15,586 PSC partitions, 136 PSC in N) and agree on the exact count of P-positions and Dyson-rank distributions for every n <= 75.

## How a win is checked

For a formal proof (A), build the development in a clean project and audit the axioms of the main theorem (Lean: `lake build` and `#print axioms`) and confirm unrestricted generality beyond width <= 6. For a counterexample (B) or finite-range verification (p1), run two independent normal-play CRIM engines (one indexing partitions by integer-partition lexicographic rank in C/C++/Rust, one using ascending colexicographic rank or Young-diagram bitmasks without conjugate folding) implementing the normal-play P/N recurrence (lambda is in P iff every legal row removal and every legal column removal lands in N). Both engines must first reproduce the paper's theorems (with lambda_1 >= 3 for Theorem 11), the n <= 65 baseline (14,320,697 partitions, 4,035,765 P-positions, 15,586 PSC partitions, 136 PSC in N, 0 counterexamples to Conjectures 1, 7, 8, 9), and printed Sprague-Grundy values, and then verify every transition of the claimed counterexample or finite range.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2606.16828>

## Sources

- <https://arxiv.org/abs/2606.16828>
- <https://arxiv.org/html/2606.16828v1>
- <https://github.com/the-omega-institute/trureturing>
- <https://github.com/ArtificialZeng/AI-Has-Taste>
- <https://doi.org/10.5281/zenodo.22070744>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Because CRIM is symmetric under conjugation (transposing the Young diagram swaps row moves and column moves and preserves Dyson rank |r - lambda_1|), canonicalizing each partition with its conjugate lambda' halves the state space immediately.
- For Criterion (A), formalizing Zijian Zeng's Theorem 1.1 boundary-word characterization (BW2-B02-P10: W(lambda) = 0^{a_1} 1^{b_1} ... 0^{a_k} 1^{b_k} in P iff |w| and M(w) = min(k, L(w) + R(w)) are even) in Lean 4 would yield unrestricted Conjecture 1 plus short boundary-word proofs of Conjecture 7 (concatenation of thick-hook words 0^a 1^{c-b} 0^{r-a} 1^b with a, b >= 2 preserves L = R = M = 0) and Conjecture 8 (stacking Gamma_{r,c} <| lambda adds equal-parity overhangs Delta_c = c - 1 - lambda_1 and Delta_r = r - 1 - l(lambda)).
- For p1 up to n = 75 (p(75) = 8,118,264), bottom-up evaluation by partition size n = |lambda| needs only the P/N bit (1 bit per partition) of smaller sizes, fitting comfortably in a few tens of megabytes of RAM.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Zijian Zeng (ArtificialZeng/AI-Has-Taste, commit f3ae144b, 2026-09-16, manuscript BW2-B02-P10 dated 2026-08-29) already proved Conjecture 1 on paper for all n >= 0 via a complete boundary-word P/N theorem (Theorem 1.1 & Corollary 1.2) and checked P-position counts to n <= 50; citing or recomputing Conjecture 1 alone or to n <= 65 is not novel.
- Sanjit Singh Mehat (doi:10.5281/zenodo.22070744, 2026-08-23) already formalized Conjecture 1 in Lean 4 for partitions of width <= 6 (l(lambda) <= 6 or lambda_1 <= 6); Criterion (A) requires an unrestricted formalization.
- Question 1 (characterization of losing 4-part partitions) was solved and formalized in Lean 4 in the-omega-institute/trureturing (D5/S3/Combinatorics/Games/CrimFourPartClassification.lean, commit f88c5c77fa6a, 2026-11-04) and is excluded as already settled.
- A 2026-11-16 negative run verified all 14,320,697 partitions of 0 <= n <= 65 (4,035,765 P-positions) with 0 counterexamples to Conjecture 1, Conjecture 7 (7,709 melds), Conjecture 8 (2,074,930 stacks), and Conjecture 9 (15,586 PSC partitions, 136 in N); re-verifying n <= 65 is baseline calibration only.
- Theorem 11 in arXiv:2606.16828v1 omits a lambda_1 >= 3 guard: the 3-part column hook [1, 1, 1] = Gamma_{3,1} has G([1, 1, 1]) = 1 in N by Proposition 7 since min(r, c) = 1.
- Removing column j decrements every part lambda_i >= j by 1 (reattaching the right side of the Young diagram to the left); do not confuse this with Chomp (which deletes all cells below and to the right).
- Dyson's rank in arXiv:2606.16828 is defined as |r - lambda_1|, where r is the number of positive parts and lambda_1 is the largest part.
- Conjectures 3 and 5 disagree on padded staircases (the case k = r - 2 of Conjecture 3 is PS_{r-1}); exact values follow Conjecture 5 (G(PS_6) = 1, G(PS_7) = 3). Conjectures 2-6 are out of scope; only the normal-play P-position Conjectures 1, 7, 8, and 9 are in scope.
- Always calibrate on all partitions up to n = 65 (extending the authors' n = 50 range and 2026-11-16 baseline), not only on small cases.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/crim-partition-game-even-rank-conjectures.md
```

Already set up? Say `run V3R1T4S on crim-partition-game-even-rank-conjectures`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `crim-partition-game-even-rank-conjectures`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
