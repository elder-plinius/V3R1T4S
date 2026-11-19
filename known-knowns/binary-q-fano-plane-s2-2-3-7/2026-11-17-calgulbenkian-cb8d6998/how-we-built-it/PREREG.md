# Pre-Registration: `binary-q-fano-plane-s2-2-3-7`

frozen_utc: 2026-11-17T10:21:42Z
target_id: binary-q-fano-plane-s2-2-3-7
null_test: not needed because exact finite projective subspace configuration in PG(6, 2) verified exhaustively

## Verbatim Gates (Partial Win `p2`)

1. Explicit `7x7` binary matrix `pi` in `GL(7, 2)` of multiplicative order `5`, fixing a 3-dimensional subspace `F` (`7` projective points).
2. Explicit list of `240` distinct rank-`3` binary `3x7` reduced row echelon form generator matrices invariant as a set under `pi`, every plane satisfying `U cap F = {0}`, no two planes meeting in a line (`<= 1` coverage across all `2,667` lines of `PG(6, 2)`), and every one of the `120` projective points outside `F` covered `14` times (`240 * 7 = 1680 = 120 * 14`), verified independently in Python 3 stdlib and C99.
