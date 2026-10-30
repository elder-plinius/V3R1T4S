# Run it yourself

## Verify (standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (exact digits):

    N = 80
    r* = 0.25546960698484976114380247994819295250762415251867
    table = 0.255463163131
    gain = 0.00000644385384976114380247994819295250762415251867
    posted r* = 0.25546316313059780968673693299770746381667479640126 (reproduces table within 1e-11: True )
    max |sorted distance difference| vs posted = 0.0122062833609006615959293610584759345431462039838
    PASS

## Rebuild the object (optional; needs numpy and scipy, see how-we-built-it/requirements.txt)

The object was produced by how-we-built-it/run_polish.py (seeded, deterministic per N: `numpy.random.default_rng(1000 + N)`)
starting from Packomania's posted hsp4-80.txt. The script expects the run layout described in how-we-built-it/COMMANDS.md.
Heuristic search is not guaranteed to reproduce the same packing on other hardware; the checker above is what matters.
