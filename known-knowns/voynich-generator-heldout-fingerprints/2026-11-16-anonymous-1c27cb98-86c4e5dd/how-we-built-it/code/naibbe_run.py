#!/usr/bin/env python3
"""Naibbe generator engine for lens 1/2 (PREREG §4).

Standalone re-implementation of the published Naibbe procedure (Greshko 2025,
default parameters: 52-card deck alpha20/beta8x3/gamma4x2, respacing 17/36, v1
ambiguity rule), with the pre-declared extension hooks:
  E1 edge-boost: per (prev-last-char -> next-first-letter) table multipliers on the
     next token's first-letter table draw (<=64 rows; stateless table).
  E2 hapax schedule: gamma table weights g1=g2=g (grid {4,8,16,32}), 52->(52+2*(g-4))
     cards; rest of the deck unchanged.
  E3 switch bit: one per-block bit; for ch/sh-bearing entries, restrict sampling to
     the cho-class (bit=1) or che-class (bit=0) homophone subsets (fall back to the
     full entry set if the class is empty). Blocks = 21-line template windows.
     Bit schedules: (i) Bernoulli(0.5) seeded per block, (ii) constant per mode.

Output per run: tokens (wrapped on the frozen 3,950-line template), the raw token
stream, and per-run stats used by the lens scorer.
"""
from __future__ import annotations
import json, os, random, sys, hashlib
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, 'output')
DATA = os.path.join(RUN, 'data')
TABLES = json.load(open(os.path.join(DATA, 'voynich-units/data/controls/naibbe/naibbe_tables.json')))
TEMPLATE = json.load(open(os.path.join(OUT, 'template.json')))
PTEXTS = json.load(open(os.path.join(OUT, 'plaintexts.json')))
SEEDS = [2026111601 + i for i in range(10)]
UNIP = 17.0/36.0

UNIGRAM = TABLES['unigram']; PREFIX = TABLES['prefix']; SUFFIX = TABLES['suffix']
UNIGLYPHS = {g for t in UNIGRAM.values() for g in t.values()}

# che/cho classing of a glyph string (on the collapsed-letter content)
def _che_cho(s):
    has_cho = ('cho' in s) or ('sho' in s)
    has_che = ('che' in s) or ('she' in s)
    if has_cho and not has_che: return 'cho'
    if has_che and not has_cho: return 'che'
    return 'other'

# per (state, table, letter) -> (che_set, cho_set, other_set, full_set)
CLASSSETS = {}
for _state in ('unigram', 'prefix', 'suffix'):
    _src = {'unigram': UNIGRAM, 'prefix': PREFIX, 'suffix': SUFFIX}[_state]
    for _t, _m in _src.items():
        for _l, _g in _m.items():
            k = (_state, _t, _l)
            che, cho, oth = [], [], []
            for g in _g:
                cls = _che_cho(g)
                (che if cls=='che' else cho if cls=='cho' else oth).append(g)
            CLASSSETS[k] = (che, cho, oth, list(_g))
N_TABLE_LETTER_ENTRIES = len(CLASSSETS)

def make_deck(rng, g_weight=4, edge_boost=None, edge_state=None):
    """52-card deck; gamma weight overridable (E2)."""
    spec = {'alpha':20, 'beta1':8, 'beta2':8, 'beta3':8, 'gamma1':g_weight, 'gamma2':g_weight}
    deck = [t for t,n in spec.items() for _ in range(n)]
    rng.shuffle(deck)
    deck.reverse()
    return deck, spec

def wrap_template(tokens, lengths):
    lines, i, pos = [], 0, 0
    n = len(lengths)
    while pos < len(tokens):
        L = lengths[pos % n]
        lines.append(tokens[pos:pos+L]); pos += L
    if lines and len(lines[-1]) < 2:
        lines.pop()
    return lines

