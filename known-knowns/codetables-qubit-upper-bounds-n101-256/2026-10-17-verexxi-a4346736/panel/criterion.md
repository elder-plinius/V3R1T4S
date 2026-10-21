context: subagent (Claude Code headless on the owner's PC, fresh context)

# Criterion skeptic verdict for [[190,2]]

## What I did
- Read CLAIM.md, REPRODUCE.md, check/check_cert.py (full source).
- Ran: python -I check/check_cert.py result/cert_190_2_64_sh.json
  output: VERIFIED [[190,2,64]] shadow=True: value=2141 digits, max column coefficient <= 0, 62+2+64 multipliers (exit 0)
- Ran: python -I check/check_cert.py result/cert_190_2_63_sh.json
  output: VERIFIED [[190,2,63]] shadow=True: value=2141 digits, max column coefficient <= 0, 62+2+64 multipliers (exit 0)
- Ran check/parse_table.py and check/propagate.py on data/qubit_table_full_n1-256.html (the final one-liner reading closure.json failed only because I wrote output to a path that does not exist on this machine; check/propagation_check.txt, which I read, gives the same figures): live (190,2): [37, 64]; closure of the live table at (190,2): 63; R1 (190,1): [37, 64]; R2 (191,2): [37, 65]; R3 (189,3): [36, 63].
- Grepped data/QECC_q4_n190_k2_claimtime.html: "lower bound: 37", "upper bound: 64" for [[190,2]].

## Reasoning
- Criterion: n in 101..256 (190 ok); proof of nonexistence of [[n,k,d]] at d equal to the live upper bound (64), lowering the bound by at least 1; exact Farkas certificate of the quantum weight-enumerator LP (MacWilliams link, A_i <= B_i, A_i = B_i for 0<i<d, nonnegativity, shadow where used), checked in exact integer arithmetic by an independent script; not implied by propagation.
- check/check_cert.py is stdlib-only, integer-only, short, and the LP it encodes matches the criterion (rows E0, E1, Q_j, G_j, H_j; Farkas rule: every column coefficient <= 0 and positive value). I read the logic and found no flaw: index ranges are enforced, inequality multipliers are checked nonnegative, shadow multipliers are only allowed when flagged. Shadow nonnegativity is valid for every qubit stabilizer code (Rains), so using it is legitimate and is explicitly permitted by the criterion.
- Literal reading: the d=64 certificate (the live upper bound) verifies on its own, so the literal criterion is met. The d=63 certificate verifies too, and since any [[190,2,64]] code satisfies the d=63 constraints (A_j=B_j for j<63 is implied), the stronger statement "upper bound at most 62" is justified. This is a drop of 2, not a stretched one.
- Non-subsumption: the propagation closure over all live cells gives 63 at (190,2), so neither 64 nor 63 is the end of what propagation yields; the new bound of 62 is strictly below the closure. The three rules used are the ones named in the criterion. Neighbours (190,1)=64, (191,2)=65, (189,3)=63 do not imply 62 or 63 for the claimed cell beyond closure 63. The live page copy confirms the upper bound of 64 at claim time.
- Hidden quantifiers / null models: no quantifier over free parameters; a single cell, a single explicit certificate. Null check: the checker rejects non-positive value, positive columns, out-of-range indices, and negative inequality multipliers, so a bogus certificate cannot pass trivially. I did not rerun the checker against a deliberately corrupted certificate. Residual caveats: the table copy is a claim-time snapshot and I could not re-fetch live (not allowed); the criterion requires a live fetch immediately before claiming, which the claim records with a timestamp and hash. This is the only residual risk, and it is a freshness matter rather than a flaw in the proof. Also this is a bound on stabilizer (additive) qubit codes, which is exactly what the table covers.

confirmed_scope: No qubit stabilizer code [[190,2,63]] (hence none with d >= 63, including d = 64) exists, as shown by an exact integer Farkas certificate of the shadow-augmented quantum weight-enumerator LP verified by check/check_cert.py, which lowers the claim-time table upper bound for [[190,2]] from 64 to at most 62 (below the propagation closure of 63 computed from the saved complete table).

pass: true
