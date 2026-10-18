# Skeptic Panel Report — Role: NOVELTY

role: NOVELTY
problem_id: ccd-binary-gupta-nanoalloys-38-55
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)

## 1. Mandate & Scope

Per the V3R1T4S skeptic panel protocol (Step 6, NOVELTY):
- Perform one honest single HTTP GET (no retries) of the primary Cambridge Cluster Database (CCD) index page and the primary comparator archive for 55-atom copper-silver binary Gupta nanoalloys, recording exact URL, UTC fetch timestamp, HTTP status code, `Last-Modified` header, byte count, SHA-256 digest, and published header energies.
- Search the four benchmark papers named in the problem statement, the Nunez & Johnston (2010) Gupta parameterization paper, their citing literature, the last 24 months of preprints and literature on arXiv and OpenAlex, GitHub repositories, the repository `TROPHY_CASE.md`, and all open pull requests.
- Pass only if the claimed result strictly beats every known published value by at least `1e-4 eV` (direction: minimization; a tie is not a record).

---

## 2. Honest Single Fetch of Primary Comparator Table & Archive

### 2.1 Cambridge Cluster Database Index Page (`CCD.html`)

- **URL:** `https://www-wales.ch.cam.ac.uk/CCD.html`
- **Fetch UTC Timestamp:** `2026-10-18T21:14:16Z` (`Date: Sun, 18 Oct 2026 21:14:16 GMT`)
- **HTTP Status:** `HTTP/1.1 200 OK`
- **Server / Last-Modified / ETag:** `Apache/2.4.58 (Ubuntu)` | `Last-Modified: Fri, 14 Aug 2026 13:42:16 GMT` | `ETag: "3acb-65901fd1ec18a"`
- **Byte Size:** `15,051` bytes (identical to `claim/CCD.html`)
- **SHA-256:** `9662d9a7fcf599815e22d6dae7fbdeac8b71cf7892f836284f2d0769383183c8`
- **Quoted Binary Gupta Nanoalloy Links on `CCD.html`:**
  - Attribution line: `Lai Xiangjing, Huang Wenqi and Xu Ruchu, published in` (linking to *J. Chem. Phys.* **135**, 164109, 2011)
  - Archive link 1: `http://www-wales.ch.cam.ac.uk/~wales/CCD/AgAu_55.rar` (anchor text `Ag/Au55`)
  - Archive link 2: `http://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar` (anchor text `Cu/Ag55`)
  - Archive link 3: `http://www-wales.ch.cam.ac.uk/~wales/CCD/CuAu_55.rar` (anchor text `Cu/Au55`)
  - Archive link 4: `http://www-wales.ch.cam.ac.uk/~wales/CCD/CuAu_38.rar` (anchor text `Cu/Au38`)

### 2.2 Primary Comparator Archive (`CuAg_55.rar`)

- **URL:** `https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar`
- **Fetch UTC Timestamp:** `2026-10-18T21:14:16Z` (`Date: Sun, 18 Oct 2026 21:14:16 GMT`)
- **HTTP Status:** `HTTP/1.1 200 OK`
- **Server / Last-Modified / ETag:** `Apache/2.4.58 (Ubuntu)` | `Last-Modified: Fri, 24 Jun 2011 13:03:13 GMT` | `ETag: "10834-4a674d2fc2640"`
- **Content-Type / Byte Size:** `application/vnd.rar` | `67,636` bytes (identical to `claim/CuAg_55.rar`)
- **SHA-256:** `c6cdc7b61eddf14da78c752368618679836f24f40c1a17c84f47230e210d01dd`
- **Extracted Contents (`bsdtar`):** Directory `CuAg55/` containing 56 coordinate files (`Cu0Ag55.txt` through `Cu55Ag0.txt`) plus `reference.txt`, which reads verbatim:
  - `The Gupta potential function and the corresponding parameters can be found in Refs. [1].`
  - `[1]S. Nunez and R. L. Johnston. J. Phys. Chem. C, 2010, 114, 13255-13266.`

