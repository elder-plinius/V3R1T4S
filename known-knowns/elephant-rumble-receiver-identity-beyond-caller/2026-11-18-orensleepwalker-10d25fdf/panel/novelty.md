# Novelty review: partial win p3 of elephant-rumble-receiver-identity-beyond-caller

context: fresh subagent started for this claim only

Reviewer role: NOVELTY skeptic (one of three). Inputs: claim/CLAIM.md, claim/target.md and claim/data/europepmc-citations.json (only to diff it against my own fetch), plus the web and the V3R1T4S repository. I did not read anything else in the workspace.

Question asked: has any published work (paper, preprint, comment, reanalysis, code release) already reported a caller-habit baseline and a within-caller receiver-label shuffle null for Pardo et al. 2024's receiver-prediction result (27.5%)? Has any V3R1T4S submission already claimed this target?

## Status source (one plain fetch, no retries)

- URL: https://www.ebi.ac.uk/europepmc/webservices/rest/MED/38858512/citations?format=json&pageSize=100
- User-Agent: `V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)`
- Time (UTC): 2026-11-18T22:55:56Z
- HTTP status: 200
- Value: hitCount = 32 (all 32 returned on one page)
- I compared this with the claimant's saved fetch (2026-11-18T19:25:40Z). That fetch also has hitCount 32 and the same set of titles: nothing added, nothing removed. target.md listed 31 on 2026-11-13, so one citing paper appeared between 2026-11-13 and the claimant's fetch. I read all 32 titles.
- Findings: none of the 32 citing titles is a reanalysis, reproduction, Matters Arising, or comment on the receiver-prediction model. They are:
  - reviews or perspectives (Utterance evolution; Language-like properties in the vocal behavior of animals; The 'design features' of language revisited; Vocal labeling of others by nonhuman primates; Do elephants have names for each other?; AI decodes the calls of the wild; AI is helping to decode animals' speech; Looking back on 2024; Do elephants really never forget?; Knowledge transmission, culture and the consequences of social disruption in wild elephants)
  - unrelated empirical work on other species or topics (parrots, bats, marmosets, rats, birds, Asian elephant voice familiarity, zoo seismic monitoring, tourism impacts, rumbles of female populations, male group departures, PAM/deep learning)
  - philosophy or theory papers.

## V3R1T4S repository (github.com/elder-plinius/V3R1T4S, via gh CLI, 2026-11-18 to 19 UTC)

- TROPHY_CASE.md (100 lines): no match for elephant, rumble or Pardo.
- known-knowns/: 39 entries, none about elephants or animal communication.
- Pull requests, all states: 1,121 listed. Titles, branch names and bodies contain no elephant, rumble or Pardo. `gh search prs` for each term (open and closed) returned none.
- Issues, all states: 48 listed, with no elephant, rumble or Pardo in title or body. `gh search issues` returned none.
- Releases: none with assets. Repository tree: the only matching path is the target file itself (known-unknowns/animal-communication/elephant-rumble-receiver-identity-beyond-caller.md).
- Conclusion: no prior or competing V3R1T4S claim on this target.

## Literature and code search (window: last 24 months and later)

- Web searches:
  - reanalysis of "African elephants address one another with individually specific calls" with caller-identity confound
  - Pardo 2024 random forest 27.5% critique, Matters Arising
  - PubPeer plus title or DOI
  - within-caller permutation or shuffle plus Dryad hmgqnk9nj
  - arXiv/bioRxiv 2025-2026 reanalyses of the elephant vocal-label data
  - Nature Ecology & Evolution comment or reply on the caller confound
- Results: only the original paper (journal, bioRxiv 2023 preprint, Dryad, Zenodo), press coverage, and quoted outside critiques in news pieces (e.g. National Geographic: caller and receiver are confounded). None of them computes a caller-habit baseline or a within-caller shuffle null.
- PubPeer: https://pubpeer.com/search?q=10.1038%2Fs41559-024-02420-w returned a JavaScript-only shell with no content. The page did not render, but this was not an HTTP block. I could not confirm or rule out a PubPeer thread this way, and web search found none.
- GitHub code and repository search:
  - repos "elephant rumble": only detection and denoising projects. One, amoghshetty7436/elephant-rumble-private, is an empty repository.
  - code "hmgqnk9nj": hits are the V3R1T4S target file; sheelmorjaria/bioacoustic_pipeline; and BowonKwon/Animal-Signals (a studies.csv list).
  - code "n469": no elephant hits apart from an unrelated emotion-classification README.
  - code "caller-habit elephant": none.
- sheelmorjaria/bioacoustic_pipeline (created 2026-10-13, last push 2026-10-24, no releases) does load the n469 spectral file. I read scripts/receiver_grounding_experiment.py. It studies the playback-response data (predicting the subject's response with Ridge regression, grouped by subject and caller). It does not re-implement the receiver-ID random forest. It contains no caller-habit baseline and no within-caller receiver-label shuffle, so it does not anticipate p3.

## Comparison and trivial-edit test

- p3 is a reproducibility and control result, not a record value. The published comparators are the paper's own numbers: 27.5% against a permuted-feature null of 8.0%, and the cross-caller model at 1.1% against a null of 1.4%.
- Neither the paper nor anything I found reports:
  - the caller-habit baseline under the paper's caller-by-receiver-stratified 7-fold scheme (the claim reports 0.4922)
  - a within-caller receiver-shuffle null for the forest (the claim reports a 99.9th percentile of 0.2426 and a maximum of 0.2449).
- Neither control can be had from the published figures by deletion, restriction, relabelling or polishing: each needs new computation on the deposit.
- The claim's conclusion is that 27.5% exceeds the within-caller shuffle null but not the caller-habit baseline. No published source states that.
- The claim names its seed object (the paper's random forest and the authors' Zenodo R code) and goes beyond it with the two new controls.
- Since no prior result exists for this comparison, there is nothing to tie or beat.

## Limits of this review

- I could not query Google Scholar directly; web search was the substitute.
- The PubPeer page did not render (see above).
- Europe PMC's citation index can lag recent comments and preprints.
- Novelty only: I did not check correctness (whether 0.2695 is within 0.02 of 0.275, fold construction, leakage). The other panel members cover that.

novelty: CONFIRMED (no published or V3R1T4S prior report of a caller-habit baseline or within-caller shuffle null for Pardo et al. 2024's receiver prediction, as of 2026-11-18T22:55:56Z)
pass: true
