// Solution validator for the Integrated Healthcare Timetabling Problem (IHTP)
// of the Integrated Healthcare Timetabling Competition (IHTC)
// Version 0.0 (23/05/24)
// Instructions:
// 1. Download the JSON library at https://github.com/nlohmann/json/blob/develop/single_include/nlohmann/json.hpp
// 2. Compile with a C++ compiler, for example with the GNU Compiler: g++ -o IHTP_Validator IHTP_Validator.cc 
// 3. Run with: ./IHTP_Validator <instance_file> <solution_file> [verbose] 

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <stdexcept>
#include "json.hpp"

using namespace std; 

enum class Gender { A, B };

class Occupant
{
 public: 
  string id; 
  Gender gender;
  int age_group;
  int length_of_stay;
  vector<int> workload_produced;
  vector<int> skill_level_required;
  int assigned_room = -1;
};

class Patient: public Occupant
{
 public: 
  bool mandatory;
  int surgery_release_day;
  int surgery_due_day;
  int surgery_duration;
  int surgeon;
  vector<bool> incompatible_rooms;
};

class Surgeon
{
 public: 
  string id;
  vector<int> max_surgery_time;
};

class OperatingTheater
{
 public: 
  string id;
  vector<int> availability;
};

class Room
{
 public: 
  string id;
  int capacity;
};

class Nurse
{
 public: 
  string id;
  int skill_level;
  vector<int> working_shifts; // list of working shifts
  vector<bool> is_working_in_shift; // for all shift
  vector<int> max_loads; // for all shifts (0 when absent)
};

class IHTP_Input
{
 public:
  IHTP_Input(string file_name);
  int Days() const { return days; }
  int ShiftsPerDay() const { return shifts_per_day; }
  int Shifts() const { return shifts; }
  int Patients() const { return patients; }
  int Occupants() const {return occupants; }
  int SkillLevels() const { return skill_levels; }
  int AgeGroups() const { return age_groups; }
  int Surgeons() const { return surgeons; }
  int OperatingTheaters() const { return operating_theaters; }
  int Rooms() const { return rooms; }
  int Nurses() const { return nurses; }

// Nurses
  string NurseId(int n) const { return nurses_vect[n].id; }
  int NurseSkillLevel(int n) const { return nurses_vect[n].skill_level; }
  bool IsNurseWorkingInShift(int n, int s) const { return nurses_vect[n].is_working_in_shift[s]; }
  int NurseWorkingShifts(int n) const { return nurses_vect[n].working_shifts.size(); }
  int NurseWorkingShift(int n, int i) const { return nurses_vect[n].working_shifts[i]; }
  int AvailableNurses(int s) const { return available_nurses[s].size(); }
  int AvailableNurse(int s, int i) const { return available_nurses[s][i]; }
  int NurseMaxLoad(int n, int s) const { return nurses_vect[n].max_loads[s]; }

//Occupants
  string OccupantId(int p) const { return occupants_vect[p].id; }
  Gender OccupantGender(int p) const { return occupants_vect[p].gender; }
  int OccupantAgeGroup(int p) const { return occupants_vect[p].age_group; }
  int OccupantLengthOfStay(int p) const { return occupants_vect[p].length_of_stay; }
  int OccupantRoom(int p) const {return occupants_vect[p].assigned_room; }
  int OccupantSkillLevelRequired (int p, int s) const  { return occupants_vect[p].skill_level_required[s]; }
  int OccupantWorkloadProduced (int p, int s) const { return occupants_vect[p].workload_produced[s]; }
  int OccupantsPresent(int r,int d) const {return room_day_fixed_list[r][d].size();}
  int OccupantPresence(int r,int d,int i) const{return room_day_fixed_list[r][d][i];}

// Patients
  string PatientId(int p) const { return patients_vect[p].id; }
  Gender PatientGender(int p) const { return patients_vect[p].gender; }
  int PatientSurgeryReleaseDay(int p) const { return patients_vect[p].surgery_release_day; }
  int PatientAgeGroup(int p) const { return patients_vect[p].age_group; }
  int PatientLengthOfStay(int p) const { return patients_vect[p].length_of_stay; }
  int PatientSurgeryDueDay(int p) const { return patients_vect[p].surgery_due_day; }
  int PatientLastPossibleDay(int p) const { return PatientMandatory(p) ? patients_vect[p].surgery_due_day : days-1; }
  int PatientSurgeryDuration(int p) const { return patients_vect[p].surgery_duration; }
  int PatientSurgeon(int p) const { return patients_vect[p].surgeon; }
  bool PatientMandatory(int p) const { return patients_vect[p].mandatory; }
  bool IncompatibleRoom(int p, int r) const { return patients_vect[p].incompatible_rooms[r]; }
  int PatientSkillLevelRequired(int p, int s) const  { return patients_vect[p].skill_level_required[s]; }
  int PatientWorkloadProduced(int p, int s) const { return patients_vect[p].workload_produced[s]; }

// Rooms
  string RoomId(int r) const { return rooms_vect[r].id; }
  int RoomCapacity(int r) const { return rooms_vect[r].capacity; }

// Operating theaters and surgeons
  string OperatingTheaterId(int t) const { return operating_theaters_vect[t].id; }
  string SurgeonId(int u) const { return surgeons_vect[u].id; }
  int OperatingTheaterAvailability(int t, int d) const { return operating_theaters_vect[t].availability[d]; }
  int SurgeonMaxSurgeryTime(int s, int d) const { return surgeons_vect[s].max_surgery_time[d]; }
  string ShiftName(int s) const { return shift_names[s]; }
  string ShiftDescription(int s) const;  
  int Weight(int c) const { return weights[c]; }

