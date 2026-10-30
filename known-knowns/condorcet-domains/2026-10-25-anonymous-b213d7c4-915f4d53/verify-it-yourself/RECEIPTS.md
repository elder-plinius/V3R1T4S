# Real verification output

Command from package root: `sh verify-it-yourself/run_checks.sh`

```text
{
  "assignment_sha256": "915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b",
  "n": 25,
  "triples": 2300,
  "exact_count": 180870896,
  "reachable_prefix_sets": 3792,
  "first9_dp": 458,
  "first9_bruteforce": 458,
  "calibration": "Fishburn9=488;20=2115186;malformed negatives rejected",
  "seconds": 0.569343667011708
}
PASS
SHA256 915f4d534bc6a8557649f3b02bf4ed21d8782ce01a450c2c39c53c25751d508b
parsed_triples 2300
parser_negative missing PASS
parser_negative duplicate PASS
parser_negative extra PASS
parser_negative unsorted PASS
parser_negative zero PASS
parser_negative out_of_range PASS
parser_negative bad_i PASS
parser_negative bad_j PASS
parser_negative bad_syntax PASS
parser_negative extra_token PASS
parser_negative blank PASS
Fishburn 9 488 states 125
Fishburn 20 2115186 states 6109
first9_DP 458 brute_all_9factorial 458 permutations 362880 states 92
full_exact_count 180870896 states 4598
elapsed_seconds 0.596225
PASS
PASS
```
