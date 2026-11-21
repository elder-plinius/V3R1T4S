# Run it yourself

Fresh shell, from this package folder. Requirements: python3 (standard library only). For the optional rebuild: a C
compiler.

## 1. Verify the object

    sh verify-it-yourself/run_checks.sh

What it does, in order:
1. Computes the sha256 of object/code_n9_d3_k1042.txt. Expected:
   b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a.
2. Runs verify-it-yourself/verify_dna_edit_code_fast.py with n = 9, d = 3 and expected size 1042. This checker was
   written from the definition (Sun's thesis, Sec. 1.5); it has the same definition, the same checks and the same two
   methods as the family checker verify_dna_edit_code.py (used unchanged in the other packages of this family), and
   only computes them faster. It checks that every line is a length-9 word over ACGT, that every word has GC weight
   exactly floor(9/2) = 4, that the 1042 words are distinct, then, exhaustively,
   (A) the exact Levenshtein distance (bit-parallel form of the dynamic program; before use it is compared with the
   plain dynamic program on 20000 random string pairs and must agree on all of them) for all 542361 distinct pairs,
   d(x, y) >= 3, and all 1085764 ordered pairs including x = y, d(x, rc(y)) >= 3, and
   (B) independently, the full sets of strings within edit distance 1 (single insertions, deletions and substitutions,
   any length) of every codeword and of every reverse complement, put in a hash index: no radius-1 ball of a codeword
   may meet the radius-1 ball of another codeword or of any reverse complement (its own included); since edit distance
   is the shortest-path metric of single edits, this is the same as distance >= 3. A and B must report the same
   violations (here none).
   Expected: `method A (bit-parallel DP Levenshtein): 542361 distinct pairs, min d(x,y) = 3; 1085764 ordered pairs
   incl. x=y, min d(x,rc(y)) = 3`, `method B (edit balls of radii 1 and 1, hash index, meet in the middle): 0
   violations; method A: 0 violations`, `VALID: 1042 words, ...` and `PASS`.
3. Six controls, each of which must FAIL:
   - the same object read with d = 4 (its minimum distance is exactly 3), method A only;
   - a copy whose last word is the first word with one A<->T substitution (edit distance 1 to the first word);
   - a copy with a duplicated word;
   - a copy whose last word is the reverse complement of the first word (d(x, rc(y)) = 0);
   - a copy with one word of GC weight 5;
   - the one-word code ACGTACGTA, whose own reverse complement TACGTACGT is at edit distance 2 (the x = y case).
   Each checker call runs once and its output is kept in a temporary folder.

Expected last line: `PASS` (exit code 0). Any mismatch prints `FAIL` (exit code 1). About 1-2 minutes on an idle
machine; see verify-it-yourself/RECEIPTS.md for the time on a loaded shared machine.

By hand:

    python3 verify-it-yourself/verify_dna_edit_code_fast.py object/code_n9_d3_k1042.txt 9 3 --expect-size 1042
    python3 verify-it-yourself/verify_dna_edit_code_fast.py object/code_n9_d3_k1042.txt 9 4 --method-a-only   # must FAIL

Cross-check with the family's plain-DP checker (pure-Python dynamic program on every pair and explicit edit balls
compared pair by pair; several minutes on 1042 words, so it is not part of run_checks.sh; its real output is in
RECEIPTS.md):

    python3 verify-it-yourself/verify_dna_edit_code.py object/code_n9_d3_k1042.txt 9 3 --expect-size 1042

## 2. Rebuild the object (optional)

    gcc -O2 -o dnae how-we-built-it/dnae.c -lm
    mkdir -p out && ./dnae 9 3 2 103 3000 out/p 20000 1042
    # original log: FOUND k=1042 it=8159505 t=612.7 restarts=404
    cmp out/p_n9_d3_G2_k1042.txt object/code_n9_d3_k1042.txt && echo identical

Arguments: n = 9, d = 3, mode G = 2, seed 103, wall-clock cap 3000 s (counted after the precompute), restart length
20000, stop at 1042. Cost on an idle core: about 50-60 CPU-s to precompute the neighbour lists of the 63224 candidate
words, then about 8.2 million tabu iterations (1-3 CPU-min). It writes one file per improvement. The search is
deterministic for a fixed seed (xorshift generator, iteration-based restarts); give the cap generously on a loaded
machine. The REPRODUCE panel and the claim run's own rerun both regenerated a byte-identical file (FOUND k=1042 at the
same iteration 8159505); see how-we-built-it/BUILD.md. The claim does not depend on the rebuild: step 1 checks the
object itself, exhaustively.

## 3. Check the integrity of the package

    sha256sum -c SHA256SUMS
