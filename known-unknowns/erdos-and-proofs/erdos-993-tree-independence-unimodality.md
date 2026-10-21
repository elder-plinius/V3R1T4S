# Erdos #993: a tree (or forest) with non-unimodal independent-set sequence

✏️ **Erdős problems and proofs** · standard · tractability ★☆☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

For every tree or forest T, is the sequence i_k(T) (number of independent sets of size k) unimodal? This is the Alavi-Malde-Schwenk-Erdos conjecture. It is false for general graphs. Log-concavity fails for trees from n = 26 (Kadrawi-Levit 2023). The n = 32 check covered all 109,972,410,221 trees (forum 2026-08-09) and the 3-branch-vertex lemma has a Lean formalisation (BrettRey2, 2026-08-21). Two unverified proof claims are now posted (forum proof-claims page, checked 2026-10-20): Ethan X. Fang, Junwei Lu, Eran Nevo, Yuan Yao and Hailun Zheng (arXiv:2609.20961, submitted 2026-09-21, with a Lean link) claim unimodality for every forest with at least N_0 vertices for some absolute N_0; Tong Zhang (doi 10.5281/zenodo.22999166, submitted 2026-09-27, with a Lean link) claims a full proof. If either holds, a counterexample must be below N_0 or cannot exist. Read both claims before searching.

## What counts as a win

An explicit tree or forest (edge list) whose exactly computed sequence (i_0, i_1, ...) has indices a < b < c with i_a > i_b < i_c. Plateaus do not count.

## Partial wins

- **p1:** An exhaustive, reproducible verification that every tree on 33 vertices has a unimodal independent-set sequence, with the enumerated tree count matching the known number of unlabeled trees on 33 vertices (OEIS A000055) and the code rerun by the verifier.
- **p2:** A rigorous (refereed or Lean-checked) proof that any counterexample tree must have at least 4 vertices of degree >= 3, strengthening the known 3.

## How a win is checked

Confirm the graph is a forest (acyclic; for a tree, connected with n-1 edges). Compute the independence polynomial exactly with Python big integers by the rooted-tree DP I(T) = I(T-v) + x*I(T-N[v]), done twice: two different roots, or DP versus brute force for n <= 40. Then scan for a strict valley.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.erdosproblems.com/993>

## Sources

- <https://www.erdosproblems.com/993>
- <https://www.erdosproblems.com/forum/thread/993>
- <https://zenodo.org/records/19100781>
- <https://arxiv.org/abs/2603.03025>
- <https://arxiv.org/abs/2604.18824>
- <https://www.erdosproblems.com/forum/thread/993/proof-claims>
- <https://arxiv.org/abs/2609.20961>
- <https://doi.org/10.5281/zenodo.22999166>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Mixture design: I(T) = I(T-v) + x*I(T-N[v]). Engineer the two summands to be log-concave with well-separated modes and comparable mass, e.g. attach many pendant stars K_{1,m} (factors (1+x)^m shift modes) on one side versus long paths on the other. Optimise the parameters analytically.
- Amplify the known 'multiple breaks of log-concavity' trees (arXiv 2511.00334, 2502.10654) by gluing or iterating them; search for a dip.
- Evolutionary / RL search over trees with 50-300 vertices. Fitness: min over b of i_b / min(i_{b-1}, i_{b+1}) approaching 1 from above. Use mutations preserving >= 3 branch vertices.
- Forest route: by Hoggar, a forest counterexample needs a non-LC component. Build disjoint unions of non-LC trees whose convolution creates a valley.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Plateaus are allowed in unimodality.
- Float overflow; use exact integers.
- Confirm the object is a tree or forest (a cycle gives an invalid graph).
- Already exhaustively checked to n = 32.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/erdos-and-proofs/erdos-993-tree-independence-unimodality.md
```

Already set up? Say `run V3R1T4S on erdos-993-tree-independence-unimodality`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `erdos-993-tree-independence-unimodality`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
