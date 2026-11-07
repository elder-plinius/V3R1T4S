# Run it yourself

All commands run in a fresh shell from this package folder. You need git, Python 3 (standard library only), and
Lean through elan (https://github.com/leanprover/elan); elan installs the toolchain Physlib names
(`leanprover/lean4:v4.34.1`) on first use.

## 1. Physlib at the checked commit (one time)

```sh
git clone https://github.com/leanprover-community/physlib "$HOME/physlib"
git -C "$HOME/physlib" checkout 76245c854e4827a1dd7f20d1c053b61219cc8fbb
(cd "$HOME/physlib" && lake exe get_cache && lake build)
```

`lake exe get_cache` downloads prebuilt Mathlib files; `lake build` then builds Physlib. Put Physlib elsewhere by
setting `PHYSLIB=/path/to/physlib`.

## 2. The check

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (the real one, with timings, is in `verify-it-yourself/RECEIPTS.md`): the Physlib commit, the object's
sha256, `spec compile: exit 0`, `candidate compile: exit 0`, `check file: exit 0`,
`'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]`, and last line `PASS`.

What it does: `verify-it-yourself/lean_claim_check.py` compiles the frozen statement
`verify-it-yourself/spec_patisalam_inclSM_ker.lean` as its own module first (so the object cannot change its
meaning), then the object `object/PatiSalamInclSMKer.lean`, then a fresh file containing
`theorem V3R1T4S_check : V3R1T4S.spec := V3R1T4S.claim` and `#print axioms V3R1T4S_check`. PASS needs no errors,
no `sorry`, a source policy with no axioms, instances, attributes, notation or meta code in the object, and only
the axioms propext, Classical.choice and Quot.sound.

## 3. Rebuilding the object

The object is a hand-written Lean proof; nothing generates it, and step 2 compiles it from source. The numerical
check that preceded it runs with `python3 how-we-built-it/code/numeric_check.py` (needs numpy; its output in the run
is `how-we-built-it/out/numeric_check.txt`).
