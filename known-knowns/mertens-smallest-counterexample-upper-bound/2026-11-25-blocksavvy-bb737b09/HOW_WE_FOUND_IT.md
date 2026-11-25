# How we found it (contributor text, unverified)

The bank listed p4: check the bzyzz exp(3.485e18) certificate. Its K_2 file gives the first 600,000 zeros as a tight ball but the
remaining 1.7 million only as a bound, so we summed every zero below 1.3e6 ourselves with python-flint balls, in 400-zero chunks
that could resume after interruptions. The first pass used 96 bits everywhere; that left the head ball at +/- 1.7e-5 because the
zero's radius is multiplied by v ~ 3.5e18 in the phase, so we redid n <= 600,000 at 128 bits, which shrank the total to +/- 5.1e-15.
The head agrees with the certificate's K2_main and the whole sum lies inside its K2 ball. In the same run a BKZ search for a
point below Kim-Nguyen's y (p3) failed: best certified value 0.98145, short of the 1 + 6e-8 threshold.
What failed: an over-wide enumeration radius ran out of memory (killed and replaced by a streaming search); the arXiv API returned
HTTP 500 once and we did not retry.
