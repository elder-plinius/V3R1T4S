# The Record We Beat (`immrep22-tcr-epitope-microauc`)

## 1. Official IMMREP22 Benchmark Tables (`MortimerLab/immrep22`, commit `8942484a902a4694628f0e4f828012884f76382e`)

- **Task 1 Per-Epitope Micro-AUC Table (`microaucs.csv`):**
  - **URL:** https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/microaucs.csv
  - **UTC fetch timestamp:** `2026-10-19T18:10:02Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `7,940` bytes
  - **SHA-256:** `28321870009bf2f122907da498ed912d227d8ad74b6f92d37d9ddfb9d043bec5`
  - **Saved Copy:** `the-record-we-beat/microaucs.csv`
  - **Listed Best `_Average` Micro-AUC Across 22 Methods:** `tcrexab = 0.8473470238751809` (followed by `netTCR_cdr123ab = 0.838462605658958`, `tcrmatch_ab = 0.8342433915091846`, `tcrexb = 0.8338411867855644`, `TCRGP = 0.8229747412277399`).
  - **Listed Best Single-Epitope `SPRWYFYYL` Micro-AUC Across 22 Methods:** `tcrexb = 0.837823275862069` (`tcrexab = 0.811242816091954`).

- **Task 2 Epitope Ranking Table (`epitoperank.csv`):**
  - **URL:** https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/epitoperank.csv
  - **UTC fetch timestamp:** `2026-10-19T18:10:02Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `2,462` bytes
  - **SHA-256:** `286e0acde8a47fd0197ff1a4d4b0715fab8869c7b51374df3ecd1a406381c2f8`
  - **Saved Copy:** `the-record-we-beat/epitoperank.csv`
  - **Listed Best `_Average` Rank (Lower Is Better):** `tcrexab = 3.284288528900479` (followed by `tcrexb = 3.441607098550225`, `tcrmatch_ab = 3.4888164301872507`).

- **Official Evaluation Script (`evaluate.py`):**
  - **URL:** https://raw.githubusercontent.com/MortimerLab/immrep22/main/evaluation/evaluate.py
  - **UTC fetch timestamp:** `2026-10-19T18:10:02Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `6,120` bytes
  - **SHA-256:** `04fa0346aa914bab770f9adbd6326581026e0fa9b94ad734f3957c54be6778ed`
  - **Saved Copy:** `the-record-we-beat/evaluate.py`
  - **Official Test Labels:** `the-record-we-beat/true_set_labels/{epitope}.txt` (the 17 official test label tables extracted from `MortimerLab/immrep22/true_set/`).

## 2. Recent Literature (2023–2026)

- **Meysman et al. (*ImmunoInformatics* 10, 100024, 2023, DOI `10.1016/j.iminfo.2023.100024`):** Official IMMREP22 workshop benchmark report (best `_Average` MicroAUC `0.847347` by `tcrexab`).
- **Recent 2026 bioRxiv Preprint (Oct 13, 2026, DOI `10.64898/2026.10.13.758726`):** Reports mean micro-AUC `0.8394` on the 17 IMMREP22 epitopes using ESM2 protein language model embeddings and paired chains, below both `tcrexab` (`0.847347`) and our `clss_tcr` (`0.882173`).
