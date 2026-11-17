# REPRODUCE skeptic: A100-like S14 + S16 event, 1973-11-26 07:46:28.6 UTC (fullwin panel)

context: subagent (fresh context, Claude Code Agent tool, subagent_type reproduce; fourth instance, three earlier ones died of an API error)

Scope: the event's numbers, the null over all of 1973 (401 controls), and the attribution evidence in CLAIM.md
"Added in this continuation". Code and outputs are in panel_work/reproduce3/ (NOTES.md is the running log).

## Method

- Own checker first, written from the prereg wording (quoted in the r3lib.py header): PREREG.v2 despike, whitening,
  band and decimation; run1_PREREG.md grid and gap handling; PREREG.v15 D14/D16/Dt and the null; PREREG.v5 R8;
  PREREG_fullwin A1-A5 and G1/G2. It has its own Steim2 decoder, standard Hampel, whitening, Butterworth (scipy
  order 4) and NCC (checked against np.corrcoef). I read none of the author's code before these results existed.
- Independent full-year scan (scan3.py, 365/365 days): forward Dt, C0 (all channels time-reversed), C1..C400 (S16
  rolled circularly by 3600 + 180 k s), the A5 reverse search (variants b and a), and A3 S16 responses.
- Own checks: candidate (cand3.py), R8/A1/A2/R9/A4/thermal/glitch rule (misc3.py), R6 on the saved tables (r6_3.py),
  G1/G2 (g12_3.py), A5/A3 scoring (a5a3_3.py), null summary (nullsum.py).
- Earlier instances' work used only after reading it. reproduce2's r2lib/scan2 implements the definitions and is
  checked against my numbers below. reproduce's BIFF reader and PDF text extraction were used for N1/N2, with my own
  byte-level cross-check.
- Author code rerun into my scratch only, after my own checks: a4_phase, att_check (R8), glitch_gates (G1/G2),
  attrib_a1a2 (A1/A2), a5_analyse (b, a) and a3_decide on the saved scans. Every output is byte-identical to
  results/. Step-3 scan rerun: see Determinism.

## Claimed vs recomputed

| item | claimed | own independent code | other |
|---|---|---|---|
| window start / onset | 07:45:58.641 / 07:46:28.641 | index 92613 on the midnight grid, same | r2: same |
| Dt | 0.3433 | 0.3437 | r2: 0.3433 |
| station lags (S14, S16) | +1.509, +2.113 s | +1.509, +2.113 s | r2: same |
| NCC S14 MH1 / MH2 | 0.426 / 0.562 | 0.4265 / 0.5757 | r2: 0.4264 / 0.5625 |
| NCC S16 MH1 / MH2 | 0.699 / -0.013 | 0.7002 / -0.0128 | r2: 0.6994 / -0.0128 |
| R8 candidate S16-S14 (ATT) | 0.93 s | 0.926 s (ATT offset, interpolated or nearest sample) | author rerun 0.93 |
| R8 nest median | 0.82 s | 0.619 s (5 events above 0.1906), 0.68 s with 08-09 | author rerun 0.82; r2 0.68 |
| R9 phase / interval | 157.2 in [46.7, 318.3] | 157.16 in [46.7, 318.3] (62 A100 events) | |
| null C0 / best shift | 0.1574 / 0.1906 (401) | 0.1318 / 0.1718 (401, 365 days) | saved file 0.1574 / 0.1906; r2 0.1389 / 0.1789 |
| gap | passed | 100% valid on all 4 channels over [onset-10 min, onset+450 s+10 min]; no timing jumps | |
| thermal | passed | solar elevation S14 -84.6, S16 -59.8 deg | |
| glitch rule | passed | 49 S14 MH2 samples flagged; Dt without S14 MH2 0.3437 > null; all half-window NCCs > 0 | |
| R6 (saved tables) | nothing within 70 min | 13,242 dated rows: none within 5 min, no levent span; nearest 06:36 A203, -70.5 min; Onodera none | |
| A1 other 11 nests | Dt 0.087-0.143, all below own null, no NCC >= 0.5 | Dt 0.0866-0.1454, all below own null, max NCC 0.451 | r2: 0.0872-0.1427 |
| A2 lag robustness | S14 +1.509 (0.494), S16 +2.113 (0.343), next S16 0.148 | S14 +1.509 (0.501; outer 0.431), S16 +2.113 (0.344; outer 0.151) | |
| A2 moveout | A100 -80 s; A35 -79, A244 -78, A7 -76 | same; 129 nests | |
| A3 candidate | R_MH1 2.49, R_MH2 1.27, r2 0.18 | 2.489, 1.247, r2 0.166 | |
| A3 refs | 06:36 A203 0.02, 14:38 A51 0.11, 05:49 A252 0.13 | 0.015, 0.092, 0.106 -> C3 does not hold | |
| A4 phases | 01-03 209.8 ... 12-23 154.3; 10-30 161.5 | all identical; spacings 27.05-27.26, 27.15, 27.22, 27.34 d | |
| A5 variant b | top 6 A100, 7 of top 10, A100 first of 98 nests by median | top 5 A100, 6th A18 (0.152), 7th A100 (0.149), 6 of top 10; A100 rank 1 of 58 (scored only), 9 of 98 (unscored = 0); C6 does not hold | author rerun identical to its text |
| A5 variant a | top 4 and 6 of top 10 | top 4 and 5 of top 10 | |
| A5 A35/A7/A244 | <= 0.106, none in 1973 | 0.109 / 0.107 / none | |
| G1 | no overlap; nearest S16 +774 s, S14 +1090 s | none; 07:59:23.0 S16 Step-Down MH1 (+774 s), 08:04:38.6 S14 (+1090 s); 18/18 sha256 OK; 26,140 / 48,854 / 40 = claim | author rerun identical |
| G2 | S14 0.451/0.648, S16 0.699/-0.013, Dt 0.343 | 0.451/0.651, 0.700/-0.013, Dt 0.344, pass | author rerun identical |
| N1 Knapmeyer-Endrun 2015 | no row; nearest 11-28 +54.9 h | byte scan of all 3 .xls: no 1973-11-25/26/27 date; 1973-11 dates 05, 06, 07, 18, 28 | reproduce BIFF parser: 290 rows, nearest +54.9 h |
| N2 Bulow 2005 Table 2 | 18 in 1973; nearest 12-02 22:36 (+158.8 h) | 123 year-led rows, 18 in 1973, none on doy 330; nearest 336 22:36 | |
| S16 levent flags 73-327..331 | LPX not LPY for most | 19 rows: LPX 10, LPY 1 | |

