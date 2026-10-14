# Actual package replay
Command: `sh verify-it-yourself/run_checks.sh`
Exit status: 0

```text
started_utc: 2026-10-14T02:52:37.533674+00:00
{"negative_controls_rejected": {"distance_two": "('distance', 1, 0, 2)", "duplicate": "duplicate vectors", "nonbinary": "('alphabet', 0)", "wrong_count": "('cardinality', 1, 2)", "wrong_length": "('length', 0, 5)", "wrong_weight": "('weight', 0, 2)"}, "positive_control": {"byte_count": 14, "cardinality": 2, "distance_histogram": {"6": 1}, "length": 6, "minimum_distance": 6, "pair_count": 1, "sha256": "08f2edadc970ddaa3aaaa73f382f9d1e1d609a9b931b9f701347fe03cbdf14ce", "weight": 3}}
{"byte_count": 364728, "cardinality": 13026, "distance_histogram": {"6": 956670, "8": 4965051, "10": 15539547, "12": 26352091, "14": 23355752, "16": 11017900, "18": 2454798, "20": 190016}, "elapsed_seconds": 12.657820149004692, "length": 27, "minimum_distance": 6, "pair_count": 84831825, "sha256": "9e824e9f8a92e74226231152fc8e8a972be5ba79549e2a10e512fe63a3934f49", "weight": 10}
INDEPENDENT_CHECK: PASS
{"run": 1, "count": 13026, "bytes": 364728, "sha256": "9e824e9f8a92e74226231152fc8e8a972be5ba79549e2a10e512fe63a3934f49", "exact_byte_match": true, "author_verifier": true}
{"run": 2, "count": 13026, "bytes": 364728, "sha256": "9e824e9f8a92e74226231152fc8e8a972be5ba79549e2a10e512fe63a3934f49", "exact_byte_match": true, "author_verifier": true}
REPRODUCTION: PASS
ENCODINGS: PASS
PASS
```
