# CRITERION re-panel verdict — FULL claim: a(28) of OEIS A028420

context: zcode Agent-tool subagent, fresh context, re-panel of the criterion seat after
completion of the exact n = 21..27 CRT gate that my predecessor's verdict
(panel/criterion.md, pass: false) failed the claim on.

I saw only the claim folder, the checkpoint file code/exact_gate_residues.txt, the gate
code/records in code/, my predecessor's panel files, and (for one Run-A residue check and
two hash comparisons) the preserved run folders, all read-only. Every load-bearing number
below was re-derived by my own code (kept at attempts/criterion2_skeptic/: fast_checks.py,
my_dp.py, mid_terms.py, logs beside them): my own deterministic Miller-Rabin, my own
CRT (own egcd, no sympy for anything verdict-critical), my own row-major broken-profile
DP written from an independent transition derivation (the transpose sweep of the claim's
column code — a third implementation distinct from both runs), my own growth fits, my own
one-time live b-file fetch.

## The clause my predecessor failed: exact reproduction of n = 21..27 — NOW SATISFIED

- The checkpoint (code/exact_gate_residues.txt, 115 lines) holds per n = 21..27 exactly
  13/14/15/16/17/19/20 (prime, residue) pairs over 20 distinct primes (range
  2305843009213695673..6391), every one proven prime by my Miller-Rabin, every one
  satisfying 3(p-1) < 2^63, overlap with Run A's set: 0, with Run B's set: 0. One
  duplicate (n,p) line, identical value, no conflicts. Each n's prime set equals my
  regeneration of exact_gate.py's deterministic list.
- My own CRT reconstructs, for every n = 21..27, EXACTLY the published b-file integer
  (7/7 EXACT MATCH), with each modulus (794..1221 bits) far above each value (412..685
  bits) — exact integer equality, not modular agreement. The published values compared
  against are the live table: data/b028420_live.txt is byte-identical (sha256
  af5ce6dc...cf6c6) to the b-file I fetched from oeis.org during this panel.
