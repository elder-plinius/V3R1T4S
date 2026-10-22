# Actual verifier output

Command: `sh verify-it-yourself/run_checks.sh` with an initially empty public-input cache. Both pinned input downloads succeeded; both exact evaluators agreed. The cache setting controls storage only, and all file hashes were checked.

```text
{"input": "stock_prices.txt.gz", "url": "https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/54d8b9d99ea382f8002f960e71e45f559e4c332a/06-portfolio/instances/po_a400_t10_s00/stock_prices.txt.gz", "utc": "2026-10-15T17:35:33.793846+00:00", "http_status": 200, "sha256": "faed9a53c7717686e2b4e664d4bc89a0dbda15e195811acd5a09aed4c717471b", "bytes": 47179}
{"input": "covariance_matrices.txt.gz", "url": "https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/54d8b9d99ea382f8002f960e71e45f559e4c332a/06-portfolio/instances/po_a400_t10_s00/covariance_matrices.txt.gz", "utc": "2026-10-15T17:35:34.938010+00:00", "http_status": 200, "sha256": "efaeb65dfa0c727cd1b7b0ba44f92c18a8c4c1e8cf9c14a13effea1d8ba0d6ed", "bytes": 20518660}
{"components": {"cash_interest": -780, "liquidation": 0, "returns": -1912445, "risk": 64891, "short_cost": 1158, "transactions": 150512}, "independent_evaluators_agree": true, "object_sha256": "7bf097a5c2987de75318a75948fbfcbc24dbe9a59323beccb374d2dddfc2bac9", "objective": -1696664, "reference_budget": 100, "risk_weight": "0.01", "seconds": 11.345}
PASS
```