  int FindAgeGroup(string age_group_name) const;
  int FindSurgeon(string surgeon_id) const;
  int FindShift(string shift_name) const;
  int FindRoom(string room_name) const;
  int FindOperatingTheater(string ot_name) const;
  int FindPatient(string patient_id) const;
  int FindNurse(string nurse_id) const;

 private:
  int days;
  int shifts_per_day;
  int shifts;
  int patients;
  int occupants;
  int skill_levels;
  int age_groups;
  int surgeons;
  int operating_theaters;
  int rooms;
  int nurses;
  const int SOFT_COST_COMPONENTS = 8;
  
  vector<Patient> patients_vect;
  vector<Occupant> occupants_vect;
  vector<Surgeon> surgeons_vect;
  vector<OperatingTheater> operating_theaters_vect;
  vector<Room> rooms_vect;
  vector<Nurse> nurses_vect; 
  vector<string> shift_names, age_group_names;
  vector<vector<vector<int>>> room_day_fixed_list;
  vector<vector<int>> available_nurses;  // list of available nurses per shift
  vector<int> weights;

  void ResizeDataStructures();
};

class IHTP_Output
{
 public:
  IHTP_Output(const IHTP_Input& my_in, string file_name, bool verbose);
  void ReadJSON(string file_name);
  void AssignPatient(int p, int d, int r, int t);
  void AssignNurse(int n, int r, int s);
  void UpdatewithOccupantsInfo();
  void Reset();

  // Getters
  bool ScheduledPatient(int p) const { return admission_day[p] != -1; }
  int AdmissionDay(int p) const { return admission_day[p]; }
  int SurgeonDayLoad(int s, int d) const { return surgeon_day_load[s][d]; }
  int OperatingTheaterDayLoad(int s, int d) const { return operatingtheater_day_load[s][d]; }
  int RoomDayBPatients(int r, int d) const { return room_day_b_patients[r][d]; }
  int RoomDayAPatients(int r, int d) const { return room_day_a_patients[r][d]; }
  int RoomDayLoad(int r, int d) const { return room_day_patient_list[r][d].size(); }
  int RoomDayPatient(int r, int d, int i) const { return room_day_patient_list[r][d][i]; }
  int NurseShiftLoad(int n, int s) const { return nurse_shift_load[n][s]; }
  int SurgeonDayTheaterCount(int s, int d, int t) const { return surgeon_day_theater_count[s][d][t]; }

  // Costs and Constraints
  // SCP (surgery case planning)
  int OperatingTheaterOvertime() const;  
  int SurgeonOvertime() const;  
  int MandatoryUnscheduledPatients() const;  
  int ElectiveUnscheduledPatients() const; 
  int PatientDelay() const;
  int OpenOperatingTheater() const;
  int SurgeonTransfer() const;
  int AdmissionDay() const;
  // PAS (patient admission scheduling) 
  int RoomCapacity() const; 
  int RoomGenderMix() const; 
  int PatientRoomCompatibility() const; 
  int RoomAgeMix() const; 
  // NRA (nurse to room assignment)
  int RoomSkillLevel() const; 
  int NursePresence() const; 
  int UncoveredRoom() const; 
  int ExcessiveNurseWorkload() const;
  int ContinuityOfCare() const;

  int CountDistinctNurses(int p) const;
  int CountOccupantNurses(int o) const;

  void PrintCosts() const;
 private:
  const IHTP_Input& in;
  const bool VERBOSE;

  // patient data
  vector<int> admission_day;  // -1 for patients postponed
  vector<int> room;
  vector<int> operating_room;

  // patient data (redundant)
  vector<vector<int>> patient_shift_nurse; // nurse assigned to the patient in the shift
  // room data (redundant)
  vector<vector<vector<int>>> room_day_patient_list;
  vector<vector<int>> room_day_b_patients, room_day_a_patients;

  // nurse data
  vector<vector<int>> room_shift_nurse; // nurse assigned to the room in the sifht
  vector<vector<vector<int>>> nurse_shift_room_list; // list of rooms assigned to the nurse in the shift 
  vector<vector<int>> nurse_shift_load;
  
  // operating theaters and surgeons (redundant)
  vector<vector<vector<int>>> operatingtheater_day_patient_list;
  vector<vector<int>> operatingtheater_day_load, surgeon_day_load;
  vector<vector<vector<int>>> surgeon_day_theater_count; // number of operations per surgeon per day per theater
};

