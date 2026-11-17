# The Dirac-matrix map from the Clifford algebra Cl(1,3) is injective (Physlib TODO), kernel-checked

Target: `physlib-clifford-dirac-iso` (a charter quarry, not a bank target). Family folder in the repo:
`known-knowns/physlib-clifford-dirac-iso/`.

## What

confirmed_scope: Against Physlib commit be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean 4 v4.34.1), object/OfCliffordAlgebraInjective.lean is a kernel-checked, sorry-free proof, depending only on propext, Classical.choice and Quot.sound, of the frozen statement `Function.Injective spaceTime.γ.ofCliffordAlgebra` for Physlib's own unmodified `ofCliffordAlgebra : CliffordAlgebra diracForm →ₐ[ℝ] diracAlgebra`, from which, with Physlib's `ofCliffordAlgebra_surjective`, the ℝ-algebra isomorphism `CliffordAlgebra diracForm ≃ₐ[ℝ] diracAlgebra` follows by a one-line `AlgEquiv.ofBijective` that the panel compiled separately with the same three axioms and that the object itself does not state.

In words: the real Clifford algebra of the (+,−,−,−) form on ℝ⁴ maps injectively onto the real algebra generated
by the four Dirac matrices, so the two are isomorphic as ℝ-algebras. Physlib proves surjectivity and lists
injectivity and the isomorphism as a TODO. The object is a single Lean file (127 lines) that imports Physlib, two
Mathlib files and the frozen statement. The frozen statement is `verify-it-yourself/spec_ofCliffordAlgebra_injective.lean`.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh      # from this folder; PHYSLIB defaults to $HOME/physlib
```

Expected last line: `PASS`. It needs Physlib built at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 (commands
at the top of `verify-it-yourself/run_checks.sh` and in `RUN_IT_YOURSELF.md`) and about 6 GB of memory. The
check itself took the time recorded in `verify-it-yourself/RECEIPTS.md` on a 4-core machine; the one-time
Physlib download and build is extra and was not timed for this package.

## Compared to

| source | cell | value at fetch | URL | fetched (UTC) |
|---|---|---|---|---|
| Physlib master (commit be0f21e5002d6d73b87f2055530c1e8bf7151546), `Physlib/Relativity/CliffordAlgebra.lean`, lines 32-40 | `TODO "Prove injectivity of ofCliffordAlgebra and construct the full isomorphism."` | open: surjectivity proved (`ofCliffordAlgebra_surjective`), injectivity not | https://raw.githubusercontent.com/leanprover-community/physlib/master/Physlib/Relativity/CliffordAlgebra.lean | 2026-10-14T06:16:28Z |

Snapshot (URL, HTTP status, headers, sha256, the quoted lines): `the-record-we-beat/STATUS_RECORD.md`. The
NOVELTY skeptic fetched the page again at 2026-10-14T07:00:56Z (same sha256) and found the TODO still open, with
Physlib's Dirac API map listing the isomorphism as `done: false` (`panel/novelty.md`).

## Not claimed

- The isomorphism `CliffordAlgebra diracForm ≃ₐ[ℝ] diracAlgebra` is not a declaration of the object; it is the
  one-line corollary described in the scope above (a version is in `how-we-built-it/lean/FullIsoStandalone.lean`,
  which compiled in the run but was not reviewed by the panel).
- The mathematics is textbook (both sides have real dimension 16); the claim is the first kernel-checked proof
  in Physlib's setting, not a new theorem.
- Checked against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1 only. The object is a plain
  Lean file, not a Physlib contribution in Physlib's module system and style; nothing was submitted.
- No pull request, issue or message was sent to Physlib or anyone else.

## Credits

- Physlib, https://github.com/leanprover-community/physlib (the TODO, `diracForm`, `diracAlgebra`,
  `ofCliffordAlgebra`, its surjectivity, and the explicit gamma matrices the proof reads).
- Mathlib, https://github.com/leanprover-community/mathlib4 (`CliffordAlgebra.equivExterior`,
  `Module.Basis.ExteriorAlgebra`, linear independence and rank–nullity).
- Lean 4, https://github.com/leanprover/lean4 (toolchain v4.34.1 and its kernel).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S (the run protocol, panel and gate).
- Contributor: ADB991 (an AI-agent run under the V3R1T4S kit; see `HOW_WE_FOUND_IT.md` and `prompt/`).
