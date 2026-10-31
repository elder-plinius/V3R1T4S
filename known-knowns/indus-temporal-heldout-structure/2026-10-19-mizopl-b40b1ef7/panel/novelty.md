# Skeptic Panel Report — Role: NOVELTY (`indus-temporal-heldout-structure`)

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: indus-temporal-heldout-structure
category: undeciphered-scripts
claim_type: partial_win
partial_win: p3
evaluated_utc: 2026-10-19T20:34:50Z

---

## 1. Mandate & Isolation Verification

Per V3R1T4S `kit/RUN.md` Step 6 (`NOVELTY`):
> "Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

- **Isolation compliance**: This review read only the package artifacts (`README.md`, `RUN_IT_YOURSELF.md`, `object/post1977_evaluation_results.json`, `object/m77_frozen_structural_model.json`, and the upstream `paragorth/Indus-` preregistration files `prereg/preregistration-frozen.json`, `prereg/preregistration-2-frozen.json`, `prereg/preregistration-3-frozen.json`, `prereg/preregistration-4-credential.json`, and `prereg/preregistration-5-minimumlot.json`) and live external HTTP endpoints fetched via single-request `curl` calls.
- **Claimed structural finding summary** (`object/post1977_evaluation_results.json`, `23,213` bytes, `sha256: b47ae1616f5af9464528572141712a350a62b0659ad38c4a7a8013339c1164fb`, evaluated at `2026-10-19T20:21:11Z` from `object/m77_frozen_structural_model.json`, `359,340` bytes, `sha256: b40b1ef7b100e944aa1d86efa3b8f7dbdfbcd15885ab785e25e7e7454b1451a3`, frozen at `2026-10-19T19:48:10Z`):
  1. **Strict Chronological Split (`M77` vs Post-1977 Held-Out)**: Trained strictly on `2,165` unique sequences (`9,652` tokens) from Iravatham Mahadevan's 1977 concordance (`data/im77/im77_corpus_lines.csv`, `559,170` bytes, `sha256: 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211`, mapped via `data/derived/bridge_extended.json`, `2,070` bytes, `sha256: ba0949e1e2dd8e9b5d6d3aea70da5ad3c1d213e76a8bbd38d993814068d7541c` from `https://github.com/paragorth/Indus-` commit `d62ec82d58642038640da25a97177d7a1fddc9d9`) and evaluated without refitting on `999` deduplicated post-1977 inscriptions (`3,731` masked tokens in `object/post1977_heldout_predictions.csv`) from `data/derived/merged-corpus-canonical.v2.json` (`2,315,998` bytes, `sha256: b68c950bee1b7ded02267c0717b5e7e5d8730b7f72de6f46d4dea086ac9e7a5f`) after excluding all `1,785` `data/derived/dark/loop24_pairs.json` alignments (`1,919,320` bytes, `sha256: 638027b53fdffc4b915cb61aa683326cd1c312b5018eac65c9c8b11e1f2efed2`), `951` exact sequence matches to `M77` (forward or reverse), and `92 + 384` recurring seal impressions via `data/derived/identity-directory.json` (`82,012` bytes, `sha256: fd5d42b65ec96ff248bbce3ffee4352bab452ff5faa8e4e4084c87a76932c03f`).
  2. **Surviving Preregistered Claim — Partial Win `p3` (Telescoping Composite/Bigram Parallel Frames on Post-1977 Held-Out Set)**: Across the Top-25 single-sign vs two-sign bigram substitution pairs frozen from `M77` (`frozen_m77_top25_telescoping_ligatures_p3`), `19 / 25` pairs are active in the post-1977 held-out set and share **`30` exact flanking frames `(l_1, r_1)`**, compared to a `10,000`-permutation frequency-matched null mean of `7.6427` (SD `3.1291`, max `23`, `0 / 10,000` permutations at least `30`, `p = 0.000100 < 0.001`).
  3. **Pooled & Site-Stratified Held-Out Masked-Sign Top-1 Restoration**:
     - **Cohort A Mode 1 (`3,731` tokens across `999` post-1977 inscriptions)**: `M77-CLSS` achieves **`20.0482%` (`748 / 3,731`)**, vs `KN3-Left` (`14.7146%`, `549`, `p = 0.000100`), `KN3-Bidir` (`18.8957%`, `705`, `p = 0.000100`), `KN3-BlanketF` (`19.4586%`, `726`, `p = 0.004800`), and `SIGIL` (`9.3809%`, `350`, `p = 0.000100`), as well as all `400` independent `SIGIL` synthetic null controls (median `8.8984%`, IQR `0.2948%`, best of 400 controls `9.6221%`, `z = +47.86` SD).
     - **Site-Stratified Mode 1**:
       * **Mohenjo-daro (`1,041` tokens)**: `M77-CLSS = 20.9414%` (`218`) vs `KN3-Left = 15.4659%` (`161`, `p = 0.000100`), vs `KN3-Bidir = 19.5005%` (`203`, `p = 0.001900`), vs `KN3-BlanketF = 20.6532%` (`215`, `p = 0.298770`), and vs `SIGIL = 9.8943%` (`103`, `p = 0.000100`).
       * **Harappa (`1,593` tokens)**: `M77-CLSS = 21.2806%` (`339`) vs `KN3-Left = 15.5053%` (`247`, `p = 0.000100`), vs `KN3-Bidir = 20.2134%` (`322`, `p = 0.014699`), vs `KN3-BlanketF = 20.5901%` (`328`, `p = 0.018798`), and vs `SIGIL = 10.1067%` (`161`, `p = 0.000100`).
       * **Dholavira (`414` tokens, post-1990 ASI excavations)**: `M77-CLSS = 16.1836%` (`67`) vs `KN3-Left = 11.5942%` (`48`, `p = 0.000100`), vs `KN3-Bidir = 15.4589%` (`64`, `p = 0.245175`), vs `KN3-BlanketF = 15.7005%` (`65`, `p = 0.369563`), and vs `SIGIL = 7.2464%` (`30`, `p = 0.000100`).
     - **Cohort A Mode 2 Connected-Component Equivalence Classes (`3,731` tokens)**: `M77-CLSS = 22.6749%` (`846`) vs `KN3-Left = 16.0547%` (`599`, `p = 0.000100`), vs `KN3-Bidir = 21.6028%` (`806`, `p = 0.000500`), vs `KN3-BlanketF = 21.9512%` (`819`, `p = 0.001200`), and vs `SIGIL = 9.0592%` (`338`, `p = 0.000100`), with Mohenjo-daro at `25.4563%` vs `KN3-Left` `17.6753%` (`p = 0.000100`), `KN3-Bidir` `24.0154%` (`p = 0.008099`), `KN3-BlanketF` `24.2075%` (`p = 0.008099`), and Harappa at `23.2894%` vs `KN3-Left` `16.4470%` (`p = 0.000100`), `KN3-Bidir` `22.1594%` (`p = 0.019598`), `KN3-BlanketF` `22.9127%` (`p = 0.156084`).

