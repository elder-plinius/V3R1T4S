# Step 5 (self-attack) for [[142,2]]
Fri Oct 16 21:02:29 UTC 2026
## check2 cert_142_2_47_sh.json
check2 PASS [[142,2,47]] value>0: True max column: <=0
exit 0
## check2 cert_142_2_48_sh.json
check2 PASS [[142,2,48]] value>0: True max column: <=0
exit 0
## mutate.py on cert_142_2_47_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
