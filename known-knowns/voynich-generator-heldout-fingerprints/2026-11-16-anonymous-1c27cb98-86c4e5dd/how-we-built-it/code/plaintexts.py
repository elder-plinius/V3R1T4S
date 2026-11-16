#!/usr/bin/env python3
"""Prepare the frozen 20-plaintext set (PREREG §4) and the line-length template.

- 10 Latin chunks: the driver's prepared Caesar (De Bello Gallico I-IV) stream, split
  into 10 contiguous chunks (L1..L10, each ~1/10 of the stream).
- 10 Italian chunks: Dante's Commedia (the Naibbe repo's own input/examples/
  divina_commedia.txt) through Greshko's clean_line pipeline (lower, de-accent,
  w->uu, j->i, k->c, v kept), split into 10 contiguous chunks (I1..I10).
- Dialect assignment (frozen in PREREG §5 for the falsifier): L1-L5, I1-I5 -> A-mode
  cells; L6-L10, I6-I10 -> B-mode cells.
- Seeded 10 (frozen): 2026111601..2026111610.
- Line template: per-P-line token counts of the fetched ZL3b-n.txt (3,950 lines),
  cycled-wrap convention of the published control (driver/PR16).

Output: output/plaintexts.json (name -> {lang, dialect, words}) + output/template.json.
"""
from __future__ import annotations
import json, os, re, sys, unicodedata, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vstats import Doc

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RUN, 'data')
OUT = os.path.join(RUN, 'output')
os.makedirs(OUT, exist_ok=True)

def greshko_clean_line(text):
    """Greshko's clean_line (naibbe.py): NFD de-accent, replacements, keep alpha,
    w->uu, j->i, k->c, lowercase."""
    normalized = unicodedata.normalize('NFD', text)
    no_diacritics = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    replacements = {'æ':'ae','Æ':'ae','œ':'oe','Œ':'oe','ð':'d','Ð':'d','þ':'th','Þ':'th',
                    'ł':'l','Ł':'l','ß':'ss','ø':'o','Ø':'o'}
    replaced = ''.join(replacements.get(c, c) for c in no_diacritics)
    cleaned = ''.join(c for c in replaced if c.isalpha()).upper()
    cleaned = cleaned.replace("W","UU").replace("J","I").replace("K","C")
    return cleaned.lower()

def caesar_stream():
    """The driver's Caesar preparation (validate_synthetics.caesar_lines):
    lowercase, de-accent, v->u, j->i, then k->c, w->uu."""
    import unicodedata as ud
    text = open(os.path.join(DATA,'voynich-units/voynich_decipherment_repro_bundle/'
                            'decipherment_attack_v6/lm_corpora/caesar_la.txt'),
                encoding='utf-8', errors='replace').read()
    # driver: attack_lib._strip_gutenberg then _deaccent; approximate faithfully:
    text = re.sub(r'^.*?(Chapter|Book)\s', '', text, flags=re.I | re.M)  # strip gutenberg headers
    norm = ud.normalize('NFD', text.lower())
    text = ''.join(c for c in norm if ud.category(c) != 'Mn')
    text = text.replace('v','u').replace('j','i')
    words = re.findall(r'[a-z]+', text)
    words = [w.replace('w','uu').replace('k','c') for w in words]
    # Naibbe alphabet is 23 letters (no v, w, k, j); strip any residue
    alphabet = set('abcdefghijklmnopqrstuvwxyz') - {'v','w','k','j'}
    words = [re.sub(r'[^' + 'abcdefghijklmnopqrstuvwxyz' + ']', '', w) for w in words]
    words = [w for w in words if w]
    return words

def dante_stream():
    text = open(os.path.join(DATA,'naibbe-cipher/input/examples/divina_commedia.txt'),
                encoding='utf-8', errors='replace').read()
    words = []
    for line in text.splitlines():
        w = greshko_clean_line(line)
        if w: words.append(w)
    alphabet = set('abcdefghijklmnopqrstuvwxyz') - {'v','w','k','j'}
    words = [re.sub(r'[^a-z]','',w) for w in words]
    return [w for w in words if w]

def chunks(words, n):
    L = len(words); size = -(-L // n)
    out = []
    for i in range(n):
        ch = words[i*size:(i+1)*size]
        if ch: out.append(ch)
    return out

def main():
    import os
    cpath = os.path.join(OUT, 'caesar_driver_words.json')
    if os.path.exists(cpath):
        lat = json.load(open(cpath))   # the pinned driver's EXACT caesar_words() output
    else:
        lat = caesar_stream()
    ita = dante_stream()
    print(f"latin words: {len(lat)}; italian words: {len(ita)}", flush=True)
    lc = chunks(lat, 10); ic = chunks(ita, 10)
    ptexts = {}
    for i, c in enumerate(lc):
        ptexts[f'L{i+1:02d}'] = {'lang':'latin','dialect':'A' if i<5 else 'B','words':c}
    for i, c in enumerate(ic):
        ptexts[f'I{i+1:02d}'] = {'lang':'italian','dialect':'A' if i<5 else 'B','words':c}
    json.dump(ptexts, open(os.path.join(OUT,'plaintexts.json'),'w'))
    # line template from fetched ZL3b (P-locus lines, token counts)
    doc = Doc(os.path.join(DATA,'ZL3b-n.txt'))
    template = [len(p['raw']) for p in doc.pages]
    json.dump({'lengths':template, 'n_lines':len(template), 'n_tokens':sum(template)},
              open(os.path.join(OUT,'template.json'),'w'))
    print(f"template: {len(template)} lines, {sum(template)} tokens, "
          f"sha256 {hashlib.sha256(json.dumps(template).encode()).hexdigest()[:16]}", flush=True)
    print("plaintexts written", flush=True)

if __name__ == '__main__':
    main()
