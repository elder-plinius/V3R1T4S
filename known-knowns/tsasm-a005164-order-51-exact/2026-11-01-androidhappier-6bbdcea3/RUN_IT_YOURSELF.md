# Run it yourself

Open a fresh shell in this folder (the one holding README.md) and run:

    sh verify-it-yourself/run_checks.sh

Needs: python3 (3.8 or newer, standard library only). No network, no compiler. About 1-3 minutes on one core
(63 s on the run machine for the DP; under 1 s for the brute force).

Expected output: the sha256 of object/A005164_25.txt matches; the brute-force fixtures print True / True False /
False; brute force prints a(0..8) = 1,1,1,2,4,13,46,248,1516; the DP prints n and a(n) for n = 0..25, ending with
`25 30533896243799704017627552102998416`; then

    DP == brute force for n=0..8: True
    DP == published a(0..24): True
    object == DP a(25): True
    PASS

The full real output is in verify-it-yourself/RECEIPTS.md.

What the checkers are:
- verify-it-yourself/tsasm_height_dp.py: an exact count of a(n) from the definition, via the height-function
  bijection for ASMs. The two generating symmetries of D4 (transpose and row reversal) reduce a TSASM of order
  2n+1 to a height function on the triangle 0 <= i <= j <= n with forced boundary values. The derivation is in the
  file's docstring. This reduction differs from the one the two search programs use.
- verify-it-yourself/tsasm_brute.py: brute force straight from the ASM definition with a full D4 test, with three
  fixtures (a known order-5 TSASM, an ASM that is not totally symmetric, a symmetric non-ASM).

## Rebuild the object (the two programs that found it)

The commands are in how-we-built-it/BUILD.md (gcc with OpenMP and python3; Program B at n = 25 needs about 1 GiB of RAM;
under 2 minutes on 8 cores). Its expected line is `n=25 value=30533896243799704017627552102998416 ... check=OK`
in both CRT outputs, and `ALL_AGREE over n=0..26` from compare.py. To write the object file from that value:

    printf '25 30533896243799704017627552102998416\n' > object/A005164_25.txt