IHTP_Input::IHTP_Input(string file_name)
  : weights(SOFT_COST_COMPONENTS) 
{
  unsigned i;
  int d, f, p, n, ag, sn, s, r, ot;
  nlohmann::json j_in, j_f, j_p, j_r, j_s, j_ot, j_n;
  ifstream is(file_name);
  
  if(!is)
    throw invalid_argument("Cannot open input file " + file_name);
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
  
  for (sn = 0; sn < shifts_per_day; sn++)
    shift_names[sn] =  j_in["shift_types"][sn];
  for (ag = 0; ag < age_groups; ag++)
    age_group_names[ag] = j_in["age_groups"][ag];

  for (s = 0; s < surgeons; s++)
  {
    j_s = j_in["surgeons"][s];
    surgeons_vect[s].id = j_s["id"];
    for (d = 0; d < days; d++)
      surgeons_vect[s].max_surgery_time[d] = j_s["max_surgery_time"][d];
  }

  for (ot = 0; ot < operating_theaters; ot++)
  {
    j_ot = j_in["operating_theaters"][ot];
    operating_theaters_vect[ot].id = j_ot["id"];
    for (d = 0; d < days; d++)
      operating_theaters_vect[ot].availability[d] = j_ot["availability"][d];
  }
  for (r = 0; r < rooms; r++)
  { // rooms must be read before patients, due to incompatibilities
    j_r = j_in["rooms"][r];
    rooms_vect[r].id = j_r["id"];
    rooms_vect[r].capacity = j_r["capacity"];
  }
  room_day_fixed_list.resize(rooms,vector<vector<int>>(days));
  for (f = 0; f < occupants; f++){
    j_f = j_in["occupants"][f];
    occupants_vect[f].id = j_f["id"];
    if (j_f["gender"] == "A")
      occupants_vect[f].gender = Gender::A;
    else
      occupants_vect[f].gender = Gender::B;
    occupants_vect[f].age_group = FindAgeGroup(j_f["age_group"]);
    occupants_vect[f].length_of_stay = j_f["length_of_stay"];
    occupants_vect[f].workload_produced.resize(occupants_vect[f].length_of_stay * shifts_per_day);
    occupants_vect[f].skill_level_required.resize(occupants_vect[f].length_of_stay * shifts_per_day);
    for (s = 0; s < occupants_vect[f].length_of_stay * shifts_per_day; s++)
    {
      occupants_vect[f].workload_produced[s] = j_f["workload_produced"][s];
      occupants_vect[f].skill_level_required[s] = j_f["skill_level_required"][s];
    } 
    r = FindRoom(j_f["room_id"]);
    occupants_vect[f].assigned_room = r;
    for(d = 0; d < occupants_vect[f].length_of_stay; d++)
      room_day_fixed_list[r][d].push_back(f);
  }
  
  for (p = 0; p < patients; p++)
  {
    j_p = j_in["patients"][p];
    patients_vect[p].id = j_p["id"];
    patients_vect[p].mandatory = j_p["mandatory"];
    if (j_p["gender"] == "A")
      patients_vect[p].gender = Gender::A;
    else
      patients_vect[p].gender = Gender::B;
    patients_vect[p].age_group = FindAgeGroup(j_p["age_group"]);

    patients_vect[p].length_of_stay = j_p["length_of_stay"];
    patients_vect[p].surgery_release_day = j_p["surgery_release_day"];
    if (patients_vect[p].mandatory)
      patients_vect[p].surgery_due_day = j_p["surgery_due_day"];
    else
      patients_vect[p].surgery_due_day = -1;
    patients_vect[p].surgery_duration = j_p["surgery_duration"];
    patients_vect[p].surgeon = FindSurgeon(j_p["surgeon_id"]);

    if (!j_p["incompatible_room_ids"].is_null())
    {
      for (i = 0; i < j_p["incompatible_room_ids"].size(); i++)
      {
        r = FindRoom(j_p["incompatible_room_ids"][i]);
        patients_vect[p].incompatible_rooms[r] = true;
      }
    }
    patients_vect[p].workload_produced.resize(patients_vect[p].length_of_stay * shifts_per_day);
    patients_vect[p].skill_level_required.resize(patients_vect[p].length_of_stay * shifts_per_day);
    for (s = 0; s < patients_vect[p].length_of_stay * shifts_per_day; s++)
    {
      patients_vect[p].workload_produced[s] = j_p["workload_produced"][s];
      patients_vect[p].skill_level_required[s] = j_p["skill_level_required"][s];
    }  
  } 

  for (n = 0; n < nurses; n++)
  {
    j_n = j_in["nurses"][n];
    nurses_vect[n].id = j_n["id"];
    nurses_vect[n].skill_level = j_n["skill_level"];
    for (i = 0; i <  j_n["working_shifts"].size(); i++)
    { // compute the global shift index from the day and the shift
      s = static_cast<int>(j_n["working_shifts"][i]["day"]) * shifts_per_day + FindShift(j_n["working_shifts"][i]["shift"]);
      nurses_vect[n].working_shifts.push_back(s);
      nurses_vect[n].is_working_in_shift[s] = true;
      nurses_vect[n].max_loads[s] = j_n["working_shifts"][i]["max_load"];
      available_nurses[s].push_back(n);
    }
  }
}

void IHTP_Input::ResizeDataStructures()
{
  int p, n, s, ot;
  occupants_vect.resize(occupants);
  patients_vect.resize(patients);
  for (p = 0; p < patients; p++)
    patients_vect[p].incompatible_rooms.resize(rooms,false);
  surgeons_vect.resize(surgeons);
  for (s = 0; s < surgeons; s++)
    surgeons_vect[s].max_surgery_time.resize(days);
  operating_theaters_vect.resize(operating_theaters);
  for (ot = 0; ot < operating_theaters; ot++)
    operating_theaters_vect[ot].availability.resize(days);
  rooms_vect.resize(rooms);
  nurses_vect.resize(nurses);  
  for (n = 0; n < nurses; n++)
  {
    nurses_vect[n].is_working_in_shift.resize(shifts, false);
    nurses_vect[n].max_loads.resize(shifts, 0);
  }
  available_nurses.resize(shifts);
  shift_names.resize(shifts_per_day);
  age_group_names.resize(age_groups);
}

