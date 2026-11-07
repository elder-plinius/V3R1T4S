#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <random>
#include <chrono>
#include <cmath>
#include <cstdlib>
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
  int days, shifts_per_day, shifts, patients, occupants, skill_levels, age_groups, surgeons, operating_theaters, rooms, nurses;
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

  IHTP_Input(string file_name) : weights(8) {
    nlohmann::json j_in;
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

    for (int sn = 0; sn < shifts_per_day; sn++) shift_names[sn] = j_in["shift_types"][sn];
    for (int ag = 0; ag < age_groups; ag++) age_group_names[ag] = j_in["age_groups"][ag];

    for (int s = 0; s < surgeons; s++) {
      auto& j_s = j_in["surgeons"][s];
      surgeons_vect[s].id = j_s["id"];
      for (int d = 0; d < days; d++) surgeons_vect[s].max_surgery_time[d] = j_s["max_surgery_time"][d];
    }
    for (int ot = 0; ot < operating_theaters; ot++) {
      auto& j_ot = j_in["operating_theaters"][ot];
      operating_theaters_vect[ot].id = j_ot["id"];
      for (int d = 0; d < days; d++) operating_theaters_vect[ot].availability[d] = j_ot["availability"][d];
    }
    for (int r = 0; r < rooms; r++) {
      auto& j_r = j_in["rooms"][r];
      rooms_vect[r].id = j_r["id"];
      rooms_vect[r].capacity = j_r["capacity"];
    }
    room_day_fixed_list.resize(rooms, vector<vector<int>>(days));
    for (int f = 0; f < occupants; f++) {
      auto& j_f = j_in["occupants"][f];
      occupants_vect[f].id = j_f["id"];
      occupants_vect[f].gender = (j_f["gender"] == "A") ? Gender::A : Gender::B;
      occupants_vect[f].age_group = FindAgeGroup(j_f["age_group"]);
      occupants_vect[f].length_of_stay = j_f["length_of_stay"];
      int tot_s = occupants_vect[f].length_of_stay * shifts_per_day;
      occupants_vect[f].workload_produced.resize(tot_s);
      occupants_vect[f].skill_level_required.resize(tot_s);
      for (int s = 0; s < tot_s; s++) {
        occupants_vect[f].workload_produced[s] = j_f["workload_produced"][s];
        occupants_vect[f].skill_level_required[s] = j_f["skill_level_required"][s];
      }
      int r = FindRoom(j_f["room_id"]);
      occupants_vect[f].assigned_room = r;
      for (int d = 0; d < occupants_vect[f].length_of_stay; d++)
        room_day_fixed_list[r][d].push_back(f);
    }
    for (int p = 0; p < patients; p++) {
      auto& j_p = j_in["patients"][p];
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
        for (size_t i = 0; i < j_p["incompatible_room_ids"].size(); i++) {
          int r = FindRoom(j_p["incompatible_room_ids"][i]);
          patients_vect[p].incompatible_rooms[r] = true;
        }
      }
      int tot_s = patients_vect[p].length_of_stay * shifts_per_day;
      patients_vect[p].workload_produced.resize(tot_s);
      patients_vect[p].skill_level_required.resize(tot_s);
      for (int s = 0; s < tot_s; s++) {
        patients_vect[p].workload_produced[s] = j_p["workload_produced"][s];
        patients_vect[p].skill_level_required[s] = j_p["skill_level_required"][s];
      }
    }
    for (int n = 0; n < nurses; n++) {
      auto& j_n = j_in["nurses"][n];
      nurses_vect[n].id = j_n["id"];
      nurses_vect[n].skill_level = j_n["skill_level"];
      for (size_t i = 0; i < j_n["working_shifts"].size(); i++) {
        int s = static_cast<int>(j_n["working_shifts"][i]["day"]) * shifts_per_day + FindShift(j_n["working_shifts"][i]["shift"]);
        nurses_vect[n].working_shifts.push_back(s);
        nurses_vect[n].is_working_in_shift[s] = true;
        nurses_vect[n].max_loads[s] = j_n["working_shifts"][i]["max_load"];
        available_nurses[s].push_back(n);
      }
    }
  }

  int PatientLastPossibleDay(int p) const { return patients_vect[p].mandatory ? patients_vect[p].surgery_due_day : days - 1; }

  int FindAgeGroup(const string& name) const {
    for (int i = 0; i < age_groups; i++) if (name == age_group_names[i]) return i;
    throw invalid_argument("Unknown age group");
  }
  int FindSurgeon(const string& id) const {
    for (int i = 0; i < surgeons; i++) if (id == surgeons_vect[i].id) return i;
    throw invalid_argument("Unknown surgeon");
  }
  int FindShift(const string& name) const {
    for (int i = 0; i < shifts_per_day; i++) if (name == shift_names[i]) return i;
    throw invalid_argument("Unknown shift");
  }
  int FindRoom(const string& id) const {
    for (int i = 0; i < rooms; i++) if (id == rooms_vect[i].id) return i;
    throw invalid_argument("Unknown room");
  }
  int FindOperatingTheater(const string& id) const {
    for (int i = 0; i < operating_theaters; i++) if (id == operating_theaters_vect[i].id) return i;
    throw invalid_argument("Unknown theater");
  }
  int FindPatient(const string& id) const {
    for (int i = 0; i < patients; i++) if (id == patients_vect[i].id) return i;
    throw invalid_argument("Unknown patient");
  }
  int FindNurse(const string& id) const {
    for (int i = 0; i < nurses; i++) if (id == nurses_vect[i].id) return i;
    throw invalid_argument("Unknown nurse");
  }
};

struct SolutionState {
  vector<int> admission_day;
  vector<int> room;
  vector<int> operating_room;
  vector<vector<int>> room_shift_nurse;
};

class FastEval {
public:
  const IHTP_Input& in;
  SolutionState cur;

