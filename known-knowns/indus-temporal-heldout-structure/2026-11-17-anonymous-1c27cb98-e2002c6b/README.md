# Indus temporal held-out object-type predictability (submission 2026-11-17-anonymous-1c27cb98-e2002c6b)

## What

The class-conditional positional trigram model (n<=3, add-one, wildcard OOV, seed 20261117) fitted only on the M77 1977 corpus predicts the 4-class object type (seal/tablet/pottery/other) of the 1,613-object deduplicated post-1977 held-out pool (pooled n=1613: 0.5846 vs Kneser-Ney 0.2808 and synthetic 0.1872, p=0.0; Mohenjo-daro n=665: 0.7098 vs 0.3293/0.1173, p=0.0; Harappa n=590: 0.4017 vs 0.2153/0.2441, p=0.0; paired bootstrap 10,000 resamples), beating both baselines simultaneously at pooled, Mohenjo-daro and Harappa — a full-criterion win, not any of the enumerated partial wins p1/p2/p3.

Target: indus-temporal-heldout-structure (V3R1T4S target bank, pinned commit 25c99686fa759e1ce2825d94e15fb162505b1597; success criterion quoted verbatim in the-record-we-beat/criterion_verbatim.txt). The result is a *structural finding* (the sign sequence predicts the object type across the 1977 time split), explicitly **not** a decipherment. The 2-class Seal-vs-Tablet sub-property (0.6532 pooled vs 0.2834/0.1936, p=0.0) is the recorded secondary of the same object, not a second claim.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS (re-derives the per-site 4-class and 2-class accuracies from
object/output_sweep_main.json pool_detail, re-derives the frozen model's class priors from
how-we-built-it/data (M77 + im77), and checks the frozen model record, the 3x10,000
paired-bootstrap null test and the p < 0.001 threshold at pooled / Mohenjo-daro / Harappa).
Rough laptop time: <1 minute (stdlib python3 only; no network, no third-party packages).

## Compared to

- The bank's success criterion (the-record-we-beat/criterion_verbatim.txt): M77-only fit,
  frozen in a timestamped file, held-out deduplicated post-1977 objects, paired-bootstrap
  p < 0.001 against BOTH a tuned Kneser-Ney 3-gram on the same M77 data AND a SIGIL-style
  non-linguistic synthetic control matched on unigram+length, replicating on Mohenjo-daro
  and Harappa separately. The object is exactly that, at the "prediction of seal versus
  tablet object type from sequence" property (4-class, with the 2-class as recorded
  secondary).
- The closest published work is in-sample, not temporal: Kriger & Hunt 2026 (Zenodo
  10.5281/zenodo.19103880, positional constraints / sequence uniqueness / stroke numerals
  on the 179-inscription CISI set), the positional/entropy findings of Mahadevan 1977 and
  Rao et al. 2009/2010 / Yadav et al., and arXiv 2608.02999 (SIGIL non-specificity — the
  design rationale for baseline (ii)). None is a temporal M77->post-1977 dual-baseline,
  multi-site object-type result (see panel/novelty.md for the 24-month search and the
  re-run novelty diff; the closest comparator Q13 is an in-sample rate-stability bound, a
  different statistic on a different population).
- Status source (the Indus script is still undeciphered):
  https://github.com/joyboseroy/indus_decipher — GitHub metadata fetched 2026-11-17T03:23:41Z
  (HTTP 200, sha256 80134dca083bb6cb01874969d9eaca39c3817ad527c2c330365a68346669b104,
  byte-identical to the run scout's 02:14:51Z record): pushed_at 2026-09-07, 0 open
  issues, no accepted decipherment. See the-record-we-beat/record.md.

## Not claimed

- Not a decipherment of the Indus script (the criterion states the claim says "structural
  finding", never "decipherment").
- Not any of the enumerated partial wins p1/p2/p3 (the p2 field-symbol and p3 ligature
  probes were run and are negative; their recorded numbers are in
  object/output_sweep_secondary.json and the run's attempts/).
- The in-sample Q1/Q3/P1/P3 reproduction is not part of this claim (it is the step-3c
  baseline record, honestly logged as UNRESOLVED within the +/-0.02 tolerance; the
  temporal claim does not depend on it).
- The 776 duplicate cisi IDs (2,104 records) in the merged corpus survive as distinct
  (object ID, sequence) pairs, which is the literal reading of the dedup rule "(object ID
  and exact sequence)"; this is recorded in panel/criterion.md, not hidden.

## Credits

- Mahadevan 1977 (corpus, M77) as exported by joyboseroy/indus_decipher (pinned commit
  cd600349f6d3193a241c3eb87ff80a2a65377efc).
- paragorth/Indus- (pinned commit d62ec82d58642038640da25a97177d7a1fddc9d9): the im77
  corpus lines, field symbols, sign frequencies, the 386-identity directory, the
  merged-corpus reading order, and the frozen P1-P9/Q1-Q14/R1-R13 predictions used for the
  novelty diff.
- Kriger & Hunt 2026 (Zenodo 10.5281/zenodo.19103880), Kriger 2026 (Zenodo
  10.5281/zenodo.20040472), arXiv 2608.02999 (SIGIL non-specificity, the design rationale
  for baseline (ii)) — the published comparators.
- The V3R1T4S target bank (indus-temporal-heldout-structure, repo/bank/targets.json,
  pinned commit 25c99686fa759e1ce2825d94e15fb162505b1597).
- Three fresh-context skeptics (REPRODUCE / NOVELTY / CRITERION, see panel/).

## Large object files (kept out of git, listed here)

One input file exceeds the 1 MB per-file package limit, so it is kept outside this
package (and outside git); its size and sha256 are recorded here:

| file | size (bytes) | sha256 |
|---|---|---|
| how-we-built-it/data/merged-corpus-reading-order.json (absent here; present in the run's claim/data/) | 1452554 | 92fc8439cf87805fa022a16e1e5fd988006ee0f4235d70b775e4388437afe101 |

## Recreation of the large file (verified)

The file is NOT a derived artifact: it is `data/derived/merged-corpus-reading-order.json`
(5,369 records, Wells coding) **as shipped in the pinned public repo**
paragorth/Indus- @ d62ec82d58642038640da25a97177d7a1fddc9d9 (2026-10-07), git-tracked at
that commit. Verified: `git ls-files --error-unmatch` succeeds at the pin, and a fresh
shallow clone's copy hashes sha256 92fc8439cf87805fa022a16e1e5fd988006ee0f4235d70b775e4388437afe101 —
byte-identical to the stored copy. Fetch with:
`git clone --depth 1 --filter=blob:none https://github.com/paragorth/Indus-` and take
`data/derived/merged-corpus-reading-order.json`.

The machine-readable object that IS in the package (object/) is self-sufficient for the
checker: the 1,613-row pool_detail with per-object predictions carries the held-out set,
and how-we-built-it/data/ carries the M77 + im77 training inputs the priors are
re-derived from.