---

## 2. Honest Single-Fetch Verification of Primary Sources

Each primary source endpoint was fetched exactly once with `curl -sS -D headers.txt -A "V3R1T4S-research-agent (honest single fetch)"`:

| Source | URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 of Response Body | Key Extracted Value / State |
|---|---|---|---:|---:|---|---|
| Primary Repo 1 (`indus_decipher` commits) | `https://api.github.com/repos/joyboseroy/indus_decipher/commits?per_page=5` | `2026-10-19T20:27:50Z` | `HTTP/2 200` | `21,810` | `8dddd5d5682f942f45fc1ebd17f4b98bc19fb2fb1cec68be70abc62ee0b329d9` | Latest commit `cd600349f6d3193a241c3eb87ff80a2a65377efc` (`2026-09-07T22:24:48Z`, `"Update README.md"`), following `1f1af9c6b7ad255e5faabde1abada378b1ed23c7` (`2026-09-07T22:24:13Z`) and bank reference `1f925b85ca8fa138b874252546f435a333b14df6`. |
| Primary Repo 2 (active target `paragorth/Indus-` repo) | `https://api.github.com/repos/paragorth/Indus-` | `2026-10-19T20:31:58Z` | `HTTP/2 200` | `5,060` | `c5c9cb7554a334820eddb7ef17d5796892443c387e7adb830e7cb2f7881109b9` | Default branch `claude/indus-script-dictionary-u3dzf8`, `updated_at: 2026-10-07T13:59:26Z`, `pushed_at: 2026-10-07T22:44:21Z`. |
| Primary Repo 2 (active target `paragorth/Indus-` commits) | `https://api.github.com/repos/paragorth/Indus-/commits?per_page=5` | `2026-10-19T20:31:59Z` | `HTTP/2 200` | `20,448` | `05284f6051d7165cc143897edf89cca47e42794b74ccec782130eb5b3ea038af` | HEAD `d62ec82d58642038640da25a97177d7a1fddc9d9` (`2026-10-07T13:59:19Z`, `"Work in progress: running loop files"`); prior Indus commit `d3a0d71d2da535f8f0ea920c61be4ef6b6af3114` (`2026-10-03T11:13:42Z`, `"Minimum-lot rule (S-DARK-15.3)..."`). |

