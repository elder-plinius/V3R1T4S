# Run It Yourself

## 1. Prepare Pinned `brownian-motion` Checkout (Once)

```sh
git clone https://github.com/RemyDegenne/brownian-motion.git
cd brownian-motion
git checkout 8fd8dc52830cdd07cf9cc8eadd533e284425fa6f
lake exe cache get
LEAN_NUM_THREADS=2 lake build
cd ..
```

## 2. Run the Standalone Checker

```sh
BROWNIAN_MOTION_ROOT=./brownian-motion sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`.

## 3. How to Rebuild / Inspect

Copy `object/IteratedLogarithm.lean` over `brownian-motion/BrownianMotion/Gaussian/IteratedLogarithm.lean`, run `LEAN_NUM_THREADS=2 lake build`, and run `#print axioms ProbabilityTheory.IsBrownianReal.reflection`.
