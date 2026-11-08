# Run it yourself

object/PROOF.md and panel/ use the run's folder names: checkers/ and tests/ are verify-it-yourself/, REPRODUCE.md is this file, CLAIM.md is README.md, table/ is the-record-we-beat/.

From this folder, in a fresh shell. C compiler and Python 3 standard library only.

## Quick check (a few seconds)

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS.

## The N = 17 certificate

Rebuild the three large files (about 15 minutes on one core; mdp3 peak about 1.3 GB, prod4 peak about 2.54 GB; about 1.7 GB of disk for the result, and scratch use during the run was not measured separately). The commands use a new folder BIN of your own:

    mkdir BIN
    cc -O2 -o BIN/mdp3 how-we-built-it/mdp3.c -lm
    cc -O2 -D_FILE_OFFSET_BITS=64 -o BIN/prod4 how-we-built-it/prod4.c -lm
    BIN/mdp3 14 2000 1.5e-4 BIN/Q14.bin 700
    POLISH=150 POLISH_CAP=1500 THETA=0.005,0.003 BIN/prod4 17 14 BIN/Q14.bin BIN/c17 2 20 3 3000 9e8 30

BIN/c17.counts, BIN/c17.states and BIN/c17.V are the certificate. They can also be downloaded from https://doi.org/10.5281/zenodo.24051334 instead of rebuilt. Compare with the sha256 values in object/CERTIFICATE.md. On the machine that made them, reruns on 2026-11-01 and 2026-11-07 were byte-identical. Elsewhere float rounding may change them. The runs also have wall-clock caps: mdp3 stops after 700 s (here it converged after 38 s), prod4 after 3000 s, and its polish after POLISH_CAP = 1500 s (here all 150 sweeps ran and prod4 ended at 729 s). On a machine several times slower, a cap can stop a run early. In either case the lowest value printed below could shift.

Check it (under a minute each; check_a17 about 1.7 GB, check_d about 70 MB, check_e a few MB):

    cc -O2 -D_FILE_OFFSET_BITS=64 -o BIN/check_a17 verify-it-yourself/check_a17.c
    cc -O2 -o BIN/check_d verify-it-yourself/check_d.c
    cc -O2 -o BIN/check_e verify-it-yourself/check_e.c
    BIN/check_a17 17 16777216 13332272 BIN/c17.counts BIN/c17.states BIN/c17.V
    BIN/check_d 17 16777216 13332272 BIN/c17.counts BIN/c17.states BIN/c17.V
    BIN/check_e 17 16777216 13332272 BIN/c17.counts BIN/c17.states BIN/c17.V

Expected last lines: `ACCEPT claimed m=13332272, L=m/K=13332272/16777216=0.794665336609`, then `ACCEPT m=13332272 K=16777216` twice.

Must refuse, for each of the three checkers (shown for check_d; the same three lines with check_a17 and check_e):

    BIN/check_d 17 16777216 13332273 BIN/c17.counts BIN/c17.states BIN/c17.V
    BIN/check_d 17 16777216 13332272 BIN/c17.counts BIN/c17.states BIN/c17.V perturb
    BIN/check_d 17 16777216 13332272 BIN/c17.counts BIN/c17.states BIN/c17.V drop

## Other tests

    cc -O2 -o BIN/sim_rate17 verify-it-yourself/sim_rate17.c; BIN/sim_rate17 17 BIN/c17.counts BIN/c17.states 200000000 7

prints a simulated rate, numerical only: 2R/T = 0.794670 at this seed. verify-it-yourself/sim_check.py compares the process with a plain DP on real strings, at N = 8:

    python3 -I verify-it-yourself/sim_check.py 8 object/small_old/c8.states 12000 21
