context: subagent

# NOVELTY verdict — polaris/pkis2-lok-slk-c-1, claimed CLASS_LOK pr_auc 0.634333770922

## 1. The one honest fetch of the primary table page

- URL: https://polarishub.io/benchmarks/polaris/pkis2-lok-slk-c-1
- Method: exactly one plain `curl.exe` request, no retries, no cookies, single attempt, `User-Agent: V3R1T4S/1.0 (novelty skeptic; open research)`
- Fetch time (UTC): request start 2026-11-18T16:58:43Z, response complete 2026-11-18T16:58:44Z
- HTTP status: **200**; 186443 bytes; final URL equal to the requested URL (no redirect); no block, no challenge page
- Page sha256 of my fetch: a1da2c1c64e5241f5910166883ee2ed478f9028b7ceafe83d289ffd9722b5eaf. The claim folder records a different hash (5671da87…5b58fbc…, exact string 5671da872b25a3afad11552ace4f0301c3f5afa3db0ac23f45868c9cdddb58fbc) for its own 2026-11-18T16:04:25Z fetch at the identical byte size (186443) with identical leaderboard values — consistent with volatile same-length tokens in the page payload (e.g. an embedded timestamp) rather than a table change. The one-fetch rule stopped me from re-fetching to compare; this is recorded, not resolved.

Every leaderboard pr_auc value read from the fetched page (the page embeds one results table per target):

CLASS_LOK (the claimed metric; the default leaderboard view):
| entry | pr_auc | roc_auc |
|---|---|---|
| pkis2-lok-slk-c-1_DGLGraphTransformer_PNAModel | 0.2553191489361702 | 0.6759259259259259 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_MPNNModel | 0.18181818181818182 | 0.5 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_GCNModel | 0.18181818181818182 | 0.5 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_GATModel | 0.18181818181818182 | 0.5 |
| pkis2-lok-slk-c-1_pharm2D_FCModel | 0.18181818181818182 | 0.5 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_AttentiveFPModel | 0.17394416607015034 | 0.4722222222222222 |

