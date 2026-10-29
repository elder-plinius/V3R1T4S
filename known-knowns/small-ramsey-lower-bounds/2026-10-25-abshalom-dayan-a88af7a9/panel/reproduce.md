context: headless claude -p session (claude-sonnet-5-5, effort high), fresh, started inside a copy of claim/ .

# REPRODUCE verdict

Definition used (CLAIM.md): circulant on Z_132, edge {i,j} has the colour of (j-i) mod 132, d and 132-d the same distance. Need no K_3 in colour 1, no K_3 in colour 2, no K_9 in colour 3, so a 3-colouring of K_132 gives R(3,3,9) >= 133.

Checks (own code in work/chk.py and work/sat.py, written before opening verify_circ.py; all from the saved file object/R_3_3_9.txt):

- `shasum -a 256 object/R_3_3_9.txt` -> a88af7a9fb8fc8eb0ddf226628db6f59df6c1fb8504ed3ec80d2eeaf972a64cd (matches the claim).
- Format/partition: header `circulant 132 3`; the listed distances of the three colours are exactly 1..66, each once (assert passed). Colour degrees: `{1: 26, 2: 27, 3: 78}` (26+27+78 = 131 = N-1, so every edge has exactly one colour).
- Method 1, exhaustive (work/chk.py, Python standard library). Circulants are vertex-transitive, so a monochromatic clique can be translated to contain vertex 0; only cliques at vertex 0 were searched, and that search was complete.
  - Colour 1: `triangles through 0: 0`. Colour 2: `triangles through 0: 0`.
  - Colour 3: branch and bound over the 78 colour-3 neighbours of 0 gave `max clique in colour-3 nbhd of 0: 7 => omega_3 = 8`, so no K_9.
- Method 2, independent SAT (work/sat.py, CaDiCaL via python-sat): for colour 3, with variables for the 78 neighbours of 0, a clause for each non-adjacent pair and an at-least-8 cardinality constraint (so a K_9 with vertex 0). Output: `K8 containing vertex 0 in colour 3 satisfiable: True` (sanity: the encoding finds cliques) and `K9 containing vertex 0 in colour 3 satisfiable: False` (UNSAT, no K_9).
- Second opinion, after my own verdict: `python3 -I verify_circ.py object/R_3_3_9.txt 3 3 9` printed "colour 1: degree 26, no K_3 ...", "colour 2: degree 27, no K_3 ...", "colour 3: degree 78, no K_9 ...", "proves R(3,3,9) >= 133", "PASS". Two further runs had identical output (md5 e6324ed1c493853f34898f724b7acc33 both times), so no non-determinism seen.

Scope: I reproduced the object and the arithmetic (N = 132, so R(3,3,9) >= 133, which is above 129 as quoted in table_record.md). I did not re-fetch DS1 or search for newer papers; that is the NOVELTY skeptic's job. The Table XIb cell value 129 was only read from table_record.md, not independently confirmed.

Every property holds, the claimed value follows, and I found no mismatch, missing object or non-determinism.

pass: true
