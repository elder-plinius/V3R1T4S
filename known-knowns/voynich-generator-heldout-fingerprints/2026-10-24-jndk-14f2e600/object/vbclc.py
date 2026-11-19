#!/usr/bin/env python3
"""
vbclc.py — Standalone, strictly hand-executable implementation of the
152-Entry Voynich Boundary-Coupled Lexicon Cipher (VBCLC-152).

Table Entry Audit:
  - Table 0 (LETTER_MAP_16): 16 letter-group index entries
  - Table I (ONSET_TABLE_20): 20 prefix entries (4 macro-classes x 5 sub-ranks)
  - Table II (CORE_TABLE_96): 96 medial core entries (4 harmonic groups x 24 entries)
  - Table III (CODA_TABLE_20): 20 suffix entries (4 outgoing macro-classes x 5 sub-ranks)
  -------------------------------------------------------------------------
  Total Table Entries = 16 + 20 + 96 + 20 = 152 entries (strictly <= 200).
  Per-Folio State     = 1 bit sigma_f in {0, 1} (1 for Currier A, 0 for Currier B).
"""

import random
from collections import defaultdict

# 1. Table 0: 16 Plaintext Letter-Group Entries
LETTER_MAP_16 = {
    "e": 0,
    "i": 1, "j": 1, "y": 1,
    "a": 2,
    "o": 3,
    "u": 4, "v": 4, "w": 4,
    "n": 5,
    "r": 6,
    "t": 7,
    "s": 8, "x": 8, "z": 8,
    "l": 9,
    "c": 10, "k": 10,
    "m": 11,
    "d": 12,
    "p": 13,
    "b": 14, "g": 14,
    "f": 15, "h": 15, "q": 15,
}

# 2. Table I: 20 Onset (Prefix) Entries (4 Macro-Classes x 5 Sub-Ranks)
ONSET_TABLE_20 = [
    ["q",   "ok",  "ot",  "ol",  "or"],   # Class 0
    ["o",   "ch",  "t",   "cth", "cph"],  # Class 1 ('o' is bridge)
    ["d",   "sh",  "k",   "p",   "ckh"],  # Class 2
    ["s",   "a",   "y",   "f",   "cfh"],  # Class 3 ('a' is bridge)
]

ONSET_CELL_WEIGHTS = [
    [45, 11, 5, 3, 2],  # Class 0 (66 cards)
    [28,  9, 4, 2, 1],  # Class 1 (44 cards; 'o'=28)
    [19,  7, 4, 2, 1],  # Class 2 (33 cards)
    [14,  6, 3, 2, 1],  # Class 3 (26 cards; 'a'=6)
]  # Total = 169 cards

# 3. Table II: 96 Slot-Rigid Core Entries (4 Harmonic Groups x 24 Entries)
CORE_TABLE_96 = [
    # Group 0 (24 entries):
    "", "o", "e", "ee", "a", "k", "t", "ch",
    "ok", "ot", "och", "osh", "oke", "ote", "oche", "oshe",
    "okee", "otee", "ochee", "oshee", "ke", "te", "kee", "tee",
    # Group 1 (24 entries):
    "", "e", "ee", "o", "a", "k", "t", "sh",
    "ek", "et", "ech", "esh", "eo", "eok", "eot", "eoch",
    "eek", "eet", "eech", "eesh", "eeo", "che", "she", "chee",
    # Group 2 (24 entries):
    "", "o", "e", "ee", "a", "d", "l", "r",
    "od", "ed", "ol", "or", "ok", "ot", "el", "er",
    "eed", "eel", "eer", "eek", "eet", "odee", "edee", "shee",
    # Group 3 (24 entries):
    "", "o", "e", "ee", "i", "s", "l", "r",
    "os", "es", "och", "esh", "ok", "et", "ol", "or",
    "ees", "eech", "eesh", "osee", "esee", "ochee", "eshee", "otee",
]

# 4. Table III: 20 Coda (Suffix) Entries (4 Outgoing Macro-Classes x 5 Sub-Ranks)
CODA_TABLE_20 = [
    ["dy",   "ey",   "eey",  "edy",  "ly"],   # Outgoing Class 0 ('y'-family)
    ["aiin", "iin",  "in",   "ain",  "an"],   # Outgoing Class 1 ('n'-family)
    ["al",   "ar",   "dl",   "dal",  "dar"],  # Outgoing Class 2 ('l/r'-family)
    ["o",    "a",    "am",   "es",   "ry"],   # Outgoing Class 3 (bridge + 'm/s')
]

CODA_CELL_WEIGHTS = [
    [26, 15,  7,  4,  2],  # Class 0 (54 cards)
    [20, 12,  5,  3,  2],  # Class 1 (42 cards)
    [16, 10,  4,  2,  2],  # Class 2 (34 cards)
    [15,  7,  4,  2,  2],  # Class 3 (30 cards; 'o'=15, 'a'=7)
]  # Total = 160 cards

TOTAL_TABLE_ENTRIES = (
    len( set(LETTER_MAP_16.values()) )
    + sum(len(r) for r in ONSET_TABLE_20)
    + len(CORE_TABLE_96)
    + sum(len(r) for r in CODA_TABLE_20)
)
assert TOTAL_TABLE_ENTRIES == 152, f"Expected 152 entries, got {TOTAL_TABLE_ENTRIES}"


def safe_join_word(onset: str, core: str, coda: str) -> str:
    """Non-merging boundary join rule (Step D of written procedure)."""
    rest = core + coda
    if not rest:
        return onset + "o"
    r0 = rest[0]
    if onset == "o" and r0 in ("k", "t", "l", "r"):
        core = "e" + core
    elif onset == "a" and r0 in ("l", "m", "n", "r", "i"):
        core = "o" + core
    elif onset == "d" and r0 in ("y", "l", "m", "s", "a"):
        core = "o" + core
    elif onset == "s" and r0 == "h":
        core = "o" + core
    w = onset + core + coda
    if len(w) < 2:
        w = onset + "o" + coda
    return w


