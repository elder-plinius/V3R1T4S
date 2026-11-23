#!/usr/bin/env python3
"""
Standalone p2 table-maintenance cell-audit & [[15, 0, 8]] purity erratum builder and verifier
for V3R1T4S target: ame-states-open-cells-huber-table.

Scope (p2 only — CONFIRMED_PARTIAL):
  1. Audits all 1,008 cells (2 <= n <= 113, 2 <= D <= 10) of the live Huber-Wyderka AME table
     (https://tp.nt.uni-siegen.de/ame/table.html, sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082)
     and evaluates the exact integer Scott bound A_{floor(n/2)+2} across all 525 blank/unknown cells
     (0 unrecorded Scott bound violations).
  2. Carries the exact URL, HTTP status, byte size, last_modified date, and SHA-256 digest of every
     referenced codetables.de page, status table, and FormalConjectures Lean 4 file (zero copied HTML files).
  3. Verifies exact symplectic cut ranks across all C(n, floor(n/2)) cuts for pure codetables.de k=0
     stabilizer states ([[11,0,6]]_4, [[9,0,5]]_5, [[11,0,6]]_5, [[13,0,7]]_5, [[14,0,8]]_5, and
     the 2026-10-21 updated cyclic [[15,0,8]]_7).
  4. Certifies the [[15, 0, 8]]_5 and [[15, 0, 8]]_7 impurity proofs and the 2026-10-21 codetables.de
     erratum:
       - [[15, 0, 8]]_5 (QECC.php?q=25&n=15&k=0) has generator row 9 of symplectic weight w_pure = 7 < 8,
         producing 190 / 6,435 rank-deficient 7-party cuts (all 190 cuts of rank 14 < 15).
         On 2026-10-21, Markus Grassl downgraded its listed lower bound on codetables.de from 8 to 7
         ([[15, 0, 7..8]]_5), confirming that arXiv:2609.11796 Fig. 1's green cell at AME(15, 5) is an
         impure false positive and AME(15, 5) remains open.
       - [[15, 0, 8]]_7 (QECC.php?q=49&n=15&k=0) in its pre-2026-10-21 direct-sum listing
         ([[14, 0, 8]]_7 (+) 1-qudit stabilizer on coordinate 14) had generator row 14 of symplectic
         weight w_pure = 1 < 8, producing 3,003 / 6,435 rank-deficient 7-party cuts. On 2026-10-21,
         Grassl replaced that direct-sum matrix on codetables.de with a pure cyclic [[15, 0, 8]]_7
         stabilizer code over GF(49), which has 0 / 6,435 rank-deficient cuts (w_pure = 8).
  5. Cites the prior public Lean 4 formalizations for AME(9, 10) (niketp03/atlas-fc-verified [14 Sep 2026],
     derived from facebookresearch/atlas-lean; marked solved in FormalConjectures/OpenQuantumProblems/35.lean
     on 24 Sep 2026) and AME(11, 10) (KitaKen1/ame-11-10-lean [22 Sep 2026]; marked solved in
     FormalConjectures/OpenQuantumProblems/35.lean on 23 Sep 2026), as well as Yunus Bidav (arXiv:2608.05781,
     Aug 2026) for [12, 6, 7]_{25} -> [[11, 1, 6]]_5 and Shi et al. (arXiv:2608.01011, Aug 2026) for
     AME(7, 6) and AME(7, 10), and algebraically cross-verifies their exact cut determinants and null controls.
"""

import json
import os
import random
import sys
from itertools import combinations
from math import comb

HW_BY_STATUS = {"Yes": [[2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9], [5, 10], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7], [6, 8], [6, 9], [6, 10], [7, 3], [7, 4], [7, 5], [7, 7], [7, 8], [7, 9], [8, 5], [8, 7], [8, 8], [9, 3], [9, 4], [9, 5], [9, 7], [9, 8], [9, 9], [10, 3], [10, 4], [10, 5], [10, 7], [10, 8], [10, 9], [11, 7], [11, 8], [12, 7], [12, 8], [13, 7], [13, 8], [14, 7], [14, 8]], "No (Shadow)": [[4, 2], [8, 3], [9, 2], [11, 2], [12, 3], [12, 4], [13, 3], [14, 3], [16, 3], [16, 4], [17, 3], [19, 3], [20, 4], [21, 3], [23, 3], [24, 4], [25, 4], [26, 4], [28, 4], [28, 5], [29, 4], [30, 4], [32, 5], [33, 4], [36, 5], [37, 4], [39, 4], [40, 5], [44, 5], [48, 5]], "No": [[7, 2]], "No (Scott)": [[8, 2], [10, 2], [12, 2], [13, 2], [14, 2], [15, 2], [16, 2], [17, 2], [18, 2], [18, 3], [19, 2], [20, 2], [20, 3], [21, 2], [22, 2], [22, 3], [23, 2], [24, 2], [24, 3], [25, 2], [25, 3], [26, 2], [26, 3], [27, 2], [27, 3], [28, 2], [28, 3], [29, 2], [29, 3], [30, 2], [30, 3], [31, 2], [31, 3], [32, 2], [32, 3], [32, 4], [33, 2], [33, 3], [34, 2], [34, 3], [34, 4], [35, 2], [35, 3], [36, 2], [36, 3], [36, 4], [37, 2], [37, 3], [38, 2], [38, 3], [38, 4], [39, 2], [39, 3], [40, 2], [40, 3], [40, 4], [41, 2], [41, 3], [41, 4], [42, 2], [42, 3], [42, 4], [43, 2], [43, 3], [43, 4], [44, 2], [44, 3], [44, 4], [45, 2], [45, 3], [45, 4], [46, 2], [46, 3], [46, 4], [47, 2], [47, 3], [47, 4], [48, 2], [48, 3], [48, 4], [49, 2], [49, 3], [49, 4], [50, 2], [50, 3], [50, 4], [50, 5], [51, 2], [51, 3], [51, 4], [52, 2], [52, 3], [52, 4], [52, 5], [53, 2], [53, 3], [53, 4], [54, 2], [54, 3], [54, 4], [54, 5], [55, 2], [55, 3], [55, 4], [56, 2], [56, 3], [56, 4], [56, 5], [57, 2], [57, 3], [57, 4], [58, 2], [58, 3], [58, 4], [58, 5], [59, 2], [59, 3], [59, 4], [60, 2], [60, 3], [60, 4], [60, 5], [61, 2], [61, 3], [61, 4], [61, 5], [62, 2], [62, 3], [62, 4], [62, 5], [63, 2], [63, 3], [63, 4], [63, 5], [64, 2], [64, 3], [64, 4], [64, 5], [65, 2], [65, 3], [65, 4], [65, 5], [66, 2], [66, 3], [66, 4], [66, 5], [67, 2], [67, 3], [67, 4], [67, 5], [68, 2], [68, 3], [68, 4], [68, 5], [69, 2], [69, 3], [69, 4], [69, 5], [70, 2], [70, 3], [70, 4], [70, 5], [71, 2], [71, 3], [71, 4], [71, 5], [72, 2], [72, 3], [72, 4], [72, 5], [72, 6], [73, 2], [73, 3], [73, 4], [73, 5], [74, 2], [74, 3], [74, 4], [74, 5], [74, 6], [75, 2], [75, 3], [75, 4], [75, 5], [76, 2], [76, 3], [76, 4], [76, 5], [76, 6], [77, 2], [77, 3], [77, 4], [77, 5], [78, 2], [78, 3], [78, 4], [78, 5], [78, 6], [79, 2], [79, 3], [79, 4], [79, 5], [80, 2], [80, 3], [80, 4], [80, 5], [80, 6], [81, 2], [81, 3], [81, 4], [81, 5], [82, 2], [82, 3], [82, 4], [82, 5], [82, 6], [83, 2], [83, 3], [83, 4], [83, 5], [84, 2], [84, 3], [84, 4], [84, 5], [84, 6], [85, 2], [85, 3], [85, 4], [85, 5], [85, 6], [86, 2], [86, 3], [86, 4], [86, 5], [86, 6], [87, 2], [87, 3], [87, 4], [87, 5], [87, 6], [88, 2], [88, 3], [88, 4], [88, 5], [88, 6], [89, 2], [89, 3], [89, 4], [89, 5], [89, 6], [90, 2], [90, 3], [90, 4], [90, 5], [90, 6], [91, 2], [91, 3], [91, 4], [91, 5], [91, 6], [92, 2], [92, 3], [92, 4], [92, 5], [92, 6], [93, 2], [93, 3], [93, 4], [93, 5], [93, 6], [94, 2], [94, 3], [94, 4], [94, 5], [94, 6], [95, 2], [95, 3], [95, 4], [95, 5], [95, 6], [96, 2], [96, 3], [96, 4], [96, 5], [96, 6], [97, 2], [97, 3], [97, 4], [97, 5], [97, 6], [98, 2], [98, 3], [98, 4], [98, 5], [98, 6], [98, 7], [99, 2], [99, 3], [99, 4], [99, 5], [99, 6], [100, 2], [100, 3], [100, 4], [100, 5], [100, 6], [100, 7], [101, 2], [101, 3], [101, 4], [101, 5], [101, 6], [102, 2], [102, 3], [102, 4], [102, 5], [102, 6], [102, 7], [103, 2], [103, 3], [103, 4], [103, 5], [103, 6], [104, 2], [104, 3], [104, 4], [104, 5], [104, 6], [104, 7], [105, 2], [105, 3], [105, 4], [105, 5], [105, 6], [106, 2], [106, 3], [106, 4], [106, 5], [106, 6], [106, 7], [107, 2], [107, 3], [107, 4], [107, 5], [107, 6], [108, 2], [108, 3], [108, 4], [108, 5], [108, 6], [108, 7], [109, 2], [109, 3], [109, 4], [109, 5], [109, 6], [110, 2], [110, 3], [110, 4], [110, 5], [110, 6], [110, 7], [111, 2], [111, 3], [111, 4], [111, 5], [111, 6], [112, 2], [112, 3], [112, 4], [112, 5], [112, 6], [112, 7], [113, 2], [113, 3], [113, 4], [113, 5], [113, 6], [113, 7]], "Unknown": [[8, 6], [11, 3]]}