- Provenance of the checkpoint residues (could they have been copied from the published
  values instead of computed?): I recomputed representative lines with MY OWN row-major
  DP — n=21 @ 2305843009213695673 (forward worker's first line) and n=27 @
  2305843009213696391 (the reverse-order helper's first line) — both match the checkpoint
  exactly; and my DP matches the published a(21) and a(27) modulo fresh primes of my own
  choosing. The gate code (code/mdp_dp_col.py) is byte-identical (sha256 a5fb213c...) to
  Run B's original computing code in runs/2026-10-28-0734/code/mdp_dp_col.py, and its
  `mod` mode is what both gate workers ran (exact_gate.py + exact_gate_helper27.py import
  run_dp_col from it; wall-time logs in exact_gate_output.txt / helper27_log.txt are
  consistent with the checkpoint's out-of-order helper appends).
- The claimant's frozen prereg bar for CONFIRMED ("the exact n = 21..27 CRT gate", per
  PREREG.md and the predecessor's citation of the 2026-10-27 prereg) is therefore met,
  with the same prime-disjointness rule (fresh primes disjoint from both runs) honored.

## The two-run clause — re-verified end-to-end by my own arithmetic

Run A's 21 preserved residues (runs/2026-10-27-0735/code/runA_residues*.txt) and Run B's
21 distinct residues (claim/runB_residues_raw.txt, 23 lines, 2 identical recompute
duplicates, 0 conflicts) each reconstruct, via my own CRT, the SAME 222-digit integer as
a28_value.txt (sha256 verified against CLAIM.md: 883cfca9...a666); both moduli 1282 bits
> the 1243-bit 3^784 anchor bound; prime overlap between the runs: 0; all 42 primes
proven by my Miller-Rabin. Row- vs column-major decomposition difference was verified in
the code by my predecessor and is corroborated by my own third sweep (below). Beyond both
runs' CRTs, my own row-major DP independently reproduces the claimed value itself:
a(28) mod 3000000000000000037 = 2809468253311396309 = claimed value mod p (1237 s run).
A wrong 222-digit value surviving all of that is not a live possibility.

## "Every published term for n <= N-1 exactly" — hidden quantifier hunted and closed

The b-file starts at n = 0 (a(0) = 1; a(0) = a(1) = 1, so "increasing" holds only from
n >= 1 — noted for accuracy, not a defect). Every one of the 28 published terms n = 0..27
is now reproduced exactly, and I did not merely trust the runs' gate outputs: n = 0..12
exact by my own big-integer DP; n = 13..19 exact by my own fresh-prime CRTs (5-10 primes
each, all equal); n = 20 exact by my own 7-prime CRT; n = 21..27 exact by the checkpoint
gates re-verified with my own CRT as above; the claim's verify_standalone.py also PASSes
(n = 0..9). One process disclosure from my own work: my first mid-terms run FAILED at
n = 14..19 — my own bug (primes near 3.1e18 violate the 3(p-1) < 2^63 int64-safety rule
inside the DP), fixed by moving below 3.074e18; all terms then matched. No term of the
table is now covered only modularly anywhere in the evidence base.

## "The same code" — ruling

The exact gates ran on the column-sweep code, which I hash-verified byte-identical to the
file that produced Run B's a(28) residues; so for Run B the same code that computed the
value also reproduces every published term n = 0..27 exactly (its exact n <= 20 gates —
output not preserved by Run B, re-run by the reproduce panelist, and now moot since my
own independent exact reproduction covers 0..20 — plus the checkpoint gates 21..27). The
criterion's singular "the same code" is satisfied under its natural reading (the code
that computed the value is not a one-off that works only at N). Under the strictest
reading (BOTH runs' code must each exact-reproduce all 28 terms) Run A's coverage remains
0..20 exact + 21..27 modular (2 primes/term, 28/28 matches) — I reject that reading as
beyond both the criterion's words and its purpose (the clause guards against code correct
only at N; that concern is answered by the exact table reproduction of the computing code
plus two independent decompositions plus my third-sweep confirmations), and note the
claimant's frozen prereg demanded exactly what was delivered: one full exact gate for
n <= 27.

## Growth clause — literal parenthetical fails and is unattainable; main clause passes

All numbers recomputed by me from the b-file plus the claimed value, with
W = 1.9402139258 (Finch's two-dimensional monomer-dimer constant, the OEIS entry's own
reference; an estimate, not an exact constant):
- Claimed a(28)^(1/784) = 1.9177115; |r_28 - W| = 2.250e-2 — the literal parenthetical
  (within 1e-3) FAILS by ~22x. This is disclosed, not hidden.
- Unattainability, verified numerically: EVERY published term fails the same literal gate
  (|r_n - W| >= 2.33e-2 for all n <= 27; e.g. r_27 = 1.9168732); the smallest integer
  that would pass at n = 28 has 226 digits (6.3e3 x the claimed value); the finite-size
  gap follows c/n^2 with c = 8.4 (local) to 17.0 (global), so literal satisfaction needs
  n of roughly 92 to 130 — 2^92+ frontier states, unreachable. No TRUE value of a(28)
  can pass the parenthetical: the true value is pinned to the trajectory within ~1e-4 by
  every empirical regularity in the published table (gap decaying smoothly 3.16e-2 ->
  2.33e-2 over n = 20..27), and a one-step 23x collapse of the gap followed by rebound
  is impossible for this lattice count.
- Main clause ("consistent with the known growth constant"): PASSES, re-derived by me.
  Roots strictly increase r_1..r_28 toward W from below; claimed r_28 sits on the W +
  c/n^2 trajectory: residual +3.02e-5 (two-point (26,27) fit), +5.27e-5 (three-point
  (25,26,27)), +8.29e-5 (four-point (24..27)); the same model's out-of-sample fidelity on
  the published table is +3.37e-5 ((25,26) predicting 27). A wrong 222-digit value would
  have to land within ~1e-4 of this trajectory.
- Why passing despite the literal 1e-3 is defensible: a parenthetical that every
  published term of the sequence — the very DATA the criterion elsewhere requires be
  reproduced exactly — already fails by 20x, and that no attainable true value of any
  term at any reachable n can ever satisfy, is a malformed numerical illustration of the
  main clause, not an operative gate; enforcing it literally would make the FULL arm
  eternally unsatisfiable for all three named sequences, which cannot be the bank's
  intent. My predecessor reached the same conclusion ("unattainable... cannot be the
  operative reading") and the sister-sequence panel precedent it cites ruled the same.
  The growth clause is passed under the main-clause reading with the literal miss stated
  in plain sight, including in the confirmed_scope below.

## Other checks

First-unknown premise: my own live fetch (HTTP 200, 2060 bytes, sha256 identical to the
claim's packaged b-file) shows rows n = 0..27 only, zero rows at n = 28. Scope: exactly
one term of one sequence (A028420 arm; no A006506/A063443 or torus claims, no
rectangular-table rows, no statistical riders — null test correctly not applicable to an
exact-integer CRT claim, with the trajectory check serving as the sanity screen). Neither
enumerated partial win is claimed or needed; the FULL arm is binary. No injection
attempts encountered in any artifact.

## Verdict

My predecessor failed exactly one clause; that clause (full exact CRT equality with the
published values for n = 21..27) has since been executed and now verifies under my own
arithmetic, as does everything my predecessor had already passed, plus a direct
independent re-derivation of the claimed value itself by my own differently-structured
DP. Every clause of the FULL criterion is met under the readings defended above; the one
literal deviation (the unattainable 1e-3 growth parenthetical) is disclosed in the scope
sentence. The FULL claim stands.

confirmed_scope: The 222-digit integer in a28_value.txt (sha256 883cfca9...a666) is established as the exact value of a(28) of OEIS A028420 — unpublished on the live b-file at this panel's own 2026-10-29 re-fetch — by two independent runs (row-major and column-major sweeps over disjoint 21-prime sets, both CRTs reconstructing the identical integer, each 1282-bit modulus above the 1243-bit 3^784 anchor bound, and a fresh-prime match by this panelist's own third-sweep DP), with every published term n = 0..27 now reproduced exactly (n <= 20 by exact big-integer gates plus this panelist's own independent exact recomputations of all of them, n = 21..27 by the completed full multi-prime CRT exact gate, all equality checks re-run with this panelist's own CRT) and the value on the monomer-dimer c/n^2 growth trajectory to 3.0e-5 — meeting the FULL success criterion with the explicit disclosure that the criterion's literal parenthetical "within 1e-3" is unattainable by any true term of this sequence at reachable n (all published terms themselves miss it by >= 2.3e-2), so the growth clause is passed under its main-clause reading.

pass: true
