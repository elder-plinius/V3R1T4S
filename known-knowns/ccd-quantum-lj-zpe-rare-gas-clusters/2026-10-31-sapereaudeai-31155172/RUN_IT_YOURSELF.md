# Run it yourself

From this folder, in a fresh shell, with Python 3 and numpy:

    sh verify-it-yourself/run_checks.sh

Expected output ends with:

    E_Ne = E_LJ + (0.095/2) * sum sqrt(lambda) = -108.929936
    record test Ne: bar -107.42431, E_sp -108.929936, bar - E_sp = 1.505626 (need >= 5e-04 on a certified minimum): BEATS BAR
    RESULT: PASS
    PASS

The criterion's calibration step uses the table's posted point files. They are not included here (third-party
data); fetch them once from the table's own archive link:

    mkdir points && cd points && curl -sSL -A "V3R1T4S verifier" -o all.tar http://www-wales.ch.cam.ac.uk/~florent/LJZPE/points/all.tar && tar -xf all.tar && cd ..
    python3 -I verify-it-yourself/check_lj_zpe.py points/17A --polish --expect Xe=-58.67010 --expect Ar=-53.37432 --expect Ne=-36.16303
    python3 -I verify-it-yourself/check_lj_zpe.py points/31B --polish --expect Xe=-128.09768 --expect Ar=-117.70540 --expect Ne=-83.93050
    python3 -I verify-it-yourself/check_lj_zpe.py points/38A --polish --expect Xe=-166.82835 --expect Ar=-152.62818 --expect Ne=-106.47765
    python3 -I verify-it-yourself/check_lj_zpe.py points/38B --polish --expect Xe=-162.08887 --expect Ar=-149.22662 --expect Ne=-107.42431

Each prints `RESULT: PASS` (all |diff| < 5e-5). `--polish` is a Newton polish on the classical surface, used for
calibration only, because the posted files carry about 7 digits. The object is checked as written, with no polish.

To rebuild the object, see `how-we-built-it/COMMANDS.md` (stochastic search; a rerun finds its own minima).