CLASS_SLK (the second target's table on the same page):
| entry | pr_auc |
|---|---|
| pkis2-lok-slk-c-1_DGLGraphTransformer_GCNModel | 0.11926605504587157 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_MPNNModel | 0.1148018648018648 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_PNAModel | 0.10317460317460317 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_GATModel | 0.1 |
| pkis2-lok-slk-c-1_pharm2D_FCModel | 0.09848484848484848 |
| pkis2-lok-slk-c-1_DGLGraphTransformer_AttentiveFPModel | 0.09848484848484848 |

- Board NOT empty: six entries, all Polaris "baseline null model" submissions dated 2023-12-08 (the hub's indexed result pages confirm the date and tag; four of the six are constant all-positive predictors, pr_auc = 24/132 = 0.18181818181818182 for CLASS_LOK, which the claim's baseline folder reproduces exactly).
- Comparison: claimed CLASS_LOK pr_auc **0.634333770922** vs best listed **0.2553191489361702** → strictly better by +0.37901462198583 (margin rule ≥ 0.020 absolute for PR-AUC: cleared). The claim's CLASS_SLK 0.377856659137 also beats the best listed CLASS_SLK 0.11926605504587157, and its two-target mean 0.506095215029 beats every listed entry's two-target mean (best listed mean ≈ 0.179).
- One documentation discrepancy, recorded for honesty: the claim's secondary per-entry table (parsed from the individual result pages) attributes CLASS_SLK values differently (its GCN 0.09848484848484848, GAT 0.09848484848484848, pharm2D 0.1) from what the main page I fetched shows (GCN 0.11926605504587157, GAT 0.1, pharm2D 0.09848484848484848). Under either attribution the claimed values clear the whole table, and the CLASS_LOK values — the metric the claim is made on — match the claim's table entry-for-entry, so the record comparison is unaffected.

## 2. What I searched and what I found (last 24 months, Nov 2024 – Nov 2026)

Exact-cell searches:
- Exact slug "pkis2-lok-slk-c-1" (web search): only polarishub.io pages and the V3R1T4S target-definition page known-unknowns/drug-discovery/polaris-pkis2-kinase-small-leaderboards.md. No paper, preprint, code repository, Zenodo record, forum or blog post reports a result on this cell.
- Dataset slugs "kinase-pkis2-1" / "drewry2017-pkis2-subset": only the hub's dataset/benchmark pages and the polaris-recipes curation notebook (data construction only, no results).
- GitHub issue + pull-request search over the V3R1T4S repository for "pkis2": total_count 0 — no open or closed PR carrying a prior or competing claim on this cell.

Kinase-wide / foundation models that could trivially report this cell:
- CheMeleon (descriptor-pretrained D-MPNN; arXiv 2506.15792 v2 Feb 2026; JCIM Aug 2026; repo JacksonBurns/chemeleon; weights on Zenodo): evaluates 28 Polaris/TDC + 29 MoleculeACE = 58 benchmarks. Its pkis2 coverage is kit-wt-cls-v2 (its hub entry holds PR-AUC 0.646), kit-wt-reg-v2, egfr-wt-reg-v2, ret-wt-cls-v2, ret-wt-reg-v2; its supplementary figure sorted by training size lists the 524- and 496-train pkis2 cells and no 508-train cell, and no CheMeleon entry exists on either lok-slk classification cell. It publishes no number for this cell.
- KIPP / large-scale kinase-profiling ML comparison (J Cheminformatics, Jan 2024): outside the 24-month window, and uses its own ChEMBL-derived KinaseNet data, not this cell.
- Pharmacophore-driven kinase profiling of PKIS2 (Sci Rep 16:12083, Mar 2026): unsupervised pharmacophore mining with a different label definition (≥ 50% inhibition), no official split, no pr_auc on this cell.
- No Polaris competition covers pkis2 (the hub's competition is the unrelated ASAP Discovery/OpenADMET antiviral one).

Neighbouring cells:
- pkis2-lok-slk-cls-v2 (the v2 classification twin; threshold > 80; 508 train / 132 test; dataset drewry2017-pkis2-subset-v2): leaderboard EMPTY ("No results", "No participants yet"). Irrelevant to the empty-board trap — the claimed cell's own board is not empty.
- pkis2-lok-slk-r-1 (the regression sibling on the same dataset kinase-pkis2-1, same 508/132 split): seven entries. Best is "aether-pharmaos-pkis2-lok-slk-ensemble" (contributor vidraft), submitted June 19, 2026 — LOK MAE 20.934, Spearman 0.620, Pearson 0.610; SLK MAE 20.406. It publishes no classification value and carries no links, code or prediction file ("No links found", "No references provided"), so a rank-propagation to a CLASS_LOK pr_auc is plausible but neither published nor computable from public assets. This is the closest neighbouring-cell object; it yields no known number for this cell.
- Other pkis2 cells (KIT PR-AUC 0.646 by CheMeleon; RET PR-AUC 0.885 by a MolGPS model; EGFR regression by the same aether-pharmaos submitter): different kinases and different splits; nothing published transfers them to the LOK/SLK cell.

Repository checks (read-only):
- TROPHY_CASE.md: 53 rows in seven families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench, cipher commitments) — no PKIS2/Polaris family, so no prior internal claim for this cell.
- known-knowns/: 38 family directories, none pkis2/polaris-kinase.
- Local git copy pinned at the "2026-11-17b" merges (commit 267887d, shallow clone).
- GitHub releases of the repo: none at all (API returned []), so no release assets can lag the tree.
- The bank entry (targets.json id polaris-pkis2-kinase-small-leaderboards) matches the claim's quoted success criterion verbatim, including the non-empty-board requirement.

Search limitation, recorded honestly: the arXiv API (export.arxiv.org) returned HTTP 429 on my query for "PKIS2"; literature coverage was completed instead through multiple web searches that surfaced and read the relevant arXiv/JCIM/Research Square content (CheMeleon v1/v2, the PKIS2 pharmacophore paper, the tabular-foundation-model paper). Neither route found any source reporting this cell.

## 3. Trivial-edit / seeded-object analysis

- The only published objects for this cell are the six 2023-12-08 null-model leaderboard entries; four are constant all-positive predictors (pr_auc exactly the 24/132 prevalence). No deletion, restriction, relabelling, propagation rule, symmetry or local numerical polish of a constant predictor yields 0.634333770922.
- The claimed object (pipeline E2 in the claim folder: ECFP4 + physchem features; ExtraTrees regressor on the continuous LOK train labels rank-blended with a LightGBM classifier on the class labels; Platt map on out-of-fold blend scores; fitted only on the 508 official train rows) is not seeded from any published object: the six entries publish no code, predictions or weights ("No links found", "No references provided" on all six), so there was nothing on this cell to seed from, and the claim names the only published objects it touches (the null models, used for harness calibration and reproduced exactly).
- Neighbouring cells give nothing that trivially beats 0.634333770922 here: the v2 twin is empty; CheMeleon's 0.646 is on the KIT cell (different kinase, different split) with no published lok-slk number; the June 2026 vidraft regression entry publishes no classification number and no predictions, so no known value arises from it. The claimed value is not reachable by trivial edits of anything published for the cell or its neighbours.

## 4. Verdict

The claimed CLASS_LOK pr_auc 0.634333770922 on polaris/pkis2-lok-slk-c-1 strictly beats everything known for the cell: the best live listed value 0.2553191489361702 (my own single fetch, HTTP 200, 2026-11-18T16:58:43Z), every other listed value in either target's table, and everything found in a 24-month sweep of literature, code, hub entries, competitions, the repo's trophy case, known-knowns, pull requests and releases. The board is not empty, no result ties the claimed value, and the object is neither a trivial edit of nor an undisclosed seed from any published object.

pass: true
