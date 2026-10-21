# Step 5 (self-attack) for [[135,8]]
Sat Oct 17 00:31:58 UTC 2026
## check2 cert_135_8_43_sh.json
check2 PASS [[135,8,43]] value>0: True max column: <=0
exit 0
## mutate.py on cert_135_8_43_sh.json
drop largest shadow multiplier H1: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: PASS  check2: PASS
