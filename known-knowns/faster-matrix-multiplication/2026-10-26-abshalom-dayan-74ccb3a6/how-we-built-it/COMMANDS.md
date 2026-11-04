# Commands (how the object was built and rebuilt)

Requirements: python3 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). Run from this folder.

1. Fetch LITA's published scheme (Khoruzhii, Serafin, Gelss, Pokutta) and check it:

       curl -s -o 15x15x15_r1977.npz https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz
       shasum -a 256 15x15x15_r1977.npz
       # 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33 (git blob sha1 65821484d954b4aade06cbda624932ba2a481f7b)

2. Convert, cut one slice, absorb, export:

       python3 code/convert.py 15x15x15_r1977.npz lita_15.json
       python3 code/rebuild_slice.py lita_15.json rebuilt.json 1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 -1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 5001 6
       python3 code/export_txt.py rebuilt.json rebuilt_txt
       cmp rebuilt_txt/u.txt ../object/u.txt && cmp rebuilt_txt/v.txt ../object/v.txt && cmp rebuilt_txt/w.txt ../object/w.txt && echo identical

   Output on the build machine (2026-10-26, about 15 s):

       parent <15,15,15> rank 1977
       slice axis 0 with e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 -> (14, 15, 15) rank 1865
       flat absorption removed 29 -> rank 1836
       wrote 1836 terms to rebuilt_txt
       identical

What the steps do: `restrict` (code/engine.py) fixes the row index shared by A and C to one direction: A's rows are
combined with e, C's rows with f, which turns the <15,15,15> scheme exactly into a <14,15,15> scheme; 112 of the 1977
terms vanish (1865 remain). `flat_all` (code/flat.py) then removes 29 terms by exact linear dependencies among term
factors ("absorption"), with a seeded random order (seed 5001, 6 restarts). All arithmetic is exact (python-flint
rationals and integer kernels).

This is the same cut as step 1 of the chain in pull request #752 (the <14,14,15> rank-1709 claim), whose
how-we-built-it/ used the same code files and named this <14,15,15> rank-1836 intermediate without claiming it.
