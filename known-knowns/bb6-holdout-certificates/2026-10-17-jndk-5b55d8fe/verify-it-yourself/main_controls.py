# driver appended after prove.py and RULES_JSON: real rules again + mutation controls (all must be rejected)
import copy
DATA = json.loads(RULES_JSON)
RULES = DATA["rules"]
byid = {r["id"]: r for r in RULES}

def mutate(rid, **kw):
    rs = copy.deepcopy(RULES)
    for r in rs:
        if r["id"] == rid:
            r.update(kw)
    return rs

CONTROLS = [
    ("C1 even steps+1 (12k-2)", mutate("even", steps="12k-2"), PROOFS, "even"),
    ("C2 Eodd steps-1 (24k+6)", mutate("Eodd", steps="24k+6"), PROOFS, "Eodd"),
    ("C3 odd flipped output bit (111->110)", mutate("odd", output="A x10 1^(2k-1) 00 110"), PROOFS, "odd"),
    ("C4 Dstep head shifted right by one", mutate("Dstep", output="10 A10 1^(2k-1) 00 111"), PROOFS, "Dstep"),
    ("C5 even output x replaced by constant 0 (true only for x=0)", mutate("even", output="A 0 1^(2k-2) 00 111"), PROOFS, "even"),
    ("C6 even window truncated on the right (context dependence)",
     mutate("even", input="x A0 1^(2k)", output="A x 1^(2k-2) 00 1"), PROOFS, "even"),
    ("C7 even_drain steps+1 (6k^2+3k+1)", mutate("even_drain", steps="6k^2+3k+1"), PROOFS, "even_drain"),
    ("C8 even_drain mutated proof step: even(k) instead of even(k+1)", RULES,
     dict(PROOFS, even_drain=[("even", "k", 0, "0^k", ""), ("IH", "k", 0, "", "111")]), "even_drain"),
    ("C9 Ddrain1 mutated proof step: IH right context 11 instead of 111", RULES,
     dict(PROOFS, Ddrain1=[("Dstep", "2k+1", 0, "", ""), ("IH", "k", 0, "1", "11")]), "Ddrain1"),
    ("C10 Ddrain3 circular proof: IH at k+1", RULES,
     dict(PROOFS, Ddrain3=[("IH", "k+1", 0, "", "")]), "Ddrain3"),
    ("C11 Ddrain1 quadratic step coefficient mutated (12k^2+14k)", mutate("Ddrain1", steps="12k^2+14k"), PROOFS, "Ddrain1"),
    ("C12 Ddrain3 output exponent mutated 1^(3k) -> 0 1^(3k-1)", mutate("Ddrain3", output="1^k A010 1^3 00 0 1^(3k-1)"), PROOFS, "Ddrain3"),
]

results = []
for name, rules, proofs, target in CONTROLS:
    pr = run_all(rules, proofs, "CONTROL " + name, verbose=False)
    rejected = not pr[target]
    results.append((name, target, rejected))
print()
print("CONTROL SUMMARY")
for name, target, rej in results:
    print("  %-70s target=%-10s %s" % (name, target, "REJECTED" if rej else "ACCEPTED (CHECKER VOID!)"))
print("all controls rejected:", all(r for _, _, r in results))
