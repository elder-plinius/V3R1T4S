# Run it yourself (fresh shell, from this folder)

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS (it recomputes the pooled Naibbe H1 from objects/pooled_{A,B}.wrapped.txt
and checks it is below the 99.9% Voynich envelope bounds on both dialects + both transliterations,
below the 16,000-control minima, and that all 20 per-plaintext means are outside).

Rough laptop time: ~30 s (the H1 re-derivation is the cost; a memoized lev1).

To rebuild the object from scratch (not needed to check it; this is how it was made):
    cd <run>/attempts/falsifier && python3 code/run_naibbe_batch.py     # 200 runs -> naibbe_batch.json
    python3 <run>/code/dump_pooled.py                                   # -> pooled_{A,B}.wrapped.txt
    python3 <run>/code/precompute.py && python3 <run>/code/env_worker.py H1 A ZL3b   # envelopes
    python3 <run>/code/null_recheck.py                                   # the 16,000-control null (PASS)
(requires the run's data/ ZL3b-n.txt + IT2a-n.txt and the pinned driver's Naibbe tables; stdlib only.)
