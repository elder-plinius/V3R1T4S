# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: The stabilizer code [[79,61]] in the supplied object file has exact minimum distance 5 (commuting, rank 18, pure distance >= 5 by distinct syndromes of all weight <= 2 errors, weight-5 logical outside the stabilizer), which exceeds the lower bound 4 shown in the codetables.de QECC cell for [[79,61]] on 2026-10-20T02:59Z, within upper bound 6; no claim about the literature or about any other cell.

## Gate notes
- Object: object/new_stabilizer_codes_d5.json, sha256 2de9ef5264ea4bbbe334bf590f12f5ce89cb8f8ce30a464b4112e55f66a2927f.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p1: a pure distance-5 qubit stabilizer code at a cell whose live codetables.de lower bound is 4 (upper bound 6, last change 2024-06-10); distance is exactly 5 (pure d >= 5 by distinct syndromes of all errors of weight <= 2; a weight-5 logical outside the stabilizer excludes 6).
- One construction (a Hermitian self-orthogonal GF(4) construction via a Plucker embedding, by the author's search agent) yields this cell; it is a separate entry of the table and does not follow from another or from any table code by the standard propagation rules or by shortening (checked by the novelty skeptic from the table's stored stabilizer matrices).
- Literature search: the arXiv export API was rate-limited (429) during the novelty check; the arXiv HTML search (6 queries) found no qubit d = 5 code at these parameters. A non-arXiv or table-unreported construction cannot be excluded.
