context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, snake-q10-coil-374-p3

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only on a private copy of the package. No network was used.

## Definition (quoted)
Claim: "object/p3_co10_drifted_r0_Q10_374.txt is a transition sequence in the hypercube Q10 (one base-36 digit per step, starting at the vertex 0) that describes an induced cycle (a coil) of length 374, which equals the live record length for this dimension and type."
Success criterion clauses I can check mechanically (quoted): "verified exhaustively (single-bit steps, distinct vertices, popcount(v_i ^ v_j) >= 2 for non-consecutive pairs, closing edge induced for coils)" and "The verifier's checker must reproduce the exact length of at least one downloaded record file of the same n and type (length-convention calibration)". Length convention (the claim record, not shipped): number of transitions; for a coil it equals the number of vertices.


## My checker (written from scratch before opening verify-it-yourself/, not shipped in this package)
Parses the base-36 digit string as transitions (each digit is a coordinate below 10), starts at vertex 0, builds all vertices, checks distinctness, then the literal all-pairs condition with numpy: for every pair of vertices at positions i, j, popcount(v_i xor v_j) is 1 for consecutive positions (and, for a coil, for the closing pair) and at least 2 for every other pair. A coil must close (the XOR of all transitions is zero). The calibration step runs the same checker on the saved published sample record(s) of the same type and compares the length with the saved table length. Canonical class: first-appearance relabelling of coordinates, minimised over reversal (and over all rotations for a coil), hashed with sha256 (first 16 hex digits).
Command: (own checker, run on object/<file> for a coil, with the-record-we-beat/published.json)
Real output (its output, shown below):
== calibration (my checker on the saved published sample record)
  minortriad sample co10 valid: True length (transitions): 374 table_length: 374 match: True
== object
kind coil n 10 transitions 374 vertices 374 valid (single-bit steps, distinct, induced): True min popcount over non-consecutive pairs: 2
length equals claimed 374 : True
table value: 374 object > table: False == table: True
symmetric by half-sequence test (ts[i]==ts[i+L/2]): False
my canonical form sha256: f2ddf6e1f06e26fd41f00531deaa85058d02ae7ea91cb432f8b3e2541ae3bc6d

## Negative control
I swapped adjacent transitions at three places in a copy of the object (this keeps a coil closed but should break inducedness) and ran the same checker:
kind coil n 10 transitions 374 vertices 374 valid (single-bit steps, distinct, induced): False min popcount over non-consecutive pairs: 1
It is rejected (valid False), so my checker does reject bad objects.

## Calibration and my class function
My checker reproduces the saved table length of the sample record(s) listed under "calibration" in the output above (same n and same type). I also computed my canonical hash of the calibration sample and it equals the saved published hash for that sample wherever the sample is in the saved class list (checked for the minortriad samples), so my class function matches the one the saved hashes were made with.
My canonical hash of the object: f2ddf6e1f06e26fd. Saved class hashes in this cell:
  - minortriad page sample co10 (Fagan2026) (length 374), canon 4b6907cdfc78b603
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 2 (n=10, length 374) (length 374), canon 4b6907cdfc78b603
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 3 (n=10, length 374) (length 374), canon 1a05aab0b4f43236
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 4 (n=10, length 374) (length 374), canon 324d332a0299772d
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 5 (n=10, length 374) (length 374), canon 3594393e661143e4
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 6 (n=10, length 374) (length 374), canon d296dd369d4059e8
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 7 (n=10, length 374) (length 374), canon 4c6b19ff06fbcd28
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 8 (n=10, length 374) (length 374), canon 542e350a04d60bcc
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 9 (n=10, length 374) (length 374), canon 4481e0cb88488cca
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 10 (n=10, length 374) (length 374), canon 09c4d899bce2947f
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 11 (n=10, length 374) (length 374), canon 57e93d9d33aba480
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 12 (n=10, length 374) (length 374), canon 9fce7d760fe4e894
  - Math-AI-Caltech/Snake-in-the-Box record_coils data row 13 (n=10, length 374) (length 374), canon 1f1cff91d226e468
  - the author's own closed PR #83 object (canonical hash from the triage log) (length 374), canon 303e36ad34660551
Object class equal to any saved class: False.
Limit, stated plainly: the saved classes are hashes only (plus the author's own earlier closed-PR objects, which are not published records); the underlying Caltech or arXiv record files for this cell are not in the folder, so inequivalence to every published record file cannot be reproduced from the folder. It is established here only against the saved list. The claim sentence itself (valid, length, equal to the table length) does not depend on that.

## Items specific to this cell
- Length 374 equals the saved table value 374 (an equal-record witness, p3); it is not a strictly longer object and does not claim to be.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (80851a336fbc159e2b27b2fa0b862285a7e099b81a57dcd283b21284eb67ab2d)
checker verdict: PASS (valid=True, length=374, calibration reproduces published lengths=True, half-period symmetric=False)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
It agrees with my validity, length and class result (no published class with the same hash).

## Verdict
Validity (exhaustive all-pairs), length 374, closure, calibration and negative control all reproduce deterministically. Inequivalence to unsaved published record files is not reproducible from the folder (see limit above).

pass: true
