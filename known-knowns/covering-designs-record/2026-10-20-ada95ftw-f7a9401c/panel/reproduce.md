# Skeptic: REPRODUCE — C(36,5,3) <= 812

context: subagent (fresh executor, saw only claim/)

Definition used (quoted): "a covering design C(v,k,t) is a family of k-subsets (blocks) of a v-set such that every t-subset lies in at least one block." Here v=36, k=5, t=3, claimed b=812.

Scope: only the claim/ folder was read. I wrote my own checker from the definition (a separate scratch checker, not inside claim/) before opening claim/check_cover.py. It uses plain sorted tuples and set membership, not the author's bitmask method.

## Checks on claim/object/C36_5_3_812.txt
- sha256 = f7a9401c9fc3e6db6721b7eee490dbad8a7cb95bf6a9e8d0de9bcf7851da6b23, the same as in CLAIM.md. PASS
- 11217 bytes, 812 newline-terminated lines, no blank or oddly formatted lines. PASS
- Each line has exactly 5 integer tokens, all distinct, all in 1..36. I found 0 bad blocks. PASS
- Repeated blocks: 812 blocks, 812 distinct when compared as sorted tuples. PASS
- Coverage, checked exhaustively: I enumerated all C(36,3) = 7140 triples of {1..36} and looked each one up in the set of triples contained in the blocks. All 7140 are covered and 0 are uncovered. This was a full check, not a sample. PASS
- Schonheim bound, recomputed with exact rational ceilings: ceil(34/3) = 12, then ceil(35/4 * 12) = 105, then ceil(36/5 * 105) = 756. So L(36,5,3) = 756 and 812 >= 756, which means the result is consistent and not suspiciously low. Trivial check: ceil(7140/10) = 714 <= 812. PASS
- Determinism: I ran the checker more than once and got output with the same md5 every time. PASS

## Comparison with the author's checker (run only after reaching my verdict)
The command `python3 check_cover.py 36 5 3 object/C36_5_3_812.txt` printed "VALID v=36 k=5 t=3 b=812 distinct=812 bad_blocks=0 uncovered=0 of 7140 schonheim=756". This matches my results and the Expected line in REPRODUCE.md. The author's Schonheim function computes the same nested-ceiling recursion.

## Out of scope
I did not re-fetch the live record tables (coveringrepository.com 821, LJCR, GitHub/Zenodo) or search GitHub/arXiv, so whether 812 beats the current record was not checked here. This verdict covers the validity of the object and the bound only.

pass: true
