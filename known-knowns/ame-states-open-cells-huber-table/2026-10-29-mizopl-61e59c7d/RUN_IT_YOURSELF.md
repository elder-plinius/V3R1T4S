# Run It Yourself

## Prerequisites
- Python 3.9+ (standard library only: `json`, `os`, `re`, `sys`, `random`, `itertools`, `math`). Zero third-party packages and zero copied HTML files required.

## One-Command Verification
```bash
bash verify-it-yourself/run_checks.sh
```

## Expected Output (`~1.5s` on Apple M1)
```text
Verified p2 1,008-cell Huber-Wyderka audit, 17 URL+SHA256 source records, [[15,0,8]]_5 (w_pure=7, 190/6,435 bad cuts) & [[15,0,8]]_7 (pre-2026-10-21 w_pure=1, 3,003/6,435 bad cuts -> 2026-10-21 cyclic w_pure=8, 0/6,435 bad cuts) purity erratum, and prior Lean 4 / literature cross-checks.
PASS
```
