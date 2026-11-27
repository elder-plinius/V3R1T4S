# Lean 4 proof of the bound

This folder is a Lean 4 project (Lean v4.36.0, Mathlib v4.36.0) that machine-checks the result of this package:

```lean
structure IsOddCovering (S : Finset (ℤ × ℕ)) : Prop where
  odd : ∀ c ∈ S, Odd c.2
  one_lt : ∀ c ∈ S, 1 < c.2
  distinct : ∀ c ∈ S, ∀ c' ∈ S, c.2 = c'.2 → c = c'
  covers : ∀ x : ℤ, ∃ c ∈ S, (c.2 : ℤ) ∣ x - c.1

def lcmModuli (S : Finset (ℤ × ℕ)) : ℕ := S.lcm (fun c => c.2)

def MainStatement : Prop :=
  ∀ S : Finset (ℤ × ℕ), IsOddCovering S → 168131152814625 ≤ lcmModuli S

theorem odd_covering_lcm_lower_bound : MainStatement
```

A pair `(a, n)` is the residue class a + nℤ. The whole statement is in `Erdos7/Statement.lean` (32 lines), written so that it can be audited by hand. The theorem is proved at `Erdos7/Main.lean`, line 212.

## Build and check

```sh
cd lean
lake exe cache get      # Mathlib's prebuilt cache
lake build              # about 80 s wall on a recent machine, after the cache
```

The build prints `#print axioms` for the main theorem and the stage lemmas (`Erdos7/Sanity.lean`). The main theorem depends only on `propext`, `Classical.choice` and `Quot.sound`. The project has no `sorry`, no `native_decide` and no `axiom` declarations. The certificate table is checked by `decide +kernel`, which is kernel reduction.

## What is formalised

1. **Statement** (`Statement.lean`): the definitions above.
2. **Certificates** (`Checker.lean`, `Cert/Chunk00.lean` to `Cert/Chunk29.lean`, `Cert/Table.lean`): all 7,036 band profiles of `object/lcm_lower_bound_certificate.tsv` and the pure-deletion profiles. Each profile's exact rational bound is checked to be below 1, and `check_sound` proves that a passing check means exactly that. A kernel-checked count confirms 2,519 pure-deletion and 4,517 capped profiles.
3. **Completeness of the enumeration** (`Enum.lean`, `EnumSigma.lean`, `Abundance.lean`): every abundant profile in the band is in the table, and the table contains no other profile. This is proved by a search the kernel evaluates. A separate theorem shows that the product used for abundance is the true sum of divisors.
4. **Lemmas** (`Convex.lean`, `Kernels.lean`, `Fibre.lean`, `Sequential.lean`, `Replacement.lean`, `Box.lean`, `Main.lean`): the nested convex comparison (Lemma 5), the capped kernels (Lemma 4(2)), pure deletion (Lemma 4(1)) and prime replacement (Lemma 1), joined into the final theorem. The formal route differs from the prose in two ways:
   - Lemmas 1 and 2 are combined into one digit map, and the 3^k scaling is done with extra digits on the prime 3.
   - The family is never modified (the prose's Lemma 3); only the size of its pure part is bounded.
   The conditions `C_i > 1` and `δ_i ≥ ρ_i` are checked for every capped coordinate.

`scripts/gen_cert.py` regenerates the certificate chunks from the package's TSV:
`python3 scripts/gen_cert.py ../object/lcm_lower_bound_certificate.tsv Erdos7/Cert`. `scripts/count.py` recounts the profile classes.

## Known tooling note

`leanchecker`, Lean's separate kernel replay tool, passes on each of the 47 modules run one at a time. It exits with code 139 and no message when it is run on all modules in one process. The ordinary build already kernel-checks every declaration, so this does not affect the proof.
