# Reproduce (Linux, gcc with __int128, Python 3 with python-flint 0.9.0, numpy, scipy). Run from the package folder.
export BRUN_WORK=$PWD/work && mkdir -p work
# Tables (same as e6b84d42; ~5 min, ~1.6 GB disk)
gcc -O2 -o work/vsieve how-we-built-it/code/vsieve.c && work/vsieve 10000000 10000000 work/V_1e7_unused.bin work/M_1e7.bin
gcc -O2 -o work/vsieve_fx how-we-built-it/code/vsieve_fx.c -lpthread -lm
work/vsieve_fx chunks 10000000000 10000 6 work/Vfx_chunks_1e10.bin
work/vsieve_fx dense 100000000 work/Vfx_dense_1e8.bin
gcc -O2 -o work/wsieve_fx how-we-built-it/code/wsieve_fx.c -lpthread -lm
work/wsieve_fx dense 10000000 work/Wfx_dense_1e7.bin
work/wsieve_fx chunks 10000000000 10000 6 work/Wfx_chunks_1e10.bin
# NEW: exact per-modulus accumulator
gcc -O2 -o work/rhofx how-we-built-it/code/rhofx.c
python3 how-we-built-it/code/lamfx.py work/rhofx 300 2740 20000                       # Sigma upper, Lambda^2, ratio, 'Lambda==W/V', 'lam1=1' (~10 s)
# Main result (~75 s each; 128 and 256 bits print the same B_upper)
python3 how-we-built-it/code/rho_bound.py --r selberg --cpi q --c1 li --vlemma own --bracket free --sprime how-we-built-it/out/sprime.json --rho work/rhofx --prec 128 --cert work/cert.json
#   -> B_upper 2.1257394310040893870; work/cert.json has the same intervals and rho_levels as object/a_bound_certificate.json
#      (its "options" field records these package-relative paths, so the bytes differ; run from the claim folder it is byte-identical)
python3 how-we-built-it/code/rho_bound.py --r selberg --cpi q --c1 li --vlemma own --bracket free --sprime how-we-built-it/out/sprime.json --rho work/rhofx --prec 256
# Controls
python3 how-we-built-it/code/rho_bound.py --r selberg --cpi q --c1 li --vlemma own --bracket free --sprime how-we-built-it/out/sprime.json --prec 128   # K1: 2.1269872000642055706
gcc -O2 -o work/rho_ld how-we-built-it/code/rho_longdouble_lead.c -lm
python3 how-we-built-it/code/controls.py work/rhofx work/rho_ld how-we-built-it/out/rho_exact_p128.json      # K3 (exact Fractions, n <= 300) and K4 (vs long double); PASS
python3 how-we-built-it/code/control_K5.py work/rhofx how-we-built-it/out/rho_exact_p128.json                # K5: lambda_1 = 1, Lambda == W/V exactly, tables; PASS
# Threads (post-panel erratum (d)): verify/wvcount.c, run by the checker, uses min(8, cpu count) threads by default
# (check_rho.py passes max(1, min(8, os.cpu_count())) to it). To limit cores, pin the run, e.g.
#   taskset -c 0-2 sh verify-it-yourself/run_checks.sh     (3 cores; os.cpu_count() still reports all cores, so threads are time-shared on the pinned ones)
# There is no environment variable for it; rhocount.c and the arb parts are single-threaded.
# Standalone check (needs no tables; ~70 s per precision on 1 core for the rho part + the e6b84d42 part)
sh verify-it-yourself/run_checks.sh                                                       # 128 and 256 bits; last line PASS
python3 verify-it-yourself/tamper_tests.py                                                # K6: 5 corrupted certificates, all must FAIL
- 2026-11-24T07:54Z: fresh copy of claim/ (sandbox): verify/run_checks.sh PASS at 128 and 256 (B <= 2.1257393973040676877); how-we-built-it/code/rho_bound.py --prec 128 rerun from the copy (existing tables via BRUN_WORK) gives B_upper 2.1257394310040893870 and a byte-identical certificate (out/check_rho_both_fresh_copy.txt, out/fresh_copy_program.txt). Tables were not rebuilt in this run (they were rebuilt from scratch in runs/2026-11-24-0527 at 05:57Z with the same code).
