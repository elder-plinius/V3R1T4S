# How we found it (contributor text, unverified)

We screened all 110 bank targets rated 3.5 or higher against every V3R1T4S pull request and picked this one because nobody had submitted on it. For even degrees 32..60 the database lists only skew-symmetric maxima, while at degrees <= 30 a non-skew polynomial is the true maximum at d = 8, 16, 18, 24 and 30.

The search is tabu / iterated local search over +-1 vectors. Its fast objective is the mean of log|f| at 1024 roots of unity (Jensen's formula), with all single flips scored at once. Calibration: in 40 s per degree it recovered the exhaustive maxima of LargeLittlewood.txt at d = 26, 28 and 30.

Unseeded 2-minute runs per even degree beat the table at d = 32, 36 and 40 and fell short elsewhere. Seeding with the table's own skew-symmetric polynomials and running for 5 minutes only returned ties at d = 34 and 38..60.

Certification used FLINT/Arb root isolation and mpmath at 60 digits. A fresh three-reviewer panel re-derived the values, three ways for the REPRODUCE reviewer. We also checked all Turyn/Fekete shifts at prime lengths 37 and 41: they fall below the claims.
