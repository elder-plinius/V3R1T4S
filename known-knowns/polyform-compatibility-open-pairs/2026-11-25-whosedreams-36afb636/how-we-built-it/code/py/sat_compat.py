"""Joint SAT model for heptiamond compatibility at tile-count k."""
from __future__ import annotations
import math
import subprocess
from pathlib import Path
from .cnfutil import CNF
from .grid import Cell, make_board, connected, holeless, neighbors
from .shapes import placements_for

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"


def board_for_k(k: int, margin: int = 2) -> list[Cell]:
    area = 7 * k
    side = max(6, int(math.ceil(2.0 * math.sqrt(area))) + margin)
    return make_board(side, side + 2)


def build_joint_cnf(
    letter_p: str,
    letter_q: str,
    k: int,
    board: list[Cell] | None = None,
) -> tuple[CNF, dict]:
    if board is None:
        board = board_for_k(k)
    P = placements_for(letter_p, board)
    Q = placements_for(letter_q, board)
    cnf = CNF()
    f_vars = {c: cnf.new_var() for c in board}
    p_vars = [cnf.new_var() for _ in P]
    q_vars = [cnf.new_var() for _ in Q]

    cnf.exactly_k(list(f_vars.values()), 7 * k)
    if not p_vars or not q_vars:
        cnf.add()
    else:
        cnf.exactly_k(p_vars, k)
        cnf.exactly_k(q_vars, k)

    cover_p = {c: [] for c in board}
    for i, pl in enumerate(P):
        for c in pl:
            cover_p[c].append(p_vars[i])
    cover_q = {c: [] for c in board}
    for j, pl in enumerate(Q):
        for c in pl:
            cover_q[c].append(q_vars[j])

    for c in board:
        fv = f_vars[c]
        ps = cover_p[c]
        qs = cover_q[c]
        for x in ps:
            cnf.add(fv, -x)
        if not ps:
            cnf.add(-fv)
        else:
            cnf.add(-fv, *ps)
            for a in range(len(ps)):
                for b in range(a + 1, len(ps)):
                    cnf.add(-ps[a], -ps[b])
        for x in qs:
            cnf.add(fv, -x)
        if not qs:
            cnf.add(-fv)
        else:
            cnf.add(-fv, *qs)
            for a in range(len(qs)):
                for b in range(a + 1, len(qs)):
                    cnf.add(-qs[a], -qs[b])

    meta = {
        "board": board,
        "P": P,
        "Q": Q,
        "f_vars": f_vars,
        "p_vars": p_vars,
        "q_vars": q_vars,
        "k": k,
        "letter_p": letter_p,
        "letter_q": letter_q,
        "nrows": max(r for r, c in board) + 1,
        "ncols": max(c for r, c in board) + 1,
    }
    return cnf, meta


def run_cadical(cnf: CNF, work_dir: Path, prove: bool = False, timeout: int | None = 120):
    work_dir.mkdir(parents=True, exist_ok=True)
    cnf_path = work_dir / "problem.cnf"
    cnf.write(cnf_path)
    cadical = BIN / "cadical"
    cmd = [str(cadical), str(cnf_path)]
    proof = None
    if prove:
        proof = work_dir / "proof.drat"
        cmd.append(str(proof))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "model": None, "proof": None, "cnf": str(cnf_path)}
    out = r.stdout + r.stderr
    if "s SATISFIABLE" in out:
        model = set()
        for line in out.splitlines():
            if line.startswith("v "):
                for tok in line.split()[1:]:
                    if tok == "0":
                        continue
                    v = int(tok)
                    if v > 0:
                        model.add(v)
        return {"status": "sat", "model": model, "proof": None, "cnf": str(cnf_path), "log": out}
    if "s UNSATISFIABLE" in out:
        return {
            "status": "unsat",
            "model": None,
            "proof": str(proof) if prove else None,
            "cnf": str(cnf_path),
            "log": out,
        }
    return {"status": "error", "model": None, "proof": None, "cnf": str(cnf_path), "log": out}


def decode_solution(meta: dict, model: set[int]) -> dict:
    f_cells = [c for c, v in meta["f_vars"].items() if v in model]
    p_pls = [meta["P"][i] for i, v in enumerate(meta["p_vars"]) if v in model]
    q_pls = [meta["Q"][j] for j, v in enumerate(meta["q_vars"]) if v in model]
    return {
        "figure": [list(c) for c in f_cells],
        "tiling_p": [[list(c) for c in pl] for pl in p_pls],
        "tiling_q": [[list(c) for c in pl] for pl in q_pls],
        "k": meta["k"],
        "letter_p": meta["letter_p"],
        "letter_q": meta["letter_q"],
        "board_rows": meta["nrows"],
        "board_cols": meta["ncols"],
    }


def verify_drat(cnf_path: Path, proof_path: Path) -> bool:
    drat = BIN / "drat-trim"
    r = subprocess.run(
        [str(drat), str(cnf_path), str(proof_path)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    return "s VERIFIED" in (r.stdout + r.stderr)
