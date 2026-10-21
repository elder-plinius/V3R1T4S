# Step 5 (self-attack) for [[115,4]]
Sat Oct 17 05:37:10 UTC 2026
## check2 cert_115_4_38_sh.json
check2 PASS [[115,4,38]] value>0: True max column: <=0
exit 0
## check2 cert_115_4_39_sh.json
check2 PASS [[115,4,39]] value>0: True max column: <=0
exit 0
## mutate.py on cert_115_4_38_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
