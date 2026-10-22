# Receipts
Command, run from the package folder on 2026-10-19 (UTC):
    sh verify-it-yourself/run_checks.sh
Real output:
    VALID size=44 table=34 BEATS
    PASS

Corruption test: a copy of the package with the first letter of word 2 moved to the other GC class (GGGGGTTTTT -> TGGGGTTTTT, so its GC count changes from 5 to 4), same command:
    INVALID word 'TGGGGTTTTT' has GC count 4, not 5
    FAIL