### 2.3 Exact Header Lines Quoted from Live-Fetched `CuAg_55.rar` vs. Claimed Structures

| Archive File in `CuAg_55.rar` | Verbatim Archive Header Line | Archive Polished Energy (eV) | Claimed Structure File | Claimed Certified Energy $E^*$ (eV) | Strict Improvement $\Delta E$ (eV) |
|---|---|---:|---|---:|---:|
| `Cu39Ag16.txt` | `NA(type:0)=39  NB(type:1)=16  E=-162.61229825` | `-162.61229825` | `claim/Cu39Ag16_improved.txt` | **`-163.80214265`** | **`-1.18984440`** |
| `Cu34Ag21.txt` | `NA(type:0)=34  NB(type:1)=21  E=-160.81218484` | `-160.81218484` | `claim/Cu34Ag21_improved.txt` | **`-161.76692486`** | **`-0.95474003`** |
| `Cu33Ag22.txt` | `NA(type:0)=33  NB(type:1)=22  E=-160.43136967` | `-160.43136967` | `claim/Cu33Ag22_improved.txt` | **`-161.35336662`** | **`-0.92199695`** |
| `Cu31Ag24.txt` | `NA(type:0)=31  NB(type:1)=24  E=-159.69487106` | `-159.69487106` | `claim/Cu31Ag24_improved.txt` | **`-160.49285973`** | **`-0.79798867`** |
| `Cu22Ag33.txt` | `NA(type:0)=22  NB(type:1)=33  E=-156.38507389` | `-156.38507389` | `claim/Cu22Ag33_improved.txt` | **`-156.61674699`** | **`-0.23167311`** |
| `Cu20Ag35.txt` | `NA(type:0)=20  NB(type:1)=35  E=-155.56958143` | `-155.56958143` | `claim/Cu20Ag35_improved.txt` | **`-155.69839654`** | **`-0.12881511`** |
| `Cu15Ag40.txt` | `NA(type:0)=15  NB(type:1)=40  E=-153.49887624` | `-153.49887624` | `claim/Cu15Ag40_improved.txt` | **`-153.62512358`** | **`-0.12624733`** |
| `Cu17Ag38.txt` | `NA(type:0)=17  NB(type:1)=38  E=-154.40077125` | `-154.40077125` | `claim/Cu17Ag38_improved.txt` | **`-154.46534927`** | **`-0.06457801`** |

Every one of the eight compositions strictly improves upon the live-fetched CCD archive record by between `0.06457801 eV` (`645x` the `1e-4 eV` threshold) and `1.18984440 eV` (`11,898x` the `1e-4 eV` threshold on headline composition `Cu39Ag16`).

---

## 3. Literature, Preprint & Repository Audit (Including Last 24 Months)

### 3.1 Benchmark Papers Named in Problem Statement & Parameterization Source (OpenAlex Single Fetches)

