# Lean 4 Kernel Proof of the Brownian Motion Reflection Principle (`IsBrownianReal.reflection`)

## What

On brownian-motion master 8fd8dc5 as re-fetched today, with no open PR on BrownianMotion/Gaussian/IteratedLogarithm.lean and no issue claiming it, the claimed file replaces the sorry of IsBrownianReal.reflection with a proof, keeps its statement unchanged, and depends only on propext, Classical.choice and Quot.sound (the unrelated IsStandardGaussian.tail sorry in the same file remains, as the criterion permits).

## Check it yourself

From this package folder (with a clean `RemyDegenne/brownian-motion` checkout at commit `8fd8dc52830cdd07cf9cc8eadd533e284425fa6f` and Mathlib cache):

```sh
BROWNIAN_MOTION_ROOT=./brownian-motion sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs in about 15 seconds on a laptop once the `brownian-motion` Mathlib cache is downloaded).

## Compared to

- **Repository**: https://github.com/RemyDegenne/brownian-motion (`master` commit `8fd8dc52830cdd07cf9cc8eadd533e284425fa6f`)
- **Declaration**: `ProbabilityTheory.IsBrownianReal.reflection` in `BrownianMotion/Gaussian/IteratedLogarithm.lean`
- **Upstream status**: `:= sorry -- needs strong Markov property` (`0` open PRs touching `IteratedLogarithm.lean`, `0` issues claiming `reflection`)
- **Fetched**: `2026-11-16T16:53:22Z` (`HTTP 200`, SHA-256 `c5a08861fdcc0f8c122c62efd8c0293c859d5f655f9a9635ebfbcdcde3aa5b44`)

## Not claimed

- Desire Andre's and Paul Levy's reflection principle for Brownian motion is a classic theorem in probability theory; only the sorry-free Lean 4 formalization in `RemyDegenne/brownian-motion` is claimed.
- The misstated declaration `IsStandardGaussian.tail` later in `IteratedLogarithm.lean` is intentionally left untouched as required by the target specification.

## Credits

- **Remy Degenne**, **Joris van Winden** (author of `BrownianMotion/Gaussian/IteratedLogarithm.lean`), and contributors to `RemyDegenne/brownian-motion` (https://github.com/RemyDegenne/brownian-motion, https://remydegenne.github.io/brownian-motion/blueprint/).
- **Mathlib Community** (https://github.com/leanprover-community/mathlib4): Gaussian measure and `IsBrownianReal` foundations.
