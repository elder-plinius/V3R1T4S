# Run It Yourself

## 1. Prepare Pinned `Lean v4.36.0-rc2` + Mathlib Environment (Once)

```sh
git clone https://github.com/YaelDillies/LeanAPAP.git
cd LeanAPAP
git checkout fb5cb9c4f594cbeeb160c715618d13640984c521
lake exe cache get
cd ..
```

## 2. Run the Standalone 5-Gate Referee

```sh
LEANAPAP_ROOT=./LeanAPAP PRM_LEAN_JOBS=6 sh verify-it-yourself/run_checks.sh
```

Expected final line: `PASS`.

## 3. Inspect Main Theorems and Axioms

See `object/PRMPlus/Defs.lean` for the game/algorithm definitions and `object/PRMPlus/Main.lean` for `alg2_caiGame_eventual_dualityGap_ge`, `alg2_caiGame_liminf_dualityGap_pos`, `alg2_caiGame_not_tendsto_zero`, and `alg2_caiGame_iter1000_bounds`.
