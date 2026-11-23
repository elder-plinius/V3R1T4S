# Honesty gate (earth-moon-biplanar-10-chromatic)

status: CONFIRMED_PARTIAL
confirmed_scope: An explicit simple 19-vertex, 92-edge graph (object/biplanar_9crit_n19_e92.json) is edge-critical 9-chromatic (confirmed independently for chi <= 9 and for all 92 edge-deleted 8-colourings; chi >= 9 via the package's own DRAT check, run_checks.sh printing PASS), splits into two layers (45 and 47 edges) whose rotation systems each give V-E+F = 2 on a single component, and has an order and a canonical hash different from every one of the 42 reconstructed Sulanke and BGS-pool graphs; the extras 5-connected, non-join and (by my own check) clique-cutset-free also hold, but the BGS list is reconstructed rather than taken from the paper, and these extras are not part of p2.

## Gate notes
- Object: object/biplanar_9crit_n19_e92.json, sha256 2cf4ffc7aaf448d3135de8dc5352cf39b78eb275119af38056bf28678f8a1a2c.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- All three fresh-context skeptics passed (reproduce.md, novelty.md, criterion.md). The REPRODUCE skeptic checked both layers' planarity (Euler on the rotation systems, zero crossings in the integer drawings, networkx), regenerated the 8-colouring CNF and verified the shipped DRAT proof with drat-trim (CaDiCaL also UNSAT), and checked all 92 edge-deletion 8-colourings.
- Live status pages fetched by the panel on 2026-11-18 (HTTP 200): optimizationproblems 27b lists lower bound 9 and upper bound 12; Epoch lists the problem as unsolved. No published 9-critical biplanar graph has 19 vertices (Sulanke n=11; Boutin-Gethner-Sulanke n=12..16; Gethner-Sulanke n=17, 25, 33).
