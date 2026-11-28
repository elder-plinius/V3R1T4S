# Run It Yourself

Exact commands from this package folder in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
--- Verifying SSZ Table 2 Calibration and Model Sanity ---
Calibration 1: Underpaying alpha=0.425, T=75, rho=0.56808: gain = -0.000120 (target: 0.00000 within 1 unit of last printed digit)
Calibration 1: PASS
Calibration 2: Underpaying alpha=0.45, T=75, rho=0.66891: gain = -0.000490 (target: 0.00000 within 1 unit of last printed digit)
Calibration 2: PASS
Sanity Check: Overpaying alpha=0.45, T=75, rho=0.66: gain = +0.012348 (must be > 0)
Sanity Check: PASS

--- Verifying Dual Certificate: certificate_alpha_0.45.json ---
Target: bitcoin-selfish-mining-revenue-bounds
Parameters: alpha = 9/20 (0.45), gamma = 0, T = 95, comp_var = 2
Certified upper bound U = 70099/100000 (0.7009900)
Certificate gain g = -3170481/200000000 (-0.01585240)
Gain check g < 0: PASS
Checked 27648 states across all valid actions.
Max Bellman residual across all state-actions: -0.01586240 (-3172481/200000000)
Inequality diff <= g: -0.01586240 <= -0.01585240
ALL STATE-ACTION INEQUALITIES SATISFIED EXACTLY! Zero violations!
CERTIFICATE VERIFIED: max REV < 0.7009900 is mathematically certified!

--- Verifying Dual Certificate: certificate_alpha_0.475.json ---
Target: bitcoin-selfish-mining-revenue-bounds
Parameters: alpha = 19/40 (0.475), gamma = 0, T = 95, comp_var = 2
Certified upper bound U = 45233/50000 (0.9046600)
Certificate gain g = -21434039/400000000 (-0.05358510)
Gain check g < 0: PASS
Checked 27648 states across all valid actions.
Max Bellman residual across all state-actions: -0.05359510 (-21438039/400000000)
Inequality diff <= g: -0.05359510 <= -0.05358510
ALL STATE-ACTION INEQUALITIES SATISFIED EXACTLY! Zero violations!
CERTIFICATE VERIFIED: max REV < 0.9046600 is mathematically certified!

...
ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% PASS RATE!
PASS
```

To re-run the discovery solver from `how-we-built-it/`:
```sh
python3 how-we-built-it/run_lens1.py
```
