# Run it yourself

Fresh shell, from this package folder. Requirements: python3 (standard library only); optionally a C compiler `cc`.

## 1. Verify the object

    sh verify-it-yourself/run_checks.sh

What it does, in order:
1. Computes the sha256 of object/net_F2_t11_m24_s17.txt. Expected:
   c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618.
2. Checks that object/net_F2_t11_m24_s17_first13rows.txt equals rows 1..13 of each block of the full file.
3. Runs verify-it-yourself/check_net.py at t = 11. This checker was written from the definition for this package. It
   checks every composition of 13 into 17 parts. Expected:
   `b=2 m=24 s=17 t=11 k=13 compositions_checked=67863915 expected=67863915: all 67863915 compositions ... have rank 13`
   followed by `PASS`. 67863915 = C(29,16).
4. Runs two controls, both of which must FAIL:
   - The same object at t = 10. A rank-deficient composition is reported, e.g. (0,0,0,0,0,0,0,0,0,0,2,1,1,7,0,3,0).
   - A copy with row 1 of C_17 replaced by row 1 of C_16.
5. If `cc` exists, compiles verify-it-yourself/netcheck_b.c (a second, separately written checker in C) and runs it.
   Expected: `PASS q=2 m=24 s=17 t=11 k=13 compositions_reached=67863915`.

Expected last line: `PASS` (exit code 0). Any mismatch prints `FAIL` (exit code 1).

You can also run the checkers by hand:

    python3 verify-it-yourself/check_net.py object/net_F2_t11_m24_s17.txt 24 17 11
    cc -O2 -o netcheck_b verify-it-yourself/netcheck_b.c && ./netcheck_b object/net_F2_t11_m24_s17.txt 2 24 17 11

Arguments: FILE m s t (check_net.py), FILE q m s t (netcheck_b).

## 2. Rebuild the object

    cc -O2 -o gvgreedy2 how-we-built-it/gvgreedy2.c
    ./gvgreedy2 24 17 11 101 > first13.txt
    python3 how-we-built-it/pad_full.py first13.txt full.txt 24 17
    cmp full.txt object/net_F2_t11_m24_s17.txt && echo identical

Takes about 20 s. The output is byte-identical to the object (see how-we-built-it/BUILD.md).

## 3. Check the integrity of the package

    sha256sum -c SHA256SUMS
