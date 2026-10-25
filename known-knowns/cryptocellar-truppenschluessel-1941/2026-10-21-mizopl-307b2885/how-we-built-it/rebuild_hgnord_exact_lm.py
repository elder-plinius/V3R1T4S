#!/usr/bin/env python3
"""
Rebuild the 1941 Heeresgruppe Nord 25-Letter Truppenschluessel Language Model (T1, T2, T3, T4)
grounded strictly in the TS encipherment rules (Ostwald & Weierud 2021, mcts.pdf Section 3.1 p. 4):
  - 25-letter alphabet (no J): J -> II, CH -> Q (so SCH -> SQ), ss -> SZ, Ae/Oe/Ue -> AE/OE/UE.
  - Unlike Enigma (where X separates every word, ~7% X), manual TS field messages concatenate
    German words directly and use X only at clause/sentence boundaries (~10% of word boundaries,
    giving ~1.6% X and ~3.1% Q).
  - All 9 TS plaintexts from Ostwald & Weierud (2021) mcts.pdf are HELD OUT for blind positive-control testing.
"""
import re
import math
import numpy as np
from bs4 import BeautifulSoup

import os
WORK = os.path.dirname(os.path.abspath(__file__))
ALPHA25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
C2I = {c: i for i, c in enumerate(ALPHA25)}

def to_ts25(s: str) -> str:
    s = s.upper()
    s = (s.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
          .replace("ß", "SZ"))
    s = s.replace("CH", "Q")
    s = s.replace("J", "II")
    return "".join(c for c in s if c in C2I)

