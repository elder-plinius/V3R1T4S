# Step 5 (self-attack) for [[185,3]]
Sat Oct 17 05:37:03 UTC 2026
## check2 cert_185_3_61_sh.json
check2 PASS [[185,3,61]] value>0: True max column: <=0
exit 0
## check2 cert_185_3_63_sh.json
check2 PASS [[185,3,63]] value>0: True max column: <=0
exit 0
## mutate.py on cert_185_3_61_sh.json
drop largest shadow multiplier H1: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: FAIL  check2: FAIL
Traceback (most recent call last):
  File "tmp\mut_185_3\x\y\code\mutate.py", line 14, in <module>
    os.remove(tmp)
    ~~~~~~~~~^^^^^
PermissionError: [WinError 5] Access is denied: 'tmp/mut_185_3/mut.json'
