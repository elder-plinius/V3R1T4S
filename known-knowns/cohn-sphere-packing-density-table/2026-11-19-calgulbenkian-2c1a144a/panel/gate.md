# Honesty gate (cohn-sphere-packing-density-table)

status: CONFIRMED_PARTIAL
confirmed_scope: A 6-translate periodic packing in R^19 over a det-300 Leech cross-section lattice has exact minimal squared center distance 52/15 and exact center density equal to the table's 3^(-9) 5^(-21/2) 13^(19/2), and it is non-isometric to the Chen-Hu-Li-Wang-Wu antipode packing in that cell (per-sphere kissing multiset (4022,4022,4072,4072,4072,4072) versus six 4110s, and norm-4 counts 6858 versus 6942 with trivial translate stabilizer), all certified by exact rational Fincke-Pohst enumeration with no floating point.

## Gate notes
- Object: object/d19_nonisometric_periodic_packing_certificate.json, sha256 2c1a144a9ddb7b04c078aa55ce5f152637ee2bb87336a755b37c8cb468e9e2ae.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic built the Leech lattice from the Golay code itself, recomputed the minimum squared distance 52/15 by exact coset enumeration and the centre density exactly equal to the table's n = 19 value, and rebuilt the published record packing (arXiv:2505.02394) independently: the lattices differ (6858 versus 6942 norm-4 vectors) and both translation stabilisers are trivial, so the packings are not isometric.
- Scope note: the published record packing already admits a continuous family of equal-density slides, so non-isometric packings at this density are easy to find; this one is not such a slide but a different Leech embedding of the same section (a different orthogonal complement), which is what p1 asks for. It matches the record density and does not exceed it.
