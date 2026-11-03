# Novelty Verification Report: C(53,20,3) <= 34

role: NOVELTY
context: subagent (fresh context that saw only claim/)

## 1. Summary of Claim Under Review

- **Target entry**: `covering-designs-record`
- **Claimed result**: An explicit `(53,20,3)` covering design with `b = 34` blocks in `claim/C53_20_3_34blocks.txt` (`sha256: ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`), strictly improving the best known upper bound `C(53,20,3) <= 35` by 1 block.
- **Independent sanity check on `claim/C53_20_3_34blocks.txt`**:
  - File size: `1,926` bytes; SHA-256: `ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e` (exact match).
  - Block structure: `34` non-empty lines, `34` distinct blocks, each block containing exactly `20` distinct integers in `1..53`.
  - Exhaustive 3-subset coverage check: All `C(53,3) = 23,426` triples in `{1,...,53}` are covered (`0` missing).
  - Bounds check: Parameters satisfy `v = 53 <= 99`, `k = 20 <= 25`, `t = 3 <= 8`, `C(53,3) = 23,426 <= 5e9`, and `b = 34` is above the Schonheim lower bound `L(53,20,3) = ceil(53/20 * ceil(52/19 * ceil(51/18))) = 24` as well as the LJCR lower bound `30`.

---

## 2. Live Verification of Authoritative Table Sources

All required live sources were re-fetched directly during this verification session and saved in `panel/work/novelty/`:

1. **Covering Repository (`https://coveringrepository.com/download_archive_vkt.aspx`)**
   - Waited 5 seconds and fetched once with `curl.exe -s -A "V3R1T4S-research-agent (curl)"` at `2026-10-16T02:08:27Z`.
   - Response: `HTTP 200`, `171,741` bytes, `sha256: 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17` (saved to `panel/work/novelty/live_coveringrepository_download_archive_vkt.html`, matching `claim/table_record/coveringrepository_download_archive_vkt.html` byte-for-byte).
   - Plain `(v,k,t)` entry (`m = t = 3` row): `53[TAB]20[TAB]03[TAB]03[TAB][TAB]35`, confirming the live upper bound is **35**.

2. **Dan Gordon's LJCR Landing Page (`https://dmgordon.org/covering-designs/`)**
   - Fetched at `2026-10-16T02:08:31Z`: `HTTP 200`, `9,200` bytes, `sha256: a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3` (saved to `panel/work/novelty/dmgordon_covering_designs.html`).
   - Serves as an informational overview pointing to `coveringrepository.com` and the Zenodo/GitHub datasets.

3. **Zenodo La Jolla Covering Repository Dataset (`19472830/versions/latest` -> `19735294`, v1.2)**
   - Fetched `https://zenodo.org/api/records/19472830/versions/latest` at `2026-10-16T02:09:28Z` (`HTTP 200`), which resolved to record `19735294` (version `1.2`, published `2026-04-24`; metadata verified at `https://zenodo.org/api/records/19735294` at `2026-10-16T02:08:31Z`, `HTTP 200`).
   - Downloaded full `coverdata.json` from `https://zenodo.org/records/19735294/files/coverdata.json?download=1` at `2026-10-16T02:09:46Z`: `HTTP 200`, `8,319,503` bytes, `sha256: 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87` (saved to `panel/work/novelty/zenodo_coverdata.json`, matching the hash in `claim/table_record/ljcr_zenodo_v1.2_C53_20_3.json`).
   - Entry for `C(53,20,3)`: `size = 35`, `low_bd = 30`, best improvement `["35", "Simple construction from (54,20,3)", "LJCR", "2009-01-21 18:53:56"]`.

4. **GitHub `dmgordo/LJCR` Repository (`coverings/coverdata.json`)**
   - Checked latest commit via `https://api.github.com/repos/dmgordo/LJCR/commits?per_page=5` (`HTTP 200`): latest commit is `459bcaf247bd8d34610d946b0465864f7d4dfa37` on `2022-12-19T18:10:24Z`.
   - Downloaded `https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json` at `2026-10-16T02:10:11Z`: `HTTP 200`, `6,517,686` bytes, `sha256: 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef` (saved to `panel/work/novelty/gh_ljcr_coverdata.json`).
   - Entry for `C(53,20,3)`: `size = 35`, `low_bd = 30` (unchanged since 2009-01-21).

---

## 3. Literature, Preprint, and Repository Sweeps (Last 24 Months and 6 Months)

We searched arXiv, Zenodo, GitHub, `elder-plinius/V3R1T4S`, and the general web for any prior or concurrent improvement to `C(53,20,3)`:

