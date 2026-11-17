# PREREG.v14: lens lagtol-25nests-1973, full criterion for 25 nests on S12 + S14 in 1973 (frozen 2026-11-13T01:18:14Z)

Written when 3 of the 1,098 S12 1973 files had been downloaded and none read. S14 1973 data were scanned before
only for nest A1 (lenses s14-single-1973 and s14-s16-coinc-1973); A1 is therefore excluded here.

Design lesson carried over from 1971 (lens coinc-25nests-1971, which stays as reported): after whitening, the
template-data NCC oscillates with lag at about 0.8 Hz, so a common-lag coincidence statistic loses events whose
S12-S14 timing differs from the template's by a fraction of a cycle (example: the A38 event of 1971-05-13 18:39,
S12 part 0.485 and S14 part 0.742 one sample apart, common-lag minimum 0.110). The bank already allows 2 s for the
relative arrival times, so the statistic below lets each station take its best lag within +/- 2 s.

## Scope

- Nests: the 25 lens-8 nests (A18, A10, A9, A6, A218, A14, A204, A39, A23, A36, A7, A26, A16, A20, A201, A100, A210,
  A29, A25, A216, A86, A38, A257, A22, A319); not A1.
- Stations S12 MH1/MH2/MHZ + S14 MH1/MH2 (location 00), all 365 days of 1973.
- Joint templates per nest from its own 1973 catalogued events, glitch-screened builder (tools/nesttemplates2.py,
  PREREG.v11), clean reference; drop rule: fewer than 3 members or a template channel with max|t|/rms > 8.

## Statistic

- D12(t) = mean single-channel NCC over valid S12 channels (>= 2), D14(t) = over valid S14 channels (>= 1), with the
  joint template's windows at common lag t. Dt(t) = min( max over |d| <= 2 s of D12(t + d), max over |d| <= 2 s of
  D14(t + d) ). Declustered peaks (+/- 5 min).

## Null (bank wording)

- C0: all channels time-reversed; C1..C400: S14 channels circularly rolled within each day span by 3600 + 180 k s.
  Same Dt, full span (365 days). A candidate's Dt must exceed every control's full-span maximum of its own nest.

## Full criterion for a candidate (all required)

- R7: at each station's own best lag within +/- 2 s of the common lag, the best single-channel NCC is >= 0.5 at S12
  and >= 0.5 at S14.
- R8: the two station lags converted to Earth-received time with each station's ATT trace; S14-minus-S12 difference
  within 2 s of the median of the same quantity over the nest's catalogued 1973 events whose Dt exceeds the null
  maximum (else those with Dt >= 0.2).
- R9: anomalistic phase inside the nest's 95% interval (all its catalogued events).
- Gap, glitch (PREREG.md rule with the null maximum) and thermal checks at both stations; R6 against every PDS table
  re-fetched live; Onodera windows; literature search of the last 24 months.
- p1 through this lens is not claimed (p1 is carried by run 2026-11-12-2317).
- Time box: if the scan has not finished by 05:20Z on 2026-11-13, the lens is reported as incomplete.
