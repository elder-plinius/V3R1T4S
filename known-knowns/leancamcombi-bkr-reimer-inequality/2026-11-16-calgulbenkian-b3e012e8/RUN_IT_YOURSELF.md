# Run It Yourself

## 1. Prepare Pinned `LeanCamCombi` Checkout (Once)

```sh
git clone https://github.com/YaelDillies/LeanCamCombi.git
cd LeanCamCombi
git checkout 0a42535119073f677dd60a28acbbdcda11b87f60
lake exe cache get
lake build CamCombi.PlainCombi.VanDenBergKesten
cd ..
```

## 2. Run the Standalone Checker

From this package directory:

```sh
LEANCAMCOMBI_ROOT=./LeanCamCombi sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
[1/5] Manifest & object integrity verified: sha256=b3e012e83c4ef62cb15af4da57291f28795c40447c4696345a8bb07199f4f4d8 (47641 bytes)
[2/5] Forbidden-token & public-import hygiene audit passed (0 forbidden tokens)
[3/5] Upstream pinned environment & verbatim diff verified (commit=0a4253511907, toolchain=leanprover/lean4:v4.36.0-rc2)
[4/5] Lean 4 kernel & mathlibStandardSet linter build succeeded (exit=0, warnings=0)
[5/5] Axiom audit passed: 'Finset.card_certificator_le' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
PASS
```

## 3. Optional Full-Library Build Check

Copy `object/VanDenBergKesten.lean` over `LeanCamCombi/CamCombi/PlainCombi/VanDenBergKesten.lean` and run `lake build` (`6699` jobs, `0` warnings).
