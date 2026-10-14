# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 69
    r* = 0.26191681458304926606905286157526151565663762364520
    table = 0.261916266401
    gain = 5.4818204926606905286157526151565663762364520E-7
    posted r* = 0.26191626640033752110213750374288630262172659940161 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00662826312033062966529272076739148487360361356005
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-69.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
