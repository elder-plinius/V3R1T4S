"""Enumerate the hierarchy using the independent loss engine and the stopping thresholds."""
import argparse
import gzip
import json
from itertools import product

from ladder import Engine, HERE, SPECS
from pinned import Pinned, residues


def mixed(a, b, c):
    representatives = {}
    for r in range(45):
        if r % 3 and r % 5 and r % 9 != 1 and r % 15 != a:
            signature = (r % 3, r % 9 == b % 9, r % 5 == a, r % 5 == c)
            representatives.setdefault(signature, r)
    for r, d, k in product(representatives.values(), (1, 2), range(1, 5)):
        if (d, k) != (a, a):
            for j, hit in ((1, 0), (2, 0), (3, 0), (4, 0), (k, 1)):
                yield (a, b, c, r, j, d, k, hit, -1)


def assemble(engine, save):
    pending = []

    def attempt(phase, key):
        reserve, losses = engine.eval(phase, key)
        if reserve - sum(losses) < engine.threshold:
            return False
        save(phase, key, reserve, losses)
        return True

    for a, b, c in product((1, 2), (2, 4), (1, 2)):
        roots = [(a, b, c, -1, j, 0, 0, 0, -1) for j in range(1, 5)]
        for phase in (("basic", "basic75") if b == 2 else ("basic",)):
            scores = [engine.eval(phase, k) for k in roots]
            if all(reserve - sum(losses) >= engine.threshold for reserve, losses in scores):
                for key, (reserve, losses) in zip(roots, scores):
                    save(phase, key, reserve, losses)
                break
        else:
            for state in mixed(a, b, c):
                if attempt("mixed", state):
                    continue
                for pad in residues(a, "fix4"):
                    key = state + pad
                    if attempt("coarse", key) or attempt("spatial", key):
                        continue
                    for z in range(27):
                        if z % 3 and z % 9 != 1 and z != b:
                            leaf = state[:-1] + (z,) + pad
                            if not attempt("pure3", leaf):
                                pending.append(leaf)
    return pending


def run(name, phase):
    engine = Engine(name)
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    pending_file = out / f"{name}.pending.json"
    with gzip.open(out / f"{name}.{phase}.gz", "wt") as dest:

        def save(label, key, reserve, losses):
            row = [label, key, str(reserve), list(map(str, losses))]
            dest.write(json.dumps(row, separators=(",", ":")) + "\n")

        if phase == "ordinary":
            pending = assemble(engine, save)
            pending_file.write_text(json.dumps(pending) + "\n")
            print(f"{name}: ordinary enumeration completed, {len(pending)} leaves require pins.")
            return

        fixed = Pinned(engine)
        witnesses = []
        for key in json.loads(pending_file.read_text()):
            for label in ("all15q", "fix4"):
                reserve, losses = fixed.eval(label, tuple(key))
                margin = reserve - sum(losses)
                if margin > 0 and (label == "fix4" or margin >= engine.threshold):
                    save(label, key, reserve, losses)
                    state, xi = tuple(key[:9]), tuple(key[9:])
                    choices = [fixed.winners[state, xi, i, label] for i in range(1, 7)]
                    witnesses.append([label, key, choices])
                    break
            else:
                raise ValueError(f"{name}: uncovered leaf {key}, surplus {margin}")
        if witnesses:
            (out / f"{name}.projections.json").write_text(json.dumps(witnesses, separators=(",", ":")) + "\n")
        print(f"{name}: {len(witnesses)} pinned leaves certified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", choices=SPECS)
    parser.add_argument("phase", choices=("ordinary", "pinned"))
    args = parser.parse_args()
    run(args.name, args.phase)
