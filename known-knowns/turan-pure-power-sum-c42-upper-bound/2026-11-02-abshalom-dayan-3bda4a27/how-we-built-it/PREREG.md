# Pre-registration (written 2026-10-31T20:44:28Z, before any attack output)

Criterion: verbatim in target.md. Bar read from command output in scout.md: 0.6863607950 (open PR #305).

Statistic and thresholds, frozen:
- Route (i): exact rational T and a rational profile in Theorem A of Bakeas (or a new reduction with a full written proof), with U <= 0.6863607850, certified F_upper < U by two independently written checkers, one using exact rationals where the expression is rational and one Arb at >= 384 bits, each with strictly positive margin. A floating optimum is never a result.
- Route (ii): complete written proof of R_n >= L for all large n (or limsup), with L > 1/2 stated as an exact rational, every numerical step interval-certified by two independently written checkers, the proof not being an evaluation of Biro's constant from Indag. Math. 11 (2000) 343-358.
- Every lemma is tested on small cases by exact computation (Fractions/Arb) before it is relied on.
- Anything short of that is reported as what it is, at most PROMISING. No partial-win package (human's steer, 2026-10-31).

null_test: not needed because any claim is an explicit object or proof checked by a deterministic checker against a table value, not a search or statistical claim.
