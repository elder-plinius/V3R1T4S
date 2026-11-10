# Reproduce skeptic: A054759(16)

context: subagent (Claude Code Agent tool, general-purpose, fresh context)

Claimed value (claim/object/a054759_16.txt, 49 digits):
A054759(16) = 2781781827849835218619790131266486746689884618378

## Definition used (quoted from claim/CLAIM.md)

> number of Eulerian orientations of the n X n square lattice with wrap-around (the n x n torus grid graph,
> 2n^2 edges): orientations of every edge such that every vertex has in-degree 2 and out-degree 2 (square ice rule).

How I formalized it: vertices (r,c), r,c in Z_n; edges V(r,c) = {(r,c),(r+1,c)} and H(r,c) = {(r,c),(r,c+1)}, which
gives 2n^2 distinct edges. For n = 1 these are loops, and for n = 2 they are parallel edges, which matches the
"2n^2 edges" in the definition. Bit V = 1 means down, bit H = 1 means right.
indeg(r,c) = V(r-1,c) + (1 - V(r,c)) + H(r,c-1) + (1 - H(r,c)), and it must equal 2 at every vertex.
The count equals trace(T^n) over the 2^n vertical-edge masks.

## Order of work

1. I read claim/CLAIM.md, claim/table_record/b054759.txt and claim/object/ only, then wrote my own checker
   skeptic_reproduce/mine/ice_mine.rs (Rust) from the definition above. It sweeps vertex by vertex. Its state is
   the vertical mask, the current horizontal edge and the wrap horizontal edge. For each start mask s it computes
   (T^n)[s][s] and sums these over s, either over every s ("full") or over orbit representatives weighted by orbit
   size. The orbits come from column rotations only ("rot"), or from rotations x reflection x global arrow reversal
   ("dihcomp"). These are symmetries of the torus that commute with T.
   Arithmetic is pure addition with five residues at once: mod 2^64 and mod 4 primes.
2. I wrote a separate brute-force enumerator, skeptic_reproduce/mine/brute.py, that runs over all 2^(2n^2)
   orientations with no transfer matrix.
3. I validated against the b-file for n = 1..14 (below). Only after that did I open claim/checker/, then compile
   and rerun the author's program on fresh primes.

## Primes (all chosen by me, all distinct from the author's)

Primality was checked with deterministic Miller-Rabin, bases being the first 13 primes, which is valid below
3.3e24 (skeptic_reproduce/mine/primes.py).
- Set A (own checker, dihcomp): 4611686011427387881 4611686011427387813 4611686011427387741 4611686011427387701
- Set B (own checker, rot): 4611683018427387901 4611683018427387899 4611683018427387893 4611683018427387863
- Set F (author program, fresh): 4611562561638375533 4611562561638375517 4611562561638375457 4611562561638375437
I also re-verified that all 8 of the author's primes in claim/checker/primes.txt are prime.

Rigorous CRT bound: an orientation is determined by the n^2 vertical bits plus one wrap bit per row, so
a(n) <= 2^(n^2+n). At n = 16 that is 2^272. My modulus is 2^64 * (four primes near 2^62), about 2^312, which is
larger than 2^272. So the CRT value is exact, not "assumed small". As an extra check, every 4-of-5 residue subset
reconstructs the same integer.

## Commands (from skeptic_reproduce/mine/)

    python primes.py
    rustc -O -C target-cpu=native ice_mine.rs -o ice_mine.exe
    python brute.py                                   # n = 1..3 direct enumeration
    ice_mine.exe <n> full    6 <set A>                # n = 1..12
    ice_mine.exe <n> dihcomp 6 <set A>                # n = 1..16
    ice_mine.exe <n> rot     6 <set B>                # n = 1..16
    python crt.py ../claim/table_record/b054759.txt <output file>
    rustc -O ../claim/checker/ice.rs -o author_build/ice.exe
    author_build/ice.exe A 16 6 <set F>

Every heavy run used idle priority and affinity mask 0xFC0 (6 logical CPUs), launched through `cmd /c start "" /low
/affinity FC0 /b /wait` or through big.ps1 / auth.ps1 (Start-Process with PriorityClass Idle). The PIDs I started
are in mine/pids.txt: 23988, 20384, 22112, 40164 (own n = 15/16) and the author A-16 run. All of them have exited.

## Results

- Brute force: n = 1, 2, 3 give 4, 18, 148, matching the b-file.
- Own checker, full trace (no symmetry), n = 1..12: all 12 terms match the b-file exactly.
- Own checker dihcomp/set A and rot/set B, n = 1..14: all 28 values match the b-file exactly. This also confirms
  that the symmetry reduction agrees with the unreduced trace for n <= 12.
- n = 15: dihcomp (612 reps, 74.2 s) = rot (2192 reps, 292.3 s) =
  4310182149988584261406143524214457416387448. The mod 2^64 residue is 9426903624262978424 in both runs. This
  equals the author's n = 15 value in claim/run_output/results.jsonl.
- n = 16, dihcomp / set A (1162 reps, 339.8 s): residues
  2^64: 17657967292181610122; 4611686011427387881: 1480833237631958468; 4611686011427387813: 4588802310974101939;
  4611686011427387741: 827744704940030855; 4611686011427387701: 1300902019684665420.
  CRT = 2781781827849835218619790131266486746689884618378.
- n = 16, rot / set B (4116 reps, 1607 s): residues
  2^64: 17657967292181610122; 4611683018427387901: 4284125354537363370; 4611683018427387899: 1699031277144207145;
  4611683018427387893: 3167121360167824472; 4611683018427387863: 1284347001268114881.
  CRT = 2781781827849835218619790131266486746689884618378.
- Both own runs equal the claimed value exactly. The two runs use different prime sets and different symmetry
  reductions, and the mod 2^64 residue is identical across them.
- Author's ice.rs, mode A, n = 16, fresh set F (535.9 s at idle): printed 1404801910391503409, 797680982501685935,
  827355257982839146 and 2374643492899447282. These equal (claimed value) mod each prime, which I computed
  separately in Python.
- Author's saved data: in claim/run_output/results.jsonl every stored residue (modes A and B, n = 1..16) equals
  value mod its prime. A equals B for all n, and n = 1..14 match the b-file.
- claim/table_record/b054759.txt has sha256 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada,
  which matches fetch_records.json. I did not re-fetch it live: I had no network access, and that is not my role.
- Growth: a(16)^(1/256) = 1.5460930823. Lieb W = (4/3)^(3/2) = 1.5396007. The difference is 0.0065. The scaled
  difference (root - W) * n^2 is 1.675, 1.665 and 1.662 at n = 8, 12 and 16, so the gap closes like 1/n^2 as
  expected for the torus. That means the value is consistent with the growth constant. Note that it is not within
  1e-3 at n = 16; that 1e-3 test belongs to the main target criterion, which the gate/criterion skeptic should
  judge.

## What was independently recomputed and what was not

Independently recomputed:
- the full value at n = 15 and 16, twice, by my own code with my own primes and two different symmetry
  decompositions, using a rigorous modulus bound;
- all published terms n = 1..14;
- brute force for n <= 3.

Not independent:
- My sweep uses the same broken-profile idea as the author's (a natural method, written before I read theirs).
  It does not use a different decomposition such as a column sweep or a different state encoding; it differs only
  in the symmetry reduction.
- The rerun of the author's binary on fresh primes checks their code only, not the method.
- The live state of OEIS and of competing pull requests was not checked.

No mismatch, missing object or non-determinism was found.

pass: true