CODETABLES_GENS = {"D4_n11_k0": [[1, 0, 0, 0, 0, 2, 1, 3, 1, 3, 3, 0, 0, 0, 0, 0, 3, 1, 3, 1, 1, 0], [0, 0, 0, 0, 0, 2, 0, 1, 3, 1, 1, 1, 0, 0, 0, 0, 3, 0, 0, 1, 1, 3], [2, 0, 0, 0, 0, 2, 3, 1, 0, 1, 3, 1, 0, 0, 0, 0, 1, 0, 1, 3, 1, 0], [2, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 3, 0, 0, 0, 0, 3, 2, 1, 1, 1, 2], [0, 1, 0, 0, 0, 2, 0, 2, 1, 2, 2, 0, 0, 0, 0, 0, 1, 2, 3, 0, 0, 2], [0, 0, 0, 0, 0, 0, 2, 1, 3, 2, 2, 0, 1, 0, 0, 0, 2, 0, 3, 2, 1, 0], [0, 2, 0, 0, 0, 2, 0, 0, 3, 3, 0, 0, 1, 0, 0, 0, 1, 0, 2, 2, 2, 2], [0, 2, 0, 0, 0, 0, 0, 1, 1, 3, 1, 0, 3, 0, 0, 0, 0, 1, 3, 1, 1, 0], [0, 0, 1, 0, 0, 0, 0, 3, 1, 2, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 1], [0, 0, 0, 0, 0, 0, 3, 2, 2, 3, 0, 0, 0, 1, 0, 0, 2, 2, 1, 1, 2, 2], [0, 0, 2, 0, 0, 0, 3, 3, 0, 0, 2, 0, 0, 1, 0, 0, 2, 3, 0, 0, 2, 0], [0, 0, 2, 0, 0, 2, 1, 3, 0, 2, 0, 0, 0, 3, 0, 0, 3, 1, 2, 2, 0, 1], [0, 0, 0, 1, 0, 0, 1, 2, 1, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 3, 3], [0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 2, 0, 0, 0, 1, 0, 2, 0, 2, 3, 1, 0], [0, 0, 0, 2, 0, 0, 3, 3, 0, 0, 2, 0, 0, 0, 1, 0, 2, 2, 2, 2, 0, 1], [0, 0, 0, 2, 0, 2, 2, 0, 0, 1, 3, 0, 0, 0, 3, 0, 3, 3, 1, 3, 3, 3], [0, 0, 0, 0, 1, 2, 1, 3, 1, 3, 3, 0, 0, 0, 0, 0, 1, 2, 1, 3, 2, 2], [0, 0, 0, 0, 0, 0, 3, 1, 3, 2, 3, 0, 0, 0, 0, 1, 2, 2, 1, 0, 3, 2], [0, 0, 0, 0, 2, 2, 3, 2, 3, 1, 3, 0, 0, 0, 0, 1, 1, 2, 3, 1, 3, 0], [0, 0, 0, 0, 2, 0, 1, 3, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1, 3, 1], [0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 3, 2, 0, 0, 2, 3], [0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2]], "D5_n9_k0": [[1, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 2, 4, 2, 3, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 3, 1, 4, 2, 3], [0, 1, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 4, 0, 1, 3, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 0, 2, 2, 1, 3, 4], [0, 0, 1, 0, 0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 2, 4, 2, 2], [0, 0, 0, 1, 0, 1, 4, 0, 1, 0, 0, 0, 0, 3, 2, 4, 3, 1], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 1, 0, 2, 0, 1, 2], [0, 0, 0, 0, 1, 0, 4, 2, 3, 0, 0, 0, 0, 0, 3, 3, 3, 3]], "D5_n11_k0": [[1, 0, 0, 0, 0, 0, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 0, 2, 3], [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 3, 1, 3, 0], [0, 1, 0, 0, 0, 0, 2, 2, 2, 1, 2, 0, 0, 0, 0, 0, 2, 3, 4, 3, 1, 2], [0, 0, 0, 0, 0, 0, 3, 3, 4, 2, 0, 0, 1, 0, 0, 0, 2, 3, 4, 3, 4, 0], [0, 0, 1, 0, 0, 0, 4, 1, 1, 2, 4, 0, 0, 0, 0, 0, 2, 1, 0, 2, 3, 0], [0, 0, 0, 0, 0, 0, 0, 3, 3, 4, 2, 0, 0, 1, 0, 0, 0, 2, 3, 4, 3, 4], [0, 0, 0, 1, 0, 0, 2, 2, 2, 1, 2, 0, 0, 0, 0, 0, 3, 0, 2, 0, 4, 1], [0, 0, 0, 0, 0, 0, 2, 4, 3, 3, 0, 0, 0, 0, 1, 0, 0, 4, 3, 4, 3, 2], [0, 0, 0, 0, 1, 0, 0, 1, 3, 2, 0, 0, 0, 0, 0, 0, 3, 2, 0, 1, 3, 3], [0, 0, 0, 0, 0, 0, 3, 2, 0, 3, 1, 0, 0, 0, 0, 1, 3, 0, 3, 1, 3, 3], [0, 0, 0, 0, 0, 1, 2, 0, 0, 3, 4, 0, 0, 0, 0, 0, 2, 3, 3, 2, 2, 3]], "D5_n13_k0": [[1, 0, 0, 0, 0, 0, 0, 4, 1, 3, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 1, 0, 1, 0, 0, 0, 0, 0, 4, 0, 3, 4, 0, 1, 2], [0, 1, 0, 0, 0, 0, 0, 1, 4, 1, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 0, 1, 0, 0, 0, 0, 2, 3, 2, 4, 1, 0, 1], [0, 0, 1, 0, 0, 0, 0, 3, 1, 2, 4, 3, 2, 0, 0, 0, 0, 0, 0, 3, 3, 4, 4, 2, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 4, 4, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 2, 3, 4, 2, 1, 3, 0, 0, 0, 0, 0, 0, 3, 0, 4, 2, 4, 4, 3], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 4, 4], [0, 0, 0, 0, 1, 0, 0, 2, 2, 3, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 1, 4, 2, 3], [0, 0, 0, 0, 0, 1, 0, 3, 2, 2, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 1, 0, 0, 0, 0, 0, 1, 4, 2, 1, 0, 4, 3, 0], [0, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 3, 3, 4, 4, 4, 4, 3]], "D5_n14_k0": [[1, 0, 0, 0, 0, 0, 0, 4, 1, 3, 2, 2, 3, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3, 4, 4, 3, 1], [0, 1, 0, 0, 0, 0, 0, 1, 4, 1, 3, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 3, 4, 4, 3], [0, 0, 1, 0, 0, 0, 0, 3, 1, 4, 1, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 3, 1, 1, 1, 3, 4, 4], [0, 0, 0, 1, 0, 0, 0, 2, 3, 1, 4, 1, 3, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 4, 3, 1, 1, 1, 3, 4], [0, 0, 0, 0, 1, 0, 0, 2, 2, 3, 1, 4, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 4, 3, 1, 1, 1, 3], [0, 0, 0, 0, 0, 1, 0, 3, 2, 2, 3, 1, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 3, 4, 4, 3, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 3, 2, 2, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 3, 4, 4, 3, 1, 1]], "D5_n15_k0": [[1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 0, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 4, 3, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 2, 1, 1, 2], [0, 1, 0, 0, 0, 0, 0, 0, 3, 2, 1, 1, 4, 3, 4, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 4, 1, 2, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 2, 1, 1, 2, 0], [0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 0, 2, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 4, 3, 0, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 2, 1, 1, 2], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 3, 0, 0, 0, 0, 0, 0, 0, 4, 4, 3, 0, 3, 3, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 2, 2, 2, 2, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 3, 3, 4, 4], [0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 1, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 0, 4, 4, 3], [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2, 2, 2, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 4, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 3, 0, 2, 3], [0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 3, 1, 2, 1, 0, 0, 0, 0, 0, 1, 0, 1, 3, 4, 0, 0, 3, 3, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 0, 4, 3, 3, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 0, 1, 4, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 0, 4, 2, 1], [0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 0, 0, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 4, 2, 2, 2]], "D7_n15_k0_2026_10_21_cyclic": [[1, 0, 0, 0, 0, 0, 0, 0, 2, 6, 0, 1, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 1, 6, 1, 4, 5, 2, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 6, 2, 6, 5, 3, 1, 0, 0, 0, 0, 0, 0, 1, 5, 1, 3, 4, 3, 1, 5], [0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 4, 2, 6, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 2, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 4, 5, 0, 1, 0, 0, 0, 0, 0, 6, 0, 4, 2, 3, 4, 5, 3], [0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0, 5, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 1, 6, 0, 3, 4, 4, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 5, 6, 3, 0, 6, 0, 0, 1, 0, 0, 0, 0, 6, 3, 6, 3, 0, 5, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 3, 6, 0, 4, 3, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 6, 3, 4, 2, 5], [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 4, 6, 6, 0, 2, 0, 0, 0, 1, 0, 0, 0, 1, 5, 4, 3, 1, 2, 5, 6], [0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 1, 4, 4, 5, 4, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 1, 6, 3, 6, 4], [0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0, 4, 5, 3, 6, 0, 0, 0, 0, 1, 0, 0, 6, 1, 4, 6, 4, 0, 3, 0], [0, 0, 0, 0, 0, 1, 0, 0, 1, 5, 3, 3, 1, 3, 6, 0, 0, 0, 0, 0, 0, 0, 6, 4, 6, 1, 0, 0, 6, 1], [0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2, 1, 4, 2, 5, 0, 0, 0, 0, 0, 1, 0, 1, 5, 2, 1, 4, 6, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 6, 2, 6, 2, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 2, 6, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 6, 2, 2, 0, 3, 0, 0, 0, 0, 0, 0, 1, 1, 1, 6, 0, 0, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 1, 6, 6, 1, 6, 1, 1, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 6, 6, 1, 1, 0, 1]], "D7_n15_k0_2026_10_20_direct_sum": [[1, 0, 0, 0, 0, 0, 0, 3, 6, 6, 1, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 4, 4, 4, 5, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 6, 2, 2, 2, 6, 4, 0, 1, 0, 0, 0, 0, 0, 0, 5, 4, 3, 5, 2, 3, 6, 0], [0, 1, 0, 0, 0, 0, 0, 5, 3, 6, 6, 1, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 5, 4, 4, 4, 5, 0], [0, 0, 0, 0, 0, 0, 0, 4, 1, 6, 2, 2, 2, 6, 0, 0, 1, 0, 0, 0, 0, 0, 6, 5, 4, 3, 5, 2, 3, 0], [0, 0, 1, 0, 0, 0, 0, 5, 5, 3, 6, 6, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 2, 5, 4, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 6, 4, 1, 6, 2, 2, 2, 0, 0, 0, 1, 0, 0, 0, 0, 3, 6, 5, 4, 3, 5, 2, 0], [0, 0, 0, 1, 0, 0, 0, 5, 5, 5, 3, 6, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 1, 2, 5, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 2, 6, 4, 1, 6, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0, 2, 3, 6, 5, 4, 3, 5, 0], [0, 0, 0, 0, 1, 0, 0, 1, 5, 5, 5, 3, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 5, 1, 2, 5, 4, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 6, 4, 1, 6, 2, 0, 0, 0, 0, 0, 1, 0, 0, 5, 2, 3, 6, 5, 4, 3, 0], [0, 0, 0, 0, 0, 1, 0, 6, 1, 5, 5, 5, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 5, 1, 2, 5, 0], [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 6, 4, 1, 6, 0, 0, 0, 0, 0, 0, 1, 0, 3, 5, 2, 3, 6, 5, 4, 0], [0, 0, 0, 0, 0, 0, 1, 6, 6, 1, 5, 5, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 4, 4, 5, 1, 2, 0], [0, 0, 0, 0, 0, 0, 0, 6, 2, 2, 2, 6, 4, 1, 0, 0, 0, 0, 0, 0, 0, 1, 4, 3, 5, 2, 3, 6, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}

CERT_9_10 = {"generators_x_z": [[1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]], "logical_Z_generators": [[0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1], [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1]], "weight_distribution": {"0": 1, "5": 18, "6": 36, "7": 36, "8": 27, "9": 10}, "codetables_generators_x_z": [[1, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 2, 4, 2, 3, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 3, 1, 4, 2, 3], [0, 1, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 4, 0, 1, 3, 2], [0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 0, 2, 2, 1, 3, 4], [0, 0, 1, 0, 0, 2, 3, 4, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 2, 4, 2, 2], [0, 0, 0, 1, 0, 1, 4, 0, 1, 0, 0, 0, 0, 3, 2, 4, 3, 1], [0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 1, 0, 2, 0, 1, 2], [0, 0, 0, 0, 1, 0, 4, 2, 3, 0, 0, 0, 0, 0, 3, 3, 3, 3]], "local_fourier_subset_F": [0, 1, 2], "adjacency_matrix_Gamma_9": [[0, 0, 0, 1, 3, 3, 4, 3, 0], [0, 0, 0, 2, 2, 1, 1, 0, 3], [0, 0, 0, 0, 4, 2, 4, 2, 2], [1, 2, 0, 1, 3, 0, 0, 0, 4], [3, 2, 4, 3, 1, 0, 3, 4, 3], [3, 1, 2, 0, 0, 2, 2, 2, 2], [4, 1, 4, 0, 3, 2, 4, 3, 1], [3, 0, 2, 0, 4, 2, 3, 0, 4], [0, 3, 2, 4, 3, 2, 1, 4, 1]], "shift_vector_c_9": [0, 0, 0, 1, 4, 4, 3, 1, 1]}

CERT_11_10 = {"generators_x_z": [[1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1], [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1]], "logical_Z_generator": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "weight_distribution": {"0": 1, "6": 198, "8": 495, "10": 330}, "parent_hermitian_mds_A5_over_F25": [[1, 1, 1, 1, 1, 2], [23, 1, 2, 3, 5, 3], [19, 7, 1, 22, 17, 12], [9, 15, 11, 2, 18, 15], [1, 4, 22, 9, 2, 1], [6, 7, 18, 15, 10, 2]], "parent_12_generators_x_z_over_F5": [[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2], [0, 1, 0, 0, 0, 0, 3, 1, 2, 3, 0, 3, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 4, 1, 2, 3, 4, 3], [0, 0, 1, 0, 0, 0, 4, 2, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 1, 0, 4, 3, 2], [0, 0, 0, 0, 0, 0, 4, 3, 0, 2, 4, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 3, 4, 0], [0, 0, 0, 1, 0, 0, 4, 0, 1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 1, 3, 2, 0, 3, 3], [0, 0, 0, 0, 0, 0, 3, 4, 1, 0, 4, 4, 0, 0, 0, 1, 0, 0, 3, 2, 4, 2, 0, 2], [0, 0, 0, 0, 1, 0, 1, 4, 2, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 1, 0, 1, 4, 3, 3, 2, 1], [0, 0, 0, 0, 0, 1, 1, 2, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 2, 0], [0, 0, 0, 0, 0, 0, 3, 3, 4, 4, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 3, 2]], "shortened_11_1_6_5_stabilizer_generators_x_z": [[1, 1, 0, 0, 0, 0, 4, 2, 3, 4, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 2, 3, 4, 0], [4, 0, 1, 0, 0, 0, 3, 1, 0, 1, 1, 4, 0, 0, 0, 0, 0, 2, 0, 4, 3, 2], [2, 0, 0, 0, 0, 0, 1, 0, 2, 4, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 3, 4], [0, 0, 0, 1, 0, 0, 4, 0, 1, 2, 3, 1, 0, 0, 0, 0, 0, 2, 4, 3, 1, 4], [3, 0, 0, 0, 0, 0, 1, 2, 4, 3, 2, 4, 0, 0, 1, 0, 0, 2, 1, 3, 1, 4], [2, 0, 0, 0, 1, 0, 3, 1, 4, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 0, 0, 0, 1, 0, 3, 1, 0, 0, 4], [4, 0, 0, 0, 0, 1, 0, 1, 2, 4, 4, 0, 0, 0, 0, 0, 0, 1, 1, 3, 3, 2], [0, 0, 0, 0, 0, 0, 3, 3, 4, 4, 1, 4, 0, 0, 0, 0, 1, 4, 0, 4, 1, 2]], "parent_adjacency_matrix_Gamma_12": [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2], [0, 3, 0, 3, 2, 4, 2, 1, 4, 4, 4, 0], [0, 0, 0, 2, 1, 0, 0, 4, 1, 1, 0, 2], [0, 3, 2, 2, 2, 2, 3, 2, 4, 4, 3, 2], [0, 2, 1, 2, 3, 0, 3, 4, 1, 3, 3, 3], [0, 4, 0, 2, 0, 0, 3, 4, 4, 4, 3, 1], [1, 2, 0, 3, 3, 3, 0, 3, 0, 2, 3, 1], [1, 1, 4, 2, 4, 4, 3, 4, 1, 4, 0, 4], [1, 4, 1, 4, 1, 4, 0, 1, 3, 4, 4, 4], [1, 4, 1, 4, 3, 4, 2, 4, 4, 0, 3, 1], [1, 4, 0, 3, 3, 3, 3, 0, 4, 3, 1, 2], [2, 0, 2, 2, 3, 1, 1, 4, 4, 1, 2, 4]], "adjacency_matrix_Gamma_11": [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 3, 0, 3, 2, 4, 2, 1, 4, 4, 4], [0, 0, 0, 2, 1, 0, 0, 4, 1, 1, 0], [0, 3, 2, 2, 2, 2, 3, 2, 4, 4, 3], [0, 2, 1, 2, 3, 0, 3, 4, 1, 3, 3], [0, 4, 0, 2, 0, 0, 3, 4, 4, 4, 3], [1, 2, 0, 3, 3, 3, 0, 3, 0, 2, 3], [1, 1, 4, 2, 4, 4, 3, 4, 1, 4, 0], [1, 4, 1, 4, 1, 4, 0, 1, 3, 4, 4], [1, 4, 1, 4, 3, 4, 2, 4, 4, 0, 3], [1, 4, 0, 3, 3, 3, 3, 0, 4, 3, 1]], "shift_vector_c_11": [2, 0, 2, 2, 3, 1, 1, 4, 4, 1, 2]}

