# Claim v3 (partial win p1 of bank target mertens-smallest-counterexample-upper-bound)

**One sentence.** For all 19 best-y rows that Kim-Nguyen print in arXiv:2502.21021v1 (Table 1: 5 rows of h_P;
Table 2: 14 rows of h_StR, exactly the 5 lines of Test-Pinch.txt and the 14 lines of Test-ST.txt in their Zenodo
record 10775723), we give certified ball-arithmetic values of h at the exact published y, computed from
separately computed zeta zeros (complete lists: 14,950 zeros with gamma < 14000, 98,625 with gamma < 74000);
the p1 deliverable is these 19 certified values to 3 decimals, together with the full balls.

target id: mertens-smallest-counterexample-upper-bound
partial win claimed: p1 (scope: the 19 certified values of arXiv v1 Tables 1-2, to 3 decimals, plus the full
balls; nothing else)

## p1 (verbatim from bank/targets.json)
An independent certified re-evaluation of Kim-Nguyen's best y values (Tables 1-2) for h_P and h_StR, confirming or
correcting their reported values to 3 decimals.

## Definitions used (from Kim-Nguyen arXiv:2502.21021, (2.6), (2.7), Theorem 2.1)
alpha = |rho zeta'(rho)|^{-1}, psi = arg(rho zeta'(rho)) for each zero rho = 1/2 + i gamma, gamma > 0.
h_P(y)   = 2 sum_{gamma < 14000} alpha exp(-1.5e-6 gamma^2) cos(gamma y - psi)
h_StR(y) = 2 sum_{gamma < 74000} alpha exp(-3e-9 gamma^2) cos(gamma y - psi)
Kim-Nguyen: "For practical values of y, |h_StR(y)| > 1 + 6e-8 implies that x < exp(y + sqrt(y))."

## Comparison conventions
The paper does not use a single display convention. It mixes rounding (half away from zero) and truncation
(toward zero), including in its own y+sqrt(y) column (see the second table of check/compare_printed.md:
y+sqrt(y) is rounded at Table 1 row 4 and Table 2 rows 2, 10, 12, 13, and truncated at Table 2 rows 7, 9, 14).
Each printed h value is therefore compared with the certified ball under both conventions, at the printed number
of decimals. MATCH means every point of the ball maps to the printed value; MISMATCH means none does (no row is
ambiguous under either convention). The two 3-decimal columns answer p1's "to 3 decimals" without choosing a
convention. The full balls are the convention-free object.

## All 19 rows (check/compare_printed.py on result/p1_certified_values.json; printed values parsed from
## inputs/kn_arxiv_v1_tables_excerpt.txt, the pdftotext of the arXiv v1 PDF, sha256 3141e044...5818f54)
| table | row | y (exact, as published) | printed | certified (7 dp) | at printed dp (round / trunc) | certified (3 dp, round / trunc) | |diff| | rounding | truncation |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 821801872381554552551865.064536 | 0.991 | 0.9911735 | 0.991 / 0.991 | 0.991 / 0.991 | 1.7e-04 | MATCH | MATCH |
| 1 | 2 | 1217019235269548564510534.246242 | -0.993 | -0.9930659 | -0.993 / -0.993 | -0.993 / -0.993 | 6.6e-05 | MATCH | MATCH |
| 1 | 3 | 2316046459031032843375257.362502 | -1.012 | -1.0122159 | -1.012 / -1.012 | -1.012 / -1.012 | 2.2e-04 | MATCH | MATCH |
| 1 | 4 | 13355123870465460300049497.114138 | 1.0019 | 1.0018861 | 1.0019 / 1.0018 | 1.002 / 1.001 | 1.4e-05 | MATCH | MISMATCH |
| 1 | 5 | 15070658556209921536065525.478881 | 1.0004 | 1.0004497 | 1.0004 / 1.0004 | 1.000 / 1.000 | 5.0e-05 | MATCH | MATCH |
| 2 | 1 | 8895437864289868028.044074 | -0.974798 | -0.9747933 | -0.974793 / -0.974793 | -0.975 / -0.974 | 4.7e-06 | MISMATCH | MISMATCH |
| 2 | 2 | 13859539710197847064.062257 | -0.9949 | -0.9949695 | -0.9950 / -0.9949 | -0.995 / -0.994 | 6.9e-05 | MISMATCH | MATCH |
| 2 | 3 | 19571878850562201959.215107 | -1.007 | -1.0074516 | -1.007 / -1.007 | -1.007 / -1.007 | 4.5e-04 | MATCH | MATCH |
| 2 | 4 | 44533695580955902790.827323 | -0.9949 | -0.9950007 | -0.9950 / -0.9950 | -0.995 / -0.995 | 1.0e-04 | MISMATCH | MISMATCH |
| 2 | 5 | 64171705557420452732.080835 | -1.02 | -1.0206515 | -1.02 / -1.02 | -1.021 / -1.020 | 6.5e-04 | MATCH | MATCH |
| 2 | 6 | 133837185572795505699.262652 | -0.9998977 | -0.9998977 | -0.9998977 / -0.9998976 | -1.000 / -0.999 | 3.9e-08 | MATCH | MISMATCH |
| 2 | 7 | 155558488686568113612.224656 | 1.025 | 1.0255843 | 1.026 / 1.025 | 1.026 / 1.025 | 5.8e-04 | MISMATCH | MATCH |
| 2 | 8 | 185415676820850375395.577179 | -0.997 | -0.9973603 | -0.997 / -0.997 | -0.997 / -0.997 | 3.6e-04 | MATCH | MATCH |
| 2 | 9 | 189471283149477540226.654238 | 0.997 | 0.9975073 | 0.998 / 0.997 | 0.998 / 0.997 | 5.1e-04 | MISMATCH | MATCH |
| 2 | 10 | 834072772235759174844.571429 | 1.0017 | 1.0017919 | 1.0018 / 1.0017 | 1.002 / 1.001 | 9.2e-05 | MISMATCH | MATCH |
| 2 | 11 | 955426264098867920866.136509 | -1.0002 | -1.0002081 | -1.0002 / -1.0002 | -1.000 / -1.000 | 8.1e-06 | MATCH | MATCH |
| 2 | 12 | 875055372917917742274.218133 | 1.00057 | 1.0005881 | 1.00059 / 1.00058 | 1.001 / 1.000 | 1.8e-05 | MISMATCH | MISMATCH |
| 2 | 13 | 1622648223749122520779.415144 | 1.0079 | 1.0079496 | 1.0079 / 1.0079 | 1.008 / 1.007 | 5.0e-05 | MATCH | MATCH |
| 2 | 14 | 1883922422293221654459.096574 | -1.00004 | -1.0000718 | -1.00007 / -1.00007 | -1.000 / -1.000 | 3.2e-05 | MISMATCH | MISMATCH |

