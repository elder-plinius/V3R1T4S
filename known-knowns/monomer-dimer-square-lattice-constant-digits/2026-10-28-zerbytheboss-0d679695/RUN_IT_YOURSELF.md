# Run It Yourself

Exact commands from this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified 31 certified decimals of h2: 0.6627989728337459151551962343893
Verified partition growth kappa = exp(h2): 1.9402153514832679617073980181702
Verified agreement with Kong (2006) 12-decimal estimate: OK
Verified strictly inside Kong bracket [0.662798972831, 0.662798972845]: OK
Verified Collatz-Wielandt enclosure [0.6627989727893, 0.6627989728449] (p1): OK
Verified exact reproduction of OEIS A028420 for n=1..14: OK
PASS
```

To re-run the full multi-lens high-precision solvers from `how-we-built-it/`:
```sh
python3 how-we-built-it/ctmrg_monomer_dimer.py
python3 how-we-built-it/cylinder_transfer_solver.py
```
