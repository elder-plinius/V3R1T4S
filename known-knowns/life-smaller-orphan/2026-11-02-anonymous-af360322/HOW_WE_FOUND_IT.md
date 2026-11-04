# How we found it (contributor text, unverified)
Brief: the bank target asks for an orphan smaller than Eker's 12 x 8; partial win p1 asks for a certified empty box
with h >= 5 that the literature does not already cover. Two numerical programs first agreed that no 5 x w orphan
exists for w <= 8, but neither gave a certificate. We then wrote a column-transfer CNF (tcnf) whose UNSAT means no
h x w orphan, and checked it with DRAT on small sizes; the unsplit 5 x 7 and 5 x 8 instances were too slow and 5 x 4's
drat-trim check timed out. What worked was cube-and-conquer: fix one target column to each of its 32 values, solve each
cube with CaDiCaL writing an LRAT proof, check it with lrat-check, and record a row per cube. Coverage was checked with
a clause-subset tool and the split validated on sizes with known answers. A second encoding (mcnf, left and right
halves joined in the middle) was written separately, validated on control rules with known orphan widths, and run on
the same 5 x 7 and 5 x 8 splits. The work ran over about seven afternoons on a single shared machine with one or two
workers. A three-reviewer panel (criterion, novelty, reproduce; the reproduce reviewer needed four sessions because of
timeouts and a memory cap) passed the p1 claim.
