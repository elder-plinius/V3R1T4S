# X criterion check (scu N=83, kind "short")

Criterion (verify-it-yourself/CLAIM.json + check_scu_p3.py): the posted coordinates must achieve r* < table_value - margin (1e-9), with r* = min(half min pair distance, 1/2 - max |coord|), cube [-1/2,1/2]^3.

Findings:
- the-record-we-beat/scu83-posted.txt: sha256 cc08dcaf…1c62 matches CLAIM.json posted_sha256; 83 centre rows, all inside the cube.
- Own exact-rational check (Fraction, no sqrt until display): wall slack = 0.116284441837827490267325191420, half min distance = 0.116284441837827490267325191419…; r* - cell = -7.1858e-7, short by far more than 1e-9 (both wall and distance are binding and both short).
- verify-it-yourself/run_checks.sh rerun on cores 4-7: PASS, matching verify-it-yourself/RECEIPTS.md.
- object/scu83_refined.txt: sha256 matches; r* 0.1162844437683589… also below cell (it is the posted file polished, not an improvement past the record; irrelevant to the criterion).
- Caveat: the table value 0.116285160418976515059766617287 comes only from the-record-we-beat/SNAPSHOT.md (radius.txt itself is not in the package, not re-fetched); the posted file is the sole offline copy of scu83.txt. The live-page match is taken from the snapshot, not checked independently.

confirmed_scope: The packaged copy of Packomania scu83.txt (sha256 cc08dcaf…1c62) has 83 centres whose exact r* is 0.11628444183782749…, which is about 7.19e-7 below the radius.txt value 0.116285160418976515059766617287 recorded in the package's own snapshot, so it falls short of that value by more than the 1e-9 margin.
context: executor subagent, fresh context
pass: true
