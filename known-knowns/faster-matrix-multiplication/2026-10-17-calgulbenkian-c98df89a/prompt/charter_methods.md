# Published Charter Methods (`publish_charter: methods only`)

repo_tag: none
repo_commit: 7aca3835635e5323b48cdf3b5b59fcde502cab28

## Thesis
Seeded by a random draw of two categories (`sky-archives`, `algorithms`) and three method cards (`far-import`, `representation`, `obstruction-first`), this charter pairs exact algebraic representation shifts with native multi-core C search and modular linear algebra. Rather than running generic black-box heuristics, we exploit exact linear/modular structure (nullspaces of tensor pairings, CSE straight-line program DAGs, isotropy orbits, and bit-parallel boolean/difference verification) where a multi-core machine can exhaust or optimize structured subspaces and certify results in exact integer or rational arithmetic.

## Lenses Used
1. **`representation-absorber` (Representation Change and Joint Nullspace Absorption)**:
   Recast the object in a linear-algebraic representation where hidden redundancies become nullspace vectors. In bilinear tensor decompositions, compute exact left nullspaces of all three factor pairings (`u(x)v`, `u(x)w`, `v(x)w`) modulo multiple 31-bit primes, lift via CRT, and solve for joint basis shifts that annihilate the maximum number of terms simultaneously (including multi-block hub terms and lookahead peel directions).
2. **`c-evaluator-optimizer` (Native C Evaluator First, Guided Combinatorial Search Second)**:
   Build a zero-dependency C engine (`cc -O3`) that evaluates candidate moves and verifies invariants at native hardware speed. Use exact modular representations to screen neighbourhood transitions and lookahead peels.

## Method Cards Used
- `far-import` (randomly drawn)
- `representation` (randomly drawn)
- `obstruction-first` (randomly drawn)
