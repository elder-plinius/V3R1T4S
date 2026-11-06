# Equational Theories Project (`etp-finite-magma-677-255`): Conditional Implication Proof & Two-Sided Separation (`p2`)

## What
Sorry-free Lean 4 proof in the Equational Theories Project (Equation677.lean, importing equational_theories.Equations.All and equational_theories.ManuallyProved.Equation677, standard axioms propext, Classical.choice, and Quot.sound only) establishing Equation677 => Equation255 on finite magmas under the natural fixed-point hypothesis EveryLeftMulHasFixedPoint (eq255_of_eq677_leftMul_has_fixed_point), together with formal finite separation counterexamples (Sep7 of order 7, Sep25 of order 25, and Sep55 of order 55) proved by decide showing EveryLeftMulHasFixedPoint is neither implied by nor equivalent to the translation-conjugacy closure condition (LeftMulConjugacyClosed) of ETP Issue #1517 (nor implied by or equivalent to RightCancellative), alongside additional conditional implication theorems under RightCancellative, IsQuasigroup, and UniformLeftMul (proved non-equivalent to LeftMulConjugacyClosed by Sep25) and dual Equation2910 => Equation47 theorems.

The fixed-point theorem is the new part of this partial result. The right-cancellative, quasigroup, and uniform-left-translation theorems formalize the reduction in Blueprint Chapter 13: surjectivity of every right translation gives Equation255. On finite Equation677 magmas, these three hypotheses are equivalent.

`LeftMulConjugacyClosed` uses `L_a⁻¹ L_b L_a`, while [ETP issue #1517](https://github.com/teorth/equational_theories/issues/1517) uses `L_a L_b L_a⁻¹`. These conditions agree here: Equation677 makes every left translation bijective, and conjugation by `L_a` injects the finite set of left translations into itself. An inclusion in either direction is therefore an equality, which gives the other direction.

**Correction (2026-11-02):** The original package carried incorrect SHA-256 values for two pinned upstream files in `panel/novelty.md`. They were corrected in place after review. At ETP commit `2f49bdaf3d38ffb722e54ac1288c8269dac61846`, `equational_theories/ManuallyProved/Equation677.lean` hashes to `dc1050b709dfe6c5ce33b9c2afa264dd70041308356df4045739061942ebbf3f` and `blueprint/src/chapter/677.tex` hashes to `e25f4c8e3ecfe454ad303782b68af69e41eb0572f780c5a7203cc8210b4b152e`. The panel reports now use package-relative artifact paths; their verdicts concern the original proof and models, whose definitions and proofs are unchanged. The package directory name retains its original object-hash suffix for PR continuity; the current object hash is recorded in `INDEX.csv` and `SHA256SUMS`.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: PASS. The standalone Python check runs in under 2 seconds on a laptop. Full Lean 4.29.1 kernel compilation is described in RUN_IT_YOURSELF.md and depends on a prepared ETP checkout. The standalone checker rejects a corrupted copy of object/ with FAIL.

## Compared to
- Primary status dashboard: Equational Theories Project live dashboard, `https://teorth.github.io/equational_theories/dashboard/` (fetched `2026-11-02T19:55:52Z`, HTTP `200`, SHA-256 `5afe452a033cc43c692c30f0fdcf8d50166e3cba240d7a005bb5e63c7ec2d90d`) and finite outcomes matrix `https://teorth.github.io/equational_theories/raw_data/finite_outcomes.json.gz` (fetched `2026-11-02T19:55:56Z`, HTTP `200`, SHA-256 `e9c6bcc5031f0d329fc75075f23513364925361515c80ba0498630bad73463e4`; parsed `4694 x 4694` matrix still shows exactly the 2 unknown cells).
- Cell / status: `(676, 254)` (`Equation677 => Equation255`) is `"unknown"` on finite magmas (one of the last 2 unknown implications out of `4694 x 4694 = 22,033,636`).
- Upstream formalization compared against: `equational_theories/ManuallyProved/Equation677.lean` at commit `2f49bdaf3d38ffb722e54ac1288c8269dac61846` (SHA-256 `dc1050b709dfe6c5ce33b9c2afa264dd70041308356df4045739061942ebbf3f`, 108 lines, containing only basic Blueprint Lemmas 13.1–13.2 and zero conditional implication theorems) and ETP Issue #1517 / PR #1518 (`LeftMulConjugacyClosed`).

## Not claimed
- Does not settle the unconditional implications `Equation677 => Equation255` or `Equation2910 => Equation47` on arbitrary finite magmas (where right-cancellativity, left-translation fixed points, and translation-conjugacy closure may simultaneously fail).
- For `RightCancellative`, `IsQuasigroup`, and `UniformLeftMul` (and dual `LeftCancellative`), `Sep25` proves they do not imply and are not equivalent to `LeftMulConjugacyClosed`, whereas whether `LeftMulConjugacyClosed` implies `RightCancellative` on finite `Equation677` magmas remains open; the full two-sided separation (`neither implied by nor equivalent to` `LeftMulConjugacyClosed`) is claimed for `EveryLeftMulHasFixedPoint`. (`UniformLeftMul`'s separation goes via its proved equivalence with `RightCancellative` on finite 677-magmas — `eq677_right_cancel_of_uniform_leftMul` plus the trivial converse — rather than a direct `Sep25` instance check.)
- Does not claim exhaustive SAT/DRAT counterexample exclusion at order `n >= 11` (`p1`).

## Credits
- Terence Tao and the Equational Theories Project contributors (`https://github.com/teorth/equational_theories`, Blueprint Chapter 13 `blueprint/src/chapter/677.tex`, and `equational_theories/ManuallyProved/Equation677.lean`)
- ETP Issue #1464 and Issue #1517 / PR #1518 contributors
- The V3R1T4S open research kit (`https://github.com/elder-plinius/V3R1T4S`)
- Contributed by RainRat.