int IHTP_Input::FindAgeGroup(string age_group_name) const
{
  for (int i = 0; i < age_groups; i++)
    if (age_group_name == age_group_names[i])
      return i;
  throw invalid_argument("Unknown age group name");
  return -1;          
}

int IHTP_Input::FindSurgeon(string surgeon_id) const
{
  for (int i = 0; i < surgeons; i++)
    if (surgeon_id == surgeons_vect[i].id)
      return i;
  throw invalid_argument("Unknown surgeon id");
  return -1;          
}

int IHTP_Input::FindShift(string shift_name) const
{
  for (int i = 0; i < shifts_per_day; i++)
    if (shift_name == shift_names[i])
      return i;
  throw invalid_argument("Unknown shift name");
  return -1;          
}

string IHTP_Input::ShiftDescription(int s) const
{
  stringstream ss;
  ss << s << " (day" << s/shifts_per_day << "@" << shift_names[s%shifts_per_day] << ")";
  return ss.str();
}

int IHTP_Input::FindRoom(string room_name) const
{
  for (int i = 0; i < rooms; i++)
    if (room_name == rooms_vect[i].id)
      return i;
  throw invalid_argument("Unknown room id " + room_name);
  return -1;          
}

int IHTP_Input::FindOperatingTheater(string ot_name) const
{
  for (int i = 0; i < operating_theaters; i++)
    if (ot_name == operating_theaters_vect[i].id)
      return i;
  throw invalid_argument("Unknown room id " + ot_name);
  return -1;          
}

int IHTP_Input::FindPatient(string patient_id) const
{
  for (int i = 0; i < patients; i++)
    if (patient_id == patients_vect[i].id)
      return i;
  throw invalid_argument("Unknown patient id " + patient_id);
  return -1;          
}

int IHTP_Input::FindNurse(string nurse_id) const
{
  for (int i = 0; i < nurses; i++)
    if (nurse_id == nurses_vect[i].id)
      return i;
  throw invalid_argument("Unknown nurse id " + nurse_id);
  return -1;          
}

IHTP_Output::IHTP_Output(const IHTP_Input& my_in, string file_name, bool verbose)
  : in(my_in), VERBOSE(verbose), admission_day(in.Patients(),-1), room(in.Patients(),-1), 
   operating_room(in.Patients(),-1),
   patient_shift_nurse(in.Patients()+in.Occupants()),
   room_day_patient_list(in.Rooms(), vector<vector<int>>(in.Days())),
   room_day_b_patients(in.Rooms(), vector<int>(in.Days(),0)),
   room_day_a_patients(in.Rooms(), vector<int>(in.Days(),0)),
   room_shift_nurse(in.Rooms(),vector<int>(in.Shifts(),-1)),
   nurse_shift_room_list(in.Nurses(),vector<vector<int>>(in.Shifts())),
   nurse_shift_load(in.Nurses(),vector<int>(in.Shifts(),0)),
   operatingtheater_day_patient_list(in.OperatingTheaters(),vector<vector<int>>(in.Days())),
   operatingtheater_day_load(in.OperatingTheaters(), vector<int>(in.Days(),0)),
   surgeon_day_load(in.Surgeons(), vector<int>(in.Days(),0)),
   surgeon_day_theater_count(in.Surgeons(), vector<vector<int>>(in.Days(), vector<int>(in.OperatingTheaters(),0)))
{
  for (int p = 0; p < in.Patients()+in.Occupants(); p++)
    if(p < in.Patients())
      patient_shift_nurse[p].resize(in.PatientLengthOfStay(p)*in.ShiftsPerDay(),-1);
    else
      patient_shift_nurse[p].resize(in.OccupantLengthOfStay(p-in.Patients())*in.ShiftsPerDay(),-1);

  ReadJSON(file_name);
}

void IHTP_Output::ReadJSON(string file_name)
{
	nlohmann::json j_sol, j_p, j_n;
	unsigned i, j, p, n, cn;
	int d, s, r, t;
	string patient_id, nurse_id, room_id, ot_id, shift_name;
	ifstream is(file_name);

	if(!is)
    throw invalid_argument("Cannot open solution file " + file_name);
  is >> j_sol;
	Reset();
	for (i = 0; i < j_sol["patients"].size(); i++)
	{
	  j_p = j_sol["patients"][i];
	  if (j_p["admission_day"] != "none")
	  {
	    patient_id = j_p["id"];
		  p = in.FindPatient(patient_id);
      if (ScheduledPatient(p))
      {
        stringstream ss;
        ss << "Patient " << p << " assigned twice in the solution";
        throw invalid_argument(ss.str());
      }
		  d = j_p["admission_day"];
      room_id = j_p["room"];
		  r = in.FindRoom(room_id);
      ot_id = j_p["operating_theater"];
		  t = in.FindOperatingTheater(ot_id);
		  AssignPatient(p,d,r,t);
	  }		  
	}
	for (n = 0; n < j_sol["nurses"].size(); n++)
	{
	  j_n = j_sol["nurses"][n];
	  nurse_id = j_n["id"];	
    cn=in.FindNurse(nurse_id);
	  for (i = 0; i < j_n["assignments"].size(); i++)
	  {
		  d = j_n["assignments"][i]["day"];
		  shift_name = j_n["assignments"][i]["shift"];
		  s = d * in.ShiftsPerDay() + in.FindShift(shift_name);
		  for (j = 0; j < j_n["assignments"][i]["rooms"].size(); j++)
		  {
			  room_id = j_n["assignments"][i]["rooms"][j];
			  r = in.FindRoom(room_id);
			  AssignNurse(cn,r,s);
		  }
	  }
	}
}