  vector<vector<vector<int>>> room_day_patients;
  vector<vector<int>> room_day_a, room_day_b;
  vector<vector<int>> ot_day_load;
  vector<vector<int>> ot_day_count;
  vector<vector<int>> surgeon_day_load;
  vector<vector<vector<int>>> surgeon_day_ot_count;

  vector<vector<int>> room_shift_load;
  vector<vector<vector<int>>> room_shift_skill_pen;
  vector<vector<int>> nurse_shift_load;
  vector<vector<int>> entity_nurse_count;
  vector<int> entity_distinct_nurses;

  long long cost_age_mix = 0;
  long long cost_skill = 0;
  long long cost_continuity = 0;
  long long cost_workload = 0;
  long long cost_open_ot = 0;
  long long cost_surgeon_transfer = 0;
  long long cost_delay = 0;
  long long cost_unscheduled = 0;

  FastEval(const IHTP_Input& input) : in(input) {
    cur.admission_day.assign(in.patients, -1);
    cur.room.assign(in.patients, -1);
    cur.operating_room.assign(in.patients, -1);
    cur.room_shift_nurse.assign(in.rooms, vector<int>(in.shifts, -1));
  }

  void LoadJSON(const string& file_name) {
    nlohmann::json j_sol;
    ifstream is(file_name);
    if (!is) throw invalid_argument("Cannot open solution file " + file_name);
    is >> j_sol;

    fill(cur.admission_day.begin(), cur.admission_day.end(), -1);
    fill(cur.room.begin(), cur.room.end(), -1);
    fill(cur.operating_room.begin(), cur.operating_room.end(), -1);
    for (int r = 0; r < in.rooms; r++) fill(cur.room_shift_nurse[r].begin(), cur.room_shift_nurse[r].end(), -1);

    for (size_t i = 0; i < j_sol["patients"].size(); i++) {
      auto& j_p = j_sol["patients"][i];
      if (j_p["admission_day"] != "none") {
        int p = in.FindPatient(j_p["id"]);
        cur.admission_day[p] = j_p["admission_day"];
        cur.room[p] = in.FindRoom(j_p["room"]);
        cur.operating_room[p] = in.FindOperatingTheater(j_p["operating_theater"]);
      }
    }
    for (size_t n = 0; n < j_sol["nurses"].size(); n++) {
      auto& j_n = j_sol["nurses"][n];
      int cn = in.FindNurse(j_n["id"]);
      for (size_t i = 0; i < j_n["assignments"].size(); i++) {
        int d = j_n["assignments"][i]["day"];
        int s = d * in.shifts_per_day + in.FindShift(j_n["assignments"][i]["shift"]);
        for (size_t j = 0; j < j_n["assignments"][i]["rooms"].size(); j++) {
          int r = in.FindRoom(j_n["assignments"][i]["rooms"][j]);
          cur.room_shift_nurse[r][s] = cn;
        }
      }
    }
    RebuildAll();
  }

  void SaveJSON(const string& file_name) const {
    nlohmann::json j_sol;
    j_sol["patients"] = nlohmann::json::array();
    for (int p = 0; p < in.patients; p++) {
      nlohmann::json jp;
      jp["id"] = in.patients_vect[p].id;
      if (cur.admission_day[p] == -1) {
        jp["admission_day"] = "none";
      } else {
        jp["admission_day"] = cur.admission_day[p];
        jp["room"] = in.rooms_vect[cur.room[p]].id;
        jp["operating_theater"] = in.operating_theaters_vect[cur.operating_room[p]].id;
      }
      j_sol["patients"].push_back(jp);
    }
    j_sol["nurses"] = nlohmann::json::array();
    for (int n = 0; n < in.nurses; n++) {
      nlohmann::json jn;
      jn["id"] = in.nurses_vect[n].id;
      jn["assignments"] = nlohmann::json::array();
      for (int s : in.nurses_vect[n].working_shifts) {
        nlohmann::json ja;
        ja["day"] = s / in.shifts_per_day;
        ja["shift"] = in.shift_names[s % in.shifts_per_day];
        ja["rooms"] = nlohmann::json::array();
        for (int r = 0; r < in.rooms; r++) {
          if (cur.room_shift_nurse[r][s] == n) {
            ja["rooms"].push_back(in.rooms_vect[r].id);
          }
        }
        jn["assignments"].push_back(ja);
      }
      j_sol["nurses"].push_back(jn);
    }
    ofstream os(file_name);
    os << j_sol.dump(2) << endl;
  }

  int EntityAgeGroup(int e) const {
    return (e < in.patients) ? in.patients_vect[e].age_group : in.occupants_vect[e - in.patients].age_group;
  }

  int ComputeRoomDayAgeDiff(int r, int d) const {
    const auto& vec = room_day_patients[r][d];
    if (vec.size() <= 1) return 0;
    int mn = EntityAgeGroup(vec[0]);
    int mx = mn;
    for (size_t i = 1; i < vec.size(); i++) {
      int g = EntityAgeGroup(vec[i]);
      if (g < mn) mn = g;
      else if (g > mx) mx = g;
    }
    return mx - mn;
  }

