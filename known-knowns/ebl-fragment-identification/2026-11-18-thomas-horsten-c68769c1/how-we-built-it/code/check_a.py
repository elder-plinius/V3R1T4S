#!/usr/bin/env python3
"""Condition (a) live checker (frozen rule): a fragment PASSES (a) w.r.t. a matched
chapter iff ALL hold:
  A1. joins == []
  A2. its museum number is not a manuscript of any corpus chapter (no direct chapter link)
  A3. NO references[].notes/title, uncuratedReferences, notes, dossiers or genre path
      names the matched composition. 'Names the composition' = the record mentions BOTH
      a canonical series name for the chapter's text AND the chapter number/name
      (e.g. 'shuila Enlil 1b', 'EAE 57', 'Anzû'). A genre alone (series without number)
      or a number without series name is NOT a naming of THIS composition (conservative:
      if both series+number appear -> FAIL; if only one -> PASS, flagged).
Conservative = when unsure, FAIL (a fragment is only 'unplaced' if it clearly does not
name the composition)."""
import json, os, re, sys, time, unicodedata, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search2 import load_corpus

DATA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/output"
API = "https://www.ebl.lmu.de/api"

def canon(s):
    return s.replace(".", "").replace(",", "").lower()

def strip_diac(s):
    out = []
    for ch in unicodedata.normalize("NFKD", s.lower()):
        if unicodedata.category(ch) == "Mn":
            continue
        out.append(ch)
    return "".join(out)

# canonical series names per (genre, category) (eBL text categories; frozen)
SERIES = {
    ("L", 1):  ["lexical"],
    ("L", 2):  ["lexical"],
    ("L", 3):  ["lexical"],
    ("L", 10): ["anzu", "anzu list", "an-zu"],
    ("L", 11): ["lexical"],
    ("L", 12): ["lexical"],
    ("D", 1):  ["enuma anu enlil", "eae", "summa alu", "almu"],
    ("D", 2):  ["summa alu", "eae", "enuma anu enlil", "summa alu apical"],
    ("D", 3):  ["summa alu"],
    ("D", 4):  ["summa alu", "eae"],
    ("D", 5):  ["enuma anu enlil", "eae"],
    ("Mag", 1): ["sui", "shuila", "prayer", "complaint"],
    ("Mag", 2): ["sui", "shuila", "prayer", "complaint"],
    ("Mag", 3): ["sui", "shuila"],
    ("Mag", 4): ["sui", "shuila"],
    ("Mag", 6): ["sui", "shuila"],
    ("Mag", 7): ["sui", "shuila"],
    ("Mag", 11): ["sui", "shuila"],
    ("Mag", 13): ["sui", "shuila"],
    ("Mag", 31): ["sui", "shuila"],
    ("Med", 1): ["medical", "diagnostic"],
}

def chapter_series(chap):
    genre, cat, idx = chap["textid"]
    _nm = chap.get("name", "")
    names = set(SERIES.get((genre, cat), []))
    names.add(strip_diac(genre))  # the raw genre code, e.g. 'mag'/'D'/'L' rarely names it
    return {n for n in names if n}

def chapter_number_tokens(chap):
    genre, cat, idx = chap["textid"]
    nm = chap.get("name", "").strip()
    toks = set()
    if nm:
        toks.add(nm)                      # e.g. '57', '1a', 'IT', '96NZK', '96nzk'
        if nm[:1].isalpha() and nm[1:].isdigit():
            toks.add(nm[1:])
    toks.add(str(idx))
    toks.add(str(int(idx)))
    return {t for t in toks if t and len(t) >= 1}