| Paper / DOI | OpenAlex Fetch URL | UTC Timestamp | HTTP | Response SHA-256 | OpenAlex ID / Cites | Findings on 55-Atom $\text{Cu}_n\text{Ag}_{55-n}$ |
|---|---|---|---:|---|---|---|
| Lai, Huang & Xu (*J. Chem. Phys.* **135**, 164109, 2011) `10.1063/1.3656766` | `https://api.openalex.org/works/https://doi.org/10.1063/1.3656766` | `2026-10-18T21:14:40Z` | `200` | `5020074e6f5c88f410b425e466f5a69806707ab9e5806d75dece266a295b4426` | `W2070096859` (`31` cites) | Source of the CCD archive `CuAg_55.rar` (with `Cu39Ag16` at `-162.61229825 eV`). |
| Wu & Cheng (*J. Chem. Phys.* **141**, 124110, 2014) `10.1063/1.4896152` | `https://api.openalex.org/works/https://doi.org/10.1063/1.4896152` | `2026-10-18T21:14:40Z` | `200` | `1b7bea8a15a862eb9c8e5bbe5885b7f97791f5d3d9d7b669a1af7881e7a05c99` | `W1968284889` (`11` cites) | Studies binary Lennard-Jones clusters and 79-atom Au-Pd Gupta clusters; no $\text{Cu}_n\text{Ag}_{55-n}$ data. |
| Rondina & Da Silva (*J. Chem. Inf. Model.* **53**, 2282, 2013) `10.1021/ci400224z` | `https://api.openalex.org/works/https://doi.org/10.1021/ci400224z` | `2026-10-18T21:14:40Z` | `200` | `885bde121fc8958fbf001c56dc21129f315e66fa7ab20a30e36506e4c3e991cf` | `W2030143939` (`144` cites) | Benchmarks revised basin-hopping on LJ, Sutton-Chen Ag-Pd, and DFT Al clusters; no $\text{Cu}_n\text{Ag}_{55-n}$ data. |
| Du et al. (*R. Soc. Open Sci.* **6**, 190342, 2019) `10.1098/rsos.190342` | `https://api.openalex.org/works/https://doi.org/10.1098/rsos.190342` | `2026-10-18T21:14:41Z` | `200` | `eacceec8c0061096457025f6cc66219d1cd4a9a68b285efd889cd355e6fe554d` | `W2964523522` (`16` cites) | Studies bimetallic Ag-Au and Cu-Au clusters at fixed stoichiometry ratios (`1:1`, `1:3`, `3:1`); does not study Cu-Ag. |
| Nunez & Johnston (*J. Phys. Chem. C* **114**, 13255, 2010) `10.1021/jp1048088` | `https://api.openalex.org/works/https://doi.org/10.1021/jp1048088` | `2026-10-18T21:14:41Z` | `200` | `1228737f2c8a00d73ff937653705bbf9b9bf24191f5677683d34781cdc338bbc` | `W2087937366` (`108` cites) | Defines the Cu-Ag Gupta parameters used by `CuAg_55.rar` and studies sizes $N = 34, 38, 98$ (not $N = 55$). |

### 3.2 Citation Graph & Recent Literature (2024–2026)

1. **All 31 Works Citing Lai, Huang & Xu (2011) (`W2070096859`):**
   - **URL:** `https://api.openalex.org/works?filter=cites:W2070096859&per-page=50`
   - **UTC Timestamp:** `2026-10-18T21:15:33Z` | **HTTP:** `200` | **SHA-256:** `816e4d7592cc7c5b0b60f5ee54330373a055c39ce1f4ad388` (full digest `816e4d7592cc7c5b0b60f7698ee0c686a00f5ee54330373a055c39ce1f4ad388`)
   - **Result:** All `31` citing works returned (`meta.count = 31`). Recent citing papers in 2024–2025 include `10.1016/j.cpc.2025.109655` (pure silver clusters), `10.1140/epjb/s10051-024-00819-9` (MD phase transitions), and `10.1016/j.cplett.2024.141200` (Cu-Pd clusters). None report putative global minimum energies for 55-atom $\text{Cu}_n\text{Ag}_{55-n}$ Gupta clusters.
2. **OpenAlex Keyword Search (`CuAg 55 Gupta nanoalloy`):**
   - **URL:** `https://api.openalex.org/works?search=CuAg+55+Gupta+nanoalloy&per-page=25`
   - **UTC Timestamp:** `2026-10-18T21:14:56Z` | **HTTP:** `200` | **SHA-256:** `384017c165238a722175805a4b88b915b6b75cc8f42c93fc4c3a0aefa069516e`
   - **Result:** `26` total works matched (`meta.count = 26`, including `10.3390/nano16181194` in 2026 on coalescence/melting of $\text{Ag}_{309}$ and $\text{Cu}_{309}$); none report 55-atom $\text{Cu}_n\text{Ag}_{55-n}$ Gupta global minima.