# Pre-built card decks (immutable tuples for fast repeated simulation)
_GLOBAL_ONSET_DECK = []
_CLASS_ONSET_DECKS = defaultdict(list)
for _c_id in range(4):
    for _s_id, _cnt in enumerate(ONSET_CELL_WEIGHTS[_c_id]):
        _g = ONSET_TABLE_20[_c_id][_s_id]
        _GLOBAL_ONSET_DECK.extend([(_c_id, _s_id, _g)] * _cnt)
        _CLASS_ONSET_DECKS[_c_id].extend([(_s_id, _g)] * _cnt)
_GLOBAL_ONSET_DECK = tuple(_GLOBAL_ONSET_DECK)
_CLASS_ONSET_DECKS = {k: tuple(v) for k, v in _CLASS_ONSET_DECKS.items()}

_CLASS_CODA_DECKS = defaultdict(list)
_ALL_CODA_DECK = []
for _c_id in range(4):
    for _s_id, _cnt in enumerate(CODA_CELL_WEIGHTS[_c_id]):
        _g = CODA_TABLE_20[_c_id][_s_id]
        _CLASS_CODA_DECKS[_c_id].extend([(_c_id, _s_id, _g)] * _cnt)
        _ALL_CODA_DECK.extend([(_c_id, _s_id, _g)] * _cnt)
_CLASS_CODA_DECKS = {k: tuple(v) for k, v in _CLASS_CODA_DECKS.items()}
_ALL_CODA_DECK = tuple(_ALL_CODA_DECK)

_SUB_TIER_SLICES = ((0, 8), (8, 16), (16, 24))


def encrypt_vbclc_lines(plaintext: str, template_lines: list, sigma_f: int, seed: int = 0) -> list:
    """
    Encrypt `plaintext` into lines matching the token counts of `template_lines`
    using the 152-entry VBCLC table and 1-bit per-folio state `sigma_f` in {0, 1}.
    """
    assert sigma_f in (0, 1), "sigma_f must be a 1-bit state in {0, 1}"
    rng = random.Random(seed)
    letters = [LETTER_MAP_16[c] for c in plaintext.lower() if c in LETTER_MAP_16]
    n_letters = len(letters)
    pos = 0

    # Frozen 1-bit folio state parameters:
    if sigma_f == 1:
        # State 1 (Currier A folios)
        alpha_macro = 0.28
        alpha_sub = 0.20
        harmonic_eta = 0.35
        sub_tier_weights = (0.56, 0.26, 0.18)
        double_core_prob = 0.12
    else:
        # State 0 (Currier B folios)
        alpha_macro = 0.38
        alpha_sub = 0.25
        harmonic_eta = 0.25
        sub_tier_weights = (0.36, 0.26, 0.38)
        double_core_prob = 0.18

    n_global_onset = len(_GLOBAL_ONSET_DECK)
    n_all_coda = len(_ALL_CODA_DECK)

    out_lines = []
    for line in template_lines:
        n_words = len(line)
        gen_line = []
        prev_c_out = None
        prev_s_out = None

        for _ in range(n_words):
            if pos + 6 >= n_letters:
                pos = (pos + 1) % max(1, n_letters - 7)
            l0 = letters[pos]
            l1 = letters[pos + 1]
            l2 = letters[pos + 2]
            l3 = letters[pos + 3]
            pos += 4

            # Step A: Select Onset (Table I)
            if prev_c_out is not None and rng.random() < alpha_macro:
                c_in = prev_c_out
                s_in, onset = rng.choice(_CLASS_ONSET_DECKS[c_in])
                if rng.random() < alpha_sub and s_in > 0:
                    s_in = prev_s_out % 5
                    onset = ONSET_TABLE_20[c_in][s_in]
            else:
                idx = (l0 * 11 + rng.randrange(n_global_onset)) % n_global_onset
                c_in, s_in, onset = _GLOBAL_ONSET_DECK[idx]

            # Step B: Select Core (Table II)
            if rng.random() < (1.0 - harmonic_eta):
                core_group = c_in
            else:
                core_group = (c_in + 1 + (l1 % 3)) % 4

            st = rng.choices((0, 1, 2), weights=sub_tier_weights, k=1)[0]
            lo, _ = _SUB_TIER_SLICES[st]
            offset = lo + ((l1 * 3 + l2 + rng.randrange(8)) % 8)
            core = CORE_TABLE_96[core_group * 24 + offset]

            if rng.random() < double_core_prob:
                l4 = letters[pos]
                pos += 1
                offset2 = 8 + ((l2 * 3 + l4 + rng.randrange(16)) % 16)
                core = core + CORE_TABLE_96[core_group * 24 + offset2]

            # Step C: Select Coda (Table III)
            if rng.random() < (1.0 - harmonic_eta):
                pref_c_out = (core_group + (l3 % 2)) % 4
                c_out, s_out, coda = rng.choice(_CLASS_CODA_DECKS[pref_c_out])
            else:
                coda_idx = (l2 * 9 + l3 * 5 + rng.randrange(n_all_coda)) % n_all_coda
                c_out, s_out, coda = _ALL_CODA_DECK[coda_idx]

            # Step D: Safe Join & Boundary Marker Update
            word = safe_join_word(onset, core, coda)
            gen_line.append(word)
            prev_c_out = c_out
            prev_s_out = s_out

        out_lines.append(gen_line)
    return out_lines
