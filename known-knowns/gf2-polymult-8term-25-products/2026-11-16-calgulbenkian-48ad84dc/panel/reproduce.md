context: Claude Code subagent, fresh context [Sonnet 5.5]

## Definition checked against (quoted from the target's success criterion)

p2: "The same kind of circuit for GF(2^7) modulo x^7 + x^4 + 1 with at most 83 gates, or modulo x^7 + x^3 + 1 with at most 84, or for GF(2^6) modulo x^6 + x^3 + 1 with at most 56, verified on all input pairs and below any smaller published circuit."
"The same kind of circuit" = "A circuit of 2-input AND, XOR and XNOR gates (no other gates, no constants) ... standard polynomial basis in and out".
Verification method: "parse the gate list, reject any gate other than AND, XOR, XNOR, evaluate all input pairs against a reference field multiplication (... 2^14 for GF(2^7)), and count gates".
Pitfall: "AND, XOR and XNOR each count one; NOT gates and constants are not allowed."

## My own checker (written before reading any author code)

I wrote a working file (not shipped) from the definition above. It:
- requires the exact "begin SLP" / "end SLP" frame and every body line to be "OP dest src1 src2" with OP in {AND, XOR} (anything else rejected, so no NOT, no constants);
- requires inputs A0..A6, B0..B6 and every source defined earlier, every destination defined exactly once and not an input, and outputs C0..C6 all defined;
- counts gates by type, computes depth, lists dead gates;
- builds its own reference multiplier (carry-less multiply, reduce by 0x91 = x^7+x^4+1, bit i = coefficient of x^i) and checks that 0x91 is irreducible (so it really is a field);
- evaluates all 128 x 128 = 16384 input pairs.

Exact output on object/gf128_0x91_82gates.slp.txt:
```
gates 82 AND 34 XOR 48 depth 6 dead []
irreducible True mismatches 0 of 16384
PASS
```
A second run gave identical output (deterministic). The file's sha256 is 48ad84dc1afddd567bcccf6574447aa229e3371548afa57f386fe2779897f100, matching the claim and INDEX.csv. File has 84 lines = 82 gates plus begin/end; no dead gates; 0 XNOR; no constants.

## Cross-check (run only after my verdict)

verify-it-yourself/verify_gf2m.py with --m 7 --poly 0x91 --max-gates 83 printed: gates 82, and 34, xor 48, xnor 0, gate_depth 6, pairs_checked 16384, PASS. Agrees with mine.

## What I could and could not confirm

Confirmed from saved files: gate-only basis, 82 gates (34 AND, 48 XOR), depth 6, exact standard-basis GF(2^7) multiplication mod x^7+x^4+1 on all 16384 pairs, 82 <= 83 threshold, and 82 < 84 (the NIST/CMT figure as recorded in the-record-we-beat/README.md).
Not reproducible by me (no network, by role): the published bars (NIST 84, CMT 84, Jain 87) and the "below any smaller published circuit" clause rest on the package's own fetch record; I took the 84 figure from the claim text and the target statement, which also gives 84. Novelty versus other literature is outside this role.
The claim's scope statement (no resolution of the 8-term 25-product problem) is consistent with the object: it is a field multiplier only.

pass: true
