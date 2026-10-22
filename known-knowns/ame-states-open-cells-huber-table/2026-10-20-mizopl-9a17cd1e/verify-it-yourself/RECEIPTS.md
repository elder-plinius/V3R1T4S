# Verification Receipts (`2026-10-20-mizopl-9a17cd1e`)

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Output**:
  ```text
  Verified exact AME(9, 10) (126/126 cuts), AME(11, 10) & pure [[11, 1, 6]]_5 (462/462 cuts), and 1,008-cell audit.
  PASS
  ```
- **Corrupted-Object Self-Break Test**: Changing any single digit in `object/ame_9_10_certificate.json` causes `run_checks.sh` to exit with status `1` and print `FAIL`.
