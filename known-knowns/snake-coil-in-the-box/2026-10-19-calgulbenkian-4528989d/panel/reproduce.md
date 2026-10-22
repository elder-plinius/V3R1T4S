context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, snake-q12-snake-1480-p3

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only on a private copy of the package. No network was used.

## Definition (quoted)
Claim: "object/p3_sn12_drifted_r0_Q12_1480.txt is a transition sequence in the hypercube Q12 (one base-36 digit per step, starting at the vertex 0) that describes an induced path (a snake) of length 1480, which equals the live record length for this dimension and type."
Success criterion clauses I can check mechanically (quoted): "verified exhaustively (single-bit steps, distinct vertices, popcount(v_i ^ v_j) >= 2 for non-consecutive pairs, closing edge induced for coils)" and "The verifier's checker must reproduce the exact length of at least one downloaded record file of the same n and type (length-convention calibration)". Length convention (the claim record, not shipped): number of transitions; for a coil it equals the number of vertices.


## My checker (written from scratch before opening verify-it-yourself/, not shipped in this package)
Parses the base-36 digit string as transitions (each digit is a coordinate below 12), starts at vertex 0, builds all vertices, checks distinctness, then the literal all-pairs condition with numpy: for every pair of vertices at positions i, j, popcount(v_i xor v_j) is 1 for consecutive positions (and, for a coil, for the closing pair) and at least 2 for every other pair. A coil must close (the XOR of all transitions is zero). The calibration step runs the same checker on the saved published sample record(s) of the same type and compares the length with the saved table length. Canonical class: first-appearance relabelling of coordinates, minimised over reversal (and over all rotations for a coil), hashed with sha256 (first 16 hex digits).
Command: (own checker, run on object/<file> for a snake, with the-record-we-beat/published.json)
Real output (its output, shown below):
== calibration (my checker on the saved published sample record)
  minortriad sample sn12 valid: True length (transitions): 1480 table_length: 1480 match: True
== object
kind snake n 12 transitions 1480 vertices 1481 valid (single-bit steps, distinct, induced): True min popcount over non-consecutive pairs: 2
length equals claimed 1480 : True
table value: 1480 object > table: False == table: True
symmetric by half-sequence test (ts[i]==ts[i+L/2]): False
my canonical form sha256: dd9f75020311847ae0f1971afa1a34034ba5dbac0522f0e62354eac777401190

## Negative control
I swapped adjacent transitions at three places in a copy of the object (this keeps a coil closed but should break inducedness) and ran the same checker:
kind snake n 12 transitions 1480 vertices 1481 valid (single-bit steps, distinct, induced): False min popcount over non-consecutive pairs: 1
It is rejected (valid False), so my checker does reject bad objects.

## Calibration and my class function
My checker reproduces the saved table length of the sample record(s) listed under "calibration" in the output above (same n and same type). I also computed my canonical hash of the calibration sample and it equals the saved published hash for that sample wherever the sample is in the saved class list (checked for the minortriad samples), so my class function matches the one the saved hashes were made with.
My canonical hash of the object: dd9f75020311847a. Saved class hashes in this cell:
  - minortriad page sample sn12 (Itty2026a) (length 1480), canon 033fea2481d5014c
  - the author's own closed PR #88 object (canonical hash from the triage log) (length 1480), canon 40e97da295d291fe
Object class equal to any saved class: False.
Limit, stated plainly: the saved classes are hashes only (plus the author's own earlier closed-PR objects, which are not published records); the underlying Caltech or arXiv record files for this cell are not in the folder, so inequivalence to every published record file cannot be reproduced from the folder. It is established here only against the saved list. The claim sentence itself (valid, length, equal to the table length) does not depend on that.

## Items specific to this cell
- Length 1480 equals the saved table value 1480 (an equal-record witness, p3); it is not a strictly longer object and does not claim to be.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (4528989d7ce26b1f97c9c4566a34daecccaa3834fcc67502369638016309fda5)
checker verdict: PASS (valid=True, length=1480, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid snake
negative control rejected as expected (valid false)
ALL CHECKS PASS
It agrees with my validity, length and class result (no published class with the same hash).

## Verdict
Validity (exhaustive all-pairs), length 1480, closure, calibration and negative control all reproduce deterministically. Inequivalence to unsaved published record files is not reproducible from the folder (see limit above).

pass: true
