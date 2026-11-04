# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target cubic-graphs-graceful-knuth-beyond-14. The task was to extend the
computer verification of Knuth's conjecture that every connected cubic graph is graceful. DS6 (28th ed.) gives 4..14
vertices, and Knuth's pre-fascicle 7A gives 16. The goal was 16, 18, 20 and 22 vertices with certificates, or a
counterexample.

- Scouting found that order 16 is already settled: Knuth's pre-fascicle 7A, answer to exercise 96, and Kennedy
  (2021). OEIS A337965 also stops at 16. Nothing was found for 18 or more vertices.
- What worked: an edge-driven randomised backtracking search (how-we-built-it/glab.c). It runs on nauty geng's list
  of connected cubic graphs. The search realises the largest difference first: q forces labels 0 and q on one edge.
  It labelled every connected cubic graph on 4..22 vertices with no failure. The 7,319,447 graphs of order 22
  needed at most 10,200 search nodes each.
- What did not work or was not needed:
  - An annealing labeller left 4,041 of the 4,060 graphs of order 16 unsolved.
  - A CP-SAT model was complete but about 100 times slower. It was kept to confirm that 2K4 and 3K4 have no
    graceful labeling.
  - A contrarian lens looked for counterexample suspects. Graphs with bridges or many triangles turned out to have
    many labelings, and an exact labeling counter reproduced OEIS A337965 a(2..6).
  - A parity obstruction holds on every certificate line but never rules out a labeling.
- Checkers: a C per-line checker with nauty labelg coverage against a fresh geng run, and a Python checker with no
  nauty. A three-skeptic panel (reproduce, novelty, criterion), each in a fresh context with its own code, then
  confirmed the scope quoted in README.md. For this package, a further standard-library checker with exact canonical
  forms (verify-it-yourself/) was written and run on all orders 4..22.
