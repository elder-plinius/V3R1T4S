# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
object: object/a204371_37.txt
n=37 rule=110 claimed_period=4403 witness=0x1c7dbbb23e
bit_order: cell0=LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic
divisors: 1 7 17 37 119 259 629 4403
after 4403 steps: state=0x1c7dbbb23e start=0x1c7dbbb23e returned=yes
divisor 1: state=0x1647eefb23 equals_start=no
divisor 7: state=0x47d0fb23b equals_start=no
divisor 17: state=0x11f43ecbec equals_start=no
divisor 37: state=0x1f43b23ec8 equals_start=no
divisor 119: state=0x16eec8fb8f equals_start=no
divisor 259: state=0x1b8fb23f77 equals_start=no
divisor 629: state=0x1d91f647ce equals_start=no
first_return: 4403
shorter_period_divisors: none
period_confirmed: 4403
result: ok
PASS
```
The last line is PASS. A fraction of a second on a laptop. This check confirms the witness period only. It does not re-run the exhaustive census.

## Live table
Open https://oeis.org/A204371 and https://oeis.org/A204371/b204371.txt. The claim that the term is new holds while neither lists a value for n=37. At the packaging snapshot the b-file and the DATA line both ended at n=36, a(36)=1584.

## Rebuild and re-run the search programs
The two C11 programs are in how-we-built-it/impl1/maxcycle.c and how-we-built-it/impl2/maxcycle.c (a C compiler is required). From how-we-built-it/:

```
./build.sh
RULE=110 N=31 IMPL=1 WORKDIR=work/heldout_n31 ./run.sh
RULE=110 N=31 IMPL=2 WORKDIR=work/heldout_n31 ./run.sh
```

At width 31 both programs should print max_period=2759, which is the live OEIS term A204371(31). Peak memory is about 256 MiB (impl1) or 512 MiB (impl2). The packaging-run outputs are in how-we-built-it/heldout/.

A full self-test (A334497(1..24) and A204371(1..30), plus a report of A334497(25..30)) is `./selftest.sh` from the same folder. That script compares against OEIS b-files which are not included here (third-party data); fetch https://oeis.org/A334497/b334497.txt and https://oeis.org/A204371/b204371.txt into how-we-built-it/data/ first. The log and witness files from the original self-test, already compared, are in how-we-built-it/selftest/.

Width 37 is a large job: impl1 needs a 16 GiB bitset (about half an hour on the machine that produced this claim) and impl2 needs a 32 GiB colour array (a few hours). Do not start it on a machine without that much free memory. `./run.sh` will refuse to start if the array would not fit. Commands:

```
RULE=110 N=37 IMPL=1 WORKDIR=work/r110_n37 ./run.sh
RULE=110 N=37 IMPL=2 WORKDIR=work/r110_n37 ./run.sh
```

Expected result lines (from how-we-built-it/results/):

```
rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e time_sec=1699.3565 impl=1
rule=110 n=37 max_period=4403 witness=0x1c7dbbb23e time_sec=11946.5399 impl=2
```

## Rebuild the object
The object file is the term and witness, not a compiled artifact. After a fresh n=37 run, the result line should match object/a204371_37.txt: n=37, rule=110, max_period=4403, witness=0x1c7dbbb23e.
