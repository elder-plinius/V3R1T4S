# A(35,6,6) >= 2225

## What
The supplied object proves A(35,6,6) >= 2225.

PROVED-HERE: the supplied finite certificate contains 2225 distinct length 35 binary words, all weight 6, with actual minimum Hamming distance 6. The claim is an improved lower bound, not the exact value of A(35,6,6).

## Check it yourself
Run `sh verify-it-yourself/run_checks.sh` from this folder. Python standard library only; expected last line `PASS`, typically seconds on a laptop. The checker examines all 2474200 pairs and independently checks 33375 four-subsets for overlap. It rejects malformed and corrupted objects.

## Compared to
KNOWN, dated source check: the live table lists 2217–3249; PR441 and earlier PR59 improve the lower bound to 2218. This construction improves the stronger located baseline by 7, and the live table by 8. Sources, fetch metadata, exact cell and propagation audit are in the-record-we-beat/ and panel/novelty.md.

## Not claimed
No optimality, new search algorithm, exhaustive search of all codes, or platform-independent discovery determinism. The complement gives the equivalent weight 29 code, not a separate result. Upper-bound experiments from the same research pass are not part of this claim.

## Credits
Jordan Boisclair's archive seed and the V3R1T4S bigger-codes polish preceded calgulbenkian's 2218 construction. This work reuses calgulbenkian's seed and engine from [PR441](https://github.com/elder-plinius/V3R1T4S/pull/441) at commit1d90d76f7c9ec29b50ba091078422b1c82008486. Andries Brouwer maintains the comparison table; William Echols and Christian Lysenstoeen supply the recent baseline literature. Full source provenance is in how-we-built-it/PROVENANCE.md. CannibalKush's contribution is the new seeded search output, exact verification and submission evidence.

Panel reports are copied unchanged from three fresh reviewers. Their `claim/` paths refer to the original frozen review package; its object is supplied here as object/A35_6_6_2225.txt. Reviewer working evidence remains in the local research run; standalone verification above does not depend on it.
