// CLSS Coupled Seam Surgery Solver v2 for IHTC-2024 (ihtp-ihtc2024-upper-bounds)
// Built directly on the official IHTP_Validator data structures for 100% exact cost/violation parity.
// Compile: clang++ -O3 -std=c++17 seam_surgery_ihtp.cc -o seam_surgery_ihtp

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <random>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <tuple>
#include "json.hpp"

using namespace std;

enum class Gender { A, B };

struct Occupant {
  string id;
  Gender gender;
  int age_group;
  int length_of_stay;
  vector<int> workload_produced;
  vector<int> skill_level_required;
  int assigned_room = -1;
};

struct Patient : public Occupant {
  bool mandatory;
  int surgery_release_day;
  int surgery_due_day;
  int surgery_duration;
  int surgeon;
  vector<bool> incompatible_rooms;
};

struct Surgeon {
  string id;
  vector<int> max_surgery_time;
};

struct OperatingTheater {
  string id;
  vector<int> availability;
};

struct Room {
  string id;
  int capacity;
};

struct Nurse {
  string id;
  int skill_level;
  vector<int> working_shifts;
  vector<bool> is_working_in_shift;
  vector<int> max_loads;
};

class IHTP_Input {
 public:
  IHTP_Input(string file_name);
  int Days() const { return days; }
  int ShiftsPerDay() const { return shifts_per_day; }
  int Shifts() const { return shifts; }
  int Patients() const { return patients; }
  int Occupants() const { return occupants; }
  int SkillLevels() const { return skill_levels; }
  int AgeGroups() const { return age_groups; }
  int Surgeons() const { return surgeons; }
  int OperatingTheaters() const { return operating_theaters; }
  int Rooms() const { return rooms; }
  int Nurses() const { return nurses; }

  string NurseId(int n) const { return nurses_vect[n].id; }
  int NurseSkillLevel(int n) const { return nurses_vect[n].skill_level; }
  bool IsNurseWorkingInShift(int n, int s) const { return nurses_vect[n].is_working_in_shift[s]; }
  int NurseWorkingShifts(int n) const { return nurses_vect[n].working_shifts.size(); }
  int NurseWorkingShift(int n, int i) const { return nurses_vect[n].working_shifts[i]; }
  int AvailableNurses(int s) const { return available_nurses[s].size(); }
  int AvailableNurse(int s, int i) const { return available_nurses[s][i]; }
  const vector<int>& AvailableNursesVec(int s) const { return available_nurses[s]; }
  int NurseMaxLoad(int n, int s) const { return nurses_vect[n].max_loads[s]; }

  string OccupantId(int p) const { return occupants_vect[p].id; }
  Gender OccupantGender(int p) const { return occupants_vect[p].gender; }
  int OccupantAgeGroup(int p) const { return occupants_vect[p].age_group; }
  int OccupantLengthOfStay(int p) const { return occupants_vect[p].length_of_stay; }
  int OccupantRoom(int p) const { return occupants_vect[p].assigned_room; }
  int OccupantSkillLevelRequired(int p, int s) const { return occupants_vect[p].skill_level_required[s]; }
  int OccupantWorkloadProduced(int p, int s) const { return occupants_vect[p].workload_produced[s]; }

  string PatientId(int p) const { return patients_vect[p].id; }
  Gender PatientGender(int p) const { return patients_vect[p].gender; }
  int PatientSurgeryReleaseDay(int p) const { return patients_vect[p].surgery_release_day; }
  int PatientAgeGroup(int p) const { return patients_vect[p].age_group; }
  int PatientLengthOfStay(int p) const { return patients_vect[p].length_of_stay; }
  int PatientSurgeryDueDay(int p) const { return patients_vect[p].surgery_due_day; }
  int PatientLastPossibleDay(int p) const { return PatientMandatory(p) ? patients_vect[p].surgery_due_day : days - 1; }
  int PatientSurgeryDuration(int p) const { return patients_vect[p].surgery_duration; }
  int PatientSurgeon(int p) const { return patients_vect[p].surgeon; }
  bool PatientMandatory(int p) const { return patients_vect[p].mandatory; }
  bool IncompatibleRoom(int p, int r) const { return patients_vect[p].incompatible_rooms[r]; }
  int PatientSkillLevelRequired(int p, int s) const { return patients_vect[p].skill_level_required[s]; }
  int PatientWorkloadProduced(int p, int s) const { return patients_vect[p].workload_produced[s]; }

  string RoomId(int r) const { return rooms_vect[r].id; }
  int RoomCapacity(int r) const { return rooms_vect[r].capacity; }

  string OperatingTheaterId(int t) const { return operating_theaters_vect[t].id; }
  string SurgeonId(int u) const { return surgeons_vect[u].id; }
  int OperatingTheaterAvailability(int t, int d) const { return operating_theaters_vect[t].availability[d]; }
  int SurgeonMaxSurgeryTime(int s, int d) const { return surgeons_vect[s].max_surgery_time[d]; }
  string ShiftName(int s) const { return shift_names[s]; }
  int Weight(int c) const { return weights[c]; }

  int FindAgeGroup(string age_group_name) const;
  int FindSurgeon(string surgeon_id) const;
  int FindShift(string shift_name) const;
  int FindRoom(string room_name) const;
  int FindOperatingTheater(string ot_name) const;
  int FindPatient(string patient_id) const;
  int FindNurse(string nurse_id) const;

 private:
  int days, shifts_per_day, shifts, patients, occupants, skill_levels, age_groups, surgeons, operating_theaters, rooms, nurses;
  const int SOFT_COST_COMPONENTS = 8;
  vector<Patient> patients_vect;
  vector<Occupant> occupants_vect;
  vector<Surgeon> surgeons_vect;
  vector<OperatingTheater> operating_theaters_vect;
  vector<Room> rooms_vect;
  vector<Nurse> nurses_vect;
  vector<string> shift_names, age_group_names;
  vector<vector<vector<int>>> room_day_fixed_list;
  vector<vector<int>> available_nurses;
  vector<int> weights;
  void ResizeDataStructures();
};

