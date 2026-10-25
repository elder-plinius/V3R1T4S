# The Record We Beat (`immrep22-tcr-epitope-microauc`)

## 1. Official IMMREP22 Benchmark Tables & Upstream Evaluation Files (`viragbioinfo/IMMREP_2022_TCRSpecificity`, commit `8942484a902a4694628f0e4f828012884f76382e`)

- **Task 1 Per-Epitope Micro-AUC Table (`microaucs.csv`):**
  - **URL:** `https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/8942484a902a4694628f0e4f828012884f76382e/evaluation/microaucs.csv`
  - **UTC fetch timestamp:** `2026-10-19T18:10:02Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `8,251` bytes
  - **SHA-256:** `28321870009bf2f122907da498ed912d227d8ad74b6f92d37d9ddfb9d043bec5`
  - **Saved Copy:** `the-record-we-beat/microaucs.csv`
  - **Listed Best `_Average` Micro-AUC Across 22 Methods:** `tcrexab = 0.8473470238751809` (followed by `TCRGP = 0.8467607945819052`, `tcrdist3 = 0.8403439378009127`, `tcrexb = 0.830092968051042`, `netTCR_cdr123ab = 0.8245956792087137`).
  - **Listed Best Single-Epitope `SPRWYFYYL` Micro-AUC Across 22 Methods:** `tcrexb = 0.837823275862069` (`tcrexab = 0.811242816091954`).

- **Task 2 Epitope Ranking Table (`epitoperank.csv`):**
  - **URL:** `https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/8942484a902a4694628f0e4f828012884f76382e/evaluation/epitoperank.csv`
  - **UTC fetch timestamp:** `2026-10-19T18:10:02Z`
  - **HTTP status:** `HTTP/2 200`
  - **Byte size:** `4,788` bytes
  - **SHA-256:** `286e0acde8a47fd0197ff1a4d4b0715fab8869c7b51374df3ecd1a406381c2f8`
  - **Saved Copy:** `the-record-we-beat/epitoperank.csv`
  - **Listed Best `_Average` Rank (Lower Is Better):** `tcrexab = 3.284288528900479` (followed by `tcrexb = 3.441607098550225`, `TCRGP = 3.490134138809314`).

- **Official Evaluation Script (`evaluate.py`) & Test Labels (`true_set/`) — Fetched & SHA-256 Verified by Checker (Not Vendored):**
  - Per `kit/SUBMIT.md` §1 (packages carry no third-party code/data), `verify-it-yourself/check_immrep22_clss.py` fetches the official `evaluate.py` and the 18 ground-truth files in `true_set/` directly from `https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/8942484a902a4694628f0e4f828012884f76382e/` and stops immediately on any SHA-256 mismatch:
    - `evaluation/evaluate.py` (`5,115` bytes, `sha256: 04fa0346aa914bab770f9adbd6326581026e0fa9b94ad734f3957c54be6778ed`)
    - `true_set/ATDALMTGF.txt` (`sha256: cedb80926ea3a0012a012c4f77685cb7d0c458470fad760f04b504895131880d`)
    - `true_set/CINGVCWTV.txt` (`sha256: ad8276318a14329eaf7fadcf77bf792927dc534a008082247c555d2991376352`)
    - `true_set/GILGFVFTL.txt` (`sha256: d54fedacebc087d0625418bdbd302590a5c3605267c7cdae8138040940c3608b`)
    - `true_set/GLCTLVAML.txt` (`sha256: 963c312643e9159c5e37ecdb808553d1eddc46c0eb5258571d8783362b19ebbc`)
    - `true_set/GPRLGVRAT.txt` (`sha256: 0f4ae81a55505dbd08321ed0daebeb50600b084e81194aa56caa9e956c5c0c19`)
    - `true_set/HPVTKYIM.txt` (`sha256: d6014823884c857882e5de3f3be3213402a02668bf6fa7d4953e7274476d8550`)
    - `true_set/KSKRTPMGF.txt` (`sha256: 8f19bcc4c3bea0c837edfd24818718a475f45f71ec222d8c17c080defc0794ab`)
    - `true_set/LLWNGPMAV.txt` (`sha256: bf2d9483091b8736b58b7137cd1cf12c086aaeb8af0a56829e8b128d08f0ccc7`)
    - `true_set/LTDEMIAQY.txt` (`sha256: 292028092f646b70e40c256381d031ca40601b256c6b0cffc52a342375fcd09b`)
    - `true_set/NLVPMVATV.txt` (`sha256: 7c6770bac58797b8c52c72b839234da6a098065669ead4d13acd53dc8c4121e7`)
    - `true_set/NQKLIANQF.txt` (`sha256: b5ae367a2d0f81d7ca21f25752fd59f14e2d182e949e19a0294f10093f30544f`)
    - `true_set/NYNYLYRLF.txt` (`sha256: 61de1eab0332e478ab7383b8cdb13132f7289740bf847176f75ec0bd180bd97c`)
    - `true_set/RAQAPPPSW.txt` (`sha256: 21eb50d21d3b1346c3828ba4898e6a04b47545a9e4ec2d91cc7069cc7fb9748e`)
    - `true_set/SPRWYFYYL.txt` (`sha256: 9087ceecff877b4807c9a6148900809ec9298835f011ea280c364f38a12f95a2`)
    - `true_set/TPRVTGGGAM.txt` (`sha256: 592dd30acc84ce7ebb1438a84aba04a773e6eee284fa7c412b6e379bacb40c8e`)
    - `true_set/TTDPSFLGRY.txt` (`sha256: d780fca7ec8c782c7f7e9f64de19f2fd2e3de1a70e5c773a93d91c26551f5a27`)
    - `true_set/YLQPRTFLL.txt` (`sha256: a7b70a8855715af3b23f2f73e74a32f919c03415f66047b74ce2e6b45cdea707`)
    - `true_set/testSet_Global.txt` (`sha256: 62b21160586f1cefb7b23710f0977a91f24f1f1e66d8fc7d41b0ad0f10cf22a0`)

## 2. Recent Literature (2023–2026)

- **Meysman et al. (*ImmunoInformatics* 10, 100024, 2023, DOI `10.1016/j.immuno.2023.100024`):** Official IMMREP22 workshop benchmark report (best `_Average` MicroAUC `0.847347` by `tcrexab`).
- **Recent 2026 bioRxiv Preprint (Oct 13, 2026, DOI `10.64898/2026.10.13.758726`):** Reports mean micro-AUC `0.8394` on the 17 IMMREP22 epitopes using ESM2 protein language model embeddings and paired chains, below both `tcrexab` (`0.847347`) and our `clss_tcr` (`0.882173`).
