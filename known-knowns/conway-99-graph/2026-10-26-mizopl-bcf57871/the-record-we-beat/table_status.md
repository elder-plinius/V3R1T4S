# Status Source & Record Baseline — `conway-99-graph`

- **Target ID:** `conway-99-graph`
- **Primary Reference URL:** `https://arxiv.org/abs/2608.11211`
- **Fetched UTC:** `2026-10-26T04:17:19Z`
- **HTTP Status:** `200`
- **Page SHA-256 (`data/2608.11211_abs.html`):** `682a82f9035b3580edd2b2f82ca3418d04ac9faf1e1cd8bff4510b9238034f65`

## Literature Baseline
1. **Aalok Thakkar & Simone Severini (`arXiv:2608.11211v2`, 18 Sep 2026, *Structure forced by Conway's 99-graph problem*):**
   Formulated the forced-structure reduction around a fixed vertex $x \in V(\Gamma)$ for $\Gamma = \mathrm{srg}(99, 14, 1, 2)$ (Section 2.3) and searched prime orders $p \in \{2, 3, 5, 7, 11\}$ via 14-core CP-SAT without published SAT CNF encodings or DRAT/LRAT proof certificates, timing out on standalone prime order $p = 7$ (`p7_fix1`) after $> 48\text{ hours}$.
2. **Patrick G. Cesarz & Andrew J. Woldar (`arXiv:2308.02978`, 2023, *On the automorphism group of a putative Conway 99-graph*) and H. A. Wilbrink (1983):**
   Excluded automorphisms of prime orders $p \in \{11, 13\}$ and the Frobenius group $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ via manual/GAP casework without machine-checkable DRAT/LRAT UNSAT proof certificates, while leaving standalone prime order $p = 7$ (`p7_fix1`) open.
