# Novelty skeptic: ttmu (2,0), partial win p1

target: muonic-molecular-ions-weakly-bound-states-energies, cell ttmu (2,0)
claimed: Rayleigh quotient upper end -0.512568647969898220243439490627127512105327902 (480 functions, eq. (14) masses)
bar: Frolov Table I, ttmu (2,0), N = 3800: -0.5125686450010

context: subagent (fresh context, saw only claim/)

## Status fetch (one request each, no retries)

- URL: https://arxiv.org/abs/2503.17389
  - fetched: Wed Nov 11 22:10:45 UTC 2026, plain curl, User-Agent "V3R1T4S-novelty-skeptic/1.0", HTTP 200, 40029 bytes
  - sha256 426c8337ecf2b47709d0c4b9a57c48fea50d971025a0c26afb722533eed551c6 (identical to the scout's saved copy)
  - value read: "Submitted on 17 Mar 2025", only [v1], no journal reference or DOI field on the page. No later version.
  - No text addressed to agents seen on the page.
- URL: https://arxiv.org/pdf/2503.17389v1 (the table itself is only in the PDF)
  - fetched: Wed Nov 11 22:10:54 UTC 2026, same client, HTTP 200, 310830 bytes
  - sha256 6d35b4b6876974670174af39b2592c06479278708802f4143c0d70ad2e2ef81f (identical to claim/source copy)
  - values read (pdftotext): eq. (14) "Mt = 5496.92153573 me, mmu = 206.7682830 me, Md = 3670.48296788 me";
    Table I, ttmu (2,0) column: N = 3000 -0.5125686232381, 3000 -0.5125686334174, 3200 -0.5125686375020,
    3400 -0.5125686421485, 3600 -0.5125686439316, 3700 -0.5125686446090, 3800 -0.5125686450010 (last row, the bar).
    Text: ttmu (2,0) binding energy quoted as about -172.701007428930 eV.
  - The column is visibly unconverged (steps of 1.8e-9, 6.8e-10, 3.9e-10 in the last rows), so a value about 3e-9
    lower is not implausible.

Current published value for the cell at the eq. (14) masses: -0.5125686450010. Claim minus bar = -2.9689e-9
(required margin 1e-13). Strictly lower, not a tie.

## Searches run and what each returned

Literature (all 2026-11-11, about 22:11 to 22:14 UTC):
1. Web search "muonic molecular ion ttmu rotationally excited (2,0) state L=2 total energy variational 2025 2026":
   returned arXiv:2503.17389 (the bar), arXiv:1008.0128 and 1008.3010 (Frolov and Wardlaw 2010), Kamimura PRA 38, 621
   (1988), an EPJ D 2026 paper on ppmu, ddmu, ttmu in non-ideal plasmas (S and P states only, screened potentials).
   No new ttmu L = 2 value.
2. Web search for a journal version of 2503.17389 (title phrases plus "journal"): none found; only the arXiv v1 and
   the older arXiv:1806.05388 ((1,1) states only).
3. Web search '"ttmu" D-state "0.51256" muon atomic units': returned arXiv:1008.3010 Table V (opened in full, see
   comparison below).
4. Web search for arXiv:2512.07323 (Wen and Zhu, extended stochastic variational approach, Dec 2025): opened the PDF.
   Its ttmu table (Table VII) lists only L = 0 and L = 1 channels, in eV with stated accuracy about 0.1 eV, CODATA
   masses in MeV. No L = 2 value; not comparable at these digits anyway.
5. Web search "ttmu three-body variational energies 2025 OR 2026 high precision exponential basis J=2": nothing beyond
   items 1, 3, 4.
6. Web search for CODATA 2018 mass recalculations by Korobov, Kamimura, Yamashita, 2024 to 2026: returned
   arXiv:2407.01756 (ddmu resonance states, Gaussian expansion, J = 0 to 3, not ttmu, not bound-state precision) and
   older work. Nothing for ttmu (2,0).
7. Web search for a 2025/2026 Frolov paper on D and F states of ttmu in EPJ D, PRA or J. Phys. B: none; only the 2011
   EPJ D paper (= arXiv:1008.3010).
8. arXiv API, three queries sorted by submission date (muonic AND molecular AND ion(s); au:Frolov AND (muonic OR
   three-body); muonic AND (three-body OR variational OR molecule(s))), HTTP 200 each. Entries since 2024-11:
   2610.11499 (dtmu near-threshold resonances), 2610.03810 and 2609.33059 (Frolov, muonic helium hyperfine),
   2604.23411 (Frolov, one-electron diatomic ions), 2512.07323 (item 4), 2508.12783 (ddmu fusion reaction T-matrix),
   2412.01507 (resonances with Li, He, H nuclei), 2503.17389 itself. None reports a ttmu L = 2 bound-state energy.
9. Semantic Scholar citations API for arXiv:2503.17389: HTTP 200, empty list (no indexed citing papers).

Code and data:
10. GitHub code search "5496.92153573": only CODATA constant tables (gt, QCElemental, mctc-lib, Antique.jl docs and
    similar) and this project's own known-unknowns page. Searches "206.7682830 5496.92153573", "ttmu muonic
    variational", "muonic molecular ion three-body variational": no code hits. Repository searches "muonic molecule",
    "muonic molecular ion", "three-body coulomb variational", "three-body variational exponential": nothing relevant
    (one unrelated muon-catalysed-fusion kinetics repository mentions a ttmu side-cycle, no energies).
11. Zenodo API, query "muonic molecular": 1 record, unrelated (true muonium speculation). Web search for
    GitHub/Zenodo wavefunction datasets for ddmu, dtmu, ttmu: none. No release assets exist to check because no
    repository with such wavefunctions was found. Frolov's papers release no wavefunctions.

This project:
12. Local read-only copy, newest tree (FETCH_HEAD fb51644, committed 2026-11-09): the only path containing "muon" is
    the known-unknowns page for this id. known-knowns/ has 27 target folders, none on muonic ions; grep for
    "muon" or "frolov" under known-knowns/ returns nothing. TROPHY_CASE.md (working copy and FETCH_HEAD): no line
    matching muon, frolov, three-body, coulomb or ttmu.
13. gh pr list --state all --search for "muonic", "muon", "ttmu", "Frolov", "molecular ions": no results (the search
    "three-body" returned only unrelated pull requests). The 25 most recent pull requests (up to #1065) contain no
    muonic claim. gh search issues "muonic" in the project: nothing.

## Comparison

Same cell, identical masses: the only published variational value found is Frolov's -0.5125686450010. The claim is
lower by 2.97e-9. No other calculation at the eq. (14) masses (which are the CODATA 2018 values) was found.

Same cell, other masses (not comparable digit for digit, reported as asked): arXiv:1008.3010 Table V, masses
m_mu = 206.768262, m_t = 5496.92158 m_e: ttmu D state -0.5125686538630 (N = 3800), extrapolated
-0.51256865410(11); earlier values quoted there -0.5125686539435 (Frolov, J. Phys. B 34, 3813 (2001)) and
-0.51256865199 (Frolov, Smith, Bishop 1994/95). These numbers are lower than the claim only because the nuclear to
muon mass ratio is larger by 1.1e-7 in that mass set.

Cross-check I ran (1 core, the claim's checker, basis file copied with only the "masses" line changed to the 2010
mass set, same 480 coefficients): Rayleigh quotient [-0.512568653931546031645 +/- 2e-51]. So the mass shift for
this function is 5.9616e-9, and at the 2010 masses the same object lies
- 6.9e-11 below the 2010 N = 3800 value,
- 1.2e-11 above the 2001 value quoted in that table (if that value refers to the same masses, which I did not verify),
- 1.7e-10 above the 2010 extrapolated limit (so it does not undercut the estimated exact energy; no sign of a
  non-variational artefact).
Reading: the object is of about the same quality as the best older D-state calculations and the 2025 Table I column
is simply under-converged by about 3e-9. Shifting the older energies by the first-order mass correction suggests
the exact eq. (14) energy is near -0.51256864814, about 1.7e-10 below the claim. That is an estimate of the exact
value from numbers at another mass set, not a published variational bound at the identical masses, and no
wavefunction behind those numbers was ever released, so it does not constitute prior art for this cell under the
bank's rule ("results for other masses are not comparable"). The claim should not be described as converged or as
better than the older calculations in an absolute sense; it is the lowest published upper bound at these masses.

Trivial-edit test: no wavefunction for this cell or for the neighbouring cells (ddmu (2,0), dtmu (2,0), the (1,1)
states) has been published anywhere I could find (papers give energies and expectation values only; no code, data
or release assets). The object therefore cannot be a deletion, restriction, relabelling, symmetry image or local
polish of a published object, and the claim names no seed. A published energy cannot be turned into an upper bound
at different masses by any valid propagation rule.

Neighbouring cells: bars -0.4887083249914 (ddmu) and -0.500118077325475 (dtmu) are for different systems and do not
bear on this cell.

Caveats: literature search is limited to what web search, the arXiv API, Semantic Scholar, GitHub and Zenodo index;
paywalled journal tables from 2025/2026 that are not on arXiv could have been missed. I did not check the
correctness of the certificate (other panel members' job); the mass-set cross-check above used the author's checker.

novelty: CONFIRMED for the cell at the eq. (14) masses (strictly below the only published value by 2.97e-9; no
equal or lower published value, no published wavefunction to derive it from).

pass: true
