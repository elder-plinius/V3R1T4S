# Skeptic Panel Report — Role: REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: ihtp-ihtc2024-upper-bounds
instance: i27
claimed_cost: 50063
previous_best_cost: 50976

## 1. Quoted Problem Definition and Success Criterion (`claim/CLAIM.md`)

Verbatim bank success criterion quoted from `claim/CLAIM.md`:

"A JSON solution file for at least one of the 60 IHTC-2024 instances (`i01`..`i30` or `m01`..`m30`) for which running the official validator `IHTP_Validator` on `(instance.json, solution.json)` reports `Total violations = 0` and a `Total cost` strictly smaller than the best known cost for that instance listed on https://ihtc2024.github.io/ihtp/index.html at claim time. Same-day claim since `IHTP_Validator` compiles in seconds and verifies a single instance/solution pair in under 1 second."

Mathematical specification quoted from `claim/CLAIM.md`:
- Planning horizon of $D$ days ($d \in \{0, \dots, D-1\}$), each divided into $S_{\text{day}} = 3$ shifts (`early`, `late`, `night`), giving $S = D \cdot S_{\text{day}}$ total shifts ($s = d \cdot S_{\text{day}} + \sigma \in \{0, \dots, S-1\}$).
- Nine Hard Constraints (`Total violations = 0` required):
  - **H1 (`RoomGenderMix`):** No room $r$ on day $d$ may simultaneously host gender `A` and gender `B` patients/occupants: $\sum_{r,d} \min(\text{count}_A(r,d), \text{count}_B(r,d)) = 0$.
  - **H2 (`PatientRoomCompatibility`):** No admitted patient $p$ may be assigned to a room $r_p \in \text{incompatible\_rooms}(p)$.
  - **H3 (`SurgeonOvertime`):** For every surgeon $u \in U$ and day $d$, total surgery duration of patients of surgeon $u$ admitted on day $d$ must not exceed $\text{max\_surgery\_time}(u, d)$.
  - **H4 (`OperatingTheaterOvertime`):** For every operating theater $t \in T$ and day $d$, total surgery duration of patients assigned to theater $t$ on day $d$ must not exceed $\text{availability}(t, d)$.
  - **H5 (`MandatoryUnscheduledPatients`):** Every mandatory patient $p$ (`mandatory == true`) must be scheduled (`admission_day != "none"`).
  - **H6 (`AdmissionDay`):** For every admitted patient $p$, $d_p \ge \text{surgery\_release\_day}(p)$, and if $p$ is mandatory, $d_p \le \text{surgery\_due\_day}(p)$.
  - **H7 (`RoomCapacity`):** For every room $r$ and day $d$, total occupants + admitted patients present in $r$ on day $d$ must not exceed $\text{capacity}(r)$.
  - **H8 (`NursePresence`):** Every nurse assignment must use a nurse $n$ who is working on shift $s$.
  - **H9 (`UncoveredRoom`):** Every occupied room $r \in R$ on every shift $s \in \{0, \dots, S-1\}$ must be assigned a working nurse.
- Eight Weighted Soft-Constraint Objective Components (weights for `i27` in `claim/i27.json`: $w_{\text{age}} = 1$, $w_{\text{skill}} = 10$, $w_{\text{coc}} = 1$, $w_{\text{work}} = 10$, $w_{\text{ot}} = 30$, $w_{\text{trans}} = 10$, $w_{\text{delay}} = 5$, $w_{\text{unsched}} = 500$):
  1. **`RoomAgeMix` ($w = 1$):** For each non-empty room $r$ and day $d$, $(\max_{q \in \text{occ}(r,d)} \text{age}(q) - \min_{q \in \text{occ}(r,d)} \text{age}(q))$.
  2. **`RoomSkillLevel` ($w = 10$):** For each room $r$, day $d$, shift $s = d \cdot S_{\text{day}} + \sigma$, and each patient/occupant $q \in \text{occ}(r,d)$, $\max(0, \text{skill\_req}(q, s_{\text{rel}}) - \text{skill}(n(r,s)))$, where $s_{\text{rel}}$ is $q$'s shift offset from admission.
  3. **`ContinuityOfCare` ($w = 1$):** For each occupant $o \in O$ and each admitted patient $p \in P$, the number of distinct nurses $|\{n(r_q, s) : s \in \text{stay\_shifts}(q)\}|$ covering $q$ during the planning horizon.
  4. **`ExcessiveNurseWorkload` ($w = 10$):** For each nurse $n \in N$ and each working shift $s$ of $n$, $\max(0, \sum_{r : n(r,s)=n} \sum_{q \in \text{occ}(r, \lfloor s/3 \rfloor)} \text{workload}(q, s_{\text{rel}}) - \text{max\_load}(n, s))$.
  5. **`OpenOperatingTheater` ($w = 30$):** Number of pairs $(t, d)$ with at least one surgery assigned to operating theater $t$ on day $d$.
  6. **`SurgeonTransfer` ($w = 10$):** For each surgeon $u$ and day $d$ where $u$ operates in $k_{u,d} \ge 1$ distinct operating theaters, $\max(0, k_{u,d} - 1)$.
  7. **`PatientDelay` ($w = 5$):** For each admitted patient $p$, $(d_p - \text{surgery\_release\_day}(p))$.
  8. **`ElectiveUnscheduledPatients` ($w = 500$):** Number of unscheduled optional patients.

