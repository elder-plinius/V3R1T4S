# Receipts

sh verify-it-yourself/run_checks.sh:

```
atoms=344 rectangles=188898 pieces=288355 area_num=10845095970898536899315634 (over 2^80) mass_num=5629639765 (over 2^30)
value=1.711011823672
strictly_above_bar True margin 0.008288090071964177
pieces=270257 area_num=10845095970898536899315634 (over 2^80) mass_num=5629639765 (over 2^30)
value=1.711011823672
SWEEP V_lower 1.71101182367469 V_upper 1.71101182367477 width 0.00000000000008  area_lower 8.97085312841852 V*mass_lower 8.97085312841852
      trivial cap area/mass 1.71382271903463
PASS
```

python3 -I verify-it-yourself/tests/small_cases.py:

```
value=1.000000000000
value=1.000000000000
value=1.085786437626
PASS
```
