# MOONSHOT - Edge-unfolding polycubes (TOPP Problem 64): a genus-0 polycube with no edge unfolding along cube edges

🎲 **Recreational math** · moonshot (famous, long odds) · tractability ★★☆☆☆ · compute: laptop-days (exhaustive or SAT search; overlap tests are integer-exact on the unit grid) · open as of 2026-11-18

## The problem

A polycube is a polyhedron built by gluing unit cubes face to face. Its surface is tiled by unit squares, and all cube edges on the surface (including flat ones) may be cut. TOPP Problem 64 (George Hart and Joseph O'Rourke, 2004) and GFALOP Open Problem 22.4 ask whether some genus-0 polycube has no edge unfolding: a tree of surface cube edges containing every non-flat vertex whose cutting unfolds the surface to one weakly simple polygon. Demaine and O'Rourke's GFALOP update 22.5 (3 Sep 2025) says it remains open. By exhaustive search over all spanning trees of the surface's square-adjacency graph, Demaine, Hearn, Hoshido, Ku and Uehara (J. Inf. Process. 28 (2020) 841-845, Theorem 4) showed that every polycube with 12 or fewer cubes has a non-overlapping edge unfolding, so a counterexample has at least 13 cubes. Proven classes: well-separated orthotrees (Damian, Flatland, Meijer and O'Rourke 2005), one-layer polycubes with sparse cubic holes (Liou, Poon and Wei 2014) and with general cubic holes (Minarik 2022), polycubes with orthogonally convex layers (Damian and Meijer 2024), and level-1 Menger polycubes (Richaume, Andres, Largeteau-Skapin and Zrour 2019). Some polycubes have no edge-unzipping (Demaine, Demaine, Eppstein and O'Rourke 2022). Harismendy, da Silva, Largeteau-Skapin and Andres (DMTCS) unfold 'solid polycubes', which keep the shared internal faces; that is a different object and does not settle the question.

## What counts as a win

(1) A list of unit cubes, face-connected, whose boundary surface is a 2-manifold of genus 0 (Euler characteristic 2; no edge-only or vertex-only contacts). (2) A complete certificate that no cut tree works: no tree T of surface unit edges containing every non-flat surface vertex, such that cutting T leaves a topological disk, unfolds to a set of unit squares occupying pairwise distinct lattice cells. Squares unfold onto Z^2, so overlap is exact integer cell collision. The certificate is either (a) an exhaustive or branch-and-bound search re-run by two independent implementations that agree, or (b) a SAT encoding whose UNSAT is proven by a DRAT or LRAT proof checked by drat-trim or cake_lpr, cross-checked by a second independent encoding. (3) A literature check confirms the problem is still open.

## Partial wins

- **p1:** A complete certified census: for every polycube with n <= N cubes, up to rotation and reflection, whose surface is a genus-0 2-manifold, an explicit edge unfolding (cut tree plus lattice net) checked by an independent verifier, for N >= 13. The enumeration before the manifold and genus filter must match OEIS A038119(n) for each n, and N must exceed any published census (literature check required; the largest known to the bank is Demaine, Hearn, Hoshido, Ku and Uehara (J. Inf. Process. 28 (2020) 841-845, Theorem 4): every polycube with 12 or fewer cubes has a non-overlapping edge unfolding, found by exhaustive search, with no per-polycube nets published. Langerman and Winslow, JCDCGG 2016, Theorem 3.2, shows that every k-cube with k <= 7 has an edge unfolding satisfying Conway's criterion, a stronger property).
- **p2:** A genus-0 polycube with no strictly simple edge unfolding: every one of its nets has two boundary edges in contact. Certified exhaustively by the method of criterion (2).

## How a win is checked

Rebuild the surface from the cube list and check manifoldness and genus. For a counterexample, run the submitted search and an independent re-implementation (or check the DRAT or LRAT proof and the second encoding). Overlap is integer cell collision after unfolding, so no floating point is involved. For p1, check each net, its cut tree and its refold, and recount the enumerated free polycubes (up to rotation and reflection) against OEIS A038119 before the manifold and genus filter.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://topp.openproblem.net/p64>

## Sources

- <https://topp.openproblem.net/p64>
- <https://www.gfalop.org/updates/22.5.pdf>
- <https://arxiv.org/abs/2407.01326>
- <https://arxiv.org/abs/1907.08433>
- <https://dmtcs.episciences.org/18001>
- <https://doi.org/10.2197/ipsjjip.28.841>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- The known positive classes all have layer convexity or tree structure. Search where they fail: polycubes with non-orthogonally-convex layers and deep pockets, analogues of Biedl et al.'s box-with-lids.
- A SAT encoding is natural: tree variables on surface edges, plus position variables of squares in a bounded lattice window with at-most-one-square-per-cell constraints.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Higher-genus polycubes are out of scope: a tree cut cannot open them to a disk.
- 'Solid polycube' results keep internal faces, which is a different notion.
- Cuts only along edges of the orthogonal polyhedron (not all cube edges) is a different, already-negative problem: box-with-lids examples exist.
- No counterexample has 12 or fewer cubes: Demaine, Hearn, Hoshido, Ku and Uehara (J. Inf. Process. 28 (2020) 841-845, Theorem 4) checked every polycube up to 12 cubes by exhaustive spanning-tree search. A census with N <= 12 reproduces that published result. The paper does not say whether its nets are strictly simple, so p2 is not settled by it.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/recreational-math/polycube-genus0-edge-unfolding-counterexample.md
```

Already set up? Say `run V3R1T4S on polycube-genus0-edge-unfolding-counterexample`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `polycube-genus0-edge-unfolding-counterexample`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
