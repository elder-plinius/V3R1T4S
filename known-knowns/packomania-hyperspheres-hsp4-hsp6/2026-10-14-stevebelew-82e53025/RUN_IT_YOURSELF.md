# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 62
    r* = 0.26883347811496426252013431587660236159020739032672
    table = 0.268830626376
    gain = 0.00000285173896426252013431587660236159020739032672
    posted r* = 0.26883062637545371685989373339364543178673411520049 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00649375747233289049206122216749139352889328526551
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-62.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
