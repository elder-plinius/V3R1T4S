# X reproduce (scu N=83, kind "short")

## Findings
- verify-it-yourself/run_checks.sh, run from a /tmp copy on cores 4-7: ends in PASS, and its output matches verify-it-yourself/RECEIPTS.md line for line.
- sha256 of object/scu83_refined.txt (7d47b674...) and the-record-we-beat/scu83-posted.txt (cc08dcaf...) match verify-it-yourself/CLAIM.json.
- My own 60-digit Decimal code (r* = min(wall gap 0.5-max|coord|, half the smallest pairwise distance)) gives:
  - the-record-we-beat/scu83-posted.txt: 83 centres, r* = 0.116284441837827490267325191419, which is -7.1858e-7 below the table cell 0.116285160418976515059766617287. That is far outside the 1e-9 margin, so the posted file really does fall short of its table value.
  - object/scu83_refined.txt: 83 centres, r* = 0.11628444376835894297..., which matches object_rstar_prefix. It is still -7.1665e-7 below the cell, so the refined object does not reach the table value either. It only improves on the posted file by about 1.9e-9.
- These match the claim's stated numbers. The claim is "short": the posted coordinates do not achieve the radius.txt value. That reproduces from the files in this package.
- Not checked: the live packomania re-fetch (the-record-we-beat/SNAPSHOT.md is taken as given). The how-we-built-it/ files named in RUN_IT_YOURSELF.md are not in the package, so steps 1-2 could not be run.

context: executor subagent, fresh context
pass: true
