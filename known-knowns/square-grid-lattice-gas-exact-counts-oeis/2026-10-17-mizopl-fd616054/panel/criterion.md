# CRITERION panel verdict — A054759(15), partial win p1

context: subagent (general-purpose)

## Scope reviewed
Only files inside this package were read for data. Scripts I wrote and ran live in a
separate temp dir; `how-we-built-it/sixvertex.py` was copied there and run as first-party code.
The claimed object is a single cell: `object/a054759_15.txt` =
4310182149988584261406143524214457416387448 (one integer, a(15)).

## What p1 requires (literal reading)
p1 says the next unknown term of A054759 under the "same two-run and reproduction
rules". It names exactly two of the main criterion's three rules. It does NOT name
the growth clause ("a(N)^(1/N^2) within 1e-3 of the entropy constant"). My literal,
conservative reading: p1 requires (a) two independent agreeing runs (disjoint
primes AND a different decomposition) and (b) reproduction of every published term
n=1..N-1. It does NOT require the growth clause. This is reinforced by the fact
that even the published a(14) fails the 1e-3 clause, so reading it as required would
make p1 (and the main criterion's published-term consistency) impossible.

## Checks performed and results

1. TWO-RUN rule — PASS.
   - Prime sets disjoint: RUN_A = 11 primes in [2^19,2^20), RUN_B = 12 primes < 2^19;
     `disjoint: True`, intersection empty, all prime (verified).
   - Different decomposition: RUN_A = forward vertex encoding + closed-form min/max
     builder; RUN_B = reversed state encoding (`bits[:, ::-1]`) + explicit
     horizontal-walk builder (`build_sector_matrix_explicit`), a different entry
     code path. The main criterion's own example lists "a different state encoding"
     as a qualifying decomposition change, so this literally qualifies.
   - I independently recomputed BOTH runs from scratch for n=15 (not trusting the
     supplied residues): RUN_A value==claim True (551.9s), RUN_B value==claim True
     (626.4s), A==B True, recomputed value = 4310182149988584261406143524214457416387448.
   - Supplied `object/residues.txt`: both runs CRT (my own routine) to the claimed value
     (RUN_A 220 bits, RUN_B 228 bits); value % prime == residue for all 23 rows.

2. REPRODUCTION rule — PASS.
   - Transfer-matrix method reproduces every published term n=1..14 exactly against
     https://oeis.org/A054759/b054759.txt (sha256 `26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`,
     recorded in `the-record-we-beat/snapshot.md`) (ALL MATCH).
   - Independent cross-check of the definition: brute force over all 2^(2n^2)
     orientations with in-degree-2 constraint gives a(1)=4, a(2)=18, a(3)=148,
     matching the published OEIS b-file. The method models the correct object.

3. GROWTH clause — fails literally, and is NOT part of p1.
   - a(15)^(1/225) = 1.546986940, W=(4/3)^1.5 = 1.539600718, gap 0.007386 > 1e-3.
   - Published a(14)^(1/196) = 1.548086836, gap 0.008486 > 1e-3.
   - Confirmed FAIL at both n=15 and the known a(14); it is an unreachable
     asymptotic note. Not required by p1 (see reading above).

4. Single object — PASS. One cell, a(15); not a bundle of claims.

5. CRT bound — PASS. RUN_A modulus (220 bits) and RUN_B modulus (228 bits) both
   exceed a(15)*2^64 (206 bits); CRT yields the true integer, not a residue.

## Caveat (not fatal)
RUN_B's "different state encoding" is vertex-order reversal — a symmetry rather than
a structurally independent transfer-matrix formulation. It is nonetheless a distinct
state encoding AND pairs with a genuinely different entry-computation code path and a
disjoint prime set, so it meets the criterion's named example literally.

confirmed_scope: A054759(15) = 4310182149988584261406143524214457416387448 is confirmed under p1's two-run rule (two agreeing runs with disjoint prime sets and different decompositions: forward+closed-form vs reversed-encoding+explicit-walk, both independently recomputed) and reproduction rule (method reproduces all published terms n=1..14 exactly, and the Eulerian-orientation definition is confirmed by brute force for n=1..3); the main criterion's 1e-3 growth clause is not met at n=15 (gap 0.0074, and the published a(14) also fails it) and is not part of p1.

pass: true
