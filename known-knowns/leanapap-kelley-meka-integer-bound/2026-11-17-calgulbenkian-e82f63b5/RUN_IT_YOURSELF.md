# Run It Yourself

## 1. Prepare Pinned `LeanAPAP` Checkout (Once)

```sh
git clone https://github.com/YaelDillies/LeanAPAP.git
cd LeanAPAP
git checkout fb5cb9c4f594cbeeb160c715618d13640984c521
lake exe cache get
LEAN_NUM_THREADS=2 lake build
cd ..
```

## 2. Run the Standalone 5-Gate Referee

```sh
LEANAPAP_ROOT=./LeanAPAP sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`.

## 3. Manual Inspection

Stage `object/Regular.lean` -> `APAP/Prereqs/Bohr/Regular.lean`, `object/{BohrBasic,BohrFourier,BohrStep,BohrIter,Integer}.lean` -> `APAP/`, run `LEAN_NUM_THREADS=2 lake build`, and run `#print axioms int` via `lake env lean`.