Also checked: waveform sha256 1481/1481 OK. The A100 stack is identical in both frozen files. The levent sha256 is
f95743b2...b0b9b93c, as claimed. The 10-30 02:25 event in my code: Dt 0.298, S14 0.631, S16 0.620, R8 0.715 s, as claimed.

## Determinism

- The author's step-3 scan: an earlier instance rerun days 1-175 with the claim's code, and I finished days 176-365
  (REPRODUCE.md step-3 command, output panel_work/reproduce3/out/author_rerun/scan_A100.jsonl). All 365 days are
  byte-identical to results/lagtol_scan_1973_A100.jsonl in fwd_peaks, rev_max and shift_max. This is a full-span
  determinism check.
- Every other author script I reran gave byte-identical output.
- The null claim does not rest on that rerun. It rests on (a) the saved full-span author file, which gives exactly
  0.1574 / 0.1906 / 401, and (b) my own independent full-span scan (365 days, 401 controls), where the candidate
  (0.3437) beats every control (best 0.1718). reproduce2's independent scan agrees (best 0.1789).

## Why my numbers differ from the claim's (the claimed values are reproduced exactly by the frozen code)

- Despike: "running MAD" is ambiguous. My standard Hampel (window MAD about the window median) gives S14 MH2 0.576;
  the running-median-of-deviations reading (reproduce2) gives 0.5625. S14 is quantised at 1-2 DU, so it is sensitive.
- After my checker was done, I found that the frozen code (apollo_lib.preprocess) widens invalid (gap) samples by
  20 s. The prereg text does not state this. It explains the lower null maxima in the two independent scans. It also
  explains the author's S14 MH2 being invalid at 07-13 and the 04-22 single-channel peak. The 07-13 event changes the
  R8 nest median: 0.82 for the author against 0.62-0.68 independently. It also moves the A5 per-nest median rank of
  A100: 1 of 98 for the author against 9 of 98 with zeros in mine. In both, the gate outcome is the same. The R8
  margin is <= 0.31 s against 2 s. C6 does not hold, because A100 has 5-7 of the top 10.

## Caveats (reported, not failures)

- Decimation phase: on the other phase of the decimation-by-2 grid, my code gives Dt 0.286, S14 best 0.470 (< 0.5) and
  S16 0.553. PREREG_fullwin declares this "reported, not gated", because the frozen grid was fixed before the scan.
  R7 therefore depends on that grid choice.
- The signal is at digitiser level. In the raw window S14 MH1 has std 0.20 DU (MAD 0), S14 MH2 1.26 DU and S16 MH1
  0.97 DU. The S16 side is MH1 alone (MH2 NCC -0.013). A3 explains this as an unresponsive MH2 then, and I
  reproduce A3.
- Not rechecked: the stack rebuild (REPRODUCE step 2), the S12 third-station file, the other 11 nests' full-year
  scans, and the live PDS re-fetch (NOVELTY's job). R6 was checked only against the saved tables.
- With my own validity rule, the unclaimed 01-30 A100-like detection has S14 best 0.4996 (borderline R7). The claim
  does not depend on it.
- Cosmetic: results/r8_att_A100.txt labels the S16-minus-S14 difference "S14-S12", an inherited label.

## Verdict

Every gate-relevant property of the claimed event holds in my independently written code: R7, R8, R9, the null over
all of 1973 with 401 controls, gap, thermal, glitch, R6 on the saved tables, G1/G2, and C1/C2/C3/C6 not holding. The
exact claimed numbers come back byte-for-byte from the frozen author code. The remaining differences are small and
traced to two implementation details the prereg leaves open: the Hampel MAD reading and the 20 s gap dilation. None
changes any gate.

pass: true
