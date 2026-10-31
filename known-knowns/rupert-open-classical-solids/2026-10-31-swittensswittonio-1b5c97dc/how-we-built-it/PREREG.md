# PREREG (frozen 2026-10-31T11:34:35Z, before any lens output exists)
null_test: not needed because the claim is a deterministic exact verification of an explicit certificate file (sha256-pinned) by an independent program; negative controls (wrong records must be refused) are required instead and are listed below.

## Criterion (verbatim, partial win p3)
A from-scratch re-implementation, written independently of Hervay (a different language from his Rust prover and Python audit, exact arithmetic), that re-verifies every one of the 192,696 records of Hervay's rhombicosidodecahedron certificate (github.com/bence-hervay/nopert-rid, proof/results/full, SHA-256 as listed there) and the completeness of its cover, and reports full agreement, or reports a discrepancy with a minimal reproducing record.

## Judging statistic (frozen)
For the claim "p3 full agreement" ALL of the following must hold, each by program output:
1. Implementation language is neither Rust nor Python; code written from paper/ (math) and not derived from proof/src or audit/.
2. Input is certificate/search.cert with sha256 df1f8dbab68b561f22fa9daeca48153d71bde7b6fba3345d9f6b7b8077df4b5f; record count 192696 (excluding header); all record checksums (8 hex digits = start of SHA-256 of the rest of the line) verified.
3. Every one of the 192,696 records re-verified in exact arithmetic (exact Q(sqrt5) arithmetic, or outward-rounded exact big-integer interval arithmetic): output counts per component Global 157458, Local 21792, Domain 12650, Exotic 796 all accepted, 0 rejected.
4. Completeness: paths prefix-free and tiling the root box exactly (Kraft sum exactly 1 with every node covered), checked exactly.
5. Zoom covers: the cells of the 38 cover files that the Local/Exotic records rely on are independently re-checked by the zoom lemma (or the claim must say precisely that cover cells were NOT rechecked and the claim level falls accordingly).
6. Negative controls: at least 400 deliberately corrupted records (wrong inequality index, wrong edge/vertex, box shifted outside the cover, perturbed path, wrong component) are each REFUSED by the verifier; any accepted corruption voids the claim.
7. Known-positive sanity of the underlying fit test: the same fit/no-fit machinery recognises a genuine Rupert passage of the cube (or cuboctahedron) as a fit.
If any record is rejected, report it with the minimal reproducing record and claim only "discrepancy found", after the panel confirms.
Claim wording allowed at most: "independent C#/Java/JS verifier agrees with all 192,696 records ..." with the exact scope of items 3-5.

## Other lenses (no claim intended unless explicitly pre-frozen here)
Passage searches and global-stage experiments are exploratory: claim level at most progress/negative; a certified passage for any of the nine would be checked by the exact checker (checker/ of run 0018: strict containment, positive certified margin) and then panelled.
