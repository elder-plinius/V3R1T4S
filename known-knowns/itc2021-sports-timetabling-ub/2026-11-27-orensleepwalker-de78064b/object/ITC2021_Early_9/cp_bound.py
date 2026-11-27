"""Build or replay the projected Early 9 CP-SAT lower bound."""
import argparse
from pathlib import Path

from ortools.sat.python import cp_model

from certificate import INSTANCE, bounds


def build(instance):
    surviving = bounds(instance)
    cases = sorted({(len(slots), int(any(r % 2 for r in slots))) for slots, _ in surviving})
    cases.append((4, 0))  # Represents all possibilities with at least four Team 2 repeats.
    model = cp_model.CpModel()
    team2 = model.new_int_var(3, 4, 'team_2_projected_repeats')
    odd = model.new_bool_var('team_2_uses_odd_repeat_when_at_three')
    total = model.new_int_var(0, 18 * 33, 'league_repeats')
    cost = model.new_int_var(0, 18 * 33 * 10, 'break_penalty')
    model.add_allowed_assignments((team2, odd), cases)
    model.add(total >= 15 + team2)
    model.add(total >= 19).only_enforce_if(odd)
    model.add_modulo_equality(0, total, 2)
    model.add_max_equality(cost, (0, 10 * (total - 16)))
    model.minimize(cost)
    return model


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model', type=Path, required=True)
    ap.add_argument('--instance', type=Path, default=INSTANCE)
    ap.add_argument('--generate', action='store_true')
    args = ap.parse_args()
    if args.generate:
        model = build(args.instance)
        assert model.export_to_file(str(args.model))
    else:
        model = cp_model.CpModel()
        assert model.proto.parse_text_format(args.model.read_text())
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 20261125
    solver.parameters.max_time_in_seconds = 15
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    print('Status:', solver.status_name(status))
    print('Best bound:', solver.best_objective_bound)
    if status != cp_model.OPTIMAL or solver.best_objective_bound != 40:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
