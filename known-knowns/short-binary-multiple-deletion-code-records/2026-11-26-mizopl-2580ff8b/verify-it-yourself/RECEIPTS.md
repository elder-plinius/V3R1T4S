# Cold Verification Receipts

```
[OK] (15,2) | size=137 (> Table 2 136) | |D_2|=3396 | maxLCS=12<13 | sha=2b226e2f0f7ab7fd
[OK] (15,3) | size=31 (> Table 2 30) | |D_3|=1397 | maxLCS=11<12 | sha=427002b54632ecc1
[OK] (16,3) | size=44 (> Table 2 42) | |D_3|=2344 | maxLCS=12<13 | sha=2580ff8bef1160cd
[OK] companion (16,3) code_16_3_44_rc.json | size=44 | |D_3|=2304 | maxLCS=12<13 | sha=c8b9fd6a57335dc0
[OK] companion (16,3) code_16_3_44_r.json | size=44 | |D_3|=2410 | maxLCS=12<13 | sha=549dc5d6b9f7cea4
[OK] companion (16,3) code_16_3_44_c.json | size=44 | |D_3|=2468 | maxLCS=12<13 | sha=bd70a4f084a4a5c2
[OK] companion (16,2) code_16_2_219_companion.json | size=219 | |D_2|=6091 | maxLCS=13<14 | sha=f7241c96f86c0dbc
PASS
```

`--corrupt` exit code: `1`
```
[OK] (15,2) | size=137 (> Table 2 136) | |D_2|=3396 | maxLCS=12<13 | sha=2b226e2f0f7ab7fd
[OK] (15,3) | size=31 (> Table 2 30) | |D_3|=1397 | maxLCS=11<12 | sha=427002b54632ecc1
[REJECTED] D_3 collision on '0000000000000' between 0000000000000000 and 1000000000000000
FAIL
```