def record_text(rec):
    parts = []
    for r in (rec.get("references") or []):
        parts.append(r.get("notes") or "")
        d = r.get("document") or {}
        parts.append(d.get("title") or "")
        parts.append(d.get("collection-title") or "")
    for u in (rec.get("uncuratedReferences") or []):
        if isinstance(u, dict):
            parts.append(u.get("notes") or "")
            parts.append(str(u.get("reference") or u.get("text") or ""))
        else:
            parts.append(str(u))
    n = rec.get("notes") or {}
    parts.append(n.get("text") or "")
    for ds in (rec.get("dossiers") or []):
        if isinstance(ds, dict):
            parts.append(ds.get("notes") or "")
            parts.append(str(ds.get("id") or ds.get("name") or ""))
        else:
            parts.append(str(ds))
    for g in (rec.get("genres") or []):
        if isinstance(g, dict):
            parts.append(" ".join(g.get("category") or []))
        elif isinstance(g, list):
            parts.append(" ".join(str(x) for x in g))
    return " || ".join(p for p in parts if p)

def names_composition(rec, chap):
    """returns (named: bool, evidence: str, partial: bool)"""
    txt = strip_diac(record_text(rec))
    series = chapter_series(chap)
    nums = chapter_number_tokens(chap)
    series_hit = None
    for s in sorted(series, key=len, reverse=True):
        if len(s) >= 3 and re.search(r"(?<![a-z0-9])" + re.escape(strip_diac(s)) + r"(?![a-z0-9])", txt):
            series_hit = s
            break
    num_hit = None
    for t in sorted(nums, key=len, reverse=True):
        tt = strip_diac(t)
        if len(tt) >= 1 and re.search(r"(?<![a-z0-9])" + re.escape(tt) + r"(?![a-z0-9])", txt):
            num_hit = t
            break
    if series_hit and num_hit:
        return True, f"series '{series_hit}' + number '{num_hit}' both in record text", False
    if series_hit:
        return False, f"series name '{series_hit}' present (genre-level), number '{chap['name']}' not -> partial", True
    if num_hit:
        return False, f"number '{num_hit}' present without series name -> partial", True
    return False, "", False

def check_a(fid, chap, rec, ms_canon):
    fails = []; partials = []
    joins = rec.get("joins") or []
    if joins:
        fails.append(f"joins non-empty ({len(joins)} join group(s))")
    mnum = rec.get("museumNumber") or {}
    mnstr = f"{mnum.get('prefix','')}{mnum.get('number','')}{mnum.get('suffix','')}"
    if canon(mnstr) in ms_canon:
        fails.append("museum number appears in a corpus chapter's manuscript list")
    named, ev, partial = names_composition(rec, chap)
    if named:
        fails.append("record names the matched composition: " + ev)
    elif partial:
        partials.append(ev)
    return (len(fails) == 0), fails, partials

def main():
    S = json.load(open(f"{OUT}/S.json"))
    chaps = load_corpus()
    ms_canon = set()
    for c in chaps:
        for m in (c.get("manuscripts") or []):
            if not m:
                continue
            mn = m if "prefix" in m or "number" in m else m.get("museumNumber")
            if isinstance(mn, dict):
                ms_canon.add(canon(f"{mn.get('prefix','')}{mn.get('number','')}{mn.get('suffix','')}"))
    out = []
    for s in S:
        fid = s["fid"]; ci = s["best"]["chapter"]; chap = chaps[ci]
        p = f"{DATA}/records/{fid.replace('/','_').replace(',','_')}.json"
        if not os.path.exists(p):
            url = API + "/fragments/" + urllib.parse.quote(fid, safe="")
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "V3R1T4S"}), timeout=60) as r:
                rec = json.load(r)
            os.makedirs(f"{DATA}/records", exist_ok=True)
            json.dump(rec, open(p, "w"))
            time.sleep(0.5)
        else:
            rec = json.load(open(p))
        ok, fails, partials = check_a(fid, chap, rec, ms_canon)
        out.append({"fid": fid, "chapter": chap["cid"], "pass_a": ok, "fails": fails,
                    "partials": partials, "best": s["best"]})
        print(f"{fid:>16} {'PASS(a)' if ok else 'FAIL(a)'} {chap['cid']:<30} {'; '.join(fails[:2])}{' [partial: '+partials[0]+']' if partials and ok else ''}")
    json.dump(out, open(f"{OUT}/check_a.json", "w"), indent=1)
    npass = sum(1 for x in out if x["pass_a"])
    print(f"\n{npass}/{len(out)} of S pass condition (a)")

if __name__ == "__main__":
    main()
