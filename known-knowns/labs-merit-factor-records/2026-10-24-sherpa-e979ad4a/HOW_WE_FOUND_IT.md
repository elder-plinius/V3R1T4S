# How we found it (contributor text, unverified)

We assembled the published record for 121 <= L <= 449 from the primary sources, decoding every witness and recomputing
its energy. One earlier attempt in the same session ran CPU local search near L = 590 and could not escape the Legendre
basin. So we wrote a GPU self-avoiding walk in the skew-symmetric space, after the restriction-class idea of Dimitrov and of
Pšeničnik et al., and validated it against brute force and on proven skew optima at L <= 119. At L = 401 a pre-registered
random-start run found this sequence after about two minutes. The three-skeptic review then found a conference paper we
had missed (ERK'2025), whose figure-only value at L = 401 we still beat by 224. Runs at L = 381 and L = 449 did not beat
their published values.
