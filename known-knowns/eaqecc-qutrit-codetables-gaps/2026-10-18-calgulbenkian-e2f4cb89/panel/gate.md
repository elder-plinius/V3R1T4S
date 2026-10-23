# Honesty gate (eaqecc-qutrit-codetables-gaps)

status: CONFIRMED_SOLUTION
confirmed_scope: The 0/1/2 matrix in object/eaqecc_16_4_8_4.json is a 16 x 32 generator matrix over GF(3) defining an entanglement-assisted qutrit code with n = 16, k = 4, c = 4 and exact minimum distance d = 8 (computed here by full enumeration of the symplectic dual outside the isotropic part), which is strictly above the live qutrit table's d_lower = 7 and not above d_upper = 9 for the cell [[16,4,7-9;4]]_3, as that page read on 2026-10-18.

## Gate notes
- Object: object/eaqecc_16_4_8_4.json, sha256 e2f4cb89b2b3c23d00e39c2126d5a3e094a9613fece4ba104dac17084c0e88c7.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- Full success criterion met for this cell; not a partial win. Only the primary cell is claimed; cells that follow from it by propagation rules are not claimed.
- Reproduce: the skeptic's own GF(3) checker and an exhaustive enumeration of the symplectic dual outside the isotropic part. Novelty: live qutrit table fetched 2026-10-18T14:23:13Z, sha256 equal to the claim record (page last changed 10.07.2025).
- The novelty skeptic lists newer literature it could not read in full as unresolved; the live table is the status source and is current, so this is not a downgrade.
- No downgrade triggers found.
