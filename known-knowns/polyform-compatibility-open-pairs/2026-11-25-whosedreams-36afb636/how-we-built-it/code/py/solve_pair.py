"""Solve one heptiamond pair for increasing k."""
from __future__ import annotations
import json
import time
from pathlib import Path
from .grid import connected, holeless, figure_ascii
from .sat_compat import build_joint_cnf, run_cadical, decode_solution, verify_drat, board_for_k
from .shapes import placements_for
from .tile_exact import can_tile


def solve_pair(
    letter_p: str,
    letter_q: str,
    k_min: int = 2,
    k_max: int = 8,
    table: str = "unrestricted",
    work_dir: Path | None = None,
    timeout_per_k: int = 120,
    prove_unsat: bool = True,
) -> dict:
    letter_p, letter_q = sorted([letter_p, letter_q])
    work_dir = Path(work_dir or Path("work") / f"{letter_p}{letter_q}")
    work_dir.mkdir(parents=True, exist_ok=True)
    require_holeless = table == "holeless"
    results = []
    best = None

    for k in range(k_min, k_max + 1):
        t0 = time.time()
        wd = work_dir / f"k{k}"
        board = board_for_k(k)
        cnf, meta = build_joint_cnf(letter_p, letter_q, k, board=board)
        # first try SAT without proof
        got = run_cadical(cnf, wd, prove=False, timeout=timeout_per_k)
        entry = {
            "k": k,
            "status": got["status"],
            "board_rows": meta["nrows"],
            "board_cols": meta["ncols"],
            "n_placements_p": len(meta["P"]),
            "n_placements_q": len(meta["Q"]),
            "seconds": round(time.time() - t0, 3),
        }
        if got["status"] == "sat":
            # may need to enumerate until connected (+ holeless) model found
            sol = decode_solution(meta, got["model"])
            fig = [tuple(c) for c in sol["figure"]]
            ok = connected(fig) and (not require_holeless or holeless(fig))
            if not ok:
                # block this F and re-solve a few times
                found = None
                for trial in range(12):
                    # add blocking clause: not exactly this F
                    from .cnfutil import CNF
                    # rebuild with blocking of prior figures — quick approach: post-check only
                    # Re-run cadical with assumptions by rewriting: forbid these f_vars pattern
                    block = []
                    for c, v in meta["f_vars"].items():
                        if c in fig:
                            block.append(-v)
                        else:
                            block.append(v)
                    cnf.add(*block)
                    cnf.write(wd / "problem.cnf")
                    got = run_cadical(cnf, wd / f"retry{trial}", prove=False, timeout=timeout_per_k)
                    if got["status"] != "sat":
                        entry["status"] = got["status"]
                        entry["note"] = "no connected model after retries"
                        break
                    sol = decode_solution(meta, got["model"])
                    fig = [tuple(c) for c in sol["figure"]]
                    if connected(fig) and (not require_holeless or holeless(fig)):
                        found = sol
                        break
                if found is None and entry.get("status") == "sat":
                    entry["status"] = "sat_disconnected_only"
                    entry["seconds"] = round(time.time() - t0, 3)
                    results.append(entry)
                    continue
                if found is not None:
                    sol = found
                    ok = True
            if ok:
                sol["table"] = table
                sol["ascii"] = figure_ascii(fig)
                # independent exact-cover recheck
                from .check_independent import check_solution
                chk = check_solution(sol, table)
                sol["checker"] = chk
                outp = wd / "solution.json"
                outp.write_text(json.dumps(sol, indent=2))
                entry["status"] = "sat"
                entry["solution"] = str(outp)
                entry["checker_ok"] = chk["ok"]
                entry["seconds"] = round(time.time() - t0, 3)
                results.append(entry)
                best = sol
                break
        elif got["status"] == "unsat" and prove_unsat:
            # re-run with proof
            got2 = run_cadical(cnf, wd / "prove", prove=True, timeout=timeout_per_k)
            entry["status"] = "unsat"
            if got2["status"] == "unsat" and got2["proof"]:
                entry["proof"] = got2["proof"]
                entry["proof_verified"] = verify_drat(Path(got2["cnf"]), Path(got2["proof"]))
            entry["seconds"] = round(time.time() - t0, 3)
            entry["p3_label"] = (
                f"bounded UNSAT: no figure with k={k} tiles "
                f"(area {7*k}) inside a {meta['nrows']}x{meta['ncols']} board "
                f"(disconnected figures also forbidden by model coverage); "
                f"table={table}"
            )
            results.append(entry)
        else:
            entry["seconds"] = round(time.time() - t0, 3)
            results.append(entry)
            if got["status"] == "timeout":
                break

    summary = {
        "pair": f"{letter_p}-{letter_q}",
        "table": table,
        "k_min": k_min,
        "k_max": k_max,
        "found": best is not None,
        "solution": best,
        "per_k": results,
    }
    (work_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
