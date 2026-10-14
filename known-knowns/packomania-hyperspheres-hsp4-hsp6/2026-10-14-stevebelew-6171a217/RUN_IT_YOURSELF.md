# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 42
    r* = 0.29336921747731549412694964078388454032569439060526
    table = 0.293368844389
    gain = 3.7308831549412694964078388454032569439060526E-7
    posted r* = 0.29336884438873034433657018132386765355532836405989 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.04078680382740889064871228961521831879353641566043
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-42.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
