# Lean 4 Kernel & Comparator Proof of `ZetaHadamard.v1` (`logDeriv_partial_fractions`) in `teorth/IEANTN`

## What

As of live main d60421f, the Lake project Solutions/ZetaHadamard.v1 (the node's only conclusion, unconditional, no declared imports) passes Comparator 10dd2b33 with lean4export cacf989b on the Lean kernel using only propext, Classical.choice and Quot.sound, run with the fake sandbox and with the NanoDa replay not run here, and the node had no solution, receipt, claim or open PR when fetched.

## Check it yourself

From this package folder (with `teorth/IEANTN` checked out at `d60421f10c16f5f6c2cb75f1067a72e24e616391` and `leanprover/comparator` built, auto-discovered or passed via `IEANTN_ROOT` and `COMPARATOR_TOOLS_ROOT`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs `LEAN_NUM_THREADS=2 lake build`, `leanprover/comparator`, and `#print axioms`, restoring `IEANTN` git-clean).

## Compared to

| Source | Node / Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| `teorth/IEANTN` `STATE.md` (`d60421f10c16`) | `ZetaHadamard.v1` (`logDeriv_partial_fractions`) | `active`, `Evidence = literature`, `Imports = 0`, `Issue = -` | https://raw.githubusercontent.com/teorth/IEANTN/main/STATE.md | 2026-11-15T18:38:17Z |
| `teorth/IEANTN` `Solutions/` (`d60421f10c16`) | `Solutions/ZetaHadamard.v1` | Absent (`22` sibling directories) | https://api.github.com/repos/teorth/IEANTN/contents/Solutions?ref=main | 2026-11-15T18:38:18Z |
| `teorth/IEANTN` Issues & PRs | `ZetaHadamard.v1` | `0` open issues, `0` open/closed solution PRs | https://api.github.com/repos/teorth/IEANTN/pulls?state=open&per_page=100 | 2026-11-15T18:38:20Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Resolves the single-conclusion node `ZetaHadamard.v1` (`logDeriv_partial_fractions`) on `teorth/IEANTN` `main` (`d60421f10c16f5f6c2cb75f1067a72e24e616391`) with no PR opened; does not claim solutions for other open `IEANTN` nodes.

## Credits

- **Jacques Hadamard** (1893), **Harold Davenport** (*Multiplicative Number Theory*, 3rd ed., §12, 2000), and **Hugh L. Montgomery & Robert C. Vaughan** (*Multiplicative Number Theory I*, Corollary 10.14, 2007): classical analytic theory of the partial-fraction expansion of `ζ'(s)/ζ(s)`.
- **Terence Tao and `teorth/IEANTN` contributors** (https://github.com/teorth/IEANTN; Apache-2.0): `IEANTN` architecture, `ZetaHadamard.v1` problem specification (PR `#108`), and the sibling infrastructure modules vendored per `docs/SOLUTIONS.md` Lake isolation convention (`Solutions/GammaAsymptotics.v2/{Analytic,ComplexToReal,GaussSeries,Oscillation,Periodic,RealAsymptotic,RealIdentity,Recurrence,Strip}.lean`, `Solutions/CH2.v1/{RectanglePort,ResiduePort,ZetaConjPort,ZetaInstance}.lean` originally extracted from `CH2.lean` in `AlexKontorovich/PrimeNumberTheoremAnd`, and `Solutions/ZetaLogDeriv.v1/Solution.lean` adapted in `ZetaZerosBasic.lean`), on top of which our `158,071` bytes of new proof (`DigammaTrivial.lean`, `ZetaGrowth.lean`, `LocalZeros.lean`, `Solution.lean`) build the full all-plane `ZetaHadamard.v1` proof.
- **Alex Kontorovich, Terence Tao, Matteo Cipollina, and `PrimeNumberTheoremAnd` / `AxiomMath/ZetaZerosV2` contributors** (https://github.com/AlexKontorovich/PrimeNumberTheoremAnd PR `#1504`; https://github.com/AxiomMath/ZetaZerosV2): related external Lean 4 developments on `ξ(s)` Hadamard products and right-half-plane Landau formulas.
- **`leanprover-community/mathlib4` and `leanprover/comparator`**: Mathlib complex-analysis/Jensen/Borel–Carathéodory libraries and kernel-level solution comparator.