IHTP_Input::IHTP_Input(string file_name) : weights(SOFT_COST_COMPONENTS) {
  unsigned i;
  int d, f, p, n, ag, sn, s, r, ot;
  nlohmann::json j_in, j_f, j_p, j_r, j_s, j_ot, j_n;
  ifstream is(file_name);
  if (!is) throw invalid_argument("Cannot open input file " + file_name);
  is >> j_in;

  weights[0] = j_in["weights"]["room_mixed_age"];
  weights[1] = j_in["weights"]["room_nurse_skill"];
  weights[2] = j_in["weights"]["continuity_of_care"];
  weights[3] = j_in["weights"]["nurse_eccessive_workload"];
  weights[4] = j_in["weights"]["open_operating_theater"];
  weights[5] = j_in["weights"]["surgeon_transfer"];
  weights[6] = j_in["weights"]["patient_delay"];
  weights[7] = j_in["weights"]["unscheduled_optional"];

  days = j_in["days"];
  shifts_per_day = j_in["shift_types"].size();
  shifts = days * shifts_per_day;
  skill_levels = j_in["skill_levels"];
  occupants = j_in["occupants"].size();
  patients = j_in["patients"].size();
  surgeons = j_in["surgeons"].size();
  operating_theaters = j_in["operating_theaters"].size();
  rooms = j_in["rooms"].size();
  nurses = j_in["nurses"].size();
  age_groups = j_in["age_groups"].size();

  ResizeDataStructures();

  for (sn = 0; sn < shifts_per_day; sn++) shift_names[sn] = j_in["shift_types"][sn];
  for (ag = 0; ag < age_groups; ag++) age_group_names[ag] = j_in["age_groups"][ag];
  for (s = 0; s < surgeons; s++) {
    j_s = j_in["surgeons"][s];
    surgeons_vect[s].id = j_s["id"];
    for (d = 0; d < days; d++) surgeons_vect[s].max_surgery_time[d] = j_s["max_surgery_time"][d];
  }
  for (ot = 0; ot < operating_theaters; ot++) {
    j_ot = j_in["operating_theaters"][ot];
    operating_theaters_vect[ot].id = j_ot["id"];
    for (d = 0; d < days; d++) operating_theaters_vect[ot].availability[d] = j_ot["availability"][d];
  }
  for (r = 0; r < rooms; r++) {
    j_r = j_in["rooms"][r];
    rooms_vect[r].id = j_r["id"];
    rooms_vect[r].capacity = j_r["capacity"];
  }
  room_day_fixed_list.resize(rooms, vector<vector<int>>(days));
  for (f = 0; f < occupants; f++) {
    j_f = j_in["occupants"][f];
    occupants_vect[f].id = j_f["id"];
    occupants_vect[f].gender = (j_f["gender"] == "A") ? Gender::A : Gender::B;
    occupants_vect[f].age_group = FindAgeGroup(j_f["age_group"]);
    occupants_vect[f].length_of_stay = j_f["length_of_stay"];
    occupants_vect[f].workload_produced.resize(occupants_vect[f].length_of_stay * shifts_per_day);
    occupants_vect[f].skill_level_required.resize(occupants_vect[f].length_of_stay * shifts_per_day);
    for (s = 0; s < occupants_vect[f].length_of_stay * shifts_per_day; s++) {
      occupants_vect[f].workload_produced[s] = j_f["workload_produced"][s];
      occupants_vect[f].skill_level_required[s] = j_f["skill_level_required"][s];
    }
    r = FindRoom(j_f["room_id"]);
    occupants_vect[f].assigned_room = r;
    for (d = 0; d < occupants_vect[f].length_of_stay; d++) room_day_fixed_list[r][d].push_back(f);
  }
  for (p = 0; p < patients; p++) {
    j_p = j_in["patients"][p];
    patients_vect[p].id = j_p["id"];
    patients_vect[p].mandatory = j_p["mandatory"];
    patients_vect[p].gender = (j_p["gender"] == "A") ? Gender::A : Gender::B;
    patients_vect[p].age_group = FindAgeGroup(j_p["age_group"]);
    patients_vect[p].length_of_stay = j_p["length_of_stay"];
    patients_vect[p].surgery_release_day = j_p["surgery_release_day"];
    patients_vect[p].surgery_due_day = patients_vect[p].mandatory ? (int)j_p["surgery_due_day"] : -1;
    patients_vect[p].surgery_duration = j_p["surgery_duration"];
    patients_vect[p].surgeon = FindSurgeon(j_p["surgeon_id"]);
    if (!j_p["incompatible_room_ids"].is_null()) {
      for (i = 0; i < j_p["incompatible_room_ids"].size(); i++) {
        r = FindRoom(j_p["incompatible_room_ids"][i]);
        patients_vect[p].incompatible_rooms[r] = true;
      }
    }
    patients_vect[p].workload_produced.resize(patients_vect[p].length_of_stay * shifts_per_day);
    patients_vect[p].skill_level_required.resize(patients_vect[p].length_of_stay * shifts_per_day);
    for (s = 0; s < patients_vect[p].length_of_stay * shifts_per_day; s++) {
      patients_vect[p].workload_produced[s] = j_p["workload_produced"][s];
      patients_vect[p].skill_level_required[s] = j_p["skill_level_required"][s];
    }
  }
  for (n = 0; n < nurses; n++) {
    j_n = j_in["nurses"][n];
    nurses_vect[n].id = j_n["id"];
    nurses_vect[n].skill_level = j_n["skill_level"];
    for (i = 0; i < j_n["working_shifts"].size(); i++) {
      s = static_cast<int>(j_n["working_shifts"][i]["day"]) * shifts_per_day + FindShift(j_n["working_shifts"][i]["shift"]);
      nurses_vect[n].working_shifts.push_back(s);
      nurses_vect[n].is_working_in_shift[s] = true;
      nurses_vect[n].max_loads[s] = j_n["working_shifts"][i]["max_load"];
      available_nurses[s].push_back(n);
    }
  }
}

