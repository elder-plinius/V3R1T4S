# How we found it (contributor text, unverified)

- A scan of the whole V3R1T4S bank on 2026-11-09 flagged meunier-stable-kneser-odd-s-small-n: its deep-check worker
  found that an exact colouring search decides the five (3,5) cases the bank lists as open (n = 17..21) in seconds.
- This run built the certificates the criterion asks for: a CNF generator from the definition, CaDiCaL proofs checked
  by drat-trim, explicit colourings, and an independent exact search, calibrated first on the (3,3) cases of
  arXiv 2607.12912. The n = 21 proof was 308 MB with a 5-set clique; the largest allowed clique (7 sets) shrank it to
  11 MB, and trimming plus binary DRAT and xz to 873 kB.
- The first three-skeptic panel failed the claim on novelty: Jonsson's 2012 manuscript (Theorem 1.3) already gives
  chi = n - 10 for n = 18..21 and every n >= 23, but not for n = 17 or n = 22. The bank and arXiv 2607.12912 quote his
  result as "n >= 22", which his text does not say for s = 5. So n = 22 was added (CaDiCaL: 312 s, a 752 MB proof,
  regenerated identically) and a fresh panel judged the revised claim; it passed 3/3.
- So the new mathematics here is n = 17 and n = 22; n = 18..21 are computer confirmations of Jonsson's theorem.
