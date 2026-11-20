# Edits made to claim/ after the panel filed, and why

All three panel files were written before these edits. **No number changed.** Both edits are corrections the
CRITERION skeptic asked for in `criterion.md` section 2 and section 7, made so the bundle does not contain a
sentence a skeptic called a stretch. The original wording is quoted in each case so nothing is hidden.

1. **`CLAIM.md`, the determinism paragraph.** Was: "three seeds were run, the seeds were passed to
   `numpy.random.default_rng` and `KFold(shuffle=True, random_state=seed)`, and the spread is reported as the
   zero it actually is." CRITERION: "the sentence as written suggests the seeds reach the fit, and they do not;
   it should read that the seeds are consumed by draws the deterministic fit does not use." Now reworded to say
   exactly that, to state that a mean over three byte-identical fits carries the information of one fit and that
   the reported standard deviation of 0 bounds no uncertainty, and to name configuration-selection noise rather
   than seed noise as the quantity no interval in this bundle covers.

2. **`CLAIM.md`, one file reference.** The selection-criterion section cited
   `../attempts/criterion-test/criterion_compare.out`, a path outside the bundle. It now names the in-bundle copy
   `the-earlier-runs/criterion_compare-this-run.out` as well. Same bytes.

Two further points CRITERION raised are recorded rather than edited, because editing them would overstate what
this run did:

- **Provenance of `data/gb1_data_full.csv`.** The claim asserts it is the released plmfit file and gives its
  sha256, but the bundle contains no evidence that it is byte-identical to upstream, because this run did not
  re-download it (its single permitted request was the status page). The same sha256 is recorded by runs
  2026-11-19-2355 and 2026-11-20-0215, both of which downloaded it. Re-verifying provenance needs one download
  and is listed under "Needs you" in the report.
- **A 5,765-against-5,743 test-set discrepancy** appears in the carried literature record
  `the-earlier-runs/related_work.md`, not in this run's measurements: every number this run reports is on the
  5,743 rows of the released file's own `three_vs_rest == test` column. It matters for comparing against
  published values, which is why the full criterion is not claimed, and it is flagged in
  `../baseline/published-values-correction.md`.