  void RebuildAll() {
    room_day_patients.assign(in.rooms, vector<vector<int>>(in.days));
    room_day_a.assign(in.rooms, vector<int>(in.days, 0));
    room_day_b.assign(in.rooms, vector<int>(in.days, 0));
    ot_day_load.assign(in.operating_theaters, vector<int>(in.days, 0));
    ot_day_count.assign(in.operating_theaters, vector<int>(in.days, 0));
    surgeon_day_load.assign(in.surgeons, vector<int>(in.days, 0));
    surgeon_day_ot_count.assign(in.surgeons, vector<vector<int>>(in.days, vector<int>(in.operating_theaters, 0)));

    for (int f = 0; f < in.occupants; f++) {
      int e = in.patients + f;
      int r = in.occupants_vect[f].assigned_room;
      for (int d = 0; d < in.occupants_vect[f].length_of_stay; d++) {
        room_day_patients[r][d].push_back(e);
        if (in.occupants_vect[f].gender == Gender::A) room_day_a[r][d]++;
        else room_day_b[r][d]++;
      }
    }

    cost_delay = 0;
    cost_unscheduled = 0;
    for (int p = 0; p < in.patients; p++) {
      int ad = cur.admission_day[p];
      if (ad == -1) {
        if (!in.patients_vect[p].mandatory) cost_unscheduled += in.weights[7];
      } else {
        int r = cur.room[p];
        int t = cur.operating_room[p];
        cost_delay += (long long)(ad - in.patients_vect[p].surgery_release_day) * in.weights[6];
        int end_d = min(in.days, ad + in.patients_vect[p].length_of_stay);
        for (int d = ad; d < end_d; d++) {
          room_day_patients[r][d].push_back(p);
          if (in.patients_vect[p].gender == Gender::A) room_day_a[r][d]++;
          else room_day_b[r][d]++;
        }
        ot_day_load[t][ad] += in.patients_vect[p].surgery_duration;
        ot_day_count[t][ad]++;
        int u = in.patients_vect[p].surgeon;
        surgeon_day_load[u][ad] += in.patients_vect[p].surgery_duration;
        surgeon_day_ot_count[u][ad][t]++;
      }
    }

    cost_age_mix = 0;
    for (int r = 0; r < in.rooms; r++) {
      for (int d = 0; d < in.days; d++) {
        cost_age_mix += (long long)ComputeRoomDayAgeDiff(r, d) * in.weights[0];
      }
    }

    cost_open_ot = 0;
    for (int t = 0; t < in.operating_theaters; t++) {
      for (int d = 0; d < in.days; d++) {
        if (ot_day_count[t][d] > 0) cost_open_ot += in.weights[4];
      }
    }

    cost_surgeon_transfer = 0;
    for (int u = 0; u < in.surgeons; u++) {
      for (int d = 0; d < in.days; d++) {
        int cnt = 0;
        for (int t = 0; t < in.operating_theaters; t++) if (surgeon_day_ot_count[u][d][t] > 0) cnt++;
        if (cnt > 1) cost_surgeon_transfer += (long long)(cnt - 1) * in.weights[5];
      }
    }

    RebuildNurseStructures();
  }

  void RebuildNurseStructures() {
    room_shift_load.assign(in.rooms, vector<int>(in.shifts, 0));
    room_shift_skill_pen.assign(in.rooms, vector<vector<int>>(in.shifts, vector<int>(in.skill_levels + 1, 0)));
    nurse_shift_load.assign(in.nurses, vector<int>(in.shifts, 0));
    int tot_e = in.patients + in.occupants;
    entity_nurse_count.assign(tot_e, vector<int>(in.nurses, 0));
    entity_distinct_nurses.assign(tot_e, 0);

    cost_skill = 0;
    cost_continuity = 0;
    cost_workload = 0;

    for (int r = 0; r < in.rooms; r++) {
      for (int s = 0; s < in.shifts; s++) {
        int d = s / in.shifts_per_day;
        int n = cur.room_shift_nurse[r][s];
        if ((n == -1 || !in.nurses_vect[n].is_working_in_shift[s]) && !in.available_nurses[s].empty()) {
          n = in.available_nurses[s][0];
          cur.room_shift_nurse[r][s] = n;
        }
        int load = 0;
        for (int e : room_day_patients[r][d]) {
          int w_prod = 0, req_skill = 0;
          if (e < in.patients) {
            int s1 = s - cur.admission_day[e] * in.shifts_per_day;
            w_prod = in.patients_vect[e].workload_produced[s1];
            req_skill = in.patients_vect[e].skill_level_required[s1];
          } else {
            int f = e - in.patients;
            w_prod = in.occupants_vect[f].workload_produced[s];
            req_skill = in.occupants_vect[f].skill_level_required[s];
          }
          load += w_prod;
          for (int sk = 0; sk <= in.skill_levels; sk++) {
            if (req_skill > sk) room_shift_skill_pen[r][s][sk] += (req_skill - sk);
          }
          if (n != -1) {
            if (entity_nurse_count[e][n] == 0) {
              entity_distinct_nurses[e]++;
              cost_continuity += in.weights[2];
            }
            entity_nurse_count[e][n]++;
          }
        }
        room_shift_load[r][s] = load;
        if (n != -1) {
          nurse_shift_load[n][s] += load;
          cost_skill += (long long)room_shift_skill_pen[r][s][in.nurses_vect[n].skill_level] * in.weights[1];
        }
      }
    }

    for (int n = 0; n < in.nurses; n++) {
      for (int s : in.nurses_vect[n].working_shifts) {
        int ex = max(0, nurse_shift_load[n][s] - in.nurses_vect[n].max_loads[s]);
        cost_workload += (long long)ex * in.weights[3];
      }
    }
  }

  long long TotalCost() const {
    return cost_age_mix + cost_skill + cost_continuity + cost_workload +
           cost_open_ot + cost_surgeon_transfer + cost_delay + cost_unscheduled;
  }

