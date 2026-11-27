"""Keep one physical projection throughout both 7-channels and all comparison layers."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import ceil

from ladder import KAPPA, PINS, ZERO, counts, field, layer_jobs, law, query, region_heights, register


def residues(a, phase):
    eta = tuple(x for x in range(15) if x % 3 and x % 5 and x != a)
    if phase == "all15q":
        return ((x,) for x in eta)
    return product((1, 2), range(1, 5), (2, 4, 5, 7, 8), eta)


@lru_cache(None)
def selected_difference(ordinary, pinned, caps, pos3, pos5, tau, w, indices, law_key, bounds):
    """Exact difference of two maxima on the same retained finite layers."""
    mmax, umax, vmax = bounds
    _, _, cells = region_heights(caps, (umax + 1, vmax + 1), pos3, pos5)
    if not cells:
        return Q(0)
    weights = [term[2] for term in cells]
    distribution, _, _ = law(*law_key)
    saving = Q(0)
    for m, prob in distribution.items():
        if m >= tau or m > mmax:
            continue
        den0, jobs0 = layer_jobs(cells, tau / m, Q(0), ())
        den1, jobs1 = layer_jobs(cells, tau / m, w / m, indices)
        free_values = query(ordinary, jobs0)
        fixed_values = query(pinned, jobs1)
        difference = sum(weight * (Q(x, den0) - Q(y, den1))
                         for weight, x, y in zip(weights, free_values, fixed_values))
        assert difference >= 0
        saving += m * prob * difference
    return saving


class Pinned:
    def __init__(self, engine):
        self.engine = engine
        self.winners = {}

    @lru_cache(None)
    def stage(self, state, xi, i, phase):
        engine = self.engine
        _, regions, _ = engine.measure(state)
        scale = tuple(KAPPA[n] for n in counts(PINS, xi))
        fields = []
        for mode in ("zero", "positive"):
            key = (engine.q[:i], engine.exps[2:2+i], engine.c[:i], mode, ceil(engine.t[i]))
            for raw, den, pos3, pos5 in regions:
                a, factor = field(raw, den, scale if mode == "zero" else None)
                fields.append((a, factor, pos3, pos5, key))

        indices = PINS
        bounds = engine.pin
        if phase == "all15q":
            indices = (4,)
            bounds = (ceil(engine.t[i]) - 1, *engine.pin[1:])
        ordinary = engine.stage(state, i, "spatial", xi) * engine.beta[i]
        least_saving = None
        for candidate in residues(state[0], phase):
            offset = counts(indices, candidate)
            saving = Q(0)
            for a, factor, pos3, pos5, law_key in fields:
                saving += factor * selected_difference(
                    register(a, ZERO), register(a, offset), engine.axcaps, pos3, pos5,
                    engine.t[i], engine.w[i], indices, law_key, bounds)
            if least_saving is None or saving < least_saving:
                least_saving = saving
                self.winners[state, xi, i, phase] = candidate
        return (ordinary - least_saving) / engine.beta[i]

    def eval(self, phase, key):
        state, xi = tuple(key[:9]), tuple(key[9:])
        current = self.engine.stage(state, 0, "spatial", xi)
        later = tuple(self.stage(state, xi, i, phase) for i in range(1, 7))
        return self.engine.measure(state)[0], (current,) + later