rows: 19; rounding {'MATCH': 11, 'MISMATCH': 8, 'AMBIGUOUS': 0}; truncation {'MATCH': 13, 'MISMATCH': 6, 'AMBIGUOUS': 0}

## Corrections (wrong at printed precision under either convention; all in Table 2)
| row | y | printed | certified value (ball, 320 bits) | correct at printed precision |
|---|---|---|---|---|
| 1 | 8895437864289868028.044074 | -0.974798 | [-0.97479333363088991334 +/- 4.79e-21] | -0.974793 (7 dp: -0.9747933) |
| 4 | 44533695580955902790.827323 | -0.9949 | [-0.99500072373864079385 +/- 4.10e-21] | -0.9950 (7 dp: -0.9950007) |
| 12 | 875055372917917742274.218133 | 1.00057 | [1.0005881419096789907 +/- 2.85e-21] | 1.00059 rounded / 1.00058 truncated (7 dp: 1.0005881) |
| 14 | 1883922422293221654459.096574 | -1.00004 | [-1.0000718299934674451 +/- 5.06e-21] | -1.00007 (7 dp: -1.0000718) |

Rows 1, 12 and 14 disagree with the print only in the last printed digit and agree at 3 decimals under both
conventions. Row 4 at 3 decimals is convention-dependent: the certified value is -0.995 under both conventions;
the printed -0.9949 becomes -0.995 if rounded to 3 decimals and -0.994 if truncated, so a 3-decimal disagreement
appears only under truncation.

## Convention-dependent rows (not listed as corrections)
At printed precision, Table 2 rows 2, 7, 9 and 10 mismatch under rounding and match under truncation:
- row 2, y = 13859539710197847064.062257, printed -0.9949, certified -0.9949695 (rounds to -0.9950, truncates to -0.9949);
- row 7, y = 155558488686568113612.224656, printed 1.025, certified 1.0255843 (rounds to 1.026, truncates to 1.025);
- row 9, y = 189471283149477540226.654238, printed 0.997, certified 0.9975073 (rounds to 0.998, truncates to 0.997);
- row 10, y = 834072772235759174844.571429, printed 1.0017, certified 1.0017919 (rounds to 1.0018, truncates to 1.0017).
Rows 7 and 9 are the only 3-decimal disagreements under rounding; they agree at 3 decimals under truncation.
The other way around, Table 1 row 4 (printed 1.0019, certified 1.0018861) and Table 2 row 6 (printed -0.9998977,
certified -0.999897661) match under rounding and mismatch under truncation; they are not called corrections.

## The 19 certified values to 3 decimals (p1 deliverable)
The convention-free objects are the 320-bit balls in result/p1_certified_values.json. Rendered to 3 decimals:

