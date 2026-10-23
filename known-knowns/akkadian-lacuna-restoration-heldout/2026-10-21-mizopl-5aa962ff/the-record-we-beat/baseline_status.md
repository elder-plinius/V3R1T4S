# Primary Record & Baseline Status — `akkadian-lacuna-restoration-heldout`

1. **Primary Repository (`SLAB-NLP/Akk`)**:
   - **Commits API URL**: `https://api.github.com/repos/SLAB-NLP/Akk/commits?per_page=5`
   - **Fetched UTC**: `2026-10-21T17:42:43Z`
   - **HTTP Status / Bytes / SHA-256**: `200`, `19,370` bytes, `sha256: 1a5c35964d3a24f560943a4ca4767c17037caab500bc5bb190136bd5804d0b9a`
   - **Latest Commit**: `dfd2a66d4305cf36981e4fd3fde823a5020161dd` (`2022-11-10T08:27:40Z`)
   - **Corpus (`data/akk_from_jsons.jsonl`)**: `21,156,545` bytes, `sha256: b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3`

2. **Primary Benchmark Paper (Lazar et al., EMNLP 2021)**:
   - **ACL Anthology PDF URL**: `https://aclanthology.org/2021.emnlp-main.384.pdf`
   - **Fetched UTC**: `2026-10-21T17:44:40Z`
   - **HTTP Status / Bytes / SHA-256**: `200`, `913,597` bytes, `sha256: 68a75ea83a5654f642a0b2cd610cf296b0612c2f84eead2649d538b3f13f427e`
   - **arXiv API URL**: `https://export.arxiv.org/api/query?id_list=2109.04513` (`2026-10-21T17:42:57Z`, `2,700` bytes, `sha256: d28c6c615ba67a65df83a8054a57c5fade90a3fb3ef2b4dec4866a6217f37a00`)
   - **Published Benchmark Values (`MBERT+Akk`, Signs, Table 1 & Abstract)**:
     * `MRR = 0.83`
     * `Hit@5 = 0.89` (`89.5%` in Abstract / Section 1)
     * `Hit@10 = 0.92`
   - **Published Per-Genre Values (`MBERT+Akk`, Signs, Table 2 `MRR / Hit@5`)**:
     * `Royal Inscription`: `0.83 / 0.90`
     * `Royal or Monumental`: `0.84 / 0.90`
     * `Astrological Report`: `0.81 / 0.88`
     * `Lexical`: `0.69 / 0.85`
     * `Decree`: `0.71 / 0.76`
