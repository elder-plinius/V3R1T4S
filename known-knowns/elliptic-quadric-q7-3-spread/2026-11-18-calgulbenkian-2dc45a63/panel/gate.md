# Honesty gate (elliptic-quadric-q7-3-spread)

status: CONFIRMED_PARTIAL
confirmed_scope: Rerunning the package (run_checks.sh PASS in 57 s, plus the SWAR engine with 0 solutions) confirms that no spread of Q^-(7,3) is invariant under any element of order 3 of the full collineation group PGO^-(8,3), covering all 430,408,160 such elements in 5 classes; order-2 automorphisms are excluded only inside PO^-(8,3), the similarity involutions (class Inv_0_sim) remain open.

## Gate notes
- Object: object/q7_3_ord3_certificate.json, sha256 2dc45a6304721dfd1612d2111c4902ad4a690d862b127568e9c7e84d299dbd65.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic built its own model of Q^-(7,3), derived the order-3 classes from Wall's classification (7 in O^-(8,3), fused to 5 in the full group by an explicit similitude), and ran its own exact-cover search in every class with 0 invariant spreads (class 13 via its own centralizer symmetry breaking, 2064 tasks); a positive control on Q^-(5,3) finds invariant spreads. The package's SWAR solver rerun gives sat=0, as p1 requires.
- Status source arXiv:2403.11188 (fetched by the panel 2026-11-18T17:31:12Z) restricts automorphism orders of a possible spread to primes 2 and 3 only; order 3 was not excluded. Order 2 remains open here for the similarity involution class.
