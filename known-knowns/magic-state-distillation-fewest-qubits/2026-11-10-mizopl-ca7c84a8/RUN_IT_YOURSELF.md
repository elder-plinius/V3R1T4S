# Run It Yourself (`magic-state-distillation-fewest-qubits`)

## 1. Requirements

- Python 3.8+ with `numpy` (no external SAT solver, C++ compiler, internet access, or third-party repository required).

## 2. One-Command Verification (`~9s`)

```bash
sh verify-it-yourself/run_checks.sh
```

Expected terminal line: `PASS` (exit code `0`).

## 3. Adversarial Corruption Check

```bash
python3 verify-it-yourself/verify.py --corrupt
```

Expected terminal line: `FAIL` (exit code `1`).