void IHTP_Input::ResizeDataStructures() {
  occupants_vect.resize(occupants);
  patients_vect.resize(patients);
  for (int p = 0; p < patients; p++) patients_vect[p].incompatible_rooms.resize(rooms, false);
  surgeons_vect.resize(surgeons);
  for (int s = 0; s < surgeons; s++) surgeons_vect[s].max_surgery_time.resize(days);
  operating_theaters_vect.resize(operating_theaters);
  for (int ot = 0; ot < operating_theaters; ot++) operating_theaters_vect[ot].availability.resize(days);
  rooms_vect.resize(rooms);
  nurses_vect.resize(nurses);
  for (int n = 0; n < nurses; n++) {
    nurses_vect[n].is_working_in_shift.resize(shifts, false);
    nurses_vect[n].max_loads.resize(shifts, 0);
  }
  available_nurses.resize(shifts);
  shift_names.resize(shifts_per_day);
  age_group_names.resize(age_groups);
}

int IHTP_Input::FindAgeGroup(string s) const { for (int i = 0; i < age_groups; i++) if (s == age_group_names[i]) return i; throw invalid_argument("ag"); }
int IHTP_Input::FindSurgeon(string s) const { for (int i = 0; i < surgeons; i++) if (s == surgeons_vect[i].id) return i; throw invalid_argument("surg"); }
int IHTP_Input::FindShift(string s) const { for (int i = 0; i < shifts_per_day; i++) if (s == shift_names[i]) return i; throw invalid_argument("sh"); }
int IHTP_Input::FindRoom(string s) const { for (int i = 0; i < rooms; i++) if (s == rooms_vect[i].id) return i; throw invalid_argument("rm"); }
int IHTP_Input::FindOperatingTheater(string s) const { for (int i = 0; i < operating_theaters; i++) if (s == operating_theaters_vect[i].id) return i; throw invalid_argument("ot"); }
int IHTP_Input::FindPatient(string s) const { for (int i = 0; i < patients; i++) if (s == patients_vect[i].id) return i; throw invalid_argument("pat"); }
int IHTP_Input::FindNurse(string s) const { for (int i = 0; i < nurses; i++) if (s == nurses_vect[i].id) return i; throw invalid_argument("nrs"); }

class FastSchedule {
 public:
  const IHTP_Input& in;
  int P, O, Q, R, D, SPD, S, N, T, U;
  int w_age, w_skill, w_coc, w_work, w_ot, w_trans, w_delay, w_unsched;

  vector<int> admission_day;
  vector<int> room;
  vector<int> operating_room;
  vector<vector<int>> rs_nurse;

  vector<vector<int>> room_day_occ_count;
  vector<vector<int>> rd_a, rd_b;
  vector<vector<int>> ot_load, surg_load;
  vector<vector<vector<int>>> room_day_people;
  vector<vector<int>> rs_load;
  vector<vector<vector<int>>> rs_skill_pen;
  vector<vector<int>> ns_load;
  vector<vector<int>> q_nurse_cnt;
  vector<int> q_distinct_nurses;
  vector<int> q_room;
  vector<int> q_start_day, q_end_day;

  int cur_skill_unw = 0;
  int cur_work_unw = 0;
  int cur_coc_unw = 0;
  int cur_base_cost = 0;

  FastSchedule(const IHTP_Input& inp)
    : in(inp), P(inp.Patients()), O(inp.Occupants()), Q(P + O),
      R(inp.Rooms()), D(inp.Days()), SPD(inp.ShiftsPerDay()), S(inp.Shifts()),
      N(inp.Nurses()), T(inp.OperatingTheaters()), U(inp.Surgeons()) {
    w_age = in.Weight(0);
    w_skill = in.Weight(1);
    w_coc = in.Weight(2);
    w_work = in.Weight(3);
    w_ot = in.Weight(4);
    w_trans = in.Weight(5);
    w_delay = in.Weight(6);
    w_unsched = in.Weight(7);

    admission_day.assign(P, -1);
    room.assign(P, -1);
    operating_room.assign(P, -1);
    rs_nurse.assign(R, vector<int>(S, -1));
  }

  void LoadJSON(const string& file_name) {
    nlohmann::json j_sol;
    ifstream is(file_name);
    if (!is) throw invalid_argument("Cannot open " + file_name);
    is >> j_sol;
    admission_day.assign(P, -1);
    room.assign(P, -1);
    operating_room.assign(P, -1);
    for (int r = 0; r < R; r++)
      for (int s = 0; s < S; s++)
        rs_nurse[r][s] = in.AvailableNurse(s, 0);

    for (size_t i = 0; i < j_sol["patients"].size(); i++) {
      auto& jp = j_sol["patients"][i];
      if (jp["admission_day"] != "none") {
        int p = in.FindPatient(jp["id"]);
        admission_day[p] = jp["admission_day"];
        room[p] = in.FindRoom(jp["room"]);
        operating_room[p] = in.FindOperatingTheater(jp["operating_theater"]);
      }
    }
    for (size_t i = 0; i < j_sol["nurses"].size(); i++) {
      auto& jn = j_sol["nurses"][i];
      int n = in.FindNurse(jn["id"]);
      for (size_t j = 0; j < jn["assignments"].size(); j++) {
        int d = jn["assignments"][j]["day"];
        int sn = in.FindShift(jn["assignments"][j]["shift"]);
        int s = d * SPD + sn;
        for (size_t k = 0; k < jn["assignments"][j]["rooms"].size(); k++) {
          int r = in.FindRoom(jn["assignments"][j]["rooms"][k]);
          rs_nurse[r][s] = n;
        }
      }
    }
    RebuildAll();
  }

  void SaveJSON(const string& file_name) const {
    nlohmann::json j_out;
    j_out["patients"] = nlohmann::json::array();
    for (int p = 0; p < P; p++) {
      nlohmann::json jp;
      jp["id"] = in.PatientId(p);
      if (admission_day[p] == -1) {
        jp["admission_day"] = "none";
      } else {
        jp["admission_day"] = admission_day[p];
        jp["room"] = in.RoomId(room[p]);
        jp["operating_theater"] = in.OperatingTheaterId(operating_room[p]);
      }
      j_out["patients"].push_back(jp);
    }
    j_out["nurses"] = nlohmann::json::array();
    for (int n = 0; n < N; n++) {
      nlohmann::json jn;
      jn["id"] = in.NurseId(n);
      jn["assignments"] = nlohmann::json::array();
      for (int ws_i = 0; ws_i < in.NurseWorkingShifts(n); ws_i++) {
        int s = in.NurseWorkingShift(n, ws_i);
        int d = s / SPD;
        int sn = s % SPD;
        nlohmann::json ja;
        ja["day"] = d;
        ja["shift"] = in.ShiftName(sn);
        ja["rooms"] = nlohmann::json::array();
        for (int r = 0; r < R; r++) {
          if (room_day_occ_count[r][d] > 0 && rs_nurse[r][s] == n) {
            ja["rooms"].push_back(in.RoomId(r));
          }
        }
        jn["assignments"].push_back(ja);
      }
      j_out["nurses"].push_back(jn);
    }
    ofstream os(file_name);
    os << j_out.dump(2) << endl;
  }

