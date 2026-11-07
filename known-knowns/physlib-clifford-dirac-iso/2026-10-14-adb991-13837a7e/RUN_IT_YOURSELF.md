# Run it yourself

All commands run in a fresh shell from this package folder. You need git, Python 3 (standard library only), and
Lean through elan (https://github.com/leanprover/elan); elan installs the toolchain Physlib names
(`leanprover/lean4:v4.34.1`) on first use.

## 1. Physlib at the claim's commit (one time)

```sh
git clone https://github.com/leanprover-community/physlib "$HOME/physlib"
git -C "$HOME/physlib" checkout be0f21e5002d6d73b87f2055530c1e8bf7151546
(cd "$HOME/physlib" && lake exe get_cache && lake build)
```

`lake exe get_cache` downloads prebuilt Mathlib files; `lake build` then builds Physlib. The finished checkout took
8.4 GB of disk on the contributor's machine (`du -sh`). Put Physlib elsewhere by setting `PHYSLIB=/path/to/physlib`.

## 2. The check

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (the real one, with timings, is in `verify-it-yourself/RECEIPTS.md`):

```
physlib commit: be0f21e5002d6d73b87f2055530c1e8bf7151546
object sha256: 13837a7e226a97b9fef5bd04d6f362c0db869627cfa3a7239d4f54343cde5c8b
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

What it does: `verify-it-yourself/lean_claim_check.py` compiles the frozen statement
`verify-it-yourself/spec_ofCliffordAlgebra_injective.lean` as its own module first (so the object cannot change
its meaning), then the object `object/OfCliffordAlgebraInjective.lean`, then a fresh file containing
`theorem V3R1T4S_check : V3R1T4S.spec := V3R1T4S.claim` and `#print axioms V3R1T4S_check`. PASS needs no errors,
no `sorry`, a source policy with no axioms, instances, attributes, notation or meta code in the object, and only
the axioms propext, Classical.choice and Quot.sound.

## 3. Rebuilding the object

The object is a hand-written Lean proof; nothing generates it, and step 2 compiles it from source. The exact
numerical check that preceded it runs with `python3 how-we-built-it/code/numcheck.py` (standard library only).