1. **arXiv Preprints (24-month and 6-month windows, 2024-10 to 2026-10)**
   - Note: `export.arxiv.org/api/query` returned `HTTP 429` (`Rate exceeded.`) due to concurrent IP rate-limiting, so we queried arXiv's live search endpoint directly (`https://arxiv.org/search/?query=%22covering+design%22...` and `%22covering+designs%22...`, both `HTTP 200`, saved in `panel/work/novelty/arxiv_html_search.html` and `arxiv_html_search_plural.html`) and ran domain-restricted web searches (`search_web` on `arxiv.org`).
   - Recent combinatorics preprints in the window include `arXiv:2609.23094` (Sep 2026, *Counting and Covering in Nearest-Neighbour Representations of Boolean Functions*), `arXiv:2607.10978` (Jul 2026, *A tight single-change covering design with block size 6*), `arXiv:2606.03890` (Jun 2026, *Note on Balanced Fractional Factorial Designs and Covering Designs*), `arXiv:2605.05109` (May 2026, *Optimal Linear Covering Codes and Saturated Sets in Projective Spaces*), `arXiv:2604.14046` (Apr 2026, *New records in the surface covering scenario of a dual version of Chvatal's Art Gallery Problem*), and `arXiv:2603.24170` (Mar 2026, *Tackling the 6/49 Lottery...*).
   - Zero arXiv preprints mention `(53,20,3)` or claim any upper bound `C(53,20,3) <= 34`.

2. **Zenodo Records Sweep (`https://zenodo.org/api/records?q="covering+design"+OR+"covering+designs"&sort=mostrecent`)**
   - Fetched at `2026-10-16T02:12:25Z` (`HTTP 200`, 36 total records, saved in `panel/work/novelty/zenodo_search_covering.json`).
   - Recent 2026 covering-design records found on Zenodo:
     - `23377562` (2026-10-14): *The covering numbers C(18,11,3) and C(20,12,3) are both 10*
     - `23191655` (2026-10-06): *Certified DRAT proofs that no 61-block (16,5,3) covering exists, so C(16,5,3) >= 62*
     - `22171255` (2026-08-30): *k34cover: deterministic minimum-excess K3/K4 coverings*
     - `21852165` (2026-08-08): *Covering design result: C(13,7,5) = 78 - ruling out all 77-block coverings*
     - `21834602` (2026-08-07): *A (28,13,4) covering design with 53 blocks* (Brock Falfas, `C(28,13,4) <= 53` and `C(32,13,4) <= 95`)
     - `21716718` & `21660461` (2026-07-28/31): *Formal elimination of link class 52 in the C(13,7,4) covering-design search*
     - `21609255` & `21609214` (2026-07-26): *The Covering Number C(12,6,4) is 41*
   - None of these records touch `C(53,20,3)`.

3. **GitHub Repositories, Issues, and Hobbyist Claims**
   - Queried GitHub REST API (`HTTP 200`, saved in `panel/work/novelty/gh_*.json`) for repositories and issues matching `"covering design"`, `"covering designs"`, `"53,20,3"`, `"C(53,20,3)"`, and `covering 53 20 3`.
   - Checked `thebrockchain/covering-designs` (`https://raw.githubusercontent.com/thebrockchain/covering-designs/main/README.md`, `HTTP 200`, `6,127` bytes): contains only `C(28,13,4) <= 53` and `C(32,13,4) <= 95`.
   - Checked `Soulxlight/covering-design-c54-16-4` (updated `2026-10-14`): studies only `C(54,16,4)` lower bounds.
   - Checked `ozgronurkoc/Twmq` (updated `2026-10-13`): general Turkish Spor Toto covering scripts, no `(53,20,3)` designs.
   - Repository search for `"53,20,3" OR "C(53,20,3)"` returned `0` repositories; issue searches returned no combinatorial covering designs for `(53,20,3)`.

4. **V3R1T4S Repository (`elder-plinius/V3R1T4S`)**
   - Fetched `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` at `2026-10-16T02:10:12Z` (`HTTP 200`, `30,936` bytes): no `covering-designs-record` or `C(53,20,3)` entry exists in `TROPHY_CASE.md` (the only `(53,...)` entry is a constant-weight code `A(53,8,7) >= 3987`).
   - Fetched `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` (`HTTP 200`, 17 open PRs) and `state=all&per_page=100` (`HTTP 200`, 100 PRs): zero open or closed PRs claim `C(53,20,3)` or any `(53,20,3)` covering design.

5. **General Web Search (`search_web`)**
   - Web searches for `"C(53,20,3)" OR "C(53, 20, 3)" OR "(53,20,3)" covering design` and `"coveringrepository" OR "La Jolla Covering Repository" "53" "20" "34" covering design` returned no record of `C(53,20,3) <= 34` anywhere on the public web.

---

## 4. Verdict

Every live authoritative table (`coveringrepository.com`, `dmgordon.org/covering-designs/`, Zenodo `19735294` v1.2, and GitHub `dmgordo/LJCR`) lists `C(53,20,3) <= 35` (standing since January 2009), and no preprint, repository, issue, or web source claims `C(53,20,3) <= 34`. The 34-block design in `claim/C53_20_3_34blocks.txt` is verified and genuinely novel.

pass: true
