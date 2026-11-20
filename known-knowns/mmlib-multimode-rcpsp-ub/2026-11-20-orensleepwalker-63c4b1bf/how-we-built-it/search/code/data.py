"""Dataset loader, strict checker gate, and win recorder for MMLIB+ Phase B."""
import json
import os
import sys
import time
import zipfile
import numpy as np

PHASEB_DIR = os.path.dirname(os.path.abspath(__file__))
SOLVER_CODE = os.path.abspath(os.path.join(PHASEB_DIR, "..", "code"))
RAW_DIR = os.path.abspath(os.path.join(PHASEB_DIR, "..", "..", "2026-11-19-mmlib-scout", "raw"))
WINS_DIR = os.path.join(PHASEB_DIR, "wins")

if SOLVER_CODE not in sys.path:
    sys.path.insert(0, SOLVER_CODE)

import mm  # noqa: E402
import engine  # noqa: E402


class MMLibDataset:
    def __init__(self, raw_dir: str = RAW_DIR):
        self.raw_dir = raw_dir
        csv_path = os.path.join(raw_dir, "MMplus_2.csv")
        lines = open(csv_path, encoding="utf-8-sig", errors="replace").read().splitlines()
        self.headers = lines[4].split(";")
        self.rows = {}
        for line in lines[5:]:
            parts = line.split(";")
            if parts and parts[0].isdigit():
                self.rows[int(parts[0])] = dict(zip(self.headers, parts))

        self.bks = {}
        bks_path = os.path.join(raw_dir, "MMplus_2_BKS.csv")
        for line in open(bks_path, encoding="utf-8-sig"):
            parts = line.strip().split(";")
            if parts and parts[0].isdigit():
                vals = [int(x) for x in parts[4:] if x]
                if vals:
                    self.bks[int(parts[0])] = vals

        self._zip = zipfile.ZipFile(os.path.join(raw_dir, "MMplus.zip"))

    def open_ids(self):
        return [i for i, r in self.rows.items() if int(r["LB value"]) < int(r["UB value"])]

    def meta(self, inst_id: int) -> dict:
        r = self.rows[inst_id]
        return {
            "id": inst_id,
            "file": r["Ref1"],
            "lb": int(r["LB value"]),
            "ub": int(r["UB value"]),
            "ub_ref": r.get("UB ref", ""),
            "act": int(r["# Act"]),
            "modes": int(float(r["# Modes"].replace(",", "."))),
            "rr": int(r["# RR"]),
            "nr": int(r["# NR"]),
            "has_bks": inst_id in self.bks,
        }

    def load_inst(self, inst_id: int):
        I = mm.read(self._zip.read("MMplus/" + self.rows[inst_id]["Ref1"]).decode())
        X = engine.Inst(I)
        return I, X

    def load_bks_schedule(self, inst_id: int):
        """Return (modes_1based_np, starts_np) or None if no posted schedule."""
        v = self.bks.get(inst_id)
        if not v:
            return None
        k = len(v) // 2 - 1
        modes = np.array([1] + v[:k] + [1], dtype=np.int64)
        starts = np.array(v[k:], dtype=np.int64)
        return modes, starts


def verify_and_save_win(
    ds: MMLibDataset,
    inst_id: int,
    I: dict,
    modes,
    starts,
    warm_start: bool,
    seed: int,
    method: str,
    runtime_sec: float,
    wins_dir: str = WINS_DIR,
):
    """Strictly verify via code/mm.py check() and save JSON if strictly < UB."""
    m_list = [int(x) for x in modes]
    s_list = [int(x) for x in starts]
    res = mm.check(I, m_list, s_list)
    if not res.startswith("VALID makespan "):
        return False, None, f"CHECKER_FAIL: {res}"
    mk = int(res.split()[-1])
    info = ds.meta(inst_id)
    ub = info["ub"]
    if mk >= ub:
        return False, mk, f"NOT_IMPROVED: mk={mk} >= ub={ub}"

    os.makedirs(wins_dir, exist_ok=True)
    # Check if we already have an equal-or-better win saved
    rec = {
        "id": inst_id,
        "file": info["file"],
        "lb": info["lb"],
        "old_ub": ub,
        "new_mk": mk,
        "gain": ub - mk,
        "ub_ref": info["ub_ref"],
        "act": info["act"],
        "modes_count": info["modes"],
        "rr": info["rr"],
        "nr": info["nr"],
        "warm_start": bool(warm_start),
        "seed": int(seed),
        "method": method,
        "runtime_sec": round(float(runtime_sec), 2),
        "checker": res,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "modes": m_list,
        "starts": s_list,
    }
    out_path = os.path.join(wins_dir, f"win_{inst_id:04d}_mk{mk}_ub{ub}.json")
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(rec, f, indent=2)
    os.replace(tmp_path, out_path)
    return True, mk, out_path
