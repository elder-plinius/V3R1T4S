# Step 5 (self-attack) for [[173,2]]
Sat Oct 17 05:36:51 UTC 2026
## check2 cert_173_2_57_sh.json
check2 PASS [[173,2,57]] value>0: True max column: <=0
exit 0
## check2 cert_173_2_59_sh.json
check2 PASS [[173,2,59]] value>0: True max column: <=0
exit 0
## mutate.py on cert_173_2_57_sh.json
drop largest shadow multiplier H1: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
