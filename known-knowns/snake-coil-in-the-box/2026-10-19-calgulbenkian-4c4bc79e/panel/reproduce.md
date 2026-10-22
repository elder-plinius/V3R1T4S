context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, snake-q12-coil-1468-p3

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only on a private copy of the package. No network was used.

## Definition (quoted)
Claim: "object/p3_co12_drifted_r0_Q12_1468.txt is a transition sequence in the hypercube Q12 (one base-36 digit per step, starting at the vertex 0) that describes an induced cycle (a coil) of length 1468, which equals the live record length for this dimension and type."
Success criterion clauses I can check mechanically (quoted): "verified exhaustively (single-bit steps, distinct vertices, popcount(v_i ^ v_j) >= 2 for non-consecutive pairs, closing edge induced for coils)" and "The verifier's checker must reproduce the exact length of at least one downloaded record file of the same n and type (length-convention calibration)". Length convention (the claim record, not shipped): number of transitions; for a coil it equals the number of vertices.


## My checker (written from scratch before opening verify-it-yourself/, not shipped in this package)
Parses the base-36 digit string as transitions (each digit is a coordinate below 12), starts at vertex 0, builds all vertices, checks distinctness, then the literal all-pairs condition with numpy: for every pair of vertices at positions i, j, popcount(v_i xor v_j) is 1 for consecutive positions (and, for a coil, for the closing pair) and at least 2 for every other pair. A coil must close (the XOR of all transitions is zero). The calibration step runs the same checker on the saved published sample record(s) of the same type and compares the length with the saved table length. Canonical class: first-appearance relabelling of coordinates, minimised over reversal (and over all rotations for a coil), hashed with sha256 (first 16 hex digits).
Command: (own checker, run on object/<file> for a coil, with the-record-we-beat/published.json)
Real output (its output, shown below):
== calibration (my checker on the saved published sample record)
  minortriad sample co12 valid: True length (transitions): 1468 table_length: 1468 match: True
== object
kind coil n 12 transitions 1468 vertices 1468 valid (single-bit steps, distinct, induced): True min popcount over non-consecutive pairs: 2
length equals claimed 1468 : True
table value: 1468 object > table: False == table: True
symmetric by half-sequence test (ts[i]==ts[i+L/2]): False
my canonical form sha256: 8b60333e45552c4e1ec76d7ec9e48f28d50bfabd6ee3a25105f4e6b88b929293

## Negative control
I swapped adjacent transitions at three places in a copy of the object (this keeps a coil closed but should break inducedness) and ran the same checker:
kind coil n 12 transitions 1468 vertices 1468 valid (single-bit steps, distinct, induced): False min popcount over non-consecutive pairs: 1
It is rejected (valid False), so my checker does reject bad objects.

## Calibration and my class function
My checker reproduces the saved table length of the sample record(s) listed under "calibration" in the output above (same n and same type). I also computed my canonical hash of the calibration sample and it equals the saved published hash for that sample wherever the sample is in the saved class list (checked for the minortriad samples), so my class function matches the one the saved hashes were made with.
My canonical hash of the object: 8b60333e45552c4e. Saved class hashes in this cell:
  - minortriad page sample co12 (Echols2026d) (length 1468), canon d7e2b96063052eb2
  - the author's own closed PR #85 object (canonical hash from the triage log) (length 1468), canon 7f89ba0c4b461656
Object class equal to any saved class: False.
Limit, stated plainly: the saved classes are hashes only (plus the author's own earlier closed-PR objects, which are not published records); the underlying Caltech or arXiv record files for this cell are not in the folder, so inequivalence to every published record file cannot be reproduced from the folder. It is established here only against the saved list. The claim sentence itself (valid, length, equal to the table length) does not depend on that.

## Items specific to this cell
- Length 1468 equals the saved table value 1468 (an equal-record witness, p3); it is not a strictly longer object and does not claim to be.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (4c4bc79e20aa730e2e8feb4c2d90d6f3cc493060cd9965dc9d252b184abe710c)
checker verdict: PASS (valid=True, length=1468, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
It agrees with my validity, length and class result (no published class with the same hash).

## Verdict
Validity (exhaustive all-pairs), length 1468, closure, calibration and negative control all reproduce deterministically. Inequivalence to unsaved published record files is not reproducible from the folder (see limit above).

pass: true
