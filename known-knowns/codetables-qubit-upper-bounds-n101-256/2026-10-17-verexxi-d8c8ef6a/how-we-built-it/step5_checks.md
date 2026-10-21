# Step 5 (self-attack) for [[161,2]]
Sat Oct 17 05:36:43 UTC 2026
## check2 cert_161_2_53_sh.json
check2 PASS [[161,2,53]] value>0: True max column: <=0
exit 0
## check2 cert_161_2_55_sh.json
check2 PASS [[161,2,55]] value>0: True max column: <=0
exit 0
## mutate.py on cert_161_2_53_sh.json
drop largest shadow multiplier H1: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
