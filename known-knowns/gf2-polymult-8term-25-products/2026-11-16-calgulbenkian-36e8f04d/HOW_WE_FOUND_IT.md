# How We Found It

_Note: contributor text, unverified._

1. **Flip-graph rank-25 / rank-32 study (`flip-graph-rank25`)**: Tensor flip-graph walks on `8 x 8` binary polynomial multiplication confirmed the `k = 25` island barrier, while showing that asymmetric Karatsuba-Schoolbook splits on `m = 7` interact strongly with trinomial modular reduction.
2. **Asymmetric `(3 + 4)` split + depth-bounded linear synthesis (`algebraic-bilinear-slp`)**: Reversing the split orientation from `(4 + 3)` (whose reduced `7 x 32` matrix modulo `x^7 + x^3 + 1` has `65` ones and layered floor `82`) to `(3 + 4)` (`3 x 3` schoolbook on unreduced low degrees `0..2`, `4 x 4` Karatsuba on reduced high degrees `3..6`) collapses the reduced `7 x 32` matrix to `57` ones (`10` multi-bit columns, layered floor `81`), synthesized at exact zero-slack floor **`81` gates** (`14` pre-XORs + `32` ANDs + `35` post-XORs, depth `6`).
