== 1. object byte-exactness
bytes: 41
== 2. interpreter check + agreement with object/expected.txt
PASS len=41 value=114514 steps=305379 mincell=0
checker output matches expected.txt on len/value/steps/mincell
== 3. corruption self-test (the checker must reject a broken object)
corrupted object -> FAIL value 114386 != 114514
corruption correctly rejected
== 4. instruction count equals the claimed 41
instructions: 41
PASS
