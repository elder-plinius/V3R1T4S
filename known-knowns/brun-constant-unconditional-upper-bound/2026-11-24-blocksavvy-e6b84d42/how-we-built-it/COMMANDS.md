# Commands that built the object (Linux, gcc, Python 3 with python-flint 0.9.0, numpy, scipy). Run from the package folder.
export BRUN_WORK=$PWD/work && mkdir -p work
gcc -O2 -o work/vsieve how-we-built-it/code/vsieve.c && work/vsieve 10000000 10000000 work/V_1e7_unused.bin work/M_1e7.bin   # exact M(z), z <= 1e7
gcc -O2 -o work/vsieve_fx how-we-built-it/code/vsieve_fx.c -lpthread -lm
work/vsieve_fx chunks 10000000000 10000 6 work/Vfx_chunks_1e10.bin     # exact fixed-point V lower bounds, ~1 min
work/vsieve_fx dense 100000000 work/Vfx_dense_1e8.bin                   # 800 MB
gcc -O2 -o work/wsieve_fx how-we-built-it/code/wsieve_fx.c -lpthread -lm
work/wsieve_fx dense 10000000 work/Wfx_dense_1e7.bin                    # W upper bounds, prints Whi(1e7) = 7573985.94...
work/wsieve_fx chunks 10000000000 10000 6 work/Wfx_chunks_1e10.bin      # prints Whi(1e10) = 7573900191.97...
python3 how-we-built-it/code/sprime.py 128 work/sprime_rerun.json                       # S'(s) bounds, compare out/sprime.json
python3 how-we-built-it/code/check_lambda.py                                            # weights vs W/V identity, exact rationals (~25 s)
python3 how-we-built-it/code/indep_W.py                                                 # W tables vs an independent computation
python3 how-we-built-it/code/selberg_bound.py --r selberg --cpi q --c1 li --vlemma own --bracket free --prec 256 --sprime how-we-built-it/out/sprime.json   # B_upper 2.1269872000642055706
python3 how-we-built-it/code/selberg_bound.py --r M --cpi q --c1 li --vlemma own --prec 128 --sprime how-we-built-it/out/sprime.json                       # control: 2.1569669355299588530
python3 how-we-built-it/code/vlemma.py                                                  # A(1e10) <= 0.0107001 (V lemma, inherited)
# Standalone check (independent of the tables above; ~30 s):
sh verify-it-yourself/run_checks.sh                                                 # 128 and 256 bits; last line PASS
- 2026-11-24T05:57Z: REPRODUCE.md rerun from a fresh copy of claim/ (all tables rebuilt): W/V tables, sprime, C2/C3, indep_W PASS; selberg 2.1269872000642055706 and control 2.1569669355299588530 identical; verify/run_checks.sh PASS (B <= 2.1269871669853558245).
python3 how-we-built-it/code/selberg_bound.py --r selberg --cpi q --c1 li --vlemma own --bracket free --prec 128 --sprime how-we-built-it/out/sprime.json --cert work/cert.json   # same intervals as object/a_bound_certificate.json (only the 'options' paths differ; checked 2026-11-24T06:18Z)
