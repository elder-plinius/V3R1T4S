# Criterion skeptic verdict: ccd-glue-potential-al-pb-clusters, Pb N = 121

context: subagent (Claude Code Agent tool, fresh context)

Scope: only claim/ was read. Independent checks were run with my own evaluator, written directly from data/lead.f. It parses the Fortran DATA blocks and uses the Fortran branch semantics. I did not use code/lead.py or code/certify_pb.py for any number below.

## Clause by clause

1. **Exact potential (Lim-Ong-Ercolessi, data/lead.f).** Every hash in data/SHA256SUMS checks OK (162 entries, 158 point files). code/lead.py is a faithful transcription of lead.f: I checked the constants, the region boundaries (GE/GT), and that the v2 region III is unreachable because RC < A. My evaluator includes region III anyway, and it agrees. MET.

2. **Calibration (ten random posted files to 1e-6 eV).** Ten files were drawn with SystemRandom: [11, 89, 90, 101, 104, 108, 112, 132, 140, 143]. For each, |E_mine - table| was ≤ 4.86e-07 eV. The largest was N = 108 at 4.86e-07, and N = 121 itself gave 4.24e-07. MET.
   Caveat: posted file 116 evaluates to -189.35189750897192 against a table value of -189.351998, a difference of about 1.0e-4. A draw that included 116 would fail at the 1e-6 level. This is an inconsistency between the table and the posted file, not a checker fault, but the gate should know that a "random 10" can fail for this reason.

3. **Units.** The table states "The unit of energy is eV". The evaluator works in eV and Angstrom, which are the table's units. The gradient therefore comes in eV/Angstrom. MET.

4. **Margin of at least 1e-4 eV against the live table.**
   - E_obj (30-digit) is -198.4790291662722464899 eV. The recorded table row for N = 121 is -198.211397. The difference E_obj - table is -0.267632166272 eV.
   - The recorded fetch is 2026-11-23T07:06:49Z, HTTP 200, with sha256 dce45e7b... (data/lead_table.html). That is the record of a fetch earlier the same day, not a proof of freshness at claim time.
   - Gate must re-check: fetch the lead table.html live immediately before claiming. Confirm that row N = 121 still reads -198.211397, or anything above -198.479129 + 1e-4. Ideally also confirm the sha256 is unchanged.
   - Met on the recorded data; at claim time it is conditional on that re-fetch.

5. **Published values.** I ran my own web searches: "glue potential clusters lead" and "arXiv glue potential clusters Pb global minimum Lim Ong Ercolessi". They return only these:
   - cond-mat/0207432 (Doye-Hendy, the source of the table)
   - cond-mat/0405234 (Gupta, a different potential)
   - cond-mat/0012167 (MD, 600-4000 atoms)
   - the CCD pages

   None reports a Pb glue value for N = 121 below the table. Google Scholar could not be queried directly: web search was the proxy, as it was for the author. The record in claim.md is adequate. MET, within that limit.

6. **Certified local minimum.** The claimant's certify_pb.py polishes in float64 and only evaluates the gradient in mpmath. That is weaker than the literal "polish in mpmath (30 digits)". I therefore reran a real 30-digit polish:
   - Coordinates were held as mp.mpf (dps = 30) and updated by Newton steps, with the mp gradient and the float64 FD Hessian with the zero modes projected out.
   - |g|_mp went from 5.0725e-14 at iteration 0 to 1.3944e-23 at iteration 1, which is < 1e-10.
   - Double-precision 363x363 Hessian (central differences, h = 1e-5): 6 eigenvalues are near zero, the largest of them in magnitude 1.72e-11. There are 0 negative modes below -1e-6. The 7th smallest |eig| is 0.14898, a wide gap.
   - Minimum interatomic distance is 3.0044 Angstrom, so there is no pathological contact.

   MET.

7. **Distinct basin.** I polished posted 121 the same way: E went to -198.2113965758774331371 and |g| to 1.8e-25, with 6 zero modes and 0 negative. E_obj - E_posted_polished = -0.267632590395 eV, which exceeds 1e-4. MET.

8. **One object / one cell per claim.** The claim covers one structure for one cell (Pb, N = 121). It holds.
   Minor: the bank's status_source is the Al page. The target id "al-pb", the criterion's "(metal, N)" and "Pb: Lim-Ong-Ercolessi" all explicitly admit lead, so this is not a stretch.

## Stretches and notes
- The authors' certifier does not literally polish in 30 digits. My independent mpmath polish closes this gap.
- The freshness of the table is a gate obligation, as described in clause 4.
- The N = 116 file/table mismatch is a hazard for random calibration, as described in clause 2.
- No null-model failure: the object's energy comes from an independently calibrated evaluator, not from the claimant's code. The bars are reference material only and are not part of the criterion.
- The margin of 0.2676 eV is large for a 2002 "global minimum" table. Still, it reproduces exactly with independent code, and the result is a genuine full-criterion win, not a partial one.

confirmed_scope: The 121 coordinates in result/Pb_121.xyz form a certified local minimum of the Lim-Ong-Ercolessi Pb glue potential (data/lead.f) at -198.47902916627225 eV, 0.26763 eV below the N = 121 value of the lead table as fetched 2026-11-23T07:06:49Z (-198.211397 eV), and 0.26763 eV below the polished posted N = 121 structure, with no lower published value found by web search; this is conditional on the gate's live re-fetch still showing -198.211397 (or any value above -198.479029) for N = 121.
pass: true
