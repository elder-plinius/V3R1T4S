# Receipts
Command: sh verify-it-yourself/run_checks.sh (with OR-Tools available)
Run UTC: 2026-11-27T17:02:48Z

```
ITC2021_Early_14: # Lower bound on Early 14: 4 (claimed 4)
ITC2021_Early_9: # Lower bound on Early 9: 40 (claimed 40)
ITC2021_Middle_6: total breaks >= 22, even -> 22; penalty lower bound from BR2: 60 (claimed 60)
ITC2021_Middle_9: total breaks >= 17, even -> 18; penalty lower bound from BR2: 20 (claimed 20)
ITC2021_Late_9: total breaks >= 18, even -> 18; penalty lower bound from BR2: 20 (claimed 20)
solver replay:
ITC2021_Early_14 OPTIMAL objective 4 bound 4 0.0s
ITC2021_Early_9 OPTIMAL objective 40 bound 40 0.0s
ITC2021_Middle_6 OPTIMAL objective 60 bound 60 17.6s
ITC2021_Middle_9 OPTIMAL objective 20 bound 20 17.1s
ITC2021_Late_9 OPTIMAL objective 20 bound 20 22.7s
checked 5, failed 0
PASS
```
