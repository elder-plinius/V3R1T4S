# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 83
    r* = 0.25201068494708888664310142074008333009469420727062
    table = 0.252008330509
    gain = 0.00000235443808888664310142074008333009469420727062
    posted r* = 0.25200833050819199120312670054400392305886022100759 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.01185410297206684907842685451416018470281553047722
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-83.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
