# Run It Yourself — `myerson-vs-anonymous-reserve-gap`

## 1. Quick Verification
To verify the certificate in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line:
```text
PASS
```

## 2. Re-building the Certificate from Scratch
To re-run the full 50-digit interval arithmetic certification and calibration:

```sh
python3 how-we-built-it/calibrate_jltx.py
python3 how-we-built-it/certify_5buyer.py
python3 how-we-built-it/scale_buyers_5_to_25.py
```

Dependencies for re-building: `python3`, `mpmath`, `scipy`.
Verification itself (`verify-it-yourself/verify_certificate.py`) uses only Python standard library modules (`json`, `math`, `sys`, `os`, `fractions.Fraction`).
