# Run it yourself

## Verify the object (fresh shell, from this folder)

    sh verify-it-yourself/run_checks.sh

Expected output (the real run is in verify-it-yourself/RECEIPTS.md):

    ok   3 <= b <= 10125
    ok   b is not a perfect power
    ok   p > 4.8e12 (the table's searched limit for bases 1053..10125)
    ok   p is prime (deterministic Miller-Rabin)
    ok   p does not divide b
    ok   b^(p-1) == 1 mod p^2
    b = 5481, p = 4848813530161, Fermat quotient q_p(b) mod p = 0
    PASS

Without the script:

    python3 verify-it-yourself/verify.py object/pair.json
    python3 -c "p=4848813530161; print(pow(5481, p-1, p*p))"      # prints 1

The table clauses (the row of base 5481, the stated limit, OEIS) are checked against the fetched pages recorded in
the-record-we-beat/RECORD.md, not by the script.

## Rebuild the object (the search that found it)

The sweep is how-we-built-it/wieferich_sweep.py, with pinned requirements in how-we-built-it/requirements.txt (gmpy2,
numpy). Its default screen is the exact meet-in-the-middle screen the search used. Make a virtual environment, install
those requirements, then run from how-we-built-it/:

    python wieferich_sweep.py sweep OUTDIR 4848800000000 20000000 1 DEADLINE 70 1053 10125 4848820000000

- OUTDIR is any empty folder.
- DEADLINE is a Unix time a few minutes ahead (for example the output of `date +%s` plus 900).

This sweeps exactly one block of primes, 4848800000000 <= p < 4848820000000, against all 2360 non-perfect-power
70-smooth bases in 1053..10125.
- OUTDIR/hits.jsonl then contains the pair 5481 / 4848813530161.
- OUTDIR/blocks.jsonl carries the block's record. Its q-matrix sha256 matches the one in hit_block_record.json,
  which is the original run's record of that block.
- On one core this takes about a minute. how-we-built-it/REBUILD_OUTPUT.txt is the real output of this command, run
  from this package's copy of the script.

The search's frozen plan is how-we-built-it/PREREG.md. how-we-built-it/selftest_output.txt is the pipeline's
pre-attack self-test on the same base set, through the same screen: six of Fischer's own table pairs in (10^12,
4.8·10^12) were all recovered, with no unlisted hit.
