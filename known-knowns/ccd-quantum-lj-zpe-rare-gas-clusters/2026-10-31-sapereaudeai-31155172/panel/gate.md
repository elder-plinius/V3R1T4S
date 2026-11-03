# Honesty gate: run 2026-10-31-1915, ccd-quantum-lj-zpe-rare-gas-clusters, N = 38 Ne

status: CONFIRMED_SOLUTION
confirmed_scope: The 38-atom configuration in object/N38_Ne.xyz (sha256 31155172...0fe1), as written with 18 significant digits, is a certified local minimum of the classical Lennard-Jones energy (E_LJ = -168.984987247422, gradient norm 1.641e-13, exactly 6 |lambda| < 1e-6, lowest eigenvalue -9.65e-14), and its harmonic Ne energy E_LJ + (0.095/2) sum sqrt(lambda) over its 108 nonzero eigenvalues is -108.929936, which is 1.505626 below -107.42431, the lowest Ne value (row 38B) for N = 38 on the LJZPE table at www-wales.ch.cam.ac.uk/~florent/LJZPE/table.html (unchanged as of 2026-10-31T19:40Z), with the table convention reproduced on rows 17A, 31B, 38A and 38B to within 1.1e-5; comparison against other published harmonic-ZPE values was not checked by this skeptic.

gate_time: 2026-10-31T19:48:17Z (date -u)

## Reading of the three panel files (by the run's main session)

- reproduce.md (fresh subagent): pass: true. Its own 60-digit Decimal checker, written before it read the author's
  code, gives E_LJ -168.984987247421833, gradient 1.641070e-13, exactly 6 |lambda| < 1e-6 and none negative, lowest
  nonzero 0.8097800344288, E_Ne -108.9299361314, and margin 1.5056261314 against -107.42431 (38B), which it read
  itself from the table. Its calibration on 17A, 31B, 38A and 38B agrees within 7.2e-6. Its runs are deterministic
  and the sha256 matches. No mismatch.
- novelty.md (fresh subagent): pass: true. It fetched the live table once at 2026-10-31T19:37:09Z (HTTP 200,
  byte-identical to the claim's copy; lowest N = 38 Ne value -107.42431). The lowest published harmonic Ne38 value it
  found is -107.42431, from the table and from Predescu, Frantsuzov and Mandelshtam 2005, Table I (state 4 = 38B).
  Deckman et al. 2008 and 2009 and Mallory and Mandelshtam 2018 give no comparable harmonic number. No TROPHY_CASE,
  known-knowns or PR entry. The object is not a trivial edit of 38A or 38B, nor an LJ39 deletion.
  **Caveat carried forward:** the object's classical energy equals, to printed precision, that of "state 3" in
  Predescu et al. 2005 (-158.312 K/atom), which that paper reports with neither coordinates nor a harmonic value.
  The structure may therefore have been seen before as a classical minimum. Only the harmonic Ne value is new, and
  the scope says nothing about the structure being new. Credit for a possible prior classical identification goes to
  that paper.
- criterion.md (fresh subagent): pass: true. Every clause holds literally. It fetched the table once itself at
  19:40:18 GMT (identical bytes). The object is stationary on the classical surface; the quantum-corrected surface's
  gradient there has norm 6.4e1, so it is not a quantum-surface re-optimisation. Its null checks (perturbed and
  rounded objects, the table's own structures, a naive 150 s search) all fail as they should. It reviewed the claim
  as one object in one cell. It explicitly left the published-harmonic-value clause to NOVELTY, and NOVELTY covered
  it. That is a division of roles, not a hedge.

## Downgrade checks (kit/RUN.md step 7)

- Hedging panelist: none. Each passes and states its own scope. The CRITERION scope sentence names what it did not check.
- Reproduction mismatch: none (three independent codes plus the author's checker agree to the printed digits).
- Strictly better than the live table: yes, by 1.505626 (needs 5e-4). The panel fetches at 19:37Z and 19:40Z are under 6 h old.
- Stretched criterion or hidden quantifier: none found. The calibration rows reproduce, the object is a classical
  minimum, and the margin is against the minimum over the A/B rows.
- Scope wider than reproduced: no. The scope sentence is the CRITERION panelist's, verbatim.
- Sample presented as complete, or capped search used as an exclusion: none. No coverage is claimed.
- Evasion in table access: none. Every fetch was one plain request with a client naming V3R1T4S or the tool default.
- Bundling: none. One object, one cell. The N = 36 Ne, N = 37 Ne and N = 67 Ar objects are separate, unpanelled leads.
- Benchmark baseline: not applicable (an explicit object against a table value).

Final status: CONFIRMED_SOLUTION (stands only if kit/check_run.py prints CHECK_RUN: PASS).
