# Commands (how the object was built and rebuilt)

Requirements: python3 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). Run from this folder.

1. Fetch LITA's published scheme (Khoruzhii, Serafin, Gelss, Pokutta) and check it:

       curl -s -o 13x13x13_r1379.npz https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/13x13x13_r1379.npz
       shasum -a 256 13x13x13_r1379.npz
       # 9df0b464793e3c9584c9e95e48dc748a4774afa07bd1b7aa7e6d4421570b40eb (git blob sha1 bc0840bbda26c63915d242360fcc56a7c0e4047b)

2. Convert, cut one slice, absorb, export:

       python3 code/convert.py 13x13x13_r1379.npz lita_13.json
       python3 code/rebuild_12x13x13.py lita_13.json rebuilt.json 1,1,1,1,1,1,-4,1,1,1,1,1,1 -1,1,1,1,1,1,1,1,1,1,1,1,1 5001 6
       python3 code/export_txt.py rebuilt.json rebuilt_txt
       cmp rebuilt_txt/u.txt ../object/u.txt && cmp rebuilt_txt/v.txt ../object/v.txt && cmp rebuilt_txt/w.txt ../object/w.txt && echo identical

   Output on the build machine (2026-10-27, about 7 s):

       parent <13,13,13> rank 1379
       slice axis 0 with e=1,1,1,1,1,1,-4,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1 -> (12, 13, 13) rank 1295
       flat absorption removed 25 -> rank 1270
       wrote 1270 terms to rebuilt_txt
       identical

What the steps do: `restrict` (code/engine.py) removes one direction from the row index shared by A and C: each A
factor is mapped through E^T and each C factor through F^T (columns of E span the vectors orthogonal to e, columns of F
those orthogonal to f, E^T F = I), which turns the <13,13,13> scheme exactly into a <12,13,13> scheme; 84 of the 1379
terms vanish (1295 remain). `flat_all` (code/flat.py) then removes 25 terms by exact linear dependencies among term
factors ("absorption"), with a seeded random order (seed 5001, 6 restarts). All arithmetic is exact (python-flint
rationals and integer kernels).
