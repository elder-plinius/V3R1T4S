# Step 5 (self-attack) for [[190,2]]
Sat Oct 17 05:37:19 UTC 2026
## check2 cert_190_2_63_sh.json
check2 PASS [[190,2,63]] value>0: True max column: <=0
exit 0
## check2 cert_190_2_64_sh.json
check2 PASS [[190,2,64]] value>0: True max column: <=0
exit 0
## mutate.py on cert_190_2_63_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
