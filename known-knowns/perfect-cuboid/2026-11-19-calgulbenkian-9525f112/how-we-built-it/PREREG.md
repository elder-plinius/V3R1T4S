# Preregistration: `perfect-cuboid` (`p1`, v2)

- frozen_utc: 2026-11-19T04:24:20Z
- target_id: perfect-cuboid
- target_cell: partial_win p1 (explicit infinite excluded family beyond arXiv:2604.28072)
- null_test: not needed because the target is a deterministic mathematical proof of non-existence on two explicit infinite two-parameter fibrations checked by formal Lean 4 kernel verification and standalone ISO C99 and Python 3 verifiers.

## Verbatim criterion from `repo/bank/targets.json`
- `success_criterion`: "CONFIRMED only for explicit positive integers a, b, c with a^2+b^2, b^2+c^2, a^2+c^2 and a^2+b^2+c^2 all perfect squares (math.isqrt check), or for a non-existence proof formalized in Lean without sorry and with a clean axiom audit. Body/face/edge cuboids (one diagonal irrational) never count."
- `p1`: "New excluded family: a rigorous non-existence proof for an explicit infinite family not covered by arXiv 2604.28072's 1,072 fibers (e.g. fibers with parameter ≥ 100, or a whole elliptic fibration of the de Grey-Gibbs-Helm reformulation), with every rank/descent computation rerunnable by the verifier in PARI or Magma and the written argument checked line by line (Lean preferred)."

## Exact acceptance gate frozen before v2 build
1. **Novelty & Complete Historical Attribution:** Excludes both open two-parameter internal-ratio edge-cuboid fibrations (constructed by Ronald van Luijk, 2000, pp. 4–5, and parametrized with open non-existence question posed by Aubrey de Grey, Philip Gibbs, and Louie Helm, 2024, `arXiv:2401.06784`, Sections 7.4 and 10.2), with unconditional infinitude of positive edge cuboids at unbounded parameters `≥ 100`.
2. **Core Lean 4 Formalization:** Compiles in Core Lean 4 (`v4.35.0`) with zero external imports, zero unproved placeholders or compiler-trusted reflection tactics, and all `12` `#print axioms` blocks strictly inside `{propext, Classical.choice, Quot.sound}`.
3. **Standalone C99 & Python Verifiers:** Both `verify_c99.c` (clean under `-std=c99 -O2 -g -Wall -Wextra -Werror -Wpedantic -fsanitize=address,undefined`) and `verify_py.py` (pure Python 3 stdlib) check the certificate fields and hashes and all polynomial identities, and `verify_py.py` also runs the 500-fiber `math.isqrt` search and the forbidden-token scan of the Lean file. The proof itself uses no rank or descent computation; it is the self-contained Lean file.
