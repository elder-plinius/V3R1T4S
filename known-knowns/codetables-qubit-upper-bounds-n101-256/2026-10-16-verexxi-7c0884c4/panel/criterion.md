context: subagent (Claude Code headless on the owner's PC, fresh context)
confirmed_scope: For the single qubit cell (n,k)=(183,1), the saved table record (live upper bound 61, fetched 2026-10-16) is lowered by at least 1 (to at most 59 via d=60, and d=61 itself is also excluded) by exact integer Farkas certificates of the quantum weight-enumerator LP with Rains shadow constraints, and the saved complete table gives a propagation closure of 61 at that cell so the bound is not implied by other cells; this says nothing about any other cell and rests on the saved table, not a fresh live re-fetch by me.

## Reasoning

Criterion (verbatim in CLAIM.md): for some qubit cell 101<=n<=256, proof that no [[n,k,d]] exists for d = live upper bound, via exact rational Farkas certificate of the QWE LP (MacWilliams link, A_i<=B_i, A_i=B_i for 0<i<d, nonnegativity, shadow where used), checked in exact integer arithmetic by an independent script, and not implied by standard propagation rules. Cell (183,1) has n in range. This is the full criterion, not a partial win.

Checks I ran (inside the claim folder):
- `python3 -I check/check_cert.py result/cert_183_1_60_sh.json` -> `VERIFIED [[183,1,60]] shadow=True: value=1980 digits, max column coefficient <= 0, 59+2+60 multipliers`, rc=0.
- Same for `result/cert_183_1_61_sh.json` -> `VERIFIED [[183,1,61]] shadow=True ... 60+2+61 multipliers`, rc=0. The literal criterion (d equals the live upper bound 61) is therefore met directly, and d=60 gives the stronger drop to 59. (A code with d>=60 also satisfies the d=60 constraints, so excluding d=60 excludes all d>=60.)
- I read the checker source: pure integer arithmetic, computes every column coefficient of the combined multipliers, requires inequality multipliers >= 0, requires positive value, and restricts index ranges (u_Q in 1..d-1, v_G in d..n). The logic matches the Farkas argument in its docstring. It is a separate script from whatever produced the certificates.
- Sanity of the LP formulas (Krawtchouk, MacWilliams, shadow): for the [[5,1,3]] code with A=(1,0,0,0,15,0), the checker's kraw gives B=(1,0,0,30,15,18) and shadow identical (nonnegative), the known values.
- Null/negative tests: dropping the first v_H multiplier -> `(False, 'column 63 has positive combined coefficient')`; setting shadow=False with no shadow multipliers -> `(False, 'column 62 has positive combined coefficient')`. So the certificate is not trivially valid and genuinely depends on the shadow constraints (which are valid for stabilizer codes, so this is an allowed ingredient).
- Table record: data/QECC_q4_n183_k1_claimtime.html reads "lower bound: 36, upper bound: 61" and the page itself notes n>100 upper bounds are weak and not necessarily monotone in k.
- Propagation: `parse_table.py` + `propagate.py` on data/qubit_table_full_n1-256.html give live (183,1)=[36,61], closure 61, neighbours R2 (184,1)=[36,62], R3 (182,2)=[35,61]. R1 does not apply (k=1). So 59 or 60 is not implied by the rules listed in the criterion.

Residual concerns (do not change the verdict): I did not re-fetch the live page (not permitted); the "re-fetched immediately before claiming" condition rests on the saved record timestamped 2026-10-16T21:01:41Z. The bound is weak-region improvement (table bounds for n>100 are loose), so significance is modest but the criterion is literal about only requiring the drop. The table's own method for 61 is unknown; I cannot rule out that other tables already know a smaller bound, but the criterion is defined against the live codetables.de bound.

pass: true
