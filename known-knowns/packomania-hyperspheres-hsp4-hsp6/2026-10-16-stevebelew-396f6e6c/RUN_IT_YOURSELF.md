# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 74
    r* = 0.25852965066023519309129266203951598448314323656090
    table = 0.258522851648
    gain = 0.00000679901223519309129266203951598448314323656090
    posted r* = 0.25852285164722350934031567238681935996897324470926 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00728408716400186230812149111527261043168516035863
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-74.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