  pair<int, int> EvaluatePatientLayer() {
    int viol = 0;
    rd_a.assign(R, vector<int>(D, 0));
    rd_b.assign(R, vector<int>(D, 0));
    vector<vector<int>> rd_cnt(R, vector<int>(D, 0));
    vector<vector<int>> rd_min_age(R, vector<int>(D, 1000000));
    vector<vector<int>> rd_max_age(R, vector<int>(D, -1));
    ot_load.assign(T, vector<int>(D, 0));
    surg_load.assign(U, vector<int>(D, 0));
    vector<vector<vector<int>>> surg_ot(U, vector<vector<int>>(D, vector<int>(T, 0)));

    for (int o = 0; o < O; o++) {
      int r = in.OccupantRoom(o);
      int ag = in.OccupantAgeGroup(o);
      Gender g = in.OccupantGender(o);
      for (int d = 0; d < min(D, in.OccupantLengthOfStay(o)); d++) {
        rd_cnt[r][d]++;
        if (g == Gender::A) rd_a[r][d]++; else rd_b[r][d]++;
        if (ag < rd_min_age[r][d]) rd_min_age[r][d] = ag;
        if (ag > rd_max_age[r][d]) rd_max_age[r][d] = ag;
      }
    }

    int delay_unw = 0;
    int unsched_unw = 0;
    for (int p = 0; p < P; p++) {
      int ad = admission_day[p];
      if (ad == -1) {
        if (in.PatientMandatory(p)) viol++;
        else unsched_unw++;
        continue;
      }
      int r = room[p];
      int t = operating_room[p];
      if (ad < in.PatientSurgeryReleaseDay(p) || ad > in.PatientLastPossibleDay(p)) viol++;
      if (in.IncompatibleRoom(p, r)) viol++;
      if (ad > in.PatientSurgeryReleaseDay(p)) delay_unw += (ad - in.PatientSurgeryReleaseDay(p));

      int dur = in.PatientSurgeryDuration(p);
      int u = in.PatientSurgeon(p);
      ot_load[t][ad] += dur;
      surg_load[u][ad] += dur;
      surg_ot[u][ad][t]++;

      int ag = in.PatientAgeGroup(p);
      Gender g = in.PatientGender(p);
      int los = in.PatientLengthOfStay(p);
      for (int d = ad; d < min(D, ad + los); d++) {
        rd_cnt[r][d]++;
        if (g == Gender::A) rd_a[r][d]++; else rd_b[r][d]++;
        if (ag < rd_min_age[r][d]) rd_min_age[r][d] = ag;
        if (ag > rd_max_age[r][d]) rd_max_age[r][d] = ag;
      }
    }

    int age_unw = 0;
    for (int r = 0; r < R; r++) {
      int cap = in.RoomCapacity(r);
      for (int d = 0; d < D; d++) {
        if (rd_cnt[r][d] > cap) viol += (rd_cnt[r][d] - cap);
        viol += min(rd_a[r][d], rd_b[r][d]);
        if (rd_cnt[r][d] > 0 && rd_max_age[r][d] > rd_min_age[r][d])
          age_unw += (rd_max_age[r][d] - rd_min_age[r][d]);
      }
    }

    int open_ot_unw = 0;
    for (int t = 0; t < T; t++) {
      for (int d = 0; d < D; d++) {
        if (ot_load[t][d] > in.OperatingTheaterAvailability(t, d))
          viol += (ot_load[t][d] - in.OperatingTheaterAvailability(t, d));
        if (ot_load[t][d] > 0) open_ot_unw++;
      }
    }

    int trans_unw = 0;
    for (int u = 0; u < U; u++) {
      for (int d = 0; d < D; d++) {
        if (surg_load[u][d] > in.SurgeonMaxSurgeryTime(u, d))
          viol += (surg_load[u][d] - in.SurgeonMaxSurgeryTime(u, d));
        int cnt = 0;
        for (int t = 0; t < T; t++) if (surg_ot[u][d][t] > 0) cnt++;
        if (cnt > 1) trans_unw += (cnt - 1);
      }
    }

    int base_cost = age_unw * w_age + open_ot_unw * w_ot + trans_unw * w_trans + delay_unw * w_delay + unsched_unw * w_unsched;
    return {viol, base_cost};
  }