void IHTP_Output::Reset()
{
    int p, r, s, t, d, n;

    for (p = 0; p < in.Patients(); p++)
    {
      admission_day[p] = -1;
      room[p] = -1;
      operating_room[p] = -1;
    }
    for (r = 0; r < in.Rooms(); r++)
       for (s = 0; s < in.Shifts(); s++)
           room_shift_nurse[r][s] = -1;

    for (n = 0; n < in.Nurses(); n++)
       for (s = 0; s < in.Shifts(); s++)
       {
           nurse_shift_room_list[n][s].clear();
           nurse_shift_load[n][s] = 0;
       }

    for (r = 0; r < in.Rooms(); r++)
       for (d = 0; d < in.Days(); d++)
       {
           room_day_patient_list[r][d].clear();
           room_day_b_patients[r][d] = 0;
           room_day_a_patients[r][d] = 0;
       }

    for (t = 0; t < in.OperatingTheaters(); t++)
       for (d = 0; d < in.Days(); d++)
       {
         operatingtheater_day_patient_list[t][d].clear();
         operatingtheater_day_load[t][d] = 0;
       }
 
    for (s = 0; s < in.Surgeons(); s++)
       for (d = 0; d < in.Days(); d++)
       {
         surgeon_day_load[s][d] = 0;
         for (t = 0; t < in.OperatingTheaters(); t++)
           surgeon_day_theater_count[s][d][t] = 0;
       }
    for (p = 0; p < in.Patients()+in.Occupants(); p++)
      if(p<in.Patients()){
       for(s=0;s<in.PatientLengthOfStay(p);s++)
        patient_shift_nurse[p][s]=-1;
      }
      else{
        for(s=0;s<in.OccupantLengthOfStay(p-in.Patients());s++)
          patient_shift_nurse[p][s]=-1;
      }
  UpdatewithOccupantsInfo();
}

void IHTP_Output::AssignPatient(int p, int ad, int r, int t)
{
  int d, s, s1, n, u;
  
  admission_day[p] = ad;
  room[p] = r;
  operating_room[p] = t;

  for (d = ad; d < min(in.Days(), ad + in.PatientLengthOfStay(p)); d++)
  {
    room_day_patient_list[r][d].push_back(p);
    if (in.PatientGender(p) == Gender::A)
       room_day_a_patients[r][d]++;
    else
       room_day_b_patients[r][d]++;
    for (s = d * in.ShiftsPerDay(); s < (d+1) * in.ShiftsPerDay(); s++ )
    {
      n = room_shift_nurse[r][s];
	    if (n != -1)
	    {// reminder that patient data is relative to the admission, not absolute (s1 is s shifted to the admission of p)
		    s1 = s - ad * in.ShiftsPerDay();
		    patient_shift_nurse[p][s1] = n;
        nurse_shift_load[n][s]+= in.PatientWorkloadProduced(p,s1);
	    }
    }
  }
  operatingtheater_day_patient_list[t][ad].push_back(p);
  operatingtheater_day_load[t][ad] += in.PatientSurgeryDuration(p);
  u = in.PatientSurgeon(p);
  surgeon_day_load[u][ad] += in.PatientSurgeryDuration(p);
  surgeon_day_theater_count[u][ad][t]++;
}

void IHTP_Output::AssignNurse(int n, int r, int s)
{
  int d, p, s1;
  unsigned i;
  if (!in.IsNurseWorkingInShift(n,s))
  {
    stringstream ss;
    ss << "Assigning a non-working nurse " << n << " to shift " << in.ShiftDescription(s);
    throw invalid_argument(ss.str());
  }
  room_shift_nurse[r][s] = n;
  nurse_shift_room_list[n][s].push_back(r);
  
  d = s/in.ShiftsPerDay();

  for (i = 0; i < room_day_patient_list[r][d].size(); i++)
  { // reminder that patient_shift_nurse is relative to the admission, not absolute (s1 is s shifted to the admission)
	  p = room_day_patient_list[r][d][i];
    if(p<in.Patients())
    {
	    s1 = s - admission_day[p] * in.ShiftsPerDay();
      nurse_shift_load[n][s] += in.PatientWorkloadProduced(p,s1);
    }
    else
    {
      s1 = s;
      nurse_shift_load[n][s] += in.OccupantWorkloadProduced(p-in.Patients(),s);
    }
	  patient_shift_nurse[p][s1] = n;
  }
}

void IHTP_Output::UpdatewithOccupantsInfo()
{
  int offset = in.Patients(), i, o, d, r;
  for(i = 0; i < in.Occupants(); i++)
  {
    o = i + offset;
    r = in.OccupantRoom(i);
    for(d = 0; d < in.OccupantLengthOfStay(i); d++)
    {
      room_day_patient_list[r][d].push_back(o);
      if (in.OccupantGender(i) == Gender::A)
        room_day_a_patients[r][d]++;
      else
        room_day_b_patients[r][d]++;
    }
  }
}

