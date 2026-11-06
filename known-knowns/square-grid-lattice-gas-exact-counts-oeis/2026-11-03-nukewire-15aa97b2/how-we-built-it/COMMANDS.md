# The exact commands that built the object (2026-11-01..03 sessions)

Run A (row sweeps; one sweep at width k records the whole column T(1..28,k)
because the frontier empties at every row boundary):

    python runA_rowsweep.py gate            # 336/336 exact vs from-definition DP
    python runA_rowsweep.py work output/runA_residues.txt 2026-11-01T12:30:00Z
    # 13 set-A primes = first proven primes > 2^61 + 1e6 (primes_A.txt);
    # ~21 min/prime; completed 2026-11-01 (9828 residue lines)

Run B (column sweep at width 28, two-half in-place layout, ~3.2 GB peak; the
memory-strategy change from the monolithic plan is documented in
PREREG_v2_2026-11-02.md; derivation and gates in PREREG_v3 and the run folders):

    python runB_chunked.py gate             # plain exact n=1..12 vs diagonal
    python runB_chunked.py gate-chunk       # sliced path n=1..12
    python runB_chunked.py validate         # width-20 vs runA residue: MATCH
    python probe_fullwidth.py               # 28/28 columns == runA residues
    python runB_chunked.py work output/runB_residues.txt 2026-11-02T17:00:00Z
    # 13 set-B primes = first proven primes > 2^61 + 1e8 (primes_B.txt);
    # ~17-23 min/prime; completed 2026-11-02 (364 residue lines)

The two-run gate and the row object:

    python crt_ab.py    # TWO-RUN GATE PASS: 27/27 cells agree; k=28 == a(28)

null_test: not needed — explicit object checked by a deterministic checker
(see the PREREG chain, v1 section "Null test").