### Verification of Non-Subsumption Across All Preregistrations in `paragorth/Indus-` (`P1–P9`, `Q1–Q14`, `R1–R13`, `4`, `5`)

Direct inspection of all five frozen preregistration files in `paragorth/Indus-` confirms that none of them trains a structural model on `data/im77/im77_corpus_lines.csv` (`M77 <= 1977`), evaluates masked-sign top-1 restoration on a post-1977 held-out set, or tests telescoping composite/bigram substitutions across parallel flanking frames (`p3`):

1. **`prereg/preregistration-frozen.json`** (`2,594` bytes, `sha256: 214964e5bf2d15d960f6d3ba6496d7a4a4d312dba6c60b641de64d81acfb8631`, frozen `2026-07-22`, tests `P1–P9`): Induces four coarse boundary rules (`TERMINAL`, `INITIAL`, `PRE-TERMINAL`, `CONNECTIVE`) on home stamp seals and tests descriptive corpus shares (`P1` modal ending `28–45%`, `P2` terminal class `50–75%`, `P3` zero-violation terminal compliance `65–82%`, `P4` stroke taxonomy, `P5` double-terminal endings, `P6` top-10 bigram, `P7` final vs initial Miller-Madow entropy difference, `P8` foreign surprisal, `P9` emblem-animal JSD). No `M77 <= 1977` vs post-1977 split and no telescoping composite/bigram permutation test.
2. **`prereg/preregistration-2-frozen.json`** (`5,124` bytes, `sha256: 1774b7c76d9d047f463c7d583169fa369ae8c3b80ff725cfd9b0ab28bdc20df4`, registered `2026-09-24`, tests `Q1–Q14`): Tests specific sign-level threshold rules on texts absent from `IDF-80` and `inscriptions.csv` (`Q1` plain jar `W740` vs stroked jar `W741` final rate, `Q2` four-stroke fish `W226` vs plain fish `W220`, `Q3` numeral paradigm `3–8` before tree family, `Q4` numerals before fish, `Q5` fixed compounds `7+575`, `7+585`, `III+520`, `Q6` comb/jar/man register split, `Q7` quantity records avoiding jar, `Q8–Q9` two-sided leaf tablets, `Q10` emblem independence, `Q11` seal/sealing non-co-location, `Q12` one-substitution twins, `Q13` excavation-period opener/jar rate stability, `Q14` dictionary validator). None of `Q1–Q14` performs masked-sign top-1 token restoration or tests the 25-pair `M77` telescoping composite/bigram parallel-frame permutation benchmark (`p3`).
3. **`prereg/preregistration-3-frozen.json`** (`5,227` bytes, `sha256: f31a81f11d58ee0e05216cfb3b17b83e6baea303012fd07488ebec38c08dccee`, registered `2026-09-25`, tests `R1–R13`): Tests within-text sign repetition avoidance (`R1`), foreign person signs and openers (`R2–R4`, `R9`, `R12`), regional Mohenjo-daro vs Harappa share of single sign `W226` vs `W220-W520` (`R5`), leaf counts (`R6`), site-specific signs (`R7`), seal vs tablet opener/suffix ratios (`R8`), marker exclusivity (`R10`), closed closer bigrams (`R11`), and tablet voucher values (`R13`). None performs general telescoping composite/bigram permutation testing across `25` frozen `M77` pairs (and `R5` `226 <-> 220 520` was explicitly excluded from the 25 frozen pairs).
4. **`prereg/preregistration-4-credential.json`** (`840` bytes, `sha256: 1a2c32398a03ee56bef02c2f87b61e8899d287da639e896e34c26ed80b8731cf`, frozen `2026-09-29T22:15Z`, tests `P1–P4`): Tests whole-text substring nesting of 3–5-sign texts inside longer texts (`P1`), reuse of 3-sign runs (`P2`), middle uniqueness (`P3`), and foreign sealing formulas (`P4`).
5. **`prereg/preregistration-5-minimumlot.json`** (`1,404` bytes, `sha256: 3fd4a37920faf3ce5f1209b19cb00470e82b9f81da49142c6bf8aba344ea89af`, frozen `2026-10-03`, tests `P5.1–P5.3`): Tests whether short-stroke `1` or `2` precedes counted goods (`P5.1–P5.2`, killed on `210` `IM77` texts and demoted).

