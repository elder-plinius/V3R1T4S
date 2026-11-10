# Verification Receipts

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Exit Code**: `0`
- **Output**:
  ```text
  Verified A182275(0..15), A116694(0..15, 0..20) [all 210 b116694.txt entries], and A333476 rows 0..14 [all 91 b333476.txt entries] via 3 independent methods.
  A182275(13) = 44952337678281087149239713571524612859282098351847918617404
  A116694(13, 12) = 1079082161133939350509688342814661590018188105589177004
  A182275(14) = 179633908970647867061644006072082999771595948524857068695476923848566
  A182275(15) = 3806271642082756769250454934171160217011193243952381412806809441536918416569002
  PASS
  ```
- **Corrupted Object Check**: Changing any digit in `object/a182275_dissections.json` causes `sh verify-it-yourself/run_checks.sh` to exit with status `1` and print `FAIL`.