  long long DeltaAssignNurse(int r, int s, int n2) const {
    int n1 = cur.room_shift_nurse[r][s];
    if (n1 == n2) return 0;
    int d = s / in.shifts_per_day;
    const auto& pats = room_day_patients[r][d];
    if (pats.empty()) return 0;

    long long delta = 0;
    int sk1 = in.nurses_vect[n1].skill_level;
    int sk2 = in.nurses_vect[n2].skill_level;
    if (sk1 != sk2) {
      delta += (long long)(room_shift_skill_pen[r][s][sk2] - room_shift_skill_pen[r][s][sk1]) * in.weights[1];
    }

    int ld = room_shift_load[r][s];
    if (ld > 0) {
      int old_ex1 = max(0, nurse_shift_load[n1][s] - in.nurses_vect[n1].max_loads[s]);
      int new_ex1 = max(0, nurse_shift_load[n1][s] - ld - in.nurses_vect[n1].max_loads[s]);
      int old_ex2 = max(0, nurse_shift_load[n2][s] - in.nurses_vect[n2].max_loads[s]);
      int new_ex2 = max(0, nurse_shift_load[n2][s] + ld - in.nurses_vect[n2].max_loads[s]);
      delta += (long long)((new_ex1 - old_ex1) + (new_ex2 - old_ex2)) * in.weights[3];
    }

    int cont_diff = 0;
    for (int e : pats) {
      if (entity_nurse_count[e][n1] == 1) cont_diff--;
      if (entity_nurse_count[e][n2] == 0) cont_diff++;
    }
    delta += (long long)cont_diff * in.weights[2];
    return delta;
  }

  void ApplyAssignNurse(int r, int s, int n2) {
    int n1 = cur.room_shift_nurse[r][s];
    if (n1 == n2) return;
    int d = s / in.shifts_per_day;
    const auto& pats = room_day_patients[r][d];
    if (!pats.empty()) {
      int sk1 = in.nurses_vect[n1].skill_level;
      int sk2 = in.nurses_vect[n2].skill_level;
      cost_skill += (long long)(room_shift_skill_pen[r][s][sk2] - room_shift_skill_pen[r][s][sk1]) * in.weights[1];

      int ld = room_shift_load[r][s];
      int old_ex1 = max(0, nurse_shift_load[n1][s] - in.nurses_vect[n1].max_loads[s]);
      int new_ex1 = max(0, nurse_shift_load[n1][s] - ld - in.nurses_vect[n1].max_loads[s]);
      int old_ex2 = max(0, nurse_shift_load[n2][s] - in.nurses_vect[n2].max_loads[s]);
      int new_ex2 = max(0, nurse_shift_load[n2][s] + ld - in.nurses_vect[n2].max_loads[s]);
      cost_workload += (long long)((new_ex1 - old_ex1) + (new_ex2 - old_ex2)) * in.weights[3];
      nurse_shift_load[n1][s] -= ld;
      nurse_shift_load[n2][s] += ld;

      for (int e : pats) {
        if (--entity_nurse_count[e][n1] == 0) {
          entity_distinct_nurses[e]--;
          cost_continuity -= in.weights[2];
        }
        if (entity_nurse_count[e][n2]++ == 0) {
          entity_distinct_nurses[e]++;
          cost_continuity += in.weights[2];
        }
      }
    }
    cur.room_shift_nurse[r][s] = n2;
  }

  long long DeltaSwapNurses(int r1, int r2, int s) const {
    int n1 = cur.room_shift_nurse[r1][s];
    int n2 = cur.room_shift_nurse[r2][s];
    if (n1 == n2) return 0;
    int d = s / in.shifts_per_day;
    const auto& p1 = room_day_patients[r1][d];
    const auto& p2 = room_day_patients[r2][d];
    if (p1.empty() && p2.empty()) return 0;

    long long delta = 0;
    int sk1 = in.nurses_vect[n1].skill_level;
    int sk2 = in.nurses_vect[n2].skill_level;
    if (sk1 != sk2) {
      int pen_before = room_shift_skill_pen[r1][s][sk1] + room_shift_skill_pen[r2][s][sk2];
      int pen_after  = room_shift_skill_pen[r1][s][sk2] + room_shift_skill_pen[r2][s][sk1];
      delta += (long long)(pen_after - pen_before) * in.weights[1];
    }

    int ld1 = room_shift_load[r1][s];
    int ld2 = room_shift_load[r2][s];
    if (ld1 != ld2) {
      int diff = ld2 - ld1;
      int old_ex1 = max(0, nurse_shift_load[n1][s] - in.nurses_vect[n1].max_loads[s]);
      int new_ex1 = max(0, nurse_shift_load[n1][s] + diff - in.nurses_vect[n1].max_loads[s]);
      int old_ex2 = max(0, nurse_shift_load[n2][s] - in.nurses_vect[n2].max_loads[s]);
      int new_ex2 = max(0, nurse_shift_load[n2][s] - diff - in.nurses_vect[n2].max_loads[s]);
      delta += (long long)((new_ex1 - old_ex1) + (new_ex2 - old_ex2)) * in.weights[3];
    }

    int cont_diff = 0;
    for (int e : p1) {
      if (entity_nurse_count[e][n1] == 1) cont_diff--;
      if (entity_nurse_count[e][n2] == 0) cont_diff++;
    }
    for (int e : p2) {
      if (entity_nurse_count[e][n2] == 1) cont_diff--;
      if (entity_nurse_count[e][n1] == 0) cont_diff++;
    }
    delta += (long long)cont_diff * in.weights[2];
    return delta;
  }

  void ApplySwapNurses(int r1, int r2, int s) {
    int n1 = cur.room_shift_nurse[r1][s];
    int n2 = cur.room_shift_nurse[r2][s];
    if (n1 == n2) return;
    ApplyAssignNurse(r1, s, n2);
    ApplyAssignNurse(r2, s, n1);
  }

