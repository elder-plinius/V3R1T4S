"""Build and replay the two-team CP-SAT relaxation for Early 14."""
import argparse
from pathlib import Path

from ortools.sat.python import cp_model

from certificate import ROUNDS, load, numbers
import certificate


def build():
    cp = cp_model.CpModel()
    score = []
    for team, (required_away, rules) in load().items():
        home = [cp.new_bool_var(f"home_{team}_{r}") for r in ROUNDS]
        cp.add(sum(home) == 19)
        cp.add(home[required_away] == 0)
        breaks = []
        for r in ROUNDS[1:]:
            repeat = cp.new_bool_var(f"repeat_{team}_{r}")
            cp.add(home[r - 1] == home[r]).only_enforce_if(repeat)
            cp.add(home[r - 1] != home[r]).only_enforce_if(~repeat)
            breaks.append(repeat)
        cp.add(sum(breaks) <= 1)
        for i, rule in enumerate(rules):
            slots = numbers(rule, "slots")
            uses = sum(home[r] if rule.get("mode") == "H" else 1 - home[r] for r in slots)
            lo, hi, weight = (int(rule.attrib[k]) for k in ("min", "max", "penalty"))
            excess = cp.new_int_var(0, len(slots), f"excess_{team}_{i}")
            cp.add_max_equality(excess, (0, lo - uses, uses - hi))
            score.append(weight * excess)
    cp.minimize(sum(score))
    return cp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--instance", type=Path)
    args = parser.parse_args()
    if args.generate:
        certificate.INSTANCE = args.instance
        cp = build()
        if not cp.export_to_file(str(args.model)):
            raise RuntimeError(f"Cannot export {args.model}")
    else:
        cp = cp_model.CpModel()
        if not cp.proto.parse_text_format(args.model.read_text()):
            raise ValueError(f"Cannot read {args.model}")
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 20261124
    solver.parameters.max_time_in_seconds = 15
    solver.parameters.log_search_progress = True
    status = solver.solve(cp)
    print("Status", solver.status_name(status))
    print("Best bound", solver.best_objective_bound)
    if status != cp_model.OPTIMAL or solver.best_objective_bound != 4:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
