# The record we beat (target: indus-temporal-heldout-structure)

Status source (fetched once, honestly, by the run's scout and again by the NOVELTY
skeptic; no retries):
- URL: https://github.com/joyboseroy/indus_decipher (GitHub API metadata:
  https://api.github.com/repos/joyboseroy/indus_decipher)
- Fetched: 2026-11-17T03:23:41Z (UTC) (the scout's record: 2026-11-17T02:14:51Z)
- HTTP status: 200
- Page sha256: 80134dca083bb6cb01874969d9eaca39c3817ad527c2c330365a68346669b104
  (byte-identical across both fetches; the scout's copy is the run's data/gh_joyboseroy_meta.json)
- Value: pushed_at 2026-09-07T22:24:48Z, open_issues_count 0; the repo's own status
  section says "Active exploration, not a finished study"; no accepted decipherment.
  The Indus script is still undeciphered; the bank's 2026-10-03 status (USD 1M Tamil
  Nadu prize, Jan 2025, unclaimed; 2026 Zenodo + LLM-dictionary claims unaccepted) is
  unchanged.

The "table" this target is judged against is the pre-registered success criterion
(criterion_verbatim.txt in this folder) plus the published in-sample positional
findings it excludes:
- Mahadevan 1977 (corpus + positional observations), Rao et al. 2009/2010 and Yadav
  et al. (writing-system statistics), Kriger & Hunt 2026 (Zenodo
  10.5281/zenodo.19103880: positional constraints, sequence uniqueness, stroke
  numerals on the 179-inscription CISI set — in-sample), Kriger 2026 (Zenodo
  10.5281/zenodo.20040472, interpretation), arXiv 2608.02999 (SIGIL non-specificity,
  the design rationale for the synthetic control), paragorth/Indus- frozen
  predictions P1-P9 / Q1-Q14 / R1-R13 (in-sample rate/entropy/statistical bounds).
- The claim's object is the first *temporal* (M77-trained -> post-1977 held-out)
  dual-baseline, multi-site object-type predictive result: pooled 0.5846 vs 0.2808
  (KN3) / 0.1872 (synthetic), Mohenjo-daro 0.7098, Harappa 0.4017, paired-bootstrap
  p=0.0 < 0.001 at all three (object/claim_object.json; verified independently in
  panel/reproduce.md and panel/criterion.md). The 24-month literature/code search and
  the 21-comparator novelty diff (all NOT equivalent; closest: Q13 in-sample rate
  stability) are in panel/novelty.md and object/output_novelty_diff.json.