  void PolishNursesOnRooms(const vector<int>& rooms_to_polish, int d_start, int d_end) {
    bool improved = true;
    int pass = 0;
    while (improved && pass < 3) {
      improved = false;
      pass++;
      for (int d = max(0, d_start); d < min(in.days, d_end); d++) {
        for (int sp = 0; sp < in.shifts_per_day; sp++) {
          int s = d * in.shifts_per_day + sp;
          for (int r : rooms_to_polish) {
            if (room_day_patients[r][d].empty()) continue;
            int best_n = cur.room_shift_nurse[r][s];
            long long best_d = 0;
            for (int n2 : in.available_nurses[s]) {
              long long dl = DeltaAssignNurse(r, s, n2);
              if (dl < best_d) {
                best_d = dl;
                best_n = n2;
              }
            }
            if (best_d < 0) {
              ApplyAssignNurse(r, s, best_n);
              improved = true;
            }
          }
          for (int r1 : rooms_to_polish) {
            if (room_day_patients[r1][d].empty()) continue;
            for (int r2 = 0; r2 < in.rooms; r2++) {
              if (r1 == r2 || room_day_patients[r2][d].empty()) continue;
              long long dl = DeltaSwapNurses(r1, r2, s);
              if (dl < 0) {
                ApplySwapNurses(r1, r2, s);
                improved = true;
              }
            }
          }
        }
      }
    }
  }

  // Fast incremental removal/addition on occupancy/capacity counters only (prior to RebuildAll)
  void UnschedulePatientCounts(int p) {
    int ad = cur.admission_day[p];
    if (ad == -1) return;
    int r = cur.room[p];
    int t = cur.operating_room[p];
    int end_d = min(in.days, ad + in.patients_vect[p].length_of_stay);
    for (int d = ad; d < end_d; d++) {
      auto& vec = room_day_patients[r][d];
      for (size_t i = 0; i < vec.size(); i++) {
        if (vec[i] == p) {
          vec[i] = vec.back();
          vec.pop_back();
          break;
        }
      }
      if (in.patients_vect[p].gender == Gender::A) room_day_a[r][d]--;
      else room_day_b[r][d]--;
    }
    int dur = in.patients_vect[p].surgery_duration;
    ot_day_load[t][ad] -= dur;
    ot_day_count[t][ad]--;
    int u = in.patients_vect[p].surgeon;
    surgeon_day_load[u][ad] -= dur;
    surgeon_day_ot_count[u][ad][t]--;
    cur.admission_day[p] = -1;
    cur.room[p] = -1;
    cur.operating_room[p] = -1;
  }

  void SchedulePatientCounts(int p, int ad, int r, int t) {
    cur.admission_day[p] = ad;
    cur.room[p] = r;
    cur.operating_room[p] = t;
    int end_d = min(in.days, ad + in.patients_vect[p].length_of_stay);
    for (int d = ad; d < end_d; d++) {
      room_day_patients[r][d].push_back(p);
      if (in.patients_vect[p].gender == Gender::A) room_day_a[r][d]++;
      else room_day_b[r][d]++;
    }
    int dur = in.patients_vect[p].surgery_duration;
    ot_day_load[t][ad] += dur;
    ot_day_count[t][ad]++;
    int u = in.patients_vect[p].surgeon;
    surgeon_day_load[u][ad] += dur;
    surgeon_day_ot_count[u][ad][t]++;
  }

  bool IsPatientPlacementFeasible(int p, int ad, int r, int t) const {
    if (ad < in.patients_vect[p].surgery_release_day || ad > in.PatientLastPossibleDay(p)) return false;
    if (in.patients_vect[p].incompatible_rooms[r]) return false;
    int dur = in.patients_vect[p].surgery_duration;
    int u = in.patients_vect[p].surgeon;
    if (surgeon_day_load[u][ad] + dur > in.surgeons_vect[u].max_surgery_time[ad]) return false;
    if (ot_day_load[t][ad] + dur > in.operating_theaters_vect[t].availability[ad]) return false;

    int end_d = min(in.days, ad + in.patients_vect[p].length_of_stay);
    Gender g = in.patients_vect[p].gender;
    int cap = in.rooms_vect[r].capacity;
    for (int d = ad; d < end_d; d++) {
      if ((int)room_day_patients[r][d].size() + 1 > cap) return false;
      if (g == Gender::A && room_day_b[r][d] > 0) return false;
      if (g == Gender::B && room_day_a[r][d] > 0) return false;
    }
    return true;
  }

  bool CanMovePatientRoom(int p, int r2) const {
    int ad = cur.admission_day[p];
    if (ad == -1 || cur.room[p] == r2) return false;
    if (in.patients_vect[p].incompatible_rooms[r2]) return false;
    int end_d = min(in.days, ad + in.patients_vect[p].length_of_stay);
    Gender g = in.patients_vect[p].gender;
    int cap = in.rooms_vect[r2].capacity;
    for (int d = ad; d < end_d; d++) {
      if ((int)room_day_patients[r2][d].size() + 1 > cap) return false;
      if (g == Gender::A && room_day_b[r2][d] > 0) return false;
      if (g == Gender::B && room_day_a[r2][d] > 0) return false;
    }
    return true;
  }

