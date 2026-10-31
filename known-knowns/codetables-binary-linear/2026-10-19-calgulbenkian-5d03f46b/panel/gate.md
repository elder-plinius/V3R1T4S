# Honesty gate (codetables-binary-linear)

status: CONFIRMED_PARTIAL
confirmed_scope: The object file's entry n=49, k=38 is a qubit stabilizer code [[49,38,4]] (11 independent commuting generators, no logical of weight 3 or less, a weight-4 logical), exactly checked here, and 4 is strictly above the live codetables.de QECC lower bound 3 for [[49,38]] (fetched 2026-10-19) and equals its upper bound; this covers only this cell under p1 and says nothing about novelty against the literature or about the other five cells.

## Gate notes
- Object: object/new_optimal_stabilizer_codes_r11_d4.json, sha256 3e9858a143b751d715399b3dc8248129a522c4d2628dfb3bc074f09c0930b9c0.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Partial win p1 (a quantum code beating the live codetables.de QECC lower bound): distance exactly 4 against the live cell's lower bound 3; 4 equals the cell's upper bound, so the code is optimal for its parameters.
- This code comes from one construction (an extension of a [[64,53,4]] code with 11 parity checks); this cell is judged on its own and does not follow from a neighbouring live cell.
- The object file credits the [[64,53,4]] base code to 'Dastbasteh et al.'; the novelty skeptic believes it is the Bierbrauer-Edel quantum twisted code and could not confirm the attribution, so no credit is given for it beyond codetables.de.