int IHTP_Output::OperatingTheaterOvertime() const
{
  int cost = 0, time;
  int p, t, d;
  unsigned i;
  for (t = 0; t < in.OperatingTheaters(); t++)
    for (d = 0; d < in.Days(); d++)
    {
      time = 0;
      for (i = 0; i < operatingtheater_day_patient_list[t][d].size(); i++)
      {
        p = operatingtheater_day_patient_list[t][d][i];
        time += in.PatientSurgeryDuration(p); 
      }
      if (time > in.OperatingTheaterAvailability(t,d))
	    { 
        cost += time - in.OperatingTheaterAvailability(t,d);
        if (VERBOSE)
          cout << "Operating theaters " << in.OperatingTheaterId(t) << " has " << time - in.OperatingTheaterAvailability(t,d) << " minutes of overtime on day " << d << endl;
	    }
    }
  return cost;
}

int IHTP_Output::SurgeonOvertime() const
{
  int cost = 0;
  int s, d;
  for (s = 0; s < in.Surgeons(); s++)
    for (d = 0; d < in.Days(); d++)
      if (surgeon_day_load[s][d] > in.SurgeonMaxSurgeryTime(s,d))
      {
        cost += surgeon_day_load[s][d] - in.SurgeonMaxSurgeryTime(s,d);
        if (VERBOSE)
          cout << "Surgeon " << in.SurgeonId(s) << " has " << surgeon_day_load[s][d] - in.SurgeonMaxSurgeryTime(s,d) << " minutes of overtime on day " << d << endl;
      }
  return cost;
}

int IHTP_Output::SurgeonTransfer() const
{
  int cost = 0, count;
  int s, d, t;
  for (s = 0; s < in.Surgeons(); s++)
    for (d = 0; d < in.Days(); d++)
    {
      count = 0;
      for (t = 0; t < in.OperatingTheaters(); t++)
        if (surgeon_day_theater_count[s][d][t] > 0)
          count++;
      if (count > 1)
      {
        cost += (count - 1);
        if (VERBOSE)
          cout << "Surgeon " << in.SurgeonId(s) << " operates in " << count << " distinct operating theaters" << endl;
      } 
    }
  return cost;
}

int IHTP_Output::MandatoryUnscheduledPatients() const
{
  int cost = 0;
  for (int p = 0; p < in.Patients(); p++)
  {
    if (admission_day[p] == -1 && in.PatientMandatory(p))
    {
      cost++;
      if (VERBOSE)
        cout << "Mandatory patient " << in.PatientId(p) << " is unscheduled" << endl;
    } 
  }
  return cost;
}

int IHTP_Output::ElectiveUnscheduledPatients() const
{
  int cost = 0;
  for (int p = 0; p < in.Patients(); p++)
  {
    if (admission_day[p] == -1 && !in.PatientMandatory(p))
    {
      cost++;    
      if (VERBOSE)
        cout << "Elective patient " << in.PatientId(p) << " is unscheduled" << endl;
    }
  }
  return cost;
}

int IHTP_Output::PatientDelay() const
{
  int cost = 0;

  for (int p = 0; p < in.Patients(); p++)
  {
    if (admission_day[p] != -1 && admission_day[p] > in.PatientSurgeryReleaseDay(p))
    {
      cost += admission_day[p] - in.PatientSurgeryReleaseDay(p);  
      if (VERBOSE)
          cout << "Patient " << in.PatientId(p) << " has been delayed for " << admission_day[p] - in.PatientSurgeryReleaseDay(p) << " days" << endl;
    }  
  }
  return cost;
}

int IHTP_Output::OpenOperatingTheater() const
{
  int cost = 0;
  for (int t = 0; t < in.OperatingTheaters(); t++)
    for (int d = 0; d < in.Days(); d++)
       if (operatingtheater_day_patient_list[t][d].size() > 0)
       {
          cost++;
          if (VERBOSE)
            cout << "Operating theater " << in.OperatingTheaterId(t) << " is open on day " << d << endl;
       }
  return cost;
}

int IHTP_Output::RoomCapacity() const
{
  int cost = 0;
  for (int r = 0; r < in.Rooms(); r++)
    for (int d = 0; d < in.Days(); d++)
       if (room_day_patient_list[r][d].size() > static_cast<unsigned>(in.RoomCapacity(r)))
       {
          cost += room_day_patient_list[r][d].size() - in.RoomCapacity(r);
          if (VERBOSE)
            cout << "Room " << in.RoomId(r) << " is overloaded by " << room_day_patient_list[r][d].size() - in.RoomCapacity(r) << " on day " << d << endl;
         }
  return cost;
}

int IHTP_Output::RoomGenderMix() const
{
  int cost = 0;
  int r, d;
  for (r = 0; r < in.Rooms(); r++)
    for (d = 0; d < in.Days(); d++)
    {
      cost += min(room_day_a_patients[r][d], room_day_b_patients[r][d]);
      if (VERBOSE)
        if (room_day_a_patients[r][d] > 0 && room_day_b_patients[r][d] > 0)
          cout << "Room " << in.RoomId(r) << " is gender-mixed " << room_day_a_patients[r][d] << "/" << room_day_b_patients[r][d] << " on day " << d << endl;
    }
  return cost;
}

int IHTP_Output::PatientRoomCompatibility() const
{
  int cost = 0;
  for (int p = 0; p < in.Patients(); p++)
    if (room[p] != -1 && in.IncompatibleRoom(p,room[p]))
    {
      cost++;
      if (VERBOSE)
        cout << "Room " << in.RoomId(room[p]) << " is incompatible with patient " << in.PatientId(p) << endl;
    }
  return cost;
} 

