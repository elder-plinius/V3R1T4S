# How we found it (contributor text, unverified)

Brief: build and calibrate an evaluator for deep-moonquake template matching on the restored Apollo PSE archive before
hunting for missed events. A MiniSEED Steim2 reader was written from the SEED 2.4 layout and checked against the PDS
GeoCSV twin (572,344 samples identical). The nest (A1, the largest), station (S12 LP, peaked mode) and scored year
(1971, the year with most A1 events among full peaked-mode S12 years) were fixed by a rule from the catalogue and the
PDS inventory before any waveform was read; 1972 was the development year.

What failed: the raw 0.3-1.2 Hz detector had a heavy-tailed null (daily maxima 0.18-0.21 on time-reversed data,
from the narrow peaked-mode resonance near 0.45 Hz) and recovered only about half of the dev events. What worked:
a Hampel despike for telemetry spikes, spectral whitening of each day (running mean of the amplitude spectrum over
0.1 Hz), and a 0.25-1.0 Hz band with a 450 s window starting 30 s before the S arrival, chosen on 1972 by
leave-one-out recall (53 of 54). Templates and threshold were then frozen and 1971 was scanned blind.