| table | row | certified (3 dp, rounding) | certified (3 dp, truncation) |
|---|---|---|---|
| 1 | 1 | 0.991 | 0.991 |
| 1 | 2 | -0.993 | -0.993 |
| 1 | 3 | -1.012 | -1.012 |
| 1 | 4 | 1.002 | 1.001 |
| 1 | 5 | 1.000 | 1.000 |
| 2 | 1 | -0.975 | -0.974 |
| 2 | 2 | -0.995 | -0.994 |
| 2 | 3 | -1.007 | -1.007 |
| 2 | 4 | -0.995 | -0.995 |
| 2 | 5 | -1.021 | -1.020 |
| 2 | 6 | -1.000 | -0.999 |
| 2 | 7 | 1.026 | 1.025 |
| 2 | 8 | -0.997 | -0.997 |
| 2 | 9 | 0.998 | 0.997 |
| 2 | 10 | 1.002 | 1.001 |
| 2 | 11 | -1.000 | -1.000 |
| 2 | 12 | 1.001 | 1.000 |
| 2 | 13 | 1.008 | 1.007 |
| 2 | 14 | -1.000 | -1.000 |

Table 2 row 5 is printed with only 2 decimals (-1.02) and matches at that precision under both conventions; the
print does not give a third decimal to confirm. The record row (Table 2 row 3, y = 19571878850562201959.215107)
matches at its printed precision under both conventions: h_StR = -1.0074515722180327214 +- 2.4e-22, so
|h_StR| > 1 + 6e-8 holds rigorously.

## Prior work (credit; the record cell is not new)
- The record cell (Table 2 row 3) was already independently re-evaluated:
  L. H. Gallego, Zenodo 10.5281/zenodo.23700211 (2026-10-27), section 4 "Control": -1.00745, ball arithmetic;
  and Zhenyu Bi and Enze Hou, HAL hal-05838582 (2026-10-26) and github.com/bzyzz/mertens_bound,
  search/results/path1_report.txt: -1.0074515722 (256-bit MPFR).
  Our value agrees with both. What is new here is the re-evaluation of the other 18 rows and the four
  convention-free corrections above. Bi and Hou also report a polished neighbour of Table 2 row 2 ("Peak1",
  about 6e-5 away in y, about -0.99590, uncertified). That is a different point; it is not a re-evaluation of
  Kim-Nguyen's printed -0.9949 at the published y, and is not used as one here.
- S. Kim and P. Q. Nguyen, arXiv:2502.21021 and Zenodo 10775723 (the y values and their own Arb evaluator).
  Their HAL deposit hal-05016898 (post-referee text linked to the journal DOI) prints identical digits for all
  19 (y, h) pairs.

## Caveats
- Independent computation, not an independent method: our zeros come from the same Arb library (FLINT
  acb.zeta_zeros, python-flint 0.9.0) that Kim-Nguyen used for h_StR. For h_P they used other zeros (Hurst).
- Only arXiv v1 was compared directly. The journal version (Res. Number Theory 11 (2025)) was not checked
  (paywall). The HAL copy named above prints the same digits; if the typeset journal tables differ, the
  corrections above are corrections of the arXiv/ANTS/HAL text only.
- result/p1_certified_values.json was computed from zero files written by the v1 writer (arb str with more=True).
  code/zeros.py now writes plain arb strings (see CHANGES.md of claim_v2); check/spot_check_zeros.out shows, on
  1,200 zeros (n = 1..400, 49,601..50,000, 98,401..98,800, the last chunk crossing gamma = 74000), that every
  v1 and v2 ball contains a 512-bit reference value and v1/v2 midpoints differ by <= 5e-68. The values were not
  recomputed in full. The v2 REPRODUCE skeptic's own no-`more` zeros overlapped all 19 shipped balls.

## Files
- inputs/Test-ST.txt (Table 2, 14 rows), inputs/Test-Pinch.txt (Table 1, 5 rows): as published in Zenodo 10775723.
- inputs/kn_arxiv_v1_tables_excerpt.txt: pdftotext of Tables 1-2 from the arXiv v1 PDF (the printed values).
- code/zeros.py: zeros n = 1..N with zeta'(rho) (FLINT acb.zeta_zeros, 256 bits), plain arb string output.
- code/verify_p1.py: completeness of the zero list below each cutoff, and h at every y at 256 and 320 bits.
- result/p1_certified_values.json: output of code/verify_p1.py (all 19 rows, unchanged from v1 and v2).
- check/compare_printed.py (+ .md, .json): the 19-row comparison under both conventions, and the y+sqrt(y) column.
- check/spot_check_zeros.py (+ .out, .json): the more=True check (unchanged from v2).
- status_source.md: the bank's status page as fetched (v1).

Not claimed: anything about the Saouter-te Riele theorem itself (its hypotheses, cutoff or tail treatment), and no new
bound on the first counterexample.
