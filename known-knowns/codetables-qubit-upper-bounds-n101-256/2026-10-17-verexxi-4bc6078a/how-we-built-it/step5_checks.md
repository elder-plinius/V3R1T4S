# Step 5 (self-attack) for [[110,5]]
Sat Oct 17 05:37:08 UTC 2026
## check2 cert_110_5_36_sh.json
check2 PASS [[110,5,36]] value>0: True max column: <=0
exit 0
## check2 cert_110_5_37_sh.json
check2 PASS [[110,5,37]] value>0: True max column: <=0
exit 0
## mutate.py on cert_110_5_36_sh.json
drop largest shadow multiplier H1: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
