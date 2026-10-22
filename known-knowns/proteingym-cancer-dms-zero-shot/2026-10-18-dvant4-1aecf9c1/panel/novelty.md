# Novelty skeptic report: proteingym-cancer-dms-zero-shot / PTEN_HUMAN_Matreyek_2021

context: subagent (Claude Code Agent, fresh context)

## 1. Status source (fetched once, no retries)
- URL: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
- Fetch time (UTC, `date -u` just before the request): 2026-10-18T19:29:11Z
- HTTP status: 200; 141,235 bytes; sha256 f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437 (same bytes as the author's 18:46:05Z fetch in SCOUT_RECORD.md)
- User-Agent: V3R1T4S-research-agent, one plain curl request
- Row PTEN_HUMAN_Matreyek_2021 (metadata: 5083 mutants, Selection Type Expression, UniProt PTEN_HUMAN, MSA_Neff_L_category Medium, Taxon Human)
- 97 numeric model columns after excluding the metadata columns. Top values:
  VenusREM 0.516; ProSST (K=1024) 0.514; ESCOTT 0.505; ProSST (K=512) 0.504; SaProt (650M) 0.499
- Maximum over model columns: **0.516 (VenusREM)**
- Claim: 0.5658. Margin = 0.5658 - 0.516 = **+0.0498**, which meets the required >= 0.015 and strictly beats the maximum (not a tie).
- Scope note: this report checks novelty only. It takes the claimed Spearman of 0.5658 as given. Recomputing it and checking for leakage is the other panel members' job.

## 2. Repo results (elder-plinius/V3R1T4S)
- TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md, fetched 2026-10-18T19:29:12Z, HTTP 200, 31,235 bytes. No line mentions "ProteinGym", "PTEN", "protein" or "DMS".
- Pull requests: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1..5, fetched 2026-10-18T19:29:12Z to 19:29:14Z, HTTP 200 on all 5 pages. That is 446 PRs; page 5 was partial (46 PRs), so the list is complete.
  - No PR title or body contains "proteingym", "proteingym-cancer-dms-zero-shot", "PTEN", "Matreyek", "VenusREM", "DMS" or "Spearman".
  - The only hit on the broader keywords was #360 (open), claim(ab-offlattice-protein-3d-best-energies). It is a lattice-protein energy target and unrelated.
  - No competing or prior claim on this target.

## 3. Literature, last 24 months (Oct 2024 to Oct 2026)
Searches: PTEN_HUMAN_Matreyek_2021 zero-shot Spearman; ProteinGym zero-shot ensemble PTEN 2025; proteingym.org leaderboard 2026; PTEN VAMP-seq predictor Spearman; VenusREM/ProSST/ESCOTT ensemble per-assay PTEN.
No published zero-shot Spearman >= 0.5658 on PTEN_HUMAN_Matreyek_2021 was found, and no published ensemble reporting that value. Sources checked:
- Sharma & Gitter 2025, structure-based zero-shot fitness prediction (finds simple multi-modal ensembles are strong baselines; reports aggregates only, no PTEN breakdown found): https://arxiv.org/abs/2504.16886
- Multi-Scale Representation Learning for Protein Fitness Prediction (S3F; its scores are already a column in the table): https://arxiv.org/pdf/2412.01108
- Metalic, meta-learning in-context with PLMs: https://arxiv.org/pdf/2410.08355
- Scaling and Data Saturation in PLMs (AMPLIFY, 2025): https://arxiv.org/pdf/2507.22210
- Matrix VAE (2025): https://arxiv.org/html/2507.02624v1
- arXiv 2506.14793: https://web3.arxiv.org/pdf/2506.14793
- VenusREM (ISMB/ECCB 2025, Bioinformatics; its score is the current max of 0.516): https://hyper.ai/de/news/54275
- VespaG (bioRxiv 2024): https://biorxiv.org/cgi/content/short/2024.04.24.590982v1
- Notin, "Have we hit the scaling wall for PLMs?": https://pascalnotin.substack.com/p/have-we-hit-the-scaling-wall-for
- ProteinGym repo and leaderboard: https://github.com/OATML-Markslab/ProteinGym ; https://proteingym.org (not fetched directly; the per-assay values come from the CSV above)
- Assay source, Matreyek et al. 2021, Genome Medicine: https://genomemedicine.biomedcentral.com/track/pdf/10.1186/s13073-021-00984-x
- Aggregator mentions of a "ProteinGym Hard" subset (an LLM-agent score, a different metric, not per-assay DMS Spearman; not relevant): https://benchmarklist.com/benchmarks/proteingym_hard/

Caveat: the web search covers a limited index. Per-assay results are rarely printed in papers, so the live ProteinGym CSV is the authoritative record. It was last pushed 2026-03-25 according to SCOUT_RECORD.md.

## Verdict
The claim's 0.5658 strictly beats the live per-assay maximum of 0.516 (VenusREM) by 0.0498, which is at least the 0.015 margin. No prior or competing result turned up in TROPHY_CASE.md, the 446 repo PRs or the literature searched. Novelty passes, provided the other panel members confirm the 0.5658.

pass: true
