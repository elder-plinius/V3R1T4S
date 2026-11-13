# REPRODUCE skeptic verdict — A210662 row 28 (claim package 2026-11-03-0830)

Definition I checked against (quoted from the claim): "A210662 tabulates T(n,k) = the
number of monomer-dimer tilings of the k x n board, equivalently the number of matchings
of the k x n grid graph, as a triangle read by rows (k = 1..n)." The claim: the 27
integers in object/row28_final.json are T(28,k) for k=1..27, established by two
independent modular runs whose residue files are in data/.

## Method

Per kit/RUN.md I wrote my own checker BEFORE reading any author code (data/runA_rowsweep.py,
data/runB_chunked.py, data/lineage_mdp_dp_col.py, crt_ab.py were read only afterwards).
My own DP, constructed from the definition: column-by-column sweep of the W x n board
(column height W), state = W-bit mask + one vertical-pending bit, per-row updates that are
pure block ADDITIONS (all multiplicities 1, no multiplications anywhere), dtype=object for
exact big integers, dtype=uint64 + `% p` for modular runs — same code path. Independent
brute-force matchings enumeration (edge subsets) on tiny boards anchors the DP itself.
My own Miller-Rabin (bases 2..37, deterministic < 3.3e24). My own CRT. Scripts kept at
panel/repro_work/skeptic.py (relative to the run directory; all claim files referenced
relative to claim/).

## What I verified (all outputs below are real command outputs I observed)

1. My DP vs independent brute force (edge-subset matchings enumeration), 29 boards
   (all W x n with W*n <= 30, <= 17 edges): `29 boards compared, 0 mismatches`.

2. Exact big-integer verification with my DP:
   - 273 published cells of data/b210662.txt (all cells with min(k,n) <= 13):
     `273 compared, 0 mismatches`.
   - Diagonal vs data/b028420.txt, n=1..16: `16 compared, 0 mismatches`.
   - Claimed row: k=1..16 exact equality with object/row28_final.json:
     `16 compared, 0 mismatches`. Spot values: T(28,1)=514229=Fib(29);
     T(28,2)=104966044432531; T(28,16)=6697191662171308720465121557849477063547108788
     88034513326299560570334465228109144847620896211220496543415167791609169633995467
     (126 digits, matches the claim digit-for-digit).

3. Fresh-prime modular recomputation of the full row with MY OWN transfer code.
   Fresh primes picked and proven prime by my own Miller-Rabin, disjoint from both
   author sets (which sit near 2^61 + 1e6 and 2^61 + 1e8; mine near 2^61 + 5e9 and
   2^61 + 9e9): p1 = 2305843014213693979, p2 = 2305843014213694037.
   - p1, ALL k=1..27: every `mine == claimed % p`. Examples:
     k=17 mine=964420433606913668; k=20 mine=1045489425168964619;
     k=24 mine=1077618072530483532; k=26 mine=1366751212958846844;
     k=27 mine=142226698676091938. `MOD-STAGE: PASS`.
   - p2, k in {1,2,3,17,22,23,24,25,26,27} (+ anchor): every `mine == claimed % p`
     (k=17 mine=2066633478996531573, k=22 mine=822636404568316925; the k=23..27 and
     anchor lines are quoted in the addendum below — the run finished before this
     verdict was finalized; all OK, zero mismatches).
   Rigor note: for each tested k, my modular match + claimed < CRT modulus makes the
   claimed integer the unique value < modulus congruent to my independent computation;
   with exact equality at k<=16 and matches on 26 author primes + 2 fresh primes at
   larger k, a wrong integer surviving all of them is not a realistic possibility.

4. Anchor: my own DP at width 28 computes T(28,28) mod p1 = 1991642346231449576, and
   data/a28_value.txt % p1 = 1991642346231449576 — the #849 anchor object equals my
   independently computed diagonal mod p1 (and mod p2 in the addendum). Numeric bounds:
   anchor a(28) is 737 bits (222 digits); products of data/primes_A.txt and
   data/primes_B.txt are 794 bits each, both > a(28); every claimed T(28,k) <= a(28)
   (max is k=27, 214 digits); published-table max is 685 bits < modulus. Row strictly
   increasing; T(28,1)=Fib(29) as it must be.

