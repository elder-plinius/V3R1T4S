# Honesty gate (perfect-cuboid)

status: CONFIRMED_PARTIAL
confirmed_scope: Machine-checked in Lean 4 (v4.35.0, only propext, Classical.choice, Quot.sound) that for all nonzero integers p, q with p^2 != q^2 the squared third edge of each of the two de Grey-Gibbs-Helm internal-ratio edge-cuboid families (arXiv:2401.06784 Section 7.4) is never an integer square, hence no member of either family, under any rational rescaling, is a perfect cuboid; the package does not prove that these families avoid Peschmann's 1,072 fibers and uses no PARI or Magma computation.

## Gate notes
- Object: object/certificate.json, sha256 59c16836ba02d8d9cf046dbc3a717ff76d4b3f3ee637a9df7d1f6230d7b5a1cc.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed. The REPRODUCE and NOVELTY skeptics reviewed the first version of this package; the CRITERION skeptic in the first round failed it because the package then carried ancillary rank and Selmer claims (with a PARI script that could not be run here) that the proof does not use. Those were removed, the Lean proof file is byte-identical, and a fresh CRITERION skeptic passed this version (criterion.md).
- The REPRODUCE skeptic compiled the Lean file (Lean 4.35.0, only propext, Classical.choice and Quot.sound), re-derived the reduction from arXiv:2401.06784 Section 7.4 by hand, and reproduced the paper's examples; the NOVELTY skeptic found that Section 10.2 of that paper leaves the exclusion of these two families open.
