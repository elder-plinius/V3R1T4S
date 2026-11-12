# Run it yourself

From this folder, in a fresh shell. Python 3 (standard library only). No network for steps 1 and 2.

1. Check the chain:

       sh verify-it-yourself/run_checks.sh

   Expected output: a line "length 281 = 251 doublings + 30 additions", then `CHECK: PASS`, then `PASS` (also in verify-it-yourself/RECEIPTS.md). check_chain.py checks, with exact integers: N from two independent formulas; N is prime; N-2 equals the hexadecimal in addchain's results.md; every element is the sum of two strictly earlier elements; the last element is N-2; the length and the number of doublings; the length is below the lowest public length 282; x * x^(N-2) = 1 mod N for 100 values of x, with the power computed by following the chain.

2. Rebuild the chain from its dictionary (about a minute):

       python3 how-we-built-it/build_wide.py 2 "1 2 4 8 16 32 64 128 256 257 289 513 1026 2052 2309 4361 8722 17444 34888 69776 70033 139809 279618 559236 699045 699061 699062 1258297 1817533 2097151" rebuilt.txt 3000
       cmp rebuilt.txt object/chain.txt && echo identical

   Expected: "secp256k1 scalar: chain length 281 (doublings 251, additions 30); DP predicted 281; checks PASS", then "identical".

3. Optional, needs network: replay the published 282 chain that sets the bar. Download

       https://additionchains.com/secp256k1-scalar-inverse-example.txt

   (sha256 at our fetches: ff57a8519d4fdc4ee5c154390d30ca83824c14cdfddb1907b9f736c30a050ccf), save it as secp256k1-scalar-inverse-example.txt, then

       python3 verify-it-yourself/check_values.py secp256k1-scalar-inverse-example.txt

   Expected: "values 283, length 282", "all steps valid: True", "ends at target n-2: True".

4. Optional, needs a C compiler, well under 5 minutes: redo the one-edit baseline for the seed dictionary.

       cd how-we-built-it/baseline && cc -O2 -o acw_big acw_big.c && python3 trivial_edits.py 2 22 seed_dictionary.txt 2048 one_edit_again.txt

   Expected histogram line: "282:11 283:183 284:150 285:3 308:1 309:37 310:229 311:49" (nothing below 282).

5. The dictionary search itself: how-we-built-it/COMMANDS.md. It uses a fixed seed and its schedule follows the move count, so the command there retraces the logged run (most of an hour of one core); step 2 is the quick deterministic part.

Run-folder names used in panel/ are mapped in README.md's Path note. Not shipped: the fetched pages and comparator files (table/), the work folders attempts/ and data/.
