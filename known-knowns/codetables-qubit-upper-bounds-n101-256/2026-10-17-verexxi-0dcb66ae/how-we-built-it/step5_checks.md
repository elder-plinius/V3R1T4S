# Step 5 (self-attack) for [[150,3]]
Sat Oct 17 05:36:36 UTC 2026
## check2 cert_150_3_49_sh.json
check2 PASS [[150,3,49]] value>0: True max column: <=0
exit 0
## check2 cert_150_3_51_sh.json
check2 PASS [[150,3,51]] value>0: True max column: <=0
exit 0
## mutate.py on cert_150_3_49_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
