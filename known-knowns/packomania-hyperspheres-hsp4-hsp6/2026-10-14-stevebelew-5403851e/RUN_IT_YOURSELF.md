# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 48
    r* = 0.28398054846874193052841907323739266845744875945232
    table = 0.283980525334
    gain = 2.313474193052841907323739266845744875945232E-8
    posted r* = 0.28398052533300828944975939435324348821153451449657 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.05362876656986979866497723307853933662061108356989
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-48.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