def main():
    c1 = np.full(25, 10.0, dtype=np.float64)
    c2 = np.full((25, 25), 1.0, dtype=np.float64)
    c3 = np.full((25, 25, 25), 0.2, dtype=np.float64)
    c4 = np.full((25, 25, 25, 25), 0.04, dtype=np.float64)

    def add_text(s: str, w: float):
        idx = [C2I[c] for c in s if c in C2I]
        n = len(idx)
        if n < 5:
            return
        arr = np.array(idx, dtype=np.int32)
        np.add.at(c1, arr, w)
        np.add.at(c2, (arr[:-1], arr[1:]), w)
        np.add.at(c3, (arr[:-2], arr[1:-1], arr[2:]), w)
        np.add.at(c4, (arr[:-3], arr[1:-2], arr[2:-1], arr[3:]), w)

    # 1. Extract all authentic 1941 HG Nord Enigma plaintexts (holding out any TS texts)
    hgn_texts = []
    for line in open(f"{WORK}/july_enigma_plaintexts.txt"):
        p = line.strip().split("\t")
        if len(p) >= 4 and p[2] not in ("CASBL", "MVUEH", "SIPVX", "SOFGI", "WRMKX"):
            hgn_texts.append(p[3])

    for fn in ["bgac.pdf.layout.txt", "enigma-modern-breaking.pdf.layout.txt", "heeresgruppe-nord-july-1941.pdf.layout.txt", "break-of-enigma-msgs-awtzk-and-znlzt.pdf.txt"]:
        txt = open(f"{WORK}/{fn}", errors="ignore").read()
        for m in re.finditer(r"(?:[A-Za-z]+\s+[xX]\s+){2,}[A-Za-z0-9\s\-\.,xX]{20,}", txt):
            s = re.sub(r"[^A-Za-z]", "", m.group(0)).upper()
            if len(s) >= 25 and s.count("X") >= 2:
                hgn_texts.append(s)

    for fn in ["the-fmngi-break.html", "the-awtzk-znlzt-breaks.html", "the-mvueh-break.html", "enigma-modern-breaking.html"]:
        txt = BeautifulSoup(open(f"{WORK}/{fn}", errors="ignore").read(), "html.parser").get_text("\n")
        for m in re.finditer(r"(?:[A-Za-z]+\s*[xX]\s*){2,}[A-Za-z\s]{15,}", txt):
            s = re.sub(r"[^A-Za-z]", "", m.group(0)).upper()
            if len(s) >= 25 and s.count("X") >= 2:
                hgn_texts.append(s)

    unique_hgn = sorted(set(hgn_texts))
    print(f"Loaded {len(unique_hgn)} unique 1941 HG Nord Enigma plaintexts...")

    rng = np.random.default_rng(19410708)
    hgn_tokens = []
    for pt in unique_hgn:
        words = [w for w in pt.split("X") if len(w) >= 2]
        for w in words:
            t25 = to_ts25(w)
            if 2 <= len(t25) <= 24:
                hgn_tokens.append(t25)
        # Convert Enigma X-separated text into TS-style continuous German (keeping X only ~12% of the time at clause breaks)
        for rep in range(6):
            out_w = []
            for wi, w in enumerate(words):
                out_w.append(w)
                if wi + 1 < len(words) and rng.random() < 0.11:
                    out_w.append("X")
            add_text(to_ts25("".join(out_w)), 80.0)

    # 2. Add 1941 HG Nord domain vocabulary & phrases in TS continuous style
    import build_hgnord_lm as b0
    for ph in b0.HGNORD_MILITARY_PHRASES:
        # ph may contain X; create both continuous (no X) and clause-X versions
        words = [w for w in ph.split("X") if w]
        cont = to_ts25("".join(words))
        add_text(cont, 120.0)
        add_text(cont + "X", 40.0)
        for w in words:
            t25 = to_ts25(w)
            if len(t25) >= 2:
                hgn_tokens.extend([t25] * 4)

    # 3. Generate a 2,500,000-char TS-style tactical stream (11% X at word boundaries -> ~1.6% X overall)
    idx_tok = rng.integers(0, len(hgn_tokens), size=300000)
    use_x = rng.random(300000) < 0.11
    parts = []
    for i, ti in enumerate(idx_tok):
        parts.append(hgn_tokens[ti])
        if use_x[i]:
            parts.append("X")
    hgn_stream = "".join(parts)
    print(f"Generated {len(hgn_stream)}-char TS tactical stream (X={hgn_stream.count('X')/len(hgn_stream)*100:.2f}%, Q={hgn_stream.count('Q')/len(hgn_stream)*100:.2f}%)")
    add_text(hgn_stream, 2.0)

    # 4. General German corpus from de_50k in TS continuous style (10% X at word boundaries -> ~1.5% X)
    de50k = []
    for line in open(f"{WORK}/de_50k.txt", errors="ignore"):
        p = line.strip().split()
        if len(p) == 2 and p[1].isdigit():
            w25 = to_ts25(p[0])
            if len(w25) >= 2:
                de50k.append((w25, int(p[1])))
    probs = np.array([math.pow(x[1], 0.65) for x in de50k], dtype=np.float64)
    probs /= probs.sum()
    s_idx = rng.choice(len(de50k), size=500000, p=probs)
    u_x = rng.random(500000) < 0.10
    bg_parts = []
    for i, wi in enumerate(s_idx):
        bg_parts.append(de50k[wi][0])
        if u_x[i]:
            bg_parts.append("X")
    bg_stream = "".join(bg_parts)
    print(f"Generated {len(bg_stream)}-char general German TS stream (X={bg_stream.count('X')/len(bg_stream)*100:.2f}%, Q={bg_stream.count('Q')/len(bg_stream)*100:.2f}%)")
    add_text(bg_stream, 1.2)

    def to_int16_table(counts):
        total = float(counts.sum())
        logp = np.log10(counts / total)
        lo = float(logp.min())
        hi = float(logp.max())
        return np.round((logp - lo) / (hi - lo) * 16000.0).astype(np.int16)

    t1_i16 = to_int16_table(c1)
    t2_i16 = to_int16_table(c2)
    t3_i16 = to_int16_table(c3)
    t4_i16 = to_int16_table(c4)

    t1_i16.tofile(f"{WORK}/hgnord_25_t1.bin")
    t2_i16.tofile(f"{WORK}/hgnord_25_t2.bin")
    t3_i16.tofile(f"{WORK}/hgnord_25_t3.bin")
    t4_i16.tofile(f"{WORK}/hgnord_25_t4.bin")
    print("Saved T1..T4. Top T1:", sorted(zip(ALPHA25, t1_i16.tolist()), key=lambda x: -x[1])[:12])

if __name__ == "__main__":
    main()
