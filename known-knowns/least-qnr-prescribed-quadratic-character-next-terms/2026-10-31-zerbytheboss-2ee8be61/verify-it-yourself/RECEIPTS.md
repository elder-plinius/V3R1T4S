# Verification Receipts

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Exit Code**: `0`
- **Output**:
  ```text
  Verified A000229(39..43) = [317398900373231, 112434732901969, 1463971373078639, 178936222537081, 501108392233679] via independent CRT modulus splits.
  PASS
  ```
- **Corrupted Object Check**: Changing any digit in `object/a000229_qnr_census.json` causes `sh verify-it-yourself/run_checks.sh` to exit with status `1` and print `FAIL`.
