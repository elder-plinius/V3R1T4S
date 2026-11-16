# Lean 4 Kernel Proof of `WrittenOnTheWallII.GraphConjecture25.conjecture25`

## What

The file object/Solution.lean, compiled against a clean checkout of formal-conjectures at e028240a (whose target file, lean-toolchain and lake-manifest are byte-identical to live main on 2026-11-15), proves the unaltered universe-polymorphic statement WrittenOnTheWallII.GraphConjecture25.conjecture25 (a research solved item that was a sorry, with no formal_proof and no open PR proving or linking it) with only propext, Classical.choice and Quot.sound and no forbidden tokens.

## Check it yourself

From this package folder (with a clean `google-deepmind/formal-conjectures` Lake checkout at commit `e028240a61822d970c933f4656f51da025cf200b` and Mathlib cache):

```sh
FC_ROOT=/path/to/formal-conjectures sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in about 6 seconds on a laptop once the `formal-conjectures` Mathlib cache is downloaded).

## Compared to

- **Repository**: https://github.com/google-deepmind/formal-conjectures (`main` commit `e028240a61822d970c933f4656f51da025cf200b`)
- **File & theorem**: `FormalConjectures/WrittenOnTheWallII/GraphConjecture25.lean`, `WrittenOnTheWallII.GraphConjecture25.conjecture25` (`@[category research solved, AMS 5]`)
- **Upstream status**: `sorry` with no `formal_proof` attribute and `0` open pull requests proving or linking it
- **Source URL**: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/WrittenOnTheWallII/GraphConjecture25.lean (fetched `2026-11-15T15:07:08Z`, SHA-256 `4e107c778baacb7178f63608f320a5dd047d8c868face022f9612394ff57298c`)

## Not claimed

- Conjecture 25 of Graffiti.pc was already known in the graph-theory literature to be false (status `F` in DeLaViña's *Written on the Wall II*); only the universe-polymorphic Lean 4 kernel proof in `formal-conjectures` is claimed.
- Other open items in `WrittenOnTheWallII/` are not claimed in this package.

## Credits

- **E. DeLaViña** (*Written on the Wall II: Conjectures of Graffiti.pc*): source collection for Graffiti.pc Conjecture 25.
- **S. Fajtlowicz** (Graffiti / Graffiti.pc): conjecture generation program.
- **Google DeepMind Formal Conjectures authors** (<https://github.com/google-deepmind/formal-conjectures>): Lean 4 problem statement (`GraphConjecture25.lean`).
- **Mathlib Community** (<https://github.com/leanprover-community/mathlib4>): `SimpleGraph` metric and induced-subgraph libraries.
