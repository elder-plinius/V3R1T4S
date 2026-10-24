Executed UTC: 2026-10-18T20:47:56.896265+00:00
Command: sh verify-it-yourself/run_checks.sh
Environment: Python 3 standard library, isolated remote job, low priority with hard timeout.

```text
reviewed object identity: PASS (hash binding only)
{
  "definition_positive_negative": "PASS",
  "direct_pairs": 15625,
  "localization_checks": 14104,
  "active_full_3_power_checks": 1326,
  "independent_polynomial_identities": "PASS",
  "constant_bounds": "PASS",
  "fixtures": [
    {
      "n": 76672,
      "j": 26775,
      "k": 6973,
      "l": 4204,
      "u": 1268,
      "v": 232,
      "in_band": false
    },
    {
      "n": 3205956776,
      "j": 1556134875,
      "k": 2737797,
      "l": 480036,
      "u": 14028,
      "v": 72,
      "in_band": false
    }
  ],
  "universal_proof": "manual argument required; finite checks only"
}
{"result": "PASS", "counts": {"identities": 3, "positivity_certificates": 15}, "identity_mutant_rejected": true, "positivity_mutant_rejected": true, "scope": "unchanged n5/6 band: n>=65536 and 2^36*(n-2j)^6<=n^5, single-context unpanelled", "limits": "Exact quotient identities and polynomial positivity only; prime localization and integer/domain inference are the written-proof premises, not a complete formal proof assistant."}
PASS
```

These are exact algebraic checks and finite corroboration. The universal proof is the written argument; neither this output nor an object hash replaces its logical review.
