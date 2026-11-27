# Pure-Kernel Lean 4.36.0 Binary Multi-Deletion Code Certification Suite

Standalone, zero-dependency Lean 4 (`v4.36.0`, no Mathlib) kernel-checked proof suite for binary `s`-deletion codes of length `n`.

## Scope and Limitations First

- **Inclusion-maximality is NOT global cardinality optimality.** The four `inclusion_maximal` theorems prove that every binary word in `{0,1}^n` outside the code `C` shares a length `n - s` subsequence with at least one codeword in `C` (equivalently, `C` cannot be extended to `|C| + 1` by adding a single word). They do **not** prove `M_s(n) <= |C|`.
- **Global optimality is proved only for the two small benchmark parameters** in `DeletionCode/DualLP.lean`: exact `M_2(7) = 5` and exact `M_3(9) = 5` via integer dual LP certificates. Global upper bounds for `(15,2)`, `(15,3)`, `(16,3)`, and `(16,2)` remain open.
- On `(16,2)`, the certified codebook has size `|C| = 219` (100% pure-scratch); the known public EinsteinArena `#34` record is `226`.

## Certified Theorems (`AuditAxioms.lean`)

All 13 headline theorems compile with **0 `sorryAx`**, **0 `native_decide`**, **0 `Lean.ofReduceBool`**, **0 `Lean.trustCompiler`**, and depend strictly on standard Lean 4 core axioms (a subset of `[propext, Classical.choice, Quot.sound]`):

| Theorem | Statement | Verified Domain |
| :--- | :--- | :--- |
| `DeletionCode.disjoint_delBall_iff_no_common_subseq` | `∀ n s ≤ n`, `D_s(x) ∩ D_s(y) = ∅ ↔ LCS(x, y) < n - s` | All `n, s ∈ ℕ`, `s ≤ n` |
| `DeletionCode.card_le_of_clique_cover` | General clique-cover / pigeonhole cardinality upper bound | All `n, s` |
| `DeletionCode.Cert_15_2.valid` & `.inclusion_maximal` | `(15, 2)` code of size **`137`** valid & non-extendable | All `32,768` words in `{0,1}^15` |
| `DeletionCode.Cert_15_3.valid` & `.inclusion_maximal` | `(15, 3)` code of size **`31`** valid & non-extendable | All `32,768` words in `{0,1}^15` |
| `DeletionCode.Cert_16_3.valid` & `.inclusion_maximal` | `(16, 3)` code of size **`44`** valid & non-extendable | All `65,536` words in `{0,1}^16` |
| `DeletionCode.Cert_16_2.valid` & `.inclusion_maximal` | `(16, 2)` pure-scratch code of size **`219`** valid & non-extendable | All `65,536` words in `{0,1}^16` |
| `DeletionCode.DualLP.exact_opt_7_2` | Exact global optimum `M_2(7) = 5` (weak LP duality `D=17, sum=98`) | All `128` words in `{0,1}^7` |
| `DeletionCode.DualLP.exact_opt_9_3` | Exact global optimum `M_3(9) = 5` (weak LP duality `D=4, sum=22`) | All `512` words in `{0,1}^9` |
| `DeletionCode.DualLP.cert_16_3_klein4_invariant` | `Cert_16_3.code` (`|C| = 44`) is invariant under bit-complement `c` and bit-reversal `r` (Klein-4 `<c, r>`) | `44` codewords in `{0,1}^16` |

## Independent Cold Verification

Run from `lean4_certs/`:

```bash
lake build DeletionCode
lake env lean AuditAxioms.lean
lake env leanchecker DeletionCode
```

Expected outputs:
- `lake build DeletionCode`: `216/216` build jobs pass, `0` errors.
- `lake env lean AuditAxioms.lean`: every theorem prints only a subset of `[propext, Classical.choice, Quot.sound]`.
- `lake env leanchecker DeletionCode`: exits with status `0`.
