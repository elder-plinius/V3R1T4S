# Commands (contributor code, from how-we-built-it/; Linux, gcc, Python 3 with python-flint 0.9.0, numpy, scipy)
In these package copies, the scripts' absolute workspace paths were replaced by relative defaults ("work",
"data/dunn_V_list_lfs.jld2", "python3"). Nothing else was changed (the run folder keeps the originals).

```sh
export BRUN_WORK=$PWD/work && mkdir -p work
gcc -O2 -o vsieve code/vsieve.c && ./vsieve 10000000 10000000 work/V_1e7_unused.bin work/M_1e7.bin    # exact M(z), z <= 1e7 (~1 s)
gcc -O2 -march=native -o vsieve_fx code/vsieve_fx.c -lpthread -lm
./vsieve_fx chunks 10000000000 10000 5 work/Vfx_chunks_1e10.bin     # ~1 min on 5 cores; prints V_lo(1e10) = 18.401710861595...
./vsieve_fx dense 100000000 work/Vfx_dense_1e8.bin                   # ~10 s, 800 MB
python3 code/replay.py --prec 128                                     # R  = 2.1593210323778804655 (Dunn's inputs, rigorous)
python3 code/replay.py --cpi q --prec 256                             # U' = 2.1569562895056571339 (change B alone)
python3 code/replay.py --cpi q --c1 li --vlemma own --prec 256        # U''= 2.1569669355299578202 (headline, before the pi_2(z) term)
python3 code/replay.py --cpi q --c1 li --vlemma own --prec 128 --cert cert_U2.json   # per-interval certificate
python3 code/vlemma.py                                                # A(1e10) <= 0.010700091 at s = 0.44
```
object/a_bound_certificate.json is cert_U2.json with the claim, the framework reference and the midpoint rule added as
fields (same "intervals" list, same B_upper_without_pi2z value). Optional: code/compare_tables.py (needs Dunn's
V_list.jld2 from his repository, and h5py) and code/check_lemma21.py (an empirical check, not a proof).
Outputs from the run are in out/. CLAIM.md is the claim as revised at the gate; CLAIM_CHANGES.md lists the
revisions against the panelled version.
