# Receipts: verify-it-yourself/run_checks.sh

Captured 2026-11-23 18:41:18 ET (America/Toronto, UTC-5) on the packaging machine, from the package root, with `sh verify-it-yourself/run_checks.sh` (python3 3.13 standard library). Wall time about 33 s.

```
object: object/a334497_37.txt
n=37 rule=30 claimed_period=49276415 witness=0x7fbfe703e
bit_order: cell0=LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic
step_crosscheck: fast step equals per-cell definition for the first 2000 steps
divisors: 1 5 37 185 266359 1331795 9855283 49276415
after 49276415 steps: state=0x7fbfe703e start=0x7fbfe703e returned=yes
divisor 1: state=0x808039843 equals_start=no
divisor 5: state=0x909ba0e6c equals_start=no
divisor 37: state=0x1463aa56b6 equals_start=no
divisor 185: state=0x179b120968 equals_start=no
divisor 266359: state=0x10ec393945 equals_start=no
divisor 1331795: state=0x1eff9c0f8f equals_start=no
divisor 9855283: state=0x740e77ad2 equals_start=no
first_return: 49276415
shorter_period_divisors: none
elapsed_sec: 33.2
period_confirmed: 49276415
result: ok
PASS
```

The elapsed_sec line varies from machine to machine; every other line should be identical. This check confirms the witness period only. It does not re-run the exhaustive census.
