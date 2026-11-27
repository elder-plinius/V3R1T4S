# Run it yourself (fresh shell, from this package folder)

## 1. Standalone check (python3 standard library, a few seconds)
    sh verify-it-yourself/run_checks.sh                     # last line PASS (see verify-it-yourself/RECEIPTS.md)
    FLINT=1 sh verify-it-yourself/run_checks.sh             # with python-flint==0.9.0: also recomputes chunks n0 = 1, 300001, 1462801, 2325201

## 2. Full recomputation (python3 with python-flint==0.9.0, about 4-6 CPU-hours; use WORKERS cores)
    pip install -r how-we-built-it/requirements.txt
    mkdir -p work/claim/code work/claim/result work/claim/inputs
    python3 how-we-built-it/code/k2_chunks.py 1 600000 400 WORKERS work/claim/chunks_head128 128
    python3 how-we-built-it/code/k2_chunks.py 600001 2325573 400 WORKERS work/claim/chunks_tail 96
    curl -o work/claim/inputs/bzyzz_k2_certificate.json https://raw.githubusercontent.com/bzyzz/mertens_bound/a0b267c2/certification/k2_certificate.json
        # sha256 811145be4741c4cb42f9fe1e5eefca2ffc9ee01bbfae32925ca2db0a85df48ff
    cp how-we-built-it/code/aggregate_claim.py work/claim/code/ && python3 work/claim/code/aggregate_claim.py
        # K2 = [1.00030525038651 +/- 5.07e-15], contained_in_bzyzz_K2 true (compare how-we-built-it/outputs/aggregate_claim.json)
    python3 how-we-built-it/code/build_object.py work/claim work/object
        # work/object/*.jsonl and k2_result.json should be byte-identical to object/

Each chunk stores S = sum of exp(-k g^2) Re(e^{igv}/(rho zeta'(rho))) over its zeros (without the factor 2). Chunks n <= 600,000 use
128-bit balls (96 bits is too coarse there: the gamma radius times v ~ 3.5e18 enters the phase); the tail uses 96 bits.
The last chunk includes n = 2,325,573 (gamma > 1.3e6), whose term is subtracted (object/k2_result.json, excluded_term_n2325573_half).

## What is not shipped
- The run's 5,814 per-chunk JSON files (chunks_head128, chunks_tail): every field of each (n0, cnt, prec, g_first, g_last, S, Abs,
  min |zeta'|) is in object/*.jsonl, one line per chunk, in n order; only the file wrapper is dropped.
- The superseded 96-bit head chunks (chunks_head, 1,500 files): a wider cross-check kept in the run; its aggregate is
  how-we-built-it/outputs/aggregate_claim_head96.json.
- The third-party bzyzz files (certificate JSON, README, Table 1): cited by URL and sha256 in the-record-we-beat/README.md, not copied.
