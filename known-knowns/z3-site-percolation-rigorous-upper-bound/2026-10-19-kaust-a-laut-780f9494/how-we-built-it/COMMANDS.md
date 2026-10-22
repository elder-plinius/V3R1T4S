# How we built it

Float probes (guides only, never part of the proof):
- code/gate.py: small blocks (up to 18 sites), LP domination (scipy). `python gate.py a b c bisect 0.5`
- code/gate3/main.go: blocks up to 27 sites; env GATE_RULE=L1 (face-weight tie-break), GATE_MINSIZE=s,
  GATE_MINFACES=m; writes law tables per p. `gate3 3 3 3 6 out_prefix p1 p2 ...`
- code/fmax.py (LP) and code/fmax2.py (up-sets): f(p), the largest q every entry law dominates at density p.
  Outputs: outputs/fgrid_s6.txt (p = 0.4425-0.467) and outputs/fgrid_hi_s6.txt (p = 0.47-0.57) for the locked rule.
- code/gate_lp.py: LP checks on gate3 tables.
The rule was locked from these probes (see HOW_WE_FOUND_IT.md); then the exact chain was run with object/code:
- outputs/chainB_summary.txt, chainB_log.txt: links 1-3 from q = 501/1000.
- outputs/chainA_summary.txt, chainA_log.txt: a seven-link run from q = 1/2; its links 4-7 (from q = 1781/4000) are
  the claim's links 4-7.
- outputs/chainW_summary_unpanelled.txt: the variant from q = 17/25 (Wierman's 2D bound), after the panel.
PREREG.md: the run's frozen rule (null test not needed: a deterministic certificate).