  bool CanSwapPatientRooms(int p1, int p2) const {
    int ad1 = cur.admission_day[p1], ad2 = cur.admission_day[p2];
    if (ad1 == -1 || ad2 == -1) return false;
    int r1 = cur.room[p1], r2 = cur.room[p2];
    if (r1 == r2) return false;
    if (in.patients_vect[p1].incompatible_rooms[r2] || in.patients_vect[p2].incompatible_rooms[r1]) return false;

    int end1 = min(in.days, ad1 + in.patients_vect[p1].length_of_stay);
    int end2 = min(in.days, ad2 + in.patients_vect[p2].length_of_stay);
    Gender g1 = in.patients_vect[p1].gender;
    Gender g2 = in.patients_vect[p2].gender;

    for (int d = min(ad1, ad2); d < max(end1, end2); d++) {
      bool in1 = (d >= ad1 && d < end1);
      bool in2 = (d >= ad2 && d < end2);
      int sz1 = (int)room_day_patients[r1][d].size() - (in1 ? 1 : 0) + (in2 ? 1 : 0);
      if (sz1 > in.rooms_vect[r1].capacity) return false;
      int a1 = room_day_a[r1][d] - (in1 && g1 == Gender::A ? 1 : 0) + (in2 && g2 == Gender::A ? 1 : 0);
      int b1 = room_day_b[r1][d] - (in1 && g1 == Gender::B ? 1 : 0) + (in2 && g2 == Gender::B ? 1 : 0);
      if (a1 > 0 && b1 > 0) return false;

      int sz2 = (int)room_day_patients[r2][d].size() - (in2 ? 1 : 0) + (in1 ? 1 : 0);
      if (sz2 > in.rooms_vect[r2].capacity) return false;
      int a2 = room_day_a[r2][d] - (in2 && g2 == Gender::A ? 1 : 0) + (in1 && g1 == Gender::A ? 1 : 0);
      int b2 = room_day_b[r2][d] - (in2 && g2 == Gender::B ? 1 : 0) + (in1 && g1 == Gender::B ? 1 : 0);
      if (a2 > 0 && b2 > 0) return false;
    }
    return true;
  }
};