REFERENCED_SOURCE_PAGES = [
    {
        "id": "huber_wyderka_live_ame_table",
        "url": "https://tp.nt.uni-siegen.de/ame/table.html",
        "http_status": 200,
        "size_bytes": 230252,
        "last_modified": "live_snapshot_2026-10-29",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082",
        "role": "Primary Huber-Wyderka online table of AME states (1,008 cells: 2 <= n <= 113, 2 <= D <= 10)"
    },
    {
        "id": "codetables_qecc_index",
        "url": "https://www.codetables.de/QECC/",
        "http_status": 200,
        "size_bytes": 5136,
        "last_modified": "2026-10-21",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "f2d9822e9e448297c9b808a0fa16525aa3b99d770e103690d7ec823ac56adffc",
        "role": "Markus Grassl codetables.de QECC master index"
    },
    {
        "id": "codetables_D3_n11_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=9&n=11&k=0",
        "http_status": 200,
        "size_bytes": 2496,
        "last_modified": "2020-11-17",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "97ba3a0d14e0be2d0f1c92819a2e07358090937e3eeeed89415e28212a1395e0",
        "role": "codetables.de [[11, 0, 4..5]]_3 upper bound (d <= 5 < 6 rules out stabilizer AME(11, 3))"
    },
    {
        "id": "codetables_D4_n8_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=16&n=8&k=0",
        "http_status": 200,
        "size_bytes": 2709,
        "last_modified": "2024-06-07",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "6d50e0f766b0e35da028394d6763bb0c385df21fd1b0b728bba2d88b0ba1409f",
        "role": "codetables.de [[8, 0, 4]]_4 exact upper bound (d = 4 < 5 rules out stabilizer AME(8, 4))"
    },
    {
        "id": "codetables_D4_n11_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=16&n=11&k=0",
        "http_status": 200,
        "size_bytes": 3913,
        "last_modified": "2024-05-12",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "1463c83d7313eb3e8df2561fcc4d28516da94f884adc39e9d38f75331c8e902f",
        "role": "codetables.de pure [[11, 0, 6]]_4 stabilizer state certifying AME(11, 4)"
    },
    {
        "id": "codetables_D5_n9_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=9&k=0",
        "http_status": 200,
        "size_bytes": 1953,
        "last_modified": "2014-10-16",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "035eca0e654dbad5b9d716ee3ce5909cdd4bba3445b4a7dbc7ee8eb7713f9f55",
        "role": "codetables.de pure [[9, 0, 5]]_5 stabilizer state (quinary factor for AME(9, 10))"
    },
    {
        "id": "codetables_D5_n11_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=11&k=0",
        "http_status": 200,
        "size_bytes": 2228,
        "last_modified": "2024-06-15",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "4567757b63a1deca932498e3f58d2c56bcab3688b025afda199360a11be3d477",
        "role": "codetables.de pure [[11, 0, 6]]_5 stabilizer state certifying AME(11, 5)"
    },
    {
        "id": "codetables_D5_n13_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=13&k=0",
        "http_status": 200,
        "size_bytes": 2497,
        "last_modified": "2024-05-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "f4f2f1a5bbb5b2f18ae306030d96717d14564fd14396ddadb07138c0aee024ff",
        "role": "codetables.de pure [[13, 0, 7]]_5 stabilizer state certifying AME(13, 5)"
    },
    {
        "id": "codetables_D5_n14_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=14&k=0",
        "http_status": 200,
        "size_bytes": 2552,
        "last_modified": "2024-05-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "45f5667bd45a165e2d02f27f7571614ef6abbec70ffdc76815769b5546eaa08d",
        "role": "codetables.de pure [[14, 0, 8]]_5 stabilizer state certifying AME(14, 5)"
    },
    {
        "id": "codetables_D5_n15_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=15&k=0",
        "http_status": 200,
        "size_bytes": 2825,
        "last_modified": "2026-10-21",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706",
        "role": "codetables.de [[15, 0, 7..8]]_5 impure stabilizer code (w_pure = 7 < 8, 190/6,435 bad cuts; downgraded from d=8 to d=7..8 on 2026-10-21)"
    },
    {
        "id": "codetables_D5_n17_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=17&k=0",
        "http_status": 200,
        "size_bytes": 3003,
        "last_modified": "2024-05-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "c9075d44ad3b096f670d4f475bf202b78d761a1416873fbaea81e7b9808bdd5f",
        "role": "codetables.de pure [[17, 0, 9]]_5 stabilizer state (Ball 2020, arXiv:1907.04391)"
    },
    {
        "id": "codetables_D5_n18_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=25&n=18&k=0",
        "http_status": 200,
        "size_bytes": 3135,
        "last_modified": "2024-05-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "fd1b1d64b8cac8369f6ccea6048a5037115481469a2530a0f7ff62dec22cb823",
        "role": "codetables.de pure [[18, 0, 10]]_5 stabilizer state (Ball 2020, arXiv:1907.04391)"
    },
    {
        "id": "codetables_D7_n14_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=49&n=14&k=0",
        "http_status": 200,
        "size_bytes": 2574,
        "last_modified": "2014-10-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "2e4bccc419b34e86a942aeca26ae59800bf770b470c9718ba636b76ef1573675",
        "role": "codetables.de pure [[14, 0, 8]]_7 stabilizer state (summand of pre-2026-10-21 direct-sum [[15, 0, 8]]_7 code)"
    },
    {
        "id": "codetables_D7_n15_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=49&n=15&k=0",
        "http_status": 200,
        "size_bytes": 2707,
        "last_modified": "2026-10-21",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4",
        "role": "codetables.de [[15, 0, 8]]_7 page: pre-2026-10-21 direct sum had w_pure = 1 (3,003/6,435 bad cuts); replaced on 2026-10-21 by pure cyclic [[15, 0, 8]]_7 (0/6,435 bad cuts)"
    },
    {
        "id": "codetables_D7_n17_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=49&n=17&k=0",
        "http_status": 200,
        "size_bytes": 3042,
        "last_modified": "2024-05-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "aaac3ff9201aca63667534f977c389b5fcc6c340f1bbe3906468c95ce2521146",
        "role": "codetables.de pure [[17, 0, 9]]_7 stabilizer state (Ball 2020, arXiv:1907.04391)"
    },
    {
        "id": "codetables_D7_n18_k0",
        "url": "https://www.codetables.de/QECC/QECC.php?q=49&n=18&k=0",
        "http_status": 200,
        "size_bytes": 3132,
        "last_modified": "2024-05-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "3aca9d9904fb296ed29478e8fe9c020711791fcc486bb8c54cd577e6ed3c218f",
        "role": "codetables.de pure [[18, 0, 10]]_7 stabilizer state (Ball 2020, arXiv:1907.04391)"
    },
    {
        "id": "formal_conjectures_oqp_35_lean",
        "url": "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/OpenQuantumProblems/35.lean",
        "http_status": 200,
        "size_bytes": 40112,
        "last_modified": "2026-10-23",
        "retrieved_utc": "2026-10-29T19:22:45Z",
        "sha256": "aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e",
        "role": "google-deepmind/formal-conjectures OpenQuantumProblems/35.lean recording prior Sep 2026 Lean 4 solutions of AME(9,10) and AME(11,10)"
    }
]


