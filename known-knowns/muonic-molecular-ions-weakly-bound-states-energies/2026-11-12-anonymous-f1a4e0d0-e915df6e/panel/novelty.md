# Novelty skeptic

Claim under test: ddmu (2,0) cell (partial win p1) of muonic-molecular-ions-weakly-bound-states-energies. Claimed
certified upper bound -0.488708325061607741252510781472877154393258585 m.a.u. at the eq. (14) masses, against the
bar -0.4887083249914 (Frolov, arXiv:2503.17389v1, Table I, N = 3700). Claimed gain 7.02e-11, required 1e-13.

## Status fetch (one request, no retries)

- URL: https://arxiv.org/abs/2503.17389
- fetch time: Wed Nov 11 22:06:51 UTC 2026 (from `date -u`, immediately before and after the request)
- client: one plain curl, User-Agent "V3R1T4S-novelty-skeptic/1.0 (research status check)"
- HTTP status: 200, 40029 bytes, sha256 426c8337ecf2b47709d0c4b9a57c48fea50d971025a0c26afb722533eed551c6
  (identical to the copy in the claim's source/ folder)
- value read from the page: "Submitted on 17 Mar 2025", version list shows only [v1], no journal reference field,
  no DOI. Title: "Properties of the weakly-bound (1,1)-states and rotationally excited (2,0)-states in the muonic
  molecular d d mu, d t mu and t t mu ions". So the status source is unchanged: no v2, no revised table.
- the abstract page carries no table. The table value was read from the v1 PDF saved in the claim's source/ folder
  (sha256 6d35b4b6...2ef81f; not re-downloaded, to keep to one request): Table I, ddmu (2,0) column, rows
  N = 2800 ... 3700: -0.4887083242297, -0.4887083245714, -0.4887083247575, -0.4887083248687, -0.4887083249605,
  -0.4887083249914 (N = 3700, the best row). Eq. (14): M_t = 5496.92153573, m_mu = 206.7682830, M_d = 3670.48296788,
  M_p = 1836.15267343 m_e. Bar confirmed as -0.4887083249914.
- nothing on the page was addressed to agents.

## Searches and what each returned

Web search (four queries, 2026-11-11 UTC):
1. the two eq. (14) mass strings with "ddmu (2,0) variational": only arXiv:2503.17389 itself uses these masses for
   this state (binding energy quoted there as about -102.648490859750 eV). No other computation at these masses.
2. Frolov (1,1)/(2,0) muonic ions 2025 2026 journal: only the arXiv preprint; no journal version found. Older Frolov
   papers: 1806.05388 ((1,1) states), 1008.3010, 1008.0128, 1111.2379, 1111.7056.
3. ddmu L = 2 D state high precision 2025 2026: 2503.17389 again; arXiv:1008.3010 gives ddmu D(L=2)
   -0.488708332375(10) m.a.u. at a DIFFERENT (older) mass set; a 2011 EPJD paper on the 22 bound S, P, D, F states,
   also at older masses; arXiv:2508.12783 (ddmu fusion T-matrix model, not a precision energy paper).
4. "2503.17389" with reproduce / recalculation / github / zenodo: no code, wavefunction or data deposit found.

arXiv API (export.arxiv.org, abstracts containing "muonic" plus molecular ions / muonic molecule / three-body /
muon-catalyzed, newest first, 50 entries): entries after 2503.17389 are 2508.12783 (ddmu T-matrix reaction model),
2512.07323 (stochastic variational, see below), 2604.18928, 2605.26432 (reviews / fusion concepts), 2606.11153
(nuclear Zemach moments), 2610.03810 (helium muonic atoms hyperfine structure), 2610.11499 (dtmu near-threshold
resonances). None reports a ddmu (2,0) total energy at the eq. (14) masses.

arXiv:2512.07323v2 (opened): masses given in MeV (m_d = 1875.61294, m_t = 2808.92113, m_mu = 105.65837), energies
in eV to 0.01 eV, S and P waves only; no L = 2 ddmu state; no wavefunctions released. Not comparable and not
competitive (0.01 eV is about 2e-6 m.a.u.).

Code and data:
- GitHub code search for "3670.48296788": CODATA constant tables (gt, great-tables, QCElemental, raven), two
  JuliaFewBody READMEs (Gaussian few-body tools using the deuteron mass with electrons, no muonic ddmu L = 2
  result), ohno/gaussian plotting scripts, and this bank's own known-unknowns page. No ddmu (2,0) wavefunction or
  energy. GitHub repository searches ("muonic molecule three-body variational", "ddmu muonic", "muon catalyzed
  fusion three-body exponential basis"): no results.
- Zenodo API: "muonic molecular" (1 hit, unrelated), 'ddmu OR "dd-mu" muonic' (nothing relevant in the newest
  hits). No deposit of muonic three-body wavefunctions found.

This repo (elder-plinius/V3R1T4S):
- remote HEAD via gh api: fb5164403fc71afeadc3d6d0dd0db44131665a8f (2026-11-09T19:54:43Z), same as the local
  FETCH_HEAD. Tree paths matching muon|frolov: only
  known-unknowns/physics/muonic-molecular-ions-weakly-bound-states-energies.md. No known-knowns entry
  (27 known-knowns directories listed, none on this id; grep for muonic / frolov / 2503.17389 in known-knowns: none).
- TROPHY_CASE.md (local copy and remote): no line matching muon, frolov or three-body.
- gh pr list --state all --search for: muonic, muon, ddmu, "dd-mu", frolov, "2503.17389", "molecular ions", the
  full bank id: all empty. ("three-body" returned only unrelated fuzzy matches.) The 12 newest PRs (up to #1065,
  2026-11-11T21:17Z) are all on other targets. gh search issues (with PRs) for muonic: empty.
- gh release list: no releases, so no release assets to lag the tree.

## Comparison

- Same-cell published values at the identical masses: only Frolov's Table I column. Its best row is
  -0.4887083249914; the claimed bound -0.48870832506160774... is lower by 7.02e-11, 700 times the required margin.
  It is a strict improvement, not a tie.
- Plausibility against the published sequence: Frolov's ddmu (2,0) column is still dropping (steps of 3.4e-10,
  1.9e-10, 1.1e-10, 9.2e-11 per 200 functions, then 3.1e-11 for the last 100), so a true level some 1e-10 below his
  last row is what his own table suggests; the claim is consistent with it.
- Other mass sets (not comparable at these digits): arXiv:1008.3010 -0.488708332375(10) is numerically lower than
  the claim by 7.3e-9, but it uses older masses; a shift of that size is what a change of order 1e-7 in the mass
  ratios produces, so it neither contradicts nor pre-empts the claim.
- Trivial-edit test: no wavefunction for this state has been published by anyone (Frolov releases none; none on
  GitHub, Zenodo or in this repo), so there is no published object from which deletion, restriction, relabelling,
  symmetry or a numerical polish could give this one. The neighbouring cells (dtmu and ttmu (2,0), ddmu (1,1))
  likewise have no published wavefunctions, and a relabelling of masses cannot map them to ddmu anyway. The claim
  names no seed and, as far as I can find, needs none.
- Limits of this check: I did not verify the certificate arithmetic (other skeptics' job); my searches cannot
  exclude unindexed or paywalled work, but nothing indexed in the last 24 months beats or ties the value.

novelty: CONFIRMED (strictly below the only published value at the identical masses; no prior object, no prior
claim in the repo)

context: subagent (fresh context, saw only claim/)

pass: true
