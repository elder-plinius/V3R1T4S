context: subagent (Claude Code Agent tool, fresh context)

# NOVELTY skeptic: covid19-hub-europe-archive-beat-eurocovidhub-ensemble, partial win p3

Claim judged: an independent Python recomputation of every row of the European COVID-19 Forecast Hub archive's
evaluation/scores.csv (31,256 rows, 15 models, forecast dates 2023-10-30 to 2024-09-16), with every per-model
difference over 1% documented and explained (it comes from the hospitalisation truth source: ECDC file vs the OWID
file the hub's README names). Novelty question for a reproduction: does an earlier public, independent
recomputation of this file's per-model WIS decomposition with a discrepancy accounting already exist, or does a
V3R1T4S PR or trophy already cover it? The hub's own scores.csv, produced by its own R pipeline, is the object
being reproduced, not a prior reproduction.

## Status source (fetched once, honestly)

- URL: https://raw.githubusercontent.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/main/evaluation/scores.csv
- fetch time: 2026-11-13T06:01:49Z (UTC, `date -u` immediately before the single request; User-Agent "V3R1T4S-panel-novelty", 60 s timeout)
- HTTP 200, 2,800,631 bytes
- sha256: c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c, identical to the claim's
  c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c (the table has not changed since the claim's fetch)
- value: 31,256 data rows + header, 15 models, forecast dates 2023-10-30 to 2024-09-16 (as the claim and the bank
  page state). For p3 there is no numeric "record"; the status is the published table being reproduced.

## What I searched (each a single request, User-Agent naming V3R1T4S, a few seconds apart, no retries)

V3R1T4S repository
- Pinned workspace copy (commit cf68067f, 2026-11-03): TROPHY_CASE.md has no row mentioning COVID, forecast hubs,
  EuroCOVIDhub or WIS; known-knowns/ has 41 entries, none for this target or any forecasting hub
  (robust-forecast-aggregation-bounds is a mathematical bound, unrelated). The only page for this target is
  known-unknowns/disease-research/covid19-hub-europe-archive-beat-eurocovidhub-ensemble.md (open, the bank text).
- Live TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
  (06:08:48Z, HTTP 200, 31,306 bytes): 0 lines matching covid / forecast hub / eurocovidhub / WIS.
- Live known-knowns tree: https://github.com/elder-plinius/V3R1T4S/tree/main/known-knowns (06:08:53Z, HTTP 200):
  no COVID or forecast-hub entry.
- Pull requests (github.com web pages, not the API; counts read from the server-rendered page payload):
  - https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+covid19-hub-europe (06:02:16Z, HTTP 200): openCount 0, closedCount 0
  - https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+is%3Aclosed+covid19-hub-europe (06:02:21Z, HTTP 200): 0 open, 0 closed
  - https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+covid (06:03:05Z, HTTP 200): 0 open, 0 closed
  - calibration that the page does render results server-side:
    https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+gauss-kuzmin (06:03:10Z, HTTP 200): 1 open (#1033, a GKW
    claim), so a zero count above is a real zero, not an unrendered page.
  - neighbouring cells: is:pr WIS (06:06:52Z, 200): 0/0; is:pr respicast (06:06:57Z, 200) and is:pr forecast hub
    (06:07:02Z, 200): 1 closed each, the same bank-maintenance PR ("bank: FMM catalogue, kissing 25-48, ... live
    values as of 2026-10-18"), not a claim on any hub.
  - Issues: https://github.com/elder-plinius/V3R1T4S/issues?q=covid (06:07:07Z, HTTP 200): "No results".

The hub archive itself (could hold an external rescoring or a corrected file in a release)
- Releases: https://github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/releases (06:05:02Z, 200):
  weekly tags v2024.08.29 ... v2024.10.30; the latest's assets
  (https://github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/releases/expanded_assets/v2024.10.30,
  06:05:55Z, 200) are only the source zip/tar.gz, i.e. the hub's own snapshot.
- PRs mentioning scores: https://github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/pulls?q=is%3Apr+scores
  (06:05:07Z, 200): 15 closed, all hub-internal maintenance ("Create evaluation readme", "Re-run evaluation scores",
  "add AE to evaluation scores csv", "split scores", ...). No external reproduction.
- Issues mentioning scores: https://github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/issues?q=scores
  (06:05:12Z, 200): 21 items, the same internal items plus "Round evaluation scores", "pairwise scores are only
  computed for a subset of models", etc. None reports an independent recomputation or a discrepancy accounting.

Literature (last 24 months, plus the two papers named in the brief)
- Europe PMC (covers PubMed, PMC and medRxiv/bioRxiv preprints):
  - "European COVID-19 Forecast Hub" OR "covid19-forecast-hub-europe", first published 2024-11-01..2026-11-13
    (06:03:44Z, 200): 6 hits. Relevant ones: Becker, Sherratt, Bosse, Funk, "The influence of ensemble size and
    composition on the performance of combined real-time COVID-19 forecasts" (preprint PPR1064946, 2025-08-12;
    PLOS Comput Biol 2026-11-03, doi 10.1371/journal.pcbi.1014908) and Sherratt et al. PPR1003033 (2025-04-11). The
    others (Gozzi et al. behavioural models; Schulte et al. Germany 2021; a varicella benchmark) are unrelated.
  - "forecast hub" AND (WIS) AND (reproduc*/recomput*/replicat*), same window (06:03:48Z, 200): 12 hits; none
    recomputes a European hub scores file (US/Canada DMD forecasting, diffusion models, synthetic-outbreak
    evaluation, allocation scoring rules, forecastability, Stapper and Funk "Mind the Baseline" PPR1063096 on
    baseline choice, a multi-model-ensembles R tutorial, etc.).
  - "forecast hub" AND ("scores.csv" OR rescor* OR re-scor* OR reproducibility), same window (06:04:22Z, 200): 9
    hits; none relevant (the closest, "Auditing the fairness of the US COVID-19 forecast hub's case prediction
    models", is the US hub).
  - all-time list for "European COVID-19 Forecast Hub" / "European Forecast Hub" (06:07:12Z, 200): 46 hits; nothing
    in the list is a recomputation of the archive's evaluation file; the in-window items are those above.
  - Abstracts (core records, 06:04:17Z, 200): PPR1003033 evaluates 181,851 forecasts from 47 models between
    8 March 2021 and 10 March 2023 with WIS on log-transformed values: a different period and a different scale,
    an analysis of model accuracy, not a reproduction of scores.csv. PMC10238088 (the hub's eLife paper, Sherratt et
    al. 2023) covers 8 March 2021 to 7 March 2022: the hub's own evaluation of an earlier period.
  - Full text of PPR1064946 and PPR1003033 via /fullTextXML (06:07:35Z, 06:07:54Z): HTTP 500 both; noted, not
    retried; judged from abstracts. For Becker et al. I read the PLOS article page once
    (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014908, 06:08:13Z, 200): it uses
    forecasts for DE, PL, CZ, GB and FR from mid-March 2021 to mid-March 2022, scored with scoringutils, to study
    ensemble size and composition (code: github.com/epiforecasts/eurohub-ensembles). A different period and a
    different question; not a reproduction of this file.
- arXiv API: http://export.arxiv.org/... returned 301 (redirect to https, 06:04:39Z); the single https request
  https://export.arxiv.org/api/query?search_query=all:%22European%20COVID-19%20Forecast%20Hub%22&... (06:06:00Z, 200):
  1 hit, "Evaluating Forecasts with scoringutils in R" (2022, older than 24 months; a package paper using 2021 hub
  example data).
- Zenodo: first requests with size=50 got HTTP 400 (validation error: anonymous page size max 25), re-issued once
  with size=25:
  - q="European COVID-19 Forecast Hub" (06:06:04Z, 200): 1 record, doi 10.5281/zenodo.21161410 (2026-07-03), the
    hub's own final archival release (zip of v2024.10.30). The hub's own data, not a reproduction.
  - q="covid19-forecast-hub-europe" (06:06:10Z, 200): 1 record, the 2022 euro-hub-ensemble software release (hub
    team, earlier period).
- GitHub web search (logged out):
  - repositories "covid19-forecast-hub-europe" (06:04:53Z, 200): 7 repos: the hub's archive, website, submissions
    and baseline repos, two hub-team (epiforecasts) research repos (covid19-forecast-hub-europe-research, read once
    at 06:08:58Z, 200: a research/ folder, no rescoring of the archive file advertised; euro-hub-ensemble: ensemble
    methods), and one third-party submission-validation repo. None is an independent rescoring of scores.csv.
  - repositories "european forecast hub weighted interval score" (06:06:16Z, 200): 0; "EuroCOVIDhub" (06:09:30Z,
    200): 0.
  - code search ("covid19-forecast-hub-europe_archive" scores.csv, 06:04:58Z, 200) and issue search
    ("forecast-hub-europe" scores reproduce, 06:09:34Z, 200): 0 results, but GitHub code search needs a login, so
    the code-search zero is NOT evidence of absence; recorded as unavailable.

injection_suspected: none (no fetched page contained instructions addressed to an agent).

## Comparison with published objects for this cell and neighbouring cells

- This cell (the archive's scores.csv, 2023-10-30 to 2024-09-16): the only published object is scores.csv itself,
  produced by the hub's R pipeline (code/evaluation, EuroForecastHub, scoringutils). That is the thing reproduced,
  not a prior reproduction. I found no public independent recomputation of it, by the hub team or anyone else, and
  no per-model discrepancy accounting.
- Neighbouring cells: the hub's earlier-period evaluations (eLife 2023, 2021-22; PPR1003033, 2021-23, log scale;
  Becker et al., 2021-22, five countries; Bosse et al. 2023 transformed-scale rescoring, older than 24 months) are
  analyses of model accuracy over different periods or scales, with no reconciliation against a published per-row
  score file. The RespiCast-COVID19 latest-forecast_scores.csv (from 2024-10-23) and the US hubs are other hubs;
  no V3R1T4S PR covers any of them.
- Trivial-edit test: the claim is not a copy or relabelling of scores.csv; it rescored all 31,256 rows from the
  357 data-processed files and the truth files with code written independently of the hub's R. It is seeded from
  the hub's published pipeline conventions (Bracher WIS with half-weight median, point-as-median substitution,
  Monday file-date mapping, add_status "final" filter) and names them (load_and_score_models.r,
  EuroForecastHub::score_forecasts and add_status). Simply re-running the hub's own R code would not count as an
  independent reproduction; this claim goes beyond that (independent implementation, re-derived row-selection
  set equal to the published one, and a row-level account of every mismatch).
- Caveat on the "why": the reconciling rule (hospitalisation truth = the archive's OWID file, Czechia only) is
  stated in the hub's own data-truth README, so the explanation confirms documented hub practice rather than
  revealing an unknown error. That does not make the reproduction non-new, since no earlier independent
  recomputation exists, but the result should be described as "scores.csv reproduces exactly under the hub's
  documented truth sources", not as a newly discovered discrepancy. Whether p3 is met when that rule was not
  declared in PREREG (primary truth = ECDC files) is a question for the CRITERION skeptic, not for me.
- Strictly beats everything known: for a reproduction partial win there is no numeric record to tie; the relevant
  bar is that nothing equivalent is published. Nothing equivalent was found in the sources above.

## Limits of this check

GitHub code search was unavailable logged out; two Europe PMC full texts returned HTTP 500 (judged from abstracts
and, for Becker et al., the journal page); medRxiv was reached only through Europe PMC; forks of the archive were not
enumerated; Stapper and Funk (PPR1063096) was judged from its abstract (baseline selection across hubs, not a
reproduction of this file). Within these limits I found no prior independent recomputation of this scores.csv with
a per-model discrepancy accounting, and no V3R1T4S PR, issue, trophy or known-knowns entry covering it.

novelty: NEW (no earlier public independent recomputation of this scores.csv found; status source unchanged,
sha256 matches)

pass: true