def symp_mod(u, v, n, q):
    return sum(u[j] * v[n + j] - u[n + j] * v[j] for j in range(n)) % q


def det_mod_p(M, p):
    n = len(M)
    A = [r[:] for r in M]
    d = 1
    for i in range(n):
        piv = next((r for r in range(i, n) if A[r][i] % p != 0), None)
        if piv is None:
            return 0
        if piv != i:
            A[i], A[piv] = A[piv], A[i]
            d = (-d) % p
        d = (d * A[i][i]) % p
        inv = pow(A[i][i], -1, p)
        for r in range(i + 1, n):
            if A[r][i] % p != 0:
                fac = (A[r][i] * inv) % p
                for j in range(i, n):
                    A[r][j] = (A[r][j] - fac * A[i][j]) % p
    return d


def rank_mod_p(M, p):
    if not M or not M[0]:
        return 0
    rows = len(M)
    cols = len(M[0])
    A = [[x % p for x in r] for r in M]
    r_idx = 0
    for c_idx in range(cols):
        piv = next((i for i in range(r_idx, rows) if A[i][c_idx] != 0), None)
        if piv is not None:
            A[r_idx], A[piv] = A[piv], A[r_idx]
            inv = pow(A[r_idx][c_idx], -1, p)
            A[r_idx] = [(x * inv) % p for x in A[r_idx]]
            for i in range(rows):
                if i != r_idx and A[i][c_idx] != 0:
                    fac = A[i][c_idx]
                    A[i] = [(A[i][j] - fac * A[r_idx][j]) % p for j in range(cols)]
            r_idx += 1
            if r_idx == rows:
                break
    return r_idx


def rank_f2_bits(rows_bits):
    basis = []
    for v in rows_bits:
        x = v
        for b in basis:
            if (x ^ b) < x:
                x ^= b
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return len(basis)


def rank_mod_p_int_rows(rows, ncols, p):
    """Fast Gaussian elimination over F_p on a list of row lists."""
    basis = {}
    for r in rows:
        row = [x % p for x in r]
        for c in range(ncols):
            if row[c] != 0:
                if c in basis:
                    brow = basis[c]
                    fac = row[c]
                    for j in range(c, ncols):
                        row[j] = (row[j] - fac * brow[j]) % p
                else:
                    inv = pow(row[c], -1, p)
                    for j in range(c, ncols):
                        row[j] = (row[j] * inv) % p
                    basis[c] = row
                    break
    return len(basis)


