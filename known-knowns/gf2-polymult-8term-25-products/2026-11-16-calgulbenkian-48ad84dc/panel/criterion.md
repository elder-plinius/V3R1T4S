context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report

## Literal reading of p2
p2 requires, for GF(2^7) mod x^7+x^4+1: a circuit of 2-input AND/XOR/XNOR gates, no constants, at most 83 gates, verified on all input pairs, and below any smaller published circuit. The claim is for the x^7+x^4+1 option only (not the other two options). That option's literal threshold is 83, and the claim's 82 is inside it.

## What I checked myself
- Wrote my own checker (scratch: a working file (not shipped), run with python -I), not using the package's verifier. Parsed object/gf128_0x91_82gates.slp.txt: 82 gates, 34 AND, 48 XOR, 0 XNOR. No NOT, no constants, no wire redefined or used before definition (the evaluation order assumes this and would have failed otherwise).
- Evaluated it on all 128 x 128 = 16384 input pairs against schoolbook multiplication reduced mod 0x91 (bit 7, bit 4, bit 0 = x^7+x^4+1). Zero mismatches in all seven output bits. I also confirmed x^7+x^4+1 is irreducible, so the object is a real field multiplier in the standard polynomial basis (inputs A0..A6, B0..B6, outputs C0..C6).
- SHA-256 of the object matches the claimed 48ad84dc...f100.
- Hidden quantifiers: none found. "All input pairs" is exhaustive (2^14), not sampled. Gate count is the same counter as NIST's (every AND/XOR line is one gate). The claim does not count inputs or outputs as gates. No stretched definition: it is the same function (standard basis, same polynomial) as the NIST 84-gate circuit, not a tower or normal basis circuit.
- Null model: the pre-registration says no null test is needed for an exact certificate; I agree, since the check is exhaustive and deterministic.

## Literature condition ("below any smaller published circuit")
Partly settled, not fully (NOVELTY skeptic owns the full search).
- Fetched Swapnil Jain's repository (fetches in a working copy (not shipped)). The README states "GF(2^7) in 83 gates". The circuit files show that 83 is for poly 0x89 (x^7+x^3+1) (header of final_f73.slp: "poly 0x89 gates=83"), while the 0x91 circuit final_f7.slp is headed "poly 0x91 gates=87". That matches the package's 87 for 0x91. So Jain's 83 does not undercut 82 and is for a different polynomial; it is also not below the 82 anyway.
- The NIST list page (fetched) still shows 84 for the 0x91 entry (40 AND, 44 XOR) and 85 for the other. I did not find a smaller published 0x91 circuit; I did not search beyond these sources (no search of Boyar-Peralta follow-ups, other preprints, or the Jain PDF itself).
- Side note, not affecting p2: the package's prereg used Jain's AES figure of 107, but the Jain README says 112 at depth 6 and 107 at depth 13; irrelevant here since only p2 is claimed.

## Scope and non-subsumption
- Does not touch the main 25-product problem, p1 or p3; the claim says so itself.
- Not a restriction of a merged package result (no merged prior package covers this cell as far as the claim folder shows; I could not check the V3R1T4S repo).
- Depth 6 versus the 84-gate circuit's depth 5 is irrelevant to p2, which sets no depth limit.
- Remaining risk: an unknown earlier published circuit at 82 or fewer for 0x91 (would tie or beat). I could not rule that out.

confirmed_scope: The file object/gf128_0x91_82gates.slp.txt is a valid 82-gate (34 AND, 48 XOR) AND/XOR circuit that exhaustively matches standard polynomial-basis multiplication in GF(2^7) modulo x^7+x^4+1 on all 16384 input pairs, meeting partial win p2's 83-gate limit for that polynomial and beating the NIST/CMT 84 and Jain 87 figures, subject to the novelty skeptic's confirmation that no smaller published circuit exists.

pass: true
