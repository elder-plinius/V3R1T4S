# Commands used to build the object

From a directory that contains this builder (ssz_table1.py) and the exact dual script, with numpy installed for the solve step only:

1. Policy iteration on the over-paying MDP N at T=95, alpha=9/20, rho=169/250 (see ssz_table1.py). The saved bias and policy are object/over_bias.npy and object/over_policy.npy in the package.

2. Exact dual (also how-we-built-it/exact_table1_dual.py, needs numpy only to load .npy):

```
python3 how-we-built-it/exact_table1_dual.py \
  --T 95 --alpha 9/20 --rho 169/250 --paying over --gamma 0 \
  --eq7-grouping rebracketed --ht-comp printed \
  --bias object/over_bias.npy --policy object/over_policy.npy \
  --out object/exact_dual_rho169_250.json
```

The package verifier does not need numpy: use verify-it-yourself/exact_dual_check.py instead.

PREREG.md in this folder is the frozen criterion from the run. FORMULA.md is the definition of N used in the claim.
