# Receipts — `bitcoin-selfish-mining-revenue-bounds`

Execution of `sh verify-it-yourself/run_checks.sh`:

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

--- Verifying Dual Certificate: certificate_alpha_0.425.json ---
Target: bitcoin-selfish-mining-revenue-bounds
Parameters: alpha = 17/40 (0.425), gamma = 0, T = 95, comp_var = 2
Certified upper bound U = 1788/3125 (0.5721600)
Certificate gain g = -811179/400000000 (-0.00202795)
Gain check g < 0: PASS
Checked 27648 states across all valid actions.
Max Bellman residual across all state-actions: -0.00203795 (-815179/400000000)
Inequality diff <= g: -0.00203795 <= -0.00202795
ALL STATE-ACTION INEQUALITIES SATISFIED EXACTLY! Zero violations!
CERTIFICATE VERIFIED: max REV < 0.5721600 is mathematically certified!

--- Verifying Dual Certificate: certificate_alpha_0.40.json ---
Target: bitcoin-selfish-mining-revenue-bounds
Parameters: alpha = 2/5 (0.4), gamma = 0, T = 95, comp_var = 2
Certified upper bound U = 24447/50000 (0.4889400)
Certificate gain g = -6869/50000000 (-0.00013738)
Gain check g < 0: PASS
Checked 27648 states across all valid actions.
Max Bellman residual across all state-actions: -0.00014738 (-7369/50000000)
Inequality diff <= g: -0.00014738 <= -0.00013738
ALL STATE-ACTION INEQUALITIES SATISFIED EXACTLY! Zero violations!
CERTIFICATE VERIFIED: max REV < 0.4889400 is mathematically certified!

--- Verifying Dual Certificate: certificate_alpha_0.45_var1.json.gz ---
Target: bitcoin-selfish-mining-revenue-bounds
Parameters: alpha = 9/20 (0.45), gamma = 0, T = 180, comp_var = 1
Certified upper bound U = 70099/100000 (0.7009900)
Certificate gain g = -388969/100000000 (-0.00388969)
Gain check g < 0: PASS
Checked 98283 states across all valid actions.
Max Bellman residual across all state-actions: -0.00389969 (-389969/100000000)
Inequality diff <= g: -0.00389969 <= -0.00388969
ALL STATE-ACTION INEQUALITIES SATISFIED EXACTLY! Zero violations!
CERTIFICATE VERIFIED: max REV < 0.7009900 is mathematically certified!

--- Verifying Stationary Policy: policy_alpha_0.45.json ---
Parameters: alpha = 0.45, T = 120
Expected epoch rewards: R1 = 0.40538676, R2 = 0.20019415
Computed Stationary Relative Revenue REV = 0.66941800
Published bar: 0.66894000, Required threshold (> bar + 1e-6): 0.66894100
Strictly exceeds published bar + 1e-6: True
POLICY EVALUATION VERIFIED: PASS!

--- Verifying Stationary Policy: policy_alpha_0.475.json ---
Parameters: alpha = 0.475, T = 120
Expected epoch rewards: R1 = 0.44438646, R2 = 0.10846090
Computed Stationary Relative Revenue REV = 0.80381402
Published bar: 0.80184000, Required threshold (> bar + 1e-6): 0.80184100
Strictly exceeds published bar + 1e-6: True
POLICY EVALUATION VERIFIED: PASS!

============================================================
ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% PASS RATE!
============================================================
PASS
```
