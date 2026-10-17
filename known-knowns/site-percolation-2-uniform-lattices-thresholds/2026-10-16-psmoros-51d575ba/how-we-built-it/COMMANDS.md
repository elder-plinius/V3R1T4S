# Commands (adapted from the claim's REPRODUCE.md; run from the package folder in a fresh shell)

Needs clang (or any C/C++17 compiler) and python3 (standard library only). No network, except where noted for the
Wikipedia page, which this package does not contain. Times are from a shared 12-core machine under load; the W = 9 and
W = 10 runs are the slow ones.

Files: code/tm/tm.cpp (slot/operation transfer matrix, C++), code/eig/eig.c with code/eig/mkgraph.py (a separately
written program that takes a torus graph as input, C), code/tm/extrap.py (PREREG rule 4), code/check/sigma_v2.py
(PREREG.v2), code/eig/extrap_eig.py (rule 4 on the eig table), code/check/q9_check.py (lattice builder, table parser,
criterion arithmetic). data/tm/*.tsv: tm roots (columns W, p(W), seconds, state counts); data/eig/*.tsv: eig roots
(also for neighbouring rows TS, TSSS, TTS, TTTS, which are not claimed here); data/eigT/: transposed-orientation runs
(diagnostic only). PREREG.md and PREREG.v2.md: the run's frozen rules.

## 1. Lattice identity
    python3 how-we-built-it/code/check/q9_check.py lattice TSS
    # expect config {'3^3.4^2': '2/3', '4^4': '1/3'}, zbar 14/3 (row #22: (2/3)(3^3,4^2) + (1/3)(4^4), z-bar 4 2/3)
    # with the page saved as page.html (one plain GET of https://en.wikipedia.org/wiki/Percolation_threshold):
    python3 how-we-built-it/code/check/q9_check.py table page.html | grep -A12 '"num": 22'

## 2. Build both transfer-matrix programs
    mkdir -p bin
    clang++ -O3 -std=c++17 -o bin/tm how-we-built-it/code/tm/tm.cpp
    clang -O2 -o bin/eig how-we-built-it/code/eig/eig.c -lm

## 3. Exact checks (must print f ~ 0 at every W)
    for W in 3 4 5 6; do bin/tm S bond $W eval 0.5 | tail -1; done
    for W in 3 4 5 6; do bin/tm T site $W eval 0.5 | tail -1; done
    for W in 3 4 5; do bin/tm T bond $W eval 0.34729635533386069 | tail -1; done
    # compare with how-we-built-it/data/tm/exact_tests.txt

## 4. The TSS bond roots p(W) (compare with object/TSS_bond_roots.tsv and how-we-built-it/data/eig/bond.tsv)
    for W in 2 3 4 5 6 7 8; do bin/tm TSS bond $W root 0.4452 0.4454 1e-14 | tail -1; done      # seconds to minutes
    bin/tm TSS bond 9 root 0.445287 0.4452872 1e-14 | tail -1                                   # several minutes
    bin/tm TSS bond 10 root 0.445287 0.4452872 1e-14 | tail -1                                  # about 5-30 minutes, 1-2 GB
    # second program, same roots (mkgraph.py wordR WORD W R: W columns, R rows = two word periods;
    # eig's argument 3 = rows per word period; eig prints "root ..."):
    python3 how-we-built-it/code/eig/mkgraph.py wordR TSS 6 6 | EIG_ROT=1 bin/eig bond 3 0.4452875 4   # root 0.44528752047593878
    python3 how-we-built-it/code/eig/mkgraph.py wordR TSS 8 6 | EIG_ROT=1 bin/eig bond 3 0.4452871 4
    # reruns agree with the saved tables to a few units in the 15th decimal, not bit for bit

## 5. Same code on known thresholds
    for W in 2 3 4 5 6 7 8; do bin/tm TS bond $W root 0.4195 0.4198 1e-14 | tail -1; done       # compare data/tm/TS_bond.tsv
    for W in 2 4 6 8; do bin/tm kagome bond $W root 0.52 0.53 1e-14 | tail -1; done              # n = W/2; Scullard-Jacobsen 2020 Table II
    python3 how-we-built-it/code/tm/extrap.py how-we-built-it/data/tm/TS_bond.tsv 0.41964035886369
    # RESULT pc_B = 0.419640362745204 sigma_B = 5.659e-09 [rule4-main]; pc_B - ref = 3.882e-09

## 6. Extrapolation and error bar of the claim
    python3 how-we-built-it/code/tm/extrap.py object/TSS_bond_roots.tsv 0.44528611 --refsig 0.0000004
    # RESULT pc_B = 0.445287065459697 sigma_B = 7.293e-09 [rule4-main] sizes W=2..10; |pc_B - ref| / combined = 2.39
    python3 how-we-built-it/code/check/sigma_v2.py object/TSS_bond_roots.tsv 7.293e-09 0.44528611
    # W_max 10: E1 0.445287065459697; sigma_B(rule 4) 7.293e-09; drift_3 1.722e-08; 2.87*sigma_B 2.093e-08; sigma_v2 2.093e-08
    python3 how-we-built-it/code/eig/extrap_eig.py how-we-built-it/data/eig/bond.tsv
    # the second program's table; block "== TSS bond": RULE4 p_B = E1 = 0.445287065459697 (its E3 is a BST
    # accelerator, so its sigma_B, 6.747e-09, is smaller than the 7.293e-09 the claim uses)

## 7. p2 arithmetic against the live table (needs page.html, see step 1)
    python3 how-we-built-it/code/check/q9_check.py claim object/p2_value.json page.html
    # prints the rule-9 arithmetic and "VERDICT: MEETS NUMERIC RULES" (if the row is unchanged)

object/TSS_bond_roots.tsv is a byte copy of the claim's data/tm/TSS_bond.tsv (also here as data/tm/TSS_bond.tsv), and
object/p2_value.json is the claim's result file; the extrapolation commands give the same numbers on either copy.