*(Audit note on `claim/CLAIM.md` prose vs `claim/i27.json` / `claim/IHTP_Validator.cc`: In `claim/i27.json`, the exact entity counts are `days = 28`, `shifts = 84`, `rooms = 26`, `operating_theaters = 8`, `surgeons = 8`, `nurses = 55`, `occupants = 41`, `patients = 493`. Also, in `claim/IHTP_Validator.cc` line 980, `UncoveredRoom` checks `room_shift_nurse[r][s] == -1` when `room_day_patient_list[r][s/in.ShiftsPerDay()].size()` is positive, so only occupied room-shifts require a nurse; `claim/sol_i27.json` leaves 27 empty room-shifts unassigned and covers 100% of occupied room-shifts, yielding `UncoveredRoom = 0`.)*

## 2. File Integrity Verification (SHA-256 and Byte Sizes)

Verified via `shasum -a 256` and `wc -c` inside `claim/`:

| File | Bytes | SHA-256 Digest | Match `claim/REPRODUCE.md` |
|---|---:|---|---|
| `claim/sol_i27.json` | 209,120 | `900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7` | Exact match |
| `claim/i27.json` | 478,008 | `a4c3d597021eca59eb2ce37ef4de189eed25a8a91d51a466bbde5c42c54e4134` | Exact match |
| `claim/published_sol_i27.json` | 209,603 | `62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5` | Exact match |
| `claim/IHTP_Validator.cc` | 38,733 | `0b56fa75ea7de1d4a7e3dbd2d5b88e7ac779d69e4287e1247305d873a06a8afa` | Exact match |
| `claim/author_checker_ihtp_check.py` | 13,255 | `f39b76a6e1bcb0d724ac3c2cb700418b534a5f31be00f08f4d2fc94dbb09cd0c` | Exact match |
| `claim/seam_surgery_ihtp.cc` | 41,738 | `68cc31a103dd68223674f997634cdc6f72a46e7a5a7d214e029a4179ec263108` | Exact match |
| `claim/subset_nra_milp.py` | 10,153 | `981c68a6a00ea3b81a31d57a9ec3bd4e2c70f7a8fb94a76cf7f3fbd397647fba` | Exact match |
| `claim/ihtp_index.html` | 17,442 | `7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495` | Exact match |

In `claim/ihtp_index.html` (lines 247-249), the published best score for `i27` is confirmed as `50976`.

## 3. Independent Checker (`panel/reproduce_work/indep_ihtp_check.py`)

Before reading `claim/author_checker_ihtp_check.py` or `claim/IHTP_Validator.cc`, we wrote a standalone Python verifier `panel/reproduce_work/indep_ihtp_check.py` directly from the mathematical specification in `claim/CLAIM.md` and the JSON schema of `claim/i27.json` and `claim/sol_i27.json`.

### 3.1 Negative Mutation Self-Tests

We first tested `panel/reproduce_work/indep_ihtp_check.py` on five synthetic negative mutations of `claim/sol_i27.json` to ensure hard-constraint violations are caught:
- **Mutation 1** (unscheduling mandatory patient `p000`): detected `MandatoryUnscheduledPatients = 1`.
- **Mutation 2** (removing occupied room `r24` on day 0 `late` from nurse `n012`): detected `UncoveredRoom = 1`.
- **Mutation 3** (assigning patient `p000` to incompatible room `r09`): detected `PatientRoomCompatibility = 1`.
- **Mutation 4** (admitting patient `p000` on day 3 before `surgery_release_day = 4`): detected `AdmissionDay = 1`.
- **Mutation 5** (assigning nurse `n000` on non-working shift day 0 `early`): detected `NursePresence = 1`.

### 3.2 Independent Evaluation of `claim/published_sol_i27.json` and `claim/sol_i27.json` (Two Deterministic Runs)

Running `panel/reproduce_work/indep_ihtp_check.py` on `claim/published_sol_i27.json` and twice on `claim/sol_i27.json` produced identical, deterministic results matching `claim/CLAIM.md`:

