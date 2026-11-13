# PREREG.v15: lens lagtol-s14s16-1973, full criterion for 25 nests on S14 + S16 in 1973 (frozen 2026-11-13T03:40:56Z)

S14 and S16 data of 1973 were scanned before only for nest A1 (lens s14-s16-coinc-1973) and S14 for A1 (lens
s14-single-1973); for the nests below no S14 + S16 analysis exists. The S12 + S14 lag-tolerant scan of these nests in
1973 (PREREG.v14) found 18 uncatalogued two-station detections above their nulls, none with CC >= 0.5 at both
stations; S16 is a different station pair, not a re-test of those.

## Scope

- Nests: the 25 lens-8 nests (A18, A10, A9, A6, A218, A14, A204, A39, A23, A36, A7, A26, A16, A20, A201, A100, A210,
  A29, A25, A216, A86, A38, A257, A22, A319); not A1.
- Stations S14 MH1/MH2 + S16 MH1/MH2 (location 00), all 365 days of 1973.
- Joint templates per nest from its own 1973 catalogued events, glitch-screened builder (tools/nesttemplates2.py),
  clean reference (largest positive A1 + A2 + A4 among events whose four reference-window channels pass the screen);
  drop rule: fewer than 3 members or a template channel max|t|/rms > 8.

## Statistic, null, criterion (as PREREG.v14, stations S14 and S16)

- D14, D16 = mean single-channel NCC over each station's valid channels (>= 1 each); Dt(t) = min(max over |d| <= 7
  samples (2.11 s at 3.3125 Hz; the PREREG.v14 implementation uses the same 7 samples) of D14(t + d), the same for
  D16). Declustered peaks (+/- 5 min).
- C0 time-reversed; C1..C400 S16 rolled by 3600 + 180 k s. Candidate Dt above every control's full-span maximum.
- R7: best single-channel NCC >= 0.5 at S14 and at S16, each at its own best lag within 7 samples of the common lag.
  R8: ATT-corrected S16-minus-S14 arrival difference within 2 s of the nest's median over its catalogued 1973 events
  above the null (else Dt >= 0.2). R9: anomalistic phase inside the nest's 95% interval. Gap, glitch and thermal
  checks at both stations; R6 live; Onodera; literature.
- Time box: if the scan has not finished by 05:15Z, the lens is reported as incomplete.
