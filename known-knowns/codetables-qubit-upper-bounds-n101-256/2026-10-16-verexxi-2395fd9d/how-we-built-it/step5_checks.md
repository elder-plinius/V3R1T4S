# Step 5 (self-attack) for [[133,2]]
Fri Oct 16 21:02:25 UTC 2026
## check2 cert_133_2_44_sh.json
check2 PASS [[133,2,44]] value>0: True max column: <=0
exit 0
## check2 cert_133_2_45_sh.json
check2 PASS [[133,2,45]] value>0: True max column: <=0
exit 0
## mutate.py on cert_133_2_44_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
