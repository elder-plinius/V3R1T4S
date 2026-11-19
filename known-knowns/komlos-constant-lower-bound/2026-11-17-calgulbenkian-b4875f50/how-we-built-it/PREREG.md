# Pre-Registration: `komlos-constant-lower-bound`

frozen_utc: 2026-11-17T10:22:17Z
target_id: komlos-constant-lower-bound
null_test: required (1000 random unit-column Gaussian 15x15 matrices evaluated exhaustively over all 2^15 sign vectors)

## Verbatim Gates (Partial Win `p2`)

1. Explicit `m x n` matrix `A` (`n <= 15` nonzero columns) with exact rational entries `P_{ij} / D` and exact squared Euclidean norm `sum_i A_{ij}^2 <= 1` for every column `j = 1..n`.
2. Exhaustive exact arithmetic evaluation of `disc(A) = min_{x in {-1,1}^n} max_i |(A x)_i|` across all `2^n` sign vectors by two independent programs (Python `Fraction` branch-and-bound + Gray-code and C99 `__int128` Gray-code), certifying `disc(A) > 2006 / 1000 = 2.006`.
