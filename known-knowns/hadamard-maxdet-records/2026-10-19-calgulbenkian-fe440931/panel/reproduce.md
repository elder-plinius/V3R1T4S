context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, maxdet-109

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only in a private copy of the package. No network was used.

## Definition (quoted from the claim record, not shipped)
Claim: "object/M109_2162897555231082049798834993796033279114137960386362436200469570917630303164899.txt is a 109 x 109 matrix with every entry +1 or -1 whose exact normalised determinant |det| / 2^108 is 297 * 27^53 = 2162897555231082049798834993796033279114137960386362436200469570917630303164899, which is larger than the Orrick archive value 1.877483842E78 for order 109 and than the merged V3R1T4S package (PR #155, known-knowns 0108345c) value 291 * 27^53 and is below the Barba bound for n = 1 mod 4."
Verification method (bank, quoted): "Compute |det| with fraction-free Bareiss elimination on Python ints (exact), cross-checked with sympy Matrix(...).det(method='bareiss'). Note that det is divisible by 2^(n-1), so report |det|/2^(n-1) as an integer and compare it exactly to the record value. Confirm all entries are +-1. Also compute the bound for the residue class and confirm det <= bound."
Barba bound used (n = 1 mod 4): |det| <= sqrt(2n-1) * (n-1)^((n-1)/2); I test it exactly as the integer inequality det^2 <= (2n-1)(n-1)^(n-1).

## My checker (written from the definition before opening verify-it-yourself/)
My own checker (not shipped in this package) reads the file, asserts the n x n shape and that every entry is the text +1 or -1, computes the determinant by my own fraction-free Bareiss on Python ints, cross-checks it with an independent exact integer determinant from python-flint (fmpz_mat; sympy was not needed, flint is a separate exact implementation), tests divisibility by 2^(n-1), compares the normalised value with the claimed integer, and tests the Barba bound exactly.
Command: (own checker, run on the object file with arguments 109 and the claimed integer)
Real output (shown below):
n 109 all entries +-1: True; python-int Bareiss == flint exact det: True
divisible by 2^(n-1): True
normalised |det|/2^(n-1) = 2162897555231082049798834993796033279114137960386362436200469570917630303164899
equals claimed value: True
n mod 4 = 1
within Barba bound sqrt(2n-1)(n-1)^((n-1)/2) (exact integer test of squares): True ratio 0.7467286566323438
time: 0.17s user 0.01s system 78% cpu 0.236 total

## Comparison with the saved records (the-record-we-beat/records.json; I did not judge whether they are current)
  object D = 2.162897555e+78 (exact integer in the file name and checked below) vs Orrick archive value 1.877483842E78: D > Orrick = True
  merged PR #155 value 291 * 27^53 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497; 297 * 27^53 = 2162897555231082049798834993796033279114137960386362436200469570917630303164899; difference = 43694900105678425248461313005980470285134100209825503761625647897325864710402 = 6 * 27^53 : True; D > PR #155 value = True

## Author's checker (run only after mine)
sh verify-it-yourself/run_checks.sh, its output as follows:
sha256 matches INDEX.csv (fe44093142381fa403c5bc471d6639775c6a3d4f5150f3ee70519e646ed1425e)
checker verdict: PASS (D=2162897555231082049798834993796033279114137960386362436200469570917630303164899, larger than all listed records=True)
== negative control: one entry negated must NOT give the claimed determinant
negative control rejected as expected (determinant differs)
ALL CHECKS PASS
It agrees with my values; no mismatch.

## Open questions concerning reproduction
- Rokicki newrec page, newer sources, EinsteinArena: not reproducible from the folder and not my role (novelty).
- The Cauchy-Schwarz "ceilings" in the author's notes are outside this folder; they do not touch the exactly verified determinant, which I recomputed independently.

## Verdict
Matrix shape, entries, exact determinant (two independent exact methods), divisibility, the claimed integer and the Barba bound all reproduce; deterministic (exact integer arithmetic). Limits: the comparison uses the saved record values only.

pass: true
