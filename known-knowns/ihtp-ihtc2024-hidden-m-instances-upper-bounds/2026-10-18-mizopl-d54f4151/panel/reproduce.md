# Panelist Report: REPRODUCE (`m28`)

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: ihtp-ihtc2024-hidden-m-instances-upper-bounds
instance: m28

## 1. Quoted Problem Definition & Success Criterion

From `claim/CLAIM.md`:

> A solution JSON for one of m01-m30 that the official IHTP_Validator reports with zero hard-constraint violations and total cost STRICTLY LOWER (direction: min) than the m-instance cost listed on https://ihtc2024.github.io/ihtp/index.html, re-fetched live immediately before claiming, and lower than any value for that instance found by the NOVELTY check in later IHTP papers.

Mathematical specification quoted from `claim/CLAIM.md`:
- Horizon $D = 28$ days ($d \in \{0, \dots, 27\}$), $S_{\text{day}} = 3$ shifts (`early`, `late`, `night`), $S = 84$ total shifts ($s = 3d + \sigma \in \{0, \dots, 83\}$).
- Instance `m28` cardinalities: $|R| = 42$ rooms, $|T| = 11$ operating theaters, $|U| = 10$ surgeons, $|N| = 84$ nurses, $|O| = 36$ pre-existing occupants, $|P| = 611$ patients ($420$ mandatory, $191$ optional).
- Nine hard constraints (`Total violations = 0` required): `H1 (RoomGenderMix)`, `H2 (PatientRoomCompatibility)`, `H3 (SurgeonOvertime)`, `H4 (OperatingTheaterOvertime)`, `H5 (MandatoryUnscheduledPatients)`, `H6 (AdmissionDay)`, `H7 (RoomCapacity)`, `H8 (NursePresence)`, `H9 (UncoveredRoom)`.
- Eight weighted soft-constraint objective components with instance weights $w_{\text{age}} = 1$, $w_{\text{skill}} = 5$, $w_{\text{coc}} = 5$, $w_{\text{work}} = 5$, $w_{\text{ot}} = 40$, $w_{\text{trans}} = 10$, $w_{\text{delay}} = 10$, $w_{\text{unsched}} = 350$.

## 2. File Integrity & Cryptographic Hashes

All files in `claim/` were verified via `shasum -a 256` and `wc -c`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `claim/sol_m28.json` | `307109` | `d54f4151a022f91800fdc8a12226a5bc4da6d47ce2dcf51c575b36ead51b79c7` |
| `claim/m28.json` | `639445` | `37061eb156c592feac39f5f148a5cfe4b594a57853638b0f2b041dd84c8f90e0` |
| `claim/published_sol_m28.json` | `484775` | `4dff74744082ab6b04608cc13186aef635350ccf2cd92018ba443e1d85113cda` |
| `claim/ihtp_index.html` | `17442` | `7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495` |
| `claim/IHTP_Validator.cc` | `38733` | `0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa` |
| `claim/author_checker_ihtp_check.py` | `13255` | `f39b76a6e1bcb0d724ac3c2cb700418b534a5f31be00f08f4d2fc94dbb09cd0c` |

In `claim/ihtp_index.html`, the table entry for `m28` lists best known cost `45913` linking to `sol_m28.json`.

## 3. Independent Checker (`reproduce_work/indep_ihtp_check.py`) Written Before Reading Author Code

Before reading `claim/author_checker_ihtp_check.py` or `claim/IHTP_Validator.cc`, we wrote a standalone checker `reproduce_work/indep_ihtp_check.py` (`11229` bytes) directly from the mathematical definition in `claim/CLAIM.md` and the JSON schema of `claim/m28.json` and `claim/sol_m28.json`.

### 3.1 Negative Mutation Sanity Tests

We tested `reproduce_work/indep_ihtp_check.py` on 5 synthetic corrupted mutations of `claim/sol_m28.json` to ensure hard-constraint violations are caught and never silently ignored:
1. Unscheduling mandatory patient `p000` (`admission_day = "none"`): reported `MandatoryUnscheduledPatients = 1`, `Total violations = 1`.
2. Moving patient `p000` to incompatible room `r10`: reported `PatientRoomCompatibility = 1`, `Total violations = 10`.
3. Setting patient `p000` `admission_day = 0` (before `surgery_release_day = 3`): reported `AdmissionDay = 1`, `Total violations = 574`.
4. Removing room assignments from nurse `n000` on day `0` shift `night`: reported `UncoveredRoom = 3`, `Total violations = 3`.
5. Assigning nurse `n000` to non-working shift `(day 0, early)`: reported `NursePresence = 1`, `Total violations = 2`.

