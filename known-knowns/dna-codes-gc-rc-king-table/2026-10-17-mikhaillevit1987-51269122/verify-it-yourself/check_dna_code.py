"""Standalone checker written from the definition. Python 3, standard library only.

Usage: python check_dna_code.py WORDS.txt N D
A_4^{GC,RC}(n,d,w) code with w = floor(n/2): distinct words of length n over ACGT, each with
exactly w letters in {C,G}; Hamming(x,y) >= d for distinct x,y; Hamming(x, rc(y)) >= d for ALL
x,y including x = y, where rc reverses the word and swaps A<->T, C<->G.
Prints one line per property and VALID or INVALID last; exit code 0 only if valid.
"""
import sys

path, n, d = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
words = [ln.strip() for ln in open(path, encoding="ascii") if ln.strip()]
comp = {"A": "T", "T": "A", "C": "G", "G": "C"}


def rc(x):
    return "".join(comp[c] for c in reversed(x))


def ham(x, y):
    return sum(a != b for a, b in zip(x, y))


ok = True
def report(name, good, detail):
    global ok
    ok = ok and good
    print("%-28s %s  %s" % (name, "ok" if good else "FAIL", detail))


report("size", True, len(words))
report("distinct", len(set(words)) == len(words), "")
report("length and alphabet", all(len(x) == n and set(x) <= set("ACGT") for x in words), "n=%d" % n)
gcs = sorted({sum(c in "CG" for c in x) for x in words})
report("GC count = floor(n/2)", gcs == [n // 2], "GC counts %s" % gcs)
pair = [ham(x, y) for i, x in enumerate(words) for y in words[i + 1:]]
report("pairwise Hamming >= d", min(pair) >= d, "min %d over %d pairs" % (min(pair), len(pair)))
rcd = [ham(x, rc(y)) for x in words for y in words]
report("Hamming(x, rc(y)) >= d", min(rcd) >= d, "min %d over %d ordered pairs incl. self" % (min(rcd), len(rcd)))
selfd = [ham(x, rc(x)) for x in words]
report("self-pairs Hamming(x, rc(x))", min(selfd) >= d, "min %d" % min(selfd))
print("VALID" if ok else "INVALID")
sys.exit(0 if ok else 1)