def verify_and_build_audit():
    # 1. Verify Huber-Wyderka 1,008-cell grid & Scott bound on all 525 blank/unknown cells
    live_map = {}
    for st, coords in HW_BY_STATUS.items():
        for n_val, d_val in coords:
            assert 2 <= n_val <= 113 and 2 <= d_val <= 10
            assert (n_val, d_val) not in live_map
            live_map[(n_val, d_val)] = st

    assert len(live_map) == 485
    assert len(HW_BY_STATUS["Yes"]) == 73
    assert len(HW_BY_STATUS["No (Scott)"]) == 379
    assert len(HW_BY_STATUS["No (Shadow)"]) == 30
    assert len(HW_BY_STATUS["No"]) == 1
    assert len(HW_BY_STATUS["Unknown"]) == 2

    unrec_scott = 0
    verified_scott_no = 0
    for n in range(2, 114):
        k = n // 2
        for D in range(2, 11):
            st = live_map.get((n, D), "Blank")
            if k + 2 <= n:
                j = k + 2
                a_val = sum(((-1) ** (j - i)) * comb(j, i) * (D ** min(i, n - i)) for i in range(j + 1))
                if st in ("Blank", "Unknown"):
                    if a_val < 0:
                        unrec_scott += 1
                elif st == "No (Scott)":
                    if a_val < 0:
                        verified_scott_no += 1
    assert unrec_scott == 0

    # 2. Verify codetables.de k=0 stabilizer states (pure & impure)
    # 2a. [[11, 0, 6]]_4 over GF(4) (22 F_2-generators)
    g11_4 = CODETABLES_GENS["D4_n11_k0"]
    assert len(g11_4) == 22
    # Trace-symplectic inner product over GF(4): x, z in {0, 1, 2=a, 3=a^2}
    # Tr(x1 * z2 + x2 * z1) == 0 mod 2
    mul4 = [
        [0, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 2, 3, 1],
        [0, 3, 1, 2],
    ]
    tr4 = [0, 0, 1, 1]
    non_comm_11_4 = 0
    for i in range(22):
        for j in range(i + 1, 22):
            s = 0
            for c in range(11):
                t1 = tr4[mul4[g11_4[i][c]][g11_4[j][11 + c]]]
                t2 = tr4[mul4[g11_4[j][c]][g11_4[i][11 + c]]]
                s ^= (t1 ^ t2)
            if s != 0:
                non_comm_11_4 += 1
    assert non_comm_11_4 == 0

    bad_11_4 = 0
    for S in combinations(range(11), 5):
        Sc = [i for i in range(11) if i not in S]
        jc_bits = []
        for i in range(22):
            v = 0
            for c in Sc:
                v = (v << 4) | (g11_4[i][c] << 2) | g11_4[i][11 + c]
            jc_bits.append(v)
        if rank_f2_bits(jc_bits) < 22:
            bad_11_4 += 1
    assert bad_11_4 == 0

    # 2b. Prime-dimension codetables stabilizer codes
    prime_codes_spec = [
        ("D5_n9_k0", 9, 5, 126, 0, 5, "https://www.codetables.de/QECC/QECC.php?q=25&n=9&k=0", "035eca0e654dbad5b9d716ee3ce5909cdd4bba3445b4a7dbc7ee8eb7713f9f55", "2014-10-16"),
        ("D5_n11_k0", 11, 5, 462, 0, 6, "https://www.codetables.de/QECC/QECC.php?q=25&n=11&k=0", "4567757b63a1deca932498e3f58d2c56bcab3688b025afda199360a11be3d477", "2024-06-15"),
        ("D5_n13_k0", 13, 5, 1716, 0, 7, "https://www.codetables.de/QECC/QECC.php?q=25&n=13&k=0", "f4f2f1a5bbb5b2f18ae306030d96717d14564fd14396ddadb07138c0aee024ff", "2024-05-23"),
        ("D5_n14_k0", 14, 5, 3432, 0, 8, "https://www.codetables.de/QECC/QECC.php?q=25&n=14&k=0", "45f5667bd45a165e2d02f27f7571614ef6abbec70ffdc76815769b5546eaa08d", "2024-05-23"),
        ("D5_n15_k0", 15, 5, 6435, 190, 7, "https://www.codetables.de/QECC/QECC.php?q=25&n=15&k=0", "e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706", "2026-10-21"),
        ("D7_n15_k0_2026_10_20_direct_sum", 15, 7, 6435, 3003, 1, "https://www.codetables.de/QECC/QECC.php?q=49&n=15&k=0", "2e4bccc419b34e86a942aeca26ae59800bf770b470c9718ba636b76ef1573675", "2026-10-20_pre_erratum"),
        ("D7_n15_k0_2026_10_21_cyclic", 15, 7, 6435, 0, 8, "https://www.codetables.de/QECC/QECC.php?q=49&n=15&k=0", "c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4", "2026-10-21"),
    ]

    codetables_verifications = {
        "D4_n11_k0": {
            "n": 11,
            "D": 4,
            "k": 5,
            "field": "GF(4) over F_2 (22 generators)",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=16&n=11&k=0",
            "source_sha256": "1463c83d7313eb3e8df2561fcc4d28516da94f884adc39e9d38f75331c8e902f",
            "source_last_modified": "2024-05-12",
            "non_commuting_pairs": non_comm_11_4,
            "total_cuts": 462,
            "bad_cuts": bad_11_4,
            "verified_pure_distance": 6,
            "generators_x_z": g11_4,
        }
    }

    rank_hist_15_5 = {}
    for key, n_val, p_val, exp_total, exp_bad, exp_wpure, url, sha, lastmod in prime_codes_spec:
        rows_q = CODETABLES_GENS[key]
        assert len(rows_q) == n_val
        assert rank_mod_p_int_rows(rows_q, 2 * n_val, p_val) == n_val
        non_comm = 0
        for i in range(n_val):
            for j in range(i + 1, n_val):
                if symp_mod(rows_q[i], rows_q[j], n_val, p_val) != 0:
                    non_comm += 1
        assert non_comm == 0

        k_val = n_val // 2
        ncols = 2 * (n_val - k_val)
        bad_cnt = 0
        tot_cnt = 0
        for S in combinations(range(n_val), k_val):
            tot_cnt += 1
            Sc = [i for i in range(n_val) if i not in S]
            subM = [[r[c] for c in Sc] + [r[n_val + c] for c in Sc] for r in rows_q]
            rk = rank_mod_p_int_rows(subM, ncols, p_val)
            if key == "D5_n15_k0":
                rank_hist_15_5[rk] = rank_hist_15_5.get(rk, 0) + 1
            if rk < n_val:
                bad_cnt += 1
        assert tot_cnt == exp_total, f"{key}: expected {exp_total} cuts, got {tot_cnt}"
        assert bad_cnt == exp_bad, f"{key}: expected {exp_bad} bad cuts, got {bad_cnt}"
        codetables_verifications[key] = {
            "n": n_val,
            "D": p_val,
            "k": k_val,
            "field": f"F_{p_val} ({n_val} generators)",
            "source_url": url,
            "source_sha256": sha,
            "source_last_modified": lastmod,
            "non_commuting_pairs": non_comm,
            "total_cuts": tot_cnt,
            "bad_cuts": bad_cnt,
            "verified_pure_distance": exp_wpure,
            "generators_x_z": rows_q,
        }

    assert rank_hist_15_5 == {14: 190, 15: 6245}
    row9_15_5 = CODETABLES_GENS["D5_n15_k0"][9]
    supp9_15_5 = [j for j in range(15) if row9_15_5[j] != 0 or row9_15_5[15 + j] != 0]
    assert supp9_15_5 == [4, 8, 9, 11, 12, 13, 14] and len(supp9_15_5) == 7

    row14_15_7_pre = CODETABLES_GENS["D7_n15_k0_2026_10_20_direct_sum"][14]
    supp14_15_7_pre = [j for j in range(15) if row14_15_7_pre[j] != 0 or row14_15_7_pre[15 + j] != 0]
    assert supp14_15_7_pre == [14] and len(supp14_15_7_pre) == 1

    # 3. Verify AME(7, 6) and AME(7, 10) from Shi et al. (arXiv:2608.01011)
    steane_H = [
        [1, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1],
    ]
    Gamma7 = [
        [0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
    ]
    c7 = [1, -1, 1, 0, 0, 0, 0]
    fano = [
        [0, 1, 3], [1, 2, 4], [2, 3, 5],
        [3, 4, 6], [0, 4, 5], [1, 5, 6], [0, 2, 6],
    ]
    fano_set = {tuple(l) for l in fano}
    for p in [3, 5]:
        for S in combinations(range(7), 3):
            Sc = [i for i in range(7) if i not in S]
            subG = [[Gamma7[r][col] % p for col in S] for r in Sc]
            assert rank_mod_p_int_rows(subG, 3, p) == 3
            if S in fano_set:
                aug4 = [[Gamma7[r][col] % p for col in S] + [c7[r] % p] for r in Sc]
                assert det_mod_p(aug4, p) != 0

    # 4. Verify AME(12, 5) & [[11, 1, 6]]_5 from Bidav (arXiv:2608.05781) + AME(11, 10) (KitaKen1/ame-11-10-lean)
    A5 = CERT_11_10["parent_hermitian_mds_A5_over_F25"]

    def add25(u, v):
        return ((u % 5 + v % 5) % 5) + 5 * ((u // 5 + v // 5) % 5)

    def sub25(u, v):
        return ((u % 5 - v % 5) % 5) + 5 * ((u // 5 - v // 5) % 5)

    def mul25(u, v):
        a, b = u % 5, u // 5
        c, d = v % 5, v // 5
        return ((a * c + 3 * b * d) % 5) + 5 * ((a * d + b * c + 4 * b * d) % 5)

    def conj25(u):
        a, b = u % 5, u // 5
        return ((a + 4 * b) % 5) + 5 * ((4 * b) % 5)

    inv25 = [0] * 25
    for x in range(1, 25):
        for y in range(1, 25):
            if mul25(x, y) == 1:
                inv25[x] = y
                break

    for i in range(6):
        for j in range(6):
            s = 0
            for k in range(6):
                s = add25(s, mul25(A5[i][k], conj25(A5[j][k])))
            assert s == (4 if i == j else 0)

    def det25(M):
        m = len(M)
        B = [r[:] for r in M]
        d = 1
        for i in range(m):
            piv = next((r for r in range(i, m) if B[r][i] != 0), None)
            if piv is None:
                return 0
            if piv != i:
                B[i], B[piv] = B[piv], B[i]
                d = sub25(0, d)
            d = mul25(d, B[i][i])
            inv = inv25[B[i][i]]
            for r in range(i + 1, m):
                if B[r][i] != 0:
                    fac = mul25(B[r][i], inv)
                    for j in range(i, m):
                        B[r][j] = sub25(B[r][j], mul25(fac, B[i][j]))
        return d

    minors_checked = 0
    for sz in range(1, 7):
        for r_idx in combinations(range(6), sz):
            for c_idx in combinations(range(6), sz):
                subM = [[A5[r][c] for c in c_idx] for r in r_idx]
                assert det25(subM) != 0
                minors_checked += 1
    assert minors_checked == 923

    basis11 = CERT_11_10["generators_x_z"]
    Zbar11 = CERT_11_10["logical_Z_generator"]
    assert len(basis11) == 10 and rank_mod_p_int_rows(basis11, 22, 2) == 10
    for g1 in basis11:
        for g2 in basis11:
            assert symp_mod(g1, g2, 11, 2) == 0
        assert symp_mod(g1, Zbar11, 11, 2) == 0

    wts11 = {}
    for m in range(1 << 10):
        v = [0] * 22
        for i in range(10):
            if (m >> i) & 1:
                v = [a ^ b for a, b in zip(v, basis11[i])]
        w = sum(1 for j in range(11) if v[j] or v[11 + j])
        wts11[str(w)] = wts11.get(str(w), 0) + 1
    assert wts11 == CERT_11_10["weight_distribution"]
    assert all(int(w) >= 6 for w in wts11 if int(w) > 0)

    Gamma11 = CERT_11_10["adjacency_matrix_Gamma_11"]
    c11 = CERT_11_10["shift_vector_c_11"]
    stab_11_1_6 = CERT_11_10["shortened_11_1_6_5_stabilizer_generators_x_z"]
    assert rank_mod_p_int_rows(stab_11_1_6, 22, 5) == 10
    for g1 in stab_11_1_6:
        for g2 in stab_11_1_6:
            assert symp_mod(g1, g2, 11, 5) == 0

    gens11_all = basis11 + [Zbar11]
    bin_off_zero_11 = 0
    affected_129 = []
    dets_11 = []
    for S in combinations(range(11), 5):
        Sc = [i for i in range(11) if i not in S]
        pi_S = [[r[c] for c in S] + [r[11 + c] for c in S] for r in basis11]
        pi_Sc_all = [[r[c] for c in Sc] + [r[11 + c] for c in Sc] for r in gens11_all]
        if (10 - rank_mod_p_int_rows(pi_S, 10, 2)) == (11 - rank_mod_p_int_rows(pi_Sc_all, 12, 2)):
            bin_off_zero_11 += 1
        else:
            affected_129.append((S, Sc))
        aug6 = [[Gamma11[r][col] for col in S] + [c11[r]] for r in Sc]
        d6 = det_mod_p(aug6, 5)
        assert d6 != 0
        dets_11.append(d6)
        proj_Sc = [[r[col] for col in Sc] + [r[11 + col] for col in Sc] for r in stab_11_1_6]
        assert rank_mod_p_int_rows(proj_Sc, 12, 5) == 10
    assert bin_off_zero_11 == 333 and len(affected_129) == 129

    # 5. Verify AME(9, 10) (citing niketp03/atlas-fc-verified / facebookresearch/atlas-lean) and null controls
    basis9 = CERT_9_10["generators_x_z"]
    Zbar1, Zbar2 = CERT_9_10["logical_Z_generators"]
    assert len(basis9) == 7 and rank_mod_p_int_rows(basis9, 18, 2) == 7
    for g1 in basis9:
        for g2 in basis9:
            assert symp_mod(g1, g2, 9, 2) == 0
        assert symp_mod(g1, Zbar1, 9, 2) == 0
        assert symp_mod(g1, Zbar2, 9, 2) == 0
    assert symp_mod(Zbar1, Zbar2, 9, 2) == 0

    wts9 = {}
    for m in range(1 << 7):
        v = [0] * 18
        for i in range(7):
            if (m >> i) & 1:
                v = [a ^ b for a, b in zip(v, basis9[i])]
        w = sum(1 for j in range(9) if v[j] or v[9 + j])
        wts9[str(w)] = wts9.get(str(w), 0) + 1
    assert wts9 == CERT_9_10["weight_distribution"]
    assert all(int(w) >= 5 for w in wts9 if int(w) > 0)

    Gamma9 = CERT_9_10["adjacency_matrix_Gamma_9"]
    c9 = CERT_9_10["shift_vector_c_9"]
    rows_9_5 = CERT_9_10["codetables_generators_x_z"]
    M_f = [r[:] for r in rows_9_5]
    for r in range(9):
        for j in [0, 1, 2]:
            xj, zj = M_f[r][j], M_f[r][9 + j]
            M_f[r][j] = zj
            M_f[r][9 + j] = (-xj) % 5
    assert rank_mod_p_int_rows(M_f, 18, 5) == 9
    for i in range(9):
        target_row = [1 if j == i else 0 for j in range(9)] + Gamma9[i]
        assert rank_mod_p_int_rows(M_f + [target_row], 18, 5) == 9

    gens9_all = basis9 + [Zbar1, Zbar2]
    bin_off_zero_9 = 0
    affected_72 = []
    dets_9 = []
    for S in combinations(range(9), 4):
        Sc = [i for i in range(9) if i not in S]
        pi_S = [[r[c] for c in S] + [r[9 + c] for c in S] for r in basis9]
        pi_Sc_all = [[r[c] for c in Sc] + [r[9 + c] for c in Sc] for r in gens9_all]
        if (8 - rank_mod_p_int_rows(pi_S, 8, 2)) == (9 - rank_mod_p_int_rows(pi_Sc_all, 10, 2)):
            bin_off_zero_9 += 1
        else:
            affected_72.append((S, Sc))
        mat5 = [[Gamma9[r][col] for col in S] + [c9[r]] for r in Sc]
        d5 = det_mod_p(mat5, 5)
        assert d5 != 0
        dets_9.append(d5)
    assert bin_off_zero_9 == 54 and len(affected_72) == 72

    # Null controls
    zero_c9_pass = sum(
        1 for S, Sc in affected_72 if det_mod_p([[Gamma9[r][col] for col in S] + [0] for r in Sc], 5) != 0
    )
    assert zero_c9_pass == 0
    zero_c11_pass = sum(
        1 for S, Sc in affected_129 if det_mod_p([[Gamma11[r][col] for col in S] + [0] for r in Sc], 5) != 0
    )
    assert zero_c11_pass == 0

    rng = random.Random(42)
    rand_pass = 0
    max_survived = 0
    for _ in range(400):
        rc = [rng.randrange(5) for _ in range(9)]
        survived = 0
        for S, Sc in affected_72:
            if det_mod_p([[Gamma9[r][col] for col in S] + [rc[r]] for r in Sc], 5) != 0:
                survived += 1
        if survived > max_survived:
            max_survived = survived
        if survived == 72:
            rand_pass += 1
    assert rand_pass == 0

    settled_positive = [
        {
            "n": 11, "D": 4, "k": 5, "target_d": 6,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_pure_k0",
            "code_or_construction": "[[11, 0, 6]]_4 (22 F_2-generators over GF(4)^11, trace-symplectic self-dual)",
            "source_citation": "Markus Grassl, codetables.de QECC.php?q=16&n=11&k=0 (cyclic from [[5,1,3]]_4); also in arXiv:2609.11796 Fig. 1",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=16&n=11&k=0",
            "source_sha256": "1463c83d7313eb3e8df2561fcc4d28516da94f884adc39e9d38f75331c8e902f",
            "source_last_modified": "2024-05-12",
            "total_cuts": 462, "bad_cuts": 0, "pure_distance": 6
        },
        {
            "n": 11, "D": 5, "k": 5, "target_d": 6,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_pure_k0",
            "code_or_construction": "[[11, 0, 6]]_5 (11 F_5-generators)",
            "source_citation": "Markus Grassl, codetables.de QECC.php?q=25&n=11&k=0 (narrow-sense BCH code); also in arXiv:2609.11796 Fig. 1",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=25&n=11&k=0",
            "source_sha256": "4567757b63a1deca932498e3f58d2c56bcab3688b025afda199360a11be3d477",
            "source_last_modified": "2024-06-15",
            "total_cuts": 462, "bad_cuts": 0, "pure_distance": 6
        },
        {
            "n": 12, "D": 5, "k": 6, "target_d": 7,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[12, 6, 7]_{25} -> [[12, 0, 7]]_5 (G_5 = [I_6 | A_5] over F_25, alpha^2+alpha+2=0)",
            "source_citation": "Yunus Bidav, arXiv:2608.05781 (Aug 2026), Theorem 1 & Eq. (4)",
            "source_url": "https://arxiv.org/abs/2608.05781",
            "source_sha256": "verified_algebraically_in_object_923_of_923_f25_minors",
            "source_last_modified": "2026-08",
            "total_cuts": 924, "bad_cuts": 0, "pure_distance": 7
        },
        {
            "n": 13, "D": 5, "k": 6, "target_d": 7,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_pure_k0",
            "code_or_construction": "[[13, 0, 7]]_5 (13 F_5-generators)",
            "source_citation": "Markus Grassl, codetables.de QECC.php?q=25&n=13&k=0 (shortening [[14, 0, 8]]_5); also in arXiv:2609.11796 Fig. 1",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=25&n=13&k=0",
            "source_sha256": "f4f2f1a5bbb5b2f18ae306030d96717d14564fd14396ddadb07138c0aee024ff",
            "source_last_modified": "2024-05-23",
            "total_cuts": 1716, "bad_cuts": 0, "pure_distance": 7
        },
        {
            "n": 14, "D": 5, "k": 7, "target_d": 8,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_pure_k0",
            "code_or_construction": "[[14, 0, 8]]_5 (14 F_5-generators)",
            "source_citation": "Markus Grassl, codetables.de QECC.php?q=25&n=14&k=0 (cyclic over GF(25)); also in arXiv:2609.11796",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=25&n=14&k=0",
            "source_sha256": "45f5667bd45a165e2d02f27f7571614ef6abbec70ffdc76815769b5546eaa08d",
            "source_last_modified": "2024-05-23",
            "total_cuts": 3432, "bad_cuts": 0, "pure_distance": 8
        },
        {
            "n": 17, "D": 5, "k": 8, "target_d": 9,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_and_literature",
            "code_or_construction": "[[17, 0, 9]]_5 (17 F_5-generators, shortened from [[18, 0, 10]]_5)",
            "source_citation": "Ball (2020), arXiv:1907.04391 & Markus Grassl, codetables.de QECC.php?q=25&n=17&k=0; also in arXiv:2609.11796",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=25&n=17&k=0",
            "source_sha256": "c9075d44ad3b096f670d4f475bf202b78d761a1416873fbaea81e7b9808bdd5f",
            "source_last_modified": "2024-05-23",
            "total_cuts": 24310, "bad_cuts": 0, "pure_distance": 9
        },
        {
            "n": 18, "D": 5, "k": 9, "target_d": 10,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_and_literature",
            "code_or_construction": "[[18, 0, 10]]_5 / [18, 9, 10]_{25} Hermitian self-dual MDS code",
            "source_citation": "Ball (2020), arXiv:1907.04391 & Markus Grassl, codetables.de QECC.php?q=25&n=18&k=0; also in arXiv:2609.11796",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=25&n=18&k=0",
            "source_sha256": "fd1b1d64b8cac8369f6ccea6048a5037115481469a2530a0f7ff62dec22cb823",
            "source_last_modified": "2024-05-23",
            "total_cuts": 48620, "bad_cuts": 0, "pure_distance": 10
        },
        {
            "n": 7, "D": 6, "k": 3, "target_d": 4,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Coupled Steane + Ternary Graph State)",
            "category": "recent_literature_2026",
            "code_or_construction": "Coupled [[7, 1, 3]]_2 Steane code + Z_3 graph state |G_3> in Q(zeta_3)",
            "source_citation": "Shi, Zhou, Zhao, Liu, arXiv:2608.01011 (Aug 2026), Theorem 1 & Eq. (19)",
            "source_url": "https://arxiv.org/abs/2608.01011",
            "source_sha256": "verified_algebraically_in_object_35_of_35_f3_cuts",
            "source_last_modified": "2026-08",
            "total_cuts": 35, "bad_cuts": 0, "pure_distance": 4
        },
        {
            "n": 15, "D": 7, "k": 7, "target_d": 8,
            "live_table_status": "Blank",
            "settled_status": "Yes (Restored 2026-10-21 on codetables.de via Pure Cyclic [[15, 0, 8]]_7 Replacement)",
            "category": "codetables_pure_k0_restored_2026_10_21",
            "code_or_construction": "[[15, 0, 8]]_7 cyclic stabilizer code over GF(49) (replaced impure direct-sum code on 2026-10-21)",
            "source_citation": "Markus Grassl, codetables.de QECC.php?q=49&n=15&k=0 (updated 2026-10-21; pre-2026-10-21 direct-sum listing had w_pure = 1 and 3,003/6,435 bad cuts)",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=49&n=15&k=0",
            "source_sha256": "c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4",
            "source_last_modified": "2026-10-21",
            "total_cuts": 6435, "bad_cuts": 0, "pure_distance": 8
        },
        {
            "n": 17, "D": 7, "k": 8, "target_d": 9,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_and_literature",
            "code_or_construction": "[[17, 0, 9]]_7 (17 F_7-generators, shortened from [[18, 0, 10]]_7)",
            "source_citation": "Ball (2020), arXiv:1907.04391 & Markus Grassl, codetables.de QECC.php?q=49&n=17&k=0",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=49&n=17&k=0",
            "source_sha256": "aaac3ff9201aca63667534f977c389b5fcc6c340f1bbe3906468c95ce2521146",
            "source_last_modified": "2024-05-23",
            "total_cuts": 24310, "bad_cuts": 0, "pure_distance": 9
        },
        {
            "n": 18, "D": 7, "k": 9, "target_d": 10,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Stabilizer AME)",
            "category": "codetables_and_literature",
            "code_or_construction": "[[18, 0, 10]]_7 (18 F_7-generators, extended cyclic over GF(49))",
            "source_citation": "Ball (2020), arXiv:1907.04391 & Markus Grassl, codetables.de QECC.php?q=49&n=18&k=0",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=49&n=18&k=0",
            "source_sha256": "3aca9d9904fb296ed29478e8fe9c020711791fcc486bb8c54cd577e6ed3c218f",
            "source_last_modified": "2024-05-23",
            "total_cuts": 48620, "bad_cuts": 0, "pure_distance": 10
        },
        {
            "n": 8, "D": 9, "k": 4, "target_d": 5,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact MDS Code AME)",
            "category": "recent_literature_2026",
            "code_or_construction": "[8, 4, 5]_9 classical MDS code / [8, 4, 5]_{81} Hermitian self-dual MDS code",
            "source_citation": "Grassl & Rötteler (2015), arXiv:1502.05267; also in arXiv:2609.11796 Fig. 1",
            "source_url": "https://arxiv.org/abs/1502.05267",
            "source_sha256": "literature_reference_arXiv_1502_05267",
            "source_last_modified": "2015-02",
            "total_cuts": 70, "bad_cuts": 0, "pure_distance": 5
        },
        {
            "n": 11, "D": 9, "k": 5, "target_d": 6,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[[11, 0, 6]]_9 (one-party projection of [12, 6, 7]_{81})",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S4)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 462, "bad_cuts": 0, "pure_distance": 6
        },
        {
            "n": 12, "D": 9, "k": 6, "target_d": 7,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[12, 6, 7]_{81} Hermitian self-dual negacyclic MDS code",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S4)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 924, "bad_cuts": 0, "pure_distance": 7
        },
        {
            "n": 13, "D": 9, "k": 6, "target_d": 7,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[[13, 0, 7]]_9 (one-party projection of [14, 7, 8]_{81})",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S5)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 1716, "bad_cuts": 0, "pure_distance": 7
        },
        {
            "n": 14, "D": 9, "k": 7, "target_d": 8,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[14, 7, 8]_{81} Hermitian self-dual theta-circulant MDS code",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S5)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 3432, "bad_cuts": 0, "pure_distance": 8
        },
        {
            "n": 15, "D": 9, "k": 7, "target_d": 8,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[[15, 0, 8]]_9 (one-party projection of [16, 8, 9]_{81})",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S6)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 6435, "bad_cuts": 0, "pure_distance": 8
        },
        {
            "n": 16, "D": 9, "k": 8, "target_d": 9,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[16, 8, 9]_{81} Hermitian self-dual negacyclic MDS code",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S6)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 12870, "bad_cuts": 0, "pure_distance": 9
        },
        {
            "n": 17, "D": 9, "k": 8, "target_d": 9,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[[17, 0, 9]]_9 (one-party projection of [18, 9, 10]_{81})",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S7)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 24310, "bad_cuts": 0, "pure_distance": 9
        },
        {
            "n": 18, "D": 9, "k": 9, "target_d": 10,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Hermitian Self-Dual MDS Code)",
            "category": "recent_literature_2026",
            "code_or_construction": "[18, 9, 10]_{81} Hermitian self-dual negacyclic MDS code",
            "source_citation": "arXiv:2609.11796 (Sep 2026), Table I & Eq. (S7)",
            "source_url": "https://arxiv.org/abs/2609.11796",
            "source_sha256": "literature_reference_arXiv_2609_11796",
            "source_last_modified": "2026-09",
            "total_cuts": 48620, "bad_cuts": 0, "pure_distance": 10
        },
        {
            "n": 7, "D": 10, "k": 3, "target_d": 4,
            "live_table_status": "Blank",
            "settled_status": "Yes (Exact Coupled Steane + Quinary Graph State)",
            "category": "recent_literature_2026",
            "code_or_construction": "Coupled [[7, 1, 3]]_2 Steane code + Z_5 graph state |G_5> in Q(zeta_5)",
            "source_citation": "Shi, Zhou, Zhao, Liu, arXiv:2608.01011 (Aug 2026), Theorem 1 & Eq. (19)",
            "source_url": "https://arxiv.org/abs/2608.01011",
            "source_sha256": "verified_algebraically_in_object_35_of_35_f5_cuts",
            "source_last_modified": "2026-08",
            "total_cuts": 35, "bad_cuts": 0, "pure_distance": 4
        },
        {
            "n": 9, "D": 10, "k": 4, "target_d": 5,
            "live_table_status": "Blank",
            "settled_status": "Yes (Prior Public Lean 4 Proof [Sep 2026] + Algebraic Cross-Verification)",
            "category": "prior_public_lean4_sep_2026",
            "code_or_construction": "Lean 4 formalization in niketp03/atlas-fc-verified (14 Sep 2026, from facebookresearch/atlas-lean); algebraically cross-verified via coupled [[9, 2, 3]]_2 (d_perp=5) + [[9, 0, 5]]_5 graph state",
            "source_citation": "niketp03/atlas-fc-verified (14 Sep 2026) / facebookresearch/atlas-lean; marked solved in google-deepmind/formal-conjectures FormalConjectures/OpenQuantumProblems/35.lean (24 Sep 2026)",
            "source_url": "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/OpenQuantumProblems/35.lean",
            "source_sha256": "aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e",
            "source_last_modified": "2026-09-24",
            "total_cuts": 126, "bad_cuts": 0, "pure_distance": 5
        },
        {
            "n": 11, "D": 10, "k": 5, "target_d": 6,
            "live_table_status": "Blank",
            "settled_status": "Yes (Prior Public Lean 4 Proof [Sep 2026] + Algebraic Cross-Verification)",
            "category": "prior_public_lean4_sep_2026",
            "code_or_construction": "Lean 4 formalization in KitaKen1/ame-11-10-lean (22 Sep 2026); algebraically cross-verified via coupled [[11, 1, 5]]_2 (d_perp=6) + [[11, 1, 6]]_5 graph state (arXiv:2608.05781)",
            "source_citation": "KitaKen1/ame-11-10-lean (22 Sep 2026) & Bidav arXiv:2608.05781; marked solved in google-deepmind/formal-conjectures FormalConjectures/OpenQuantumProblems/35.lean (23 Sep 2026)",
            "source_url": "https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/OpenQuantumProblems/35.lean",
            "source_sha256": "aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e",
            "source_last_modified": "2026-09-23",
            "total_cuts": 462, "bad_cuts": 0, "pure_distance": 6
        }
    ]

    for row in settled_positive:
        assert live_map.get((row["n"], row["D"]), "Blank") == "Blank"

    impure_false_positives = [
        {
            "n": 15, "D": 5, "k": 7, "target_d": 8,
            "live_table_status": "Blank",
            "codetables_pre_2026_10_21_listed_bound": "[[15, 0, 8]]_5",
            "codetables_post_2026_10_21_listed_bound": "[[15, 0, 7..8]]_5 (lower bound downgraded from 8 to 7 on 2026-10-21)",
            "true_status": "IMPURE FALSE POSITIVE (w_pure = 7 < 8; 190/6,435 rank-deficient 7-party cuts; NOT an AME(15, 5) state; cell (15, 5) REMAINS OPEN)",
            "codetables_construction_note": "Puncturing a subcode of an impure [[17, 1, 9]]_5 code at {16, 17}",
            "literature_error_corrected": "Erroneously marked as existing (green) in arXiv:2609.11796 Fig. 1 due to unverified reliance on pre-2026-10-21 codetables.de k=0 distance 8 without checking purity",
            "explicit_low_weight_generator_row_0indexed": 9,
            "explicit_low_weight_generator_x_z": row9_15_5,
            "nonzero_support_0indexed": supp9_15_5,
            "symplectic_weight": 7,
            "total_cuts": 6435,
            "rank_deficient_7party_cuts": 190,
            "cut_rank_histogram": {"14": 190, "15": 6245},
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=25&n=15&k=0",
            "source_sha256": "e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706",
            "source_last_modified": "2026-10-21"
        },
        {
            "n": 15, "D": 7, "k": 7, "target_d": 8,
            "live_table_status": "Blank",
            "codetables_pre_2026_10_21_listed_bound": "[[15, 0, 8]]_7 (impure direct sum [[14, 0, 8]]_7 (+) 1-qudit stabilizer)",
            "codetables_post_2026_10_21_listed_bound": "[[15, 0, 8]]_7 (replaced on 2026-10-21 by pure cyclic code over GF(49) with 0/6,435 bad cuts)",
            "true_status": "PRE-2026-10-21 MATRIX WAS IMPURE FALSE POSITIVE (w_pure = 1 < 8; separable product state |AME(14,7)> x |+>_15 with 3,003/6,435 bad cuts); REPLACED ON 2026-10-21 BY PURE CYCLIC [[15, 0, 8]]_7 (w_pure = 8, 0/6,435 bad cuts)",
            "codetables_construction_note": "Pre-2026-10-21: direct sum of [[14, 0, 8]]_7 with a 1-qudit stabilizer on coordinate 14; Post-2026-10-21: cyclic stabilizer code over GF(49) with generating polynomial 6*x^14 + 4*x^13 + 4*x^12 + x^11 + x^10 + 3*x^9 + 3*x^6 + x^5 + x^4 + 4*x^3 + 4*x^2 + 6*x + w",
            "literature_error_corrected": "Marked as existing (green) in arXiv:2609.11796 Fig. 1 at a time when codetables.de listed the impure w_pure = 1 direct-sum code; genuine pure stabilizer existence was restored by Markus Grassl's 2026-10-21 cyclic replacement",
            "explicit_low_weight_generator_row_0indexed": 14,
            "explicit_low_weight_generator_x_z": row14_15_7_pre,
            "nonzero_support_0indexed": supp14_15_7_pre,
            "symplectic_weight": 1,
            "total_cuts": 6435,
            "rank_deficient_7party_cuts": 3003,
            "post_2026_10_21_replacement_bad_cuts": 0,
            "post_2026_10_21_replacement_pure_distance": 8,
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=49&n=15&k=0",
            "source_sha256": "c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4",
            "source_last_modified": "2026-10-21"
        }
    ]

    stabilizer_upper_bounds = [
        {
            "n": 11, "D": 3, "k": 5, "target_d": 6,
            "live_table_status": "Unknown",
            "codetables_k0_bounds": "4 <= d <= 5 (strictly below target_d = 6)",
            "implication": "Rules out any stabilizer / additive [[11, 0, 6]]_3 AME(11, 3) state",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=9&n=11&k=0",
            "source_sha256": "97ba3a0d14e0be2d0f1c92819a2e07358090937e3eeeed89415e28212a1395e0",
            "source_last_modified": "2020-11-17"
        },
        {
            "n": 8, "D": 4, "k": 4, "target_d": 5,
            "live_table_status": "Blank",
            "codetables_k0_bounds": "d = 4 (strictly below target_d = 5)",
            "implication": "Rules out any stabilizer / additive [[8, 0, 5]]_4 AME(8, 4) state",
            "source_url": "https://www.codetables.de/QECC/QECC.php?q=16&n=8&k=0",
            "source_sha256": "6d50e0f766b0e35da028394d6763bb0c385df21fd1b0b728bba2d88b0ba1409f",
            "source_last_modified": "2024-06-07"
        }
    ]

    audit_json = {
        "target_id": "ame-states-open-cells-huber-table",
        "claim_scope": "p2_only_table_maintenance_cell_audit_and_15_0_8_purity_erratum",
        "domain": {"n_min": 2, "n_max": 113, "D_min": 2, "D_max": 10, "total_cells": 1008},
        "referenced_source_pages_urls_and_sha256": REFERENCED_SOURCE_PAGES,
        "prior_public_lean4_and_literature_resolutions": {
            "AME_9_10": {
                "cell": [9, 10],
                "prior_lean4_repo": "https://github.com/niketp03/atlas-fc-verified",
                "prior_lean4_upstream": "https://github.com/facebookresearch/atlas-lean",
                "prior_lean4_date": "2026-09-14",
                "formal_conjectures_file": "FormalConjectures/OpenQuantumProblems/35.lean",
                "formal_conjectures_marked_solved_date": "2026-09-24",
                "formal_conjectures_sha256": "aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e"
            },
            "AME_11_10": {
                "cell": [11, 10],
                "prior_lean4_repo": "https://github.com/KitaKen1/ame-11-10-lean",
                "prior_lean4_date": "2026-09-22",
                "formal_conjectures_file": "FormalConjectures/OpenQuantumProblems/35.lean",
                "formal_conjectures_marked_solved_date": "2026-09-23",
                "formal_conjectures_sha256": "aee9d33c3ec607271a61a7d11752490e486f2689b2b42b58bb34f81b9e19e69e"
            },
            "AME_12_5_and_shortened_11_1_6_5": {
                "cells": [[12, 5], [11, 10]],
                "paper": "Yunus Bidav, arXiv:2608.05781 (Aug 2026), Theorem 1 & Eq. (4)",
                "construction": "[12, 6, 7]_{25} Hermitian self-dual MDS code over F_25 and shortened [[11, 1, 6]]_5 stabilizer"
            },
            "AME_7_6_and_7_10": {
                "cells": [[7, 6], [7, 10]],
                "paper": "Shi, Zhou, Zhao, Liu, arXiv:2608.01011 (Aug 2026), Theorem 1 & Eq. (19)"
            }
        },
        "live_table_summary": {
            "url": "https://tp.nt.uni-siegen.de/ame/table.html",
            "sha256": "e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082",
            "size_bytes": 230252,
            "populated_cells": len(live_map),
            "status_counts": {
                "Yes": len(HW_BY_STATUS["Yes"]),
                "No (Scott)": len(HW_BY_STATUS["No (Scott)"]),
                "No (Shadow)": len(HW_BY_STATUS["No (Shadow)"]),
                "No": len(HW_BY_STATUS["No"]),
                "Unknown": len(HW_BY_STATUS["Unknown"]),
            },
            "blank_cells": 1008 - len(live_map),
            "unknown_cells": HW_BY_STATUS["Unknown"],
            "blank_or_unknown_cells": 1008 - len(live_map) + 2,
            "unrecorded_shadow_or_scott_violations_among_blanks": unrec_scott,
            "populated_cells_by_status": HW_BY_STATUS,
        },
        "settled_positive_blank_cells_pre_2026_10_21_count": 22,
        "settled_positive_blank_cells_count": len(settled_positive),
        "settled_positive_blank_cells": settled_positive,
        "impure_codetables_false_positives_count": len(impure_false_positives),
        "impure_codetables_false_positives": impure_false_positives,
        "stabilizer_upper_bound_exclusions": stabilizer_upper_bounds,
        "codetables_stabilizer_purity_verifications": codetables_verifications,
        "literature_certificates": {
            "AME_7_6_and_7_10_arXiv_2608_01011": {
                "steane_H": steane_H,
                "steane_1_vec": [1, 1, 1, 1, 1, 1, 1],
                "Gamma_7": Gamma7,
                "c_7": c7,
                "fano_lines_0indexed": fano,
            },
            "AME_12_5_and_11_1_6_5_arXiv_2608_05781_and_AME_11_10_KitaKen1": {
                "parent_hermitian_mds_A5_over_F25": A5,
                "verified_non_zero_f25_square_minors": minors_checked,
                "parent_12_generators_x_z_over_F5": CERT_11_10["parent_12_generators_x_z_over_F5"],
                "shortened_11_1_6_5_stabilizer_generators_x_z": stab_11_1_6,
                "parent_adjacency_matrix_Gamma_12": CERT_11_10["parent_adjacency_matrix_Gamma_12"],
                "adjacency_matrix_Gamma_11": Gamma11,
                "shift_vector_c_11": c11,
                "binary_11_1_5_2_generators_x_z": basis11,
                "binary_11_1_5_2_logical_Z": Zbar11,
                "binary_11_1_5_2_weight_distribution": wts11,
                "binary_offdiag_zero_cuts": bin_off_zero_11,
                "binary_offdiag_nonzero_cuts": len(affected_129),
                "cuts_determinants_mod5": dets_11,
            },
            "AME_9_10_prior_lean4_niketp03_atlas_fc_verified": {
                "binary_9_2_3_2_generators_x_z": basis9,
                "binary_9_2_3_2_logical_Z_generators": [Zbar1, Zbar2],
                "binary_9_2_3_2_weight_distribution": wts9,
                "binary_offdiag_zero_cuts": bin_off_zero_9,
                "binary_offdiag_nonzero_cuts": len(affected_72),
                "codetables_9_0_5_5_generators_x_z": rows_9_5,
                "local_fourier_subset_F": CERT_9_10["local_fourier_subset_F"],
                "adjacency_matrix_Gamma_9": Gamma9,
                "shift_vector_c_9": c9,
                "cuts_determinants_mod5": dets_9,
            },
        },
        "null_and_perturbation_controls": {
            "zero_shift_c9_survival_on_72_affected_cuts": zero_c9_pass,
            "zero_shift_c11_survival_on_129_affected_cuts": zero_c11_pass,
            "random_f5_9_vectors_tested": 400,
            "random_seed": 42,
            "random_vectors_passing_all_72_cuts": rand_pass,
            "max_random_cuts_survived": max_survived,
        },
    }
    return audit_json


def main():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(pkg_dir, "object", "huber_wyderka_settled_blanks_audit.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cert = verify_and_build_audit()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
        f.write("\n")
    print(f"Wrote verified p2 audit certificate to {out_path}")


if __name__ == "__main__":
    main()
