# Run it yourself

Work from this package folder in a fresh shell. Python 3 is required. The mandatory check uses only the standard library.

## Mandatory: exact dual of the claimed object

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. The checker rebuilds Table 1 and the (26)-(27) reading of equation (7), loads object/over_bias.npy as exact dyadic rationals, and requires

- 72678 inequalities (match at (a, 0, relevant) included),
- 0 off-board successors,
- g_bar = -51696398727/351843720888320,
- matching object/exact_dual_rho169_250.json.

This takes about one second. The captured output of a passing run is in verify-it-yourself/RECEIPTS.md.

To invoke the checker directly:

```sh
python3 verify-it-yourself/exact_dual_check.py
```

Exit status 0 means the dual matched; 1 means it did not.

## Optional: Table 2 calibration and over-pay sanity

Needs numpy. From this folder:

```sh
python3 how-we-built-it/calibrate_and_sanity.py
```

Expect under-paying REV at T=95, alpha=0.425 and 0.45, within one unit of the last printed digit of 0.56808 and 0.66891, and a strictly positive over-paying gain at alpha=0.45, rho=0.66, T=95. Runtime is several minutes.

## Optional: supplementary conservative h=T recertification

Needs numpy. The saved dual is how-we-built-it/supplementary/recert_corrected_ht_dual.json (g_bar = -27657597973/281474976710656). To rebuild the bias and re-check, run how-we-built-it/recert_corrected_ht.py from a copy of the builder layout (it expects the exact-dual script next to itself and writes under ../object/). The primary claimed object does not depend on this optional step.

## Rebuild note

The bias vector in object/over_bias.npy was obtained by policy iteration on N_{169/250}^{95} (how-we-built-it/ssz_table1.py). The certificate is the exact dual, not the floating-point gain.
