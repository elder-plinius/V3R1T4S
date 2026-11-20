"""Second, independent composition check of the enc1 chain of SAT refutations.

Written from the logic only (see report.md for the conditions C0..C9 and the proof).
Standard library only. No solver, no proof checker is run.

Usage:
  python -I second_audit.py --fbase F.cnf --flem Flem.cnf --root CHAINROOT [--skip-proofs] [--hash-proofs-upto K]

Last output line is exactly one of
  SECOND AUDIT enc1: PASS
  SECOND AUDIT enc1: PARTIAL (classes 0..k finished, no problem found)
  SECOND AUDIT enc1: FAIL ...
(with --skip-proofs the prefix is "SECOND AUDIT enc1 [PROOF FILES NOT CHECKED]:" and PASS is never printed).
"""
import argparse
import hashlib
import json
import os
import sys

NCLASS_EXPECTED = 20


class Bad(Exception):
    pass


LINECACHE = {}


def _key(x):
    return (abs(x), x)


def _parse_clause(ln):
    toks = ln.split(b" ")
    if toks[-1] != b"0":
        raise Bad("clause line does not end with ' 0': %r" % ln[:60])
    lits = []
    for t in toks[:-1]:
        try:
            n = int(t)
        except ValueError:
            raise Bad("non integer token %r" % t[:20])
        if n == 0 or str(n).encode() != t:
            raise Bad("irregular literal token %r (zero in the middle, sign or padding, or spacing)" % t[:20])
        lits.append(n)
    return tuple(sorted(set(lits), key=_key))


def parse_cnf(data):
    """Strict DIMACS reader. Returns (nv, nc_header, clauses as canonical tuples, in file order)."""
    if b"\r" in data:
        raise Bad("carriage return in file")
    if not data.endswith(b"\n"):
        raise Bad("no final newline")
    lines = data.split(b"\n")
    lines.pop()
    if not lines or not lines[0].startswith(b"p cnf "):
        raise Bad("first line is not a 'p cnf' header")
    h = lines[0].split(b" ")
    if len(h) != 4:
        raise Bad("malformed header")
    try:
        nv = int(h[2])
        nc = int(h[3])
    except ValueError:
        raise Bad("non integer header")
    out = []
    cache = LINECACHE
    for ln in lines[1:]:
        c = cache.get(ln)
        if c is None:
            c = _parse_clause(ln)
            cache[ln] = c
        out.append(c)
    return nv, nc, out


def is_taut(c):
    s = set(c)
    return any(-l in s for l in c)


def maxvar(clauses):
    m = 0
    for c in clauses:
        if c:
            v = abs(c[-1])
            if v > m:
                m = v
    return m


