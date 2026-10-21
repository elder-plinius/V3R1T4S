# Step 5 (self-attack) for [[200,10]]
Sat Oct 17 05:36:19 UTC 2026
## check2 cert_200_10_63_sh.json
check2 PASS [[200,10,63]] value>0: True max column: <=0
exit 0
## check2 cert_200_10_67_sh.json
check2 PASS [[200,10,67]] value>0: True max column: <=0
exit 0
## mutate.py on cert_200_10_63_sh.json
drop largest shadow multiplier H0: check_cert: FAIL  check2: FAIL
remove all shadow rows: check_cert: FAIL  check2: FAIL
same multipliers at d-1: check_cert: FAIL  check2: FAIL
double u_E0: check_cert: FAIL  check2: FAIL
same multipliers at k+1: check_cert: PASS  check2: PASS

## Follow-up on "same multipliers at k+1: PASS PASS" (known exception)
Copy of cert_200_10_63_sh.json with k set to 9 (k-1), run through both checkers:
check_cert: FAILED [[200,9,63]] shadow=True: certificate value is not positive (exit 1)
check2: FAIL [[200,9,63]] value>0: False (exit 1)
k-1 is rejected, so the k+1 acceptance is expected (d(n,k+1) <= d(n,k): the certificate for k=10 may also certify larger k). Continue.
