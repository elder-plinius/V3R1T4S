# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 89
    r* = 0.24800542008440667899066559596859197503166605598113
    table = 0.247998099891
    gain = 0.00000732019340667899066559596859197503166605598113
    posted r* = 0.24799809989033811121926269724249286997438597696443 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.01120635152360802610321951338680514634794963033876
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-89.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
