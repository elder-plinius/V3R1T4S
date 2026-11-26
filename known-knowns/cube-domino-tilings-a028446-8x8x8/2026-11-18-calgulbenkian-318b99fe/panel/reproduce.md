context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE report, cube-domino-tilings-a028446-8x8x8, partial win p1 (A049507(7), P_6 x P_6 x P_7)

## Own checker (written before reading any package code)
- Definition used: perfect matchings of the grid graph P_a x P_b x P_c (vertices (x,y,z), edges between points at
  distance 1). Broken-profile DP in C, my own state encoding (bitmask of already-matched future vertices, window
  relative to the current vertex) and my own vertex order (sorted by x+y+z, ties lexicographic). Each step is a
  k-way merge of sorted streams. Arithmetic modulo three 61-bit primes (2^61-1, 2^61-31, 2^61-45; primality checked
  in the CRT script), one prime per run, recombined by CRT.
- Validation, CRT output, all exact matches to OEIS: P_4xP_4xP_4 = 5051532105 (A028446(2)); A028446(1)=9 (2x2x2);
  A049507(1..5) = 6728, 53786626921, 57248060375968384, 123115692449982216049513, 216388579168758145017797108072;
  P_6xP_6xP_6 = 417898687046465734392674187695263185 = A028446(3) = A049507(6). A049507(0)=1 by convention
  (empty grid; my program does not run N=0, it is trivially 1).
- Cost: 6x6x6 peak 1.45e8 states; 6x6x7 peak 1.037e9 states, about 25 min per prime on one thread (16 bytes per
  state), about 1.3 hours for the three primes, under heavy machine load. Well inside the 3 hour limit.
- Result for P_6xP_6xP_7 (3 primes, residues 2070855326039171090, 2219099346247943366, third run 443605481731654174;
  CRT): 781760467628825425251897322894619609502208. Equals the claimed A049507(7) digit for digit. Even, as
  parity expects (parity/GF(2) determinant not separately recomputed by me).
- Note: I ran one vertex order only (my own diagonal order). The second order, with different code, comes from the
  package's two programs below, so the two-orders requirement is covered by my run plus theirs, not by two runs of mine.

## OEIS fetches (curl -A 'V3R1T4S-research (honest client; curl)')
- 2026-11-18T17:31:45Z https://oeis.org/A049507/list HTTP 200 sha256 6b9825399308ab77a642d11d695dd44a9002e0e6d92779495ef6984f229dfc1d
  Data lists n=0..5 only (1, 6728, 53786626921, 57248060375968384, 123115692449982216049513,
  216388579168758145017797108072). A(7) not in DATA.
- 2026-11-18T17:31:45Z https://oeis.org/A028446/list HTTP 200 sha256 e11771ebde287ee25e778ab9eee5a99d51615567f82a53cae63eae4a8042dabf
  Data lists a(0)=1, a(1)=9 and the later terms; used for a(1..3). (I did not read the page past the header lines;
  the a(3) value matched the task's stated value.)
  Not a novelty check: no literature search was part of this role.

## Package checks, run in a copy of this package
- sh verify-it-yourself/run_checks.sh: PASS (about 4 min wall). It reproduces A049507(0..5), A028446(3)=A049507(6),
  A028454 terms, and the fresh-prime residues of P_6xP_6xP_7 mod 21713 (=9050) and mod 21683 (=16489).
- how-we-built-it/domino_mitm_a.c --solve-667: RESULT A049507(7) = 781760467628825425251897322894619609502208,
  10-prime CRT, overdetermined 4-prime check PASS.
- how-we-built-it/domino_tilted_b.c --solve-667: calibration 16/16 pass; RESULT A049507(7) =
  781760467628825425251897322894619609502208, 15-prime CRT, overdetermined 5-prime check PASS.
- All three programs agree with each other and with my independent code.

## Verdict (reproduction only)
The claimed value 781760467628825425251897322894619609502208 for P_6xP_6xP_7 is reproduced by my own independent
DP (validated on the stated small cases and A028446(3)) and by both package programs. Not assessed here: novelty,
whether the value is already published, and the criterion wording.

pass: true
