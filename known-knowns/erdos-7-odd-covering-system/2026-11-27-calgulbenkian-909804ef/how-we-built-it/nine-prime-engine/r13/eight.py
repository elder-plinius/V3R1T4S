"""Re-evaluate an eight-prime hierarchy with the author's previous geometric kernel."""
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from time import monotonic

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "r12"))
from harvest import assemble
from pinned import Pinned
from ladder import Engine, SPECS

class Eight(Engine):
    @lru_cache(None)
    def ordinary(self, state):
        return tuple(self.stage(state, i, "ordinary", ()) for i in range(len(self.q)))

    def eval(self, phase, key):
        if phase in ("spatial", "pure3"):
            state = tuple(key[:9])
            xi = tuple(key[9:])
            reserve = self.measure(state)[0]
            return reserve, tuple(self.stage(state, i, "spatial", xi) for i in range(len(self.q)))
        return super().eval(phase, key)

if __name__ == "__main__":
    q = (7, 11, 13, 17, 19, 23)
    taus = tuple(map(Fraction, sys.argv[1].split(","))) if len(sys.argv) > 1 else (4, 4, 6, 8, 12)
    cuts = tuple(map(int, sys.argv[2].split(","))) if len(sys.argv) > 2 else (8, 6)
    stop = Fraction(sys.argv[3]) if len(sys.argv) > 3 else Fraction(1, 1000000)
    SPECS["eight"] = (q, (None,) * 8, taus, cuts, (8, 4, 3), stop)
    engine = Eight("eight")
    start = monotonic()
    minimum = None
    tally = Counter()
    def record(phase, key, reserve, losses):
        global minimum
        tally[phase] += 1
        entry = (reserve - sum(losses), phase, key, reserve, losses)
        if minimum is None or entry < minimum:
            minimum = entry
    pending = assemble(engine, record)
    if len(sys.argv) > 4:
        fixed = Pinned(engine)
        open_keys = []
        for key in pending:
            state, xi = tuple(key[:9]), tuple(key[9:])
            reserve, before = engine.eval("pure3", key)
            for phase in ("first15", "all15q", "fix4"):
                fixed_stages = (1,) if phase == "first15" else range(1, len(q))
                losses = list(before)
                for i in fixed_stages:
                    losses[i] = fixed.stage(state, xi, i, "all15q" if phase == "first15" else phase)
                if reserve > sum(losses):
                    record(phase, key, reserve, tuple(losses))
                    break
            else:
                open_keys.append(key)
        pending = open_keys
    print("parameters", taus, cuts, "threshold", stop)
    print("tally", dict(tally), "pending",len(pending), "least",minimum[:4])
    print("least decimal", float(minimum[0]), "seconds", round(monotonic()-start, 2))
    print("first pending", pending[:1])