int main(int argc, char* argv[]) {
  if (argc < 4) {
    cerr << "Usage: " << argv[0] << " <instance.json> <initial_sol.json> <output_best.json> [seconds=30] [seed=42]" << endl;
    return 1;
  }
  string inst_file = argv[1];
  string sol_file = argv[2];
  string out_file = argv[3];
  double max_seconds = (argc >= 5) ? atof(argv[4]) : 30.0;
  uint64_t seed = (argc >= 6) ? strtoull(argv[5], nullptr, 10) : 42ULL;

  IHTP_Input in(inst_file);
  FastEval ev(in);
  ev.LoadJSON(sol_file);

  long long init_cost = ev.TotalCost();
  long long best_cost = init_cost;
  SolutionState best_state = ev.cur;

  mt19937_64 rng(seed);
  auto t_start = chrono::steady_clock::now();

  vector<int> all_rooms(in.rooms);
  for (int r = 0; r < in.rooms; r++) all_rooms[r] = r;
  ev.PolishNursesOnRooms(all_rooms, 0, in.days);
  if (ev.TotalCost() < best_cost) {
    best_cost = ev.TotalCost();
    best_state = ev.cur;
    ev.SaveJSON(out_file);
    cout << "[GREEDY NRA] Improved " << inst_file << " from " << init_cost << " -> " << best_cost << endl;
  }

  double T_start = 12.0;
  double T_end = 0.05;
  long long iter = 0;

  while (true) {
    auto now = chrono::steady_clock::now();
    double elapsed = chrono::duration<double>(now - t_start).count();
    if (elapsed >= max_seconds) break;

    double progress = elapsed / max_seconds;
    double cycle_prog = fmod(progress * 6.0, 1.0);
    double T = T_start * 0.4 * pow(T_end / (T_start * 0.4), cycle_prog);

    // Inner loop: 250 fast Nurse (NRA) moves
    for (int k = 0; k < 250; k++) {
      iter++;
      int move_type = rng() % 100;
      if (move_type < 50) {
        int r = rng() % in.rooms;
        int s = rng() % in.shifts;
        int d = s / in.shifts_per_day;
        if (ev.room_day_patients[r][d].empty()) continue;
        const auto& avail = in.available_nurses[s];
        if (avail.size() <= 1) continue;
        int n2 = avail[rng() % avail.size()];
        if (n2 == ev.cur.room_shift_nurse[r][s]) continue;
        long long dl = ev.DeltaAssignNurse(r, s, n2);
        if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
          ev.ApplyAssignNurse(r, s, n2);
          if (ev.TotalCost() < best_cost) {
            best_cost = ev.TotalCost();
            best_state = ev.cur;
            ev.SaveJSON(out_file);
            cout << "[NRA-1] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
          }
        }
      } else if (move_type < 80) {
        if (in.rooms < 2) continue;
        int s = rng() % in.shifts;
        int d = s / in.shifts_per_day;
        int r1 = rng() % in.rooms;
        int r2 = rng() % in.rooms;
        if (r1 == r2) continue;
        if (ev.room_day_patients[r1][d].empty() && ev.room_day_patients[r2][d].empty()) continue;
        long long dl = ev.DeltaSwapNurses(r1, r2, s);
        if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
          ev.ApplySwapNurses(r1, r2, s);
          if (ev.TotalCost() < best_cost) {
            best_cost = ev.TotalCost();
            best_state = ev.cur;
            ev.SaveJSON(out_file);
            cout << "[NRA-SWAP] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
          }
        }
      } else {
        int tot_e = in.patients + in.occupants;
        int e = rng() % tot_e;
        int r = -1, ad = 0, len = 0;
        if (e < in.patients) {
          ad = ev.cur.admission_day[e];
          if (ad == -1) continue;
          r = ev.cur.room[e];
          len = in.patients_vect[e].length_of_stay;
        } else {
          int f = e - in.patients;
          ad = 0;
          r = in.occupants_vect[f].assigned_room;
          len = in.occupants_vect[f].length_of_stay;
        }
        int end_d = min(in.days, ad + len);
        if (ad >= end_d) continue;
        int d1 = ad + (rng() % (end_d - ad));
        int s1 = d1 * in.shifts_per_day + (rng() % in.shifts_per_day);
        int n_target = ev.cur.room_shift_nurse[r][s1];
        if (n_target == -1) continue;

        int d2 = ad + (rng() % (end_d - ad));
        int s2 = d2 * in.shifts_per_day + (rng() % in.shifts_per_day);
        if (s1 == s2 || !in.nurses_vect[n_target].is_working_in_shift[s2]) continue;
        int n_old = ev.cur.room_shift_nurse[r][s2];
        if (n_old == n_target) continue;

        long long dl_direct = ev.DeltaAssignNurse(r, s2, n_target);
        int best_r_other = -1;
        long long dl_swap = 1e18;
        for (int r_o = 0; r_o < in.rooms; r_o++) {
          if (r_o != r && ev.cur.room_shift_nurse[r_o][s2] == n_target) {
            long long d_sw = ev.DeltaSwapNurses(r, r_o, s2);
            if (d_sw < dl_swap) {
              dl_swap = d_sw;
              best_r_other = r_o;
            }
          }
        }
        if (dl_swap < dl_direct && best_r_other != -1) {
          if (dl_swap <= 0 || exp(-dl_swap / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
            ev.ApplySwapNurses(r, best_r_other, s2);
            if (ev.TotalCost() < best_cost) {
              best_cost = ev.TotalCost();
              best_state = ev.cur;
              ev.SaveJSON(out_file);
              cout << "[NRA-KEMPE] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
            }
          }
        } else {
          if (dl_direct <= 0 || exp(-dl_direct / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
            ev.ApplyAssignNurse(r, s2, n_target);
            if (ev.TotalCost() < best_cost) {
              best_cost = ev.TotalCost();
              best_state = ev.cur;
              ev.SaveJSON(out_file);
              cout << "[NRA-CONT] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
            }
          }
        }
      }
    }

    // Coupled Patient + Nurse Moves
    int p_move = rng() % 100;
    if (p_move < 20) {
      // Operating theater move on same day
      int p = rng() % in.patients;
      int ad = ev.cur.admission_day[p];
      if (ad != -1 && in.operating_theaters > 1) {
        int t_old = ev.cur.operating_room[p];
        int t_new = rng() % in.operating_theaters;
        int dur = in.patients_vect[p].surgery_duration;
        if (t_new != t_old && ev.ot_day_load[t_new][ad] + dur <= in.operating_theaters_vect[t_new].availability[ad]) {
          int u = in.patients_vect[p].surgeon;
          long long dl = 0;
          if (ev.ot_day_count[t_old][ad] == 1) dl -= in.weights[4];
          if (ev.ot_day_count[t_new][ad] == 0) dl += in.weights[4];
          int old_u_ots = 0, new_u_ots = 0;
          for (int t = 0; t < in.operating_theaters; t++) {
            if (ev.surgeon_day_ot_count[u][ad][t] > 0) old_u_ots++;
            int c = ev.surgeon_day_ot_count[u][ad][t] - (t == t_old ? 1 : 0) + (t == t_new ? 1 : 0);
            if (c > 0) new_u_ots++;
          }
          dl += (long long)(max(0, new_u_ots - 1) - max(0, old_u_ots - 1)) * in.weights[5];
          if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
            ev.ot_day_load[t_old][ad] -= dur;
            ev.ot_day_count[t_old][ad]--;
            ev.ot_day_load[t_new][ad] += dur;
            ev.ot_day_count[t_new][ad]++;
            ev.surgeon_day_ot_count[u][ad][t_old]--;
            ev.surgeon_day_ot_count[u][ad][t_new]++;
            ev.cur.operating_room[p] = t_new;
            ev.cost_open_ot += (ev.ot_day_count[t_new][ad] == 1 ? in.weights[4] : 0) - (ev.ot_day_count[t_old][ad] == 0 ? in.weights[4] : 0);
            ev.cost_surgeon_transfer += (long long)(max(0, new_u_ots - 1) - max(0, old_u_ots - 1)) * in.weights[5];
            if (ev.TotalCost() < best_cost) {
              best_cost = ev.TotalCost();
              best_state = ev.cur;
              ev.SaveJSON(out_file);
              cout << "[SCP-OT] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
            }
          }
        }
      }
    } else if (p_move < 45) {
      // Move patient p to another feasible room r2 on same admission day + polish nurses
      int p = rng() % in.patients;
      int ad = ev.cur.admission_day[p];
      if (ad != -1 && in.rooms > 1) {
        int r1 = ev.cur.room[p];
        int r2 = rng() % in.rooms;
        if (ev.CanMovePatientRoom(p, r2)) {
          SolutionState backup = ev.cur;
          long long old_total = ev.TotalCost();
          ev.cur.room[p] = r2;
          ev.RebuildAll();
          int end_d = min(in.days, ad + in.patients_vect[p].length_of_stay);
          ev.PolishNursesOnRooms({r1, r2}, ad, end_d);
          long long new_total = ev.TotalCost();
          long long dl = new_total - old_total;
          if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
            if (new_total < best_cost) {
              best_cost = new_total;
              best_state = ev.cur;
              ev.SaveJSON(out_file);
              cout << "[PAS-ROOM] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
            }
          } else {
            ev.cur = backup;
            ev.RebuildAll();
          }
        }
      }
    } else if (p_move < 70) {
      // Swap rooms of two patients p1, p2 + polish nurses
      int p1 = rng() % in.patients;
      int p2 = rng() % in.patients;
      if (p1 != p2 && ev.CanSwapPatientRooms(p1, p2)) {
        SolutionState backup = ev.cur;
        long long old_total = ev.TotalCost();
        int r1 = ev.cur.room[p1], r2 = ev.cur.room[p2];
        int d_min = min(ev.cur.admission_day[p1], ev.cur.admission_day[p2]);
        int d_max = max(min(in.days, ev.cur.admission_day[p1] + in.patients_vect[p1].length_of_stay),
                        min(in.days, ev.cur.admission_day[p2] + in.patients_vect[p2].length_of_stay));
        swap(ev.cur.room[p1], ev.cur.room[p2]);
        ev.RebuildAll();
        ev.PolishNursesOnRooms({r1, r2}, d_min, d_max);
        long long new_total = ev.TotalCost();
        long long dl = new_total - old_total;
        if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
          if (new_total < best_cost) {
            best_cost = new_total;
            best_state = ev.cur;
            ev.SaveJSON(out_file);
            cout << "[PAS-SWAP] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
          }
        } else {
          ev.cur = backup;
          ev.RebuildAll();
        }
      }
    } else if (p_move < 88) {
      // Move patient p to a new (ad_new, r_new, t_new)
      int p = rng() % in.patients;
      int old_ad = ev.cur.admission_day[p];
      int old_r = ev.cur.room[p];
      int old_t = ev.cur.operating_room[p];
      int rel = in.patients_vect[p].surgery_release_day;
      int due = in.PatientLastPossibleDay(p);
      if (due >= rel) {
        if (old_ad != -1) ev.UnschedulePatientCounts(p);
        int ad_new = rel + (rng() % (due - rel + 1));
        int r_new = rng() % in.rooms;
        int t_new = rng() % in.operating_theaters;
        if (ev.IsPatientPlacementFeasible(p, ad_new, r_new, t_new) && !(ad_new == old_ad && r_new == old_r && t_new == old_t)) {
          if (old_ad != -1) ev.SchedulePatientCounts(p, old_ad, old_r, old_t);
          SolutionState backup = ev.cur;
          long long old_total = ev.TotalCost();
          ev.cur.admission_day[p] = ad_new;
          ev.cur.room[p] = r_new;
          ev.cur.operating_room[p] = t_new;
          ev.RebuildAll();
          vector<int> rms = {r_new};
          if (old_r != -1 && old_r != r_new) rms.push_back(old_r);
          int d0 = (old_ad != -1) ? min(old_ad, ad_new) : ad_new;
          int d1 = min(in.days, max(old_ad != -1 ? old_ad : ad_new, ad_new) + in.patients_vect[p].length_of_stay);
          ev.PolishNursesOnRooms(rms, d0, d1);
          long long new_total = ev.TotalCost();
          long long dl = new_total - old_total;
          if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
            if (new_total < best_cost) {
              best_cost = new_total;
              best_state = ev.cur;
              ev.SaveJSON(out_file);
              cout << "[SCP-FULL] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
            }
          } else {
            ev.cur = backup;
            ev.RebuildAll();
          }
        } else {
          if (old_ad != -1) ev.SchedulePatientCounts(p, old_ad, old_r, old_t);
        }
      }
    } else {
      // 2-Patient Full Schedule Swap / Ruin-and-Recreate:
      // Unschedule p1 and p2, try swapping their (ad, r, t) or (ad, r) or re-inserting both
      int p1 = rng() % in.patients;
      int p2 = rng() % in.patients;
      if (p1 != p2 && ev.cur.admission_day[p1] != -1 && ev.cur.admission_day[p2] != -1) {
        int ad1 = ev.cur.admission_day[p1], r1 = ev.cur.room[p1], t1 = ev.cur.operating_room[p1];
        int ad2 = ev.cur.admission_day[p2], r2 = ev.cur.room[p2], t2 = ev.cur.operating_room[p2];
        ev.UnschedulePatientCounts(p1);
        ev.UnschedulePatientCounts(p2);
        // Try assigning p1 to (ad2, r2, t2 or t1) and p2 to (ad1, r1, t1 or t2)
        int try_t1 = (in.patients_vect[p1].surgeon == in.patients_vect[p2].surgeon) ? t2 : t1;
        int try_t2 = (in.patients_vect[p1].surgeon == in.patients_vect[p2].surgeon) ? t1 : t2;
        bool ok = false;
        if (ev.IsPatientPlacementFeasible(p1, ad2, r2, try_t1)) {
          ev.SchedulePatientCounts(p1, ad2, r2, try_t1);
          if (ev.IsPatientPlacementFeasible(p2, ad1, r1, try_t2)) {
            ok = true;
          }
          ev.UnschedulePatientCounts(p1);
        }
        ev.SchedulePatientCounts(p1, ad1, r1, t1);
        ev.SchedulePatientCounts(p2, ad2, r2, t2);
        if (ok) {
          SolutionState backup = ev.cur;
          long long old_total = ev.TotalCost();
          ev.cur.admission_day[p1] = ad2; ev.cur.room[p1] = r2; ev.cur.operating_room[p1] = try_t1;
          ev.cur.admission_day[p2] = ad1; ev.cur.room[p2] = r1; ev.cur.operating_room[p2] = try_t2;
          ev.RebuildAll();
          vector<int> rms = {r1};
          if (r2 != r1) rms.push_back(r2);
          ev.PolishNursesOnRooms(rms, min(ad1, ad2), in.days);
          long long new_total = ev.TotalCost();
          long long dl = new_total - old_total;
          if (dl <= 0 || exp(-dl / T) > uniform_real_distribution<double>(0.0, 1.0)(rng)) {
            if (new_total < best_cost) {
              best_cost = new_total;
              best_state = ev.cur;
              ev.SaveJSON(out_file);
              cout << "[SCP-2SWAP] Improved " << inst_file << " to " << best_cost << " (init " << init_cost << ") at " << fixed << setprecision(1) << elapsed << "s" << endl;
            }
          } else {
            ev.cur = backup;
            ev.RebuildAll();
          }
        }
      }
    }

    if (ev.TotalCost() > best_cost + 50 && (rng() % 25 == 0)) {
      ev.cur = best_state;
      ev.RebuildAll();
    }
  }

  ev.cur = best_state;
  ev.RebuildAll();
  ev.PolishNursesOnRooms(all_rooms, 0, in.days);
  if (ev.TotalCost() < best_cost) {
    best_cost = ev.TotalCost();
    best_state = ev.cur;
  }
  ev.SaveJSON(out_file);
  cout << "[DONE] " << inst_file << " | Init: " << init_cost << " | Best: " << best_cost << " | Delta: " << (best_cost - init_cost) << " | Iters: " << iter << endl;
  return 0;
}
