# Skeptic Panel Report — Role: NOVELTY

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: ihtp-ihtc2024-upper-bounds
instance: i27
claimed_cost: 50063
published_table_cost: 50976
pending_pr_359_cost: 50125
delta_vs_published_table: -913 (-1.791%)
delta_vs_pending_pr_359: -62 (-0.124%)

## 1. Honest Single Fetch of Primary Benchmark Table and Published Solution

All fetches were executed as single honest HTTP GET requests with User-Agent `V3R1T4S-research-agent (honest single fetch)` and zero retries:

1. **Primary Benchmark Table (`https://ihtc2024.github.io/ihtp/index.html`)**
   - Fetch timestamp (UTC): `2026-10-18T14:39:28Z`
   - HTTP status: `200`
   - Payload size: `17442` bytes
   - SHA-256: `7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495` (identical to `claim/ihtp_index.html`)
   - Exact `i27` row on the live page:
     - Instance column: `i27`
     - Best Known Objective Cost column: `50976` (attributed in the page header to Kletzander, Mischek & Musliu)
     - Solution link column: `/assets/files/solutions/public/IHTP/sol_i27.json` (`sol_i27.json`)

2. **Published Best-Known Solution File (`https://ihtc2024.github.io/assets/files/solutions/public/IHTP/sol_i27.json` and raw GitHub mirror)**
   - Note: `https://ihtc2024.github.io/assets/files/sol_i27.json` returned HTTP `404` at `2026-10-18T14:39:28Z` because the live table links to `/assets/files/solutions/public/IHTP/sol_i27.json`.
   - Fetch of `https://raw.githubusercontent.com/ihtc2024/ihtc2024.github.io/main/assets/files/solutions/public/IHTP/sol_i27.json` at `2026-10-18T14:39:50Z`: HTTP `200`, `209603` bytes, SHA-256 `62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5`.
   - Fetch of `https://ihtc2024.github.io/assets/files/solutions/public/IHTP/sol_i27.json` at `2026-10-18T14:39:51Z`: HTTP `200`, `209603` bytes, SHA-256 `62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5` (identical to `claim/published_sol_i27.json`).

3. **Benchmark Repository Commit History (`https://api.github.com/repos/ihtc2024/ihtc2024.github.io/commits?per_page=5`)**
   - Fetch timestamp (UTC): `2026-10-18T14:39:29Z`, HTTP status: `200`
   - Latest 5 commits on `main`:
     - `ce2f5e5a820f6b16ce2893c8253031172c3ab441` (`2026-08-25T10:59:55Z`): `updated .gitignore`
     - `311173468a6181ae967fa906426696118a4e534a` (`2026-08-25T10:57:09Z`): `deleted DS_Store files`
     - `cbe61b8905205854afbf327f243a3e4fdc378252` (`2026-08-25T10:55:28Z`): `updated global UB`
     - `f378e23151ac45af02d6670ef09058dcaa9a4dc5` (`2026-03-03T11:03:39Z`): `updated README.md`
     - `bef73adaf052c3893bc314f7fa33db0f6cad07f4` (`2026-03-03T11:02:25Z`): `updated README.md`

## 2. Independent Verification of Claimed vs. Published Solutions on `i27`

Running `claim/author_checker_ihtp_check.py` on `claim/i27.json` (`478008` bytes, SHA-256 `a4c3d597021eca59eb2ce37ef4de189eed25a8a91d51a466bbde5c42c54e4134`):

- **Claimed solution (`claim/sol_i27.json`, `209120` bytes, SHA-256 `900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7`)**:
  - `Total violations = 0`
  - `RoomAgeMix = 298`, `RoomSkillLevel = 3610`, `ContinuityOfCare = 3045`, `ExcessiveNurseWorkload = 620`, `OpenOperatingTheater = 3210`, `SurgeonTransfer = 290`, `PatientDelay = 16490`, `ElectiveUnscheduledPatients = 22500`
  - `Total cost = 50063` (`PASS`)
- **Published baseline (`claim/published_sol_i27.json`, `209603` bytes, SHA-256 `62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5`)**:
  - `Total violations = 0`
  - `RoomAgeMix = 298`, `RoomSkillLevel = 3930`, `ContinuityOfCare = 3518`, `ExcessiveNurseWorkload = 740`, `OpenOperatingTheater = 3210`, `SurgeonTransfer = 290`, `PatientDelay = 16490`, `ElectiveUnscheduledPatients = 22500`
  - `Total cost = 50976` (`PASS`)

## 3. Literature and Code Search (Last 24 Months)

