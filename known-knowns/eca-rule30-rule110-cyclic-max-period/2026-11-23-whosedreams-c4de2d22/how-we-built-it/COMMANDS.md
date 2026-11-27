# Commands (as the search was run, and as this packaging run checked it)

## Source
The PC run kit was sent out as a tarball with sha256 51a9219af43b20178afcde5ff504dae33ec5e47f05e1e24ca66c6a97bd44714a. The files in this folder are byte-identical to that kit's impl1/maxcycle.c, impl2/maxcycle.c, build.sh, status.sh and check_period.py; logs/kit_sha256.txt (written by the kit at the end of the run) lists the sha256 of each source, of both compiled binaries on the PC, and of the OEIS data files the self-test compared against.

One file differs from the run copy: in run_r30.sh, line 15, the default copy-to folder for the finished send-back archive, a personal Windows path, is replaced by an empty default (set WIN_DL to a folder to get the extra copy). The run copy had sha256 1f33388a407540c55a627ac32cc91c320ed66b0fde2d3eb78517b7634d18141d (as in logs/kit_sha256.txt). That line only decides where the archive is copied; it does not touch any computation. In logs/run.log the PC home folder is likewise written as `~` (three lines), and in logs/sysinfo.txt the host name and the kernel build-host string are removed. Nothing else in the logs was changed.

The programs are the same as in the Rule 110 width-37 package (V3R1T4S PR #1173, how-we-built-it/impl1 and impl2 there): impl1 sha256 9e24406731671802a57bdc13dd3f2a3b47c1f0ddbba4876ad2ff133a61a330cc, impl2 sha256 bf2321ce02bef42ef6fe45219c39b85832af35694d054704f664051c2a7333bc.

## Build
```
./build.sh          # cc -O3 -march=native, impl1/maxcycle and impl2/maxcycle
```
On the PC: cc (Ubuntu 15.2.0-16ubuntu1) 15.2.0, Python 3.14.4 (logs/sysinfo.txt).

## The run
```
nohup nice -n 19 ./run_r30.sh > run_console.txt 2>&1 &
./status.sh         # progress
```
Stages, in order (logs/run.log):
1. selftest, 2026-11-22 13:06:22 to 13:15:01 ET (18:06:22Z to 18:15:01Z): both programs, A334497(1..30) at Rule 30 and A204371(1..30) at Rule 110, compared with the OEIS b-files. Log selftest/selftest.log: 108 OK lines (A334497(1..24) and A204371(1..30), two programs) and 12 REPORT_MATCHES_LISTED lines (A334497(25..30), two programs; every reported value equals the listed term). No BUG or MISMATCH line. Per-width outputs in selftest/r30_nN/ and selftest/r110_nN/.
2. heldout, to 13:24:13 ET: both programs at width 31, Rule 110 (2759 = A204371(31)) and Rule 30 (2841150 = A334497(31)). heldout/, including check_period_r110.txt (PASS).
3. main impl1, Rule 30, n=37: 13:24:13 to 14:26:39 ET. results/result_impl1.txt:
   `rule=30 n=37 max_period=49276415 witness=0x7fbfe703e time_sec=3739.3822 impl=1`; peak RSS 16791800 kB.
4. main impl2, Rule 30, n=37: 2026-11-22 14:26:39 ET to 2026-11-23 01:51:05 ET (06:51:05Z). results/result_impl2.txt:
   `rule=30 n=37 max_period=49276415 witness=0x7fbfe703e time_sec=41058.0073 impl=2`; peak RSS 33943584 kB.
5. check: results/compare.txt (AGREE max_period=49276415; FLOOR_OK A334496(37)=49276415) and check_period.py on each witness, results/check_period_impl1.txt and check_period_impl2.txt (PASS, return at 49276415, none at 49276415/5, /37 or /266359).

Some peak_rss_kB files for tiny widths read 2 to 8 kB; the kit samples memory while a program runs, and those programs finished before a useful sample. They carry no result.

## Witness period (this packaging run)
From the package root:
```
sh verify-it-yourself/run_checks.sh
```
Expected last line: PASS. Output in verify-it-yourself/RECEIPTS.md.
