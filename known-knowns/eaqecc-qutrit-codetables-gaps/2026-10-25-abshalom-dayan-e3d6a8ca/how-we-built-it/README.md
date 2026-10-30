# How we built it

Commands from this folder (python3 standard library and cc), in the order the object was found. Coordinates of the
head: the 27 affine points of the Hermitian curve y^3 + y = x^4 over GF(9), then P_inf; GF(9) elements are coded
a + 3b.

1. The degree-4 places of the curve (arithmetic in GF(6561)) and their orbits under the 216 automorphisms fixing
   P_inf together with the Frobenius:

       python3 deg4.py orbits     # orbits4.txt: 1512 places in 4 orbits, representatives 0, 18, 36, 54

2. The Construction X pairs C1 = C_L(D_28, aQ + (16 - 4a)P_inf) > C2 = C_L(D_28, (a - 1)Q + (16 - 4a)P_inf) for the
   four representatives and a = 1..6, with exact minimum distances by Brouwer-Zimmermann over GF(9) (gen_pairs4.sh
   ran this from a folder with code/, data/ and out/ subfolders; gen_pairs4.txt is its output). For the pair used:

       python3 deg4.py pair 0 2 8 X.xin     # byte-identical to X16d4_q0_a2.xin here; C1 = L(2Q + 8P) [28,14], C2 = L(Q + 8P) [28,10]
       cc -O3 -o bz9 bz9.c
       python3 deg4.py code 0 2 8 C1.code && ./bz9 < C1.code     # d = 12
       python3 deg4.py code 0 1 8 C2.code && ./bz9 < C2.code     # d = 16

   Every one of the 24 pairs is exactly [28,14,12] > [28,10,16], so every X code with a [7,4,4] tail is
   [35,14,16]_9 by the Construction X bound min(16, 12 + 4).

3. The exact maximum Hermitian hull of every Construction X code of a pair (all 2^27 head sign patterns, every
   [7,4] Reed-Solomon tail on the projective line and every 4 x 4 gluing matrix, plus an upper bound for any tail
   code; minimal-rank-completion bound, made exact by the rank classification of Hermitian forms; run_bound4.sh ran
   all 24 pairs, about 1.5 CPU-minutes each):

       cc -O3 -o hullbound4 hullbound4.c && ./hullbound4 bound 7 7 < X16d4_q0_a2.xin    # bound4_X16d4_q0_a2.txt

   Exact maximum 7 (Reed-Solomon tails and any tail), reached at exactly one head pattern:
   +---++---+--+++-+----++-+--+. Over the 24 pairs: a = 2 and a = 6 reach 7 in all four orbits, a = 1 and a = 5 at
   most 6 with any tail, a = 3 and a = 4 at most 6 with Reed-Solomon tails; no pair reaches 8.

4. A tail and gluing matrix that reach hull 7 at that pattern (random Reed-Solomon tails):

       ./hullbound4 real 7 +---++---+--+++-+----++-+--+ SEED_LINE < X16d4_q0_a2.xin    # real4_X16d4_q0_a2.txt

   REAL_NOTE

   Points 8, 0, 4, 6, 3, 7, 5; tail signs -+--++- (columns 29, 31, 32 and 35, counting from 1, multiplied by w);
   M = 6,8,4,5,7,4,0,1,5,1,7,2,0,1,8,3 (row-major).

5. The object (the X code, its Hermitian dual and S = phi(dual) over GF(3)):

       python3 build_x4.py 0 2 8 8,0,4,6,3,7,5 6,8,4,5,7,4,0,1,5,1,7,2,0,1,8,3 '+---++---+--+++-+----++-+--+-+--++-' out.json 16
       shasum -a 256 out.json ../object/eaqecc_35_7_16_14.json    # both e3d6a8cad3db3a6ea28262ced2969b03a429b1ede488ae9cd59b69f5055b73b4

   It prints `X code [35,14] hull=7 -> [[35,7,?;14]]  S 42x70  D9 21x35`. The object's "construction" string says
   that rows 10..13 (0-based) of G9 carry M A; C2 has dimension 10, so that is right.

- `PREREG.md`: the frozen plan of the run folder that produced this claim, written before any of
  its checkers ran on the object. No null test: an explicit object checked by deterministic exact checkers against a
  table value.
