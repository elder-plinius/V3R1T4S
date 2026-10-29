# Commands (how the object was built and rebuilt)

Requirements: python3 with numpy 2.5.4 and python-flint 0.9.0 (requirements.txt). Run from this folder.

1. Fetch LITA's published scheme (Khoruzhii, Serafin, Gelss, Pokutta) and check it:

       curl -s -o 15x15x15_r1977.npz https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz
       shasum -a 256 15x15x15_r1977.npz
       # 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33 (git blob sha1 65821484d954b4aade06cbda624932ba2a481f7b)

2. Convert, cut three slices with absorption, export, compare:

       python3 code/convert.py 15x15x15_r1977.npz lita_15.json
       python3 code/rebuild_chain.py lita_15.json rebuilt.json
       python3 code/export_txt.py rebuilt.json rebuilt_txt
       cmp rebuilt_txt/u.txt ../object/u.txt && cmp rebuilt_txt/v.txt ../object/v.txt && cmp rebuilt_txt/w.txt ../object/w.txt && echo identical

   Output on the build machine (2026-10-28, about 35 s):

       parent <15,15,15> rank 1977
       axis 0 e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1: slice -> (14, 15, 15) rank 1865; flat absorption seed 5001 removed 29 -> rank 1836
       axis 2 e=1,0,0,0,0,0,0,0,0,0,0,0,0,0,0 f=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1: slice -> (14, 15, 14) rank 1709; flat absorption seed 1000 removed 0 -> rank 1709
       axis 2 e=0,0,1,0,0,0,0,-1,0,0,0,0,0,0 f=0,0,1,0,0,0,0,0,0,0,1,0,0,0: slice -> (14, 15, 13) rank 1677; flat absorption seed 1008 removed 33 -> rank 1644
       wrote 1644 terms to rebuilt_txt
       identical

What the steps do: `restrict` (code/engine.py) removes one direction from one index: on axis 0 (the row index shared
by A and C) each A factor is mapped through E^T and each C factor through F^T; on axis 2 (the column index shared by B
and C) the B and C factors are mapped on the right. The columns of E span the vectors orthogonal to e, those of F the
vectors orthogonal to f, and E^T F = I, so each step turns a scheme exactly into a scheme for the format with that
dimension one smaller. The three steps and their vectors are fixed in code/rebuild_chain.py:
(1) axis 0, e = (1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1), f = (-1,1,...,1): 1977 -> 1865 terms, absorption (seed 5001) -> 1836,
    <14,15,15>;
(2) axis 2, e = e_0, f = (1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1): -> 1709, <14,15,14>, nothing absorbed (seed 1000);
(3) axis 2, e = e_2 - e_7, f = e_2 + e_10: -> 1677, absorption (seed 1008) -> 1644, <14,15,13>.
`flat_all` (code/flat.py) removes terms by exact linear dependencies among term factors ("absorption"), with a seeded
random order (6 restarts). All arithmetic is exact (python-flint rationals and integer kernels).
