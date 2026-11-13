# REPRODUCE panel verdict — FULL claim: a(28) of OEIS A028420

context: zcode Agent-tool subagent, fresh context

Judged only from the claim package and the preserved run folders it names. Before reading
the author's DP code I wrote my own counters from the definition; every number below was
re-derived by my own code, then the author's code was executed by me where the claim
relies on it.

## What I implemented (definition quoted, then my methods)

Definition, quoted from CLAIM.md: "the number of matchings of the 28 x 28 grid graph
(monomer-dimer tilings; the Hosoya index)" — for general n, sets of pairwise-disjoint
dominoes on the n x n board (grid-graph edges no two sharing a vertex; cells may stay
empty).

1. Own edge-subset brute force (every subset of the 2n(n-1) grid edges, keep pairwise
   vertex-disjoint ones): n=2, n=3.
2. Own DFS-over-edges brute force with conflict pruning (explicit enumeration of every
   matching): n=4, n=5.
3. Own row-by-row transfer DP, exact big integers (state = mask of columns occupied by
   verticals from the row above; DFS placement per row -> (outmask, ways); n transfers):
   n = 0..11.
4. Same transfer of mine mod primes: n = 12..15.
5. Own deterministic Miller-Rabin (bases 2..37), own CRT, own sha256, own growth fits.
Author code run by me: the claim folder's standalone verifier (as shipped and with its
in-code n<=9 cap lifted in a copy), and BOTH runs' sweep codes (exact gate n=0..20 and
modular spots), from copies so no preserved folder was modified.

## Independently computed values

- Brute force: a(2)=7, a(3)=131 (edge-subset), a(4)=10012, a(5)=2810694 (DFS) — all four
  duty anchors confirmed against the packaged b-file.
- My transfer DP, exact: n=0..11 all equal the packaged b-file (a(11)=17438298232401644
  94694386437970640 among them); modular: n=12..15 equal the b-file mod 1000000007 (and
  mod 998244353 for 12, 13). 0 mismatches.
- Author's verify_standalone.py (2 s, well under the 3-minute cap): prints n=0..9 OK,
  last line PASS; with the cap lifted to n=11 in a copy it also reproduces a(10), a(11).
- CRT (mine): the 21 distinct (prime, residue) pairs of runB_residues_raw.txt over
  primesB.txt reconstruct EXACTLY the value in a28_value.txt AND the value inside
  runA_crt_output.txt (the 222-digit integer). Run A's own 21 residues (its run folder's
  residue files, primes = its primes21.txt) CRT to the same integer. Combined 42-prime
  CRT also equals it. Raw-residue file: 23 lines, exactly 21 distinct primes, the 2
  recomputed duplicates (primes ...4917, ...4963) identical, zero conflicts, every
  residue < its prime.
- Primality: all 21 Run A primes and all 21 Run B primes pass my deterministic
  Miller-Rabin. Prime overlap between the runs: 0 (Run A max ...4791 < Run B min ...4837;
  set intersection empty).
- Gates: Run A's preserved exact gate output ends "GATE PASS (n=0..20)"; I re-ran Run A's
  row-sweep gate myself in full: GATE PASS (n=0..20). Run B's column-sweep exact gate is
  NOT preserved as an output file (only asserted in its attempt NOTES); I ran it myself
  in full: GATE PASS (n=0..20). Preserved spot gates (n=21..27, 2 primes per run per
  term): Run A's shows the 14 residue values and PASS; Run B's shows 14 boolean-True
  comparisons and PASS.
- Spot recomputes by me (Run B column code, one fresh proven prime
  2305843009213695563, disjoint from both runs): a(20) mod p = 1881477638761186672 =
  b-file a(20) mod p. Also n=21 mod runA_q1 via Run A's code = 2165480176849721653 =
  the preserved spot-gate value = b-file reduction; n=21 mod runB_q1 via Run B's code =
  603297351862002321 = b-file reduction; n=27 mod runB_q1 via Run B's code =
  1156797182408159717 = b-file reduction (far end of the spot gate).
- Arithmetic: anchor bound 3^784 has exactly 1243 bits and a(28) (737 bits, 222 digits)
  is far below it; BOTH modulus products are 1282 bits — each exceeds the 1243-bit
  bound, so each run's CRT uniquely pins the value. a(28)^(1/784) = 1.9177114986 as
  claimed; two-point W + c/n^2 fit through the published n=26,27 roots predicts
  1.9176813 for n=28 vs measured 1.9177115, |dev| = 3.02e-5 (claim: 3.0e-5); raw
  deviation from the ~1.9402 literature constant is 2.25e-2 (claim says 2.3e-2 —
  accurately disclosed as the finite-size effect); published roots climb 1.9139363
  (n=24) -> 1.9168732 (n=27) and a(28)'s 1.9177115 continues the curve smoothly;
  a(28)//a(27) = 4914909436853280 exactly as recorded in Run A's skeptic output.
- Hashes/objects: a28_value.txt sha256 matches CLAIM.md; the packaged b-file is 2060
  bytes, rows n=0..27 only (a(28) absent), sha256 matches table_record.md, and is
  byte-identical across all six copies in the claim and run folders; the value in
  a28_value.txt equals both runs' saved value files and the two-run CRT output.

## Mismatches / errata found (none affect the claimed value)

1. "1302 bits" for Run B's CRT modulus (stated twice in CLAIM.md) is wrong: the product
   of primesB.txt's 21 primes is 1282 bits — my computation and the author's own two-run
   CRT output line agree on 1282. No impact: 1282 > 1243-bit anchor bound either way.
2. Run B's exact n=0..20 gate output is not preserved in its run folder (only noted in
   its attempt NOTES); CLAIM.md's "outputs in both run folders" overstates this one
   artifact. I closed the gap by running that gate myself: PASS.
3. verify_standalone.py ships with an in-code cap at n=9 while CLAIM.md says it
   reproduces "n = 0..11"; REPRODUCE.md discloses the 0..9 cap. With the cap lifted the
   code does reproduce n=10, n=11 (I ran it). Wording nit only.
4. Cosmetic, disclosed by the artifacts themselves: the preserved two-run CRT output ends
   in a traceback (a Windows escape bug writing the value file AFTER printing "EXACT
   MATCH with Run A: True"; the value file exists and matches my CRT); first spot-gate
   attempts in both run folders are OOM-crashed partials superseded by the *2.txt
   complete outputs; Run A's saved exact-gate output keeps only the n=19, n=20 tail plus
   the PASS summary line.

## Notes for the chair (verified facts, judgment left to the panel)

- The full exact CRT gate for n = 21..27 was not computed; coverage there is the 2-prime
  modular spot gate per run (4 primes per term, 28/28 True). This deviation is disclosed
  in the claim. My independent recomputes sampled n=21 (both codes) and n=27 (Run B
  code) and all match; those are spot checks, not exhaustive.
- The growth criterion arm "a(N)^(1/N^2) within 1e-3 of the entropy constant" is not met
  on the raw reading (2.25e-2 from ~1.9402); the claim discloses both readings and the
  trajectory reading agrees to 3.0e-5. The numbers are exactly as claimed.

Everything I could recompute — four brute-force anchors, the full published table
through n=15 by my own transfer DP, both runs' exact n=0..20 gates executed by me,
modular spots at n=20 (fresh prime), n=21 (both codes) and n=27, both 21-prime CRTs, all
primality, all hashes, bit-lengths and growth arithmetic — reproduces exactly, with the
three errata above being wording/record-keeping slips that do not touch the value.

pass: true
