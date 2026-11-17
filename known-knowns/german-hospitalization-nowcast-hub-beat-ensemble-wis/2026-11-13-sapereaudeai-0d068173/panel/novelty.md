# Panel skeptic: NOVELTY

context: subagent (fresh context, Claude Code Agent tool)

Claim judged: partial win p3 of `german-hospitalization-nowcast-hub-beat-ensemble-wis` (claim/CLAIM.md): an
independently written Python script (claim/code/p3_reproduce.py) recomputes the 31 per-model mean WIS cells of
Wolffram et al. 2023 (PLoS Comput Biol 19:e1011394, Fig 7; data/scores/wis_{national,states,age}.csv of the
evaluation repository) and documents the rules needed to reconcile them (S0 no rules / S1 exclusion / S2 repairs then
exclusion). Read: claim/CLAIM.md, claim/scout_record.md, claim/REPRODUCE.md, claim/baseline/README.md,
claim/baseline/p3_S2_vs_published.csv, claim/reference_outputs/p3_log.txt (tail), claim/reference_outputs/p3_provenance_part1.txt,
claim/reference_outputs/hub_fetch_log_part1.tsv (head), the input-loading part of claim/code/p3_reproduce.py, and the
exclusion lists in claim/data/eval_data/. Nothing else in the run folder was read.

## Status source (one honest request, User-Agent "V3R1T4S-novelty-skeptic/1.0 (research audit; read-only)")

- URL: https://github.com/KITmetricslab/hospitalization-nowcast-hub
- HTTP status: 200 (232,412 bytes; sha256 6938696895ff2e0a9ea1aee61893763388ebec0e9a098ab97923619e928d3303)
- UTC fetch time: 2026-11-13T04:53:55Z (request start) to 2026-11-13T04:53:56Z (from `date -u` around the curl call)
- Value: the README describes the repository as an archive of nowcasts (data-truth, data-processed,
  data-processed_retrospective, data-processed_replaced). It carries no leaderboard, no "solved" or "reproduced" notice,
  and no instructions aimed at agents. Releases (GitHub API, 04:54Z): `Release_2023-04-14` (state used for the paper)
  and `Release2022-09-13`, neither with release assets.

## Sources checked (URL, time, what it shows)

