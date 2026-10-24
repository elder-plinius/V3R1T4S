# Verification Receipts (`2026-10-18-mizopl-537faa12`)

## 1. Standalone Python Verifier (`verify-it-yourself/run_checks.sh`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Real command output:
```text
w12_k4_improved.gm sha256  : 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4 (136 bytes)
published_w12_k4.gm sha256 : 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131 (136 bytes)
Improved order (16 uint64s): [15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]
Published order (16 uint64s): [6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]

--- Exact Expected DNA Density (over all 4^16 = 4,294,967,296 DNA windows) ---
Published w12_k4.gm (prob_gc_dna)        : 584312429 / 2^32 = 0.1360458389
Improved  w12_k4_improved.gm (prob_gc_dna): 573933439 / 2^32 = 0.1336292920
Improved  w12_k4_improved.gm (4-ary DP)   : 573933439 / 2^32 = 0.1336292920

--- Comparison vs All Published Methods at (w=12, k=4) ---
  GreedyMini          : 0.136046000  (our order improves by -1.7764%)
  angle-based         : 0.138322748  (our order improves by -3.3931%)
  decycling           : 0.143956000  (our order improves by -7.1735%)
  double decycling    : 0.145236000  (our order improves by -7.9916%)
  miniception         : 0.156164000  (our order improves by -14.4302%)
  mod-minimizer       : 0.156164000  (our order improves by -14.4302%)
  open-close-syncmer  : 0.156164000  (our order improves by -14.4302%)
Smallest published value: 0.1360458389 (GreedyMini)
Our exact DNA density   : 0.1336292920
Relative reduction      : -1.776274% (required >= 0.500000%)

--- Empirical Check (10-minimizers random_density_function_dna_includes_tiebreaking, N=1,000,000, seed=0) ---
  Published w12_k4.gm     : 0.136117
  Improved w12_k4_improved: 0.133727 (-1.7558%)

VERIFICATION: PASS
PASS
```

## 2. Verbatim `GreedyMini` C++ `prob_gc_dna` Verifier (`verify-it-yourself/verify_greedymini_dna.cpp`)

Command:
```bash
./verify_greedymini_dna 12 4 the-record-we-beat/published_w12_k4.gm object/w12_k4_improved.gm
```

Real command output:
```text
the-record-we-beat/published_w12_k4.gm -> prob_gc_dna = 584312429 / 2^32 | density_expected_dna = 0.1360458389
object/w12_k4_improved.gm -> prob_gc_dna = 573933439 / 2^32 | density_expected_dna = 0.1336292920
```
