# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 88
    r* = 0.24851407139040025934558484215530328638211795818054
    table = 0.248505598356
    gain = 0.00000847303440025934558484215530328638211795818054
    posted r* = 0.24850559835516205845593916198371092216981064525629 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.01570545602964661198051749303473821676212027560111
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-88.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