  void RebuildAll() {
    auto [viol, bcost] = EvaluatePatientLayer();
    cur_base_cost = bcost;

    room_day_occ_count.assign(R, vector<int>(D, 0));
    room_day_people.assign(R, vector<vector<int>>(D));
    rs_load.assign(R, vector<int>(S, 0));
    rs_skill_pen.assign(R, vector<vector<int>>(S, vector<int>(N, 0)));
    q_room.assign(Q, -1);
    q_start_day.assign(Q, -1);
    q_end_day.assign(Q, -1);

    for (int o = 0; o < O; o++) {
      int q = P + o;
      int r = in.OccupantRoom(o);
      int los = in.OccupantLengthOfStay(o);
      q_room[q] = r;
      q_start_day[q] = 0;
      q_end_day[q] = min(D, los);
      for (int d = 0; d < min(D, los); d++) {
        room_day_occ_count[r][d]++;
        room_day_people[r][d].push_back(q);
        for (int sn = 0; sn < SPD; sn++) {
          int s = d * SPD + sn;
          int wl = in.OccupantWorkloadProduced(o, s);
          int sk = in.OccupantSkillLevelRequired(o, s);
          rs_load[r][s] += wl;
          for (int n : in.AvailableNursesVec(s)) {
            if (sk > in.NurseSkillLevel(n))
              rs_skill_pen[r][s][n] += (sk - in.NurseSkillLevel(n));
          }
        }
      }
    }

    for (int p = 0; p < P; p++) {
      int ad = admission_day[p];
      if (ad == -1) continue;
      int r = room[p];
      int los = in.PatientLengthOfStay(p);
      q_room[p] = r;
      q_start_day[p] = ad;
      q_end_day[p] = min(D, ad + los);
      for (int d = ad; d < min(D, ad + los); d++) {
        room_day_occ_count[r][d]++;
        room_day_people[r][d].push_back(p);
        for (int sn = 0; sn < SPD; sn++) {
          int s = d * SPD + sn;
          int s1 = s - ad * SPD;
          int wl = in.PatientWorkloadProduced(p, s1);
          int sk = in.PatientSkillLevelRequired(p, s1);
          rs_load[r][s] += wl;
          for (int n : in.AvailableNursesVec(s)) {
            if (sk > in.NurseSkillLevel(n))
              rs_skill_pen[r][s][n] += (sk - in.NurseSkillLevel(n));
          }
        }
      }
    }

    for (int r = 0; r < R; r++) {
      for (int s = 0; s < S; s++) {
        int n = rs_nurse[r][s];
        if (n < 0 || n >= N || !in.IsNurseWorkingInShift(n, s)) {
          rs_nurse[r][s] = in.AvailableNurse(s, 0);
        }
      }
    }

    ns_load.assign(N, vector<int>(S, 0));
    q_nurse_cnt.assign(Q, vector<int>(N, 0));
    q_distinct_nurses.assign(Q, 0);
    cur_skill_unw = 0;
    cur_work_unw = 0;
    cur_coc_unw = 0;

    for (int r = 0; r < R; r++) {
      for (int s = 0; s < S; s++) {
        int d = s / SPD;
        if (room_day_occ_count[r][d] == 0) continue;
        int n = rs_nurse[r][s];
        cur_skill_unw += rs_skill_pen[r][s][n];
        ns_load[n][s] += rs_load[r][s];
        for (int q : room_day_people[r][d]) {
          if (q_nurse_cnt[q][n] == 0) {
            q_distinct_nurses[q]++;
            cur_coc_unw++;
          }
          q_nurse_cnt[q][n]++;
        }
      }
    }

    for (int n = 0; n < N; n++) {
      for (int ws_i = 0; ws_i < in.NurseWorkingShifts(n); ws_i++) {
        int s = in.NurseWorkingShift(n, ws_i);
        int max_l = in.NurseMaxLoad(n, s);
        if (ns_load[n][s] > max_l) {
          cur_work_unw += (ns_load[n][s] - max_l);
        }
      }
    }
  }

  inline int TotalNRACost() const {
    return cur_skill_unw * w_skill + cur_coc_unw * w_coc + cur_work_unw * w_work;
  }

  inline int TotalCost() const {
    return cur_base_cost + TotalNRACost();
  }

  inline int DeltaSetNurse(int r, int s, int n_new) const {
    int d = s / SPD;
    if (room_day_occ_count[r][d] == 0) return 0;
    int n_old = rs_nurse[r][s];
    if (n_old == n_new) return 0;

    int d_skill = rs_skill_pen[r][s][n_new] - rs_skill_pen[r][s][n_old];

    int wl = rs_load[r][s];
    int old_e1 = max(0, ns_load[n_old][s] - in.NurseMaxLoad(n_old, s));
    int new_e1 = max(0, ns_load[n_old][s] - wl - in.NurseMaxLoad(n_old, s));
    int old_e2 = max(0, ns_load[n_new][s] - in.NurseMaxLoad(n_new, s));
    int new_e2 = max(0, ns_load[n_new][s] + wl - in.NurseMaxLoad(n_new, s));
    int d_work = (new_e1 - old_e1) + (new_e2 - old_e2);

    int d_coc = 0;
    for (int q : room_day_people[r][d]) {
      if (q_nurse_cnt[q][n_old] == 1) d_coc--;
      if (q_nurse_cnt[q][n_new] == 0) d_coc++;
    }

    return d_skill * w_skill + d_work * w_work + d_coc * w_coc;
  }

  inline void ApplySetNurse(int r, int s, int n_new) {
    int d = s / SPD;
    int n_old = rs_nurse[r][s];
    if (n_old == n_new) return;
    if (room_day_occ_count[r][d] == 0) {
      rs_nurse[r][s] = n_new;
      return;
    }

    cur_skill_unw += (rs_skill_pen[r][s][n_new] - rs_skill_pen[r][s][n_old]);

    int wl = rs_load[r][s];
    int old_e1 = max(0, ns_load[n_old][s] - in.NurseMaxLoad(n_old, s));
    int new_e1 = max(0, ns_load[n_old][s] - wl - in.NurseMaxLoad(n_old, s));
    int old_e2 = max(0, ns_load[n_new][s] - in.NurseMaxLoad(n_new, s));
    int new_e2 = max(0, ns_load[n_new][s] + wl - in.NurseMaxLoad(n_new, s));
    cur_work_unw += (new_e1 - old_e1) + (new_e2 - old_e2);
    ns_load[n_old][s] -= wl;
    ns_load[n_new][s] += wl;

    for (int q : room_day_people[r][d]) {
      q_nurse_cnt[q][n_old]--;
      if (q_nurse_cnt[q][n_old] == 0) {
        q_distinct_nurses[q]--;
        cur_coc_unw--;
      }
      if (q_nurse_cnt[q][n_new] == 0) {
        q_distinct_nurses[q]++;
        cur_coc_unw++;
      }
      q_nurse_cnt[q][n_new]++;
    }
    rs_nurse[r][s] = n_new;
  }