---

## 3. Literature & Repository Search (Last 24 Months & Foundational Prior Work)

Single honest GET requests were executed across arXiv, OpenAlex, and GitHub search APIs:

| Search Endpoint | Query URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 of Response Body | Summary of Results |
|---|---|---|---:|---:|---|---|
| arXiv API | `https://export.arxiv.org/api/query?search_query=all:%22Indus+script%22+OR+all:%22Mahadevan+1977%22&sortBy=submittedDate&sortOrder=descending&max_results=20` | `2026-10-19T20:28:06Z` | `HTTP/2 200` | `16,345` | `db1752d37bfd06d662d5c69a64b18f685dfb4b2163ede7715eb50414c73b374d` | `7` total matches (`2001`–`2026`), including `arXiv:2608.02999v1` (`2026-08-04`), `arXiv:2503.21074v3` (`2025-03-27`), `arXiv:1702.00523v1` (`2017`), and `arXiv:0901.3017v1` (`2009`). |
| OpenAlex API (Markov / n-gram / Mahadevan) | `https://api.openalex.org/works?search=Indus+script+Markov+OR+n-gram+OR+Mahadevan&per-page=20` | `2026-10-19T20:28:07Z` | `HTTP/2 200` | `254,716` | `1c89507fa1be3c345c44afd607ba7cc1972bcd417eb14cd5dd1d030cfe1a7a83` | `12,971` total hits; top results are Rao et al. (`2009`, `W1973400336`, `10.1073/pnas.0906237106`) and Yadav et al. (`2010`, `W2048909216`, `10.1371/journal.pone.0009506`). |
| OpenAlex API (Rao / Yadav / Mukhopadhyay) | `https://api.openalex.org/works?search=%22Indus+script%22+Rao+OR+Yadav+OR+Mukhopadhyay&per-page=20` | `2026-10-19T20:33:07Z` | `HTTP/2 200` | `263,728` | `a59c7c4463a1b9fb3e746357613f8eb8afa5a83027a5c4c2f91a2917d90a97d2` | `1,416` hits; includes Rao et al. (*Science* `2009`, `W1980469977`, `10.1126/science.1170391`), Yadav et al. (*PLOS ONE* `2010`), Mahadevan (`1977`, `W562434422`), and Farmer, Sproat & Witzel (`2004`, `W2097228943`). |
| OpenAlex API (Sorted by `publication_date:desc`, 2024–2026) | `https://api.openalex.org/works?search=%22Indus+script%22&sort=publication_date:desc&per-page=20` | `2026-10-19T20:33:48Z` | `HTTP/2 200` | `283,574` | `429bd111e798d98641add0627b414a3b214ffbd24bdfe5f562ff37c7eb346917` | `20` most recent `2026` publications/preprints through `2026-10-15` (`W7221866242`, `W7222223836`, `W7221577147`, `W7221644713`, `W7221436126`, etc.). |
| GitHub Repository Search API | `https://api.github.com/search/repositories?q=indus-temporal-heldout-structure+OR+indus_decipher` | `2026-10-19T20:28:50Z` | `HTTP/2 200` | `162,968` | `96320c7ba000b7cecdf0d434fb2be94eedaa60eede40c7dfba462261cdc10f32` | `27` repositories (`0` for `indus-temporal-heldout-structure`); includes `indus_decipher`, `indus-blind-benchmark`, `indus-tests`, `glossa-lab`, and `indus-script`. |
| GitHub Commit Search API (`im77_corpus_lines.csv` / `loop24_pairs.json`) | `https://api.github.com/search/commits?q=%22im77_corpus_lines.csv%22+OR+%22loop24_pairs.json%22+OR+%22S-DARK-15.3%22` | `2026-10-19T20:31:45Z` | `HTTP/2 200` | `7,425` | `f67c783990c1248030074d5dfdf9c5ac47ac489b5cf5e746bed3928e8f9aa8c9` | `1` commit match across all of GitHub (`d3a0d71d2da535f8f0ea920c61be4ef6b6af3114` in `paragorth/Indus-`, `2026-10-03T11:13:42Z`). |

### Detailed Comparison Against Foundational and 2024–2026 Literature

