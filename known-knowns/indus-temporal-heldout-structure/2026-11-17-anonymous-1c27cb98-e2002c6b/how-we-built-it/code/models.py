"""Frozen models for the Indus temporal held-out structure run (PREREG 2026-11-17T02:50Z).

Implements:
- TemplateModel: position-aware class-conditional n-gram (n<=3), add-one smoothing,
  wildcard token for OOV, 4-class. Fit on M77 lines only.
- KN3: Kneser-Ney 3-gram over the M77 sign stream (discount tuned on the 10% M77 split).
- SIGIL-style synthetic control: same-length, position-marginal-matched independent draws.
- Paired bootstrap (10,000 resamples, seed 20261117).

All deterministic given the seed.
"""
import collections, math, random

OOV = -1  # wildcard token
CLASSES = ["Seal", "Tablet", "Pottery", "Other"]

def _logaddexp(a, b):
    if a < b:
        a, b = b, a
    if a == -math.inf:
        return b
    return a + math.log1p(math.exp(b - a))

class TemplateModel:
    """Position-aware class-conditional n-gram. n<=3, add-one, OOV->wildcard."""
    def __init__(self, nmax=3):
        self.nmax = nmax
        self.classes = CLASSES
        self.cnt = {}          # (cls, ctx_tuple, sign) -> count ; ctx tuple = (prev, prev2) with -1 = BOS
        self.class_tot = {}    # cls -> total signs (for class prior)
        self.voc = set()
        self.class_sign_tot = {}  # cls -> count (for smoothing denominator per ctx)
        self.ctx_tot = {}      # (cls, ctx) -> count

    def fit(self, records):
        # records: list of (seq, class)
        for seq, cls in records:
            self.class_tot[cls] = self.class_tot.get(cls, 0) + 1
            prev2 = -1
            prev1 = -1
            self.class_sign_tot[cls] = self.class_sign_tot.get(cls, 0)
            for s in seq:
                self.voc.add(s)
                ctx = (prev1, prev2)
                key = (cls, ctx, s)
                self.cnt[key] = self.cnt.get(key, 0) + 1
                self.ctx_tot[(cls, ctx)] = self.ctx_tot.get((cls, ctx), 0) + 1
                prev2, prev1 = prev1, s
        # OOV wildcard: add one count per (cls, ctx, OOV) so it is never -inf
        for cls in self.classes:
            for (prev1, prev2) in [( -1, -1)] + [(p1, p2) for (p1, p2) in set((c[1][0], c[1][1]) for c in self.cnt if c[0] == cls)]:
                self.cnt[(cls, (prev1, prev2), OOV)] = self.cnt.get((cls, (prev1, prev2), OOV), 0) + 1

    def _p(self, cls, s, prev1, prev2):
        ctx = (prev1, prev2)
        tot = self.ctx_tot.get((cls, ctx), 0)
        V = len(self.voc) + 1  # +wildcard
        alpha = 1.0
        num = self.cnt.get((cls, ctx, s), 0) + alpha
        return (num + 0.0) / (tot + alpha * V) if tot + alpha * V > 0 else 1.0 / (tot + alpha * V)

    def score_seq(self, seq, cls):
        s = 0.0
        prev1, prev2 = -1, -1
        for x in seq:
            xw = x if x in self.voc else OOV
            s += math.log(self._p(cls, xw, prev1, prev2))
            prev2, prev1 = prev1, xw
        return s

    def class_priors(self):
        tot = sum(self.class_tot.values())
        return {c: (self.class_tot.get(c, 0) + 1.0) / (tot + len(self.classes)) for c in self.classes}

    def predict(self, seq):
        priors = self.class_priors()
        best, bestv = None, -math.inf
        for c in self.classes:
            v = math.log(priors[c]) + self.score_seq(seq, c)
            if v > bestv:
                bestv, best = v, c
        return best

