# How we found it (contributor text, unverified)
- Aim: bank partial win p1, an independent certified re-evaluation of Kim-Nguyen's Tables 1-2. Overnight hunt also
  tried to beat the exp(1.96e19) record by their lattice method (no smaller certified y) and to check the
  bzyzz exp(3.485e18) claim (partial, not used as a record).
- Replay: own zeros n = 1..99,200 (FLINT acb.zeta_zeros, 256 bits, index-certified; 98,625 below 74000). All 19
  published rows certified at 256 and 320 bits. Record point h_StR = -1.0074515722180327214 +- 2.4e-22.
- Two wording panels failed before this one: v1 compared only 5 of 14 Table 2 rows; v2 assumed the paper only
  rounds, and listed 8 "corrections" of which four are convention-dependent. v3 reports both conventions and
  calls only Table 2 rows 1, 4, 12 and 14 corrections, at printed precision.
- Panel v3: three new fresh contexts passed. REPRODUCE recomputed the zeros and matched every row (same Arb
  library, so an independent computation, not an independent method). NOVELTY's GitHub PR listing was blocked
  (403); a later connector check found no PR on this target (only #1218, a different Mertens target).
