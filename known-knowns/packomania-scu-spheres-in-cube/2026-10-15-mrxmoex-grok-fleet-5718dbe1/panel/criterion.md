# Y criterion skeptic

## Findings
- Criterion (verify-it-yourself/CLAIM.json, kind "short", checker verify-it-yourself/check_scu_p3.py): the posted coordinates for N=507 achieve r* = min(half min pair distance, 1/2 - max|coord|) short of the table value 0.065932119200351706079281328718 by more than margin 1e-9; object r* starts with 0.06592848603610355706 and is also short.
- Hashes match CLAIM.json: the-record-we-beat/scu507-posted.txt a62939a8…a338a04, object/scu507_refined.txt 5718dbe1…a2c61. Both have 507 rows.
- My own independent check (exact rational arithmetic, Decimal sqrt at 50 digits, taskset -c 4-7): posted r* = 0.0659283580135823720729146228657738…, r* - cell = -3.7611867693e-6 (well beyond -1e-9); all centres within the cube. Object r* = 0.0659284860361035570699380765…, matches prefix, r* - cell = -3.633e-6.
- Limits: the posted copy is a local snapshot; I did not re-fetch packomania, so "is the live posted file" rests on the-record-we-beat/SNAPSHOT.md hashes. how-we-built-it/ (named in RUN_IT_YOURSELF.md) is absent from the package. The refined object is also below the cell, so it is not a record improvement; this is only a data-integrity finding (posted coordinates don't reach the posted radius).

confirmed_scope: The packaged copy of Packomania's scu507.txt (sha256 a62939a8…) yields r* ≈ 0.06592835801358237 for 507 spheres in the unit cube, about 3.76e-6 below the radius.txt table value 0.065932119200351706, so those coordinates do not certify the tabulated radius.
context: executor subagent, fresh context
pass: true
