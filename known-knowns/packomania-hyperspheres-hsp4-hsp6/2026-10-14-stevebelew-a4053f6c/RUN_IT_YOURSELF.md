# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 64
    r* = 0.26680295830395308096301031961740075212031177022409
    table = 0.266800405039
    gain = 0.00000255326495308096301031961740075212031177022409
    posted r* = 0.26680040503881106522160674323861008984985429653876 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.00776522607613052927133789808004208020323218312119
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-64.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