```text
File: published_sol_i27.json (209603 bytes, sha256=62669ec464f96211d362f2f4af07ac4913178975511d309110bd75e81493d1d5)
Hard constraint violations: {'RoomGenderMix': 0, 'PatientRoomCompatibility': 0, 'SurgeonOvertime': 0, 'OperatingTheaterOvertime': 0, 'MandatoryUnscheduledPatients': 0, 'AdmissionDay': 0, 'RoomCapacity': 0, 'NursePresence': 0, 'UncoveredRoom': 0}
Total violations = 0
Soft constraint costs:
  RoomAgeMix                  : 298
  RoomSkillLevel              : 3930
  ContinuityOfCare            : 3518
  ExcessiveNurseWorkload      : 740
  OpenOperatingTheater        : 3210
  SurgeonTransfer             : 290
  PatientDelay                : 16490
  ElectiveUnscheduledPatients : 22500
Total cost = 50976
VERIFIED: Total violations = 0 and Total cost = 50976

=== Determinism Run 1 on sol_i27.json ===
File: sol_i27.json (209120 bytes, sha256=900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7)
Hard constraint violations: {'RoomGenderMix': 0, 'PatientRoomCompatibility': 0, 'SurgeonOvertime': 0, 'OperatingTheaterOvertime': 0, 'MandatoryUnscheduledPatients': 0, 'AdmissionDay': 0, 'RoomCapacity': 0, 'NursePresence': 0, 'UncoveredRoom': 0}
Total violations = 0
Soft constraint costs:
  RoomAgeMix                  : 298
  RoomSkillLevel              : 3610
  ContinuityOfCare            : 3045
  ExcessiveNurseWorkload      : 620
  OpenOperatingTheater        : 3210
  SurgeonTransfer             : 290
  PatientDelay                : 16490
  ElectiveUnscheduledPatients : 22500
Total cost = 50063
VERIFIED: Total violations = 0 and Total cost = 50063

=== Determinism Run 2 on sol_i27.json ===
File: sol_i27.json (209120 bytes, sha256=900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7)
Hard constraint violations: {'RoomGenderMix': 0, 'PatientRoomCompatibility': 0, 'SurgeonOvertime': 0, 'OperatingTheaterOvertime': 0, 'MandatoryUnscheduledPatients': 0, 'AdmissionDay': 0, 'RoomCapacity': 0, 'NursePresence': 0, 'UncoveredRoom': 0}
Total violations = 0
Soft constraint costs:
  RoomAgeMix                  : 298
  RoomSkillLevel              : 3610
  ContinuityOfCare            : 3045
  ExcessiveNurseWorkload      : 620
  OpenOperatingTheater        : 3210
  SurgeonTransfer             : 290
  PatientDelay                : 16490
  ElectiveUnscheduledPatients : 22500
Total cost = 50063
VERIFIED: Total violations = 0 and Total cost = 50063
```

## 4. Verification with Author Checker (`claim/author_checker_ihtp_check.py`) and Official C++ Validator (`claim/IHTP_Validator.cc`)

After completing the independent checker, we inspected and executed `claim/author_checker_ihtp_check.py` and compiled and ran `claim/IHTP_Validator.cc` on both `claim/published_sol_i27.json` and `claim/sol_i27.json`.

### 4.1 Output of `claim/author_checker_ihtp_check.py`

- On `claim/published_sol_i27.json`: `Total violations = 0`, `Total cost = 50976`, `IHTP_CHECK: PASS`.
- On `claim/sol_i27.json`: `Total violations = 0`, `Total cost = 50063`, `IHTP_CHECK: PASS`.

### 4.2 Output of Official C++ Validator (`claim/IHTP_Validator.cc`)

On `claim/published_sol_i27.json`:
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
RoomAgeMix...........................298 (  1 X 298)
RoomSkillLevel......................3930 ( 10 X 393)
ContinuityOfCare....................3518 (  1 X 3518)
ExcessiveNurseWorkload...............740 ( 10 X  74)
OpenOperatingTheater................3210 ( 30 X 107)
SurgeonTransfer......................290 ( 10 X  29)
PatientDelay.......................16490 (  5 X 3298)
ElectiveUnscheduledPatients........22500 (500 X  45)
Total cost = 50976
```

On `claim/sol_i27.json`:
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
RoomAgeMix...........................298 (  1 X 298)
RoomSkillLevel......................3610 ( 10 X 361)
ContinuityOfCare....................3045 (  1 X 3045)
ExcessiveNurseWorkload...............620 ( 10 X  62)
OpenOperatingTheater................3210 ( 30 X 107)
SurgeonTransfer......................290 ( 10 X  29)
PatientDelay.......................16490 (  5 X 3298)
ElectiveUnscheduledPatients........22500 (500 X  45)
Total cost = 50063
```

All three verifiers (`panel/reproduce_work/indep_ihtp_check.py`, `claim/author_checker_ihtp_check.py`, and `claim/IHTP_Validator.cc`) agree 100% on every hard-constraint violation count (`0`) and every soft-constraint component cost (`50976` for `claim/published_sol_i27.json` and `50063` for `claim/sol_i27.json`, a strict improvement of `-913`).

pass: true
