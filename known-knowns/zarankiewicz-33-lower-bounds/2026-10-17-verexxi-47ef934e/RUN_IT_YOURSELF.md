# Run it yourself (fresh shell, from this folder)
1. Check: `sh verify-it-yourself/run_checks.sh` -> last line `PASS`, exit status 0 (output in verify-it-yourself/RECEIPTS.md). On any
   failure the last line is `FAIL` and the exit status is 1. Needs only Python 3 (standard library). About 1 second.
2. Check by hand if you prefer: the object is plain text, 16 lines of 19 characters 0 or 1. It is valid when no 3 rows and 3 columns
   have all nine common entries equal to 1. For each of the 560 row triples count the columns where all three rows have a 1; a
   violation is a count of 3 or more. The file must have exactly 142 ones (sha256
   47ef934e67f7931526d0f9b57fbd617a7ea8100c4efdeccf765c4f29286f3fa8).
3. Rebuild or probe: how-we-built-it/COMMANDS.md (search code, the surgery baseline, the sub-matrix copy test).
