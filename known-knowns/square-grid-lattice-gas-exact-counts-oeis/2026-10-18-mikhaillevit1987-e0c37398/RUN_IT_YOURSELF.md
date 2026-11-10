# Run it yourself

In a fresh shell, from this folder:

    sh verify-it-yourself/run_checks.sh

Expected output ends with:

    runs that alone determine a(16) (modulus > 2^272): 2
    VALID
    == checker on a corrupted copy (last digit changed; must be INVALID)
    corrupted copy rejected
    PASS

Rebuilding the object from scratch (Rust, 5-25 minutes on 6 cores): see `how-we-built-it/COMMANDS.md`.
Any other prime p < 2^62 is a fresh check: `ice A 16 6 p` must print the value mod p.
