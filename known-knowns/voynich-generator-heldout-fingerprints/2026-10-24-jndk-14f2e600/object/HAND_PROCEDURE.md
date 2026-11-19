# Hand-Executable Procedure & Complete 152-Entry Lookup Table (`VBCLC-152`)

## Overview
The **Voynich Boundary-Coupled Lexicon Cipher (`VBCLC-152`)** is a strictly hand-executable plaintext-driven homophonic cipher and morphological generator that converts period Latin and Italian plaintexts into Voynich EVA text line by line.
- **Total Table Entries**: **152 entries** across all tables combined ($\le 200$ maximum budget):
  - **Table 0 (Plaintext Letter-Group Index)**: 16 entries
  - **Table I (Onset / Prefix Table)**: 20 entries (organized as 4 Boundary Macro-Classes $\times$ 5 Zipf Sub-Ranks)
  - **Table II (Slot-Rigid Core / Stem Table)**: 96 entries (organized as 4 Harmonic Groups $\times$ 24 Core Syllables)
  - **Table III (Coda / Suffix Table)**: 20 entries (organized as 4 Outgoing Boundary Macro-Classes $\times$ 5 Suffixes)
- **Per-Folio State**: **1 bit** $\sigma_f \in \{0, 1\}$ per folio ($\sigma_f = 1$ on Currier A folios; $\sigma_f = 0$ on Currier B folios), which selects between two fixed card-threshold settings (Currier A compact mode vs Currier B extended mode).
- **Physical Apparatus (Hand Execution)**:
  - One printed sheet containing Tables 0, I, II, and III (152 entries total),
  - Two small homophonic card decks (or 162-card Onset deck and 147-card Coda deck, directly analogous to Greshko's 52/78-card Naibbe deck),
  - A single 4-state boundary marker (a token placed on column $0, 1, 2,$ or $3$ at the end of each word to remember the outgoing boundary class $C_{\text{out}} \in \{0, 1, 2, 3\}$ and sub-rank $s_{\text{out}} \in \{0, \dots, 4\}$, reset at the start of each new manuscript line).

---

## Complete Lookup Tables (152 Entries Total)

### Table 0: Plaintext Letter-Group Index (16 Entries)
Normalize plaintext letters (`j->i, u/w->v, k->c, x/z->s`) and look up the base-16 index $L \in \{0, \dots, 15\}$:

| Index | Letters | Index | Letters | Index | Letters | Index | Letters |
|---:|---|---:|---|---:|---|---:|---|
| **0** | `e` | **4** | `u, v, w` | **8** | `s, x, z` | **12** | `d` |
| **1** | `i, j, y` | **5** | `n` | **9** | `l` | **13** | `p` |
| **2** | `a` | **6** | `r` | **10** | `c, k` | **14** | `b, g` |
| **3** | `o` | **7** | `t` | **11** | `m` | **15** | `f, h, q` |

### Table I: Onset / Prefix Table (20 Entries, 4 Macro-Classes $\times$ 5 Sub-Ranks)
Interleaved by global Zipf rank $m = 4s + c + 1 \in \{1, \dots, 20\}$ (card multiplicity in parentheses, 169 cards total):

| Macro-Class $C_{\text{in}}$ | Sub-Rank $s=0$ | Sub-Rank $s=1$ | Sub-Rank $s=2$ | Sub-Rank $s=3$ | Sub-Rank $s=4$ |
|---|---|---|---|---|---|
| **Class 0** | `q` (45) | `ok` (11) | `ot` (5) | `ol` (3) | `or` (2) |
| **Class 1** | `o` (28, *bridge*) | `ch` (9) | `t` (4) | `cth` (2) | `cph` (1) |
| **Class 2** | `d` (19) | `sh` (7) | `k` (4) | `p` (2) | `ckh` (1) |
| **Class 3** | `s` (14) | `a` (6, *bridge*) | `y` (3) | `f` (2) | `cfh` (1) |

### Table II: Slot-Rigid Core / Stem Table (96 Entries, 4 Harmonic Groups $\times$ 24 Entries)
Each Harmonic Group $G \in \{0, 1, 2, 3\}$ is divided into three length sub-tiers: Sub-Tier 0 (`cols 0..7`, compact 0–1 char), Sub-Tier 1 (`cols 8..15`, medial 1–2 char), and Sub-Tier 2 (`cols 16..23`, `ee`-ligature 2-char):

- **Group 0 (`cols 0..23`)**:
  - `0..7`: `""`, `"o"`, `"e"`, `"ee"`, `"a"`, `"k"`, `"t"`, `"ch"`
  - `8..15`: `"ok"`, `"ot"`, `"och"`, `"osh"`, `"oke"`, `"ote"`, `"oche"`, `"oshe"`
  - `16..23`: `"okee"`, `"otee"`, `"ochee"`, `"oshee"`, `"ke"`, `"te"`, `"kee"`, `"tee"`
- **Group 1 (`cols 0..23`)**:
  - `0..7`: `""`, `"e"`, `"ee"`, `"o"`, `"a"`, `"k"`, `"t"`, `"sh"`
  - `8..15`: `"ek"`, `"et"`, `"ech"`, `"esh"`, `"eo"`, `"eok"`, `"eot"`, `"eoch"`
  - `16..23`: `"eek"`, `"eet"`, `"eech"`, `"eesh"`, `"eeo"`, `"che"`, `"she"`, `"chee"`
- **Group 2 (`cols 0..23`)**:
  - `0..7`: `""`, `"o"`, `"e"`, `"ee"`, `"a"`, `"d"`, `"l"`, `"r"`
  - `8..15`: `"od"`, `"ed"`, `"ol"`, `"or"`, `"ok"`, `"ot"`, `"el"`, `"er"`
  - `16..23`: `"eed"`, `"eel"`, `"eer"`, `"eek"`, `"eet"`, `"odee"`, `"edee"`, `"shee"`
- **Group 3 (`cols 0..23`)**:
  - `0..7`: `""`, `"o"`, `"e"`, `"ee"`, `"i"`, `"s"`, `"l"`, `"r"`
  - `8..15`: `"os"`, `"es"`, `"och"`, `"esh"`, `"ok"`, `"et"`, `"ol"`, `"or"`
  - `16..23`: `"ees"`, `"eech"`, `"eesh"`, `"osee"`, `"esee"`, `"ochee"`, `"eshee"`, `"otee"`

### Table III: Coda / Suffix Table (20 Entries, 4 Outgoing Macro-Classes $\times$ 5 Sub-Ranks)
Card multiplicity in parentheses (160 cards total):

| Outgoing Class $C_{\text{out}}$ | Sub-Rank $s=0$ | Sub-Rank $s=1$ | Sub-Rank $s=2$ | Sub-Rank $s=3$ | Sub-Rank $s=4$ |
|---|---|---|---|---|---|
| **Class 0 (`y`-family)** | `dy` (26) | `ey` (15) | `eey` (7) | `edy` (4) | `ly` (2) |
| **Class 1 (`n`-family)** | `aiin` (20) | `iin` (12) | `in` (5) | `ain` (3) | `an` (2) |
| **Class 2 (`l/r`-family)** | `al` (16) | `ar` (10) | `dl` (4) | `dal` (2) | `dar` (2) |
| **Class 3 (*bridge* + `m/s`)** | `o` (15, *bridge*) | `a` (7, *bridge*) | `am` (4) | `es` (2) | `ry` (2) |

---

## Step-by-Step Written Procedure for the Human Scribe

1. **Folio Setup**: At the top of each folio, note the 1-bit folio state $\sigma_f \in \{0, 1\}$ ($\sigma_f = 1$ for Currier A; $\sigma_f = 0$ for Currier B). At the beginning of each manuscript line, clear the boundary marker ($C_{\text{prev}} = \text{None}$).
2. **Read Plaintext Tetrad**: For the next Voynich word on the line, read the next 4 normalized plaintext letters and convert them via **Table 0** into indices $(l_0, l_1, l_2, l_3) \in \{0, \dots, 15\}^4$.
3. **Step A — Select Onset (Table I)**:
   - If $C_{\text{prev}} \ne \text{None}$ and the coupling card draw succeeds (probability $\alpha_{\text{macro}}(\sigma_f)$: $0.25$ for $\sigma_f=1$, $0.35$ for $\sigma_f=0$), set $C_{\text{in}} = C_{\text{prev}}$ and draw an onset from row $C_{\text{in}}$ of **Table I** (copying sub-rank $s_{\text{in}} = s_{\text{prev}}$ when $s_{\text{in}} > 0$ and the sub-coupling draw succeeds).
   - Otherwise, advance $11 \times l_0$ cards in the global Onset deck and read $(C_{\text{in}}, s_{\text{in}}, \text{onset})$ from **Table I**.
4. **Step B — Select Core (Table II)**:
   - Set Harmonic Group $G = C_{\text{in}}$ (or shift to $(C_{\text{in}} + 1 + (l_1 \bmod 3)) \bmod 4$ on an off-harmonic draw $\eta(\sigma_f)$).
   - Select the sub-tier $t \in \{0, 1, 2\}$ according to the folio mode $\sigma_f$, compute column $\text{col} = 8t + ((3l_1 + l_2 + d_8) \bmod 8)$, and read $\text{core} = \text{Table II}[G, \text{col}]$. On a compound-word draw, append a second syllable from `cols 8..23` of Group $G$ using a 5th plaintext letter $l_4$.
5. **Step C — Select Coda (Table III)**:
   - On a harmonic draw, set $C_{\text{out}} = (G + (l_3 \bmod 2)) \bmod 4$ and draw $(C_{\text{out}}, s_{\text{out}}, \text{coda})$ from row $C_{\text{out}}$ of **Table III**; otherwise advance $9l_2 + 5l_3$ cards in the full Coda deck.
6. **Step D — Non-Merging Boundary Join & Advance**:
   - Write $\text{word} = \text{onset} + \text{core} + \text{coda}$, inserting the buffer vowel `'e'` after onset `'o'` before `k/t/l/r` or `'o'` after onset `'a'/'d'/'s'` before `l/m/n/r/i/y/s/a/h` so the initial grapheme is never altered.
   - Update the boundary marker to $(C_{\text{prev}}, s_{\text{prev}}) \leftarrow (C_{\text{out}}, s_{\text{out}})$ and proceed to the next word on the line.