1. **Rao et al. (*Science* 2009, `10.1126/science.1170391`; *PNAS* 2009, `10.1073/pnas.0906237106`) & Yadav et al. (*PLOS ONE* 2010, `10.1371/journal.pone.0009506`; *Palgrave Commun.* 2017)**:
   - Evaluated bigram conditional entropy and static n-gram restoration on `EBUDS` (a filtered subset of `1,548` texts from Mahadevan 1977 `M77`) using within-M77 random splits or leave-one-out checks. They never constructed a chronological `M77 (<= 1977)` to post-1977 (`CISI Vol. 2 / 3.1 / 3.2 / Dholavira / HARP`) out-of-sample benchmark, never deduplicated seal-impression identity groups across the 1977 boundary via `identity-directory.json`, and never tested frozen `M77` telescoping composite/bigram substitutions on post-1977 parallel frames (`p3`).
2. **Mukhopadhyay (*Palgrave Commun.* 2019)**:
   - Analyzed positional entropy and ancestral-token distributions inside static Mahadevan 1977 / Wells sign inventories without out-of-sample post-1977 evaluation or telescoping composite/bigram permutation testing.
3. **Raghavendra (*arXiv:2608.02999v1*, 2026-08-04) & `indus-blind-benchmark` (`2026-10-09`, commit `3f01abf3cfd0100c1bcd83c2f6e29731b3f4de9f`)**:
   - Introduces the `SIGIL` non-linguistic generative emblem control (`adversarial_null_model.py`). Our package directly incorporates `SIGIL` as a baseline (`400` independent `SIGIL` controls, `best_control = 0.096221` vs `real = 0.200482`).
4. **Recent October 2026 Preprints & Repositories (`W7221866242` / `zenodo.23404360`, `W7222223836` / `zenodo.23396757`, `W7221577147` / `zenodo.23307027`, `W7221436126` / `osf.io/7m35w`, `Savirinc/indus-script` commit `dff0d1727434ea9aaade6d824c54e6b42bf2edc6`)**:
   - None of these works trains a closed-form slot-syntax + `32` Ward distributional equivalence-class (`C0..C31`) + center-bypass skip-bigram model (`M77-CLSS`) strictly on `data/im77/im77_corpus_lines.csv` (`M77 <= 1977`) or validates the Top-25 `M77` telescoping composite/bigram substitutions on the deduplicated `999`-inscription (`3,731`-token) post-1977 held-out corpus (`30` shared frames vs `7.6427` null mean, `max = 23`, `p = 0.000100 < 0.001`, `p3`).

---

## 4. V3R1T4S `TROPHY_CASE.md` and Open Pull Requests Check

| V3R1T4S Endpoint | URL | UTC Timestamp | HTTP Status | Bytes | SHA-256 of Response Body | Audit Result |
|---|---|---|---:|---:|---|---|
| `TROPHY_CASE.md` | `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` | `2026-10-19T20:28:09Z` | `HTTP/2 200` | `31,235` | `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` | `100` lines inspected; `0` matches for `indus`, `mahadevan`, `im77`, or `undeciphered-scripts`. |
| Open PRs (Page 1, newest 100: PR #469–#569) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-19T20:28:09Z` | `HTTP/2 200` | `2,146,142` | `ca64c03544277e6edbd812255722619d96602eb55ad48dfcd5933781d10c0861` | `100` open PRs inspected (PR #569 down to PR #469); `0` PRs reference `indus-temporal-heldout-structure`, `Indus`, `Mahadevan`, or `undeciphered-scripts`. |
| Open PRs (Page 2, next 100: PR #367–#468) | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2` | `2026-10-19T20:30:01Z` | `HTTP/2 200` | `2,211,407` | `267523b8302c8ac60fc05faa999cf2cda8430cbd098ad0f55a9dd30cb6d7ac30` | `100` open PRs inspected (PR #468 down to PR #367); `0` claim PRs target `indus-temporal-heldout-structure` (only bank-maintenance PR #399 mentions `Linear A corpus`). |

---

## 5. Verdict

The partial win `p3` structural finding (`30` shared parallel frames across the 25 frozen `M77` telescoping composite/bigram pairs on `999` post-1977 held-out inscriptions vs `10,000`-permutation null mean `7.6427`, `max = 23`, `p = 0.000100 < 0.001`, accompanied by `M77-CLSS` `20.0482%` Mode 1 / `22.6749%` Mode 2 masked-sign restoration beating `KN3-Left` and `SIGIL` at `p = 0.000100` and all `400` `SIGIL` controls) is novel, does not subsume any existing preregistration (`P1–P9`, `Q1–Q14`, `R1–R13`, `4`, `5`), and strictly beats all known baselines on `p3`.

pass: true
