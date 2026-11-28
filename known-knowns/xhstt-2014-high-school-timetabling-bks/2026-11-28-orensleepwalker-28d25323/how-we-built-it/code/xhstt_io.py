"""
Shared XHSTT I/O, Archive XML Writer & Independent Disk Round-Trip Verifier
(scans/2026-11-27-xhstt-charlie/xhstt_io.py)
"""
import copy
import hashlib
import os
import sys
import time
import xml.etree.ElementTree as ET

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANS_DIR = os.path.dirname(CHARLIE_DIR)
SCOUT_DIR = os.path.join(SCANS_DIR, "2026-11-27-xhstt-scout")
RAW_INST_DIR = os.path.join(SCOUT_DIR, "raw", "inst")
WINS_DIR = os.path.join(CHARLIE_DIR, "wins")
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")

sys.path.insert(0, os.path.join(SCOUT_DIR, "code"))
import xhstt_eval as X  # noqa: E402

# Strict win thresholds (must beat BOTH overview and dataset page!)
TARGETS = {
    "AU-BG-98": {"rec": (0, 128), "win_max": (0, 125)},
    "DK-HG-12": {"rec": (12, 2330), "win_max": (12, 2329)},  # any (<=11, *) also < (12, 2329)!
    "DK-VG-09": {"rec": (2, 2323), "win_max": (2, 2322)},
}


def load_target(tid: str):
    path = os.path.join(RAW_INST_DIR, f"{tid}.xml")
    root = ET.parse(path).getroot()
    inst_el = next(i for i in root.find("Instances") if i.attrib["Id"] == tid)
    inst = X.Instance(inst_el)
    sols = [
        (X.evaluate(inst, s)[:2], s)
        for sg in root.find("SolutionGroups")
        for s in sg.findall("Solution")
        if s.attrib.get("Reference") == tid
    ]
    start_val, best_sol = min(sols, key=lambda z: z[0])
    assert start_val == TARGETS[tid]["rec"], f"{tid}: expected {TARGETS[tid]['rec']}, got {start_val}"
    se = X.read_solution(inst, best_sol)
    return root, inst_el, inst, se, start_val


def is_strict_win(tid: str, val: tuple) -> bool:
    return tuple(val) <= TARGETS[tid]["win_max"]


def write_and_verify_xml(inst_el, inst, sev, out_path: str, desc: str = "CP-SAT LNS"):
    sol = ET.Element("Solution", Reference=inst.id)
    evs = ET.SubElement(sol, "Events")
    for eid in inst.eorder:
        for s in sev[eid]:
            e = ET.SubElement(evs, "Event", Reference=eid)
            ET.SubElement(e, "Duration").text = str(s["dur"])
            if s["t"] is not None:
                ET.SubElement(e, "Time", Reference=inst.times[s["t"]])
            rs = ET.SubElement(e, "Resources")
            for k, er in enumerate(inst.events[eid]["ers"]):
                if s["res"][k] is not None and er["role"] is not None:
                    r = ET.SubElement(rs, "Resource", Reference=s["res"][k])
                    ET.SubElement(r, "Role").text = er["role"]

    arch = ET.Element("HighSchoolTimetableArchive", Id=f"V3R1T4S_{inst.id}")
    ins = ET.SubElement(arch, "Instances")
    ins.append(copy.deepcopy(inst_el))
    sgs = ET.SubElement(arch, "SolutionGroups")
    sg = ET.SubElement(sgs, "SolutionGroup", Id="V3R1T4S_charlie")
    md = ET.SubElement(sg, "MetaData")
    for tag, v in (("Contributor", "V3R1T4S"), ("Date", time.strftime("%Y-%m-%d")), ("Description", desc)):
        ET.SubElement(md, tag).text = v
    sg.append(sol)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    ET.ElementTree(arch).write(out_path, encoding="UTF-8", xml_declaration=True)

    # Round-trip re-parse & independent evaluation from disk!
    rt = ET.parse(out_path).getroot()
    inst_chk = X.Instance(rt.find("Instances")[0])
    sol_chk = rt.find("SolutionGroups")[0].find("Solution")
    h, o, per = X.evaluate(inst_chk, sol_chk)
    sha = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    return (h, o), per, sha
