# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 75
    r* = 0.25808612483722137340564182868577520221606981638184
    table = 0.258082894946
    gain = 0.00000322989122137340564182868577520221606981638184
    posted r* = 0.25808289494565822872505347353145241437235369820641 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00798042775131095940371051214315138431395796966322
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-75.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
