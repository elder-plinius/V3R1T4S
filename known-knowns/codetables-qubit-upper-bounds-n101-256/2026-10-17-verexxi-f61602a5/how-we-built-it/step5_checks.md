# Step 5 (self-attack) for [[215,6]]
Sat Oct 17 05:37:34 UTC 2026
## check2 cert_215_6_72_sh.json
check2 PASS [[215,6,72]] value>0: True max column: <=0
exit 0
## check2 cert_215_6_73_sh.json
check2 PASS [[215,6,73]] value>0: True max column: <=0
exit 0
## mutate.py on cert_215_6_72_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