3. **arXiv API Preprint Search (Sorted Newest First, 2022–2026):**
   - **URL:** `https://export.arxiv.org/api/query?search_query=all:CuAg+OR+all:%22Gupta+potential%22+nanoalloy&sortBy=submittedDate&sortOrder=descending&max_results=25`
   - **UTC Timestamp:** `2026-10-18T21:14:42Z` | **HTTP:** `200` | **SHA-256:** `c9e912cc3247d07a0b9e925f31875255bc439eed89a2bfd4017340d8846c983a`
   - **Result:** `72` total matches (`25` newest entries returned, spanning `2022-07` through `2026-09`, including `arXiv:2609.02492v1`, `arXiv:2607.00195v1`, `arXiv:2603.23442v1`, and `arXiv:2507.13791v1`). The closest Cu-Ag nanoalloy preprint is `arXiv:2603.23442v1` (*Structural Chart of Copper-Silver Nanoalloys through machine learning*, 2026-03-24), which constructs finite-temperature parallel-tempering MD structural maps exclusively for 38-atom $\text{Ag-Cu}$ nanoalloys and does not study 55-atom $\text{Cu}_n\text{Ag}_{55-n}$.
4. **GitHub API Search:**
   - **Code Search URL:** `https://api.github.com/search/code?q=Cu39Ag16+OR+CuAg_55` (`2026-10-18T21:14:42Z`, HTTP `401` unauthenticated REST endpoint, SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`).
   - **Repositories Search URL:** `https://api.github.com/search/repositories?q=CuAg+nanoalloy+OR+Gupta+nanoalloy` (`2026-10-18T21:14:56Z`, HTTP `200`, SHA-256 `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f`): `total_count = 0` matching repositories.

---

## 4. V3R1T4S Repository `TROPHY_CASE.md` & Open Pull Requests Check

1. **`TROPHY_CASE.md` Single Fetch:**
   - **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **UTC Timestamp:** `2026-10-18T21:14:43Z` | **HTTP:** `200` | **Bytes:** `31,235` | **SHA-256:** `b946f68eb0a6473dd2224065a535d3282da24669f6724a1472171a1` (full digest `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`)
   - **Result:** `100` lines inspected; `0` matches for `ccd-binary-gupta-nanoalloys-38-55`, `CuAg`, `Cu39Ag16`, or `Gupta`.
2. **Open Pull Requests Single Fetch:**
   - **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
   - **UTC Timestamp:** `2026-10-18T21:14:43Z` | **HTTP:** `200` | **Bytes:** `2,175,790` | **SHA-256:** `8b3858f5dd80fd86ab35f757ab025bc3de3ffb410a6a5320855b88fc31ac9f07`
   - **Result:** `100` open pull requests inspected (PR numbers `#363` through `#464`). Only one PR in the list mentions Gupta clusters at all — PR `#374`, which targets a completely different problem (`ccd-gupta-murrell-mottram-metal-clusters`, pure/binary Zn/Cd clusters). Zero open pull requests touch `ccd-binary-gupta-nanoalloys-38-55` or $\text{Cu}_n\text{Ag}_{55-n}$.

---

## 5. Verdict

The live-fetched Cambridge Cluster Database archive `CuAg_55.rar` (`https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar`, `67,636` bytes, SHA-256 `c6cdc7b61eddf14da78c752368618679836f24f40c1a17c84f47230e210d01dd`) lists `-162.61229825 eV` as the putative global minimum energy for `Cu39Ag16` (and `-160.81218484 eV`, `-160.43136967 eV`, `-159.69487106 eV`, `-156.38507389 eV`, `-155.56958143 eV`, `-153.49887624 eV`, `-154.40077125 eV` for the seven additional compositions). No subsequent publication on OpenAlex or arXiv, no GitHub repository, no entry in `TROPHY_CASE.md`, and no open pull request improves upon these 2011 values. The claimed structures in `claim/Cu39Ag16_improved.txt` ($E^* = -163.80214265\text{ eV}$, $\Delta E = -1.18984440\text{ eV}$) and the seven companion compositions strictly beat all known records by orders of magnitude above the `1e-4 eV` threshold.

pass: true