1. Evaluation repository https://github.com/dwolffram/hospitalization-nowcast-hub-evaluation (API, 04:54:08Z):
   created 2023-04-17, last push 2023-10-26, 0 forks, no releases or tags, no issues or PRs. The `-new` URL redirects
   to the same repository. Its tree (329 files) holds the authors' full R pipeline: data_preparation/load_submissions.R,
   submission_check.R, frozen_baseline.R; src/fix_submissions.R; score_computation/compute_scores.R, compute_wis.R.
   It also holds the intermediate data (data/submissions.csv.gz, submissions_KIT-frozen_baseline.csv.gz,
   truth_2022-08-08.csv, submission_check/fixed/*-missing.csv) and the score tables. README: figure-to-script map plus
   renv instructions. No third-party reproduction is mentioned.
2. https://github.com/dwolffram/hospitalization-nowcast-hub-evaluation-old (API, 04:54:09Z): created 2022-04-20,
   last push 2023-04-19, 0 forks, no releases, no issues. An earlier copy of the authors' own pipeline.
3. Paper full text https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10446237/fullTextXML (05:02:40Z, HTTP 200)
   and S1 Appendix via https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10446237/supplementaryFiles (05:02:53Z,
   HTTP 200, zip; pcbi.1011394.s001.pdf). **The authors already document the reconciliation rules in prose.** Table
   A3 lists the excluded targets ("394 nowcast targets among the 109,968"). Table A4 lists the repairs: Epiforecasts
   0.1 quantile imputed by a normal approximation; LMU Saarland/Bremen and ILM 22-26 and 29 Nov 2021 filled from
   revised models; RKI 0-day values of "more than 1 billion" replaced "with the respective -1 day nowcasts".
4. Europe PMC citations of PMID 37566642 = PMC10446237
   (https://www.ebi.ac.uk/europepmc/webservices/rest/MED/37566642/citations, 04:55:01Z, HTTP 200): 28 citing items
   (2023-2026). Three of them reuse the hub data, and I read their full texts (04:55:28Z to 04:55:57Z, all HTTP 200):
   - Amaral, Wolffram, Moraga, Bracher 2025, PLoS Comput Biol (PMC11902281; code https://github.com/avramaral/ensemble_learning,
     last push 2024-12-17). It recomputes the WIS of the original models, but "in our adapted setting". That setting
     uses a 40-day target and a shortened evaluation period starting 8 Feb 2022, and the paper says it "is similar to
     Fig 13 from [10]". So it is a neighbouring cell from the same authors, not a reproduction of Fig 7.
   - Johnson et al. 2025, baselinenowcast, Wellcome Open Res (PMC13005074; code https://github.com/epinowcast/baselinenowcast-paper).
     They regenerated the KIT simple nowcast from its codebase and found a bug (hub issue #5899, open). They compared
     their method's WIS with the regenerated nowcasts. They do not recompute the hub's per-model published table.
   - Rieger et al. 2024, BMC Med Res Methodol (PMC11555927; code https://github.com/jo-rie/aatc). It applies
     ability-to-track-change measures to the hub's nowcasts. No WIS reproduction.
5. OpenAlex works citing W4385754098 (https://api.openalex.org/works?filter=cites:W4385754098, 05:04:06Z, HTTP 200):
   29 items. This list also covers arXiv and medRxiv. None is a reproduction of the evaluation. The one candidate by
   title, the MIPRO 2024 "Automated Processing of Pipelines..." paper (abstract read 05:04:15Z), is about a MEmilio /
   Airflow pipeline and is unrelated.
6. Europe PMC keyword searches limited to 2024-11-01..2026-11-13 (05:01:34Z to 05:01:40Z, HTTP 200):
   "hospitalization nowcast hub", KITmetricslab / "hospitalization-nowcast-hub", and "nowcast hub" with
   reproduction/replication and Germany. They return only the Amaral and Johnson papers above.
7. arXiv API https://export.arxiv.org/api/query (05:01:59Z): HTTP 429. Not retried. The http URL at 05:01:50Z
   gave a 301 redirect. arXiv citing works are covered through OpenAlex (item 5).
8. Zenodo https://zenodo.org/api/records?q=hospitalization nowcast hub (05:05:58Z, HTTP 200; two earlier calls
   gave HTTP 400 for a page-size parameter error, not a block). The only relevant records are the hub's own release
   (10.5281/zenodo.7828604) and the paper.
9. GitHub repository search for "hospitalization-nowcast-hub" (04:56:40Z): the hub, the hub website, the
   -validations repo, team model repos (RIVM, SU), and the two authors' evaluation repositories. No third-party
   evaluation repo.
10. GitHub forks of the hub (API, 04:56:50Z): 12 forks. The only recent ones (2024-2025) relate to the KIT-baseline
    bug work of item 4. None holds an evaluation reproduction.
11. GitHub code search (04:56:52Z to 04:58:12Z) for "wis_national", "wis_national.csv", "submission_check/fixed",
    fix_epiforecasts, "submissions_KIT-frozen_baseline", "truth_2022-08-08", "NowcastHub-MeanEnsemble" interval_score
    and KITmetricslab/hospitalization-nowcast-hub. The evaluation-specific strings occur only in the authors' two
    evaluation repositories. Hub-data users found and inspected:
    - https://github.com/DiogoRibeiro7/Medium-Blog (pipeline-time-correctness/part3, last push 2026-11-13T00:05Z;
      output.txt read 04:58:38Z). It scores ten hub models over 22 Nov 2021 - 29 Apr 2022, national all-ages only,
      by bias, MAE and 95% coverage. No WIS, no comparison with the published table. A neighbouring cell, not
      equivalent.
    - https://github.com/redam94/pymc-challenges (tools/build_e90_data.py). It rebuilds the reporting triangle and
      vintages only and reads no nowcasts.
    - https://github.com/MeioNeiz/meiolol (research/raw/wolffram-2023-collab-nowcast.md). A copy of the paper text.
    - https://github.com/stefanheyder/dissertation, https://github.com/kassteele/Nowcast-hub, epinowcast/epinowcast
      vignettes and nowcastdatasets. These are model code or data packaging, with no per-model reproduction of the
      evaluation.
12. Hub issues and PRs (GitHub search API, 05:01:03Z to 05:01:18Z): "WIS", "reproduce" and "score" return 0 hits;
    "evaluation" returns 1 unrelated hit (#194, 2021). The latest items, #5898 to #5900 (2025), are the
    KIT-baseline bug work.
13. V3R1T4S repository https://github.com/elder-plinius/V3R1T4S (API, 04:59:19Z to 05:00:36Z):
    - TROPHY_CASE.md has no nowcast, hospitalization or German entry.
    - known-knowns/ (6,177 tree entries) has no nowcast or hospitalization family.
    - Searches of PRs and issues for nowcast, hospitalization, the target id, Wolffram, KITmetricslab and
      "weighted interval score" return 0 hits.
    - Listing PRs in all states (1,000 listed, up to #1073) shows no title on this target.
    - The bank page known-unknowns/disease-research/german-hospitalization-nowcast-hub-beat-ensemble-wis.md says
      "open as of 2026-10-15" and defines p3 as "A reproduction of the hub's published evaluation".

## Reasoning

What is the object? p3 asks for a reproduction. Its "result" is a recomputation that matches the published numbers,
so a tie on the numbers is the goal, not a defect. The novelty question therefore has two parts: (a) is an equivalent
independent recomputation of the published per-model WIS (Fig 7 / wis_*.csv) already public, and (b) does this one
add, beyond the authors' own released code, what the bank asks for?

(a) Prior reproductions: none found.
- Every source I could reach was checked: citing literature through Europe PMC (28) and OpenAlex (29, which covers
  arXiv and medRxiv), keyword literature searches over the last 24 months, Zenodo, GitHub repository and code search,
  the hub's forks and issues, the evaluation repositories (0 forks, 0 issues, no releases), and the V3R1T4S trophy
  case, known-knowns, PRs and issues. None contains a third-party recomputation of the 31 published cells.
- The closest neighbours are different cells. Amaral et al. 2025 (same author group) use a 40-day target and a period
  from 8 Feb 2022 (parallel to Fig 13). Johnson et al. 2025 regenerate the KIT model's nowcasts. The Medium-Blog
  analysis is national-only and uses bias, MAE and coverage, not WIS.
- The only object that reproduces the published table is the authors' own pipeline. It is the original evaluation,
  not a reproduction. If it counted, p3 would have been met when the bank entry was written.

(b) Additions beyond the authors' released material. The claim is openly seeded from that material, and CLAIM.md
names it. Simply running or porting the authors' R code on their own assembly would give the 31 numbers and nothing
else. The claim adds:
- A second, independent implementation of WIS and of the four repairs. The Epiforecasts normal fit is solved in closed
  form instead of with rriskDistributions, and the resulting +1.0e-4 / +1.3e-5 / +6.7e-7 residuals are explained.
- A per-cell ladder quantifying each rule: without the rules, 6 of 31 cells miss by more than 1% (up to +11.1%) or
  are undefined. Neither the paper nor the S1 Appendix publishes this.
- The truth series re-derived from the hub's own truth file at the pinned commit, with max |diff| 0 against the
  authors' truth file.
- The FrozenBaseline rebuilt from the hub's raw triangle: 106,053 of 106,053 targets equal.
- A row-by-row provenance check of the authors' assembly against 189 hub files (all 159 MeanEnsemble dates plus 30
  sampled files of other models), with 0 mismatches.

None of this is public elsewhere. On novelty, then, the record is new and not a trivial edit of a published object.

Caveats for the panel. These do not make the claim old, but they limit how independent it is and bear on whether
"every discrepancy" is documented. The criterion skeptic should weigh them.
- **Inputs are the authors' intermediates, only sample-checked.** Submissions enter through the authors' own
  assembly, `submissions.csv.gz`, not straight from data-processed. Only 189 files are checked against the hub, so
  10 of the 11 models are verified on a sample only. The exclusion keys are also the authors' lists
  (claim/data/eval_data/submission_check_fixed_*-missing.csv), consumed as given rather than re-derived from
  data-processed.
- **The rules are not new, only their check.** The authors already describe the exclusion and repair rules in S1
  Appendix Tables A3 and A4. What the claim adds is their independent confirmation and quantification, not their
  discovery.
- **Unexplained paper-vs-release mismatch: excluded targets.** CLAIM.md does not explain how the paper's text and the
  released data and code differ:
  - The authors' lists hold 4,376 keys, which is 547 targets × 8 rows (7 quantiles + mean). Table A3 states 394
    targets.
  - The lists include forecast date 2022-02-08, which Table A3's dates (22-24 Nov 2021, 31 Jan and 1 Feb 2022) do
    not mention. I counted this from claim/data/eval_data.
- **Unexplained paper-vs-code mismatch: RKI repair.** Table A4 says values above 1 billion were replaced by the -1-day
  nowcast. The rule the claim re-implements is "> 1e6 or NA, replaced by the minimum of the 0- and -1-day values".

pass: true
