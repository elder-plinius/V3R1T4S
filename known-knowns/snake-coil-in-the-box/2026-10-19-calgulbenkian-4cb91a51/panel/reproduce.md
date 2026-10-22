context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, snake-q13-symcoil-2886

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only on a private copy of the package. No network was used.

## Definition (quoted)
Claim: "object/best_sym13_from2882_Q13_2886.txt is a transition sequence in the hypercube Q13 (one base-36 digit per step, starting at the vertex 0) that describes an induced cycle (a coil) of length 2886 whose first half of the sequence equals its second half (the table page's symmetry test)."
Success criterion clauses I can check mechanically (quoted): "verified exhaustively (single-bit steps, distinct vertices, popcount(v_i ^ v_j) >= 2 for non-consecutive pairs, closing edge induced for coils)" and "The verifier's checker must reproduce the exact length of at least one downloaded record file of the same n and type (length-convention calibration)". Length convention (the claim record, not shipped): number of transitions; for a coil it equals the number of vertices.
Symmetry test of the table page (quoted from the-record-we-beat/minortriad_page_symmetric_test.txt): even length 2h and edges[i] == edges[i+h] for all i < h.

## My checker (written from scratch before opening verify-it-yourself/, not shipped in this package)
Parses the base-36 digit string as transitions (each digit is a coordinate below 13), starts at vertex 0, builds all vertices, checks distinctness, then the literal all-pairs condition with numpy: for every pair of vertices at positions i, j, popcount(v_i xor v_j) is 1 for consecutive positions (and, for a coil, for the closing pair) and at least 2 for every other pair. A coil must close (the XOR of all transitions is zero). The calibration step runs the same checker on the saved published sample record(s) of the same type and compares the length with the saved table length. Canonical class: first-appearance relabelling of coordinates, minimised over reversal (and over all rotations for a coil), hashed with sha256 (first 16 hex digits).
Command: (own checker, run on object/<file> for a coil, with the-record-we-beat/published.json)
Real output (its output, shown below):
== calibration (my checker on the saved published sample record)
  minortriad sample sc13 valid: True length (transitions): 2830 table_length: 2830 match: True
== object
kind coil n 13 transitions 2886 vertices 2886 valid (single-bit steps, distinct, induced): True min popcount over non-consecutive pairs: 2
length equals claimed 2886 : True
table value: 2830 object > table: True == table: False
symmetric by half-sequence test (ts[i]==ts[i+L/2]): True
my canonical form sha256: ee70083e8016dbc6984c2e07805efc513d1685f6a8f56366d5d435f5b1080fed

## Negative control
I swapped adjacent transitions at three places in a copy of the object (this keeps a coil closed but should break inducedness) and ran the same checker:
kind coil n 13 transitions 2886 vertices 2886 valid (single-bit steps, distinct, induced): False min popcount over non-consecutive pairs: 1
It is rejected (valid False), so my checker does reject bad objects.

## Calibration and my class function
My checker reproduces the saved table length of the sample record(s) listed under "calibration" in the output above (same n and same type). I also computed my canonical hash of the calibration sample and it equals the saved published hash for that sample wherever the sample is in the saved class list (checked for the minortriad samples), so my class function matches the one the saved hashes were made with.
My canonical hash of the object: ee70083e8016dbc6. Saved class hashes in this cell:
  - the author's own closed PR #80 object (canonical hash from the triage log) (length 2870), canon 8bfabfe09335d4f7
Object class equal to any saved class: False.
Limit, stated plainly: the saved classes are hashes only (plus the author's own earlier closed-PR objects, which are not published records); the underlying Caltech or arXiv record files for this cell are not in the folder, so inequivalence to every published record file cannot be reproduced from the folder. It is established here only against the saved list. The claim sentence itself (valid, length, symmetry) does not depend on that.

## Items specific to this cell
- Symmetry: my half-sequence test (transition i equals transition i + 1443) printed True above. This is the minortriad page's own analyzer test; the Caltech sigma-symmetry (coordinate swap plus translation) is a different, not tested, notion (the folder does not define it precisely, so I did not test it).
- Value: 2886 against the saved minortriad symmetric-coil value 2830: strictly greater = True.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (4cb91a51274083a86d9f3edca2dc46358757d9990d246755f6756b989ff6fbda)
checker verdict: PASS (valid=True, length=2886, calibration reproduces published lengths=True, half-period symmetric=True)
== negative control: one transition changed must NOT be a valid coil
negative control rejected as expected (valid false)
ALL CHECKS PASS
It agrees with my validity, length and class result (no published class with the same hash).

## Verdict
Validity (exhaustive all-pairs), length 2886, closure, half-sequence symmetry, calibration and negative control all reproduce deterministically. Inequivalence to unsaved published record files is not reproducible from the folder (see limit above).

pass: true
