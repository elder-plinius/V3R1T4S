# Run It Yourself

## 1. Prepare Pinned `formal-conjectures` Checkout (Once)

```sh
git clone https://github.com/google-deepmind/formal-conjectures.git
cd formal-conjectures
git checkout e028240a61822d970c933f4656f51da025cf200b
lake exe cache get
lake build FormalConjecturesUtil FormalConjectures.Wikipedia.RamseyNumbers
cd ..
```

## 2. Run the Standalone Checker

From this package directory:

```sh
FC_ROOT=./formal-conjectures sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
[1/5] Manifest & object integrity verified: sha256=53b1ce2a8a0e258b3fed499681bbb63ce796625b6bd2f38e093340f483a55275 (17579 bytes)
[2/5] Forbidden-token & import hygiene audit passed (0 forbidden tokens)
[3/5] Upstream pinned environment & verbatim statement match verified (commit=e028240a6182, toolchain=leanprover/lean4:v4.33.1)
[4/5] Lean 4 kernel & FC linter build succeeded (exit=0, warnings=0)
[5/5] Axiom audit passed: 'RamseyNumbers.ramsey_number_six_six_lower_bound' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
PASS
```

## 3. Rebuild Witness Parameters

```sh
python3 how-we-built-it/gen_witnesses.py
```
