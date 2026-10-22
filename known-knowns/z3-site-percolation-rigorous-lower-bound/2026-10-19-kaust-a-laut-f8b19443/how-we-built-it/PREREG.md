# PREREG (frozen 2026-10-19T06:30:24Z, before the N = 18 and N = 20 outputs of this run exist)

Disclosure. Exploration in the same live session (explore/z3-site-lower/) preceded this freeze and its outputs were
seen: NAW counts to n = 18, Alm certificates up to (18,6) = 0.243582, and the canonical-geodesic criterion for
N = 10, 12, 14, 16 (0.250856, 0.254646, 0.257568, 0.259894). The N = 18 and N = 20 jobs (explore/z3-site-lower/
canon/par/par.exe, PID 17196 for N = 18, started 2026-10-19 01:23 local) were launched before this freeze; at the
freeze time p18.txt is empty (0 bytes) and p20.txt does not exist.

Criterion (target.md, verbatim): A rigorous proof that p_c^site(Z^3) >= p* for an explicit rational p*, strictly
above every explicit rigorous lower bound published (or directly implied by published results) at verification
time, whose finite part is an exhaustive computation in exact integer or rational arithmetic released with code a
stranger can rerun.

Method fixed now (proof skeleton):
- Canonical geodesics: BFS tree of the open cluster of 0, parent = the neighbour at distance d - 1 in the smallest
  direction index (+x,-x,+y,-y,+z,-z). A tree path v_0..v_N is a neighbour-avoiding walk; its forced-closed set F is
  (i) every off-path site adjacent to v_i and v_j with j - i >= 3, and (ii) at each turn v_{k-1} v_k v_{k+1}, the
  corner u = v_{k-1} + v_{k+1} - v_k when, seen from v_{k+1}, its direction index is smaller than that of v_k.
- Finite criterion: theta(p) <= K_N(p) theta(p) with K_N(p) = sum over N-step NAWs gamma from 0 of
  ext(gamma) p^(N+1) (1-p)^|F(gamma)|, where ext counts neighbours of v_N off gamma, adjacent to no other path
  vertex, not in F. Hence K_N(p) < 1 implies theta(p) = 0 and p_c^site(Z^3) >= p.

Checker and statistic:
- Counts: ext[f] for each f, exact 64-bit integers, from an exhaustive enumeration (par.exe, sign-flip symmetric,
  parallel). The run's claim also needs an INDEPENDENT implementation written from this definition (self-break or
  panel) that reproduces ext[f] exactly for at least one N >= 12 and the walk totals a_N.
- p* = the largest j/10^6 with K_N(j/10^6) < 1, evaluated in exact rational arithmetic (kcheck.py), at the largest N
  completed in this run (N = 20 planned; N = 18 is the fallback).

Thresholds:
- Claim: p* > 0.21103 (the record) with the checker passing and the independent reproduction matching.
- Reported, not part of the criterion: whether p* > 5/19 = 0.263158 (Torquato-Jiao, unproven).
- No result: any failure of exact reproduction, or any gap in the proof skeleton found by self-break or the panel.

null_test: not needed because the result is a deterministic proof certificate (exact counts checked against an
explicit inequality); no search statistic or "beats chance" claim is made.