def gen_run(ptext_name, seed, g_weight=4, edge_boost=None, e3_mode=None,
            e3_bit_mode=None, novel_q=None, novel_rng=None):
    """Generate one Naibbe run. Returns dict with tokens + wrapped lines + meta.

    Base path (edge_boost=None, e3_mode=None, g_weight=4) consumes the RNG exactly
    like the pinned driver's NaibbeCipher (respace pass, then 1 draw/token for
    unigrams and 2 draws/token for bigrams, ambiguity redraws consume draws) —
    verified token-identical to the driver (see lens 1/2 code checks).
    """
    words = PTEXTS[ptext_name]['words']
    letters = ''.join(words)
    rng = random.Random(seed)
    spec = {'alpha':20, 'beta1':8, 'beta2':8, 'beta3':8, 'gamma1':g_weight, 'gamma2':g_weight}
    # Lazy deck exactly like the driver: built+shuffled on first draw (AFTER respace),
    # and rebuilt+reshuffled whenever it empties.
    deck = []
    comp_w = [t for t,n in spec.items() for _ in range(n)]  # weighted list for E1
    def draw():
        if not deck:
            deck.extend(spec_t for spec_t in (t for t,n in spec.items() for _ in range(n)))
            rng.shuffle(deck); deck.reverse()
        return deck.pop()
    # E1: rows (prev_char, first_letter) -> {table: multiplier} (<=64 rows)
    def draw_first(letter, prev_last):
        if edge_boost is not None and prev_last is not None:
            rows = edge_boost.get((prev_last, letter))
            if rows:
                w = []
                for t, n in spec.items():
                    w += [t] * int(round(n * rows.get(t, 1.0)))
                if w:
                    return rng.choice(w)
        return draw()
    # E4 (PREREG.v4, generator probe only): novelty-card speciation. With prob novel_q
    # per token, emit a FRESH glyph string from the novelty deck (each string usable
    # once per run); otherwise the normal Naibbe token.
    from itertools import product as _prod
    novel_deck = []
    if novel_q is not None:
        AL = 'aceghiklmnoprstu'  # 20-letter Naibbe alphabet (from tables)
        nr = random.Random(seed ^ 0x5a17)
        seen = set()
        # build 40k distinct strings, length 4-6, shuffled order, each usable once
        while len(seen) < 40000:
            L = nr.choice([4,4,5,5,5,6,6])
            seen.add(''.join(nr.choice(AL) for _ in range(L)))
        novel_deck = list(seen)
        nr.shuffle(novel_deck)
        novel_used = set()
    tokens = []
    prev_last = None
    BLOCK = 120  # 21-line template window ~ 21*5.7 tokens
    bit_by_block = {}
    def bit_for_block(bi):
        if e3_mode is None: return None
        if e3_mode == 'bernoulli':
            if bi not in bit_by_block:
                bit_by_block[bi] = (random.Random(seed + 7919*bi).random() < 0.5)
            return bit_by_block[bi]
        return (e3_bit_mode == 'cho')
    def _glyph(state, table, letter):
        src = {'unigram': UNIGRAM, 'prefix': PREFIX, 'suffix': SUFFIX}[state]
        return src[table].get(letter)
    def _e3_excluded(glyph, b):
        cls = _che_cho(glyph)
        if b: return cls == 'che'
        return cls == 'cho'
    tok_idx = 0
    for chunk in list(_respace(letters, rng)):
        b = bit_for_block(tok_idx // BLOCK)
        if novel_q is not None and rng.random() < novel_q:
            for _ in range(20):
                if novel_deck:
                    s_nov = novel_deck.pop()
                    if s_nov not in novel_used:
                        novel_used.add(s_nov)
                        break
            else:
                s_nov = ''.join(random.Random(seed ^ tok_idx).choice('aceghiklmnoprstu') for _ in range(5))
            tokens.append(s_nov)
            prev_last = s_nov[-1]
            tok_idx += 1
            continue
        if len(chunk) == 1:
            t = draw_first(chunk, prev_last)
            g = _glyph('unigram', t, chunk)
            if b is not None and g is not None and _e3_excluded(g, b):
                for _ in range(5):  # up to 5 redraws; fallback = accept (PREREG)
                    t2b = draw()
                    g2 = _glyph('unigram', t2b, chunk)
                    if g2 is not None and not _e3_excluded(g2, b):
                        g = g2
                        break
            tokens.append(g if g is not None else chunk)
        else:
            # base path == driver v1 rule exactly (redraw BOTH draws when the
            # combined string equals any unigram glyph); E3 adds class exclusion
            # to the redraw condition (bounded fallback after 8 redraws, PREREG)
            n_tries = 0
            while True:
                t1 = draw_first(chunk[0], prev_last)
                pre = _glyph('prefix', t1, chunk[0]) or chunk[0]
                t2 = draw()
                suf = _glyph('suffix', t2, chunk[1]) or chunk[1]
                cand = pre + suf
                ok = cand not in UNIGLYPHS and (b is None or not _e3_excluded(cand, b))
                n_tries += 1
                if ok or (b is not None and n_tries >= 8):
                    tokens.append(cand)
                    break
        prev_last = tokens[-1][-1] if tokens else None
        tok_idx += 1
    lines = wrap_template(tokens, TEMPLATE['lengths'])
    return {'ptext': ptext_name, 'seed': seed, 'tokens': tokens, 'lines': lines,
            'n_tokens': len(tokens), 'spec': spec, 'g_weight': g_weight,
            'e3': e3_mode, 'sha': hashlib.sha256(' '.join(tokens).encode()).hexdigest()[:16]}

def _respace(letters, rng):
    out = []
    i = 0; n = len(letters)
    while i < n:
        if i == n-1 or rng.random() < UNIP:
            out.append(letters[i]); i += 1
        else:
            out.append(letters[i:i+2]); i += 2
    return out

def _classopts(key, bit):
    """E3: restrict options by the per-block bit (None -> full set)."""
    if bit is None:
        return CLASSSETS[key][3]
    che, cho, oth, full = CLASSSETS[key]
    if bit:  # cho-biased
        s = cho + oth
    else:    # che-biased
        s = che + oth
    return s if s else full

if __name__ == '__main__':
    # smoke test: one run, check token counts and template wrap
    r = gen_run('L01', SEEDS[0])
    print(f"L01 seed {SEEDS[0]}: {r['n_tokens']} tokens, {len(r['lines'])} lines, "
          f"mean token len {sum(len(t) for t in r['tokens'])/r['n_tokens']:.2f}, sha {r['sha']}")
    r2 = gen_run('I01', SEEDS[0], e3_mode='bernoulli')
    print(f"I01 E3-bernoulli: {r2['n_tokens']} tokens sha {r2['sha']}")