1. **arXiv API (`https://export.arxiv.org/api/query?search_query=all:%22IHTC%22+OR+all:%22Integrated+Healthcare+Timetabling%22&sortBy=submittedDate&sortOrder=descending&max_results=25` and `all:%22IHTP%22`)**
   - Fetched at `2026-10-18T14:39:29Z` and `2026-10-18T14:41:37Z` (HTTP `200`).
   - Only two preprints in the last 24 months address the IHTC-2024 / IHTP benchmark:
     - `arXiv:2610.00044v1` (`2026-09-03T05:41:19Z`, *Improved upper bounds for five IHTC-2024 benchmark instances via exact reoptimization of the nurse-to-room layer*, A. Gippini Requeijo): improves only five small instances (`i02`: `1264` to `1263`, `i05`: `12760` to `12744`, `m01`: `3384` to `3380`, `m03`: `6697` to `6692`, `m04`: `3318` to `3315`). Full text inspection confirms that on the remaining 51 instances (including `i27`) the exact MILP did not close within 180 seconds and no bound for `i27` was improved.
     - `arXiv:2511.04685v2` (`2025-10-23T10:14:04Z`, updated `2026-05-01T08:12:45Z`, *A hybrid solution approach for the Integrated Healthcare Timetabling Competition 2024*, D. Guericke et al., Team Twente): reports a lower bound of `37302` on `i27`, cites the earlier competition best upper bound of `51828` (prior to Kletzander, Mischek & Musliu's `50976`), and obtains Team Twente upper bounds of `59948` (10-minute run) and `59029` (1-hour run) on `i27`.
   - Neither preprint reports an upper bound on `i27` below `50976`.

2. **GitHub Repository Search (`https://api.github.com/search/repositories?q=IHTC2024+OR+IHTP`)**
   - Fetched at `2026-10-18T14:39:30Z` (HTTP `200`, `46` total results).
   - Relevant repositories (`ihtc2024.github.io`, `IHTC2024`, `ihtc2024-imada-submission`, `IHTP`, `ihtc2024-tfg`) correspond to the official benchmark website and competition submissions whose best solutions are already reflected in `ihtc2024.github.io/ihtp/index.html` (`50976` on `i27`).
   - Note: unauthenticated GitHub code search (`https://api.github.com/search/code?q=%22i27.json%22+IHTP`, fetched at `2026-10-18T14:39:31Z`) returned HTTP `401` (`Requires authentication`), which is standard for GitHub's `/search/code` endpoint without a token.

## 4. Check of V3R1T4S `TROPHY_CASE.md` and Pull Requests

1. **`TROPHY_CASE.md` (`https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`)**
   - Fetched at `2026-10-18T14:39:32Z` (HTTP `200`, SHA-256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`, entries `1` through `53`).
   - Zero entries in `TROPHY_CASE.md` mention `ihtp`, `ihtc2024`, or `i27`.

2. **Open Pull Requests (`https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` and `page=2`) and Closed Pull Requests (`state=closed&per_page=100`)**
   - Fetched at `2026-10-18T14:39:32Z`, `2026-10-18T14:40:08Z`, and `2026-10-18T14:40:28Z` (all HTTP `200`; `95` open PRs total spanning `#9` to `#402`, plus `100` most recent closed PRs).
   - Closed PRs: `0` matches for `ihtc`, `ihtp`, or `i27`.
   - Open PRs: two matches for IHTC-2024:
     - **PR `#358`** (created `2026-10-17T17:17:30Z`): targets hidden instance `m26` (`69730` to `68496`), a different target and different instance.
     - **PR `#359`** (created `2026-10-17T17:17:32Z`): `[claim] ihtp-ihtc2024-upper-bounds: i27 feasible schedule cost 50125 (was 50976; -851)`, reporting a feasible solution for `i27` with `Total cost = 50125` (`RoomAgeMix 292`, `RoomSkillLevel 3650`, `ContinuityOfCare 3103`, `ExcessiveNurseWorkload 590`, `OpenOperatingTheater 3210`, `SurgeonTransfer 290`, `PatientDelay 16490`, `ElectiveUnscheduledPatients 22500`).
   - **Comparison against PR `#359`**: The present claim (`claim/sol_i27.json`) achieves `Total violations = 0` and `Total cost = 50063`, which **strictly beats** both the live benchmark table (`50976`, improvement `-913`) and pending open PR `#359` (`50125`, improvement `-62`).

## 5. Verdict

The claimed solution `claim/sol_i27.json` (`Total violations = 0`, `Total cost = 50063`) strictly beats the official live benchmark record (`50976` on `https://ihtc2024.github.io/ihtp/index.html` at `2026-10-18T14:39:28Z`), strictly beats all bounds in the last 24 months of literature, and strictly beats pending open PR `#359` (`50125`) by `62` points.

pass: true
