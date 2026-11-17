# PREREG.v5: amendment to PREREG.v4 R8 (frozen 2026-11-12T19:27:29Z, no S14 1971 file downloaded yet)

Reason, from the PDS description document (apollo_pse_description.pdf, section 3.3.1, fetched 19:26:00Z): MiniSEED
sample times use the nominal sampling interval from the day's first timestamp and can diverge from the original
Earth-received timestamps (timing trace ATT) by a few seconds over 24 hours, independently per station. A +/- 2 s
moveout test on nominal times could therefore pass or fail for timing reasons alone.

R8 (replaces the PREREG.v4 wording): for a candidate, each station's arrival is the time of its best station-mean
NCC within +/- 10 s of the common lag, converted to Earth-received time with that station's ATT trace (the ATT
value of the nearest sample; ATT files fetched only for candidate days). The nest moveout is the median of the same
ATT-corrected S14-minus-S12 difference over the 1971 catalogued A1 events whose network detection exceeds the same
null maximum (if fewer than 5 such events, all 1971 catalogued A1 events with Dn >= 0.2). R8 passes if the
candidate's ATT-corrected difference is within 2 s of that median.

Also clarified: -1 marks missing samples on MH1/MH2/MHZ/SHZ (description section 3.3.2), as already assumed.
