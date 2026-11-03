# How the object was built (search provenance; the commands are those the run used, with paths shortened)

Tools (code/):
- lsearch_wave1.c: exact subset-DP count of the full domain of a never-condition assignment, the lexicographic enumerator (`enum`) and pair-LNS (`lns`).
- lsx.c: extends lsearch_wave1.c with:
  - `dlns`: sequenced pair-LNS, then triple-of-alternatives LNS;
  - `restrict`: delete one alternative and count exactly;
  - `restrict2`;
  - `extend`: clone an alternative and complete the mixed triples by exact branch and bound;
  - `rr`.
- Drivers: multistart.py, topdown.py, dchain.py, vcycle.py. Utilities: write_list.py, write_assign_txt.py, txt2npy.py, gather.py, offer.py, verify_all.py.
- Assignment encoding in .npy files: colex triple index C(c,3)+C(b,2)+a (0-based, a<b<c), value 3*(i-1)+(j-1) for "iNj".

Build: `cc -O3 -o lsx code/lsx.c -lm` (and the same for lsearch_wave1.c).

Provenance of the n = 21 assignment (object/n21_assignment.txt). Each step was a time-limited search, so a rerun may end elsewhere.
1. The record paper's n = 8 maximum (never conditions from arXiv:2303.15002, Table 2) was extended one alternative at a time by the paper's inductive step, with exact branch and bound on the mixed triples. This rebuilt the paper's Table 4 domains exactly for n = 9..17 (292015 at n = 17).
2. Pair-LNS (`lsearch lns`) lifted n = 17 to 297146.
3. The chain (clone step plus exact completion plus pair-LNS polish) ran up to n = 25.
4. The polished n = 24 (81305714) was restricted to n = 23, then to n = 22 (16403698). `lsx dlns` gave 16533994.
5. That n = 22 assignment was restricted to 21 alternatives by deleting alternative 11 (0-based), giving 7457770.
6. One `lsx dlns` pass (pair 8, 9) gave 7467760.
7. `lsx enum 21 <assignment.npy>` writes the list in lexicographic order. The list was compressed with `xz -9e` and split with `split -b 1000000`.

The frozen rule of the claiming run folder is PREREG.md.
