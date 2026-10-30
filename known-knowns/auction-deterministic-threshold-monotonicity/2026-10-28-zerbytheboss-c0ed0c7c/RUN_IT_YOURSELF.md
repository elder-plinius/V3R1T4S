# Run It Yourself

Exact commands from this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified Shift A: c_A = 11702081697/2754078775 (~4.24900036), c2*(c_A) = 42356979257312942/1733702834035543 (~24.43151065)
Verified Shift B: c_B = 939499441/214943135 (~4.37092090), c2*(c_B) = 44961617784851576/1848022051345129 (~24.32958944)
Verified shift strictly increases: c_B - c_A = 14434668720632936/118394065187091925 (~0.12192054) > 0
Verified threshold strictly decreases: c2*(c_A) - c2*(c_B) = 326547519462491356287836793750/3203921067777227907166545920047 (~0.10192121) > 0
Verified uniform distribution calibration: 2/(1-c)^2 strictly increasing across all shifts
PASS
```

To re-run the full multi-lens discovery pipeline from `how-we-built-it/`:
```sh
python3 how-we-built-it/sturm_rational_engine.py
python3 how-we-built-it/interval_certified_engine.py
```
