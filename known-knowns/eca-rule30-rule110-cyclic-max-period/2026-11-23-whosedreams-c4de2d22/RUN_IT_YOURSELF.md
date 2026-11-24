# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md; only the elapsed_sec line varies):
```
object: object/a334497_37.txt
n=37 rule=30 claimed_period=49276415 witness=0x7fbfe703e
bit_order: cell0=LSB, idx=(L<<2)|(C<<1)|R, L=i-1, R=i+1 cyclic
step_crosscheck: fast step equals per-cell definition for the first 2000 steps
divisors: 1 5 37 185 266359 1331795 9855283 49276415
after 49276415 steps: state=0x7fbfe703e start=0x7fbfe703e returned=yes
divisor 1: state=0x808039843 equals_start=no
divisor 5: state=0x909ba0e6c equals_start=no
divisor 37: state=0x1463aa56b6 equals_start=no
divisor 185: state=0x179b120968 equals_start=no
divisor 266359: state=0x10ec393945 equals_start=no
divisor 1331795: state=0x1eff9c0f8f equals_start=no
divisor 9855283: state=0x740e77ad2 equals_start=no
first_return: 49276415
shorter_period_divisors: none
elapsed_sec: 33.2
period_confirmed: 49276415
result: ok
PASS
```
The last line is PASS. About 30 to 60 seconds on a laptop. This check confirms the witness period only. It does not re-run the exhaustive census.

## Live table
Open https://oeis.org/A334497 and https://oeis.org/A334497/b334497.txt. The claim that the term is new holds while neither lists a value for n=37. At the packaging snapshot the b-file and the DATA line both ended at n=36, a(36)=2237472.

## Rebuild and re-run the search programs
The two C11 programs are in how-we-built-it/impl1/maxcycle.c and how-we-built-it/impl2/maxcycle.c (a C compiler is required). From how-we-built-it/:

```
./build.sh
mkdir -p work
nice -n 19 impl1/maxcycle --rule 30 --n 31 --witness-out work/w1.txt
nice -n 19 impl2/maxcycle --rule 30 --n 31 --witness-out work/w2.txt
```

At width 31 both programs should print max_period=2841150 (the listed A334497(31)); `--rule 110 --n 31` should give 2759 (A204371(31)). Peak memory is about 260 MiB (impl1) or 540 MiB (impl2). The PC-run outputs are in how-we-built-it/heldout/.

The whole pipeline that produced this claim is how-we-built-it/run_r30.sh (self-test, held-out check, width 37 with impl1 then impl2, witness check). It compares against OEIS data files that are not included here (third-party data): put https://oeis.org/A334497/b334497.txt, https://oeis.org/A204371/b204371.txt and a file data/a334496_data.txt with the line `37 49276415` (from https://oeis.org/A334496/b334496.txt) into how-we-built-it/data/ first. `SMOKE=1 ./run_r30.sh` runs the same pipeline at widths up to 20 in about a minute. The one line changed from the run copy is the default Windows Downloads folder (see how-we-built-it/COMMANDS.md).

Width 37 is a large job: impl1 needs a 16 GiB bitset (about 62 minutes on the machine that produced this claim) and impl2 needs a 32 GiB colour array (about 11.4 hours). Do not start it on a machine without that much free memory; run_r30.sh refuses to start a program whose array would not fit. Direct commands:

```
nice -n 19 impl1/maxcycle --rule 30 --n 37 --witness-out work/w37_1.txt
nice -n 19 impl2/maxcycle --rule 30 --n 37 --witness-out work/w37_2.txt
```

Expected result lines (from how-we-built-it/results/):

```
rule=30 n=37 max_period=49276415 witness=0x7fbfe703e time_sec=3739.3822 impl=1
rule=30 n=37 max_period=49276415 witness=0x7fbfe703e time_sec=41058.0073 impl=2
```

## Rebuild the object
The object file is the term and witness, not a compiled artifact. After a fresh n=37 run, the result line should match object/a334497_37.txt: n=37, rule=30, max_period=49276415, witness=0x7fbfe703e.
