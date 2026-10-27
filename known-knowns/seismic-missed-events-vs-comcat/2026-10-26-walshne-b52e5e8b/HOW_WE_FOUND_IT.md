# How we found it (contributor text, unverified)

- **Search:** a matched-filter search of the first 72 h of the 2024 Parker Butte, Nevada sequence. The templates were
  385 ComCat events; the data were 8 public NN vertical channels.
- **Candidate:** it turned up a well-correlated detection 11.7 min after the mainshock with no ComCat entry. We picked
  8 P/S arrivals, relocated it, and measured a Wood-Anderson magnitude calibrated on co-located ComCat events.
- **Earlier panels:** the event was panelled twice (2/3 each).
  - The first package could not rerun its full null.
  - The second had a float32 FFT and running-sum normalisation artefact, which gave spurious correlations in the chunk
    holding the mainshock. That made a stated control summary irreproducible.
- **This run:**
  - Switched the detector to float64 numerators with directly computed window norms.
  - Reran the 600-control null and shipped every control's maximum.
  - Added the strictest null a skeptic had used: sample-level shifts within the busiest 2 h, where 1 of 3,000 controls
    beats the event. This is stated plainly.
  - Trimmed every side statement without a shipped input.
- **What did not work:** the float64 numerator alone was not enough. The cumulative-sum variance cancels catastrophically
  in the mainshock coda, so each window's norm had to be computed directly.
