# Pre-Registration (`2026-10-29-mizopl-61e59c7d`)

- **Target:** `ame-states-open-cells-huber-table` (`p2`-only follow-up to PR `#576`)
- **Claimed Tier:** `CONFIRMED_PARTIAL` (`partial_win: p2` — Table-Maintenance Cell Audit & `[[15, 0, 8]]` Purity Erratum)
- **Falsification Criterion:** Any mismatch between `object/huber_wyderka_settled_blanks_audit.json` and the exact finite-field / integer recomputation in `how-we-built-it/audit_huber_wyderka.py` causes `verify-it-yourself/check_ame_claim.py` to print `FAIL` and exit with code `1`.