  // Exact greedy zero-temperature polish over single moves, swaps, and patient-stay nurse consolidations
  void GreedyPolishNRA() {
    bool improved = true;
    while (improved) {
      improved = false;
      // 1. Single (r, s) best nurse
      for (int r = 0; r < R; r++) {
        for (int s = 0; s < S; s++) {
          if (room_day_occ_count[r][s / SPD] == 0) continue;
          int best_d = 0, best_n = -1;
          for (int n : in.AvailableNursesVec(s)) {
            int d = DeltaSetNurse(r, s, n);
            if (d < best_d) { best_d = d; best_n = n; }
          }
          if (best_n != -1) {
            ApplySetNurse(r, s, best_n);
            improved = true;
          }
        }
      }
      // 2. Two-room swap in same shift s
      for (int s = 0; s < S; s++) {
        int d = s / SPD;
        for (int r1 = 0; r1 < R; r1++) {
          if (room_day_occ_count[r1][d] == 0) continue;
          for (int r2 = r1 + 1; r2 < R; r2++) {
            if (room_day_occ_count[r2][d] == 0) continue;
            int n1 = rs_nurse[r1][s], n2 = rs_nurse[r2][s];
            if (n1 == n2) continue;
            int c0 = TotalNRACost();
            ApplySetNurse(r1, s, n2);
            ApplySetNurse(r2, s, n1);
            if (TotalNRACost() < c0) {
              improved = true;
            } else {
              ApplySetNurse(r1, s, n1);
              ApplySetNurse(r2, s, n2);
            }
          }
        }
      }
      // 3. Patient-stay nurse consolidation (eliminate a nurse n_drop from person q by replacing/swapping with n_keep)
      for (int q = 0; q < Q; q++) {
        int r = q_room[q];
        if (r == -1) continue;
        int d_start = q_start_day[q], d_end = q_end_day[q];
        for (int n_drop = 0; n_drop < N; n_drop++) {
          if (q_nurse_cnt[q][n_drop] == 0 || q_nurse_cnt[q][n_drop] > 6) continue;
          for (int n_keep = 0; n_keep < N; n_keep++) {
            if (n_keep == n_drop || q_nurse_cnt[q][n_keep] == 0) continue;
            int c0 = TotalNRACost();
            vector<tuple<int, int, int>> undo;
            bool possible = true;
            for (int d = d_start; d < d_end; d++) {
              for (int sn = 0; sn < SPD; sn++) {
                int s = d * SPD + sn;
                if (rs_nurse[r][s] == n_drop) {
                  if (!in.IsNurseWorkingInShift(n_keep, s)) { possible = false; break; }
                  // Try direct assignment vs swapping with a room r2 of n_keep
                  int best_r2 = -1;
                  int d_direct = DeltaSetNurse(r, s, n_keep);
                  int best_step = d_direct;
                  for (int r2 = 0; r2 < R; r2++) {
                    if (r2 != r && room_day_occ_count[r2][d] > 0 && rs_nurse[r2][s] == n_keep) {
                      int c_pre = TotalNRACost();
                      ApplySetNurse(r, s, n_keep);
                      ApplySetNurse(r2, s, n_drop);
                      int d_sw = TotalNRACost() - c_pre;
                      ApplySetNurse(r, s, n_drop);
                      ApplySetNurse(r2, s, n_keep);
                      if (d_sw < best_step) { best_step = d_sw; best_r2 = r2; }
                    }
                  }
                  undo.push_back({r, s, n_drop});
                  ApplySetNurse(r, s, n_keep);
                  if (best_r2 != -1) {
                    undo.push_back({best_r2, s, n_keep});
                    ApplySetNurse(best_r2, s, n_drop);
                  }
                }
              }
              if (!possible) break;
            }
            if (possible && TotalNRACost() < c0) {
              improved = true;
              break;
            } else {
              for (int i = (int)undo.size() - 1; i >= 0; i--) {
                auto [ur, us, un] = undo[i];
                ApplySetNurse(ur, us, un);
              }
            }
          }
        }
      }
    }
  }
};

