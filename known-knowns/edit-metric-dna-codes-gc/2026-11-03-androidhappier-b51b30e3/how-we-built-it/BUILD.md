# How the object was built (exact commands)

Run from the package folder in a fresh shell. Needs a C compiler (tested with gcc 14.2) and the C math library;
nothing else, nothing to pin.

    gcc -O2 -o dnae how-we-built-it/dnae.c -lm
    mkdir -p out && ./dnae 9 3 2 103 3000 out/p 20000 1042   # n=9 d=3 G=2 seed=103 cap=3000 s, restart length 20000, stop at 1042
    cmp out/p_n9_d3_G2_k1042.txt object/code_n9_d3_k1042.txt && echo identical

Arguments of dnae: `n d G seed seconds outprefix [restartL] [target]`. The candidate words are all words of length n
over ACGT with GC weight floor(n/2) and d(x, rc(x)) >= d (for (9,3): 63224 words, as printed on the first stderr
line). A vertex of the search graph is an orbit of a symmetry group K that always contains the reverse complement; G
selects K (dnae.c line 4): 0 = {id, rc} (orbits are the pairs {x, rc(x)}), 1 = <rc, reversal>, 2 = <rc, (C G)>
(C<->G swap at every position), 3 = <reversal, (C G), (A T)>. An orbit is admissible when its words are pairwise at
edit distance >= d; two orbits conflict when any of their words are at distance < d; a set of pairwise
non-conflicting orbits gives a code by taking one word from each rc-pair (valid because d(rc x, rc y) = d(x, y), so
the reverse-complement constraint is the same as the pair condition). For (9,3) with G = 2 the program reports
15806 orbits, 15084 admissible. The search is a weighted multi-neighbourhood tabu search (ADD / SWAP / DROP with tabu
tenure, restarts every restartL iterations; the move scheme follows Wu, Hao and Glover's multi-neighbourhood tabu
search for maximum-weight clique, implemented from scratch) for a maximum-weight independent set in the orbit
conflict graph. With G = 2 the code together with its reverse complements is closed under the C<->G swap.

Every time the best size improves, the program writes `OUTPREFIX_nN_dD_GG_kSIZE.txt` (one word per line) and prints a
FOUND line on stderr; it stops at `target` or at the wall-clock cap and prints a BEST line on stdout.
Determinism: xorshift generator seeded from the seed argument; restarts are iteration-based, so the wall-clock cap
only decides when to give up. Cost: the neighbour-list precompute for 63224 words takes about 50-60 CPU-s on an idle
core (about 20 min of wall time on the loaded shared machine of the run), then about 8.2 million tabu iterations
(1-3 CPU-min on an idle core). It writes one file per improvement (521 files up to k = 1042).

## Provenance and regeneration status

- Original (claim run, bounded push, nice 19, timeout 1800, heavily loaded shared machine, load average about
  90-110): `./dnae 9 3 2 103 ... 20000 1100` (target 1100). Log header `n=9 d=3 w=4 valid=63224 fullreps=7950
  avgdeg=182.3`, `G=2 Korbits=15806 admissible=15084`, ..., `FOUND k=1042 it=8159505 t=612.7 restarts=404`
  (file written 2026-11-03 15:06:35 EST = 20:06:35Z); the job then ran into its timeout without a larger code. Its
  k = 1042 file is object/code_n9_d3_k1042.txt (sha256 b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a).
- Claim run's same-seed rerun (started about 15:09 EST, nice 19, timeout 2400):
  `nice -n 19 timeout 2400 ../push/dnae 9 3 2 103 2300 r 20000 1042` -> `FOUND k=1042 it=8159505 t=595.4
  restarts=404`, `BEST 1042 its=8159505 restarts=404 t=595.4`, file written 15:29:30 EST (20:29:30Z); `cmp` with the
  object: identical.
- Panel (REPRODUCE skeptic, panel/reproduce.md): rebuilt dnae from this dnae.c (sha256 b4a39bfb...) and ran
  `nice -n 19 timeout 1260 ./dnae 9 3 2 103 1200 out/p 20000 1042` (15:26:24-15:42:55 EST). All 521 FOUND lines are
  identical to the original log once the t= wall-time fields are removed, ending `FOUND k=1042 it=8159505
  restarts=404`; the regenerated p_n9_d3_G2_k1042.txt is **byte-identical** to object/code_n9_d3_k1042.txt. So the
  reproduce panel got a byte-identical regeneration.
- The object was also verified directly: four checkers in the run (check_dna.py, check3.py, check4.py with full DP,
  check2.c), 60/60 single-symbol mutations rejected, the reproduce skeptic's own C checker and edit-ball checker, the
  criterion skeptic's own C checker, and verify-it-yourself/ here, all exhaustive over every pair. The claim rests on
  the object, not on the rebuild.

## Files
- dnae.c: the search program, copied unchanged from the run (claim/search/dnae.c, sha256
  b4a39bfb177aa436f575f73c0ddf3393f77ae56b483721fe543dbdc613a21a81; the same file as in the other packages of this
  family).
- PREREG.md: the run's preregistration, copied unchanged (sha256
  3712b6ee84639c9c72f260b33199e024a5a7947294c4e2f0f6a00c158273082d, frozen 2026-11-03T19:35:31Z = 14:35:31 EST,
  before the run's claim/ and data/ folders existed). It discloses that a 1011-word candidate already existed (from
  the carrier run, G=0 seed 7) when this one-cell run was opened, fixes the decision rule (claim the largest code that
  all four checkers call VALID at the end of a bounded push of at most 30 min, at most 3 concurrent jobs, nice 19)
  and binds the claim to the bank's success rule (strictly larger than Table 7.1 in a non-exact cell; ties fail). The
  checker paths it names are the run's own; the package's checkers are in verify-it-yourself/. Process note: the
  object was written 28.8 min after its own job started and about 30-31 min after the first push job started, so the
  "<= 30 min total" wording was borderline (disclosed to the panel; the criterion skeptic judged it a process note,
  not a criterion stretch).
