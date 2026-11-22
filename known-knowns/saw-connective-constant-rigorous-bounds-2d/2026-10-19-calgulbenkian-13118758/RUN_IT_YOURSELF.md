# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only; the fork start method, so Linux or macOS; no network). Needs about 8 GB of memory in the coordinating process (7.6 GB peak measured) and under 1 GB in each of 3 worker processes, about 150 MB of temporary disk, and about 35 to 45 minutes on an Apple-silicon Mac (a slower or busy machine may need much longer; a driver that enforces a timeout should allow at least 3000 s, and 5400 s on a slow machine):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The steps it runs:

1. Check every file under object/ against SHA256SUMS (stops with FAIL on any mismatch).
2. Concatenate object/vector_part_00.bin to vector_part_14.bin and check the sha256 of the whole (13118758b86bc0f0daef592d3e85d353851556e54dcd07ad93b6a1c52fc26e54), then of each part against object/SHA256_PARTS.txt.
3. Two negative controls on the first 3000 states (a vector entry set to 1; a vector entry set to 0); both must be rejected.
4. The full check, which can also be run alone on a reassembled file (use a folder of your own for the temporary file):

```sh
mkdir -p work && cat object/vector_part_*.bin > work/vector.xz
python3 -I verify-it-yourself/check_saw482_k34.py work/vector.xz 34 --workers 3
```

Expected output of the full check ends with (RECEIPTS.md has a complete run):

```
states found 16873086, moves kept 26331184, pruned by test 1 2507806, by test 2 1217699, multi-candidate moves 9458099, ...
pocket tests: monotone-ray proofs 50783383, full searches 6822189, full searches that hit the 4096 cap 0
ok   vector length 16873086 against the rebuilt state count 16873086
ok   no full pocket search hit the 4096 cap, so every pocket decision is exact (cap hits: 0)
ok   every rebuilt state is in canonical form (non-canonical: 0)
ok   ordered subset-inclusion invariant holds for every candidate target examined (failures: 0)
second-pass candidates present in the state set (all enter the minimum): 0; of these, strictly lowering the running minimum: 0
exact max (P x)_i / x_i = 710041141248 / 388946198528 = 169287/92732 = 1.825551050339  (state index 6930368)
ok   bound 169287/92732 < 1.82926 - 2e-6 (exact rational comparison)
ok   loop length K = 34 and 16,873,086 states, as claimed (K = 34, N = 16873086)
ok   bound equals the claimed 169287/92732 exactly (got 169287/92732)
PASS
```

(The comparison line uses the rounded 1.82926 minus 2e-6; the stricter bar used in README.md is Alm's published 1.829254, which the bound also beats: 1.825551050339 < 1.829254.)

## How the object was built

The object is the rounded integer test vector (16-bit mantissa, exponent) for the automaton of loop length 34 with finite-pocket pruning, produced from the contributor's generator, how-we-built-it/saw_bounds_2d.c, run as saw_bounds_2d 482 34 cert_482_k34.txt 2 (command and provenance in how-we-built-it/README.md). The vector file format and the definition of the automaton, the state order and the pocket tests are in object/AUTOMATON.md; the proof that the pruned matrix bounds mu is object/THEOREM.md. The checker needs only the binary parts.
