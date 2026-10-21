# Step 5 (self-attack) for [[146,2]]
Fri Oct 16 21:02:31 UTC 2026
## check2 cert_146_2_48_sh.json
check2 PASS [[146,2,48]] value>0: True max column: <=0
exit 0
## check2 cert_146_2_49_sh.json
check2 PASS [[146,2,49]] value>0: True max column: <=0
exit 0
## mutate.py on cert_146_2_48_sh.json
drop largest shadow multiplier H1: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
