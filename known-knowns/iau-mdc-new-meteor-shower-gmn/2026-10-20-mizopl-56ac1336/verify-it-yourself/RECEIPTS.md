# Verification Receipts (`2026-10-20-mizopl-56ac1336`)

- **Command**: `sh verify-it-yourself/run_checks.sh`
- **Output**:
  ```text
  Verified 4 Main uncatalogued GMN showers (M2_Hercules N=20, M1_Cepheus_Core N=15, M1_Cepheus_MC N=15, M3_Camelopardalis N=16), p1 4.84h outburst (N=10), p2 17 multi-year working-list recurrences, and 400-control null test across all 2,192 IAU MDC rows.
  PASS
  ```
- **Corrupted-Object Self-Break Test**: Changing any single digit in `object/new_shower_cluster.json` (or `object/independent_cluster_audit.json`, `object/new_shower_gmn_lines.txt`, `object/p1_outburst_cluster.json`, `object/p2_working_list_recurrence.json`) causes `run_checks.sh` to exit with status `1` and print `FAIL`.
