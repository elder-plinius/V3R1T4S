# Receipts: Independent Checker Output

Command run:
```bash
sh verify-it-yourself/run_checks.sh
```

Actual stdout:
```text
Evaluated all 864 complete allocations.
Ordered no-envy violations: 828
EF1 violations: 36
Universal obstruction confirmed: 0 valid allocations exist.
PASS
```

Exit code: `0`
Execution time: ~0.4s
All 864 complete allocations generated directly from group constraints violate either ordered no-envy or EF1.
Zero valid allocations exist.
