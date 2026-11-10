# Run it yourself

In a fresh shell, from this folder:

    sh verify-it-yourself/run_checks.sh

Expected output ends with:

    VALID
    ...
    corrupted copy rejected
    == size must be 16, strictly above the table entry 15
    size 16
    PASS

Rebuilding the object: see `how-we-built-it/COMMANDS.md` (time-capped random search; a rerun need not
reproduce the identical list, the frozen object is the evidence).
