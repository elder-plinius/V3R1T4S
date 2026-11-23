# Run It Yourself

## 1. Prepare Pinned `FLT` Checkout (Once)

```sh
git clone https://github.com/ImperialCollegeLondon/FLT.git
cd FLT
git checkout a3210204ad8876e851e32f73dd97d882bf1ccd0a
lake exe cache get
LEAN_NUM_THREADS=2 lake build
cd ..
```

## 2. Run the Standalone Checker

```sh
FLT_ROOT=./FLT sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`.

## 3. How to Rebuild / Inspect

Copy `object/CompactHausdorffRings.lean` over `FLT/FLT/Patching/Utils/CompactHausdorffRings.lean`, run `LEAN_NUM_THREADS=2 lake build`, and run `#print axioms Group.subsingleton_of_pow_prime_eq_one`.
