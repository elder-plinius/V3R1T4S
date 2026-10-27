# Verification Receipts — `qoblib-portfolio-ten-assets-exact`

## Execution Command
```sh
sh verify-it-yourself/run_checks.sh
```

## Environment
- OS: Darwin 23.6.0 (macOS Apple Silicon)
- Python: 3.12 (standard library only: `gzip`, `hashlib`, `json`, `math`, `os`, `sys`, `time`, `urllib.request`, `fractions.Fraction`)
- Verification Date: 2026-10-27

## Verifier Execution Output
```
Feasibility: VERIFIED (all constraints satisfied)
Breakdown: risk=25950, return=-37218, transaction=3831, cash_interest=-990, short_cost=30, liquidation=0, total=-8397
Hasse Bellman Inequalities: ALL 5 PASS across all 10,606 states
Exact Global Optimality Certified: min V_9 = -8397 in 0.579s
PASS
```
