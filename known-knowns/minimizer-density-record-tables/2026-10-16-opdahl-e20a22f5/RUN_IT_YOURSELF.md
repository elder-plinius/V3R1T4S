# Run it yourself

Do these steps in this folder:

1. Open a shell.
2. Run this command:

       sh verify-it-yourself/run_checks.sh

The last line of the output must be PASS. The command needs two to four minutes on a laptop.

Requirements: python3 (3.9 or later) and numpy. No other package is necessary.

## What the check does

The file `verify-it-yourself/check.py` does these steps:

1. It reads `object/order.txt` and `object/order.json`.
2. It compares the two files. The order in both files must agree.
3. It examines the order. The order must contain each number from 0 to 7 one time.
4. It measures this order and the incumbent GreedyMini order over 2000000 windows on seeds 0, 1 and 2.
5. It compares the two values with the smallest listed table value.
6. It prints PASS or FAIL.

The rank composition comes from the published notebook `greedymini_density.ipynb`. The file `check.py`
quotes the composition.

## How to rebuild the object

The search code is in `how-we-built-it/`. The code enumerates the 40320 orderings of the eight
projected classes. The code ranks the orderings on a short sequence. Then the code ranks the best
orderings again on longer sequences. The file `how-we-built-it/PREREG.md` is the plan. The plan was
frozen before the first measurement.

## Note about the measurement code

The file `check.py` uses the composition that the published notebook gives: the high-bit projection and
the rank

    (((order[bin_kmer] << (2*k)) + kmer) << (8*k)) + get_kmer_id_dna(k, km, seed)

An earlier version of the checker from the run used a low-bit projection and omitted the term
+ kmer. The file `panel/gate.md` records both compositions and their measured values. The claim holds
for both compositions. This package uses the composition of the notebook.