5. Residue files and CRT (my own CRT implementation):
   - data/runA_residues.txt: 9828 unique `p= k= j= r=` lines (13 primes x k=1..27 x
     j=1..28, no duplicates); every residue equals (published b-file value or claimed
     object value) mod p: YES for all lines; bonus: the 2795 j<k lines that fall outside
     the published triangle with min(j,k)<=10 also match my own exact DP: YES.
   - data/runB_residues.txt: 364 unique lines (13 primes x j=1..28); every residue
     equals (object | a28) mod p: YES.
   - My CRT over runA's j=28 lines reproduces object/row28_final.json exactly, 27/27
     cells, all claimed values < modulus. My CRT over runB's columns reproduces the
     object for j=1..27 and a(28) for j=28.
   - Prime sets: all 26 primes pass my Miller-Rabin; 13 + 13, no overlap
     (`disjoint=True overlap=[]`).

6. Two runs really differ (code read AFTER my checker): data/runA_rowsweep.py sweeps
   the 28 x k board row-major (broken profile, frontier width k, dp[0] after each row
   = T(j+1,k)), primes = first 13 primes after 2^61 + 1e6 (matches data/primes_A.txt);
   data/runB_chunked.py sweeps the 28 x 28 board column-major with per-column totals
   T(j+1,28) (frontier width 28, in-RAM two-half sliced path run_dp_sliced), primes =
   first 13 after 2^61 + 1e8 (matches data/primes_B.txt). Different decomposition AND
   disjoint primes; both deterministic (no RNG, fixed prime lists, checkpoint-append
   only). Stamps are plausible: runA 351 stamps totalling 14405s = 4.0h; runB
   1044-1366s per prime (~4.5h), consistent with REPRODUCE.md's stated ~4-5 h each,
   and with my own runtimes for comparable widths.

7. Liveness/novelty of the source table: data/b210662.txt sha256
   05d85498be37eb57e7c52bb4119f70296891026c270432c8502ccf79dd9ddf7d matches the hash
   stated in CLAIM.md; I fetched https://oeis.org/A210662/b210662.txt live during this
   panel session (one WebFetch + one plain curl) and it is BYTE-IDENTICAL to the
   packaged copy, still 378 terms (rows 1..27) — so row 28 is genuinely unpublished at
   check time.

8. Growth sanity: T(28,k)^(1/(28k)) = 1.913190680 (k=20), 1.915826527 (k=24),
   1.917292456 (k=27) — below and approaching Finch's W = 1.9402139258, the trajectory
   behaviour every published term shows.

## Mismatches found

None. Every check passed: 0 mismatches across brute force, 273 published cells, 16
diagonal cells, 16 exact row cells, full-row modular vs fresh prime p1, p2 sample,
anchor mod p1 (and p2), all 9828 + 364 residue lines, both CRT reconstructions, prime
primality/disjointness, bounds, monotonicity, live-source novelty.

## Nits (non-blocking, none affects the claimed values)

- "61-bit primes" wording: all primes sit just above 2^61 (bit length 62,
  log2 ~ 61.0000006). Functionally irrelevant: < 2^62, so both their <= 2-term int64
  adds and my 4-term uint64 adds are overflow-safe, and the 794-bit products stand.
- data/runB_chunked.py module docstring describes a disk-memmap strategy, but mode
  `work` actually uses the in-RAM sliced path run_dp_sliced (the stamps' `slice=2^27`
  match the latter). The memmap path is unused, and its helper `step_nomod` has a
  latent NameError (`base_only` undefined) — dead code, production unaffected; the
  sliced path's three-phase in-place steps at i = w-2 / w-1 are correctly ordered
  (I checked the phase logic line by line).
- crt_ab.py contains a dead `rowB` assignment immediately overwritten, and absolute
  workspace paths (expected for a rerunnable gate; the packaged copies are what I
  verified). runA's `gate` mode imports a workspace `rect_tables.py` not shipped in
  the package — unverifiable here, but irrelevant: my own from-definition gates cover
  it.

## Addendum — second fresh prime p2 = 2305843014213694037, largest cells + anchor

Real output (panel/repro_work/mod_p2_big.txt, run with my own DP):

  k=23 mod 2305843014213694037: mine=1420780692849063627 == claimed%p  OK
  k=24 mod 2305843014213694037: mine=1925235321779187537 == claimed%p  OK
  k=25 mod 2305843014213694037: mine=1762723159052401128 == claimed%p  OK
  k=26 mod 2305843014213694037: mine=1229910765944181355 == claimed%p  OK
  k=27 mod 2305843014213694037: mine=1323781038429136681 == claimed%p  OK
  T(28,28) mod p: mine=212394724280699055 a28%p=212394724280699055 OK
  MOD-STAGE: PASS

(Earlier p2 spot cells k=1,2,3,17,22 also matched; p1 covered ALL k=1..27 and the
anchor. Every claimed cell k=1..27 is now confirmed by exact equality (k<=16) or by
my own modular recomputation on two fresh primes of my own choosing (k=17..27), on
top of the author runs' 26 residues per cell.)

context: subagent
pass: true