int IHTP_Output::RoomAgeMix() const
{ // computes max age_group difference between patients in the room in the day
  int cost = 0;
  int r, d, g, p, min, max;
  unsigned i;
  for (r = 0; r < in.Rooms(); r++)
	  for (d = 0; d < in.Days(); d++)
	  {
		  if (room_day_patient_list[r][d].size() > 0)
		  {
        p = room_day_patient_list[r][d][0];
			  if(p<in.Patients())
          min = in.PatientAgeGroup(room_day_patient_list[r][d][0]);
        else
          min = in.OccupantAgeGroup(room_day_patient_list[r][d][0]-in.Patients());
			  max = min;
		    for (i = 1; i < room_day_patient_list[r][d].size(); i++)
			  {
          p = room_day_patient_list[r][d][i];
          if(p<in.Patients())
			      g = in.PatientAgeGroup(room_day_patient_list[r][d][i]);
          else
            g = in.OccupantAgeGroup(room_day_patient_list[r][d][i]-in.Patients());
			    if (g < min)
				    min = g;
			    else if (g > max)
				    max = g;
			    }
			  if (max > min)
        {
          cost += max - min;
          if (VERBOSE)
             cout << "Room " << in.RoomId(r) << " is age-mixed " << min << "/" << max << " on day " << d << endl;
        }
		}
	}
  return cost;
}

int IHTP_Output::RoomSkillLevel() const
{
  int cost = 0;
  int r, s, s1, n, d, p;
  unsigned i;
  for (r = 0; r < in.Rooms(); r++)
    for (s = 0; s < in.Shifts(); s++)
    {
      d = s / in.ShiftsPerDay();
      n = room_shift_nurse[r][s]; // nurse assigned to the room in that shift
      for (i = 0; i < room_day_patient_list[r][d].size(); i++)
      {
        p = room_day_patient_list[r][d][i];
        if(p<in.Patients()){
          s1 = s - admission_day[p] * in.ShiftsPerDay(); // translation of the shift w.r.t. the admission of the patient
          if (in.PatientSkillLevelRequired(p,s1) > in.NurseSkillLevel(n))
          {
            cost += in.PatientSkillLevelRequired(p,s1) - in.NurseSkillLevel(n);
            if (VERBOSE)
              cout << "Nurse " << in.NurseId(n) << " is underqualified for patient " << 
              in.PatientId(p) << " in room " << in.RoomId(r) << " in shift " << in.ShiftDescription(s) << endl;
          }
        }
        else if (in.OccupantSkillLevelRequired(p-in.Patients(),s) > in.NurseSkillLevel(n))
          {
            cost += in.OccupantSkillLevelRequired(p-in.Patients(),s) - in.NurseSkillLevel(n);
            if (VERBOSE)
              cout << "Nurse " << in.NurseId(n) << " is underqualified for occupant " << 
              in.OccupantId(p-in.Patients()) << " in room " << in.RoomId(r) << " in shift " << in.ShiftDescription(s) << endl;
          }
        }
    }
  return cost;
}

int IHTP_Output::AdmissionDay() const
{
  int cost = 0;
  for (int p = 0; p < in.Patients(); p++)
    if (admission_day[p] != -1 && 
        (admission_day[p] < in.PatientSurgeryReleaseDay(p)
         || (admission_day[p] > in.PatientLastPossibleDay(p))))
    {
      cost++;
      if (VERBOSE)
      {
        if (admission_day[p] < in.PatientSurgeryReleaseDay(p))
          cout << "Patient " << in.PatientId(p) << " is admitted at " 
               << admission_day[p] << " before the release date " << in.PatientSurgeryReleaseDay(p) << endl;
        else
           cout << "Patient " << in.PatientId(p) << " is admitted at " 
               << admission_day[p] << " after the last possible date " << in.PatientLastPossibleDay(p) << endl;
      }
   }
  return cost;
}

int IHTP_Output::NursePresence() const
{
  int cost = 0;
  int r, s, n;
  for (r = 0; r < in.Rooms(); r++)
    for (s = 0; s < in.Shifts(); s++)
    {
      n = room_shift_nurse[r][s]; 
      if (n != -1 && !in.IsNurseWorkingInShift(n,s))
      {
        cost++;
        if (VERBOSE)
             cout << "Nurse " << in.NurseId(n) << " assigned in a non-working shift: " << s/in.ShiftsPerDay() << "@" << in.ShiftName(s%in.ShiftsPerDay()) << endl;
      }
    }
  return cost;
}

int IHTP_Output::UncoveredRoom() const
{
  int cost = 0;
  int r, s;
  for (r = 0; r < in.Rooms(); r++)
    for (s = 0; s < in.Shifts(); s++)
      if (room_shift_nurse[r][s] == -1 && room_day_patient_list[r][s/in.ShiftsPerDay()].size()>0) 
      {
        cost++;
        if (VERBOSE)
             cout << "Room " << in.RoomId(r) << " is uncovered in shift "  << in.ShiftDescription(s) <<endl;
      }
  return cost;
}

