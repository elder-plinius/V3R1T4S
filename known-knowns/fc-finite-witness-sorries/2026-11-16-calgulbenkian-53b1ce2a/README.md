# Lean 4 Kernel Proof of `RamseyNumbers.ramsey_number_six_six_lower_bound` (`R(6,6) >= 102`)

## What

A kernel-checked Lean 4 v4.33.1 proof, compiled standalone with `lake env lean` against a clean checkout of formal-conjectures at e028240a (whose RamseyNumbers.lean, lean-toolchain and lake-manifest.json are identical to live main f50ff7be), of the verbatim, research-solved, still-`sorry`, formal_proof-free theorem RamseyNumbers.ramsey_number_six_six_lower_bound with axioms exactly propext, Classical.choice and Quot.sound, with no open PR found proving or linking it (not a spliced in-tree `lake build`, and PR file lists not enumerated for all 798 open PRs).

## Check it yourself

From this package folder (with a clean `google-deepmind/formal-conjectures` Lake checkout at commit `e028240a61822d970c933f4656f51da025cf200b` and Mathlib cache):

```sh
FC_ROOT=/path/to/formal-conjectures sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in about 7 seconds on a laptop once the `formal-conjectures` Mathlib cache is downloaded).

## Compared to

- **Repository**: https://github.com/google-deepmind/formal-conjectures (`main` commit `e028240a61822d970c933f4656f51da025cf200b`)
- **File & theorem**: `FormalConjectures/Wikipedia/RamseyNumbers.lean`, `RamseyNumbers.ramsey_number_six_six_lower_bound` (`@[category research solved, AMS 5]`)
- **Upstream status**: `sorry` with no `formal_proof` attribute and `0` open pull requests proving or linking it
- **Source URL**: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/RamseyNumbers.lean (fetched `2026-11-15T15:07:07Z`, SHA-256 `36d0764d496b8a96b5dd9eaa804dfe4fccffbf8cb4744b9de146cfdaa9def43d`)

## Not claimed

- The mathematical lower bound `R(6,6) >= 102` via the 101-vertex Paley graph `P(101)` is classical (Kalbfleisch 1965); only the kernel-checked Lean 4 formalization of the `formal-conjectures` theorem is new.
- Upper bounds on `R(6,6)` and other open theorems in `RamseyNumbers.lean` are not claimed.

## Credits

- **J. G. Kalbfleisch** (1965, *Canad. Math. Bull.* 8, 575-584): classical `R(6,6) >= 102` lower bound via the 101-vertex Paley graph `P(101)`.
- **S. P. Radziszowski** (*Electronic Journal of Combinatorics*, Dynamic Survey DS1, *Small Ramsey Numbers*): survey reference cited in upstream `RamseyNumbers.lean`.
- **Google DeepMind Formal Conjectures authors** (<https://github.com/google-deepmind/formal-conjectures>): problem formalization and benchmark infrastructure.
- **Mathlib Community** (<https://github.com/leanprover-community/mathlib4>): `SimpleGraph` and `ZMod` foundations.
