# Run it yourself

Fresh shell, from this package folder. Needs python3 (>= 3.8) and pip access once (run_checks.sh installs mpmath==1.3.0
into verify-it-yourself/.venv unless python3 already has mpmath).

```sh
sh verify-it-yourself/run_checks.sh      # under 1 s; last line: PASS
```

What it does (real output in verify-it-yourself/RECEIPTS.md), at 200 and at 300 bits, PASS only if both pass:
1. Reads object/certificate.json and checks every constant equals the cited value (Y = 29.735, alpha = 1/3 + 1e-9,
   delta = 1e-9, u2 = 1e-6, K = 2.4798, c = 51.34, KLN C1 = 17.418 / C2 = 5.272, Bellotti Thm 1.1 rows and log T > 481958).
2. Recomputes, in mpmath interval arithmetic, X0 = 3 e^Y, nu0 = 1/(c L^(2/3) (log L)^(1/3)) with L = alpha X0, the terms
   A0, A1, A2, R_E, R_T of object/proof.md and Phi = 2(A0 + A1 + A2) + R_E + R_T, plus conditions (M1)-(M4), (V1)-(V4).
3. Requires Phi < 1, the stated upper bound >= the recomputed one and within 1e-9 of it, and Phi > 1 at Y - 0.001.

Rebuild the object and every number in the claim (python-flint==0.9.0 and mpmath==1.3.0, how-we-built-it/requirements.txt):

```sh
cd how-we-built-it/code && PY=python3 sh run_all.sh    # about 5 s; prints FAIL PASS ... RUN_ALL_DONE (the FAILs are expected controls)
```

cert_arb.py is the arb certificate (prec 128 and 256), standalone_check.py an independent mpmath.iv implementation,
scan.py the grid search (out/scan_out.txt), null_tests.py and mutation.py the controls, replay_ch.py the float replay of
the published 32.892 and 32.76. See how-we-built-it/COMMANDS.md.
