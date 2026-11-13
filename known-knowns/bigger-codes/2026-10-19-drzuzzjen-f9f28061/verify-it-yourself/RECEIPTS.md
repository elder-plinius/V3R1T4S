# Publisher offline clean-copy tests

These verify object/checker execution only, not novelty or package readiness.

Actual macOS clean-copy command: `sh verify-it-yourself/run_checks.sh`

Exit0, stdout:

```text
{"checker_sha256": "3a898717447d6915a7f57efc00ebf5b523b49f41cca6c4b53b7658f7e57c68e0", "count_convention": "number of distinct explicit codewords; not orbits", "d": 6, "distance_histogram": {"6": 657169, "8": 2652252, "10": 7965356, "12": 11975256, "14": 9533429, "16": 4330519, "18": 919672, "20": 100335, "22": 3023}, "distinct_M": 8734, "elapsed_seconds": 3.452144583920017, "ended_utc": "2026-10-19T11:48:08.735236+00:00", "expected_M": 8734, "expected_pairs": 38137011, "max_rss_bytes": 25673728, "min_distance": 6, "min_distance_witness": [0, 1], "n": 25, "object_sha256": "f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde", "observed_M": 8734, "pairs_checked": 38137011, "pass": true, "pid": 77985, "python_version": "3.14.8 (main, Sep 30 2026, 17:55:09) [Clang 21.0.0 (clang-2100.3.34.2)]", "source": "object/CANDIDATE_M8734.txt", "started_utc": "2026-10-19T11:48:05.283085+00:00", "threading": "one main Python thread; no libraries or workers", "unique_pair_convention": "all unordered pairs 0 <= i < j < M", "w": 11}
PASS
```

Eight calibration cases passed. Altered-object clean-copy wrapper exited1 on hash_mismatch and did not print PASS. The resource-unavailable branch passed all38137011 pairs with null RAM telemetry; this was simulation on macOS, not native Windows evidence. Standard library only; no environment install or search.