def sha256_file(path, bufsize=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def fmt_clause(c, n=6):
    c = list(c)
    if len(c) <= n:
        return "{" + " ".join(map(str, c)) + "}"
    return "{" + " ".join(map(str, c[:n])) + " ... (%d lits)}" % len(c)


class Audit:
    def __init__(self, fbase, flem, root, skip_proofs=False, hash_upto=0, out=print, label="enc1"):
        self.label = label
        self.fbase = fbase
        self.flem = flem
        self.root = root
        self.skip_proofs = skip_proofs
        self.hash_upto = hash_upto
        self.out = out
        self.fails = []
        self.notes = []
        self.E = set()          # established clauses (canonical tuples)
        self.derived = {}       # tuple -> label, for clauses established by the chain (not F)
        self.cnf_hashes = {}    # sha -> label
        self.proof_hashes = {}

    def say(self, s):
        self.out(s)

    def fail(self, where, why):
        msg = "%s: %s" % (where, why)
        self.fails.append(msg)
        self.say("  FAIL " + msg)

    def note(self, where, why):
        msg = "%s: %s" % (where, why)
        self.notes.append(msg)
        self.say("  note " + msg)

    # ---------------------------------------------------------------- global part
    def load_base(self):
        try:
            with open(self.fbase, "rb") as f:
                nv, nc, F = parse_cnf(f.read())
            with open(self.flem, "rb") as f:
                nv2, nc2, FL = parse_cnf(f.read())
        except (Bad, OSError) as e:
            self.fail("base files", str(e))
            return False
        ok = True
        if nc != len(F):
            self.fail("Fbase", "header says %d clauses, file has %d" % (nc, len(F)))
            ok = False
        if nc2 != len(FL):
            self.fail("Fbase-lemmas", "header says %d clauses, file has %d" % (nc2, len(FL)))
            ok = False
        if nv != nv2:
            self.fail("Fbase-lemmas", "variable count %d differs from Fbase %d" % (nv2, nv))
            ok = False
        if maxvar(F) > nv or maxvar(FL) > nv:
            self.fail("base", "a literal exceeds the declared variable count")
            ok = False
        if any(len(c) == 0 for c in F):
            self.note("Fbase", "F contains the empty clause (trivially unsatisfiable)")
        nF = len(F)
        if FL[:nF] != F:
            self.fail("Fbase-lemmas", "the first %d clauses are not exactly the clauses of Fbase, in order" % nF)
            ok = False
        lem = FL[nF:]
        if len(lem) != 3 * NCLASS_EXPECTED:
            self.fail("Fbase-lemmas", "%d extra clauses, expected %d" % (len(lem), 3 * NCLASS_EXPECTED))
            ok = False
        for i, c in enumerate(lem):
            if len(c) == 0 or is_taut(c):
                self.fail("Fbase-lemmas", "lemma %d (class %d, a%d) is empty or tautological" % (i, i // 3, i % 3 + 1))
                ok = False
        if len(set(lem)) != len(lem):
            self.note("Fbase-lemmas", "some lemma clauses coincide with each other")
        self.nv = nv
        self.nF = nF
        self.E = set(F)
        self.lem = lem
        self.say("base: Fbase %d vars %d clauses; Fbase-lemmas = Fbase + %d clauses (prefix identical, in order); lemma sizes %s"
                 % (nv, nF, len(lem), ",".join(str(len(c)) for c in lem[:6]) + ",..."))
        return ok

    # ---------------------------------------------------------------- one CNF file
    def check_cnf(self, where, path, rec_sha, target, cls):
        """Return dict with D (derived clause), or None if the file is unusable (FAIL already recorded)."""
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError as e:
            self.fail(where, "cannot read %s: %s" % (os.path.basename(path), e))
            return None
        sha = hashlib.sha256(data).hexdigest()
        if sha != rec_sha:
            self.fail(where, "sha256 of %s is %s, the recorded verdict is for %s" % (os.path.basename(path), sha[:16], str(rec_sha)[:16]))
            return None
        if sha in self.cnf_hashes:
            self.note(where, "same CNF bytes as %s" % self.cnf_hashes[sha])
        self.cnf_hashes[sha] = where
        try:
            nv, nc, cl = parse_cnf(data)
        except Bad as e:
            self.fail(where, "unreadable DIMACS: %s" % e)
            return None
        if nc != len(cl):
            self.fail(where, "header says %d clauses, file has %d" % (nc, len(cl)))
            return None
        if nv != self.nv:
            self.fail(where, "header variable count %d differs from F (%d)" % (nv, self.nv))
            return None
        if maxvar(cl) > nv:
            self.fail(where, "literal above declared variable count")
            return None
        E = self.E
        units = set()
        bad = []
        n_in = 0
        n_sub = 0
        for c in cl:
            if c in E:
                n_in += 1
            elif len(c) == 1:
                units.add(c[0])
            else:
                cs = set(c)
                if any(set(d) <= cs for d in self.derived):
                    n_sub += 1      # a superset of an established clause: implied by it
                else:
                    bad.append(c)
        if bad:
            self.fail(where, "%d clause(s) are neither in F, nor established earlier, nor unit, e.g. %s" % (len(bad), fmt_clause(bad[0])))
            return None
        D = tuple(sorted({-u for u in units}, key=_key))
        if is_taut(D):
            self.fail(where, "the unit clauses outside the established set contradict each other (derived clause is a tautology)")
            return None
        info = {"n": len(cl), "n_in": n_in, "n_sub": n_sub, "nunits": len(units), "D": D, "sha": sha}
        fileset = set(cl)
        info["used"] = [self.derived[d] for d in self.derived if d in fileset]
        info["all_units_neg"] = {-c[0] for c in cl if len(c) == 1}
        if target is not None:
            if not set(D) <= set(target):
                extra = sorted(set(D) - set(target), key=_key)
                self.fail(where, "derived clause %s is not a subset of the claimed lemma (extra literals %s)" % (fmt_clause(D), extra[:6]))
                return None
            missing_neg = [l for l in target if l not in info["all_units_neg"]]
            info["target_exact"] = (set(D) == set(target))
            info["target_missing_neg"] = len(missing_neg)
        return info

    def check_proof_file(self, where, path, rec_bytes, rec_sha, hash_it):
        try:
            sz = os.path.getsize(path)
        except OSError:
            self.fail(where, "proof file %s missing" % os.path.basename(path))
            return False
        if rec_bytes is None:
            self.note(where, "no recorded proof size for %s (actual %d bytes)" % (os.path.basename(path), sz))
        elif sz != rec_bytes:
            self.fail(where, "proof file %s has %d bytes, recorded %s" % (os.path.basename(path), sz, rec_bytes))
            return False
        if rec_sha is not None:
            if rec_sha in self.proof_hashes:
                self.note(where, "same recorded proof hash as %s" % self.proof_hashes[rec_sha])
            self.proof_hashes[rec_sha] = where
        if hash_it:
            if sha256_file(path) != rec_sha:
                self.fail(where, "sha256 of proof file differs from the recorded one")
                return False
        return True

    def check_record(self, where, rec):
        if not isinstance(rec, dict):
            self.fail(where, "record is not an object")
            return False
        if rec.get("drat_trim") != "s VERIFIED":
            self.fail(where, "recorded verdict is %r, not 's VERIFIED'" % rec.get("drat_trim"))
            return False
        if not isinstance(rec.get("cnf_sha256"), str):
            self.fail(where, "no cnf_sha256 in the record")
            return False
        return True

    # ---------------------------------------------------------------- class
    def load_json(self, path):
        try:
            with open(path, "rb") as f:
                return json.loads(f.read().decode("utf-8"))
        except (OSError, ValueError):
            return None

    def finished_state(self, c):
        d1 = os.path.join(self.root, self.label + "-c%02d-l12" % c)
        d2 = os.path.join(self.root, self.label + "-c%02d-a4" % c)
        if not os.path.isdir(d1):
            return None, None, None, "folder l12 absent"
        if not os.path.isdir(d2):
            return None, None, None, "folder a4 absent"
        l12 = self.load_json(os.path.join(d1, "l12.json"))
        if not isinstance(l12, list):
            return None, None, None, "l12.json absent or unreadable"
        st = self.load_json(os.path.join(d2, "state.json"))
        if not isinstance(st, dict):
            return None, None, None, "state.json absent or unreadable"
        if not isinstance(st.get("glue"), dict) or not st["glue"].get("drat_trim"):
            return None, None, None, "no glue record yet (a4 still running)"
        return (d1, d2), l12, st, None

    def run_class(self, c):
        """Return 'PASS', 'FAIL' or 'NOT FINISHED'."""
        nfail0 = len(self.fails)
        dirs, l12, st, why = self.finished_state(c)
        W = "c%02d" % c
        if dirs is None:
            self.say("class %02d: NOT FINISHED (%s)" % (c, why))
            return "NOT FINISHED"
        d1, d2 = dirs
        a1, a2, a3 = self.lem[3 * c], self.lem[3 * c + 1], self.lem[3 * c + 2]
        self.say("class %02d: lemma sizes |a1|=%d |a2|=%d |a3|=%d" % (c, len(a1), len(a2), len(a3)))
        hp = (not self.skip_proofs) and c < self.hash_upto
        chk_proof = not self.skip_proofs

        # ---- L1, L2
        recs = {}
        if len(l12) != 2:
            self.fail(W + " l12.json", "expected exactly 2 records, found %d" % len(l12))
            return "FAIL"
        for r in l12:
            if isinstance(r, dict) and r.get("lemma") in ("L1", "L2"):
                if r["lemma"] in recs:
                    self.fail(W + " l12.json", "record %s appears twice" % r["lemma"])
                    return "FAIL"
                recs[r["lemma"]] = r
        if set(recs) != {"L1", "L2"}:
            self.fail(W + " l12.json", "records are not exactly L1 and L2")
            return "FAIL"
        extra = [x for x in os.listdir(d1) if x not in ("L1.cnf", "L1.bin", "L2.cnf", "L2.bin", "l12.json", "tmp")]
        if extra:
            self.fail(W + " l12", "unrecorded file(s) in folder: %s" % extra[:5])
            return "FAIL"
        for name, tgt, k in (("L1", a1, 1), ("L2", a2, 2)):
            where = "%s %s" % (W, name)
            r = recs[name]
            if not self.check_record(where, r):
                return "FAIL"
            if r.get("literals") is not None and r["literals"] != len(tgt):
                self.fail(where, "record says %s literals, the lemma a%d has %d" % (r["literals"], k, len(tgt)))
                return "FAIL"
            info = self.check_cnf(where, os.path.join(d1, name + ".cnf"), r["cnf_sha256"], tgt, c)
            if info is None:
                return "FAIL"
            if chk_proof and not self.check_proof_file(where, os.path.join(d1, name + ".bin"), r.get("proof_bytes"), r.get("proof_sha256"), hp):
                return "FAIL"
            self.say("  %s: %d clauses (%d established, %d new units, %d supersets); derived %s %s a%d; used from earlier: %s; sha ok%s"
                     % (name, info["n"], info["n_in"], info["nunits"], info["n_sub"], fmt_clause(info["D"]),
                        "==" if info["target_exact"] else "subset of", k, info["used"] or "none",
                        "" if not chk_proof else "; proof %s bytes ok%s" % (r.get("proof_bytes"), " + sha ok" if hp else "")))
            if info["target_missing_neg"]:
                self.note(where, "%d literal(s) of a%d are not negated by any unit of the file (stronger claim, still sound)" % (info["target_missing_neg"], k))
            tgt_t = tgt
            self.E.add(tgt_t)
            self.derived[tgt_t] = "c%02d:a%d" % (c, k)

        # ---- pieces and glue
        pieces = st.get("pieces")
        if not isinstance(pieces, list) or not pieces:
            self.fail(W + " state.json", "no piece records")
            return "FAIL"
        K = len(pieces)
        if st.get("verified") != K:
            self.fail(W + " state.json", "'verified' is %r but %d piece records" % (st.get("verified"), K))
            return "FAIL"
        for i, r in enumerate(pieces):
            if not isinstance(r, dict) or r.get("piece") != i:
                self.fail(W + " state.json", "piece record %d has index %r (pieces must be 0..K-1 in order, none missing)" % (i, None if not isinstance(r, dict) else r.get("piece")))
                return "FAIL"
        sq = [r.get("square") for r in pieces]
        if len(set(sq)) != K:
            self.note(W + " state.json", "'square' values are not all distinct: %s" % sq)
        expect = {"piece-%02d.cnf" % i for i in range(K)} | {"piece-%02d.bin" % i for i in range(K)} | {"glue.cnf", "glue.bin", "state.json", "tmp"}
        actual = set(os.listdir(d2))
        if actual - expect:
            self.fail(W + " a4", "unrecorded file(s) in folder: %s" % sorted(actual - expect)[:5])
            return "FAIL"
        Qs = []
        agg_miss = []
        agg_sub = []
        tot_proof = 0
        sizes = []
        for i, r in enumerate(pieces):
            where = "%s piece-%02d" % (W, i)
            if not self.check_record(where, r):
                return "FAIL"
            info = self.check_cnf(where, os.path.join(d2, "piece-%02d.cnf" % i), r["cnf_sha256"], None, c)
            if info is None:
                return "FAIL"
            if chk_proof and not self.check_proof_file(where, os.path.join(d2, "piece-%02d.bin" % i), r.get("proof_bytes"), r.get("proof_sha256"), hp):
                return "FAIL"
            Q = info["D"]
            if len(Q) == 0:
                self.note(where, "derived clause is EMPTY: the file refutes the established set alone (F would be unsatisfiable)")
            expected_used = ["c%02d:Q%d" % (c, j) for j in range(i)]
            miss = [x for x in expected_used if x not in info["used"]]
            if miss:
                agg_miss.append((i, len(miss)))
            foreign = [x for x in info["used"] if not x.startswith("c%02d:" % c)]
            if foreign:
                self.note(where, "uses clauses established in other classes: %s" % foreign[:4])
            if info["n_sub"]:
                agg_sub.append((i, info["n_sub"]))
            Qs.append(Q)
            sizes.append(len(Q))
            self.E.add(Q)
            self.derived[Q] = "c%02d:Q%d" % (c, i)
            tot_proof += r.get("proof_bytes") or 0
        if agg_miss or agg_sub:
            self.note(W, "in %d piece file(s) an earlier Q is present only as a SUPERSET of the clause read off its own piece (%d such clauses in total); "
                         "accepted because a superset of an established clause is implied by it" % (len(agg_sub), sum(n for _, n in agg_sub)))
        self.say("  pieces: %d, each file = established clauses + negation units, hashes ok%s; derived |Q_i| = %s; proofs total %.1f MB"
                 % (K, "" if not chk_proof else ", proof sizes ok" + (" + proof sha ok" if hp else ""), ",".join(map(str, sizes)), tot_proof / 1e6))
        if len(set(Qs)) != K:
            self.note(W, "some Q clauses coincide")
        gr = st["glue"]
        where = "%s glue" % W
        if not self.check_record(where, gr):
            return "FAIL"
        info = self.check_cnf(where, os.path.join(d2, "glue.cnf"), gr["cnf_sha256"], a3, c)
        if info is None:
            return "FAIL"
        if chk_proof and not self.check_proof_file(where, os.path.join(d2, "glue.bin"), gr.get("proof_bytes"), gr.get("proof_sha256"), hp):
            return "FAIL"
        usedQ = [x for x in info["used"] if x.startswith("c%02d:Q" % c)]
        self.say("  glue: %d clauses (%d established, %d new units, %d supersets); derived %s a3; contains %d of %d Q clauses and a1,a2: %s; sha ok"
                 % (info["n"], info["n_in"], info["nunits"], info["n_sub"], "==" if info["target_exact"] else "subset of",
                    len(usedQ), K, all(x in info["used"] for x in ("c%02d:a1" % c, "c%02d:a2" % c))))
        if info["target_missing_neg"]:
            self.note(where, "%d literal(s) of a3 are not negated by any unit (stronger claim, still sound)" % info["target_missing_neg"])
        if len(usedQ) != K:
            self.note(where, "glue carries %d of the %d clauses read off the pieces literally and %d others as supersets of them (the full-width case clauses); sound either way" % (len(usedQ), K, info["n_sub"]))
        self.E.add(a3)
        self.derived[a3] = "c%02d:a3" % c
        if len(self.fails) > nfail0:
            return "FAIL"
        self.say("  class %02d: all conditions hold" % c)
        return "PASS"

    def run(self):
        if not self.load_base():
            self.say("SECOND AUDIT %s: FAIL (%s)" % (self.label, "; ".join(self.fails)))
            return "FAIL"
        status = []
        for c in range(NCLASS_EXPECTED):
            status.append(self.run_class(c))
        fin = [c for c, s in enumerate(status) if s != "NOT FINISHED"]
        prefix = 0
        while prefix < NCLASS_EXPECTED and status[prefix] != "NOT FINISHED":
            prefix += 1
        tag = "SECOND AUDIT " + self.label + (" [PROOF FILES NOT CHECKED]" if self.skip_proofs else "")
        if self.fails:
            self.say("")
            self.say("summary of failures:")
            for m in self.fails:
                self.say("  - " + m)
            v = "FAIL (%d problem(s); first: %s)" % (len(self.fails), self.fails[0])
        elif prefix == NCLASS_EXPECTED and not self.skip_proofs:
            v = "PASS"
        else:
            extra = [c for c in fin if c >= prefix]
            if prefix == 0:
                v = "PARTIAL (no class finished, no problem found)"
            else:
                v = "PARTIAL (classes 0..%d finished, no problem found)" % (prefix - 1)
            if extra:
                self.say("note: classes %s are finished although an earlier class is not" % extra)
            if prefix == NCLASS_EXPECTED:
                v = "PARTIAL (classes 0..%d finished, no problem found; proof files not checked)" % (prefix - 1)
        self.say("")
        self.say("%s: %s" % (tag, v))
        return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fbase", required=True)
    ap.add_argument("--flem", required=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--label", default="enc1")
    ap.add_argument("--skip-proofs", action="store_true")
    ap.add_argument("--hash-proofs-upto", type=int, default=0, help="also sha256 the proof files of classes below this number")
    a = ap.parse_args()
    v = Audit(a.fbase, a.flem, a.root, a.skip_proofs, a.hash_proofs_upto, label=a.label).run()
    sys.exit(0 if not v.startswith("FAIL") else 1)


if __name__ == "__main__":
    main()