def kn3_fit(seq_stream, lambda_max=1.0, min_lambda=0.05, step=0.05, tune_stream=None):
    """Kneser-Ney 3-gram. lambda is a single discount shared across contexts (grid-tuned on the
    held-out 10% M77 split by perplexity; frozen at the argmin)."""
    counts1 = collections.Counter()
    counts2 = collections.Counter()
    counts3 = collections.Counter()
    cont1 = collections.Counter()  # X | _ Y Z  (continuation counts for order 1)
    cont2 = collections.Counter()  # X Y | _ Z
    for s in seq_stream:
        padded = [-1, -1] + list(s) + [-1]
        for i in range(len(padded) - 3):
            a, b, c = padded[i], padded[i + 1], padded[i + 2]
            counts3[(a, b, c)] += 1
        for i in range(len(padded) - 2):
            b, c = padded[i + 1], padded[i + 2]
            counts2[(b, c)] += 1
        for i in range(len(padded) - 1):
            c = padded[i + 1]
            counts1[c] += 1
        # continuations
        for i in range(1, len(padded) - 2):
            a, b, c = padded[i - 1], padded[i], padded[i + 1]
            cont2[(b, c)] += 1
            d = padded[i + 2]
            cont1[(c,)] += 1
    tot_cont2_by_c = collections.Counter()
    for (b, c), v in cont2.items():
        tot_cont2_by_c[c] += v
    tot_cont1 = sum(cont1.values())
    tot_counts1 = sum(counts1.values())
    V1 = len(counts1)
    # KN probability with shared discount lambda (simplified absolute discounting, backoff to lower orders)
    def P(c, b, a, lam):
        n3 = counts3.get((a, b, c), 0)
        if n3 > lam:
            p = (n3 - lam) / max(counts2.get((b, c), 0), 1)
            return p
        # backoff
        w2 = lam * cont2.get((b, c), 1) / max(tot_cont2_by_c.get(c, 0), 1)
        n2 = counts2.get((b, c), 0)
        if n2 > lam:
            p2 = (n2 - lam) / max(counts1.get(c, 0), 1)
            return w2 * p2
        w1 = lam * cont1.get((c,), 1) / max(tot_cont1, 1)
        n1 = counts1.get(c, 0)
        p1 = (n1 - lam) / tot_counts1 if n1 > lam else 1.0 / V1
        return w2 * w1 * p1

    def nll(stream, lam):
        tot = 0.0
        for s in stream:
            padded = [-1, -1] + list(s) + [-1]
            for i in range(1, len(padded) - 2):
                a, b, c = padded[i - 1], padded[i], padded[i + 1]
                p = P(c, b, a, lam)
                tot -= math.log(max(p, 1e-12))
        return tot
    if tune_stream:
        grid = []
        lam = min_lambda
        while lam <= lambda_max + 1e-9:
            grid.append((nll(tune_stream, lam), lam))
            lam += step
        best_lam = min(grid)[1]
    else:
        best_lam = 0.5
    return {"P": P, "lambda": best_lam, "counts3": counts3, "counts2": counts2, "counts1": counts1}

def kn3_sequence_logprob(km, seq, class_prior=None):
    P = km["P"]
    padded = [-1, -1] + list(seq) + [-1]
    tot = 0.0
    for i in range(1, len(padded) - 2):
        a, b, c = padded[i - 1], padded[i], padded[i + 1]
        tot += math.log(max(P(c, b, a, km["lambda"]), 1e-12))
    return tot

def synthetic_position_marginals(heldout_seqs):
    """Position -> Counter(sign) marginals of the held-out sequences (matched on unigram+length)."""
    pos = collections.defaultdict(collections.Counter)
    lens = collections.Counter()
    for s in heldout_seqs:
        lens[len(s)] += 1
        for i, x in enumerate(s):
            pos[i][x] += 1
    return pos, lens

def paired_bootstrap_p(claim_acc_fn, kn_acc_fn, synth_acc_fn, objects, B=10000, seed=20261117, rng=None):
    """p = fraction of B resamples in which claim <= max(kn, synth). objects: list.
    The *_fn take the resampled object list and return accuracy in [0,1]."""
    rng = rng or random.Random(seed)
    n = len(objects)
    if n == 0:
        return 1.0
    real_c = claim_acc_fn(objects)
    real_k = kn_acc_fn(objects)
    real_s = synth_acc_fn(objects)
    wins = 0
    for _ in range(B):
        res = [objects[rng.randrange(n)] for _ in range(n)]
        c = claim_acc_fn(res)
        k = kn_acc_fn(res)
        s = synth_acc_fn(res)
        if c <= max(k, s):
            wins += 1
    return wins / B