### 3.2 Independent Verification of `claim/published_sol_m28.json` and `claim/sol_m28.json`

Running `reproduce_work/indep_ihtp_check.py` on `claim/published_sol_m28.json` and twice on `claim/sol_m28.json` (elapsed `16.78 ms` per run, confirming exact determinism) yielded:

| Metric / Component | Weight | `claim/published_sol_m28.json` | `claim/sol_m28.json` (Run 1) | `claim/sol_m28.json` (Run 2) | Delta |
|---|---:|---:|---:|---:|---:|
| `H1 RoomGenderMix` | hard | `0` | `0` | `0` | `0` |
| `H2 PatientRoomCompatibility` | hard | `0` | `0` | `0` | `0` |
| `H3 SurgeonOvertime` | hard | `0` | `0` | `0` | `0` |
| `H4 OperatingTheaterOvertime` | hard | `0` | `0` | `0` | `0` |
| `H5 MandatoryUnscheduledPatients` | hard | `0` | `0` | `0` | `0` |
| `H6 AdmissionDay` | hard | `0` | `0` | `0` | `0` |
| `H7 RoomCapacity` | hard | `0` | `0` | `0` | `0` |
| `H8 NursePresence` | hard | `0` | `0` | `0` | `0` |
| `H9 UncoveredRoom` | hard | `0` | `0` | `0` | `0` |
| **Total violations** | — | **`0`** | **`0`** | **`0`** | **`0`** |
| `RoomAgeMix` | `1` | `58` (raw `58`) | `58` (raw `58`) | `58` (raw `58`) | `0` |
| `RoomSkillLevel` | `5` | `1565` (raw `313`) | `1560` (raw `312`) | `1560` (raw `312`) | `-5` |
| `ContinuityOfCare` | `5` | `13920` (raw `2784`) | `13875` (raw `2775`) | `13875` (raw `2775`) | `-45` |
| `ExcessiveNurseWorkload` | `5` | `170` (raw `34`) | `180` (raw `36`) | `180` (raw `36`) | `+10` |
| `OpenOperatingTheater` | `40` | `4880` (raw `122`) | `4880` (raw `122`) | `4880` (raw `122`) | `0` |
| `SurgeonTransfer` | `10` | `480` (raw `48`) | `480` (raw `48`) | `480` (raw `48`) | `0` |
| `PatientDelay` | `10` | `16440` (raw `1644`) | `16440` (raw `1644`) | `16440` (raw `1644`) | `0` |
| `ElectiveUnscheduledPatients` | `350` | `8400` (raw `24`) | `8400` (raw `24`) | `8400` (raw `24`) | `0` |
| **Total cost** | — | **`45913`** | **`45873`** | **`45873`** | **`-40`** |

Structural comparison between `claim/published_sol_m28.json` and `claim/sol_m28.json` shows `0/611` patient admission/room/theater assignments changed and `81/84` nurse-to-room assignment schedules were re-optimized, reducing `RoomSkillLevel` by `5` (`313 -> 312`) and `ContinuityOfCare` by `45` (`2784 -> 2775`) at the expense of `+10` on `ExcessiveNurseWorkload` (`34 -> 36`), for a net exact reduction of `-40` (`45913 -> 45873`).

## 4. Author Checker & Official C++ Validator Cross-Check

After completing independent verification, we inspected and executed `claim/author_checker_ihtp_check.py` and compiled and ran `claim/IHTP_Validator.cc` (removing the compiled binary after execution).

Verbatim output of `claim/IHTP_Validator.cc` on `claim/sol_m28.json`:
```text
VIOLATIONS: 
RoomGenderMix.....................0
PatientRoomCompatibility..........0
SurgeonOvertime...................0
OperatingTheaterOvertime..........0
MandatoryUnscheduledPatients......0
AdmissionDay......................0
RoomCapacity......................0
NursePresence.....................0
UncoveredRoom.....................0
Total violations = 0

COSTS (weight X cost): 
RoomAgeMix............................58 (  1 X  58)
RoomSkillLevel......................1560 (  5 X 312)
ContinuityOfCare...................13875 (  5 X 2775)
ExcessiveNurseWorkload...............180 (  5 X  36)
OpenOperatingTheater................4880 ( 40 X 122)
SurgeonTransfer......................480 ( 10 X  48)
PatientDelay.......................16440 ( 10 X 1644)
ElectiveUnscheduledPatients.........8400 (350 X  24)
Total cost = 45873
```

All three verifiers (`reproduce_work/indep_ihtp_check.py`, `claim/author_checker_ihtp_check.py`, and `claim/IHTP_Validator.cc`) agree 100% on every hard constraint (`0` violations) and every soft-constraint component (`Total cost = 45873` vs `45913`).

pass: true
