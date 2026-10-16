# Step 5 (self-attack) for [[177,1]]
Fri Oct 16 21:02:44 UTC 2026
## check2 cert_177_1_58_sh.json
check2 PASS [[177,1,58]] value>0: True max column: <=0
exit 0
## check2 cert_177_1_59_sh.json
check2 PASS [[177,1,59]] value>0: True max column: <=0
exit 0
## mutate.py on cert_177_1_58_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