int IHTP_Output::ExcessiveNurseWorkload() const
{
  int cost = 0;
  int n, r, s, s1, d, p, load, k;
  unsigned i, j;
  for (n = 0; n < in.Nurses(); n++)
    for (k = 0; k < in.NurseWorkingShifts(n); k++)
    {
      s = in.NurseWorkingShift(n,k);
      d = s / in.ShiftsPerDay();
      load = 0;
      for (i = 0; i < nurse_shift_room_list[n][s].size(); i++)
      {
        r = nurse_shift_room_list[n][s][i];
        for (j = 0; j < room_day_patient_list[r][d].size(); j++)
        {
          p = room_day_patient_list[r][d][j];
          if(p<in.Patients()){
            s1 = s - admission_day[p] * in.ShiftsPerDay(); 
            load += in.PatientWorkloadProduced(p,s1);
          }
          else
            load += in.OccupantWorkloadProduced(p-in.Patients(),s);
        }
      }
      if (load > in.NurseMaxLoad(n,s))
      {
        cost += load - in.NurseMaxLoad(n,s);
        if (VERBOSE)
          cout << "Excessive workload  " << load - in.NurseMaxLoad(n,s) << " for nurse " <<
          in.NurseId(n) << " in shift " << in.ShiftDescription(s) << endl;

      }
    }
  return cost;
}

int IHTP_Output::ContinuityOfCare() const
{ // number of distinct nurses per patient
  int cost = 0, count;
  for (int o = 0; o < in.Occupants(); o++)
  {
    count = CountOccupantNurses(o);
      if (count > 0)
      {
        cost += count;
        if (VERBOSE)
          cout << count << " distinct nurses for occupant " << in.OccupantId(o) << endl; 
      }
  }
  for (int p = 0; p < in.Patients(); p++)
  {
    if (admission_day[p] != -1)
    {
      count = CountDistinctNurses(p);
      if (count > 0)
      {
        cost += count;
        if (VERBOSE)
          cout << count << " distinct nurses for patient " << in.PatientId(p) << endl; 
      }
    }
  }
  return cost;
}

int IHTP_Output::CountDistinctNurses(int p) const
{
	int count = 0, n, s, st = patient_shift_nurse[p].size();
	vector<bool> tag(in.Nurses(), false);
	for (s = 0; s < min(st,(in.Days()-admission_day[p])*in.ShiftsPerDay()); s++)
	{
		n = patient_shift_nurse[p][s];
		if (n != -1 && !tag[n])
		{
			tag[n] = true;
			count++;
		}
	}
	return count;
}

int IHTP_Output::CountOccupantNurses(int o) const
{
  int count = 0, n, s;
	vector<bool> tag(in.Nurses(), false);
	for (s = 0; s < in.OccupantLengthOfStay(o)*in.ShiftsPerDay(); s++)
	{
		n = patient_shift_nurse[o+in.Patients()][s];
		if (n != -1 && !tag[n])
		{
			tag[n] = true;
			count++;
		}
	}
  return count;
}


void IHTP_Output::PrintCosts() const
{
  int total_violations = 0, total_cost = 0;
  unsigned i;

  vector<pair<string,int>> violations{
	  {"RoomGenderMix", RoomGenderMix()},
	  {"PatientRoomCompatibility", PatientRoomCompatibility()},
	  {"SurgeonOvertime", SurgeonOvertime()},
	  {"OperatingTheaterOvertime", OperatingTheaterOvertime()},
	  {"MandatoryUnscheduledPatients", MandatoryUnscheduledPatients()},
	  {"AdmissionDay", AdmissionDay()},
	  {"RoomCapacity", RoomCapacity()},
	  {"NursePresence", NursePresence()},
	  {"UncoveredRoom", UncoveredRoom()}};

  vector<pair<string,int>> costs{
	  {"RoomAgeMix", RoomAgeMix()},
	  {"RoomSkillLevel", RoomSkillLevel()},
	  {"ContinuityOfCare", ContinuityOfCare()},
	  {"ExcessiveNurseWorkload", ExcessiveNurseWorkload()},
	  {"OpenOperatingTheater", OpenOperatingTheater()},
    {"SurgeonTransfer", SurgeonTransfer()},
	  {"PatientDelay", PatientDelay()},
	  {"ElectiveUnscheduledPatients", ElectiveUnscheduledPatients()}};
   

  cout << "VIOLATIONS: " << endl;
  for (i = 0; i < violations.size(); i++)
  {
      cout.setf(ios::left, ios::adjustfield);      
      cout << setfill('.') << setw(30) << violations[i].first; 
      cout.setf(ios::right, ios::adjustfield);      
      cout << setfill('.') << setw(5) << violations[i].second << endl;
	    total_violations += violations[i].second;
  }
  cout << "Total violations = " << total_violations << endl;

  cout << endl;
  cout << "COSTS (weight X cost): " << endl;
  for (i = 0; i < costs.size(); i++)
  {
    cout.setf(ios::left, ios::adjustfield);      
    cout << setfill('.') << setw(30) << costs[i].first;
    cout.setf(ios::right, ios::adjustfield);      
    cout << setfill('.') << setw(10) << costs[i].second * in.Weight(i);
	  cout << " (" << setfill(' ') << setw(3) << in.Weight(i) << " X " << setw(3) << costs[i].second << ")" << endl; 
    total_cost += costs[i].second * in.Weight(i);
  }
  cout << "Total cost = " << total_cost << endl;
}

int main(int argc, const char *argv[])
{
  if (argc != 3 && argc != 4)
  {
    cerr << "Usage: " << argv[0] << " <instance_file> <solution_file> [verbose]" << endl;
    exit(1);
  }
  string instance_file_name = argv[1];
  string solution_file_name = argv[2];
  bool verbose = (argc == 4); // any word passed as fourth argument is interpreted as "verbose"

  IHTP_Input in(instance_file_name);
  IHTP_Output out(in, solution_file_name, verbose); 
  out.PrintCosts();
  return 0;
}
