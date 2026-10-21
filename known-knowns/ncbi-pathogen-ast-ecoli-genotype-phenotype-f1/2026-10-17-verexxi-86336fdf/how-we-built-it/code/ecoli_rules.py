"""Reimplementation (as code) of the published genotype-field rule of PMC13513162 (Supplementary Table S3 /
NCBI_S7 rule summaries), calibrated so it reproduces the paper's own per-comparison predictions (NCBI_S9) exactly.
Input: the NCBI 'AMR genotypes' / AMR_genotypes field (comma-separated tokens; name=STATUS, a bare name means COMPLETE). Output: 'R' or 'S' per antibiotic."""
import re
ANTIBIOTICS = ["ciprofloxacin", "ampicillin", "gentamicin", "tetracycline", "trimethoprim-sulfamethoxazole",
               "ceftriaxone", "amoxicillin-clavulanic acid", "meropenem"]
OK_STATUS = {"COMPLETE", "POINT"}
def tokens(field):
    out = []
    for t in str(field).split(","):
        t = t.strip()
        if not t or t == "NULL": continue
        if "=" in t:
            n, s = t.rsplit("=", 1); out.append((n, s))
        else:
            out.append((t, "COMPLETE"))  # NCBI FTP metadata TSV omits '=COMPLETE'; the browser export spells it out
    return out
ACQ_BLA = re.compile(r"^bla(?!EC\b|EC-|HER)")          # any acquired beta-lactamase; intrinsic blaEC (and blaHER) excluded
ESC = re.compile(r"^bla(CTX-M|CMY|DHA|KPC|NDM|VIM|IMP|VEB|GES|PER|ACC|FOX|MOX|ACT|OXA-(48|181|232|244|162|204|370|484|1397)\b)")
CARBA = re.compile(r"^bla(KPC|NDM|VIM|IMP|OXA-(48|181|232|244|162|204|370|484)\b|GES-(2|4|5|6|14|16|20)\b)")
QUIN = re.compile(r"^(gyrA_|parC_(S80|E84)|parE_|qnr|qepA|oqx|aac\(6'\)-Ib-cr)")
GEN = re.compile(r"^(aac\(3\)|aac\(6'\)-(Ib|IIc|Il)|ant\(2''\)|armA|rmt|npmA)")
TET = re.compile(r"^tet\(")
def matched(ab, field):
    tk = [(n, s) for n, s in tokens(field) if s in OK_STATUS]
    if ab in ("ampicillin", "amoxicillin-clavulanic acid"):
        return [n for n, s in tk if ACQ_BLA.match(n)]
    if ab == "ceftriaxone":
        return [n for n, s in tk if ESC.match(n)]
    if ab == "meropenem":
        return [n for n, s in tk if CARBA.match(n)]
    if ab == "ciprofloxacin":
        return [n for n, s in tk if QUIN.match(n)]
    if ab == "gentamicin":
        return [n for n, s in tk if GEN.match(n)]
    if ab == "tetracycline":
        return [n for n, s in tk if TET.match(n)]
    if ab == "trimethoprim-sulfamethoxazole":
        d = [n for n, s in tk if n.startswith("dfr")]; su = [n for n, s in tk if n.startswith("sul")]
        return d + su if d and su else []
    raise KeyError(ab)
def predict(ab, field):
    return "R" if matched(ab, field) else "S"
