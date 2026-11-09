# Honesty gate: LW1, partial win p2 (massbalancemachine-norway-test-glaciers-rmse), run 2026-11-07-2047

Read by the run's main session, 2026-11-07T21:13:00Z: novelty.md (pass: true, new this run), reproduce.md (pass: true) and criterion.md
(pass: true). The last two are carried unchanged from runs/2026-11-07-1740/panel/ (sha256 f20ba968... and 7e2ae31f...),
as PREREG.md Part B fixed in advance: the claim folder here is byte-identical to that run's claim/ (44 files, sha256 lists in
attempts/vdm-read/), plus claim/table/related/ with the local van der Meer et al. 2026 text. Each of the three files was
written by its own fresh subagent context: two in the 17:40 run, one (claude-opus-5-5) in this run.

Why a new NOVELTY file: the 17:40 NOVELTY skeptic passed with one stated open gap, van der Meer et al. 2026, unread then.
A local copy of the paper's full text (sha256 a88f20daf53f6cf2ab61681dcfbc301675ea7398f292d791e2c606d14ae3dd04) was read in place of a web fetch.

Checked against the downgrade list (kit/RUN.md step 7):
- Hedging: none on p2. The skeptic read the paper text in full, confirms it has no Norway experiment (8 Swiss test
  glaciers, 471 annual and 1,707 winter points) and no model of at most 20 parameters. Its residual risk (the Transformers
  preprint, unread) concerns many-parameter models, so it bears on p1 and the main criterion, not on p2.
- Value against the table: MBM Bw 0.59 (0.5881 reproduced), status page fetched 20:48:55Z (scout.md) and 20:54:46Z (skeptic),
  commitCount 403, no newer result; both fetches are under 6 hours old. The skeptic also found every other published
  winter RMSE for these glaciers (GloGEM 0.65, OGGM 0.82, PyGEM 0.87, MBM 0.55, all on the 517-point subset) above 0.5239.
- Scope: confirmed_scope below is the CRITERION skeptic's sentence, unchanged; it claims Bw only.
- Reproduction: unchanged object; the new skeptic's own csv-and-math scorer gives RMSE 0.523911 on 999 points.
- Zenodo record 18267624 metadata (title, date, file list) was also returned at 20:58:46Z, HTTP 200; no archive was
  downloaded and none of it was used.
- The skeptic corrects two details of the contributor's summary: the quoted Norway figures 0.55 / 0.97 are Sjursen et al.'s
  1980-2019 subset values, and the paper's "ongoing work" is transfer learning that draws on Alpine and Scandinavian data,
  not transfer to Scandinavia as such. Neither changes the conclusion.
- No status was upgraded: p2 was confirmed in runs/2026-11-07-1740 and stays at that level.

status: CONFIRMED_PARTIAL
confirmed_scope: A linear winter model with 3 fitted parameters (monthly solid precipitation and its product with the altitude difference, summed over Oct-Apr), fitted by least squares on the 18 training glaciers' 2752 winter point balances only, structure chosen by glacier-grouped 6-fold cross-validation, with a fixed 0.0065 K/m lapse rate and a fixed 1.0 C snow threshold, has Bw RMSE 0.5239 m w.e. over all 999 winter point balances of the 14 test glaciers, which meets partial win p2 (at most 20 fitted parameters, test Bw RMSE at most 0.59); it makes no claim on annual or summer balances, p1 or the main criterion.