void OptimizeNRA(FastSchedule& sched, double seconds, uint64_t seed) {
  mt19937_64 rng(seed);
  sched.GreedyPolishNRA();
  int best_nra = sched.TotalNRACost();
  auto best_rs = sched.rs_nurse;

  vector<pair<int, int>> occ_rs;
  for (int r = 0; r < sched.R; r++) {
    for (int s = 0; s < sched.S; s++) {
      if (sched.room_day_occ_count[r][s / sched.SPD] > 0 && sched.in.AvailableNurses(s) > 1) {
        occ_rs.push_back({r, s});
      }
    }
  }
  if (occ_rs.empty() || seconds <= 0.0) return;

  auto t_start = chrono::steady_clock::now();
  double t_el = 0.0;
  long long iters = 0;
  int num_cycles = 3;
  double T_start = 6.0, T_end = 0.04;
  double temp = T_start;
  int last_cycle = 0;

  while (true) {
    if ((iters & 16383) == 0) {
      t_el = chrono::duration<double>(chrono::steady_clock::now() - t_start).count();
      if (t_el >= seconds) break;
      double total_frac = t_el / seconds;
      int cyc = min(num_cycles - 1, (int)(total_frac * num_cycles));
      if (cyc != last_cycle) {
        last_cycle = cyc;
        sched.rs_nurse = best_rs;
        sched.RebuildAll();
        sched.GreedyPolishNRA();
        if (sched.TotalNRACost() < best_nra) {
          best_nra = sched.TotalNRACost();
          best_rs = sched.rs_nurse;
        }
      }
      double cyc_frac = (total_frac * num_cycles) - cyc;
      temp = T_start * pow(T_end / T_start, cyc_frac);
    }
    iters++;

    int move_type = rng() % 100;
    if (move_type < 42) {
      auto [r, s] = occ_rs[rng() % occ_rs.size()];
      const auto& av = sched.in.AvailableNursesVec(s);
      int n_new = av[rng() % av.size()];
      if (n_new == sched.rs_nurse[r][s]) continue;
      int delta = sched.DeltaSetNurse(r, s, n_new);
      if (delta <= 0 || exp(-delta / temp) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
        sched.ApplySetNurse(r, s, n_new);
        if (sched.TotalNRACost() < best_nra) {
          best_nra = sched.TotalNRACost();
          best_rs = sched.rs_nurse;
        }
      }
    } else if (move_type < 72) {
      int s = rng() % sched.S;
      if (sched.R < 2) continue;
      int r1 = rng() % sched.R;
      int r2 = rng() % (sched.R - 1);
      if (r2 >= r1) r2++;
      int d = s / sched.SPD;
      if (sched.room_day_occ_count[r1][d] == 0 && sched.room_day_occ_count[r2][d] == 0) continue;
      int n1 = sched.rs_nurse[r1][s];
      int n2 = sched.rs_nurse[r2][s];
      if (n1 == n2) continue;
      int cur = sched.TotalNRACost();
      sched.ApplySetNurse(r1, s, n2);
      sched.ApplySetNurse(r2, s, n1);
      int delta = sched.TotalNRACost() - cur;
      if (delta <= 0 || exp(-delta / temp) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
        if (sched.TotalNRACost() < best_nra) {
          best_nra = sched.TotalNRACost();
          best_rs = sched.rs_nurse;
        }
      } else {
        sched.ApplySetNurse(r1, s, n1);
        sched.ApplySetNurse(r2, s, n2);
      }
    } else if (move_type < 90) {
      int r = rng() % sched.R;
      int d1 = rng() % sched.D;
      int len = 1 + (rng() % min(7, sched.D - d1));
      int n_target = rng() % sched.N;
      int cur = sched.TotalNRACost();
      vector<tuple<int, int, int>> undo;
      for (int d = d1; d < d1 + len; d++) {
        if (sched.room_day_occ_count[r][d] == 0) continue;
        for (int sn = 0; sn < sched.SPD; sn++) {
          int s = d * sched.SPD + sn;
          if (sched.in.IsNurseWorkingInShift(n_target, s) && sched.rs_nurse[r][s] != n_target) {
            int n_old = sched.rs_nurse[r][s];
            int r_swap = -1;
            if ((rng() & 1) == 0) {
              for (int r2 = 0; r2 < sched.R; r2++) {
                if (r2 != r && sched.room_day_occ_count[r2][d] > 0 && sched.rs_nurse[r2][s] == n_target) {
                  r_swap = r2;
                  break;
                }
              }
            }
            undo.push_back({r, s, n_old});
            sched.ApplySetNurse(r, s, n_target);
            if (r_swap != -1) {
              undo.push_back({r_swap, s, n_target});
              sched.ApplySetNurse(r_swap, s, n_old);
            }
          }
        }
      }
      if (undo.empty()) continue;
      int delta = sched.TotalNRACost() - cur;
      if (delta <= 0 || exp(-delta / temp) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
        if (sched.TotalNRACost() < best_nra) {
          best_nra = sched.TotalNRACost();
          best_rs = sched.rs_nurse;
        }
      } else {
        for (int i = (int)undo.size() - 1; i >= 0; i--) {
          auto [ur, us, un] = undo[i];
          sched.ApplySetNurse(ur, us, un);
        }
      }
    } else {
      int n1 = rng() % sched.N;
      int n2 = rng() % (sched.N - 1);
      if (n2 >= n1) n2++;
      int d1 = rng() % sched.D;
      int len = 1 + (rng() % min(6, sched.D - d1));
      int cur = sched.TotalNRACost();
      vector<tuple<int, int, int>> undo;
      for (int s = d1 * sched.SPD; s < (d1 + len) * sched.SPD; s++) {
        if (sched.in.IsNurseWorkingInShift(n1, s) && sched.in.IsNurseWorkingInShift(n2, s)) {
          int d = s / sched.SPD;
          for (int r = 0; r < sched.R; r++) {
            if (sched.room_day_occ_count[r][d] == 0) continue;
            if (sched.rs_nurse[r][s] == n1) {
              undo.push_back({r, s, n1});
              sched.ApplySetNurse(r, s, n2);
            } else if (sched.rs_nurse[r][s] == n2) {
              undo.push_back({r, s, n2});
              sched.ApplySetNurse(r, s, n1);
            }
          }
        }
      }
      if (undo.empty()) continue;
      int delta = sched.TotalNRACost() - cur;
      if (delta <= 0 || exp(-delta / temp) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
        if (sched.TotalNRACost() < best_nra) {
          best_nra = sched.TotalNRACost();
          best_rs = sched.rs_nurse;
        }
      } else {
        for (int i = (int)undo.size() - 1; i >= 0; i--) {
          auto [ur, us, un] = undo[i];
          sched.ApplySetNurse(ur, us, un);
        }
      }
    }
  }

  sched.rs_nurse = best_rs;
  sched.RebuildAll();
  sched.GreedyPolishNRA();
}

