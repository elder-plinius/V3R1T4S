# MOONSHOT - The binary q-analog of the Fano plane S_2[2,3,7] (fallback: a (7,4;3)_2 subspace code with more than 333 planes)

📊 **Record tables** · moonshot (famous, long odds) · tractability ★★☆☆☆ · compute: needs cluster (exhaustive or symmetry-reduced ILP/SAT); partial wins laptop-days · open as of 2026-11-18

## The problem

A binary q-Fano plane is a set of planes (3-dim subspaces) of F_2^7 such that every line (2-dim subspace) lies in exactly one of them; it would have 381 planes. It is the smallest admissible q-Steiner system S_2[2,3,7] and its existence is the best-known open problem on q-analogs of designs. Equivalently A_2(7,4;3)=381, where A_2(7,4;3) is the largest set of planes in F_2^7 pairwise meeting in at most a point; Kurz's survey (arXiv 2112.11766, v3 2025-12-20, Section 6) calls it the smallest unknown binary value and gives 333 <= A_2(7,4;3) <= 381, and either A_2(7,4;3) <= 378 or = 381 (Nakic and Storme: a 380-plane code extends to 381; the rest via divisible codes). The 333 code is by Heinlein, Kiermaier, Kurz and Wassermann (arXiv 1708.06224), who also show any code with >= 334 planes has automorphism group of order <= 12. Braun, Kiermaier and Nakic (arXiv 1501.07790) showed a q-Fano plane is rigid or has a cyclic automorphism group of order 2, 3 or 4, and Kiermaier, Kurz and Wassermann (arXiv 1605.03853) brought this down to order <= 2. Thomas (1996), Heden and Sissokho (2016) and Kiermaier (arXiv 2105.00365) proved that non-alpha points must exist.

## What counts as a win

Full win (either direction): (a) an explicit list of 381 planes of F_2^7 (each as a 3x7 binary generator matrix of rank 3) such that every one of the 2667 lines of F_2^7 is contained in exactly one listed plane; or (b) a machine-checked proof that no such set exists: a Lean/Isabelle/Coq proof, or a complete exhaustive search with a verifiable certificate (e.g. DRAT/LRAT proof checked by an independent checker for a published SAT encoding, plus an independent check of every symmetry-reduction step). Compared against the status in arXiv 2112.11766 (open, current lower bound 333).

## Partial wins

- **p1:** A set of at least 334 planes of F_2^7, pairwise intersecting in at most a 1-dimensional subspace (i.e. every line in at most one plane), strictly beating A_2(7,4;3) >= 333.
- **p2:** Settle the research problem in arXiv 2112.11766 Section 6 in either direction: 240 planes in PG(6,2) admitting an automorphism pi of order 5, all disjoint from the plane F of pi-fixed points (an order-5 element of GL(7,2) fixes exactly a 3-dim subspace, 7 points), no two meeting in a line, and covering each of the 120 points outside F exactly 14 times (explicit planes plus the matrix of pi), or an exhaustive certificate that none exist. The survey text says '15 times', which is arithmetically impossible (240*7 = 1680 = 120*14); 14 is the count forced in a q-Fano plane by the stated complementary set (F plus 140 planes meeting F in a point).
- **p3:** For the relaxation in arXiv 2112.11766 Section 6 (45 planes of F_2^6 with every 5-space containing exactly five, every point in exactly five, each line and each solid in at most one), an explicit set with strictly more alpha'-points in total than the stated lower bound 19, or in one fixed 5-space strictly more than 15. Not reachable as stated: two independent SAT certificates (see pitfalls) show that no such set has more than 15 alpha'-points, in total or in one 5-space, so the maximum is 15 for both counts.

## How a win is checked

Represent each plane by its reduced row echelon form; enumerate its 7 lines; count how often each of the 2667 lines of F_2^7 is covered (exactly once for a full win, at most once for p1, with all planes distinct and of rank 3). For p2/p3 check every stated incidence condition by brute force over all subspaces of PG(6,2)/PG(5,2). For a nonexistence claim, re-run the certificate checker and independently audit the encoding and symmetry breaking. Re-fetch arXiv 2112.11766 and its citing literature before claiming.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://arxiv.org/abs/2112.11766>

## Sources

- <https://arxiv.org/abs/2112.11766>
- <https://arxiv.org/abs/1708.06224>
- <https://arxiv.org/abs/1605.03853>
- <https://arxiv.org/abs/2105.00365>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Prescribe automorphism groups allowed by the 333-paper classification (order <= 12 for >= 334 planes; the group G_{12,1} = Z3 x| Z4 named in the survey) and solve the Kramer-Mesner style ILP with a modern solver.
- For p1, start from the 333 code (Klein four-group) and run large-neighbourhood search: remove k planes, re-solve the exact cover-at-most-once ILP on the freed lines.
- Use the derived structure: through each point the planes induce a line spread of PG(5,2); constrain by non-alpha-point results.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- A 380-plane code would already extend to 381, and codes of size 379 or 380 are ruled out unless 381 exists, so heuristic searches stalling near 333 are normal.
- Do not confuse with the ternary case or with partial q-Fano planes; the win is about q=2, n=7, k=3.
- arXiv 1709.05145 (Bamberg, Ihringer, Lansdown, Royle) claimed a trivial automorphism group but was withdrawn after a computational mistake; the proven bound is order <= 2.
- The Bayreuth table site was unreachable on 2026-10-30; use the survey and arXiv for status.
- p3's bounds (total between 19 and 44, one 5-space between 15 and 22, by ILP; the same sentence in v1, v2 and v3) do not match the stated definition. Under that definition (every point and every 5-space in exactly five planes, so #C = 45) the maximum is 15 for both counts, shown by two independent certificates: (1) a written structure theorem (the alpha'-points carry an alternating form; five cases) with five CaDiCaL refutations, 135 DRAT proofs checked by drat-trim; (2) a direct encoding of the definition with three proved covering lemmas and GL(6,2) orbit splitting, 545 + 496 leaves for the total and 15 + 93 for one 5-space, every leaf refuted by CaDiCaL 2.1.3 with a DRAT proof checked by drat-trim. 15 is attained, with all 15 points in one 5-space. Reading 'exactly five' as 'at least five' gives a 53-plane set with 19 alpha'-points, 15 of them in one 5-space, which matches the survey's two lower bounds, so its ILP probably used at-least-five constraints.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/binary-q-fano-plane-s2-2-3-7.md
```

Already set up? Say `run V3R1T4S on binary-q-fano-plane-s2-2-3-7`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `binary-q-fano-plane-s2-2-3-7`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
