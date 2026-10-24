# Commands (all were run as 1-CPU batch jobs; Python 3 standard library, gcc)

1. Exterior automaton, base 13, periods 1-10, every overflow signature:
       gcc -O2 -o ext2 ext2.c && for p in 1 2 3 4 5 6 7 8 9 10; do ./ext2 13 $p 2000000; done
   (the base-13 self-loop appears at p=10, o=1010010000)
2. Print exterior paths for that signature:
       gcc -O2 -o extpath2 extpath2.c && ./extpath2 13 10 2000000 1010010000
   The phase-shifted exterior specs used next are in specs2.txt (one line per phase: b p a L[a] R[a] lb rb).
3. Seeded interior search (N = 12 bulk digits per side, all interiors up to the cap, 300 steps):
       gcc -O2 -o seeded seeded.c && ./seeded specs2.txt 12 300 300000
   The object is spec line index 36 (0-based) with the empty interior.
4. Template extraction and exact checks (needs rle_check.py from verify-it-yourself/ next to it):
       python3 extract.py specs2.txt 36 . 12 400 b13
PREREG.md is the run's frozen pre-registration (null_test: not needed, explicit object with an exact checker).