// Fast Smart-Feasible Coupled Patient + Nurse Search
void OptimizeCoupled(FastSchedule& sched, double seconds, uint64_t seed) {
  if (seconds <= 0.0) return;
  mt19937_64 rng(seed);
  int best_total = sched.TotalCost();
  auto best_ad = sched.admission_day;
  auto best_rm = sched.room;
  auto best_ot = sched.operating_room;
  auto best_rs = sched.rs_nurse;

  auto t_start = chrono::steady_clock::now();
  double t_el = 0.0;
  long long iters = 0;
  double T_start = 10.0, T_end = 0.1;
  double temp = T_start;

  while (true) {
    if ((iters & 511) == 0) {
      t_el = chrono::duration<double>(chrono::steady_clock::now() - t_start).count();
      if (t_el >= seconds) break;
      double frac = t_el / seconds;
      temp = T_start * pow(T_end / T_start, frac);
    }
    iters++;

    int prev_cost = sched.TotalCost();
    int mtype = rng() % 100;
    vector<pair<int, tuple<int, int, int>>> pat_undo;

    if (mtype < 35) {
      // Move P1: Move a scheduled patient p to another compatible room r_new (checking capacity & gender in O(los))
      int p = rng() % sched.P;
      int ad = sched.admission_day[p];
      if (ad == -1) continue;
      int r_old = sched.room[p];
      int r_new = rng() % sched.R;
      if (r_new == r_old || sched.in.IncompatibleRoom(p, r_new)) continue;
      int los = sched.in.PatientLengthOfStay(p);
      Gender g = sched.in.PatientGender(p);
      bool ok = true;
      for (int d = ad; d < min(sched.D, ad + los); d++) {
        if (sched.room_day_occ_count[r_new][d] + 1 > sched.in.RoomCapacity(r_new)) { ok = false; break; }
        if (g == Gender::A && sched.rd_b[r_new][d] > 0) { ok = false; break; }
        if (g == Gender::B && sched.rd_a[r_new][d] > 0) { ok = false; break; }
      }
      if (!ok) continue;
      pat_undo.push_back({p, {ad, r_old, sched.operating_room[p]}});
      sched.room[p] = r_new;
    } else if (mtype < 70) {
      // Move P2: Same-gender two-patient room swap
      int p1 = rng() % sched.P;
      int p2 = rng() % sched.P;
      if (p1 == p2 || sched.admission_day[p1] == -1 || sched.admission_day[p2] == -1) continue;
      if (sched.in.PatientGender(p1) != sched.in.PatientGender(p2)) continue;
      int r1 = sched.room[p1], r2 = sched.room[p2];
      if (r1 == r2 || sched.in.IncompatibleRoom(p1, r2) || sched.in.IncompatibleRoom(p2, r1)) continue;
      pat_undo.push_back({p1, {sched.admission_day[p1], r1, sched.operating_room[p1]}});
      pat_undo.push_back({p2, {sched.admission_day[p2], r2, sched.operating_room[p2]}});
      sched.room[p1] = r2;
      sched.room[p2] = r1;
    } else if (mtype < 88) {
      // Move P3: Operating theater change or swap on same day
      int p1 = rng() % sched.P;
      if (sched.admission_day[p1] == -1) continue;
      int t_old = sched.operating_room[p1];
      int t_new = rng() % sched.T;
      if (t_new == t_old) continue;
      int ad = sched.admission_day[p1];
      int dur = sched.in.PatientSurgeryDuration(p1);
      if (sched.ot_load[t_new][ad] + dur <= sched.in.OperatingTheaterAvailability(t_new, ad)) {
        pat_undo.push_back({p1, {ad, sched.room[p1], t_old}});
        sched.operating_room[p1] = t_new;
      }
    } else {
      // Move P4: Admission day shift for patient p
      int p = rng() % sched.P;
      if (sched.admission_day[p] == -1) continue;
      int rel = sched.in.PatientSurgeryReleaseDay(p);
      int last = sched.in.PatientLastPossibleDay(p);
      if (rel >= last) continue;
      int ad_old = sched.admission_day[p];
      int ad_new = rel + (rng() % (last - rel + 1));
      if (ad_new == ad_old) continue;
      int r_new = (rng() & 1) ? sched.room[p] : (int)(rng() % sched.R);
      int t_new = (rng() & 1) ? sched.operating_room[p] : (int)(rng() % sched.T);
      if (sched.in.IncompatibleRoom(p, r_new)) continue;
      pat_undo.push_back({p, {ad_old, sched.room[p], sched.operating_room[p]}});
      sched.admission_day[p] = ad_new;
      sched.room[p] = r_new;
      sched.operating_room[p] = t_new;
    }

    if (pat_undo.empty()) continue;

    auto [viol, bcost] = sched.EvaluatePatientLayer();
    if (viol > 0) {
      for (auto& [up, tup] : pat_undo) {
        sched.admission_day[up] = get<0>(tup);
        sched.room[up] = get<1>(tup);
        sched.operating_room[up] = get<2>(tup);
      }
      sched.EvaluatePatientLayer();
      continue;
    }

    auto sav_rs = sched.rs_nurse;
    sched.RebuildAll();
    int new_cost = sched.TotalCost();
    if (new_cost - prev_cost <= 35) {
      sched.GreedyPolishNRA();
      new_cost = sched.TotalCost();
    }
    int delta = new_cost - prev_cost;

    if (delta <= 0 || exp(-delta / temp) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
      if (new_cost < best_total) {
        best_total = new_cost;
        best_ad = sched.admission_day;
        best_rm = sched.room;
        best_ot = sched.operating_room;
        best_rs = sched.rs_nurse;
      }
    } else {
      for (auto& [up, tup] : pat_undo) {
        sched.admission_day[up] = get<0>(tup);
        sched.room[up] = get<1>(tup);
        sched.operating_room[up] = get<2>(tup);
      }
      sched.rs_nurse = sav_rs;
      sched.RebuildAll();
    }
  }

  sched.admission_day = best_ad;
  sched.room = best_rm;
  sched.operating_room = best_ot;
  sched.rs_nurse = best_rs;
  sched.RebuildAll();
}

int main(int argc, char** argv) {
  if (argc < 5) {
    cerr << "Usage: " << argv[0] << " <instance.json> <in_sol.json> <out_sol.json> <nra_sec> [coupled_sec] [seed]" << endl;
    return 1;
  }
  string inst_file = argv[1];
  string sol_file = argv[2];
  string out_file = argv[3];
  double nra_sec = stod(argv[4]);
  double coupled_sec = (argc >= 6) ? stod(argv[5]) : 0.0;
  uint64_t seed = (argc >= 7) ? stoull(argv[6]) : 42ULL;

  IHTP_Input in(inst_file);
  FastSchedule sched(in);
  sched.LoadJSON(sol_file);

  auto [v0, b0] = sched.EvaluatePatientLayer();
  int orig_cost = sched.TotalCost();
  int orig_nra = sched.TotalNRACost();

  if (nra_sec > 0) {
    OptimizeNRA(sched, nra_sec, seed);
  }
  int after_nra_cost = sched.TotalCost();

  if (coupled_sec > 0) {
    OptimizeCoupled(sched, coupled_sec, seed + 1000);
    OptimizeNRA(sched, max(0.5, nra_sec * 0.5), seed + 2000);
  }

  auto [vf, bf] = sched.EvaluatePatientLayer();
  int final_cost = sched.TotalCost();

  if (vf == 0 && final_cost < orig_cost) {
    sched.SaveJSON(out_file);
  }
  cout << "RESULT orig=" << orig_cost << " (nra=" << orig_nra << ") after_nra=" << after_nra_cost
       << " final=" << final_cost << " (nra=" << sched.TotalNRACost() << ") viol=" << vf
       << " gain=" << (orig_cost - final_cost) << endl;
  return 0;
}
